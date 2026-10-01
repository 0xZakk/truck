#!/usr/bin/env python3
"""Coordinated front boundary conflict map; does not cut or union a candidate."""
from pathlib import Path
import sys,json,hashlib
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'cad/engine'))
import build123d as b
b.SkipClean.clean=False
from cad_metrics import solid_volume
from assembly_math import transforms
import timing_cover_front_joint_candidate as front
import timing_cover_joint_candidate as outline
import timing_cover_attachment_v2 as owners
import timing_block_axis_feature_candidate as protected
import timing_block_support_machining_candidate as journals
import water_pump_joint_candidate as pump
import oil_pan_joint_v9_candidate as pan
OUT=ROOT/'cad/engine/generated/timing-front-block-contract-research';OUT.mkdir(exist_ok=True)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def vol(s):return sum(abs(solid_volume(q,'adaptive')) for q in s.solids()) if s is not None and getattr(s,'wrapped',True) is not None else 0.
def bounds(s):
 if s is None or not s.solids():return None
 q=s.bounding_box();return [list(q.min),list(q.max)]
paths={'block':ROOT/'cad/engine/generated/timing-pump-foot-faceted-candidate/block.step'}
paths.update({k:ROOT/'cad/engine/generated/timing-cover-attachment-v2'/(k+'.step') for k in ['cover','main-gasket','future-block-land','pan-gasket','front-terminal-sealant']})
inputs={str(p.relative_to(ROOT)):sha(p) for p in paths.values()}
for mod in [front,outline,owners,protected,journals,pump,pan]:inputs[str(Path(mod.__file__).relative_to(ROOT))]=sha(Path(mod.__file__))
inputs[str(Path(__file__).relative_to(ROOT))]=sha(Path(__file__))
parts={k:b.import_step(p) for k,p in paths.items()};block=parts['block'];shared=block.intersect(parts['cover']);print('shared',vol(shared),bounds(shared),flush=True)
# Identical source tracing and bottom seat convention; no neighboring shape enters prism.
points=[front.c.yz(q,front.P) for q in outline.OUTLINE_NORMALIZED]
outer=front.face(points[:45]+[(front.RIGHT,front.PLANE),(front.RIGHT,-70),(front.LEFT,-70),(front.LEFT,front.PLANE)])
prism=front.c.extrude_x(outer,373,47)-front.c.extrude_x(front.band_profile(-150,0),372,50)
proposed=block.intersect(prism);unexplained=shared.cut(prism)
base_masks,spec=protected.protected_masks();guards={k:q for k,q in base_masks.items() if k.startswith(('main-','water-','accessory-front'))}
for i,q in journals.backing_shells().items():guards[f'cam-bearing-backing-{i}']=q
for i,(x,y,z) in enumerate(pan.STATIONS,1):
 q=b.Pos(x,y)*pan.cylinder(10 if y>0 or (x in(-371.,371.) and y!=0) else 7,z+7.6,z+25)
 guards[('retired-pan-boss-' if i in owners.RELOCATIONS else 'active-pan-boss-')+str(i)]=q
# Analytic guard extends2mm beyond known passage radius, not fabricated routing.
guards['pump-chamber-wall-guard']=pump.cx(61,357.5,376,-32,170)
guards['pump-fifth-passage-wall-guard']=pump.cx(8.5,357.5,376,pump.EXTRA[0]-32,pump.EXTRA[1]+170)
for i,(y,z) in enumerate(pump.MOUNTING,1):guards[f'pump-entire-mount-{i}']=pump.cx(10,350,373,y-32,z+170)
manifest=ROOT/'inventory/engine/full-assembly.json';inputs[str(manifest.relative_to(ROOT))]=sha(manifest);m=json.loads(manifest.read_text());poses=transforms(m);defs={q['id']:q for q in m['definitions']};occ={q['id']:q for q in m['occurrences']}
for name in ['water-pump-gasket','water-pump-housing']:
 p=ROOT/defs[occ[name]['definition']]['step'].lstrip('/');inputs[str(p.relative_to(ROOT))]=sha(p);q=poses[name]*b.import_step(p);guards['actual-'+name]=q;parts[name]=q
