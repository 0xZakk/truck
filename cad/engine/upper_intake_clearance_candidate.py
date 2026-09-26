"""Isolated owner-photo-led intake envelope study, never an OEM dimension claim.

Preserves six lower runner stations, seven studs and regulator vacuum port.
Balanced compact plenum moves throttle/EGR frames and the provisional cap station.
"""
from pathlib import Path
import build123d as b
import json,hashlib,sys
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'cad/engine'))
PITCH=113.792
PORTS=[(2.5-i)*PITCH for i in range(6)]
MAINS=[(3-i)*PITCH for i in range(7)]
REAR=-200.
FRONT=200. # inferred balanced-envelope trial, not photo metrology
CAP_X=300.
CAP_DELTA=(CAP_X-240.,0.,0.)
EGR_DELTA=(REAR+367.,0.,25.)
THROTTLE_DELTA=(FRONT-367.,0.,0.)

def rounded_box(x,y,z,r):return b.extrude(b.RectangleRounded(x,y,r),amount=z/2,both=True)
def cx(r,h):return b.Rot(0,90,0)*b.Cylinder(r,h)

def candidate():
    center=(REAR+FRONT)/2;length=FRONT-REAR
    upper=b.Pos(center,25,490)*rounded_box(length,145,90,25)
    upper+=b.Pos(0,-228,366.5)*rounded_box(734,56,10,14)
    paths=[]
    for x in PORTS:
        # Fan from unchanged cylinder stations into a shorter common plenum.
        terminal=-150+(x+PORTS[0])/(2*PORTS[0])*300
        path=b.Bezier((x,-228,366.5),(x,-228,490),(terminal,-145,490),(terminal,-20,490))
        paths.append(path)
        upper+=b.sweep(b.Plane(origin=path@0,z_dir=path%0)*b.Circle(22),path=path)
    upper-=b.Pos(center,25,490)*rounded_box(length-8,137,82,21)
    for x,path in zip(PORTS,paths):
        bore=b.Wire([b.Line((x,-228,354),path@0),path])
        upper-=b.sweep(b.Plane(origin=bore@0,z_dir=bore%0)*b.Circle(16.5),path=bore)
    for x in MAINS:upper-=b.Pos(x,-228,366.5)*b.Cylinder(4.4,16)
    upper+=b.Pos(FRONT,25,490)*b.Box(8,124,68)
    for y in (-24,74):
        for z in (464,516):upper-=b.Pos(FRONT-5,y,z)*cx(4.2,22)
    for y in (-2,52):upper-=b.Pos(FRONT,y,490)*cx(20,22)
    from egr import intake_interface
    from regulator_vacuum import intake_interface as vacuum_interface
    upper=b.Pos(*EGR_DELTA)*intake_interface(b.Pos(*(-v for v in EGR_DELTA))*upper)
    return vacuum_interface(upper),paths

def coordinated_cap_cover(cover):
    """Regenerate roof material at old opening; new bore/neck share new capaxis.

    This changes the service-assembly shape, not an invented separate plug part.
    Existing flat3mm roof and all other cover geometry remain inherited estimates.
    """
    from oil_fill_neck_candidate import candidate as neck_candidate,cap_at
    _,neck=neck_candidate(cover)
    roof=cover+b.Pos(240,-12,411.5)*b.Cylinder(17.3,3)
    roof-=b.Pos(CAP_X,-12,408)*b.Cylinder(17,20)
    neck=b.Pos(*CAP_DELTA)*neck
    cap,seal=cap_at(0)
    return roof+neck,neck,b.Pos(*CAP_DELTA)*cap,b.Pos(*CAP_DELTA)*seal

def volume(s):return sum(x.volume for x in s.solids()) if s else 0.
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()

