"""Freeze and package finite accessory studies. Never publish or extract."""
from pathlib import Path
import argparse,gzip,hashlib,json,tarfile,subprocess
R=Path(__file__).resolve().parents[1]
M=R/'docs/accessory-layout-checkpoint-draft.json'
SEEDS=['inventory/engine/'+x+'.json' for x in ['block-fs10-investigation-complete','block-fs10-source-datum-delivery','timing-right-contour-source-delivery','accessory-common-layout-discovery-delivery','accessory-constrained-layout-delivery','accessory-matched-carriers-delivery']]
# Legacy authored inputs cited by frozen delivery but absent from predecessor inventories.
SUPPLEMENTAL=[
 'cad/engine/generated/block.step',
 *['cad/engine/generated/timing-cover-joint-candidate/'+n for n in ['candidate-review.png','main-gasket.glb','main-gasket.step','preview.npz']],
 *['cad/engine/generated/timing-cover-registration-study/'+n for n in ['check.log','registration-preview.npz','registration-review.png','render.log']]]
EXCLUDED_GENERATED={'cad/engine/generated/timing-cover-front-joint-candidate/source-comparison.png','cad/engine/generated/timing-cover-joint-candidate/reference/dorman-635109-009.jpg'}
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def hashes(x):
 if isinstance(x,dict):
  for k,v in x.items():
   if isinstance(v,str) and len(v)==64 and all(c in '0123456789abcdef' for c in v) and '/' in k:yield k,v
   else:yield from hashes(v)
 elif isinstance(x,list):
  for v in x:yield from hashes(v)
def archive_rows(x):
 if isinstance(x,dict):
  if isinstance(x.get('path'),str) and isinstance(x.get('sha256'),str):yield x['path'],x['sha256']
  for v in x.values():yield from archive_rows(v)
 elif isinstance(x,list):
  for v in x:yield from archive_rows(v)
def prepare():
 owned=set(SEEDS);claims={};excluded=[]
 for seed in SEEDS:
  j=json.loads((R/seed).read_text())
  for field in ['owned_files_sha256','files_sha256','input_sha256']:
   for p,h in j.get(field,{}).items():
    if p.startswith('manuals/') or (p.startswith('reference/') and not p.endswith('.json')):
     excluded.append(dict(path=p,reason='source original/capture'));continue
    assert 'accessory-psac-carrier' not in p
    owned.add(p);claims.setdefault(p,set()).add(h)
 mismatches=[dict(path=p,expected=sorted(hs),actual=sha(R/p))for p,hs in claims.items()if sha(R/p) not in hs or len(hs)>1]
 assert not mismatches,mismatches
 owned.update(SUPPLEMENTAL)
 artifacts=sorted(p for p in owned if p.startswith('cad/engine/generated/'))
 sources=sorted(owned-set(artifacts))
 for p in artifacts:
  assert Path(p).suffix in {'.step','.glb','.ply','.png','.npz','.json','.log','.py','.txt'}
 # Only derivative plots/live meshes: scripts generating included PNGs do not read source pixels.
 images=[p for p in artifacts if p.endswith('.png')]
 metadata=sorted(R.glob('docs/*checkpoint*.json'))
 indexes={};prereqs=[]
 for path in metadata:
  if path==M:continue
  j=json.loads(path.read_text());tag=j.get('release_tag')
  if path.name=='waterpump-studies-checkpoint-draft.json':tag='waterpump draft (not yet published)'
  for p,h in list(archive_rows(j))+list(hashes(j)):indexes.setdefault((p,h),[]).append(str(path.relative_to(R)))
  prereqs.append(dict(path=str(path.relative_to(R)),sha256=sha(path),release_tag=tag,archive_sha256=j.get('sha256',j.get('archive',{}).get('sha256')),required_base_release=j.get('required_base_release'),required_base_archive_sha256=j.get('required_base_archive_sha256')))
 neck=R/'inventory/engine/waterpump-prerequisite-archive-audit.json'
 nj=json.loads(neck.read_text())
 for row in nj['members']:indexes.setdefault((row['path'],row['archive_member_sha256']),[]).append(str(neck.relative_to(R)))
 ext={}
 for p in owned:
  if not p.endswith('.json'):continue
  for target,h in hashes(json.loads((R/p).read_text())):
   if target in SUPPLEMENTAL:assert sha(R/target)==h,(target,h)
   if target not in owned:ext.setdefault(target,set()).add(h)
 external=[]
 for p,hs in sorted(ext.items()):
  local=R/p
  if p in EXCLUDED_GENERATED or p.startswith('manuals/') or (p.startswith('reference/') and not p.endswith('.json')):kind='excluded source original'
  elif p.startswith('cad/engine/generated/'):
   kind='prerequisite metadata/member-audit match' if all((p,h) in indexes for h in hs) else 'UNRESOLVED artifact prerequisite'
  else:kind='repository input'
  external.append(dict(path=p,expected_hashes=sorted(hs),local_sha256=sha(local)if local.is_file()else None,local_matches_all=local.is_file()and all(sha(local)==h for h in hs),classification=kind,matching_prerequisite_records=sorted({a for h in hs for a in indexes.get((p,h),[])})))
 row=lambda p:dict(path=p,sha256=sha(R/p),size_bytes=(R/p).stat().st_size)
 by_tag={p['release_tag']:p for p in prereqs if p['release_tag']}
 chain=[];node=next(p for p in prereqs if p['path']=='docs/waterpump-studies-checkpoint-draft.json')
 while node.get('required_base_release'):
  parent=by_tag[node['required_base_release']]
  assert parent['archive_sha256']==node['required_base_archive_sha256']
  chain.append(dict(release_tag=parent['release_tag'],archive_sha256=parent['archive_sha256'],metadata=parent['path']))
  node=parent
 j=dict(prerequisite_chain_in_reverse_restore_order=chain,supplemental_legacy_inputs=SUPPLEMENTAL,baseline_commit=subprocess.check_output(['git','rev-parse','HEAD'],cwd=R,text=True).strip(),packaging_script=dict(path=str(Path(__file__).relative_to(R)),sha256=sha(__file__)),status='DRAFT frozen archive; publication root-owned',asset='truck-accessory-layout-studies-20261001.tar.gz',scope='Block-FS10 source/datum/contour and common/constrained layout; matched ALT/AP carriers through trial 6 including rejected trials; no installation',artifact_files=[row(p)for p in artifacts],source_report_handoff_files=[row(p)for p in sources],frozen_delivery_bindings_verified=len(claims),exclusions=excluded+[dict(path=p,reason='source image or composite containing source pixels')for p in sorted(EXCLUDED_GENERATED)]+['All active accessory-psac-carrier files','Original photographs/manuals/catalogs and reference image composites'],image_provenance=[dict(path=p,kind='project-authored geometry/landmark plot; no original source pixels')for p in images],prerequisite_metadata=prereqs,external_report_inputs=external,required_base='Waterpump study draft plus its full neck-core/timing/ignition predecessor chain; waterpump publication must resolve before accessory release restore instructions are final',limits=['Prerequisite matching uses exact metadata/member-audit hashes; does not claim every predecessor archive freshly opened','Excluded originals remain separately authorized source dependencies','No full clean-clone CAD rerun or installed acceptance'])
 M.write_text(json.dumps(j,indent=2)+'\n')
