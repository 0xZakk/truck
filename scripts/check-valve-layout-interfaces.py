"""Positive contact/material checks for the isolated candidate seat and load path."""
from pathlib import Path
import sys,json,math,hashlib
import build123d as b
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'cad/engine'))
from valve_layout_candidate import OUT,BASE,VALVE_Y,VALVE_RADII,PIVOT_Y,intersect_volume
layout=json.loads((OUT/'occurrence-layout.json').read_text());parts={};hashes={}
for o in layout['occurrences']:
    name=o['definition'];path=OUT/(name+'.step')
    if not path.exists():path=BASE/(name+'.step')
    hashes[str(path.relative_to(ROOT))]=hashlib.sha256(path.read_bytes()).hexdigest()
    parts[o['id']]=b.Pos(*o['position'])*b.Rot(*o['orientation'])*b.import_step(path)
contacts=[];probes=[];failures=[]
for kind,x in zip(['intake','exhaust'],layout['stations']):
    tag=f'c1-{kind}';r=VALVE_RADII[kind]-1.1;z=255.5+7.6
    for deg in range(0,360,45):
        a=math.radians(deg);point=b.Vertex(x+r*math.cos(a),VALVE_Y+r*math.sin(a),z)
        distances=[point.distance_to(parts[name]) for name in ['cylinder-head',tag+'-valve']]
        contacts.append({'kind':kind,'azimuth_deg':deg,'point_distances_mm':distances})
        if max(distances)>1e-5:failures.append(contacts[-1])
        for direction in [-1,1]:
            delta=direction*.15/math.sqrt(2)
            probe=b.Pos(x+(r+delta)*math.cos(a),VALVE_Y+(r+delta)*math.sin(a),z+delta)*b.Sphere(.04)
            head_fill=intersect_volume(probe,parts['cylinder-head'])/probe.volume
            valve_fill=intersect_volume(probe,parts[tag+'-valve'])/probe.volume
            item={'kind':kind,'azimuth_deg':deg,'direction':direction,'head_fraction':head_fill,'valve_fraction':valve_fill};probes.append(item)
            expected_head=1 if direction==1 else 0
            if abs(head_fill-expected_head)>.01 or abs(valve_fill-(1-expected_head))>.01:failures.append(item)
    for a,c in [(tag+'-guide','cylinder-head'),(tag+'-fulcrum',tag+'-guide'),(tag+'-rocker-bolt',tag+'-fulcrum')]:
        distance=parts[a].distance_to(parts[c]);contacts.append({'a':a,'b':c,'distance_mm':distance})
        if distance>1e-5:failures.append(contacts[-1])
assert all(hashlib.sha256((ROOT/p).read_bytes()).hexdigest()==h for p,h in hashes.items())
report={'status':'PASS local contact and material probes' if not failures else 'FAIL local interface probes',
 'source_step_hashes':hashes,'seat_and_load_path_contact_checks':len(contacts),'positive_material_probes':len(probes),
 'contacts':contacts,'probes':probes,'failures':failures,'source_limits':'Nominal contact of assumed geometry; not seal performance, measured production casting or force analysis.'}
(OUT/'interface-validation.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
if failures:sys.exit(1)
