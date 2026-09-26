"""Exact sampled motion on isolated candidate STEP + snapshotted saved neighbors."""
from pathlib import Path
import hashlib,json,math,sys
import build123d as b
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'cad/engine'))
from valve_layout_candidate import OUT,BASE,PIVOT_Y,PIVOT_Z,VALVE_Y,solve,intersect_volume,box_overlap
from assembly_math import transforms
m=json.loads((BASE/'manifest.json').read_text());layout=json.loads((OUT/'occurrence-layout.json').read_text())
provenance=json.loads((OUT/'provenance.json').read_text())
assert not provenance['failures'],'Static candidate must pass before motion audit'
occ={o['id']:o for o in m['occurrences']};defs={};static={};source_hashes={}
for o in layout['occurrences']:
    name=o['definition'];path=OUT/(name+'.step')
    if not path.exists():path=BASE/(name+'.step')
    if name not in defs:
        defs[name]=b.import_step(path);source_hashes[str(path.relative_to(ROOT))]=hashlib.sha256(path.read_bytes()).hexdigest()
    static[o['id']]=b.Pos(*o['position'])*b.Rot(*o['orientation'])*defs[name]


def lift(crank,kind):
    center=468 if kind=='intake' else 246
    offset=(crank-center+360)%720-360
    t=offset/135
    if abs(t)>=1:return 0.
    u=96/135;k=-math.log(.05/.247)*(1-u*u)/(u*u)
    return .247*25.4*math.exp(-k*t*t/(1-t*t))


def spring_shape(height):
    path=b.Helix(height/6,height,13)
    return b.sweep(b.Plane(origin=path@0,z_dir=path%0)*b.Circle(2),path=path)


def contact_pair(parts,a,c,angle,contacts,failures):
    distance=parts[a].distance_to(parts[c]);contacts.append({'crank_deg':angle,'a':a,'b':c,'gap_mm':distance})
    if distance>.002:failures.append({'crank_deg':angle,'a':a,'b':c,'contact_gap_mm':distance})