BAKE_ROWS=[]
def bake(shape, label):
    """Bake world locations by STEP roundtrip before kernel Boolean checks.

    A translated helical cap falsely returned zero retention interference in
    native OCC shapes; the exported world-coordinate solids retain it.
    """
    folder=ROOT/'cad/engine/generated/upper-intake-clearance-study/baked'
    folder.mkdir(parents=True,exist_ok=True)
    path=folder/(label+'.step');b.export_step(shape,path);result=b.import_step(path)
    aa,bb=shape.bounding_box(),result.bounding_box()
    delta=max(abs(a-c) for a,c in zip((*aa.min,*aa.max),(*bb.min,*bb.max)))
    row={'id':label,'valid':result.is_valid,'solids':len(result.solids()),'volume_delta_mm3':abs(volume(shape)-volume(result)),'bounds_delta_mm':delta}
    assert row['valid'] and row['solids']==len(shape.solids()) and delta<.01 and row['volume_delta_mm3']<.1,row
    BAKE_ROWS.append(row)
    return result

def neighbor_audit(m,poses,definitions,actors,originals,groups,tracked):
    """Exact overlap checks against all broad-phase nearby installed occurrences.

    Same rigid-group pairs preserve their old relationships. Other pairs are
    tested, including changed-to-changed neighbors. Existing overlaps are shown
    separately from new/worsened collisions; neither is called factory fidelity.
    """
    import numpy as np
    import trimesh
    local_bounds={}; world_bounds={}; exact={}; rows=[]; broad=0
    occurrence={o['id']:o for o in m['occurrences']}
    def bounds(shape):
        bb=shape.bounding_box();return np.array(tuple(bb.min)),np.array(tuple(bb.max))
    for o in m['occurrences']:
        if o['id'] in actors:world_bounds[o['id']]=bounds(actors[o['id']]);continue
        d=definitions[o['definition']];gp=ROOT/d['glb'].lstrip('/');tracked.add(gp)
        if o['definition'] not in local_bounds:
            a=np.asarray(trimesh.load(gp,force='mesh').vertices)
            v=np.column_stack((a[:,0],-a[:,2],a[:,1]))*1000
            local_bounds[o['definition']]=(v.min(0)-.2,v.max(0)+.2)
        lo,hi=local_bounds[o['definition']]
        corners=np.array([tuple(b.Vertex(x,y,z).moved(poses[o['id']]).center()) for x in (lo[0],hi[0]) for y in (lo[1],hi[1]) for z in (lo[2],hi[2])])
        world_bounds[o['id']]=(corners.min(0),corners.max(0))
    def installed(ident):
        if ident in originals:return originals[ident]
        if ident not in exact:
            o=occurrence[ident];sp=ROOT/definitions[o['definition']]['step'].lstrip('/');tracked.add(sp)
            exact[ident]=bake(poses[ident]*b.import_step(sp),'baseline-'+ident)
        return exact[ident]
    seen=set()
    for ident,actor in actors.items():
        print('Neighbor audit',ident,flush=True)
        alo,ahi=bounds(actor)
        for neighbor in occurrence:
            if neighbor==ident:continue
            if neighbor in actors and groups.get(ident)==groups.get(neighbor):continue
            pair=tuple(sorted((ident,neighbor)))
            if pair in seen:continue
            seen.add(pair);lo,hi=world_bounds[neighbor]
            if np.any(ahi<lo) or np.any(hi<alo):broad+=1;continue
            other=actors[neighbor] if neighbor in actors else installed(neighbor)
            overlap=volume(actor&other)
            row={'actor':ident,'neighbor':neighbor,'overlap_mm3':overlap}
            if overlap>.1:
                baseline=volume(installed(ident)&installed(neighbor))
                row.update(baseline_overlap_mm3=baseline,new_or_worsened=overlap>baseline+.1)
            rows.append(row)
    return {'scope':'All current occurrences at rest; exact CAD after conservative GLB/CAD AABB exclusion. Same rigid-frame internal pairs unchanged. Contact-only interfaces audited separately.','exact_pairs':len(rows),'aabb_excluded_pairs':broad,'new_or_worsened':[r for r in rows if r.get('new_or_worsened')],'existing_overlaps':[r for r in rows if r['overlap_mm3']>.1 and not r.get('new_or_worsened')],'pairs':rows}

