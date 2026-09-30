"""Package frozen isolated studies; restore the named engine archive first."""
from pathlib import Path
import argparse,hashlib,json,tarfile
ROOT=Path(__file__).resolve().parents[1]
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
FOLDERS=('timing-block-migration-candidate','timing-block-axis-feature-candidate','timing-cover-front-joint-candidate','timing-gear-backlash-candidate','timing-studies-checkpoint')
OWN_IMAGES={'block-render.png','side-cover-sections.png','candidate-review.png','terminal-contact-review.png'}
LOGS=('timing-block-axis-feature-check-empty-compound.log','timing-block-axis-feature-check-shapelist.log','timing-block-axis-feature-check-stale-input.log','timing-block-axis-feature-check.log','timing-block-baseline-check.log','timing-block-core-interface-check.log','timing-block-side-cover-conflict.log')
def main():
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--output',type=Path,required=True);a=p.parse_args()
 base=json.loads((ROOT/'docs/cad-neck-core-checkpoint.json').read_text())
 manifest=ROOT/'inventory/engine/full-assembly.json';digest=sha(manifest)
 assert digest==base['manifest_sha256'],'Current engine no longer matches required base'
 files=[]
 for folder in FOLDERS:
  d=ROOT/'cad/engine/generated'/folder;assert d.is_dir(),d
  for f in d.rglob('*'):
   if not f.is_file() or f.is_symlink() or any(q in f.parts for q in ('__pycache__','mpl','.cache')):continue
   if 'source-comparison' in f.name or 'reference' in f.name:continue
   if f.suffix.lower() in ('.png','.jpg','.jpeg','.webp','.pdf','.heic') and f.name not in OWN_IMAGES:continue
   if f.suffix.lower() not in ('.json','.step','.glb','.npz','.log','.py','.png'):continue
   files.append(f)
 files += [ROOT/'cad/engine/generated'/n for n in LOGS]
 files=sorted(set(files));hashes={str(f.relative_to(ROOT)):sha(f) for f in files}
 assert all(name.startswith('cad/engine/generated/') for name in hashes)
 with tarfile.open(a.output,'w:gz') as t:
  for f in files:t.add(f,arcname=str(f.relative_to(ROOT)),recursive=False)
 assert all(sha(ROOT/n)==h for n,h in hashes.items()) and sha(manifest)==digest
 r=dict(release_tag='studies-2026-09-30-timing-fit',asset=a.output.name,sha256=sha(a.output),size_bytes=a.output.stat().st_size,files=len(files),required_base_release=base['release_tag'],required_base_archive_sha256=base['sha256'],manifest_sha256=digest,scope='Isolated studies only: exact block baseline, failed first block axis migration, reviewed estimated cover/pan joint and revised backlash pair with explicit ledger rebind. No canonical installation. Restore neck-core base first. Excludes source originals/composites, manuals/photos and active fixed-stock, attachment and coupled-core work.',file_sha256=hashes)
 (ROOT/'docs/cad-timing-studies-checkpoint.json').write_text(json.dumps(r,indent=2)+'\n')
 print(json.dumps({k:v for k,v in r.items() if k!='file_sha256'},indent=2))
if __name__=='__main__':main()
