"""Two stationary valve stations in installed coordinates; unpublished candidate.

Snapshots saved neighbor STEP files before working; never overwrites installed
geometry, shared manifest or viewer modules. See exported provenance for limits.
"""
from pathlib import Path
import json, math, hashlib, shutil, sys
import build123d as b
from assembly_math import transforms
from valve_motion_candidate import lobe_shape, PIVOT_Y
ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'cad/engine/candidates/valve-station'
BASE=OUT/'baseline'
DECK=254.
PIVOT_Z=383.5
CUP_Z=367.5
LIFTER_BODY_Z=116.
PUSHROD_LENGTH=226.6


def snapshot():
    OUT.mkdir(parents=True,exist_ok=True);BASE.mkdir(exist_ok=True)
    # Snapshot only on first run. Delete baseline deliberately to adopt new input.
    saved=BASE/'manifest.json'
    if not saved.exists():shutil.copy2(ROOT/'inventory/engine/full-assembly.json',saved)
    m=json.loads(saved.read_text())
    definitions={d['id']:d for d in m['definitions']}
    ids={'cylinder-head','block','camshaft','valve-cover','pushrod','rocker-arm','rocker-fulcrum','rocker-bolt','rocker-guide','intake-valve','exhaust-valve','valve-spring','valve-seal','spring-retainer','valve-keeper'}
    ids|={k for k in definitions if k.startswith('lifter-')}
    ids|={o['definition'] for o in m['occurrences'] if o['id'].startswith('spark-plug-1-') or o['id']=='c1-piston-1'}
    hashes={}
    for name in sorted(ids):
        path=BASE/(name+'.step')
        if not path.exists():shutil.copy2(ROOT/definitions[name]['step'].lstrip('/'),path)
        hashes[name]=hashlib.sha256(path.read_bytes()).hexdigest()
    return m,hashes


def rocker():
    s=b.Pos(0,36-PIVOT_Y,-8)*b.Box(17,119,11)
    # Rounded valve pad preserves a unique tangent contact through rocker travel.
    pad_y=-16-PIVOT_Y
    patch=b.Pos(0,pad_y,-11)*b.Box(30,20,6)
    original=s
    s-=patch
    s+=(b.Pos(0,pad_y,-1.5)*b.Sphere(12)) & patch & original
    s-=b.Sphere(15)
    s-=b.Pos(0,90-PIVOT_Y,-16)*b.Sphere(3.8)
    s-=b.Pos(0,0,-8)*b.Cylinder(5,30)
    return s


def fulcrum():
    s=b.Sphere(15)&b.Pos(0,0,-7.5)*b.Box(30,30,15)
    s+=b.Pos(0,0,-14)*b.Cylinder(6,4)
    s-=b.Cylinder(5.2,40)
    return s


def pushrod():
    s=b.Cylinder(3.8,PUSHROD_LENGTH)
    for z in [-PUSHROD_LENGTH/2,PUSHROD_LENGTH/2]:s+=b.Pos(0,0,z)*b.Sphere(3.8)
    return s-b.Cylinder(1.2,PUSHROD_LENGTH+10)


def cup():
    return b.Cylinder(8,5)-b.Pos(0,0,4)*b.Sphere(3.8)-b.Cylinder(1,10)


def head_adapter(head,stations):
    for x in stations:
        # Remove only old boss above floor. Keep old floor drilling blind.
        head-=b.Pos(x,36,(48.5+109)/2)*b.Cylinder(12.001,109-48.5)
        head+=b.Pos(x,PIVOT_Y,(48+108)/2)*b.Cylinder(12,108-48)
        head-=b.Pos(x,PIVOT_Y,94)*b.Cylinder(4.6,43)
    return head


def cam_adapter(cam,stations):
    profile=json.loads((ROOT/'cad/engine/candidates/valve-motion/profile.json').read_text())['profile']
    lobe=lobe_shape(profile)
    for x,phase in zip(stations,[234,123]):
        cutter=b.Pos(x,0,0)*b.Rot(0,90,0)*b.Cylinder(26,15)
        cut=cam-cutter
        solids=list(cut) if isinstance(cut,b.ShapeList) else cut.solids()
        replacement=b.Pos(x,0,0)*b.Rot(phase,0,0)*lobe
        fused=replacement.fuse(*solids)
        cam=b.Compound(children=list(fused)) if isinstance(fused,b.ShapeList) else fused
        assert len(cam.solids())==1,('cam fusion',x,len(cam.solids()))
        cam=cam.solids()[0]
    return cam


def intersect_volume(a,c):
    inter=a&c
    return sum(s.volume for s in inter.solids()) if inter else 0


def box_overlap(a,c):
    aa=a.bounding_box();cc=c.bounding_box()
    return all(min(getattr(aa.max,k),getattr(cc.max,k))-max(getattr(aa.min,k),getattr(cc.min,k))>0.001 for k in ['X','Y','Z'])


