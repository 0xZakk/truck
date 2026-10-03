"""Deterministic authored screw supplement; excludes source-original pixels/PDF."""
from pathlib import Path
import tarfile,gzip,io,json,hashlib
R=Path(__file__).resolve().parents[1];O=R/'cad/engine/generated/airbox-screw-online-20261002'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
owned=['cad/engine/airbox_screw_online_20261002.py','docs/components/airbox-screw-online-20261002-contract.md','docs/components/airbox-screw-online-20261002-handoff.md','scripts/check-airbox-screw-online-20261002.py','scripts/check-airbox-screw-online-20261002-replay.py','scripts/render-airbox-screw-online-20261002.py','scripts/package-airbox-screw-online-20261002.py','reference/engine/airbox-screw-online-20261002-validation.json','reference/engine/airbox-screw-online-20261002-replay.json']
deps=['cad/engine/pan_fastener_thread_candidate.py','cad/requirements-engine-lock.txt','reference/engine/airbox-host-online-20261002.json','docs/components/airbox-host-online-20261002-contract.md','kb/sources/airbox-host-online-20261002-screw.md','kb/sources/airbox-host-online-20261002-service.md','kb/notes/airbox-host-online-20261002-screw-envelope.md']
files=sorted(set(owned+deps+[str(p.relative_to(R)) for p in O.iterdir() if p.is_file() and not p.name.endswith('.tar.gz')]))
for report in ['reference/engine/airbox-screw-online-20261002-validation.json','reference/engine/airbox-screw-online-20261002-replay.json']:
 d=json.loads((R/report).read_text())
 for p,h in (d['inputs']|d.get('asset_hashes',{})).items():assert sha(R/p)==h,p
archive=O/'airbox-screw-online-20261002-authored.tar.gz'
with archive.open('wb') as raw:
 with gzip.GzipFile(filename='',fileobj=raw,mode='wb',mtime=0) as gz:
  with tarfile.open(fileobj=gz,mode='w',format=tarfile.PAX_FORMAT) as tf:
   for p in files:
    data=(R/p).read_bytes();info=tarfile.TarInfo(p);info.size=len(data);info.mtime=0;info.mode=0o644;info.uid=info.gid=0;tf.addfile(info,io.BytesIO(data))
report={'schema_version':1,'baseline':'4f1fe9da2ec177e1ff61668df66ca422e37b0b7c','readiness':'candidate; no installed pose','archive':str(archive.relative_to(R)),'archive_sha256':sha(archive),'archive_bytes':archive.stat().st_size,'release_url':None,'publication_status':'LOCAL; root to publish','members':{p:{'sha256':sha(R/p),'bytes':(R/p).stat().st_size} for p in files},'source_and_build_dependencies':deps,'original_source_images_included':False,'restoration':'Verify archive SHA, extract at repository root; verify each member; do not replace newer shared dependency files without review. Build needs repository CAD lock and renderer matplotlib3.10.9. Source catalog URL/hash in host ledger; original pixels not a build dependency.'}
(R/'reference/engine/airbox-screw-online-20261002-delivery.json').write_text(json.dumps(report,indent=2)+'\n');print(len(files),'members',report['archive_bytes'],report['archive_sha256'])
