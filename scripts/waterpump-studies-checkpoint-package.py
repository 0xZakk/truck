"""Package only the frozen, hash-bound project-artifact allowlist. No publishing."""
from pathlib import Path
import argparse,gzip,hashlib,io,json,tarfile
R=Path(__file__).resolve().parents[1]
M=R/'docs/waterpump-studies-checkpoint-draft.json'
def sha(data): return hashlib.sha256(data).hexdigest()
def main():
 parser=argparse.ArgumentParser();parser.add_argument('--verify-only',action='store_true');args=parser.parse_args()
 j=json.loads(M.read_text());out=R/'cad/engine/generated/waterpump-studies-checkpoint'/j['asset'];rows=j['artifact_files']; names=[x['path'] for x in rows]
 assert len(names)==len(set(names)) and names==sorted(names)
 for row in rows:
  p=Path(row['path']);assert not p.is_absolute() and '..' not in p.parts and str(p).startswith('cad/engine/generated/')
  assert p.suffix in {'.step','.glb','.png','.npz','.json','.log'}
  assert not (R/p).is_symlink();data=(R/p).read_bytes();assert sha(data)==row['sha256'] and len(data)==row['size_bytes'],str(p)
 for row in j['source_report_handoff_files']:
  assert sha((R/row['path']).read_bytes())==row['sha256'],row['path']
 if not args.verify_only:
  out.parent.mkdir(parents=True,exist_ok=True)
  with out.open('wb') as raw,gzip.GzipFile(filename='',mode='wb',fileobj=raw,mtime=0) as gz,tarfile.open(fileobj=gz,mode='w',format=tarfile.PAX_FORMAT) as tar:
   for row in rows:
    data=(R/row['path']).read_bytes();info=tarfile.TarInfo(row['path']);info.size=len(data);info.mode=0o644;info.mtime=0;info.uid=info.gid=0;info.uname=info.gname='';tar.addfile(info,io.BytesIO(data))
 with tarfile.open(out,'r:gz') as tar:
  members=tar.getmembers();assert [x.name for x in members]==names
  for member,row in zip(members,rows):
   assert member.isfile();data=tar.extractfile(member).read();assert len(data)==row['size_bytes'] and sha(data)==row['sha256']
 result={'archive_path':str(out.relative_to(R)),'sha256':sha(out.read_bytes()),'size_bytes':out.stat().st_size,'files':len(rows),'uncompressed_file_bytes':sum(x['size_bytes']for x in rows),'archive_member_hash_verification':'PASS','source_report_hash_verification':'PASS','publication':'NOT RUN; root-owned','packaging_script_sha256':sha(Path(__file__).read_bytes())}
 if args.verify_only:
  assert j['archive']==result,'Archive summary differs'
 else:
  j['archive']=result;M.write_text(json.dumps(j,indent=2)+'\n')
 print(json.dumps(result,indent=2))
if __name__=='__main__':main()
