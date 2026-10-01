from pathlib import Path
import json,hashlib,numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
R=Path(__file__).resolve().parents[1];p=R/'inventory/engine/waterpump-neck-registration-research.json';j=json.loads(p.read_text());O=R/'cad/engine/generated/waterpump-port-access-research';O.mkdir(exist_ok=True);w=np.array(j['landmarks']['model_relative_yz_mm']);fig,axes=plt.subplots(1,2,figsize=(13,6))
for ax,name,parity in zip(axes,['rear','front'],['-1','1']):
 d=j['fits'][name][parity];q=np.array(d['predicted_model_yz']);ax.scatter(w[:,0],w[:,1],s=[80,80,80,80,140],facecolors='none',edgecolors='k',label='Retained hole pattern');ax.scatter(q[:,0],q[:,1],s=25,color='#307ea5',label='Registered photo landmarks')
 for i,(y,z) in enumerate(w):ax.text(y+3,z+3,'5th'if i==4 else str(i+1))
 n=np.array(d['neck_model_yz_estimate']);ax.plot(n[:,0],n[:,1],color='#bf563d',lw=5,label='Photo neck line (parallax unbounded)');h=np.array(d['heater_root_model_yz_estimate']);ax.scatter(*h,color='#3c9456',marker='x',s=70,label='Photo heater root');ax.arrow(0,0,120,0,width=.5,color='#aaa',length_includes_head=True,head_width=6);ax.text(48,7,'Current inlet +Y',color='#777');ax.axhline(0,color='#ddd');ax.axvline(0,color='#ddd');ax.set_aspect('equal');ax.set(xlim=(-150,145),ylim=(-155,110),xlabel='Relative Y in existing model frame (mm)',ylabel='Relative Z in existing model frame (mm)',title=f'{name.capitalize()} correspondence: RMS {d["rms_model_mm"]:.3f} model mm');ax.legend(fontsize=8,loc='lower right')
fig.suptitle('Five unequal apertures establish orientation; no physical scale inferred');fig.tight_layout();out=O/'registration-review.png';fig.savefig(out,dpi=160);(R/'inventory/engine/waterpump-neck-registration-render.json').write_text(json.dumps({'image':str(out.relative_to(R)),'image_sha256':hashlib.sha256(out.read_bytes()).hexdigest(),'research_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'renderer_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()},indent=2)+'\n')