def cap_motion(m,cap,neck,tracked):
    import math
    from assembly_math import transforms
    rockers=[o for o in m['occurrences'] if o.get('valvetrain',{}).get('role')=='rocker']
    assert len(rockers)==12
    definitions={d['id']:d for d in m['definitions']};shapes={}
    for o in rockers:
        p=ROOT/definitions[o['definition']]['step'].lstrip('/');tracked.add(p)
        if o['definition'] not in shapes:shapes[o['definition']]=b.import_step(p)
    angles=set(range(0,721,5))
    for phase in range(0,720,120):
        for peak in (246,468):
            for delta in (-135,0,135):angles.add((phase+peak+delta)%720)
    focused=dict(m,occurrences=rockers);rows=[];closest=None
    for angle in sorted(angles):
        poses=transforms(focused,angle)
        for o in rockers:
            rocker=poses[o['id']]*shapes[o['definition']]
            rocker_baked=False
            for name,part in [('cap',cap),('neck',neck)]:
                aa,cc=part.bounding_box(),rocker.bounding_box()
                lower=math.sqrt(sum(max(0.,tuple(aa.min)[i]-tuple(cc.max)[i],tuple(cc.min)[i]-tuple(aa.max)[i])**2 for i in range(3)))
                row={'angle_deg':angle,'rocker':o['id'],'part':name,'aabb_distance_lower_bound_mm':lower}
                if lower<2:
                    if not rocker_baked:
                        rocker=bake(rocker,f"motion-{o['id']}-{angle}");rocker_baked=True
                    row['exact_distance_mm']=part.distance_to(rocker)
                    row['overlap_mm3']=volume(part&rocker) if row['exact_distance_mm']<.002 else 0.
                    if closest is None or row['exact_distance_mm']<closest['exact_distance_mm']:closest=dict(row)
                rows.append(row)
        print('Relocated cap rocker phase',angle,flush=True)
    assert closest is not None
    o=next(o for o in rockers if o['id']==closest['rocker'])
    r=bake(transforms(focused,closest['angle_deg'])[o['id']]*shapes[o['definition']],'motion-negative-rocker')
    bad=volume(bake(b.Pos(0,0,-10)*cap,'motion-negative-cap')&r)
    failures=[r for r in rows if r.get('exact_distance_mm',r['aabb_distance_lower_bound_mm'])<.002 or r.get('overlap_mm3',0)>.1]
    assert bad>.1
    return {'status':'PASS' if not failures else 'FAIL','phases':len(angles),'pairs':len(rows),'closest_exact':closest,'minimum_aabb_bound_mm':min(r['aabb_distance_lower_bound_mm'] for r in rows),'negative_lowered_cap_overlap_mm3':bad,'failures':failures,'scope':'All12 rockers,181 crank phases; AABB separates distant pairs, exact CAD for pairs closer than2 mm.'}

def render_comparison(old,new,cover,cap,throttle,out):
    import numpy as np
    items=[];view=np.array([.55,-.74,.39]);view/=np.linalg.norm(view)
    right=np.array([.803,.597,0.]);up=np.cross(view,right)
    for panel,manifold in enumerate((old,new)):
        shapes=[(cover,[163,176,181]),(manifold,[98,141,158]),(cap,[181,126,48])]
        shapes.extend(((b.Pos(*THROTTLE_DELTA)*t if panel else t),[84,102,115]) for t in throttle)
        for shape,col in shapes:
            vs,fs=shape.tessellate(.5,.3);tri=np.array([tuple(v) for v in vs])[np.array(fs)]-np.array([0,-65,435])
            norm=np.cross(tri[:,1]-tri[:,0],tri[:,2]-tri[:,0]);norm/=np.maximum(np.linalg.norm(norm,axis=1)[:,None],1e-8)
            shade=.45+.55*np.abs(norm@np.array([.3,-.4,.866]));uv=np.stack([tri@right,-tri@up],axis=-1)*.77+np.array([350+panel*700,365]);dep=(tri@view).mean(1)
            for pts,z,k in zip(uv,dep,shade):items.append((panel,z,pts,tuple(int(c*k) for c in col)))
    svg=['<svg xmlns="http://www.w3.org/2000/svg" width="1400" height="650"><rect width="1400" height="650" fill="#f7f9fb"/>']
    for panel,z,pts,col in sorted(items,key=lambda x:(x[0],x[1])):
        svg.append('<polygon points="'+' '.join(f'{x:.2f},{y:.2f}' for x,y in pts)+'" fill="rgb'+str(col)+'"/>')
    svg+=['<text x="25" y="34" font-family="sans-serif" font-size="22">Actual CAD comparison — trial shape and throttle frame remain inferred; cap shape unchanged; station shifted 60 mm</text>','<text x="35" y="82" font-family="sans-serif" font-size="20">Existing 734 mm plenum / proposed cap station</text>','<text x="735" y="82" font-family="sans-serif" font-size="20">Trial 400 mm plenum / balanced runners / cap forward 60 mm</text>','<text x="30" y="615" font-family="sans-serif" font-size="18">Review against owner bay photographs; perspective photos do not establish these numerical dimensions.</text>','</svg>']
    (out/'comparison.svg').write_text('\n'.join(svg))