angles=[0,111,150,180,210,246,282,333,342,360,372,420,468,516,540,564,603,720]
if '--peaks' in sys.argv:angles=[0,246,468]
checks=0;failures=[];contacts=[];max_closure=0;min_coil_gap=999;max_pad_slide=0
for angle in angles:
    parts=dict(static);moving=set();rigid={};loc=transforms(m,angle)
    parts['camshaft']=defs['camshaft'].moved(loc['camshaft']);moving.add('camshaft')
    parts['c1-piston-1']=defs[occ['c1-piston-1']['definition']].moved(loc['c1-piston-1']);moving.add('c1-piston-1')
    for kind,x in zip(['intake','exhaust'],layout['stations']):
        tag=f'c1-{kind}';height=lift(angle,kind);state=solve(height);t=state['angle'];vl=state['valve_lift']
        max_closure=max(max_closure,abs(state['closure_error']));min_coil_gap=min(min_coil_gap,(51-vl)/6-4)
        pad_y=PIVOT_Y-(PIVOT_Y-VALVE_Y)*math.cos(t)+1.5*math.sin(t)
        max_pad_slide=max(max_pad_slide,abs(pad_y-VALVE_Y))
        assert abs(pad_y-VALVE_Y)<4.5,'Curved pad contact leaves valve stem tip'
        parts[tag+'-rocker']=b.Pos(x,PIVOT_Y,PIVOT_Z)*b.Rot(math.degrees(t),0,0)*defs['rocker-arm']
        top,bottom=state['top'],state['bottom'];rotation=-math.degrees(math.atan2(top[0]-bottom[0],top[1]-bottom[1]))
        parts[tag+'-pushrod']=b.Pos(x,(top[0]+bottom[0])/2,(top[1]+bottom[1])/2)*b.Rot(rotation,0,0)*defs['pushrod']
        moving|={tag+'-rocker',tag+'-pushrod'}
        for oid in static:
            if oid.startswith(tag+'-lifter-'):
                parts[oid]=b.Pos(0,0,height)*static[oid];moving.add(oid);rigid[oid]=tag+'-lifter'
            elif oid in [tag+'-valve',tag+'-retainer',tag+'-keeper-1',tag+'-keeper-2']:
                parts[oid]=b.Pos(0,0,-vl)*static[oid];moving.add(oid);rigid[oid]=tag+'-valve-set'
        parts[tag+'-spring']=b.Pos(x,VALVE_Y,310)*spring_shape(51-vl);moving.add(tag+'-spring')
        for a,c in [(tag+'-rocker',tag+'-fulcrum'),(tag+'-rocker',tag+'-pushrod'),(tag+'-pushrod',tag+'-lifter-pushrod-cup')]:
            contact_pair(parts,a,c,angle,contacts,failures)
        # OCC's shape/shape extrema sometimes returns a false nonzero gap for a
        # trimmed tangent sphere/plane. Require the analytic common point to lie
        # on BOTH actual STEP surfaces, rather than loosening contact tolerance.
        witness=b.Vertex(x,pad_y,370-vl)
        witness_a=witness.distance_to(parts[tag+'-rocker'])
        witness_b=witness.distance_to(parts[tag+'-valve'])
        contacts.append({'crank_deg':angle,'a':tag+'-rocker','b':tag+'-valve',
          'gap_mm':max(witness_a,witness_b),'method':'common tangent-point on both STEP surfaces'})
        if max(witness_a,witness_b)>.002:failures.append({'crank_deg':angle,'contact_witness_failure':[witness_a,witness_b]})
        # Common tangent point for the clockwise cam: profile normal angle is
        # (center-crank)/2, so its lateral derivative has the opposite sign.
        center=468 if kind=='intake' else 246
        offset=(angle-center+360)%720-360;u=offset/135
        q=96/135;k=-math.log(.05/.247)*(1-q*q)/(q*q)
        slope=0 if abs(u)>=1 else height*(-2*k*u/(1-u*u)**2)/math.radians(67.5)
        cam_point=b.Vertex(x,90-slope,90+height)
        gap_a=cam_point.distance_to(parts['camshaft']);gap_b=cam_point.distance_to(parts[tag+'-lifter-body'])
        contacts.append({'crank_deg':angle,'a':'camshaft','b':tag+'-lifter-body','gap_mm':max(gap_a,gap_b),
          'method':'common support-envelope tangent point on both STEP surfaces'})
        if max(gap_a,gap_b)>.002:failures.append({'crank_deg':angle,'cam_contact_witness_failure':[gap_a,gap_b]})
        # Negative controls: a0.1mm normal perturbation cannot remain a common
        # surface point. This catches an accidentally interior or unrelated probe.
        for point,a,bid in [(witness,tag+'-rocker',tag+'-valve'),(cam_point,'camshaft',tag+'-lifter-body')]:
            for sign in [-1,1]:
                displaced=b.Pos(0,0,sign*.1)*point
                separation=max(displaced.distance_to(parts[a]),displaced.distance_to(parts[bid]))
                if separation<.05:failures.append({'crank_deg':angle,'negative_control_failed':[a,bid,sign,separation]})
    keys=list(parts)
    for i,a in enumerate(keys):
        for c in keys[i+1:]:
            if a not in moving and c not in moving:continue
            if a in rigid and rigid.get(a)==rigid.get(c):continue
            if not box_overlap(parts[a],parts[c]):continue
            volume=intersect_volume(parts[a],parts[c]);checks+=1
            if volume>.1:
                failure={'crank_deg':angle,'a':a,'b':c,'overlap_mm3':volume};failures.append(failure);print(failure,flush=True)
    print('Checked crank',angle,'exact checks',checks,'failures',len(failures),flush=True)
    if angle==468:b.export_step(b.Compound(children=list(parts.values())),OUT/'intake-peak-assembly.step')
assert all(hashlib.sha256((ROOT/p).read_bytes()).hexdigest()==h for p,h in source_hashes.items()),'Candidate or baseline changed during audit'
report={'status':'PASS sampled local motion' if not failures else 'FAIL sampled local motion',
 'baseline_manifest_sha256':provenance['baseline_manifest_sha256'],'source_step_hashes':source_hashes,
 'crank_angles_deg':angles,'exact_intersections':checks,'contact_checks':len(contacts),'max_contact_gap_mm':max(x['gap_mm'] for x in contacts),
 'max_pushrod_closure_error_mm':max_closure,'minimum_helix_pitch_minus_wire_diameter_mm':min_coil_gap,'max_pad_slide_mm':max_pad_slide,
 'overlap_failure_threshold_mm3':.1,'failures':failures,
 'scope':'Cylinder1 intake/exhaust candidate vs saved block/head/cover/spark plug/piston and candidate cam; unchanged rigid-group internal pairs reuse static audit.',
 'limits':[f'Sampled clearance only;{len(angles)} poses not continuous proof.','Spring is an assumed6-turn helix, not production closed/ground ends or force model.','No claim of OEM cam law, rocker construction, head galleries or calibrated valve lift.','Other10 lobes remain original shapes; other cylinder valvetrains were not animated.']}
(OUT/('peak-validation.json' if '--peaks' in sys.argv else 'motion-validation.json')).write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2),flush=True)
if failures:sys.exit(1)
