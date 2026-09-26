#!/usr/bin/env python3
"""Validate isolated casting detail against immutable719/1323 geometry context."""
from pathlib import Path
import hashlib,json,sys,platform
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'cad/engine'))
import build123d as b
import numpy as np
import trimesh
import intake_exterior_candidate as candidate
from assembly_math import transforms
OUT=ROOT/'cad/engine/generated/intake-exterior-study';OUT.mkdir(exist_ok=True)
STAGE=ROOT/'cad/engine/generated/intake-cap-integration-stage'
CHANGED={'efi-upper-intake','valve-cover','oil-filler-cap','oil-filler-cap-seal','egr-exhaust-tube','egr-tube-heat-sleeve','egr-tube-valve-nut','egr-control-vacuum-hose'}
PRE_IAC={'iac-armature','iac-gasket','iac-valve-body','throttle-housing','throttle-shaft','throttle-plate'}
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def volume(s):return sum(z.volume for z in s.solids()) if s else 0.
def difference(a,z):
    if not a:return 0.
    if not z:return volume(a)
    aa=a if isinstance(a,b.Shape) else b.Compound(children=list(a))
    zz=z if isinstance(z,b.Shape) else b.Compound(children=list(z))
    return volume(aa-zz)
def path_for(d,kind):
    if d['id'] in CHANGED:return STAGE/('step' if kind=='step' else 'models')/(d['id']+'.'+kind)
    if d['id'] in PRE_IAC:return OUT/'baseline'/(d['id']+'.'+kind)
    return ROOT/d[kind].lstrip('/')
def bake(shape,name):
    path=OUT/(name+'.step');b.export_step(shape,path);s=b.import_step(path)
    assert s.is_valid and len(s.solids())==len(shape.solids()) and abs(volume(s)-volume(shape))<.1,name
    return s

def render(meshes,path):
    """Depth-buffered actual GLB triangles; no conceptual geometry or AI image."""
    import base64,struct,zlib
    width,height=1400,720
    pixels=np.full((height,width,3),(247,249,251),dtype=np.uint8)
    depths=np.full((height,width),-np.inf)
    view=np.array([.45,-.67,.59]);view/=np.linalg.norm(view)
    right=np.array([.83,.557,0.]);right/=np.linalg.norm(right);up=np.cross(view,right)
    for panel,mesh in enumerate(meshes):
        a=np.asarray(mesh.vertices);v=np.column_stack((a[:,0],-a[:,2],a[:,1]))*1000
        tri=v[np.asarray(mesh.faces)]-np.array([0,-65,440])
        normals=np.cross(tri[:,1]-tri[:,0],tri[:,2]-tri[:,0]);normals/=np.maximum(np.linalg.norm(normals,axis=1)[:,None],1e-9)
        uv=np.stack([tri@right,-tri@up],axis=-1)*.84+np.array([350+panel*700,420]);zs=tri@view
        shades=.42+.58*np.maximum(normals@np.array([.2,-.4,.89]),0)
        for pts,depth,shade,normal in zip(uv,zs,shades,normals):
            if normal@view<=0:continue
            xmin=max(0,int(np.floor(pts[:,0].min())));xmax=min(width-1,int(np.ceil(pts[:,0].max())))
            ymin=max(0,int(np.floor(pts[:,1].min())));ymax=min(height-1,int(np.ceil(pts[:,1].max())))
            if xmin>xmax or ymin>ymax:continue
            (x0,y0),(x1,y1),(x2,y2)=pts
            denominator=(y1-y2)*(x0-x2)+(x2-x1)*(y0-y2)
            if abs(denominator)<1e-12:continue
            xx,yy=np.meshgrid(np.arange(xmin,xmax+1)+.5,np.arange(ymin,ymax+1)+.5)
            w0=((y1-y2)*(xx-x2)+(x2-x1)*(yy-y2))/denominator
            w1=((y2-y0)*(xx-x2)+(x0-x2)*(yy-y2))/denominator;w2=1-w0-w1
            dz=w0*depth[0]+w1*depth[1]+w2*depth[2]
            target=depths[ymin:ymax+1,xmin:xmax+1];mask=(w0>=-1e-8)&(w1>=-1e-8)&(w2>=-1e-8)&(dz>target)
            target[mask]=dz[mask];pixels[ymin:ymax+1,xmin:xmax+1][mask]=np.array([178,186,190])*shade
    def chunk(name,data):return struct.pack('!I',len(data))+name+data+struct.pack('!I',zlib.crc32(name+data)&0xffffffff)
    raw=b''.join(b'\x00'+row.tobytes() for row in pixels)
    png=b'\x89PNG\r\n\x1a\n'+chunk(b'IHDR',struct.pack('!2I5B',width,height,8,2,0,0,0))+chunk(b'IDAT',zlib.compress(raw,9))+chunk(b'IEND',b'')
    path.with_suffix('.png').write_bytes(png)
    svg=['<svg xmlns="http://www.w3.org/2000/svg" width="1400" height="720">',
         '<image width="1400" height="720" href="data:image/png;base64,'+base64.b64encode(png).decode()+'"/>',
         '<text x="25" y="32" font-family="sans-serif" font-size="23">Actual exported meshes — source-compared casting exterior candidate</text>',
         '<text x="35" y="80" font-family="sans-serif" font-size="19">Checked compact casting baseline</text>',
         '<text x="735" y="80" font-family="sans-serif" font-size="19">Rounded shoulder, ribs and observed raised wording</text>',
         '<text x="25" y="680" font-family="sans-serif" font-size="17">Feature existence follows owner/specimen photos; dimensions and font shapes are estimates. No interface relocation.</text>','</svg>']
    path.write_text('\n'.join(svg))