def build(verify_only):
 j=json.loads(M.read_text());assert sha(R/j['packaging_script']['path'])==j['packaging_script']['sha256']
 for row in j['prerequisite_metadata']:
  assert sha(R/row['path'])==row['sha256']
 for row in j['external_report_inputs']:
  if row['local_sha256'] is not None:assert sha(R/row['path'])==row['local_sha256']
 rows=j['artifact_files'];names=[r['path']for r in rows]
 assert names==sorted(set(names))
 for row in rows+j['source_report_handoff_files']:
  p=R/row['path'];assert not p.is_symlink();assert sha(p)==row['sha256'];assert p.stat().st_size==row['size_bytes']
 out=R/'cad/engine/generated/accessory-layout-checkpoint'/j['asset']
 if not verify_only:
  out.parent.mkdir(exist_ok=True)
  with out.open('wb')as raw,gzip.GzipFile(filename='',mode='wb',fileobj=raw,mtime=0)as gz,tarfile.open(fileobj=gz,mode='w')as tar:
   for row in rows:
    p=row['path'];assert p.startswith('cad/engine/generated/')and'accessory-psac-carrier'not in p
    info=tarfile.TarInfo(p);info.size=row['size_bytes'];info.mode=0o644;info.mtime=0
    with (R/p).open('rb')as f:tar.addfile(info,f)
 with tarfile.open(out,'r|gz')as tar:
  seen=[]
  for member in tar:
   row=rows[len(seen)];assert member.name==row['path']and member.isfile();h=hashlib.sha256()
   with tar.extractfile(member)as f:
    for chunk in iter(lambda:f.read(1048576),b''):h.update(chunk)
   assert h.hexdigest()==row['sha256'];seen.append(member.name)
  assert seen==names
 result=dict(path=str(out.relative_to(R)),sha256=sha(out),size_bytes=out.stat().st_size,files=len(rows),source_files_verified=len(j['source_report_handoff_files']),member_verification='PASS',publication='NOT RUN')
 if verify_only:assert j['archive']==result
 else:j['archive']=result;M.write_text(json.dumps(j,indent=2)+'\n')
 print(json.dumps(result))
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--prepare',action='store_true');p.add_argument('--verify-only',action='store_true');a=p.parse_args()
 if a.prepare:prepare()
 build(a.verify_only)
