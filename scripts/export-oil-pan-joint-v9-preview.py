"""Offline assembled/exploded/cutaway previews of the unpublished pan joint."""
from pathlib import Path
import hashlib,json,sys
import build123d as b
import numpy as np
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'cad/engine'))
import oil_pan_joint_v9_candidate as p
from explode_stages_candidate import pan_hardware_stages,explode_offset
raw=(ROOT/'inventory/engine/full-assembly.json').read_bytes();m=json.loads(raw);defs={x['id']:x for x in m['definitions']}
module=Path(p.__file__);module_hash=hashlib.sha256(module.read_bytes()).hexdigest()
path=ROOT/defs['oil-pan']['step'].lstrip('/');pan_hash=hashlib.sha256(path.read_bytes()).hexdigest()
pan=b.Pos(0,-12,-96)*p.pan_interface(b.import_step(path))
parts={'oil-pan':pan,'oil-pan-molded-gasket':p.gasket_shape()}
screw,washer=p.screw_shape(),p.washer_shape()
for n,(x,y,z) in enumerate(p.STATIONS,1):
    parts[f'screw-{n}']=b.Pos(x,y,z)*screw;parts[f'washer-{n}']=b.Pos(x,y,z)*washer
cutaway='--cutaway' in sys.argv
if cutaway:parts['oil-pan']=parts['oil-pan']&b.Pos(0,-250,0)*b.Box(1200,500,800)
arrays={};colors=[]
for i,(ident,s) in enumerate(parts.items()):
    verts,faces=s.tessellate(.2,.2);arrays[f'vertices_{i}']=np.asarray([tuple(v) for v in verts]);arrays[f'faces_{i}']=np.asarray(faces)
    offset=(0,0,-320 if ident=='oil-pan' else -210)
    if ident.startswith(('screw-','washer-')):
        n=int(ident.split('-')[-1]);x,y,z=p.STATIONS[n-1]
        offset=((25 if x>0 else -25) if n>20 else 0,(25 if y>0 else -25) if n<=20 else 0,-340 if 'washer' in ident else -360)
    if ident.startswith(('screw-','washer-')):offset=tuple(v/.6 for v in explode_offset({'explode_stages':pan_hardware_stages(offset)},.6))
    arrays[f'explode_{i}']=np.asarray(offset)
    colors.append('#42686c' if ident=='oil-pan' else '#3e75bd' if 'gasket' in ident else '#a3adb3')
assert module_hash==hashlib.sha256(module.read_bytes()).hexdigest() and pan_hash==hashlib.sha256(path.read_bytes()).hexdigest() and raw==(ROOT/'inventory/engine/full-assembly.json').read_bytes()
arrays['metadata']=np.array(json.dumps({'assembly':'Unpublished oil-pan V9 joint'+(' cutaway' if cutaway else ''),'parts':len(parts),'colors':colors,'module_sha256':module_hash,'manifest_sha256':hashlib.sha256(raw).hexdigest(),'pan_input_sha256':pan_hash}))
np.savez_compressed(sys.argv[1],**arrays);print(sys.argv[1],flush=True)
