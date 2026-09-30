"""Read-only motion study of frozen timing core against canonical rotating parts."""
from pathlib import Path
from copy import deepcopy
import json
import build123d as b
from assembly_math import transforms
from timing_coupled_core_candidate import AXIS, cam_frame
ROOT=Path(__file__).resolve().parents[2]
CAM=ROOT/'cad/engine/generated/timing-coupled-core-candidate/camshaft.step'
MANIFEST=ROOT/'inventory/engine/full-assembly.json'
CAM_RADIUS=25.622251
CRANK_RADIUS=87.546001
ROD_STATION_RADIUS=15.001

def inputs():
    manifest=json.loads(MANIFEST.read_text())
    selected=deepcopy(manifest)
    selected['occurrences']=[o for o in manifest['occurrences'] if o['id']=='crankshaft' or o['parent'].startswith(('rod-group-','piston-group-'))]
    defs={d['id']:d for d in manifest['definitions']}
    shapes={key:b.import_step(ROOT/defs[key]['step'].lstrip('/')) for key in {o['definition'] for o in selected['occurrences']}}
    return selected,shapes,b.import_step(CAM)

def posed(manifest,shapes,cam,theta=0,axial=0):
    """Reuse shared actual transforms; frozen core frame moves complete cam group."""
    frames=transforms(manifest,theta)
    return {o['id']:frames[o['id']]*shapes[o['definition']] for o in manifest['occurrences']},cam_frame(theta,axial)*cam

def cylinder(radius,axis=(0,0),xmin=-500,xmax=500):
    return b.Pos((xmin+xmax)/2,*axis)*b.Rot(0,90,0)*b.Cylinder(radius,xmax-xmin)
