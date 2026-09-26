#!/usr/bin/env python3
"""Inspect installed receiver feasibility without changing block, pan or manifest."""
import hashlib
import json
import platform
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'cad/engine'))
import build123d as b
from OCP.BRepAdaptor import BRepAdaptor_Surface
from dipstick_tube_candidate import passage_evidence, candidate


def sha(path):
    return hashlib.sha256((ROOT / path).read_bytes()).hexdigest()


def vec(v):
    return [v.X(), v.Y(), v.Z()]


def main():
    manifest_path = 'inventory/engine/full-assembly.json'
    manifest = json.loads((ROOT / manifest_path).read_text())
    block = b.import_step(ROOT / 'cad/engine/generated/block.step')
    bolt = b.import_step(ROOT / 'cad/engine/generated/pushrod-cover-bolt.step')
    faces = []
    # Full cylindrical-surface survey in the rear half of the +Y side. Includes
    # fillets, exterior cylinders and known bores: none is silently called a port.
    for face in block.faces():
        if face.geom_type != b.GeomType.CYLINDER:
            continue
        bb = face.bounding_box()
        if bb.center().X >= 0 or bb.center().Y <= 50:
            continue
        cyl = BRepAdaptor_Surface(face.wrapped).Cylinder()
        faces.append({'axis_origin_mm': vec(cyl.Axis().Location()),
                      'axis_direction': vec(cyl.Axis().Direction()),
                      'radius_mm': cyl.Radius(), 'bounds_min_mm': list(bb.min),
                      'bounds_max_mm': list(bb.max)})
    # Coarse diagnostics across rear-side lower casting; no claimed entry axis.
    probes = [passage_evidence(block, (x,155,z), (x,70,z), 3)
              for x in [-320,-285,-240,-171,-120,-57] for z in [0,25,50,75,100,125]]
    mounts = []
    for occ in manifest['occurrences']:
        if occ['definition'] != 'pushrod-cover-bolt':
            continue
        pos = occ['position_cad_mm']
        mounted = b.Pos(*pos) * b.Rot(*occ['rotation_cad_deg']) * bolt
        bb = mounted.bounding_box()
        x, _, z = pos
        mounts.append({'occurrence': occ['id'], 'shank_start_mm': pos,
                       'axis_direction': [0,1,0],
                       'head_outer_plane_y_mm': bb.max.Y,
                       'blind_bore_clear_probe': passage_evidence(block,(x,117.4,z),(x,109.5,z),3),
                       'blind_bore_bottom_probe': passage_evidence(block,(x,109.3,z),(x,108,z),3),
                       'external_support_stud': False,
                       'classification': 'model-derived generic headed bolt; not verified 6C517'})
    # Sensitivity checks: exact same passage test distinguishes an open bore,
    # an obstructed bore and an offset bore; these are synthetic fixtures only.
    fixture = b.Box(20,20,20)
    open_fixture = fixture - b.Cylinder(4,24)
    controls = {
        'open_bore': passage_evidence(open_fixture,(0,0,-12),(0,0,12),3),
        'plugged_bore': passage_evidence(fixture,(0,0,-12),(0,0,12),3),
        'offset_bore': passage_evidence(open_fixture,(3,0,-12),(3,0,12),3),
    }
    assert controls['open_bore']['clear']
    assert not controls['plugged_bore']['clear'] and not controls['offset_bore']['clear']
    assert all(m['blind_bore_clear_probe']['clear'] and not m['blind_bore_bottom_probe']['clear'] for m in mounts)
    # Ignored isolated diagnostic exports, deliberately no decorative tube.
    out = ROOT / 'cad/engine/generated/dipstick-tube-feasibility'
    out.mkdir(parents=True, exist_ok=True)
    b.export_step(open_fixture, out / 'passage-positive-control.step')
    b.export_step(fixture, out / 'passage-obstruction-control.step')
    inputs = [manifest_path, 'cad/engine/generated/block.step',
              'cad/engine/generated/pushrod-cover-bolt.step', 'cad/engine/pushrod_cover.py',
              'cad/engine/full_engine.py', 'reference/engine/dipstick-tube-review.json',
              'cad/engine/dipstick_tube_candidate.py', 'scripts/check-dipstick-tube-candidate.py']
    report = {
        'schema_version': 1, 'issue': 78, 'baseline_commit': subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),
        'status': 'upstream_interfaces_required', 'readiness': 'feasibility only; not integration-ready or Done',
        'environment': {'python': platform.python_version(), 'build123d': b.__version__, 'platform': platform.platform()},
        'inputs_sha256': {p:sha(p) for p in inputs},
        'coordinate_system': 'millimeters; front +X, pushrod cover +Y, up +Z; installed CAD coordinates',
        'cylindrical_face_survey': faces, 'lower_side_diagnostic_probes': probes,
        'cover_support_datums': mounts, 'negative_controls': controls,
        'findings': ['No source-authored dipstick receiver is present in the block builder or its adapters.',
                     'Survey/probes identify no accepted lower receiver; finite probes cannot prove absence of every possible angled aperture.',
                     'Cover holes are blind mounting bores; their headed bolts have no external support stud.',
                     'A tube route and blade insertion cannot be meaningfully tested before the two independently accepted attachment interfaces exist.'],
        'gates': {'audit_reproducibility':'PASS','passage_negative_controls':'PASS','mount_datums':'PASS model-derived only',
                  'lower_receiver':'FAIL unidentified','upper_retention':'FAIL no support stud',
                  'curved_tube_export':'NOT RUN','blade_insertion':'NOT RUN','installed_collisions':'NOT RUN',
                  'factory_applicability':'UNRESOLVED','browser':'NOT RUN'},
        'exports': {str(p.relative_to(ROOT)):sha(str(p.relative_to(ROOT))) for p in sorted(out.glob('*.step'))},
    }
    # Isolated educational upstream interfaces; never write installed artifacts.
    from assembly_math import transforms
    from dipstick_tube_candidate import SEAT, AXIS
    locations = transforms(manifest,0)
    installed_bolt = locations['pushrod-cover-bolt-1'] * bolt
    parts, tools = candidate(block, installed_bolt)
    def volume(shape):
        return sum(s.volume for s in shape.solids()) if shape is not None else 0.0
    def overlap(a,c):
        return volume(a.intersect(c))
    box_cache={}
    last_neighbor=[None,None]
    def boxes_overlap(a,c):
        if id(a) not in box_cache: box_cache[id(a)]=a.bounding_box()
        if last_neighbor[0] is not c: last_neighbor[:]=[c,c.bounding_box()]
        aa,cc=box_cache[id(a)],last_neighbor[1]
        return all(min(getattr(aa.max,k),getattr(cc.max,k))-max(getattr(aa.min,k),getattr(cc.min,k))>.001 for k in 'XYZ')
    part_checks = {}
    for name,shape in parts.items():
        path = out / (name+'.step')
        b.export_step(shape,path)
        restored = b.import_step(path)
        part_checks[name] = {'valid':shape.is_valid,'solids':len(shape.solids()),
                            'volume_mm3':volume(shape),'roundtrip_volume_error_mm3':abs(volume(shape)-volume(restored))}
        assert shape.is_valid and restored.is_valid and len(shape.solids())==1 and len(restored.solids())==1
        assert part_checks[name]['roundtrip_volume_error_mm3']<.02
    for name,shape in tools.items():
        b.export_step(shape,out/(name+'.step'))
    added = b.Compound((parts['block-candidate']-block).solids())
    removed = b.Compound((block-parts['block-candidate']).solids())
    protected_main = b.Pos(-341.376,0,40)*b.Box(31,300,160)
    # Covers lower end of cylinder barrel and all above it, inclusive of rear lifter.
    protected_upper = b.Pos(-315,0,185)*b.Box(60,300,220)
    preservation = {'main_support_removed_mm3':overlap(removed,protected_main),
                    'cylinder_lifter_zone_removed_mm3':overlap(removed,protected_upper),
                    'added_block_mm3':volume(added),'removed_block_mm3':volume(removed)}
    block_probe = passage_evidence(parts['block-candidate'],tuple(SEAT+AXIS*16),tuple(SEAT-AXIS*116),3)
    seating = []
    for a,c in [('block-candidate','engine-oil-dipstick-tube'),
                ('engine-oil-dipstick-tube','engine-oil-dipstick-tube-retaining-nut'),
                ('engine-oil-dipstick-tube','engine-oil-dipstick-tube-bracket'),
                ('engine-oil-dipstick-tube-bracket','pushrod-cover-retainer-candidate'),
                ('engine-oil-dipstick-tube-bracket','engine-oil-dipstick-tube-support-nut')]:
        seating.append({'a':a,'b':c,'gap_mm':parts[a].distance_to(parts[c]),'overlap_mm3':overlap(parts[a],parts[c])})
    import itertools
    internal_pairs=[{'a':a,'b':c,'overlap_mm3':overlap(parts[a],parts[c])} for a,c in itertools.combinations(parts,2)]
    blade_checks = {name:overlap(probe,parts['engine-oil-dipstick-tube']) for name,probe in tools.items() if 'blade' in name}
    static_checks=[]; collisions=[]
    definitions={}
    neighbor_hashes={}
    cache=out/'brep-cache'
    cache.mkdir(exist_ok=True)
    for definition in manifest['definitions']:
        p=definition['step'].lstrip('/')
        digest=sha(p)
        cached=cache/(digest+'.brep')
        if cached.exists(): definitions[definition['id']]=b.import_brep(cached)
        else:
            definitions[definition['id']]=b.import_step(ROOT/p)
            b.export_brep(definitions[definition['id']],cached)
        neighbor_hashes[p]=digest
    evaluated = {k:v for k,v in parts.items() if k!='block-candidate'}
    evaluated['block-added-material']=added
    evaluated.update({k:v for k,v in tools.items() if 'blade' in k})
    for oid in ['oil-pan','oil-pan-molded-gasket']:
        occ=next(o for o in manifest['occurrences'] if o['id']==oid)
        preservation[oid+'-receiver-cutter-overlap_mm3']=overlap(tools['receiver-cutter'],locations[oid]*definitions[occ['definition']])
    print('Loaded installed definitions; testing static neighbors',flush=True)
    for occurrence in manifest['occurrences']:
        oid=occurrence['id']
        if oid in ('block','pushrod-cover-bolt-1'):
            continue
        neighbor=locations[oid]*definitions[occurrence['definition']]
        for name,shape in evaluated.items():
            if not boxes_overlap(shape,neighbor):continue
            v=overlap(shape,neighbor)
            static_checks.append({'candidate':name,'neighbor':oid,'overlap_mm3':v})
            if v>.1:collisions.append(static_checks[-1])
    # Also check guide and free blade passage against modified block.
    for name in ['blade-guide-probe','blade-free-tip-probe']:
        v=overlap(tools[name],parts['block-candidate'])
        blade_checks[name+'-block']=v
    moving_groups={a['id'] for a in manifest['assemblies'] if (a.get('motion') or {}).get('type') in ('crank','rod','piston')}
    moving=[o for o in manifest['occurrences'] if o['parent'] in moving_groups]
    motion_checks=0;motion_collisions=[]
    print('Static collisions',collisions,flush=True)
    for degrees in range(0,721,10):
        if degrees%90==0: print('Motion degrees',degrees,flush=True)
        poses=transforms(manifest,degrees)
        for o in moving:
            neighbor=poses[o['id']]*definitions[o['definition']]
            for name,shape in evaluated.items():
                if not boxes_overlap(shape,neighbor):continue
                motion_checks+=1
                v=overlap(shape,neighbor)
                if v>.1:motion_collisions.append({'degrees':degrees,'candidate':name,'neighbor':o['id'],'overlap_mm3':v})
    # Continuous crank envelope covering all X stations. Source crank cheeks are union
    # of R43 hub, 66-wide web at stroke/2, R37 throw end, R49 offset20 counterweight.
    # Their maximum radial support is max(43, hypot(33,stroke/2),stroke/2+37,69).
    import math
    crank_radius=max(43,math.hypot(33,manifest['mechanism']['stroke_mm']/2),manifest['mechanism']['stroke_mm']/2+37,69)
    crank_envelope=b.Rot(0,90,0)*b.Cylinder(crank_radius,1000)
    continuous_crank={name:overlap(shape,crank_envelope) for name,shape in evaluated.items()}
    # Rods rotate about X: world_y=jy*(1-local_z/L)+local_y*cos(theta).
    # Their X bounds never change. Piston parts only
    # translate along Z; enlarge their zero-pose boxes downward by full stroke.
    continuous_recip=[]
    assembly_map={a['id']:a for a in manifest['assemblies']}
    for o in moving:
        typ=assembly_map[o['parent']]['motion']['type']
        if typ not in ('piston','rod'):continue
        bb=(locations[o['id']]*definitions[o['definition']]).bounding_box()
        if typ=='rod':
            local=definitions[o['definition']].bounding_box()
            radius=manifest['mechanism']['stroke_mm']/2
            rod_length=manifest['mechanism']['rod_length_mm']
            ly=max(abs(local.min.Y),abs(local.max.Y))
            lz=max(abs(local.min.Z),abs(local.max.Z))
            y_bound=radius*max(abs(1-local.min.Z/rod_length),abs(1-local.max.Z/rod_length))+ly
            z_bound=radius+math.hypot(ly,lz)
            env=b.Pos((bb.min.X+bb.max.X)/2,0,0)*b.Box(bb.size.X,2*y_bound,2*z_bound)
        else:
            # Phase-zero can be anywhere in stroke: expand both directions.
            env=b.Pos(bb.center().X,bb.center().Y,bb.center().Z)*b.Box(bb.size.X,bb.size.Y,bb.size.Z+2*manifest['mechanism']['stroke_mm'])
        for name,shape in evaluated.items():
            if boxes_overlap(shape,env):
                v=overlap(shape,env)
                continuous_recip.append({'candidate':name,'neighbor':o['id'],'envelope_overlap_mm3':v})
    candidate_controls={
        'offset_tube_block_overlap_mm3':overlap(b.Pos(2,0,0)*parts['engine-oil-dipstick-tube'],parts['block-candidate']),
        'offset_support_nut_stud_overlap_mm3':overlap(b.Pos(3,0,0)*parts['engine-oil-dipstick-tube-support-nut'],parts['pushrod-cover-retainer-candidate']),
        'unmachined_receiver_probe':passage_evidence(block,tuple(SEAT+AXIS*16),tuple(SEAT-AXIS*116),3),
    }
    assert candidate_controls['offset_tube_block_overlap_mm3']>.1
    assert candidate_controls['offset_support_nut_stud_overlap_mm3']>.1
    assert not candidate_controls['unmachined_receiver_probe']['clear']
    report['isolated_candidate']={
        'status':'PASS bounded educational geometry' if all(c['overlap_mm3']<.1 for c in internal_pairs) and preservation['main_support_removed_mm3']<.001 and preservation['cylinder_lifter_zone_removed_mm3']<.001 and preservation['oil-pan-receiver-cutter-overlap_mm3']<.001 and preservation['oil-pan-molded-gasket-receiver-cutter-overlap_mm3']<.001 and not collisions and not motion_collisions and all(v<.001 for v in blade_checks.values()) and block_probe['clear'] and all(c['gap_mm']<.002 and c['overlap_mm3']<.1 for c in seating) and all(v<.001 for v in continuous_crank.values()) and all(c['envelope_overlap_mm3']<.001 for c in continuous_recip) else 'FAIL review diagnostics',
        'estimated_datums':{'seat_mm':list(SEAT),'outward_axis':list(AXIS),'upper_station_mm':[-285,144.292,185]},
        'blade_length_study':{'comparison_length_mm':692.15,'guide_path_length_mm':692.15-volume(tools['blade-free-tip-probe'])/(math.pi*((6.5**2+.8**2)/4)),'free_tip_length_mm':volume(tools['blade-free-tip-probe'])/(math.pi*((6.5**2+.8**2)/4)),'mouth_mm':[-285,170,500],'calibration':'unknown'},
        'parts':part_checks,'candidate_negative_controls':candidate_controls,'preservation':preservation,'receiver_passage':block_probe,
        'seating':seating,'internal_pairs':internal_pairs,'blade_probes_overlap_mm3':blade_checks,
        'static_comparisons':static_checks,'static_collisions':collisions,
        'motion_degrees':list(range(0,721,10)),'motion_comparisons':motion_checks,'motion_collisions':motion_collisions,
        'continuous_crank_envelope_radius_mm':crank_radius,'continuous_crank_envelope_intersections_mm3':continuous_crank,
        'continuous_reciprocating_envelope_intersections':continuous_recip,
        'neighbor_step_sha256':neighbor_hashes,
        'limits':['All newly selected datums and dimensions are educational estimates; exact1994 applicability unresolved.',
                  'Threads are clearance envelopes, not mating helical thread surfaces; retention strength unvalidated.',
                  'Blade tip envelope encloses pilot6.5x0.8mm section; mouth envelope encloses3mm waves plus2.2mm stem. No elastic insertion or calibrated oil level claim.',
                  'Continuous crank bound derives from modeled cheek primitives; rod Y bound uses jy*(1-local_z/L)+local_y*cos(theta); piston swept boxes bound full stroke. These check model motion, not factory shape.']}
    report['gates'].update({'isolated_candidate_geometry':report['isolated_candidate']['status'],'lower_receiver':'PASS estimated isolated receiver' if block_probe['clear'] else 'FAIL','upper_retention':'PARTIAL isolated stud/shoulder contacts; thread surfaces absent','curved_tube_export':'PASS isolated STEP','blade_insertion':'PARTIAL dimensional envelopes; elastic motion NOT RUN','installed_collisions':'NOT RUN installed; isolated neighbor audit reported','motion':'sampled actual shapes plus continuous conservative envelopes'})
    report['findings']=['Baseline receiver audit and isolated estimated replacement interfaces are reported separately.','No installed geometry was changed; see isolated_candidate for quantitative feasibility results.']
    report['status']='isolated_candidate_evaluated'
    report['readiness']='isolated educational feasibility candidate; not installed or Done'
    if '--render' in sys.argv:
        from dipstick_tube_candidate import render_review
        render_review(parts,out)
        report['visual_review']={'path':str((out/'candidate-review.png').relative_to(ROOT)),'sha256':sha(str((out/'candidate-review.png').relative_to(ROOT))),'status':'generated; visual inspection recorded in handoff'}
    report['exports']={str(p.relative_to(ROOT)):sha(str(p.relative_to(ROOT))) for p in sorted(out.glob('*.step'))}
    report['inputs_sha256'].update({p:sha(p) for p in ['cad/engine/assembly_math.py','cad/engine/pilot/dipstick/dipstick.py']})
    assert all(sha(p)==digest for p,digest in neighbor_hashes.items()), 'Installed STEP changed during audit'
    assert all(sha(p)==digest for p,digest in report['inputs_sha256'].items()), 'Input changed during audit'
    path = ROOT / 'inventory/engine/dipstick-tube-candidate-validation.json'
    path.write_text(json.dumps(report,indent=2)+'\n')
    if report['isolated_candidate']['status']!='PASS bounded educational geometry':
        raise SystemExit('FAIL isolated candidate; inspect written report')
    print(json.dumps({'status':report['status'],'cylinder_faces':len(faces),'probes':len(probes),
                      'blocked_probes':sum(not p['clear'] for p in probes),'cover_mounts':len(mounts),
                      'report':str(path.relative_to(ROOT))}))

if __name__ == '__main__':
    main()
