"""Deterministic isolated HO2S authored package; no source-original media."""
from pathlib import Path
import hashlib,json,gzip,tarfile,io
R=Path(__file__).resolve().parents[1];O=R/'cad/engine/generated/ho2s-specimen-20261003';sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
owned=['cad/engine/ho2s_specimen_20261003.py','docs/components/ho2s-specimen-20261003-contract.md','docs/components/ho2s-specimen-20261003-handoff.md','scripts/check-ho2s-specimen-20261003.py','scripts/replay-ho2s-specimen-20261003.py','scripts/render-ho2s-specimen-20261003.py','scripts/package-ho2s-specimen-20261003.py','reference/engine/ho2s-specimen-20261003-pre-cad.json','reference/engine/ho2s-specimen-20261003-contract-amendment.json','reference/engine/ho2s-specimen-20261003-validation.json','reference/engine/ho2s-specimen-20261003-replay.json']
ledgers=['reference/engine/ho2s-online-20261003-delivery.json','reference/engine/ho2s-dimensions-20261003-delivery.json'];deps=['cad/engine/pan_fastener_thread_candidate.py','cad/requirements-engine-lock.txt']+ledgers
for f in ledgers:
 d=json.loads((R/f).read_text());members=d.get('files',d.get('authored_files_sha256',{}))
 for p,h in members.items():
  assert sha(R/p)==(h['sha256'] if isinstance(h,dict) else h),p
  deps.append(p)
for f in ['reference/engine/ho2s-specimen-20261003-validation.json','reference/engine/ho2s-specimen-20261003-replay.json','cad/engine/generated/ho2s-specimen-20261003/render.json']:
 d=json.loads((R/f).read_text())
 for p,h in (d['inputs']|d.get('asset_hashes',{})|d.get('outputs',{})).items():assert sha(R/p)==h,p
files=sorted(set(owned+deps+[str(p.relative_to(R)) for p in O.iterdir() if p.is_file() and not p.name.endswith('.tar.gz')]))
assert not any(p.endswith(('.jpg','.pdf','.html')) for p in files)
archive=O/'ho2s-specimen-20261003-authored.tar.gz'
with archive.open('wb') as raw:
 with gzip.GzipFile(filename='',fileobj=raw,mode='wb',mtime=0) as gz:
  with tarfile.open(fileobj=gz,mode='w',format=tarfile.PAX_FORMAT) as tf:
   for p in files:
    data=(R/p).read_bytes();i=tarfile.TarInfo(p);i.size=len(data);i.mtime=0;i.mode=0o644;i.uid=i.gid=0;tf.addfile(i,io.BytesIO(data))
report={'schema_version':1,'baseline':'4f2760612a18e597da5e6df15e27b6b9ae69ac6c','readiness':'isolated estimated exterior candidate; no installed acceptance','archive':str(archive.relative_to(R)),'archive_sha256':sha(archive),'archive_bytes':archive.stat().st_size,'release_url':None,'publication_status':'LOCAL; integration owner to publish','members':{p:{'sha256':sha(R/p),'bytes':(R/p).stat().st_size} for p in files},'owned_authored_files':owned,'source_and_build_dependencies':sorted(set(deps)),'generated_predecessor_required':False,'original_source_images_included':False,'restoration':'Verify archive SHA; inspect members and preserve newer shared dependency files before extraction at repository root. Restore the project CAD lock for CAD commands. Renderer uses system NumPy/Matplotlib, recorded in render.json. Original public source photos require separate URL/hash retrieval for visual re-review; they are not geometry build dependencies.','checks':{'prior_20_authored_files_unchanged':True,'region_exports':27,'max_bounds_error_mm':.0021249130368232727,'saved_step_and_glb_thread_probes':48,'saved_step_and_glb_slot_void_probes':36,'same_frame_overlap_pairs':169,'original_thresholds_preserved':True,'installed':'NOT RUN','browser':'NOT RUN'},'running_processes':[]}
(R/'reference/engine/ho2s-specimen-20261003-delivery.json').write_text(json.dumps(report,indent=2)+'\n');print(len(files),'members',report['archive_bytes'],report['archive_sha256'])
