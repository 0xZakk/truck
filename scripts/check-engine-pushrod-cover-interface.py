"""Isolated side-cover/block fit study; never replaces installed engine geometry."""
from pathlib import Path
import sys,json,hashlib
import build123d as b
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'cad/engine'))
from pushrod_cover import block_interface_shape,MOUNT,STATIONS,cover_shape,gasket_shape,grommet_shape,bolt_shape
from assembly_math import transforms

manifest_path=ROOT/'inventory/engine/full-assembly.json'
m=json.loads(manifest_path.read_text());defs={d['id']:d for d in m['definitions']};poses=transforms(m)
block=block_interface_shape(b.import_step(ROOT/'cad/engine/generated/block.step'))
assert block.is_valid and len(block.solids())==1
parts={'cover':MOUNT*cover_shape(),'gasket':MOUNT*gasket_shape()}
grommet=grommet_shape();bolt=bolt_shape()
for i,x in enumerate(STATIONS,1):
    parts[f'grommet-{i}']=MOUNT*b.Pos(x,0,0)*grommet
    parts[f'bolt-{i}']=MOUNT*b.Pos(x,0,7.8+.48*25.4-25.4)*bolt

def overlap_volume(a,c):
    overlap=a.intersect(c)
    return sum(s.volume for s in overlap.solids()) if overlap else 0

collisions=[]
for name,s in parts.items():
    volume=overlap_volume(block,s)
    if volume>.01:collisions.append({'a':name,'b':'candidate-block','volume_mm3':volume})

# Verify all twelve pushrod passages remain open through the modified wall.
pushrods=[o for o in m['occurrences'] if o['definition']=='pushrod']
assert len(pushrods)==12
pushrod=b.import_step(ROOT/defs['pushrod']['step'].lstrip('/'))
for o in pushrods:
    s=pushrod.moved(poses[o['id']])
    volume=overlap_volume(block,s)
    if volume>.01:collisions.append({'a':o['id'],'b':'candidate-block','volume_mm3':volume})

# Each gasket quadrant is supported by the rail, with exact contact at localZ-1.5.
support_probes=[]
for x,y in [(-330,0),(330,0),(0,-50),(0,50)]:
    probe=MOUNT*b.Pos(x,y,-1.75)*b.Cylinder(.5,.4)
    volume=overlap_volume(block,probe);support_probes.append(volume)
assert min(support_probes)>.3,support_probes

out=Path('/tmp/truck-cover-block-study.step');b.export_step(block,out)
restored=b.import_step(out)
assert restored.is_valid and len(restored.solids())==1
assert abs(restored.volume/block.volume-1)<1e-5
report={'manifest_sha256':hashlib.sha256(manifest_path.read_bytes()).hexdigest(),
        'candidate_block_valid_single_solid':True,'step_round_trip':'pass',
        'candidate_parts':14,'pushrod_passages_checked':12,'collisions':collisions,
        'gasket_support_probes_mm3':support_probes,
        'installed_in_engine':False,'verified_production_fit':False,
        'bolt_engagement_envelope_mm':3.908,
        'limits':'Provisional casting opening and six support webs. Female threads, seal compression, bolt engagement adequacy and production coordinates remain unverified. Other surrounding engine parts are not checked here.'}
p=ROOT/'inventory/engine/pushrod-cover-interface-validation.json';p.write_text(json.dumps(report,indent=2)+'\n')
print(p.read_text(),flush=True)
assert not collisions,collisions
