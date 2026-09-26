"""Frozen conditional belt diagnostic against connected outlet and pump candidates.

Never installs a belt or optimizes station coordinates. All radii/coordinates
retain their existing uncertainty; catalog effective length is comparison only.
"""
import hashlib,json,sys
from pathlib import Path
import build123d as cad
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'cad/engine'))
import accessory_belt as belt
import accessory_belt_profile as profile
import coolant_outlet_head_candidate as outlet
import alternator_carrier_1994_candidate as alt
import accessory_carrier_1994 as carrier
import water_pump_joint_candidate as pump
import water_pump_inlet_v3_candidate as inlet
base=ROOT/'cad/engine/candidates/outlet-head-20260925/baseline'
files={}
def read(path):
 raw=path.read_bytes();files[str(path)]=hashlib.sha256(raw).hexdigest();return raw
for module in (belt,profile,outlet,alt,carrier,pump,inlet):read(Path(module.__file__))
m=json.loads(read(base/'manifest.json'));local=outlet.parts();mount=cad.Pos(*outlet.POSITION);obstacles={}
def load(d):
 path=base/(d+'.step');read(path);return cad.import_step(path)
for o in m['occurrences']:
 d=o['definition'];identifier=o['id']
 if d in local:
  if d=='heater-supply-ect-elbow':s=local[d]
  elif d=='thermostat-piston':s=mount*cad.Pos(*outlet.THERMOSTAT_POSITION)*local[d]
  elif d=='coolant-outlet-bolt':
   y,z=outlet.HOLES[int(identifier.rsplit('-',1)[1])-1];s=mount*cad.Pos(0,y,z)*local[d]
  else:s=mount*local[d]
 elif o['parent']=='thermostat-assembly':s=mount*cad.Pos(*outlet.THERMOSTAT_POSITION)*load(d)
 elif o['parent']=='engine-coolant-temperature-assembly':s=cad.Pos(*outlet.ect_position(identifier))*load(d)
 else:continue
 obstacles[identifier]=s
# The head itself is far behind the belt plane; include the accepted receiver nevertheless.
obstacles['cylinder-head']=cad.Pos(0,0,255.5)*outlet.head_interface(load('cylinder-head'))
path=ROOT/'cad/engine/generated/water-pump-housing.step';read(path)
pump_housing=inlet.housing_interface(pump.housing_interface(cad.import_step(path)))
obstacles['water-pump-housing-with-inlet-v3']=cad.Pos(*pump.PUMP_POSITION)*pump_housing
assert len(obstacles)==21,len(obstacles)
nodes=[dict(n) for n in belt.PULLEYS]
nodes[0]['center']=alt.POSITION[1:];nodes[1]['center']=carrier.TENSIONER_POSITION[1:];nodes[4]['center']=pump.PUMP_POSITION[1:]
solution=belt.solve(nodes);first=solution['spans'][0]
direction=(0,*((first['end'][i]-first['start'][i])/first['length'] for i in range(2)))
plane=cad.Plane(origin=belt.world(first['start']),x_dir=(-1,0,0),z_dir=direction)
swept=cad.sweep(plane*cad.Polygon(*belt.belt_section_points(),align=None),belt.path(solution),is_frenet=False)
assert swept.is_valid and len(swept.solids())==1
checks=[]
for name,s in obstacles.items():
 hit=swept.intersect(s);volume=sum(q.volume for q in hit.solids()) if hit else 0
 row={'id':name,'overlap_mm3':volume,'minimum_distance_mm':swept.distance_to(s),'passes':volume<=.01}
 checks.append(row);print(row,flush=True)
# Finite-difference sensitivities diagnose scale; these hypothetical perturbations
# are not fit suggestions and are never emitted as replacement stations.
sensitivities=[]
for index,n in enumerate(nodes):
 shifted=[dict(v) for v in nodes];shifted[index]['radius']+=1
 sensitivities.append({'id':n['id'],'length_change_per_plus1mm_radius':belt.solve(shifted,False)['length']-belt.solve(nodes,False)['length']})
assert all(hashlib.sha256(Path(p).read_bytes()).hexdigest()==h for p,h in files.items()),'Inputs mutated'
report={'status':'rejected-conditional-belt' if any(not r['passes'] for r in checks) else 'conditional-obstacle-clear-only','installed':False,'tested_obstacles':len(checks),'checks':checks,'nodes':nodes,'outside_radius_loop_mm':belt.solve(nodes,False)['length'],'illustrative_cord_path_mm':solution['length'],'catalog_comparison_effective_length_mm':profile.NOMINAL_EFFECTIVE_LENGTH,'outside_radius_residual_vs_catalog_mm':belt.solve(nodes,False)['length']-profile.NOMINAL_EFFECTIVE_LENGTH,'radius_sensitivities':sensitivities,'solution':solution,'input_sha256':files,'limits':['Uses frozen 4b847 head/thermostat/ECT definitions, accepted outlet9aea module, and original main pump housing with pump+inlet adapters; no installed belt acceptance.','All 20 outlet components plus pump housing/inlet tested; remaining engine obstacles, pulley traction, travel, dynamic clearance and accurate pitch gauge remain outside this diagnostic.','Ford TSB identifies E8TZ8620T/JK6-984-B; 2491mm comes from Gates replacement comparison and is not independently a measurement of that Ford belt.','No station or radius adjusted to force fit. Source-supported topology does not supply manufacturing coordinates.']}
(ROOT/'inventory/engine/connected-outlet-pump-belt-validation.json').write_text(json.dumps(report,indent=2)+'\n')
print(report['status'],report['outside_radius_loop_mm'],report['illustrative_cord_path_mm'],flush=True)