def render_neck_section(cover,cap,seal,out):
    """Actual CAD cutaway at the cap axis; no illustrative geometry added."""
    import numpy as np
    crop=b.Pos(CAP_X,-12,423)*b.Box(90,90,80)
    cut=b.Pos(CAP_X,-62,423)*b.Box(110,100,100)
    polygons=[]
    for part,color in [(cover,(163,176,181)),(cap,(181,126,48)),(seal,(66,81,92))]:
        section=(part&crop)-cut
        vs,fs=section.tessellate(.1,.15);tri=np.array([tuple(v) for v in vs])[np.array(fs)]
        for face in tri:
            pts=np.column_stack(((face[:,0]-CAP_X)*6+360,600-(face[:,2]-380)*6))
            polygons.append((float(face[:,1].mean()),pts,color))
    svg=['<svg xmlns="http://www.w3.org/2000/svg" width="720" height="650"><rect width="720" height="650" fill="#f7f9fb"/>']
    for _,pts,color in sorted(polygons,key=lambda t:-t[0]):
        svg.append('<polygon points="'+' '.join(f'{x:.2f},{y:.2f}' for x,y in pts)+'" fill="rgb'+str(color)+'"/>')
    svg+=['<text x="20" y="30" font-family="sans-serif" font-size="21">Actual CAD: cap / seal / fused neck section</text>',
          '<text x="20" y="58" font-family="sans-serif" font-size="16">X300 station; 4.5 mm pitch is assumed, not an OEM specification</text>',
          '<text x="20" y="630" font-family="sans-serif" font-size="16">Nominal seal contact; open fill passage; production neck construction unknown</text>','</svg>']
    (out/'neck-section.svg').write_text('\n'.join(svg))

