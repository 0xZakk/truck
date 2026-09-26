#!/usr/bin/env python3
"""Bind staged/installed rotor-only solids, frames, motion, lessons and replay."""
from pathlib import Path
import argparse,copy,hashlib,importlib.util,json,sys,itertools
import build123d as b,numpy as np,trimesh
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'cad/engine'))
import distributor_center_contact_integration as adapter
import distributor_center_contact_candidate as candidate
from assembly_math import transforms
STAGE=ROOT/'cad/engine/generated/distributor-center-contact-integration-stage'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p):return json.loads(p.read_text())
def helper():
 spec=importlib.util.spec_from_file_location('rotor_install_helper',ROOT/'scripts/install-distributor-center-contact.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m

def replay(m,shapes,partial=False):
 data=copy.deepcopy(m);old={d['id']:d for d in data['definitions']};work=dict(shapes)
 if partial:work.update(candidate.baseline_parts())
 def define(i,s,n,f,system,color,sources,gaps,claims,prepared=False):
  assert prepared
  row=copy.deepcopy(old[i]);row.update(name=n,function=f,system=system,color=color,sources=sources,unresolved=gaps,dimension_claims=claims)
  data['definitions'].append(row);work[i]=s
 def add(i,d,p,pos=(0,0,0),explode=(0,0,0),rotation=(0,0,0),name=None):
  row=next(x for x in data['definitions'] if x['id']==d);data['occurrences'].append(dict(id=i,definition=d,parent=p,name=name or row['name'],function=row['function'],position_cad_mm=list(pos),rotation_cad_deg=list(rotation),explode_cad_mm=list(explode)))
 def group(*a,**k):raise AssertionError('No new groups')
 adapter.install(define,add,group,data['definitions'],data['occurrences'],data['assemblies'],work)
 for key in ('definitions','occurrences','assemblies'):
  assert len(data[key])==len({r['id'] for r in data[key]})
  assert {r['id']:r for r in data[key]}=={r['id']:r for r in m[key]},'Replay metadata '+key
 return {i:adapter.difference(work[i],shapes[i]) for i in adapter.IDS}

def contact_area(a,z):
 total=0.
 for f in a.faces():
  if f.geom_type!=b.GeomType.PLANE:continue
  for g in z.faces():
   if g.geom_type!=b.GeomType.PLANE or f.distance_to(g)>1e-6:continue
   patch=f.intersect(g)
   if patch:total+=patch.area
 return total

def validate(installed=False,stage_dir=STAGE):
 out=Path(stage_dir);recordpath=ROOT/'inventory/engine/distributor-center-contact-installation.json' if installed else out/'installation.json';record=read(recordpath);h=helper()
 mp=ROOT/'inventory/engine/full-assembly.json' if installed else out/'full-assembly.json';raw=mp.read_bytes();m=json.loads(raw)
 if not installed:assert sha(mp)==record['staged_manifest_sha256']
 assert h.scope(m)==record['installed_scope'],'Installed distributor scope changed'
 assert h.scene_frames(m)==record['scene_frames'],'Static scene frames changed; re-audit neighbors'
 assert sha(h.PROOF)==record['candidate_report_sha256']
 for p,value in record['source_sha256'].items():assert sha(ROOT/p)==value,'Changed rotor source '+p
 assert sha(h.HELPER)==record['transaction_helper_sha256']
 hashes={}
 def track(p):hashes[str(p.relative_to(ROOT))]=sha(p);return p
 ds={d['id']:d for d in m['definitions']};os={o['id']:o for o in m['occurrences']};parts={}
 for oid in record['installed_scope']['occurrences']:
  definition=ds[os[oid]['definition']];p=out/'step'/(definition['id']+'.step') if definition['id'] in adapter.IDS and not installed else ROOT/definition['step'].lstrip('/')
  parts[oid]=b.import_step(track(p))
 expected=candidate.parts();geometry={};exports={}
 for i in adapter.IDS:
  error=adapter.difference(parts[i],expected[i]);assert error<.01,(i,error);geometry[i]=error
  sp=ROOT/ds[i]['step'].lstrip('/') if installed else out/'step'/(i+'.step');gp=ROOT/ds[i]['glb'].lstrip('/') if installed else out/'models'/(i+'.glb')
  declared=record['canonical_artifact_sha256'] if installed else record['staged_artifact_sha256']
  for path in (sp,gp):assert sha(track(path))==declared[str(path.relative_to(ROOT if installed else out))]
  mesh=trimesh.load(gp,force='mesh');mesh.merge_vertices(digits_vertex=8);assert mesh.is_watertight and mesh.nondegenerate_faces().all() and mesh.unique_faces().all()
  v=np.asarray(mesh.vertices)[:,[0,2,1]]*np.array([1,-1,1])*1000;box=parts[i].bounding_box();err=float(np.max(abs(np.array([v.min(0),v.max(0)])-np.array([tuple(box.min),tuple(box.max)]))))
  assert err<.02 and parts[i].is_valid and len(parts[i].solids())==1
  assert np.max(abs(np.array(tuple(box.size))-np.array(ds[i]['model_bounds_mm'])))<.01
  exports[i]=dict(bounds_error_mm=err,watertight=True)
 # Exact installed witness versus baseline/integration stage binds cap brush
 # and the unchanged shaft/tip envelope without claiming hidden construction.
 baseline=candidate.baseline_parts();protected={}
 for name,i,region in [('shaft_seat','distributor-rotor',b.Pos(0,0,119)*b.Box(50,50,22)),('outer_tip','distributor-rotor-contact',b.Pos(30,0,134)*b.Box(6,20,8))]:
  protected[name]=adapter.difference(parts[i]&region,baseline[i]&region);assert protected[name]<.01
 leaf=parts[adapter.NEW];contacts={}
 for name,a,z in [('center',leaf,parts['distributor-center-contact']),('outer',leaf,parts['distributor-rotor-contact']),('leaf_seat',leaf,parts['distributor-rotor']),('outer_seat',parts['distributor-rotor-contact'],parts['distributor-rotor'])]:
  contacts[name]=dict(distance_mm=a.distance_to(z),overlap_mm3=adapter.volume(a&z),planar_contact_area_mm2=contact_area(a,z));assert contacts[name]['distance_mm']<1e-5 and contacts[name]['overlap_mm3']<.1 and contacts[name]['planar_contact_area_mm2']>1
 failures=[];pairs=0;gap=0.
 for crank in range(0,721,20):
  poses=transforms(m,crank);ref=poses['distributor-cap'].inverse();placed={i:ref*poses[i]*s for i,s in parts.items()}
  gap=max(gap,placed[adapter.NEW].distance_to(placed['distributor-center-contact']))
  for a,z in itertools.combinations(placed,2):
   if not ({a,z}&adapter.IDS):continue
   ba,bz=placed[a].bounding_box(),placed[z].bounding_box()
   if any(min(getattr(ba.max,k),getattr(bz.max,k))-max(getattr(ba.min,k),getattr(bz.min,k))<1e-6 for k in 'XYZ'):continue
   pairs+=1;v=adapter.volume(placed[a]&placed[z])
   if v>.1:failures.append(dict(crank_deg=crank,a=a,b=z,overlap_mm3=v))
 assert not failures and gap<1e-5
 capids=['distributor-cap','distributor-center-contact','distributor-coil-terminal']+[f'distributor-terminal-{i}' for i in range(1,7)]
 removal=max(adapter.volume((b.Pos(0,0,dz)*parts[cap])&parts[i]) for dz in (0,.1,.5,1,2,5,10,20,40,80) for cap in capids for i in adapter.IDS);assert removal<.1
 ordinary=replay(m,parts);partial=replay(m,parts,True);assert max(ordinary.values())<.01 and max(partial.values())<.01
 moved=copy.deepcopy(m);a=next(x for x in moved['assemblies'] if x['id']=='distributor-assembly');a['position_cad_mm'][0]+=20;a.setdefault('rotation_cad_deg',[0,0,0])[2]+=13
 rigid=replay(moved,parts);assert max(rigid.values())<.01
 bad=copy.deepcopy(m);next(o for o in bad['occurrences'] if o['id']==adapter.NEW)['position_cad_mm'][0]+=.25
 frame_rejected=False
 try:replay(bad,parts)
 except ValueError as e:frame_rejected='relative frame' in str(e)
 assert frame_rejected
 bad_shapes=dict(parts);bad_shapes['distributor-rotor']=b.Pos(0,0,.25)*bad_shapes['distributor-rotor'];shape_rejected=False
 try:replay(m,bad_shapes)
 except ValueError as e:shape_rejected='geometry' in str(e)
 assert shape_rejected
 lessons=read(ROOT/'inventory/engine/distributor-center-contact-learning.json')
 for i,lesson in lessons.items():
  assert i in ds and set(lesson['sources'])<=set(m['sources'])
  for section in ('steps','troubleshooting'):
   for item in lesson.get(section,[]):assert 'part' not in item or item['part'] in os
 assert m['sources'][adapter.SOURCE]==adapter.sources()[adapter.SOURCE]
 # Global static stage context remains bound; changed assets use installed hashes.
 for p,value in record['neighbor_sha256'].items():
  wanted=record['canonical_artifact_sha256'].get(p,value) if installed else value
  assert sha(track(ROOT/p))==wanted,'Static neighbor changed '+p
 assert mp.read_bytes()==raw and all(sha(ROOT/p)==v for p,v in hashes.items())
 return dict(status='PASS installed rotor-only binding; browser acceptance pending' if installed else 'PASS staged rotor-only binding',manifest_sha256=sha(mp),installation_record_sha256=sha(recordpath),geometry_difference_mm3=geometry,exports=exports,protected_difference_mm3=protected,contacts=contacts,motion=dict(crank_samples=37,exact_pairs=pairs,maximum_center_gap_mm=gap,failures=failures),cap_withdrawal_maximum_overlap_mm3=removal,replay=dict(repeat_difference_mm3=ordinary,partial_refresh_difference_mm3=partial,rigid_group_move_difference_mm3=rigid,changed_relative_frame_rejected=frame_rejected,changed_geometry_rejected=shape_rejected),learning_valid=True,input_sha256=hashes,input_guard_pass=True,limits=adapter.GAPS)

def main():
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--installed',action='store_true');args=p.parse_args();result=validate(args.installed);dest=ROOT/'inventory/engine/distributor-center-contact-installed-validation.json' if args.installed else STAGE/'validation.json';dest.write_text(json.dumps(result,indent=2)+'\n');print(result['status'])
if __name__=='__main__':main()
