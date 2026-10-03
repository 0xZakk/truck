from pathlib import Path
import json,hashlib,numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
R=Path(__file__).resolve().parents[1];p=R/'reference/engine/pump-source-registration-20261003-measurements.json';r=json.loads(p.read_text());b=r['best_by_bolts'];t=np.array(b['translation_math_px']);rad=r['bolt_rms_radius_px'];rot=np.array(b['rotation']);scale=b['scale_px_per_candidate_mm']
def normpix(v):return (np.asarray(v)*[1,-1]-t)/rad
M=np.array([[7.7,-66.5],[66.3,6.3],[-66.2,5.3],[17.,64.9]])*[-1,1];S=np.array([q['xy']for q in r['source_holes']]);MP=scale*M@rot+t
fig=plt.figure(figsize=(13,8),facecolor='#fafafa');gs=fig.add_gridspec(2,2,width_ratios=[1.05,1]);whole=fig.add_subplot(gs[:,0]);bolt=fig.add_subplot(gs[0,1]);arm=fig.add_subplot(gs[1,1])
for ax in [whole,bolt]:
 src=normpix(S);mod=(MP-t)/rad
 ax.scatter(src[:,0],src[:,1],s=100,facecolors='none',edgecolors='#b15b34',label='Carter pixel measurements',zorder=3)
 ax.scatter(mod[:,0],mod[:,1],s=45,marker='+',c='#247288',label='Registered candidate',zorder=4)
 fifth=normpix(r['source_fifth_xy']);me=(scale*np.array([10.9,69.])@rot)/rad
 ax.scatter(*fifth,s=140,marker='s',facecolors='none',edgecolors='#b15b34');ax.scatter(*me,s=55,marker='+',c='#247288')
 ax.scatter(0,0,c='black',s=20);ax.set_aspect('equal');ax.grid(alpha=.16);ax.set_xlabel('Normalized rear-view horizontal');ax.set_ylabel('Normalized rear-view vertical')
for i,xy in enumerate((MP-t)/rad,1):bolt.text(xy[0]+.07,xy[1],f'bolt{i}',fontsize=9)
bolt.set_title(f'Proper rotation {r["roll_deg"]:.2f}° · no mirror\nFour-bolt RMS {b["bolt_rms_px"]:.2f}px; fifth held out {b["fifth_error_px"]:.2f}px',fontsize=11);bolt.set_xlim(-1.05,1.05);bolt.set_ylim(-1.25,1.05)
labels={'heater_visible_root_cuff_axis':'heater cuff','heater_terminal_opening_center':'heater tip','inlet_terminal_rim_center':'inlet rim'}
for name,v in r['manual_features'].items():
 src=normpix(v['source_xy']);mod=normpix(v['candidate_registered_xy'])
 whole.plot([0,src[0]],[0,src[1]],color='#b15b34',lw=1.2,alpha=.7);whole.plot([0,mod[0]],[0,mod[1]],color='#247288',lw=1.2,ls='--',alpha=.7)
 whole.scatter(*src,c='#b15b34',s=35);whole.scatter(*mod,c='#247288',s=35,marker='x');whole.text(src[0]+.05,src[1]+.1,labels[name],fontsize=10)
whole.set_title('Projected directions broadly align after bolt registration\nTip/rim extents remain different',fontsize=12);whole.set_xlim(-1.8,3);whole.set_ylim(-1.4,4.8)
outline=r['outline_samples'];xs=np.array([q['x_px']for q in outline]);source=np.array([q['source_threshold_y_bounds'][2]for q in outline])
xx=(xs-t[0])/rad;top=(-source[:,0]-t[1])/rad;bottom=(-source[:,1]-t[1])/rad
arm.fill_between(xx,bottom,top,color='#b15b34',alpha=.16);arm.plot(xx,top,c='#b15b34',label='Carter casting / neck silhouette');arm.plot(xx,bottom,c='#b15b34')
valid=[q for q in outline if q['candidate_y_bounds']is not None];mx=(np.array([q['x_px']for q in valid])-t[0])/rad;my=np.array([q['candidate_y_bounds']for q in valid]);arm.plot(mx,(-my[:,0]-t[1])/rad,c='#247288',ls='--',label='Actual candidate housing GLB');arm.plot(mx,(-my[:,1]-t[1])/rad,c='#247288',ls='--')
arm.set_title('Projected candidate inlet arm is narrower/shorter\nImage-space finding; no factory millimeters inferred',fontsize=11);arm.set_xlabel('Normalized rear-view horizontal');arm.set_ylabel('Normalized rear-view vertical');arm.legend(fontsize=8);arm.grid(alpha=.16)
fig.legend(*bolt.get_legend_handles_labels(),loc='upper center',bbox_to_anchor=(.5,.90),ncol=2,fontsize=9)
fig.suptitle('Carter W9046M · rear bolt-pattern registration\nAuthored measurements only — manufacturer pixels excluded',fontsize=15)
fig.text(.5,.015,'Normalization: RMS bolt radius. Candidate bolt dimensions are estimates; camera perspective, axial parallax and manual endpoint uncertainty remain.',ha='center',fontsize=9)
fig.tight_layout(rect=[0,.035,1,.92]);out=R/'reference/engine/pump-source-registration-20261003-registration.png';fig.savefig(out,dpi=145)
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
(R/'reference/engine/pump-source-registration-20261003-plot.json').write_text(json.dumps({'path':str(out.relative_to(R)),'sha256':sha(out),'inputs':{str(p.relative_to(R)):sha(p),str(Path(__file__).relative_to(R)):sha(Path(__file__))}},indent=2)+'\n')
