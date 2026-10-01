#!/usr/bin/env python3
from pathlib import Path
import sys,json,hashlib,math
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'cad/engine'))
import build123d as b
from cad_metrics import solid_volume
from assembly_math import transforms
import front_seal_2692_candidate as c
OUT=ROOT/'cad/engine/generated/front-seal-2692-candidate';OUT.mkdir(parents=True,exist_ok=True);REPORT=ROOT/'inventory/engine/front-seal-2692-candidate-validation.json'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def vol(q):return sum(abs(solid_volume(s,'adaptive')) for s in q.solids()) if q else 0.
def comp(q):return b.Compound(children=list(q.solids()))
m=json.loads((ROOT/'inventory/engine/full-assembly.json').read_text());defs={d['id']:d for d in m['definitions']};frames=transforms(m)
paths={k:ROOT/defs[k]['step'].lstrip('/') for k in ['damper-hub','damper-key','damper-bolt','damper-washer','crankshaft']}
paths.update({'cover':ROOT/'cad/engine/generated/timing-cover-attachment-v2/cover.step','block':ROOT/'cad/engine/generated/timing-front-block-adapter-candidate/block.step','block-land':ROOT/'cad/engine/generated/timing-cover-attachment-v2/future-block-land.step','pan':ROOT/'cad/engine/generated/timing-pan-dry-neck-candidate/pan.step','pan-gasket':ROOT/'cad/engine/generated/timing-cover-attachment-v2/pan-gasket.step','crank-gear':ROOT/'cad/engine/generated/timing-thrust-land-candidate/crank-timing-gear.step'})
watch=[Path(__file__),Path(c.__file__),Path(c.e.__file__),ROOT/'cad/engine/cad_metrics.py',ROOT/'cad/engine/assembly_math.py',ROOT/'reference/engine/front-crank-seal-envelope-review.json',ROOT/'inventory/engine/full-assembly.json']+list(paths.values())
r={'status':'RUNNING','inputs':{str(p.relative_to(ROOT)):sha(p) for p in watch},'exports':{},'interfaces':{},'neighbors':[],'failures':[]}
def save():REPORT.write_text(json.dumps(r,indent=2)+'\n')
old={k:(frames[k]*b.import_step(p) if k in frames else b.import_step(p)) for k,p in paths.items()};save()
q={'cover':c.cover_adapter(old['cover']),'damper-hub':c.hub_adapter(old['damper-hub']),'seal-case-installed':c.case(),'seal-case-free':c.case(True),'seal-elastomer':c.elastomer()}
print('case elastomer cover hub built',flush=True);save()
q['seal-garter-spring']=c.spring();print('spring built',q['seal-garter-spring'].is_valid,len(q['seal-garter-spring'].solids()),flush=True)
for key,mask in [('cover',c.cover_mask()),('damper-hub',c.hub_mask())]:
 added=q[key].cut(old[key]);removed=old[key].cut(q[key]);a=vol(added);z=vol(removed)
 r[key+'_change']={'added_mm3':a,'removed_mm3':z,'added_outside_mask_mm3':vol(comp(added).cut(mask)) if a>1e-8 else 0.,'removed_outside_mask_mm3':vol(comp(removed).cut(mask)) if z>1e-8 else 0.}
 assert max(r[key+'_change']['added_outside_mask_mm3'],r[key+'_change']['removed_outside_mask_mm3'])<1e-5
for key,s in q.items():
 assert s.is_valid and len(s.solids())==1,(key,s.is_valid,len(s.solids()))
 path=OUT/(key+'.step');b.export_step(s,path);again=b.import_step(path);assert again.is_valid and len(again.solids())==1
 # Spring spline volume uses the same strict adaptive metric as other solids.
 error=abs(vol(s)-vol(again));assert error<.01,(key,error)
 r['exports'][key]={'sha256':sha(path),'volume_mm3':vol(again),'roundtrip_volume_error_mm3':error,'bounds_mm':[list(again.bounding_box().min),list(again.bounding_box().max)]};q[key]=again
