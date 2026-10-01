from pathlib import Path
import sys,json,hashlib
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'cad/engine'))
import build123d as b
b.SkipClean.clean=False
import timing_front_block_contract as contract
import timing_block_axis_feature_candidate as masks
import timing_block_support_machining_candidate as journals
import timing_cover_attachment_v2 as owners
import water_pump_joint_candidate as pump
import oil_pan_joint_v9_candidate as pan
from cad_metrics import solid_volume
OUT=ROOT/'cad/engine/generated/timing-front-block-contract-research'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def vol(q):return sum(abs(solid_volume(s,'adaptive')) for s in q.solids()) if q is not None and getattr(q,'wrapped',True) is not None else 0.
def bounds(s):
 if s is None or not s.solids():return None
 q=s.bounding_box();return [list(q.min),list(q.max)]
proof=ROOT/'inventory/engine/timing-front-block-contract-research.json';inputs=json.loads(proof.read_text())['input_sha256'];assert inputs=={p:sha(ROOT/p) for p in inputs};inputs[str(proof.relative_to(ROOT))]=sha(proof)
for p in [Path(__file__),Path(contract.__file__)]:inputs[str(p.relative_to(ROOT))]=sha(p)
block=b.import_step(ROOT/'cad/engine/generated/timing-pump-foot-faceted-candidate/block.step');shared=b.import_step(OUT/'existing-shared-cover-material.step');regions=contract.proposed_regions()
guards,_=masks.protected_masks();guards={k:v for k,v in guards.items() if k.startswith(('main-','water-','accessory-front'))}
for i,v in journals.backing_shells().items():guards[f'cam-bearing-backing-{i}']=v
for i,(x,y,z) in enumerate(pan.STATIONS,1):guards[('retired-pan-boss-' if i in owners.RELOCATIONS else 'active-pan-boss-')+str(i)]=b.Pos(x,y)*pan.cylinder(10 if y>0 or(x in(-371.,371.) and y!=0) else 7,z+7.6,z+25)
for i,(y,z) in enumerate(pump.MOUNTING,1):guards[f'pump-entire-mount-{i}']=pump.cx(10,350,373,y-32,z+170)
guards['pump-chamber-wall-guard']=pump.cx(61,357.5,376,-32,170);guards['pump-fifth-passage-wall-guard']=pump.cx(8.5,357.5,376,pump.EXTRA[0]-32,pump.EXTRA[1]+170)
for name in ['future-block-land','main-gasket','pan-gasket','front-terminal-sealant']:guards[name]=b.import_step(ROOT/'cad/engine/generated/timing-cover-attachment-v2'/(name+'.step'))
# Retention backing: source plate bearing footprint and blind screw axes.
import cam_retention as retention
frame=b.Pos(*journals.DELTA)*retention.MOUNT
guards['cam-thrust-seat-backing']=frame*(b.Pos(0,0,-2)*retention.plate_shape())
for i,x in enumerate(retention.BOLT_STATIONS,1):guards[f'cam-thrust-socket-wall-{i}']=frame*(b.Pos(x,0,-6)*b.Cylinder(6.05,12.2))
old_pan_support=pan.low_half(pan.x_cylinder(59.4,365,381)-pan.x_cylinder(42,364,382))
retired=b.Compound(children=[v for k,v in guards.items() if k.startswith('retired-pan')]+[old_pan_support])
rows=[]
for name,region in regions.items():
 material=block.intersect(region);checks=[]
 for label,q in guards.items():
  hit=material.intersect(q);checks.append({'name':label,'removed_mm3':vol(hit),'unchanged':vol(hit)<1e-5})
 row={'region':name,'material_mm3':vol(material),'bounds_mm':bounds(material),'cover_overlap_contained_mm3':vol(shared.intersect(region)),'material_outside_retired_pan_additions_mm3':vol(material.cut(retired)),'guards':checks};rows.append(row);print(name,{k:v for k,v in row.items() if k!='guards'},flush=True)
 for v in checks:
  if not v['unchanged']:print('guard',v,flush=True)
 if material.solids():b.export_step(material,OUT/(name+'-material.step'))
combinations={}
for label,add in [('main-plus-upper-band',regions['source-upper-band-supplement']),('main-plus-lower-step',regions['stepped-lower-region'])]:
 remaining=shared.cut(regions['main-plane-only']).cut(add);combinations[label]={'remaining_cover_overlap_mm3':vol(remaining),'bounds_mm':bounds(remaining)}
r={'status':'RESEARCH ONLY; no candidate cut','input_sha256':inputs,'boundary_mm':{'main':373,'lower':365,'lower_step_top_z':contract.STEP_TOP},'regions':rows,'combinations':combinations,'limits':['Functional source-boundary masks, not neighboring part subtraction','Cam-thrust backing/socket probes added before any construction','Retiredpan material provenance is additive-source envelope only; outside volume identifies original lowerfrontweb needing explicit adaptation','No activepart changed; no production or installed acceptance']}
assert inputs=={p:sha(ROOT/p) for p in inputs};(ROOT/'inventory/engine/timing-front-block-step-research.json').write_text(json.dumps(r,indent=2)+'\n');print(combinations,flush=True)
