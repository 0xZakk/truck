"""Render actual isolated candidate STEP, with a back half-section through head."""
from pathlib import Path
import json,sys,math,argparse
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
p=argparse.ArgumentParser();p.add_argument('--export',type=Path);p.add_argument('--render',type=Path);p.add_argument('--output',type=Path);args=p.parse_args()
if args.export:
    import build123d as b
    sys.path.insert(0,str(ROOT/'cad/engine'))
    from valve_layout_candidate import OUT as FIRST,BASE
    from valve_source_layout import OUT,VALVE_Y,PIVOT_Y,solve,spring,INSTALLED,LENGTHS
    layout=json.loads((OUT/'occurrence-layout.json').read_text());defs={};placed={};x=layout['stations'][0];tag='c1-intake'
    for o in layout['occurrences']:
        if not (o['id'].startswith(tag) or o['id'] in ['cylinder-head','camshaft']):continue
        name=o['definition'];path=OUT/(name+'.step')
        if not path.exists():path=FIRST/(name+'.step')
        if not path.exists():path=BASE/(name+'.step')
        if name not in defs:defs[name]=b.import_step(path)
        placed[o['id']]=b.Pos(*o['position'])*b.Rot(*o['orientation'])*defs[name]
    arrays={};metadata=[]
    for panel,height in enumerate([0,.247*25.4]):
        state=solve(height);t=state['angle'];vl=state['valve_lift'];parts=dict(placed)
        parts[tag+'-rocker']=b.Pos(x,PIVOT_Y,state['pivot_z'])*b.Rot(math.degrees(t),0,0)*defs['rocker-arm']
        top,bottom=state['top'],state['bottom'];rotation=-math.degrees(math.atan2(top[0]-bottom[0],top[1]-bottom[1]))
        parts[tag+'-pushrod']=b.Pos(x,(top[0]+bottom[0])/2,(top[1]+bottom[1])/2)*b.Rot(rotation,0,0)*defs['pushrod']
        for oid in placed:
            if oid.startswith(tag+'-lifter-'):parts[oid]=b.Pos(0,0,height)*placed[oid]
            elif oid in [tag+'-valve',tag+'-retainer',tag+'-keeper-1',tag+'-keeper-2']:parts[oid]=b.Pos(0,0,-vl)*placed[oid]
        parts[tag+'-spring']=b.Pos(x,VALVE_Y,363+LENGTHS['intake']-109-INSTALLED['intake'])*spring('intake',vl)
        parts['camshaft']=b.Pos(0,90,72)*b.Rot(-234 if panel else 0,0,0)*defs['camshaft']
        parts['camshaft']&=b.Pos(x,90,72)*b.Box(15,70,70)
        parts['cylinder-head']&=b.Pos(x-6,40,315)*b.Box(4,160,150)
        for oid,shape in parts.items():
            if '-lifter-' in oid and not oid.endswith('-lifter-body'):continue
            verts,faces=shape.tessellate(.15);index=len(metadata)
            arrays[f'v{index}']=np.asarray([tuple(v) for v in verts]);arrays[f'f{index}']=np.asarray(faces)
            color=[.63,.7,.74]
            if oid=='cylinder-head':color=[.54,.64,.61]
            elif oid=='camshaft':color=[.72,.49,.24]
            elif 'spring' in oid:color=[.72,.59,.28]
            elif 'lifter' in oid:color=[.28,.57,.68]
            elif 'rocker' in oid:color=[.43,.5,.6]
            metadata.append({'id':oid,'panel':panel,'color':color})
    arrays['metadata']=np.array(json.dumps(metadata));np.savez_compressed(args.export,**arrays)
else:
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    from engine_qc_raster import render_mesh
    archive=np.load(args.render,allow_pickle=False);meta=json.loads(str(archive['metadata']))
    fig,axes=plt.subplots(1,2,figsize=(11,9))
    for panel,axis in enumerate(axes):
        triangles=[];colors=[]
        for i,item in enumerate(meta):
            if item['panel']!=panel:continue
            verts=archive[f'v{i}'];faces=verts[archive[f'f{i}']];normals=np.cross(faces[:,1]-faces[:,0],faces[:,2]-faces[:,0]);normals/=np.maximum(np.linalg.norm(normals,axis=1)[:,None],1e-12)
            shade=.4+.6*np.abs(normals@np.array([.768,-.4,.5]));triangles.append(faces);colors.append(shade[:,None]*np.array(item['color']))
        axis.imshow(render_mesh(np.concatenate(triangles),np.concatenate(colors),azimuth=8,elevation=8));axis.set_axis_off();axis.set_title('Intake at maximum candidate lift' if panel else 'Intake closed · actual STEP')
    fig.suptitle('Source-sized valve/pushrod/lifter candidate · assumed internal datums\nHead back section; block/cover omitted. Not the installed engine or a verified Ford casting.')
    fig.tight_layout();fig.savefig(args.output,dpi=130)
