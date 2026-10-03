"""Explicit educational frame choices; only sampled 2D envelope check, no CAD."""
from pathlib import Path
import ast,json,hashlib,math
import numpy as np
from matplotlib.path import Path as Polygon
R=Path(__file__).resolve().parents[1];P='pump-cover-joint-20261003';ip=R/f'reference/engine/{P}-joint-fit.json';j=json.loads(ip.read_text());x=np.array(j['parameters']);k=np.exp(x[8]);ang=x[9];rot=np.array([[np.cos(ang),np.sin(ang)],[-np.sin(ang),np.cos(ang)]]);t=150*x[10:12]
source=R/'cad/engine/timing_cover_joint_candidate.py';a={n.targets[0].id:ast.literal_eval(n.value)for n in ast.parse(source.read_text()).body if isinstance(n,ast.Assign)and isinstance(n.targets[0],ast.Name)and n.targets[0].id in ['OUTLINE_NORMALIZED','HOLES_NORMALIZED']}
a0=np.radians(-.039823552987937626);r0=np.array([[np.cos(a0),np.sin(a0)],[-np.sin(a0),np.cos(a0)]])
def old(p):return ((np.array(p)*1600-[588.5373742452892,930.4751087566926])*[1,-1])*.26223302269259874@r0
outline=old(a['OUTLINE_NORMALIZED']);holes=old(a['HOLES_NORMALIZED'])
pump=np.array([[-24.3,103.5],[34.3,176.3],[-98.2,175.3],[-15,234.9]])
def margin(poly):
 angles=np.arange(360)*np.pi/180;ring=np.array([95.1098209901611,76.08785679212887])+86.947*np.c_[np.cos(angles),np.sin(angles)]
 a=poly;b=np.roll(poly,-1,axis=0);v=b-a;w=ring[:,None,:]-a;f=np.clip(np.sum(w*v,axis=2)/np.sum(v*v,axis=1),0,1);dist=np.min(np.linalg.norm(w-f[:,:,None]*v,axis=2),axis=1)*np.where(Polygon(poly).contains_points(ring),1,-1);return float(dist.min())
options=[]
for name,g,scope in [('A_fixed_pump_pattern_scale',1.,'Preserve current estimated pump transverse scale; shrink cover to source relative size. FAIL sampled cam+wall envelope.'),('B_fixed_cover_global_scale',1/k,'Preferred educational hypothesis. Preserve prior source-traced cover scale and engine crank/pan frame; derive enlarged pump mounting footprint and coupled pose. Not scale sourced hardware.')]:
 center=g*(np.array([-32.,170.])-t)@rot.T;pa=g*(pump-t)@rot.T;ch=g*k*holes
 options.append({'id':name,'global_scale_relative_pump_rectification':float(g),'status':scope,'pump_center_yz_mm':center.tolist(),'pump_center_delta_from_old_mm':(center-[-32,170]).tolist(),'pump_clock_delta_deg':float(-np.degrees(ang)),'pump_mounting_axes_yz_mm':pa.tolist(),'pump_mounting_offsets_from_new_center_mm':(pa-center).tolist(),'cover_axes_yz_mm':ch.tolist(),'pump_lower_to_cover3_axis_gap_mm':float(np.linalg.norm(pa[0]-ch[2])),'sampled_cam_envelope_margin_mm':margin(g*k*outline[:45]),'pump_gasket_base_R59_scaled_estimate_mm':59*g,'pump_old_dry_boss_radius_scaled_for_reference_only_mm':11.5*g,'cover_source_scale_mm_per_1600reference_px':float(g*k*.26223302269259874),'rigid_pump_occurrence_transform':'X unchanged; transverse local offsets rotate by clock delta only for internals/hardware; casting/gasket mounting footprint uses declared global-scale ratio separately.'})
r={'readiness':'CONTRACT REVIEW ONLY; no CAD','frame':{'crank_center_yz':[0,0],'pan_orientation':'horizontal engine datum; source terminal trace waviness retained, no5.64degree pan tilt','axial_planes_preserved_as_estimates':{'block':373,'pump_back':375,'pump_seat':389,'pump_hub_seat':473.43,'cover_back':373.8,'cover_screw_seat':379.8},'absolute_crank_location_in_source_gasket':'Inherited Dorman-aperture estimate588.537374,930.475109 reference pixels, with unbounded parallax. Not independently fixed by ATK hub.'},'options':options,'envelope_check':{'scope':'360samples at1degree around currentcam(95.109821,76.087857),R86.947=sourcecomparisontip83.947+clearance1+wall2 against raw45point outerarch. No lowerbridge, actualsolid, support, pan or motion check.','why_prior_margin_differs':'This uses one currentcam and rawtrace; older report included two cam hypotheses plus current parameter construction.'},'dependencies':['Full52pump occurrences and new source-compared housing/gasket','Block pump seat/cavity/fifth opening/four dry sockets, coolant jacket and cylinder1 clearance','Four pump fasteners: retain diameters/length, relocate to newaxes','Cover7 axes/seat contact/main gasket/2692seal and gear clearance: preserve optionB geometry provisionally and freshly verify','Pan-front terminal contacts and fixedhorizontalplane; source trace terminalwaviness','Pump pulley/fan/belt path and accessorycarrier/thermactor supports','Heater hose/inlet/radiator routing; no stationary downstream endpoint silently translated','Impeller sweep/shaft/bearing/seal internal coaxes, fullprotectedregions attached to revisedpumpframe'],'input_sha256':{str(p.relative_to(R)):hashlib.sha256(p.read_bytes()).hexdigest()for p in [ip,source,Path(__file__)]}}
(R/f'reference/engine/{P}-datums.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r,indent=2))
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
fig,axes=plt.subplots(1,2,figsize=(13,7))
for ax,o in zip(axes,options):
 g=o['global_scale_relative_pump_rectification'];co=g*k*outline
 ax.plot(*co.T,label='Cover gasket source outline');pc=np.array(o['pump_center_yz_mm']);pa=np.array(o['pump_mounting_axes_yz_mm']);ch=np.array(o['cover_axes_yz_mm']);ax.scatter(*pa.T,s=25,label='Pump bolts');ax.scatter(*ch.T,marker='+',label='Cover bolts');ax.plot([0,0],[-65,20],':',color='gray');ax.scatter(0,0,marker='x',s=70,color='black',label='Crank convention')
 ax.add_patch(plt.Circle(pc,59*g,fill=False,color='tab:green',label='Estimated gasket opening'))
 ax.add_patch(plt.Circle([95.1098209901611,76.08785679212887],86.947,fill=False,color='tab:red',label='Cam+wall sampled envelope'))
 for center in pa:ax.add_patch(plt.Circle(center,11.5,fill=False,color='tab:blue',alpha=.5))
 ax.annotate('pump',pc);ax.set_aspect('equal');ax.set_xlim(-160,275);ax.set_ylim(-65,285);ax.set_title(o['id']+'\nSampled cam margin '+format(o['sampled_cam_envelope_margin_mm'],'.2f')+' mm');ax.set_xlabel('Y / estimated mm');ax.set_ylabel('Z / estimated mm');ax.legend(fontsize=7,loc='upper right')
fig.suptitle('Coordinated frame options: crank origin and horizontal pan convention\nB is the proposed educational scale; no CAD or installed acceptance');fig.tight_layout();fig.savefig(R/f'reference/engine/{P}-datum-options.png',dpi=150);plt.close(fig)
