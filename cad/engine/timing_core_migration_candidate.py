"""Isolated timing-core translation; existing local shapes/IDs, no installation."""
from pathlib import Path
import json,math
import build123d as b
ROOT=Path(__file__).resolve().parents[2]
CENTER=121.8
CAM_YZ=(CENTER*90/math.hypot(90,72),CENTER*72/math.hypot(90,72))
DELTA=(0,CAM_YZ[0]-90,CAM_YZ[1]-72)
IDS=['camshaft']+[f'cam-bearing-{i}' for i in range(1,5)]+['rear-cam-plug','crank-timing-gear','cam-timing-gear','cam-thrust-plate','cam-gear-spacer','cam-timing-key']+[f'cam-thrust-{part}-{i}' for part in ['bolt','washer'] for i in [1,2]]
def source_parts(manifest):
    defs={d['id']:d for d in manifest['definitions']};occ={o['id']:o for o in manifest['occurrences']};assemblies={a['id']:a for a in manifest['assemblies']}
    def frame(identifier):
        if identifier not in assemblies:return b.Location()
        a=assemblies[identifier]
        return frame(a['parent'])*b.Pos(*a.get('position_cad_mm',[0,0,0]))*b.Rot(*a.get('rotation_cad_deg',[0,0,0]))
    parts={};records={};inputs={}
    for identifier in IDS+['block','timing-cover','crankshaft']:
        o=occ[identifier];path=ROOT/defs[o['definition']]['step'].lstrip('/')
        if identifier in ['cam-timing-gear','crank-timing-gear']:
            path=ROOT/'cad/engine/generated/timing-gear-pair-refined'/('cam.step' if identifier.startswith('cam-') else 'crank.step')
        local=b.import_step(path)
        pose=frame(o['parent'])*b.Pos(*o['position_cad_mm'])*b.Rot(*o.get('rotation_cad_deg',[0,0,0]))
        q=pose*local
        if identifier in IDS and identifier!='crank-timing-gear':q=b.Pos(*DELTA)*q
        parts[identifier]=q;inputs[identifier]=path
        records[identifier]={'definition':o['definition'],'parent':o['parent'],'baseline_position_cad_mm':o['position_cad_mm'],'baseline_rotation_cad_deg':o.get('rotation_cad_deg',[0,0,0]),'additional_world_translation_mm':list(DELTA) if identifier in IDS and identifier!='crank-timing-gear' else [0,0,0]}
    return parts,records,inputs
