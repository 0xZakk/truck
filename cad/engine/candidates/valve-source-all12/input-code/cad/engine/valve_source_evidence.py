"""Source-v2 presentation/evidence annotations, separate from geometry authority."""
from copy import deepcopy
from pathlib import Path
import hashlib
ROOT=Path(__file__).resolve().parents[2]
SOURCES={
 'melling-valve-progressive-size-chart-2025':{'title':'Melling stock replacement valve progressive size chart','url':'https://melling.com/wp-content/uploads/2025/05/Stock-Replacement-Valve-Progressive-Size-Chart.pdf','path':'reference/engine/valve-layout/melling-2025-valve-progressive-size-chart.pdf'},
 'melling-jb900-lifter-envelope':{'title':'Melling JB-900 manufacturer specification response','url':'https://specsearch.melling.com/','path':'reference/engine/valve-layout/melling-jb900-details.html'},
 'melling-cam-lifter-kit-chart':{'title':'Melling camshaft/lifter/rocker arm kit identification chart July2023','url':'https://specsearch.melling.com/PDF/Camshaft%20Lifter-Rocker%20Arm%20Kit%20ID%20Chart%2007-2023.pdf','path':'reference/engine/valve-layout/melling-cam-lifter-kit-chart.pdf'},
}
for row in SOURCES.values():row['sha256']=hashlib.sha256((ROOT/row['path']).read_bytes()).hexdigest()

def annotate_evidence(manifest):
 result=deepcopy(manifest);result.setdefault('sources',{}).update(deepcopy(SOURCES))
 for d in result['definitions']:
  d['unresolved']=[s for s in d.get('unresolved',[]) if not s.startswith('The current pushrod is226.6mm') and not s.startswith('Valve head diameters compare Melling V1504/V1505')]
  if d['id'] in ['intake-valve','exhaust-valve','pushrod','rocker-arm','lifter-body','cylinder-head','intake-spring','exhaust-spring']:
   notes=['Source-sized replacement envelopes are not installed-part identification. Absolute cam/deck/station datums, lifter socket/internal offsets and rocker geometry remain assumptions.','Guide bore and separate spring load-test heights are service-reference constraints; spring wire/turns, keeper/groove construction and casting contours remain illustrative.']
   for note in notes:
    if note not in d['unresolved']:d['unresolved'].append(note)
  if d['id'] in ['intake-valve','exhaust-valve']:
   kind=d['id'].split('-')[0];d['source_constraints_mm']={'overall_length':120.6246 if kind=='intake' else 120.65,'stem_diameter':8.6868,'head_diameter':45.2882 if kind=='intake' else 39.5986}
   d['sources']=list(dict.fromkeys(d.get('sources',[])+['melling-valve-progressive-size-chart-2025']))
  elif d['id']=='pushrod':
   d['function']='Transfers lifter motion to the rocker and provides an oil route. The replacement catalog constrains overall length257.556mm and diameter7.9248mm; drilled spherical end shape and absolute installed datums remain illustrative.'
   d['source_constraints_mm']={'overall_length':257.556,'outside_diameter':7.9248};d['sources']=list(dict.fromkeys(d.get('sources',[])+['melling-pushrod-specifications']))
  elif d['id']=='lifter-body':
   d['source_constraints_mm']={'body_length':50.8,'maximum_body_diameter':22.1996};d['sources']=list(dict.fromkeys(d.get('sources',[])+['melling-jb900-lifter-envelope','melling-cam-lifter-kit-chart']))
  elif d['id'] in ['intake-spring','exhaust-spring']:
   d['source_constraints_mm']={'closed_load_test_height':41.656 if d['id']=='intake-spring' else 37.338}
   d['sources']=list(dict.fromkeys(d.get('sources',[])+['fsm-2e5473b2bf99']))
   d['function']='Returns the valve toward its seat. Separate intake/exhaust closed load-test heights follow the service reference; coil geometry, rate and spring dynamics are illustrative. Ground ends maintain contact in the teaching motion.'
 return result