# Full actual gasket with2mm rear support prism provides physical face footprint.
guards['pump-gasket-rear-support']=b.Pos(-2,0,0)*parts['water-pump-gasket']
core=ROOT/'cad/engine/generated/timing-thrust-land-candidate'
for name in ['cam-thrust-plate','cam-thrust-bolt-1','cam-thrust-bolt-2','cam-thrust-washer-1','cam-thrust-washer-2','cam-gear-spacer','camshaft','crank-timing-gear','cam-timing-gear']:
 p=core/(name+'.step');inputs[str(p.relative_to(ROOT))]=sha(p);q=b.import_step(p);guards['actual-'+name]=q;parts[name]=q
# Actual retention-seat backing probes around translated source bolt and plate interfaces.
for name in ['future-block-land','main-gasket','pan-gasket','front-terminal-sealant']:guards[name]=parts[name]
rows=[]
for name,q in guards.items():
 hit=proposed.intersect(q);coverhit=shared.intersect(q)
 row={'name':name,'proposed_material_in_guard_mm3':vol(hit),'proposed_intersection_bounds_mm':bounds(hit),'existing_block_cover_overlap_in_guard_mm3':vol(coverhit),'minimum_proposed_distance_mm':proposed.distance_to(q),'protected_unchanged':vol(hit)<1e-5};rows.append(row)
 if vol(hit)>1e-5 or vol(coverhit)>1e-5:print(row,flush=True)
bands=[]
for lo,hi in [(-500,363),(363,365),(365,373),(373,373.8),(373.8,378.009375),(378.009375,381),(381,420)]:
 q=shared.intersect(b.Pos((lo+hi)/2,0,0)*b.Box(hi-lo,1000,1000));bands.append({'x_mm':[lo,hi],'overlap_mm3':vol(q),'bounds_mm':bounds(q)})
for name,q in [('existing-shared-cover-material',shared),('source-dry-prism',prism),('proposed-material-region',proposed),('overlap-outside-proposal',unexplained)]:
 if q.solids():b.export_step(q,OUT/(name+'.step'))
sections={}
for x in [366,372,374,380.5]:
 rows2={}
 for name in ['block','cover','main-gasket','future-block-land','pan-gasket','water-pump-gasket','cam-thrust-plate']:
  rows2[name]=[[list(e.position_at(i/100))[1:] for i in range(101)] for e in b.section(parts[name],section_by=b.Plane.YZ.offset(x)).edges()]
 rows2['analytic dry prism']=[[list(e.position_at(i/100))[1:] for i in range(101)] for e in b.section(prism,section_by=b.Plane.YZ.offset(x)).edges()]
 sections[str(x)]=rows2
(OUT/'sections.json').write_text(json.dumps(sections))
r={'status':'RESEARCH ONLY; candidate NOT BUILT','input_sha256':inputs,'overlap_mm3':vol(shared),'overlap_bounds_mm':bounds(shared),'axial_overlap_bands':bands,'source_analytic_region':{'seat_x_mm':373,'front_limit_mm':420,'source':'timing_cover_front_joint_candidate source-outline outer profile and analytic lower-seat band','estimate':True},'proposed_material_volume_mm3':vol(proposed),'proposed_material_bounds_mm':bounds(proposed),'overlap_remaining_outside_proposal_mm3':vol(unexplained),'remaining_overlap_bounds_mm':bounds(unexplained),'guards':rows,'limits':['No candidate created; source-defined diagnostic region only','Broad chamber guard includesfluidvoid andsupport; actualmaterial overlap reported','Retiredpanstations remain geometry until explicitlycoordinated','No production wall or flow approval','Actual cam/core surface probes do not by themselves prove backing strength'],'artifacts':{p.name:sha(p) for p in OUT.glob('*') if p.suffix in ['.step','.json']}}
assert inputs=={p:sha(ROOT/p) for p in inputs}
(ROOT/'inventory/engine/timing-front-block-contract-research.json').write_text(json.dumps(r,indent=2)+'\n');print('done',r['proposed_material_volume_mm3'],r['overlap_remaining_outside_proposal_mm3'],flush=True)