def main():
    manifest_path=STAGE/'full-assembly.json';manifest=json.loads(manifest_path.read_text());defs={d['id']:d for d in manifest['definitions']};poses=transforms(manifest)
    assert len(defs)==719 and len(manifest['occurrences'])==1323
    sources=[Path(__file__),ROOT/'cad/engine/intake_exterior_candidate.py',ROOT/'cad/engine/upper_intake_clearance_candidate.py',ROOT/'cad/engine/egr.py',ROOT/'cad/engine/regulator_vacuum.py',ROOT/'cad/engine/assembly_math.py',ROOT/'cad/engine/valvetrain_dispatch.py',ROOT/'reference/engine/intake-exterior-review.json',manifest_path]
    sources.extend(ROOT/'cad/engine'/name for name in ('valve_source_integration.py','valve_source_layout.py','valve_layout_integration.py','valve_layout_candidate.py','valve_motion_candidate.py','valve_dimensions_candidate.py','valve_spring_seating_candidate.py'))
    sources.extend(ROOT/p for p in ('cad/engine/throttle_return_spring_candidate.py','cad/engine/throttle_return_spring_integration.py','cad/engine/throttle_linkage_candidate.py','cad/engine/throttle_shield_candidate.py','reference/engine/throttle-return-spring-review.json','inventory/engine/throttle-return-spring-candidate-validation.json'))
    assets={path_for(d,kind) for d in defs.values() for kind in ('step','glb')}
    before={str(p):sha(p) for p in set(sources)|assets|set(candidate.FONTS.values())}
    tracked=set(sources)|set(candidate.FONTS.values())
    shape,old,paths,features,air=candidate.parts();shape=bake(shape,'upper-intake-exterior');old=bake(old,'compact-baseline')
    # Exact agreement with the checked scene's starting casting prevents an
    # exterior patch from silently changing the source/interface baseline.
    baseline_path=path_for(defs['efi-upper-intake'],'step');tracked.add(baseline_path)
    baseline=poses['efi-upper-intake']*b.import_step(baseline_path)
    baseline_diff=volume(old-baseline)+volume(baseline-old);assert baseline_diff<.1
    regions={
      'lower flange and seven studs':b.Pos(0,-228,366.5)*b.Box(800,60,15),
      'throttle mating pad and ports':b.Pos(200,25,490)*b.Box(16,124,68),
      'EGR mating pad and port':b.Pos(-197,25,514)*b.Box(16,62,28),
      'regulator vacuum bore/seat protected R10':b.Pos(0,-47,460)*b.Rot(90,0,0)*b.Cylinder(10,20),
    }
    interfaces=[]
    for name,region in regions.items():
        diff=difference(shape&region,old&region)+difference(old&region,shape&region);interfaces.append({'interface':name,'symmetric_difference_mm3':diff})
    new_air_blockage=difference(shape&air,old&air)
    probes=[]
    for i,(x,path) in enumerate(zip(candidate.core.PORTS,paths),1):
        wire=b.Wire([b.Line((x,-228,359),path@0),path]);probe=b.sweep(b.Plane(origin=wire@0,z_dir=wire%0)*b.Circle(12),path=wire)
        probes.append({'cylinder':i,'blocked_volume_mm3':volume(shape&probe)})
    envelope=b.Pos(300,-12,414.75)*b.Cylinder(15.9,41.5)+b.Pos(300,-12,435)*b.Cylinder(37,44)
    cap_hit=volume(shape&envelope)
    # Relevant fault controls: a plugged runner and a new front protrusion.
    path=paths[0];plug=b.Plane(origin=path@.55,z_dir=path%.55)*b.Cylinder(17,10)
    bad_air=difference((shape+plug)&air,old&air);bad_cap=volume((shape+b.Pos(250,-12,450)*b.Box(110,10,10))&envelope)
    assert bad_air>1 and bad_cap>1
    print('Interface/air checks',interfaces,new_air_blockage,cap_hit,flush=True)
    # Added exterior is static; all original rocker/shaft interfaces remain
    # unchanged. Audit candidate against every actor in the frozen scene.
    local_bounds={};pairs=[];excluded=0;bb=shape.bounding_box();alo=np.array(tuple(bb.min));ahi=np.array(tuple(bb.max))
    for o in manifest['occurrences']:
        if o['id']=='efi-upper-intake':continue
        d=defs[o['definition']];gp=path_for(d,'glb');tracked.add(gp)
        if d['id'] not in local_bounds:
            a=np.asarray(trimesh.load(gp,force='mesh').vertices);v=np.column_stack((a[:,0],-a[:,2],a[:,1]))*1000;local_bounds[d['id']]=(v.min(0)-.2,v.max(0)+.2)
        lo,hi=local_bounds[d['id']];corners=np.array([tuple(b.Vertex(x,y,z).moved(poses[o['id']]).center()) for x in (lo[0],hi[0]) for y in (lo[1],hi[1]) for z in (lo[2],hi[2])]);lo,hi=corners.min(0),corners.max(0)
        if np.any(ahi<lo) or np.any(hi<alo):excluded+=1;continue
        sp=path_for(d,'step');tracked.add(sp);neighbor=bake(poses[o['id']]*b.import_step(sp),'neighbor-'+o['id'])
        hit=volume(shape&neighbor);prior=volume(old&neighbor) if hit>.1 else 0.
        pairs.append({'neighbor':o['id'],'overlap_mm3':hit,'baseline_overlap_mm3':prior,'new_or_worsened':hit>prior+.1});print('Neighbor',o['id'],hit,flush=True)
    # Removing material cannot create a collision; only added metal needs a
    # new sweep relative to the already checked compact casting.
    added=shape-old
    added=b.Compound(children=list(added.solids()))
    ab=added.bounding_box();newlo=np.array(tuple(ab.min));newhi=np.array(tuple(ab.max))
    assemblies={a['id']:a for a in manifest['assemblies']}
    def throttle_actor(o):
        parent=o.get('parent')
        while parent in assemblies:
            a=assemblies[parent]
            if (a.get('motion') or {}).get('type')=='throttle':return True
            parent=a.get('parent')
        return False
    rockers=[o for o in manifest['occurrences'] if o.get('valvetrain',{}).get('role')=='rocker']
    throttles=[o for o in manifest['occurrences'] if throttle_actor(o)]
    angles=set(range(0,721,5))
    for phase in range(0,720,120):
        for peak in (246,468):
            for delta in (-135,0,135):angles.add((phase+peak+delta)%720)
    motion=[]
    for family,actors,phases in [('rocker',rockers,sorted(angles)),('throttle',throttles,list(range(0,91,2)))]:
        focused=dict(manifest,occurrences=actors)
        for angle in phases:
            pp=transforms(focused,angle if family=='rocker' else 0,throttle_degrees=angle if family=='throttle' else 0)
            for o in actors:
                lo,hi=local_bounds[o['definition']]
                corners=np.array([tuple(b.Vertex(x,y,z).moved(pp[o['id']]).center()) for x in (lo[0],hi[0]) for y in (lo[1],hi[1]) for z in (lo[2],hi[2])]);lo,hi=corners.min(0),corners.max(0)
                lower=float(np.linalg.norm(np.maximum(np.maximum(newlo-hi,lo-newhi),0)))
                row={'family':family,'angle_deg':angle,'actor':o['id'],'added_material_aabb_distance_lower_mm':lower,'overlap_mm3':0.}
                if lower<=0:
                    sp=path_for(defs[o['definition']],'step');tracked.add(sp)
                    actor=bake(pp[o['id']]*b.import_step(sp),'motion-'+o['id']+'-'+str(angle));row['overlap_mm3']=volume(shape&actor)
                motion.append(row)
    # The complete current spring path fits a continuous cylinder: all hook
    # controls are at radius<=20mm, helix radius_at lies within6..10mm and the
    # .7mm tangent handles remain inside20mm. Add the .45mm wire radius.
    from throttle_return_spring_candidate import PARAMS,AXIS
    assert PARAMS['wire_radius']==.45 and PARAMS['moving_radius']==18 and list(AXIS)==[394.,25.,490.]
    spring_envelope=b.Pos(227,97.25,490)*b.Rot(90,0,0)*b.Cylinder(20.45,20.4)
    spring_hit=volume(shape&spring_envelope)
    spring_bad=volume(shape&(b.Pos(-40,0,0)*spring_envelope))
    assert spring_bad>1
    meshes=[];exports=[]
    for name,part in [('compact-baseline',old),('upper-intake-exterior',shape)]:
        vertices,faces=part.tessellate(.12,.15);v=np.array([tuple(p) for p in vertices]);mesh=trimesh.Trimesh(vertices=v[:,[0,2,1]]*np.array([1,1,-1])/1000,faces=faces)
        mesh.vertices=mesh.vertices.astype(np.float32);mesh.merge_vertices(digits_vertex=8)
        zero_faces=int(np.count_nonzero(mesh.area_faces==0));mesh.update_faces(mesh.area_faces>0);mesh.remove_unreferenced_vertices()
        mesh.visual.vertex_colors=[178,186,190,255];path=OUT/(name+'.glb');path.write_bytes(trimesh.Scene(mesh).export(file_type='glb'));rt=trimesh.load(path,force='mesh');rt.merge_vertices(digits_vertex=8)
        a=np.asarray(rt.vertices);world=np.column_stack((a[:,0],-a[:,2],a[:,1]))*1000;box=part.bounding_box();error=float(np.max(np.abs(np.array([world.min(0),world.max(0)])-np.array([tuple(box.min),tuple(box.max)]))))
        assert rt.is_watertight and error<.15,(name,error,rt.is_watertight)
        exports.append({'id':name,'glb_sha256':sha(path),'step_sha256':sha(OUT/(name+'.step')),'mesh_bounds_error_mm':error,'watertight':rt.is_watertight,'zero_area_faces_removed_after_float32_quantization':zero_faces});meshes.append(rt)
    render(meshes,OUT/'mesh-comparison.svg')
    after={str(p):sha(p) for p in tracked};assert all(before[p]==h for p,h in after.items()),'Inputs changed during exterior audit'
    passed=all(x['symmetric_difference_mm3']<.1 for x in interfaces) and new_air_blockage<.1 and all(x['blocked_volume_mm3']<.1 for x in probes) and cap_hit<.1 and not any(x['new_or_worsened'] for x in pairs) and all(r['overlap_mm3']<.1 for r in motion) and spring_hit<.1
    report={'status':'PASS bounded exterior candidate; current722 context and browser pending' if passed else 'FAIL exterior geometry requires rework','baseline_scope':'Immutable719definitions/1323occurrences;8coordinated staged overrides plus6verified pre-IAC/plate restoreddefinitions. Current IAC additions/replacements intentionally excluded and require later audit.','valid':shape.is_valid,'solid_count':len(shape.solids()),'baseline_difference_mm3':baseline_diff,'protected_interfaces':interfaces,'new_air_blockage_mm3':new_air_blockage,'runner_probes':probes,'cap_withdrawal_overlap_mm3':cap_hit,'negative_controls':{'plugged_runner_new_air_blockage_mm3':bad_air,'front_protrusion_cap_overlap_mm3':bad_cap,'spring_envelope_shifted_toward_casting_overlap_mm3':spring_bad},'neighbor_audit':{'exact_pairs':len(pairs),'aabb_excluded':excluded,'pairs':pairs,'new_or_worsened':[r for r in pairs if r['new_or_worsened']]},'motion':{'rocker_phases':len(angles),'throttle_phases':46,'pairs':len(motion),'spring_continuous_envelope_overlap_mm3':spring_hit,'spring_envelope':{'axis_xz_mm':[227,490],'radius_mm':20.45,'y_extent_mm':[87.05,107.45],'basis':'All current hook/Bezier control points and bounded-radius helix plus wire; all0–90degree spring poses.'},'minimum_added_material_aabb_bound_mm':min(r['added_material_aabb_distance_lower_mm'] for r in motion),'failures':[r for r in motion if r['overlap_mm3']>.1],'scope':'Added metal versus12rockers at181phases and rigid throttle descendants at46poses. Spring uses a continuous source-code-bounded envelope; current IAC/plate update excluded.'},'exports':exports,'feature_ids':list(features),'environment':{'python':platform.python_version(),'build123d':b.__version__},'input_sha256':{str(Path(p).relative_to(ROOT)) if Path(p).is_relative_to(ROOT) else p:h for p,h in after.items()},'input_guard_pass':True,'render_sha256':sha(OUT/'mesh-comparison.svg')}
    (ROOT/'inventory/engine/intake-exterior-candidate-validation.json').write_text(json.dumps(report,indent=2)+'\n');(OUT/'validation.json').write_text(json.dumps(report,indent=2)+'\n');print(report['status']);sys.exit(0 if passed else 1)
if __name__=='__main__':main()
