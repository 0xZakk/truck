"""Focused outlet, attached takeoff and sensor QC before full-engine validation."""
import hashlib,json,sys
from pathlib import Path
import build123d as cad
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'cad/engine'))
import coolant_outlet_head_candidate as current
base=ROOT/'cad/engine/candidates/outlet-head-20260925/baseline'
parts={'housing':cad.Pos(*current.POSITION)*current.housing(),'heater-supply-ect-elbow':current.supply_elbow()}
for identifier in ['engine-coolant-temperature-body','engine-coolant-temperature-insulator','engine-coolant-temperature-thermistor','engine-coolant-temperature-terminal-1','engine-coolant-temperature-terminal-2']:
 definition='engine-coolant-temperature-terminal' if 'terminal' in identifier else identifier
 parts[identifier]=cad.Pos(*current.ect_position(identifier))*cad.import_step(base/(definition+'.step'))
def vol(s):return sum(x.volume for x in s.solids()) if s else 0
failures=[];pairs=0;keys=list(parts)
for i,k in enumerate(keys):
 assert parts[k].is_valid and len(parts[k].solids())==1,k
 for j in keys[i+1:]:
  pairs+=1;overlap=vol(parts[k].intersect(parts[j]))
  if overlap>.01:failures.append({'a':k,'b':j,'overlap_mm3':overlap})
contacts={name:parts['heater-supply-ect-elbow'].distance_to(parts[name]) for name in ('housing','engine-coolant-temperature-body')}
assert all(distance<1e-6 for distance in contacts.values())
flows={name:sum(vol(s.intersect(probe)) for s in parts.values()) for name,probe in current.flow_probes().items()}
assert all(v<1e-6 for v in flows.values())
report={'passed':not failures,'scope':'Focused seven-part coupling only; complete engine validation still required.','candidate_sha256':hashlib.sha256(Path(current.__file__).read_bytes()).hexdigest(),'exact_pairs':pairs,'failures':failures,'contact_gaps_mm':contacts,'flow_obstructions_mm3':flows}
(ROOT/'inventory/engine/coolant-outlet-sleeve-bore-correction-validation.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
assert not failures
