"""Exact broad-failure bounds and additional actual access/isolation evidence."""
from pathlib import Path
import sys,json,hashlib
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'cad/engine'))
import build123d as b
from OCP.BRepGProp import BRepGProp
from OCP.GProp import GProp_GProps
import timing_cover_seven_fastener_candidate as c
import timing_cover_attachment_v2 as owner
from assembly_math import transforms
OUT=ROOT/'cad/engine/generated/timing-seven-block-guard-study';newpath=ROOT/'cad/engine/generated/timing-cover-seven-fastener-candidate/block.step';block=b.import_step(newpath);paths=[newpath,Path(__file__)];witnesses={};sections={}
def vol(s):
 if s is None:return 0.
 if isinstance(s,b.ShapeList):return sum(vol(t)for t in s)
 v=0.
 for t in s.solids():
  q=GProp_GProps();e=BRepGProp.VolumeProperties_s(t.wrapped,q,1e-9,True,False);assert e<=1e-7,e;v+=abs(q.Mass())
 return v
for p in OUT.glob('*.step'):
 s=b.import_step(p);paths.append(p);bb=s.bounding_box();witnesses[p.stem]={'bounds_mm':[list(bb.min),list(bb.max)],'volume_mm3':vol(s)};sec=b.section(s,b.Plane.YZ.offset(365.5));sections[p.stem]=[[list(e.position_at(i/60))for i in range(61)]for e in sec.edges()]
(OUT/'failure-sections.json').write_text(json.dumps(sections))
loc=b.Pos(*owner.RELOCATIONS[20]);tool=loc*owner.cz(17.526/2,-138.26,0);washerpath=ROOT/'cad/engine/generated/pan-fastener-thread-candidate/existing-pan-washer.step';paths.append(washerpath);washer=loc*b.import_step(washerpath)
access={'pan20_actual_washer_overlap_mm3':vol(block.intersect(washer)),'pan20_nominal_tool_overlap_mm3':vol(block.intersect(tool)),'pan20_nominal_tool_distance_mm':tool.distance_to(block)}
manifest=ROOT/'inventory/engine/full-assembly.json';paths.append(manifest);man=json.loads(manifest.read_text());poses=transforms(man);defs={x['id']:x for x in man['definitions']};occ={x['id']:x for x in man['occurrences']};pumprows=[]
for i in range(1,5):
 name=f'water-pump-mounting-screw-{i}';p=ROOT/defs[occ[name]['definition']]['step'].lstrip('/');paths.append(p);s=poses[name]*b.import_step(p);bb=s.bounding_box();pumprows.append({'id':name,'actual_screw_block_overlap_mm3':vol(block.intersect(s)),'actual_screw_x_bounds_mm':[bb.min.X,bb.max.X],'support_front_x_mm':373,'axial_front_approach_separation_from_new_support_mm':bb.max.X-373,'limit':'Unknown production socket outerdiameter; only forward half-space from actual head has disjointX support proof. Not a complete pump service tool test.'})
r={'broad_failure_witnesses':witnesses,'pan20_access':access,'pump_actual_hardware':pumprows,'guard_origins':{'water-pump-front-interface':'timing_block_axis_feature_candidate.protected_masks: radius85,centerX365/Y-32/Z170,width20. Declared fixed-interface neighborhood from migration study; not measured pump fluid passage. It conservatively encloses flange/mount surroundings.','active-pan-interface-20':'Inherited V3 guard: R12 vertical atX365.5/Y-132/Z-24.5..-7.1, encompassing R10estimatedsocket support plus surrounding stock. Not a source-defined required minimumwall.'},'dry_wet_interpretation':'Seven main blind cavities have completeR4.17..6.2 annularwalls and2mmrear caps, so new holes do not open through those modeled wet-side boundaries. Pan20 completefunctionalR6.2neighborhood, femaleandfloor unchanged. Pumpchamber/fifthactualdeclaredspaces unchanged andempty. Unknown deepercoolant routing/otheroil passages remain unverified; broadstockchange is not automatically acceptable.','input_sha256':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest()for p in paths}};(ROOT/'inventory/engine/timing-seven-block-guard-localization.json').write_text(json.dumps(r,indent=2)+'\n');print(r)