save();print('exports done',flush=True)
# Positive support bands at flange and rear shoulder, not distance-only contacts.
for name,x,ri,ro,owner in [('flange-cover',c.SEAT-.005,c.BORE_R+.05,c.FLANGE_R-.05,'cover'),('flange-case',c.SEAT+.005,c.BORE_R+.05,c.FLANGE_R-.05,'seal-case-installed'),('rear-shoulder-cover',c.REAR-.005,28.5,c.BORE_R-.05,'cover'),('rear-case',c.REAR+.005,28.5,c.BORE_R-.05,'seal-case-installed')]:
 probe=c.ring(ro,ri,x-.005,x+.005);missing=vol(probe.cut(q[owner]));r['interfaces'][name]={'probe_mm3':vol(probe),'missing_mm3':missing};assert missing<1e-5
for a,z in [('seal-case-installed','cover'),('seal-elastomer','seal-case-installed'),('seal-elastomer','damper-hub'),('seal-garter-spring','seal-elastomer')]:
 gap=q[a].distance_to(q[z]);v=vol(q[a].intersect(q[z]));r['interfaces'][a+'__'+z]={'gap_mm':gap,'overlap_mm3':v}
 if gap>.002 or v>.1:r['failures'].append({'interface':[a,z],'gap':gap,'overlap':v})
save();print('interfaces done',flush=True)
# Exclude intentional free-case nominal press-fit from physical collision gates.
r['nominal_fit']={'free_OD_mm':c.e.CASE_DIAMETER,'installed_OD_mm':c.e.HOUSING_BORE,'diametral_difference_mm':c.e.CASE_DIAMETER-c.e.HOUSING_BORE,'free_case_cover_overlap_mm3':vol(q['seal-case-free'].intersect(q['cover'])),'classification':'Intentional nominal press allowance; not a manufacturing tolerance or accidental collision'}
for key in ['cover','damper-hub','seal-case-installed','seal-elastomer','seal-garter-spring']:
 for name,s in old.items():
  if name in ['cover','damper-hub']:continue
  aa,zz=q[key].bounding_box(),s.bounding_box()
  alo,ahi,zlo,zhi=map(list,[aa.min,aa.max,zz.min,zz.max])
  if not all(min(ahi[i],zhi[i])-max(alo[i],zlo[i])>1e-7 for i in range(3)):
   r['neighbors'].append({'candidate':key,'neighbor':name,'method':'continuous axis-aligned bound separation','candidate_bounds_mm':[alo,ahi],'neighbor_bounds_mm':[zlo,zhi]});continue
  v=vol(q[key].intersect(s));row={'candidate':key,'neighbor':name,'overlap_mm3':v};r['neighbors'].append(row)
  if v>.1:r['failures'].append(row)
# Fault: move lip behind hub; support ring above any case front must be unsupported.
r['negative_controls']={'lip_back20_hub_gap_mm':(b.Pos(-20,0,0)*q['seal-elastomer']).distance_to(q['damper-hub']),'flange_front1_missing_mm3':vol(c.ring(c.FLANGE_R-.05,c.BORE_R+.05,c.SEAT+.995,c.SEAT+1.005).cut(q['cover']))}
assert r['negative_controls']['lip_back20_hub_gap_mm']>1 and r['negative_controls']['flange_front1_missing_mm3']>1
assert all(sha(ROOT/p)==h for p,h in r['inputs'].items())
r['status']='FAIL candidate interface or neighbor gates' if r['failures'] else 'PASS scoped nominal-installed seal/cover/hub candidate; not production or installation acceptance'
r['limits']=['Lip/spring/case internals, absolute seat and boss contour are estimates; no force/deformation/tolerance claim.','Garter96 turns/.12wire/.45winding are illustrative; actual join/preload unknown.','Clockwise micro-spiral texture, crank endplay, actual hub bore/strength, disassembly and browser NOT RUN.','Free-case nominal interference intentionally retained separately.']
save();print(r['status'])