if __name__=='__main__':
    from oil_fill_neck_candidate import cap_at
    from assembly_math import transforms
    out=ROOT/'cad/engine/generated/upper-intake-clearance-study';out.mkdir(exist_ok=True)
    manifest=ROOT/'inventory/engine/full-assembly.json'
    manifest_before=sha(manifest)
    snapshot_paths=set((ROOT/'cad/engine').glob('*.py'))|{manifest}
    snapshot_paths.add(ROOT/'cad/engine/pilot/oil-cap/oil_cap.py')
    snapshot_paths.update((ROOT/'cad/engine/generated').glob('*.step'))
    snapshot_paths.update((ROOT/'models/engine').glob('*.glb'))
    before={str(p.relative_to(ROOT)):sha(p) for p in snapshot_paths}
    shape,paths=candidate();shape=bake(shape,'upper-intake');b.export_step(shape,out/'upper-intake.step');checks={'valid':shape.is_valid,'solid_count':len(shape.solids()),'runner_probes':[]}
    # Each continuous small-bore swept probe goes from lower face into plenum.
    for i,(x,path) in enumerate(zip(PORTS,paths),1):
        wire=b.Wire([b.Line((x,-228,359),path@0),path])
        probe=b.sweep(b.Plane(origin=wire@0,z_dir=wire%0)*b.Circle(12),path=wire)
        checks['runner_probes'].append({'cylinder':i,'start_mm':[x,-228,359],'end_mm':list(path@1),'blocked_volume_mm3':volume(probe&shape)})
    # Existing full-length lower mating face and seven stud axes are preserved.
    m=json.loads((ROOT/'inventory/engine/full-assembly.json').read_text());defs={d['id']:d for d in m['definitions']};poses=transforms(m)
    old=poses['efi-upper-intake']*b.import_step(ROOT/defs['efi-upper-intake']['step'].lstrip('/'))
    slab=b.Pos(0,-228,363)*b.Box(800,60,3)
    checks['lower_flange_symmetric_difference_mm3']=volume((old&slab)-(shape&slab))+volume((shape&slab)-(old&slab))
    # A conservative box contains the cap and seal through all five screw turns.
    # Exact disjointness proves the whole path, avoiding redundant expensive
    # global minimum-distance solves against this multi-surface manifold.
    # Axisymmetric union proves every rotation and0–22.5mm lift while
    # avoiding the empty lower corners of a whole-cap bounding box.
    envelope=b.Pos(CAP_X,-12,414.75)*b.Cylinder(15.9,41.5)+b.Pos(CAP_X,-12,435)*b.Cylinder(37,44)
    envelope_hit=volume(shape&envelope)
    old_hit=volume(old&envelope)
    checks['cap_removal_envelope']={'bounds_mm':[[CAP_X-37,-49,390],[CAP_X+37,25,457]],'candidate_overlap_mm3':envelope_hit,'old_intake_negative_overlap_mm3':old_hit,'scope':'Axisymmetric stemR15.9 Z394–435.5 and headR37 Z413–457 enclosure of all rotations and0–22.5mm lift; no hand/tool envelope'}
    removal=[{'angle_deg':a,'lift_mm':4.5*a/360,'envelope_disjoint':envelope_hit<.1} for a in range(0,1801,90)]
    checks['cap_removal']=removal
    print('Envelope and interface checks:',json.dumps(checks),flush=True)
    # Identify all descendants rather than a hand-maintained mechanism list.
    parents={a['id']:a.get('parent') for a in m['assemblies']}
    def descendant(o):
        parent=o.get('parent')
        while parent:
            if parent=='throttle-assembly':return True
            parent=parents.get(parent)
        return False
    moved=[];throttle_shapes=[];extra_paths=[]
    actors={'efi-upper-intake':shape};originals={'efi-upper-intake':old};groups={'efi-upper-intake':'manifold'}
    for o in m['occurrences']:
        if not descendant(o):continue
        sp=ROOT/defs[o['definition']]['step'].lstrip('/');extra_paths.append(sp)
        original=bake(poses[o['id']]*b.import_step(sp),'original-'+o['id']);shifted=bake(b.Pos(*THROTTLE_DELTA)*original,'moved-'+o['id'])
        actors[o['id']]=shifted;originals[o['id']]=original;groups[o['id']]='throttle'
        moved.append({'id':o['id'],'delta_mm':THROTTLE_DELTA,'cap_envelope_overlap_mm3':volume(shifted&envelope)})
        if o['id'] in ('throttle-housing','throttle-gasket'):
            checks[o['id']+'_new_intake_overlap_mm3']=volume(shifted&shape)
            checks[o['id']+'_new_intake_distance_mm']=shifted.distance_to(shape)
        throttle_shapes.append(original)
    checks['coordinated_throttle_parts']=moved
    cover_path=ROOT/defs['valve-cover']['step'].lstrip('/');extra_paths.append(cover_path)
    cover=poses['valve-cover']*b.import_step(cover_path)
    newcover,neck,newcap,newseal=coordinated_cap_cover(cover)
    native_pull=volume((b.Pos(0,0,1.125)*newcap)&newcover)
    newcover=bake(newcover,'cover-with-neck');neck=bake(neck,'neck');newcap=bake(newcap,'cap');newseal=bake(newseal,'seal')
    seated_enclosure=b.Pos(CAP_X,-12,403.5)*b.Cylinder(15.9,19)+b.Pos(CAP_X,-12,423)*b.Cylinder(37,20)
    checks['withdrawal_enclosure_proof']={'cap_outside_seated_enclosure_mm3':volume(newcap-seated_enclosure),'seal_outside_seated_enclosure_mm3':volume(newseal-seated_enclosure),'method':'Seated axisymmetric two-cylinder enclosure extended upward22.5mm; rotation leaves radial bounds invariant.'}
    assert all(checks['withdrawal_enclosure_proof'][k]<.1 for k in ('cap_outside_seated_enclosure_mm3','seal_outside_seated_enclosure_mm3'))
    checks['retention_kernel_regression']={'native_translated_pull_overlap_mm3':native_pull,'step_baked_pull_overlap_mm3':volume(bake(b.Pos(0,0,1.125)*newcap,'pull-cap')&newcover),'policy':'All audited actors and posed moving solids use STEP-baked world coordinates; native translated zero is not accepted as clearance evidence.'}
    checks['relocated_cap_cover']={'cover_solids':len(newcover.solids()),'cover_valid':newcover.is_valid,'seated_overlap_mm3':volume(newcap&newcover),'seal_overlap_mm3':volume(newseal&newcover),'seal_distance_mm':newseal.distance_to(newcover),'old_hole_closed_probe_mm3':volume(newcover&(b.Pos(240,-12,411.5)*b.Cylinder(10,2))),'fill_path_blocked_mm3':volume(newcover&(b.Pos(CAP_X,-12,411)*b.Cylinder(10,30)))}
    actors.update({'valve-cover':newcover,'oil-filler-cap':newcap,'oil-filler-cap-seal':newseal})
    groups.update({'valve-cover':'cover','oil-filler-cap':'cap','oil-filler-cap-seal':'cap'})
    originals['valve-cover']=cover
    # EGR and EVP move rigidly together; fixed-end tube/hose routes are separately
    # coordinated and must not be declared connected by this translation alone.
    def under(o,root):
        parent=o.get('parent')
        while parent:
            if parent==root:return True
            parent=parents.get(parent)
        return False
    egr_ids=[]
    for o in m['occurrences']:
        if under(o,'egr-valve-assembly') or under(o,'egr-position-sensor') or o['id'] in ('egr-intake-gasket','egr-mount-bolt-1','egr-mount-bolt-2'):
            sp=ROOT/defs[o['definition']]['step'].lstrip('/');extra_paths.append(sp)
            original=bake(poses[o['id']]*b.import_step(sp),'original-'+o['id'])
            originals[o['id']]=original;actors[o['id']]=bake(b.Pos(*EGR_DELTA)*original,'moved-'+o['id']);groups[o['id']]='egr';egr_ids.append(o['id'])
    checks['coordinated_egr_parts']=egr_ids
    from intake_egr_routes_candidate import parts as route_parts
    for ident,route_shape in route_parts().items():
        o=next(o for o in m['occurrences'] if o['id']==ident)
        sp=ROOT/defs[o['definition']]['step'].lstrip('/');extra_paths.append(sp)
        originals[ident]=bake(poses[ident]*b.import_step(sp),'original-'+ident)
        actors[ident]=bake(route_shape,'route-'+ident);groups[ident]='route-'+ident
    checks['egr_routes']={'scope':'Root-owned compact Bezier route proposal; inferred geometry, fixed exhaust/EVR endpoints retained.','interfaces':[]}
    for left,right in [('egr-exhaust-tube','egr-body'),('egr-tube-valve-nut','egr-body'),('egr-control-vacuum-hose','egr-vacuum-nipple'),('egr-intake-gasket','efi-upper-intake'),('egr-body','egr-intake-gasket')]:
        checks['egr_routes']['interfaces'].append({'left':left,'right':right,'distance_mm':actors[left].distance_to(actors[right]),'overlap_mm3':volume(actors[left]&actors[right])})
    checks['relocated_cap_cover']['straight_pull_overlap_mm3']=volume(bake(b.Pos(0,0,1.125)*newcap,'pull-cap')&newcover)
    oversized=newcover-b.Pos(CAP_X,-12,408)*b.Cylinder(16.1,40)
    checks['relocated_cap_cover']['oversized_bore_pull_overlap_mm3']=volume(bake(b.Pos(0,0,1.125)*newcap,'pull-cap')&bake(oversized,'oversized-control'))
    checks['relocated_cap_cover']['screw_removal']=[]
    for angle in (0,90,180,360,720,1080,1440,1800):
        c,se=cap_at(angle);c=bake(b.Pos(*CAP_DELTA)*c,f'screw-cap-{angle}');se=bake(b.Pos(*CAP_DELTA)*se,f'screw-seal-{angle}')
        checks['relocated_cap_cover']['screw_removal'].append({'angle_deg':angle,'cap_overlap_mm3':volume(c&newcover),'seal_overlap_mm3':volume(se&newcover)})
    tracked=set(extra_paths)
    (out/'pre-motion-checks.json').write_text(json.dumps(checks,indent=2)+'\n')
    # Conservative withdrawal envelope against every current occurrence. Cover
    # and cap/seal are excluded here because the helical joint is checked above.
    import numpy as np
    import trimesh
    withdrawal=[]
    eb=envelope.bounding_box();elo=np.array(tuple(eb.min));ehi=np.array(tuple(eb.max))
    for o in m['occurrences']:
        ident=o['id']
        if ident in ('valve-cover','oil-filler-cap','oil-filler-cap-seal'):continue
        if ident in actors:
            neighbor=actors[ident];bb=neighbor.bounding_box();lo=np.array(tuple(bb.min));hi=np.array(tuple(bb.max))
        else:
            gp=ROOT/defs[o['definition']]['glb'].lstrip('/');tracked.add(gp)
            a=np.asarray(trimesh.load(gp,force='mesh').vertices);v=np.column_stack((a[:,0],-a[:,2],a[:,1]))*1000
            ll,hh=v.min(0)-.2,v.max(0)+.2
            corners=np.array([tuple(b.Vertex(x,y,z).moved(poses[ident]).center()) for x in (ll[0],hh[0]) for y in (ll[1],hh[1]) for z in (ll[2],hh[2])]);lo,hi=corners.min(0),corners.max(0)
        if np.any(ehi<lo) or np.any(hi<elo):continue
        if ident not in actors:
            sp=ROOT/defs[o['definition']]['step'].lstrip('/');tracked.add(sp);neighbor=bake(poses[ident]*b.import_step(sp),'withdrawal-'+ident)
        withdrawal.append({'neighbor':ident,'envelope_overlap_mm3':volume(envelope&neighbor)})
    checks['full_withdrawal_neighbors']={'scope':'Proven axisymmetric two-cylinder enclosure covers all cap/seal rotations and0–22.5mm lift. Joint cover excluded, separately screw-checked. No hand/tool or later carrying path.','exact_pairs':withdrawal,'failures':[r for r in withdrawal if r['envelope_overlap_mm3']>.1]}
    (out/'pre-motion-checks.json').write_text(json.dumps(checks,indent=2)+'\n')
    checks['relocated_cap_motion']=cap_motion(m,newcap,neck,tracked)
    checks['neighbor_audit']=neighbor_audit(m,poses,defs,actors,originals,groups,tracked)
    extra_paths=list(tracked)
    b.export_step(newcover,out/'cover-with-relocated-neck.step')
    b.export_step(newcap,out/'relocated-cap.step')
    render_comparison(old,shape,newcover,newcap,throttle_shapes,out)
    render_neck_section(newcover,newcap,newseal,out)
    assert sha(manifest)==manifest_before,'Manifest changed during proposal check; rerun with frozen integration baseline'
    # All actual throttle/IAC/TPS/bracket parts must move rigidly together;
    # this study records the frame proposal without altering installed assets.
    report={'status':'PROPOSAL_CHECKS_PASS' if shape.is_valid and len(shape.solids())==1 and checks['lower_flange_symmetric_difference_mm3']<.1 and all(x['blocked_volume_mm3']<.1 for x in checks['runner_probes']) and envelope_hit<.1 and old_hit>1 and all(x['cap_envelope_overlap_mm3']<.1 for x in moved) and checks['throttle-housing_new_intake_overlap_mm3']<.1 and checks['throttle-gasket_new_intake_overlap_mm3']<.1 else 'PROPOSAL_CHECKS_FAIL','scope':'Isolated inferred envelope; not installed; full neighboring assembly audit outstanding','parameters':{'rear_x':REAR,'front_x':FRONT,'length':FRONT-REAR,'plenum_yz_center':[25,490],'throttle_frame_delta_mm':THROTTLE_DELTA,'egr_frame_delta_mm':EGR_DELTA,'cap_station_mm':[CAP_X,-12,419],'runner_terminal_x_mm':[float((p@1).X) for p in paths]},'checks':checks,'input_hashes':{str(p.relative_to(ROOT)):sha(p) for p in [Path(__file__),ROOT/'cad/engine/efi_intake.py',ROOT/'cad/engine/egr.py',ROOT/'cad/engine/regulator_vacuum.py',ROOT/'cad/engine/pilot/oil-cap/oil_cap.py',ROOT/'inventory/engine/full-assembly.json',ROOT/defs['efi-upper-intake']['step'].lstrip('/')]}}
    extra_paths.extend(ROOT/'cad/engine'/n for n in ('assembly_math.py','valvetrain_dispatch.py','valve_source_integration.py','valve_source_layout.py','valve_layout_integration.py','valve_layout_candidate.py','valve_motion_candidate.py','valve_dimensions_candidate.py','valve_spring_seating_candidate.py','oil_fill_neck_candidate.py','intake_egr_routes_candidate.py'))
    report['input_hashes'].update({str(p.relative_to(ROOT)):sha(p) for p in extra_paths})
    report['input_hashes_before']={p:before[p] for p in report['input_hashes']}
    report['input_guard_pass']=report['input_hashes_before']==report['input_hashes']
    assert report['input_guard_pass'],'Inputs changed during proposal'
    joint=checks['relocated_cap_cover']
    report['step_roundtrip_checks']=BAKE_ROWS
    import numpy as np
    import trimesh
    meshchecks=[];scene=trimesh.Scene()
    for name,part in [('upper-intake',shape),('cover',newcover),('cap',newcap),('seal',newseal)]:
        vertices,faces=part.tessellate(.12,.15);xyz=np.array([tuple(v) for v in vertices])
        mesh=trimesh.Trimesh(vertices=xyz[:,[0,2,1]]*np.array([1,1,-1])/1000,faces=faces)
        target=out/(name+'.glb');target.write_bytes(trimesh.Scene(mesh).export(file_type='glb'));scene.add_geometry(mesh,node_name=name)
        rt=trimesh.load(target,force='mesh');a=np.asarray(rt.vertices);back=np.column_stack((a[:,0],-a[:,2],a[:,1]))*1000
        bb=part.bounding_box();delta=float(np.max(np.abs(np.array([back.min(0),back.max(0)])-np.array([tuple(bb.min),tuple(bb.max)]))))
        meshchecks.append({'id':name,'bounds_error_mm':delta,'watertight':rt.is_watertight,'sha256':sha(target)})
        assert delta<.15 and rt.is_watertight
    (out/'assembly.glb').write_bytes(scene.export(file_type='glb'));report['mesh_exports']=meshchecks
    report['gate_summary']={'base_interfaces':report['status']=='PROPOSAL_CHECKS_PASS','static_neighbors':not checks['neighbor_audit']['new_or_worsened'],'withdrawal_neighbors':not checks['full_withdrawal_neighbors']['failures'],'egr_contacts':all(r['distance_mm']<.002 and r['overlap_mm3']<.1 for r in checks['egr_routes']['interfaces']),'rocker_motion':checks['relocated_cap_motion']['status']=='PASS','cap_joint':joint['cover_valid'] and joint['cover_solids']==1 and joint['seated_overlap_mm3']<.1 and joint['seal_overlap_mm3']<.1 and joint['seal_distance_mm']<.002 and joint['old_hole_closed_probe_mm3']>600 and joint['fill_path_blocked_mm3']<.1 and joint['straight_pull_overlap_mm3']>1 and joint['oversized_bore_pull_overlap_mm3']<.1 and all(r['cap_overlap_mm3']<.1 and r['seal_overlap_mm3']<.1 for r in joint['screw_removal'])}
    report['status']='COORDINATION_REQUIRED' if all(report['gate_summary'].values()) else 'GEOMETRY_REWORK_REQUIRED'
    report['manifest_before']=manifest_before;report['manifest_after']=sha(manifest)
    report['render']={'path':str((out/'comparison.svg').relative_to(ROOT)),'sha256':sha(out/'comparison.svg'),'section_path':str((out/'neck-section.svg').relative_to(ROOT)),'section_sha256':sha(out/'neck-section.svg')}
    b.export_step(shape,out/'upper-intake.step');(out/'validation.json').write_text(json.dumps(report,indent=2)+'\n')
    print(report['status'],flush=True)
    sys.exit(0 if report['status']=='PROPOSAL_CHECKS_PASS' else 1)