def solve(lift):
    a=90-PIVOT_Y;v=PIVOT_Y+16;L=PUSHROD_LENGTH
    low=0.;high=.3
    for _ in range(60):
        t=(low+high)/2;dy=a*(math.cos(t)-1)+16*math.sin(t)
        result=a*math.sin(t)+16*(1-math.cos(t))+L-math.sqrt(L*L-dy*dy)
        if result<lift:low=t
        else:high=t
    t=(low+high)/2
    # Bottom of R12 curved pad centred at localZ=-1.5 contacts flat valve tip.
    valve_lift=v*math.sin(t)+1.5*(math.cos(t)-1)
    top=(PIVOT_Y+a*math.cos(t)+16*math.sin(t),PIVOT_Z+a*math.sin(t)-16*math.cos(t))
    bottom=(90,140.9+lift)
    return {'angle':t,'valve_lift':valve_lift,'top':top,'bottom':bottom,
      'closure_error':math.hypot(top[0]-bottom[0],top[1]-bottom[1])-L}


def main():
    m,hashes=snapshot();loc=transforms(m)
    defs={n:b.import_step(BASE/(n+'.step')) for n in hashes}
    occ={o['id']:o for o in m['occurrences']}
    stations=[occ[f'c1-{kind}-valve']['position_cad_mm'][0] for kind in ['intake','exhaust']]
    candidate={'cylinder-head':head_adapter(defs['cylinder-head'],stations),'rocker-arm':rocker(),'rocker-fulcrum':fulcrum(),'pushrod':pushrod(),'lifter-pushrod-cup':cup(),'camshaft':cam_adapter(defs['camshaft'],stations)}
    placed={}
    unchanged=['block','valve-cover']
    for name in unchanged:placed[name]=defs[name].moved(loc[name])
    placed['cylinder-head']=candidate['cylinder-head'].moved(loc['cylinder-head'])
    placed['camshaft']=candidate['camshaft'].moved(loc['camshaft'])
    for oid,o in occ.items():
        if oid.startswith('spark-plug-1-') or oid=='c1-piston-1':
            placed[oid]=defs[o['definition']].moved(loc[oid])
    for kind,x in zip(['intake','exhaust'],stations):
        tag=f'c1-{kind}'
        for oid,o in occ.items():
            if not oid.startswith(tag+'-'):continue
            definition=o['definition']
            if definition not in defs:continue
            position=list(o['position_cad_mm']);shape=candidate.get(definition,defs[definition])
            if oid.endswith('-rocker') or oid.endswith('-fulcrum'):
                position=[x,PIVOT_Y,PIVOT_Z]
            elif oid.endswith('-guide') or oid.endswith('-rocker-bolt'):position[1]=PIVOT_Y
            elif oid.endswith('-pushrod'):position=[x,90,(140.9+367.5)/2]
            elif '-lifter-' in oid:position[2]-=12
            placed[oid]=b.Pos(*position)*b.Rot(*o.get('rotation_cad_deg',[0,0,0]))*shape
    checks=0;failures=[]
    keys=list(placed)
    for i,aid in enumerate(keys):
        for bid in keys[i+1:]:
            if not box_overlap(placed[aid],placed[bid]):continue
            if aid in unchanged and bid in unchanged:continue
            volume=intersect_volume(placed[aid],placed[bid]);checks+=1
            if volume>.1:failures.append({'a':aid,'b':bid,'overlap_mm3':volume})
    for name,shape in candidate.items():
        assert shape.is_valid and len(shape.solids())==1,name
        b.export_step(shape,OUT/(name+'.step'))
    b.export_step(b.Compound(children=list(placed.values())),OUT/'two-station-assembly.step')
    report={'status':'PASS static local candidate' if not failures else 'FAIL static local candidate',
      'baseline_manifest_sha256':hashlib.sha256((BASE/'manifest.json').read_bytes()).hexdigest(),
      'baseline_step_hashes':hashes,'static_exact_checks':checks,'overlap_failure_threshold_mm3':.1,'failures':failures,
      'placement':{'pivot_y':PIVOT_Y,'pivot_z':PIVOT_Z,'lifter_body_z':LIFTER_BODY_Z,'pushrod_ball_centers_distance':PUSHROD_LENGTH},
      'source':'Melling SYB-38 replacement ratio1.6 only; dimensions and contact construction are assumptions.',
      'limits':['Onlycylinder1 intake/exhaust local neighbors; other cylinders unchanged.','Onlytwo replacement cam lobes; remaining10 lobes are unchanged.','Zero-lash spherical contact is an ideal fit study, not production clearance.','Motion and spring compression require separate checks.']}
    (OUT/'provenance.json').write_text(json.dumps(report,indent=2)+'\n')
    # Preserve exact occurrence transforms for independent candidate checks.
    (OUT/'occurrence-layout.json').write_text(json.dumps({
      'stations':stations,'occurrences':[{
        'id':oid,'definition':occ[oid]['definition'] if oid in occ else oid,
        'position':list(shape.location.position),
        'orientation':list(shape.location.orientation)} for oid,shape in placed.items()]},indent=2)+'\n')
    print(json.dumps(report,indent=2),flush=True)

if __name__=='__main__':main()
