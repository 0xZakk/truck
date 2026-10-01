"""Package isolated closure envelopes and the separate pump topology study."""
from pathlib import Path
import argparse,hashlib,json,tarfile
ROOT=Path(__file__).resolve().parents[1]
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--output',type=Path,required=True);args=parser.parse_args()
files=[]
for folder,name in [('block-closures-coverage-candidate','block-core-cup-mps126'),('block-closures-additional-candidate','block-core-cup-mps59a')]:
 base=ROOT/'cad/engine/generated'/folder
 files += [base/(name+'.step'),base/(name+'.glb'),base/'cup-section.png']
base=ROOT/'cad/engine/generated/oil-pump-topology-candidate'
for name in ('oil-pump-topology-housing','oil-pump-topology-pickup-gasket','oil-pump-topology-pickup-tube-flange'):
 files += [base/(name+'.step'),base/(name+'.glb')]
files.append(base/'topology-review.png')
hashes={str(p.relative_to(ROOT)):sha(p)for p in files}
with tarfile.open(args.output,'w:gz')as archive:
 for p in files:archive.add(p,arcname=str(p.relative_to(ROOT)),recursive=False)
assert all(sha(ROOT/p)==h for p,h in hashes.items())
r={'release_tag':'studies-2026-10-01-block-closures','asset':args.output.name,'sha256':sha(args.output),'size_bytes':args.output.stat().st_size,'files':len(files),'file_sha256':hashes,'required_base_release':'checkpoint-2026-09-30-neck-core','scope':'Two isolated free-envelope cup candidates and three illustrative oil-pump topology assets. No host bores, block discharge, placement, thread plugs or installed acceptance. No reference originals or owner photographs.','reproduction':'Source modules and checks in repository; public Melling catalog access required for original evidence re-review.'}
(ROOT/'docs/cad-block-closures-checkpoint.json').write_text(json.dumps(r,indent=2)+'\n');print({k:v for k,v in r.items()if k!='file_sha256'})
