"""Deterministic authored-only preservation; no publish, extraction or shared edits."""
from pathlib import Path
import json,hashlib,tarfile,gzip,io,subprocess
R=Path(__file__).resolve().parents[1]
G='cad/engine/generated/airbox-refined-20261002/'
PARTS=['online-airbox-duct-long','online-airbox-duct-short','online-airbox-joining-web','online-airbox-retainer']+[f'online-airbox-clamp-{i}-{kind}' for i in range(1,5) for kind in ['band','screw']]
ARTIFACTS=[G+n+ext for n in PARTS for ext in ['.step','.glb']]+[G+n for n in ['validation-stages.json','airbox-refined-20261002-source-view.png','airbox-refined-20261002-render.json','historical-native-loft.py','historical-native-loft.log','historical-relative-mesh-bounds-failure.log','historical-boundary-classifier.log']]
SOURCES=['cad/engine/airbox_refined_20261002.py','scripts/check-airbox-refined-20261002.py','scripts/check-airbox-refined-20261002-sections.py','scripts/render-airbox-refined-20261002.py','docs/components/airbox-refined-20261002-contract.md','docs/components/airbox-refined-20261002-handoff.md','reference/engine/airbox-refined-20261002-check.json','reference/engine/airbox-refined-20261002-sections.json','reference/engine/airbox-refined-20261002-delivery.json','scripts/airbox-refined-20261002-package.py','docs/components/airbox-refined-20261002-package-handoff.md']
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def row(p):return {'path':p,'sha256':sha(R/p),'size_bytes':(R/p).stat().st_size}
def check(mapping):
 for p,h in mapping.items():assert sha(R/p)==h,p
main=json.loads((R/'reference/engine/airbox-refined-20261002-check.json').read_text());check(main['inputs']);check(main['asset_hashes']);check(main['reused_clamps'])
sections=json.loads((R/'reference/engine/airbox-refined-20261002-sections.json').read_text());check(sections['inputs'])
render=json.loads((R/(G+'airbox-refined-20261002-render.json')).read_text());check(render['inputs']);assert sha(R/(G+'airbox-refined-20261002-source-view.png'))==render['output_sha256']
delivery=json.loads((R/'reference/engine/airbox-refined-20261002-delivery.json').read_text());check(delivery['files'])
old=json.loads((R/'reference/engine/online-airbox-duct-delivery.json').read_text());check(old['files'])
priorpath='docs/online-research-candidates-checkpoint.json';prior=json.loads((R/priorpath).read_text());pm={x['path']:x['sha256'] for x in prior['artifact_files']}
external={**main['inputs'],**main['reused_clamps'],**render['inputs']}
external={p:h for p,h in external.items() if p not in SOURCES and p not in ARTIFACTS}
for p,h in external.items():
 assert sha(R/p)==h,p
 if p.startswith('cad/engine/generated/'):assert pm[p]==h,(p,'predecessor mismatch')
O=R/'cad/engine/generated/airbox-refined-20261002-package';O.mkdir(exist_ok=True)
archive=O/'truck-airbox-refined-20261002.tar.gz'
with archive.open('wb') as raw:
 with gzip.GzipFile(filename='',mode='wb',fileobj=raw,mtime=0) as gz:
  with tarfile.open(fileobj=gz,mode='w') as tf:
   for p in sorted(ARTIFACTS):
    data=(R/p).read_bytes();info=tarfile.TarInfo(p);info.size=len(data);info.mtime=0;info.uid=info.gid=0;info.uname=info.gname='';info.mode=0o644;tf.addfile(info,io.BytesIO(data))
with tarfile.open(archive,'r:gz') as tf:
 assert tf.getnames()==sorted(ARTIFACTS)
 for member in tf:
  assert hashlib.sha256(tf.extractfile(member).read()).hexdigest()==sha(R/member.name),member.name
report={'status':'UNPUBLISHED; all source/member/prerequisite hashes verified','baseline':'54c2abf7aae73a8a5818321ee48ad81c8b7346ad','artifact_files':[row(p) for p in sorted(ARTIFACTS)],'source_files':[row(p) for p in SOURCES],'external_inputs':external,'prerequisite_metadata':row(priorpath),'prerequisite_archive':{'sha256':prior['archive']['sha256'],'size_bytes':prior['archive']['size_bytes'],'release':'https://github.com/0xZakk/truck/releases/tag/studies-2026-10-01-online-research','release_id':401293444,'verification':'Required member hashes match frozen predecessor metadata; previous archive not freshly reopened'},'archive':{'path':str(archive.relative_to(R)),'sha256':sha(archive),'size_bytes':archive.stat().st_size,'members':len(ARTIFACTS),'stream_member_verification':'PASS'},'exclusions':['All original public/owner photos, manuals and raw captures','All source-pixel composite images','Unrelated generated studies and shared manifests'],'limits':['Preservation only, no new CAD acceptance','All shape dimensions estimated; no vehicle installation','Historical logs/source distinctly retain failed attempts; final assets are current']}
(R/'docs/airbox-refined-20261002-package.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report['archive'],indent=2))
