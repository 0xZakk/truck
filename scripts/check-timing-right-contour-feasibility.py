#!/usr/bin/env python3
"""Analytic 2D common corridor only; no replacement CAD or neighbor subtraction."""
from pathlib import Path
import ast,json,hashlib,math
import numpy as np
R=Path(__file__).resolve().parents[1];source=R/'cad/engine/timing_cover_joint_candidate.py';reg=R/'inventory/engine/timing-cover-registration-validation.json'
a={n.targets[0].id:ast.literal_eval(n.value) for n in ast.parse(source.read_text()).body if isinstance(n,ast.Assign) and isinstance(n.targets[0],ast.Name) and n.targets[0].id in ('OUTLINE_NORMALIZED','HOLES_NORMALIZED')};j=json.loads(reg.read_text());param=j['estimated_coordinated_alternative']['parameters']
def trans(p,pr):
 scale,cx,cy,deg=pr;ang=math.radians(deg);rot=np.array([[math.cos(ang),-math.sin(ang)],[math.sin(ang),math.cos(ang)]]);return ((np.array(p)*1600-[cx,cy])*[1,-1])*scale@rot.T
outline=trans(a['OUTLINE_NORMALIZED'],param);holes=trans(a['HOLES_NORMALIZED'],param)
CAM=(95.1098209901611,76.08785679212887);support=9.;wall=6.;clearance=1.;barrel=65.;cam_cavity=84.947;crank_cavity=44.18
# Conservative circular support margin is an explicit feasibility estimate.
def right(c,r,z):return c[0]+math.sqrt(max(0,r*r-(z-c[1])**2)) if abs(z-c[1])<=r else -1e6
def bounds(z):
 lo=max(right(CAM,cam_cavity+wall+support,z),right((0,0),crank_cavity+wall+support,z),right((-32,170),66.25+support,z))
 rr=barrel+support+clearance;hi=280-math.sqrt(rr*rr-(z-100)**2) if abs(z-100)<rr else 1e6
 return lo,hi
rows=[]
for z in [-24.5,0,25,35,50,float(holes[5,1]),100,125,150,175,190,200]:
 lo,hi=bounds(z);rows.append({'z_mm':z,'minimum_axis_y_mm':lo,'maximum_axis_y_mm':None if hi==1e6 else hi,'corridor_width_mm':None if hi==1e6 else hi-lo})
sensitivity=[]
for q in j['estimated_coordinated_alternative']['pixel_interval_corner_sensitivity']:
 pp=[q['scale'],*q['crank_source_pixel'],param[3]];h=trans(a['HOLES_NORMALIZED'],pp)[5];lo,hi=bounds(h[1]);sensitivity.append({'station6_yz_mm':h.tolist(),'inboard_change_to_corridor_upper_mm':float(h[0]-hi)})
station=[]
for i,(y,z) in enumerate(holes):
 lo,hi=bounds(z);station.append({'station':i+1,'axis_yz_mm':[y,z],'right_corridor_lower_mm':lo,'right_corridor_upper_mm':None if hi==1e6 else hi,'inboard_change_to_upper_mm':None if hi==1e6 else y-hi,'scope':'Right-side corridor relevant to stations5/6/7 only; other stations protected unchanged'})
O=R/'cad/engine/generated/timing-right-contour-feasibility';O.mkdir(exist_ok=True)
np.savez(O/'corridor.npz',outline=outline,holes=holes,z=np.linspace(-24.5,200,900),bounds=np.array([bounds(z) for z in np.linspace(-24.5,200,900)]))
manual=next((R/'manuals/factory-service-manual').glob('1994*L6*/Repair*/Engine*/Engine/Timing*/Timing%20Cover/Service*/index.html'))
inputs=[Path(__file__),source,reg,R/'cad/engine/timing_cover_shell_candidate.py',R/'reference/engine/timing-cover-registration-review.json',manual]
r={'status':'FEASIBLE local analytic corridor; no replacement contour built','declared_estimates':{'cam_cavity_radius':cam_cavity,'crank_cavity_radius':crank_cavity,'wall_mm':wall,'common_land_halfwidth_mm':support,'compressor_barrel_radius_mm':barrel,'external_clearance_mm':clearance},'scope':'Actual axes; inherited envelope radii. Section feasibility alone does not preserve whole seal topology, exact gear fit, support stock or source shape. No compressor Boolean used.','sections':rows,'source_stations':station,'registration_pixel_corner_sensitivity':sensitivity,'source_assessment':{'seven_hole_homography_residual_px':j['image_fit']['seven_hole_residual_pixels'],'flat009_similarity_rms_px':j['image_fit']['flat009_similarity_rms_pixels'],'flat009_homography_rms_px':j['image_fit']['flat009_homography_rms_pixels'],'conclusion':'Broad asymmetric right lobe exists in both manufacturer photos. Exact width/axis registration remains estimated; correspondence residual cannot identify physical parallax or justify40mm recontouring. Corner pixel-only perturbations do not remove station6 intrusion.'},'service_state':{'timing_cover_manual_step3':'Remove belt and PS pump/AC compressor/bracket assembly before cover screws','installed_access_tool_gate':'NOT CLAIMED; original installed tool failures retained','service_tool_gate':'Candidate must check exact tool against remaining engine/pump/cover; not run because no contour yet'},'input_sha256':{str(p.relative_to(R)):hashlib.sha256(p.read_bytes()).hexdigest() for p in inputs}}
(R/'inventory/engine/timing-right-contour-feasibility.json').write_text(json.dumps(r,indent=2)+'\n')
if '--render' in __import__('sys').argv:
 import matplotlib;matplotlib.use('Agg')
 import matplotlib.pyplot as plt
 fig,ax=plt.subplots(figsize=(10,7));z=np.linspace(-24.5,200,900);bo=np.array([bounds(v) for v in z]);ax.fill_betweenx(z,bo[:,0],np.minimum(bo[:,1],290),color='#b9e4cf',alpha=.6,label='Analytic centerline corridor (9mm half-land)');ax.plot(outline[:,0],outline[:,1],color='#ad4b36',lw=1.5,label='Frozen registered gasket outline');ax.scatter(holes[:,0],holes[:,1],c='#ad4b36');
 for i,(y,zz) in enumerate(holes):ax.annotate(str(i+1),(y,zz),xytext=(4,4),textcoords='offset points')
 for c,rad,col,name in [(CAM,cam_cavity,'#537bad','cam cavity envelope'),((0,0),crank_cavity,'#7c739e','crank cavity envelope'),((280,100),barrel,'#333333','compressor barrel envelope')]:
  t=np.linspace(0,math.tau,300);ax.plot(c[0]+rad*np.cos(t),c[1]+rad*np.sin(t),c=col,label=name)
 ax.set(xlim=(70,295),ylim=(-35,225),xlabel='Y mm',ylabel='Z mm',title='Right common contour feasibility — no replacement route\nRadii, 6mm wall and 1mm clearance remain estimates');ax.set_aspect('equal');ax.grid(alpha=.2);ax.legend(fontsize=8,loc='upper left');fig.tight_layout();fig.savefig(O/'corridor-review.png',dpi=160)
