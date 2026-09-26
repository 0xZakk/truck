"""Conditional diagnostic: proposed outlet and pump station, not an installed belt."""
import json,hashlib,sys
from pathlib import Path
import build123d as cad
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'cad/engine'))
import accessory_belt as belt
import coolant_outlet_head_candidate as outlet
import alternator_carrier_1994_candidate as alt
import accessory_carrier_1994 as carrier

def shape(solution):
 span=solution['spans'][0]
 direction=(0,*((span['end'][i]-span['start'][i])/span['length'] for i in range(2)))
 plane=cad.Plane(origin=belt.world(span['start']),x_dir=(-1,0,0),z_dir=direction)
 return cad.sweep(plane*cad.Polygon(*belt.belt_section_points(),align=None),belt.path(solution),is_frenet=False)

results=[]
for pump_y in (0,-32):
 nodes=[dict(n) for n in belt.PULLEYS]
 nodes[0]['center']=alt.POSITION[1:];nodes[1]['center']=carrier.TENSIONER_POSITION[1:];nodes[4]['center']=(pump_y,170)
 solution=belt.solve(nodes);s=shape(solution)
 assert s.is_valid and len(s.solids())==1
 housing=cad.Pos(*outlet.POSITION)*outlet.housing()
 hit=s.intersect(housing);volume=sum(x.volume for x in hit.solids()) if hit else 0
 result={'pump_y_mm':pump_y,'cord_path_mm':solution['length'],'outside_radius_loop_mm':belt.solve(nodes,False)['length'],'outlet_overlap_mm3':volume,'outlet_distance_mm':s.distance_to(housing),'passes_outlet_only':volume<=.01}
 results.append(result);print(result,flush=True)
report={'status':'conditional-routing-diagnostic-only','installed_belt':False,'results':results,'candidate_sources_sha256':{Path(m.__file__).name:hashlib.sha256(Path(m.__file__).read_bytes()).hexdigest() for m in (belt,outlet,alt,carrier)},'limits':['PumpY−32 is an unintegrated coordinated pump candidate; originalY0 retained as comparison.','No belt effective gauge, nominal fit, arm travel, traction or full-engine clearance is verified.','This exact solid test isolates the prior coolant-outlet obstacle only; it does not accept a belt assembly.']}
(ROOT/'inventory/engine/revised-outlet-belt-clearance.json').write_text(json.dumps(report,indent=2)+'\n')
