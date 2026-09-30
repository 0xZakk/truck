#!/usr/bin/env python3
"""Independent pair diagnostics; unchanged engine mismatch is reported, not hidden."""
from pathlib import Path
import sys,json,hashlib,math
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'cad/engine'))
import build123d as b
import numpy as np
import trimesh
import timing_gear_pair_candidate as c
from cad_metrics import solid_volume
from assembly_math import transforms
OUT=ROOT/'cad/engine/generated/timing-gear-pair-candidate';OUT.mkdir(parents=True,exist_ok=True)
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def vol(q):return sum(abs(solid_volume(s,'adaptive')) for s in q.solids()) if q else 0.
inputs={str(p.relative_to(ROOT)):sha(p) for p in [Path(__file__),Path(c.__file__),ROOT/'cad/engine/cam_retention.py',ROOT/'cad/engine/cad_metrics.py',ROOT/'cad/engine/assembly_math.py',ROOT/'reference/engine/timing-gear-evidence-review.json',ROOT/'inventory/engine/timing-gear-evidence-validation.json',ROOT/'inventory/engine/full-assembly.json']}
parts=c.parts();exports={};preview={}
for key,q in parts.items():
 sp=OUT/(key+'.step');b.export_step(q,sp);actual=b.import_step(sp);assert actual.is_valid and len(actual.solids())==1
 v,f=q.tessellate(.05,.1);mesh=trimesh.Trimesh(np.array([tuple(x) for x in v])[:,[0,2,1]]*[1,1,-1]/1000,np.asarray(f));mesh.update_faces(mesh.nondegenerate_faces());mesh.update_faces(mesh.unique_faces());mesh.remove_unreferenced_vertices();gp=OUT/(key+'.glb');mesh.export(gp)
 assert mesh.is_watertight
 exports[key]=dict(step_sha256=sha(sp),glb_sha256=sha(gp),valid=True,solids=1,watertight=True,step_volume_error_mm3=abs(vol(q)-vol(actual)),triangles=len(mesh.faces));parts[key]=actual
print('Exports valid; starting engagement diagnostics',flush=True)
# For parallel axes, every solid overlap lies in the intersection of tip
# cylinders. In the centerline/perpendicular frame the lens lies inside
# u=[center-Rcam,Rcrank], |v|<=sqrt(Rcrank²-u_chord²).
r1=c.PARAMS['crank_tip_diameter_mm']/2;r2=c.PARAMS['cam_tip_diameter_mm']/2
chord=(r1*r1-r2*r2+c.CENTER*c.CENTER)/(2*c.CENTER);lens_half=math.sqrt(r1*r1-chord*chord)
assert c.CENTER-r2>33.6 and r1<47.6 and lens_half<22
region=b.Pos(0,40.6*math.cos(c.AXIS_ANGLE),40.6*math.sin(c.AXIS_ANGLE))*b.Rot(math.degrees(c.AXIS_ANGLE),0,0)*b.Box(16,14,44)
def pair_overlap(a,z):return vol(a.intersect(region).intersect(z.intersect(region)))
poses=np.linspace(0,360/c.PARAMS['crank_teeth'],25);sweep=[]
for angle in poses:
 q=c.posed(parts,float(angle));a=b.Compound(children=list(q['crank'].intersect(region).solids()));z=b.Compound(children=list(q['cam'].intersect(region).solids()));overlap=vol(a.intersect(z));distance=a.distance_to(z);sweep.append(dict(crank_angle_deg=float(angle),cam_angle_deg=-float(angle)/2,overlap_mm3=overlap,engagement_region_surface_gap_mm=distance));print(sweep[-1],flush=True)
# These deliberate incompatible phases and old-axis placement must not pass.
neutral=c.posed(parts);badphase=b.Pos(0,*c.CAM_YZ)*b.Rot(180/c.PARAMS['cam_teeth'],0,0)*parts['cam'];old=c.posed(parts,center=math.hypot(90,72))
controls=dict(half_cam_tooth_phase_overlap_mm3=pair_overlap(neutral['crank'],badphase),old_axis_overlap_mm3=vol(old['crank'].intersect(old['cam'])))
m=json.loads((ROOT/'inventory/engine/full-assembly.json').read_text());D={d['id']:d for d in m['definitions']};O={o['id']:o for o in m['occurrences']};T=transforms(m);current={}
for ident in ['crank-timing-gear','cam-timing-gear','camshaft','crankshaft','cam-gear-spacer','cam-timing-key','timing-cover']:
 p=ROOT/D[O[ident]['definition']]['step'].lstrip('/');inputs[str(p.relative_to(ROOT))]=sha(p);current[ident]=b.import_step(p)
protected={}
for key,radius in [('crank',30),('cam',47.5)]:
 guard=b.Rot(0,90,0)*b.Cylinder(radius,20);base=current[key+'-timing-gear'].intersect(guard);now=parts[key].intersect(guard);protected[key+'_local_core_difference_mm3']=vol(base.cut(now))+vol(now.cut(base))
# Independent hypothesized axes are deliberately not installed. Report actual
# baseline incompatibility so a later integration cannot mistake pair PASS.
x=T['crank-timing-gear'].position.X;world={key:b.Pos(x,0,0)*q for key,q in neutral.items()};installation=[]
for key,q in world.items():
 for ident in ['camshaft','crankshaft','cam-gear-spacer','cam-timing-key','timing-cover']:
  neighbor=current[ident].moved(T[ident]);installation.append(dict(gear=key,neighbor=ident,overlap_mm3=vol(q.intersect(neighbor)),distance_mm=q.distance_to(neighbor)))
for key,q in neutral.items():
 v,f=q.tessellate(.07,.15);preview[key+'_vertices']=np.array([tuple(x) for x in v]);preview[key+'_faces']=np.asarray(f)
np.savez_compressed(OUT/'preview.npz',**preview)
assert all(sha(ROOT/p)==h for p,h in inputs.items()),'Input changed during check'
passed=max(row['overlap_mm3'] for row in sweep)<1e-5 and min(controls.values())>.1 and max(protected.values())<1e-5 and max(x['step_volume_error_mm3'] for x in exports.values())<.001
r=dict(status='PASS independent sampled pair; NOT INSTALLABLE at unchanged current axes' if passed else 'FAIL independent pair diagnostics',engagement_lens=dict(chord_u_mm=chord,half_height_mm=lens_half,clip_u_mm=[33.6,47.6],clip_v_mm=[-22,22],clip_x_mm=[-8,8],guarantee='All possible tip-cylinder overlap contained; clipped-region distance is an upper bound on global gap.'),parameters=c.PARAMS,center_distance_mm=c.CENTER,cam_yz_mm=c.CAM_YZ,inputs_sha256=inputs,exports=exports,sweep=sweep,negative_controls=controls,protected_local_interfaces=protected,current_installation_comparison=installation,limits=['Independent hypothesis only. Pair profiles,25deg helix,14mm width, backlash and web-hole dimensions are estimates.','Sweep samples one tooth period25times; does not establish continuous contact, load strength or production calibration. Surface gap is unloaded backlash, not demonstrated loaded flank contact.','Current engine camshaft/block/valvetrain and cover are unchanged and incompatible with proposed axis relocation. Separate coherent datum revision required.','Source counts and diameters come from different replacement manufacturers; diameter-as-tip assumption remains explicit.'])
(ROOT/'inventory/engine/timing-gear-pair-candidate-validation.json').write_text(json.dumps(r,indent=2)+'\n');print(r['status'],flush=True)
