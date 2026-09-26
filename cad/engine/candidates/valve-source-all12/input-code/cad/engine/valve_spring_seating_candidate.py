"""Second-stage source-constrained spring/stem/guide study; never edits live assets.

Factory table constrains heights/clearances, not assumed coils or casting bosses.
Preserves first-stage valve-layout STEP hashes.
"""
from pathlib import Path
import json,hashlib,sys
import build123d as b
from valve_layout_candidate import OUT as FIRST, BASE, VALVE_Y
ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'cad/engine/candidates/valve-spring-seating'
INSTALLED={'intake':1.64*25.4,'exhaust':1.47*25.4}
FREE={'intake':1.96*25.4,'exhaust':1.78*25.4}
GUIDE_DIAMETER=.3438*25.4
STEM_CLEARANCE=.00185*25.4
STEM_DIAMETER=GUIDE_DIAMETER-STEM_CLEARANCE
RETAINER_BOTTOM=363.
HEAD_Z=255.5
HEAD_FLOOR=304.


def spring(kind,lift=0):
    """Six-turn illustrative wire with flat ground end faces, exact axial height.

    Free/installed heights sourced; six turns,26mm mean diameter and4mm wire
    remain visual assumptions. Constant-pitch end grinding is not OEM end form.
    """
    h=INSTALLED[kind]-lift
    if h<INSTALLED[kind]-10.0330001 or h>INSTALLED[kind]+1e-8:raise ValueError('Outside candidate lift')
    path=b.Helix(h/6,h,13)
    coil=b.sweep(b.Plane(origin=path@0,z_dir=path%0)*b.Circle(2),path=path)
    return coil & (b.Pos(0,0,h/2)*b.Box(40,40,h))


def stem_adapter(valve):
    # Keep head and keeper groove; reduce only cylindrical stem above head.
    shell=b.Cylinder(5,110)-b.Cylinder(STEM_DIAMETER/2,112)
    return valve-b.Pos(0,0,58.2)*shell


def head_adapter(head,stations):
    for kind,x in zip(['intake','exhaust'],stations):
        top=RETAINER_BOTTOM-INSTALLED[kind]-HEAD_Z
        # Restore old guide's excess bore, maintaining correct head material.
        sleeve=b.Cylinder(5.01,48.5-21)-b.Cylinder(GUIDE_DIAMETER/2,50)
        head+=b.Pos(x,VALVE_Y,(21+48.5)/2)*sleeve
        boss=b.Cylinder(18,top-48)-b.Cylinder(GUIDE_DIAMETER/2,100)
        head+=b.Pos(x,VALVE_Y,(top+48)/2)*boss
    return head


def seal():
    return b.Cylinder(8,9)-b.Cylinder(STEM_DIAMETER/2+.05,12)


def main():
    OUT.mkdir(parents=True,exist_ok=True)
    layout=json.loads((FIRST/'occurrence-layout.json').read_text())
    source_files={n:FIRST/(n+'.step') for n in ['cylinder-head','intake-valve','exhaust-valve']}
    source_hashes={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in source_files.values()}
    shapes={'cylinder-head':head_adapter(b.import_step(source_files['cylinder-head']),layout['stations']),'valve-seal':seal()}
    for kind in INSTALLED:
        shapes[kind+'-valve']=stem_adapter(b.import_step(source_files[kind+'-valve']))
        shapes[kind+'-spring']=spring(kind)
    for key,s in shapes.items():
        assert s.is_valid and len(s.solids())==1,(key,len(s.solids()))
        b.export_step(s,OUT/(key+'.step'))
    source=next(p for p in (ROOT/'manuals/factory-service-manual').rglob('index.html') if 'Engine%20Rebuilding%20Specifications' in str(p) and 'Mechanical%20Specifications' in str(p))
    report={'status':'candidate geometry generated; validation separate','input_hashes':source_hashes,
      'source_path':str(source.relative_to(ROOT)),'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),
      'source_reference':'kb/sources/spc-engine-rebuilding-specifications.md',
      'dimensions':{'installed_height_mm':INSTALLED,'free_length_mm':FREE,'guide_diameter_mm':GUIDE_DIAMETER,'stem_diameter_mm':STEM_DIAMETER,'diametral_clearance_mm':STEM_CLEARANCE},
      'derivations':['Installed heights use factory closed-load test heights, within installed ranges.','Guide uses factory bore midpoint; stem derived from midpoint of permitted diametral clearance. Not a catalog stem dimension.'],
      'assumptions':['Six turns,4mm wire,26mm mean diameter and constant-pitch ground end shape unverified. No force/rate claim.','Head floor/retainer absolute datums inherited; added boss heights enforce sourced installed spring heights, not a factory casting replica.','Seal lip is illustrative noninterfering fit; no elastic sealing simulation.','Valve head/groove/length and keeper construction retained from prior teaching study.'],
      'shape_hashes':{n:hashlib.sha256((OUT/(n+'.step')).read_bytes()).hexdigest() for n in shapes}}
    (OUT/'provenance.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))
if __name__=='__main__':main()
