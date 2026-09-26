#!/usr/bin/env python3
"""Replay coordinated intake adapters in isolated output; never rebuild canonical files."""
from pathlib import Path
import copy,hashlib,json,sys
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'cad/engine'))
import build123d as b
import full_engine as e
import intake_cap_coordination as coordination
import iac_attachment_integration as attachment
import throttle_plate_fasteners_integration as plates
import intake_exterior_integration as exterior
import iac_closure_integration as closure
import iac_electrical_integration as electrical
from assembly_math import transforms

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def vol(s):return sum(x.volume for x in s.solids()) if s else 0.
def main():
 path=ROOT/'inventory/engine/full-assembly.json';raw=path.read_bytes();m=json.loads(raw)
 assert closure.SOURCE_IDS[0] in m['sources'],'Install reviewed closure first'
 ids=set(coordination.CHANGED_IDS)|attachment.CHANGED_IDS|closure.CHANGED_IDS|{'throttle-shaft','throttle-plate','throttle-plate-screw-illustrative'}
 definitions={d['id']:d for d in m['definitions']};ids |= set(electrical.CHANGED_IDS);ids &= definitions.keys()
 bound={ROOT/definitions[i][k].lstrip('/') for i in ids for k in ('step','glb')}
 before={str(p.relative_to(ROOT)):sha(p) for p in bound}
 out=ROOT/'cad/engine/generated/intake-detail-replay';out.mkdir(exist_ok=True)
 e.STEP=out/'step';e.OUT=out/'models';e.STEP.mkdir(exist_ok=True);e.OUT.mkdir(exist_ok=True)
 e.defs[:]=copy.deepcopy(m['definitions']);e.occurrences[:]=copy.deepcopy(m['occurrences']);e.assemblies[:]=copy.deepcopy(m['assemblies']);e.shapes.clear()
 # Current installed input: upstream adapter regenerates the compact casting,
 # then exterior/closure restore their successors in the actual builder order.
 coordination.install(e.define,e.add,e.group,e.defs,e.occurrences,e.assemblies,e.shapes,m['mechanism'])
 attachment.install(e.define,e.add,e.group,e.defs,e.occurrences,e.assemblies,e.shapes)
 plates.install(e.define,e.add,e.defs,e.occurrences,e.assemblies,e.shapes)
 exterior.install(e.define,e.defs,e.occurrences,e.assemblies,e.shapes,m['mechanism'],e.OUT)
 closure.install(e.define,e.add,e.group,e.defs,e.occurrences,e.assemblies,e.shapes)
 electrical.install(e.define,e.add,e.group,e.defs,e.occurrences,e.assemblies,e.shapes)
 final=dict(m,definitions=e.defs,occurrences=e.occurrences,assemblies=e.assemblies)
 assert len(e.defs)==len(m['definitions']) and len(e.occurrences)==len(m['occurrences'])
 oldposes=transforms(m);newposes=transforms(final);rows=[]
 for i in sorted(ids):
  original=b.import_step(ROOT/definitions[i]['step'].lstrip('/'));actual=b.import_step(e.STEP/(i+'.step'))
  difference=vol(actual-original)+vol(original-actual);assert difference<.1,(i,difference)
  placed=[o for o in m['occurrences'] if o['definition']==i]
  for o in placed:assert attachment.frame_error(oldposes[o['id']],newposes[o['id']])<1e-6,o['id']
  rows.append(dict(definition=i,local_symmetric_difference_mm3=difference,occurrences=len(placed)))
 assert path.read_bytes()==raw
 for p,h in before.items():assert sha(ROOT/p)==h,p
 report=dict(status='PASS installed-input ordered adapter replay; not a clean whole-engine rebuild',manifest_sha256=sha(path),canonical_modified=False,definitions=len(e.defs),occurrences=len(e.occurrences),geometry=rows,input_artifact_sha256=before,source_sha256={str(Path(x.__file__).relative_to(ROOT)):sha(Path(x.__file__)) for x in [coordination,attachment,plates,exterior,closure,electrical]},checker_sha256=sha(Path(__file__)),exporter_sha256=sha(ROOT/'cad/engine/full_engine.py'),metrics_sha256=sha(ROOT/'cad/engine/cad_metrics.py'))
 (ROOT/'inventory/engine/intake-detail-replay-validation.json').write_text(json.dumps(report,indent=2)+'\n');print(report['status'])
if __name__=='__main__':main()
