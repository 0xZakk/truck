"""Hash owned pump candidate delivery; do not redistribute photographed originals."""
from pathlib import Path
import hashlib,json
R=Path(__file__).resolve().parents[1];P='pump-cover-candidate-20261003';out=R/f'reference/engine/{P}-resume-package.json';sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
authored=[]
for folder in ['scripts','reference/engine','docs/components']:
 authored.extend(p for p in (R/folder).glob(P+'*') if p.is_file() and p!=out)
authored.extend((R/'cad/engine').glob('pump_cover_candidate_20261003*.py'))
authored.extend((R/'kb/sources').glob('pump-deck-height-20261003*.md'));authored.extend((R/'kb/notes').glob('pump-deck-height-20261003*.md'))
excluded={R/'cad/engine/generated/pump-cover-candidate-20261003/deck-source-overlay.png'}
generated=[p for p in (R/'cad/engine/generated'/P).rglob('*') if p.is_file() and p not in excluded]
def row(p):return {'path':str(p.relative_to(R)),'sha256':sha(p),'bytes':p.stat().st_size}
deps={}
for p in authored:
 if p.suffix!='.json':continue
 try:j=json.loads(p.read_text())
 except ValueError:continue
 for key in ['inputs','inputs_sha256','input_sha256']:
  mapping=j.get(key,{})
  if not isinstance(mapping,dict):continue
  for rel,h in mapping.items():
   q=R/rel
   if q.exists() and q.is_file() and q not in authored and q not in generated:
    deps[rel]={'path':rel,'actual_sha256':sha(q),'reported_sha256':h,'matches':sha(q)==h,'policy':'Existing dependency; restore from existing checkpoint. Source images are review-only, not redistribution authorized.'}
r={'status':'SEPARATE LOCAL FLOW SUCCESSOR REVIEWED; full coupled candidate FAIL','baseline':'5584306a595f87b60b29eca9ea82b527ade5ae98','authored':[row(p) for p in sorted(set(authored))],'generated_artifacts':[row(p) for p in sorted(generated)],'existing_dependencies':list(deps.values()),'exclude_from_git_and_archive':[str(p.relative_to(R)) for p in excluded],'raw_source_policy':'Do not include Ford PDF or downloaded builder/seller photos. Public URLs, hashes and authored observations persist. Source-overlay contains seller pixels and is excluded.','review':'Root accepted separate analytic own-axis flow successor as candidate progress; no full hydraulic section/factory radius/installed acceptance; tube-minus-loft adaptive volume INCONCLUSIVE.','restore':'Restore original functional/cover/v4 dependencies via docs/CAD-ARTIFACTS.md, restore generated_artifacts preserving paths, run resume-audit then selected scripts from handoff. No personal/tmp file required.','processes':'No modeling/check process left running at checkpoint. CADViewer open for review.','usage':'Model/effort/token and billing measurements unavailable.'}
out.write_text(json.dumps(r,indent=2)+'\n');print(json.dumps({'authored':len(r['authored']),'generated':len(generated),'generated_bytes':sum(p.stat().st_size for p in generated),'existing_dependencies':len(deps),'excluded':r['exclude_from_git_and_archive']}))
