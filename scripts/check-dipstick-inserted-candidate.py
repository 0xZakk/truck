#!/usr/bin/env python3
"""Isolated inserted-blade validation; unrelated manifest/throttle edits allowed."""
from pathlib import Path
import hashlib,json,math,platform,subprocess,sys
import numpy as np
import build123d as b
import trimesh
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'cad/engine'))
import dipstick_inserted_candidate as candidate
from assembly_math import transforms
OUT=ROOT/'cad/engine/generated/dipstick-inserted-feasibility'
TUBE=ROOT/'cad/engine/generated/dipstick-tube-feasibility'
REPORT=ROOT/'inventory/engine/dipstick-inserted-candidate-validation.json'


def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def volume(s):return sum(q.volume for q in s.solids()) if s is not None else 0.
def overlap(a,c):return volume(a.intersect(c))
def bbox_overlap(a,c):
    return all(min(getattr(a.max,k),getattr(c.max,k))-max(getattr(a.min,k),getattr(c.min,k))>.001 for k in 'XYZ')
def dependency_summary(manifest,selected):
    occurrences={o['id']:o for o in manifest['occurrences']}
    assemblies={a['id']:a for a in manifest['assemblies']}
    parents=set()
    for oid in selected:
        parent=occurrences[oid]['parent']
        while parent in assemblies:
            parents.add(parent);parent=assemblies[parent]['parent']
    return {'occurrences':{oid:occurrences[oid] for oid in sorted(selected)},
            'assemblies':{a:assemblies[a] for a in sorted(parents)},
            'mechanism':{k:manifest['mechanism'][k] for k in ['stroke_mm','rod_length_mm']}}

def planar_contact(a,c,z):
    def faces(s):return [f for f in s.faces() if abs(f.bounding_box().min.Z-z)<1e-5 and abs(f.bounding_box().max.Z-z)<1e-5]
    return sum((common.area if common else 0) for f in faces(a) for g in faces(c) for common in [f.intersect(g)])

def main():
    OUT.mkdir(parents=True,exist_ok=True)
    manifest_path=ROOT/'inventory/engine/full-assembly.json'
    manifest=json.loads(manifest_path.read_text());poses=transforms(manifest)
    sources=[ROOT/'cad/engine/dipstick_inserted_candidate.py',Path(__file__),
             ROOT/'cad/engine/dipstick_tube_candidate.py',candidate.PILOT_PATH,
             ROOT/'docs/pilot/dipstick.md',ROOT/'cad/engine/assembly_math.py',
             ROOT/'inventory/engine/dipstick-tube-candidate-validation.json']
    frozen={str(p.relative_to(ROOT)):sha(p) for p in sources}
    parts,metadata=candidate.parts()
    body=parts['engine-oil-dipstick-blade-inserted'];handle=parts['engine-oil-dipstick-handle-inserted']
    tube_parts={}
    for name in ['block-candidate','engine-oil-dipstick-tube','engine-oil-dipstick-tube-retaining-nut',
                 'pushrod-cover-retainer-candidate','engine-oil-dipstick-tube-bracket','engine-oil-dipstick-tube-support-nut']:
        p=TUBE/(name+'.step');frozen[str(p.relative_to(ROOT))]=sha(p);tube_parts[name]=b.import_step(p)
    tube=tube_parts['engine-oil-dipstick-tube']
    checks={};scene=trimesh.Scene();render_items=[]
    for index,(name,shape) in enumerate(parts.items()):
        step=OUT/(name+'.step');b.export_step(shape,step);restored=b.import_step(step)
        vertices,faces=shape.tessellate(.1,.12)
        vertices=np.array([tuple(v) for v in vertices]);faces=np.array(faces)
        mesh=trimesh.Trimesh(vertices=vertices[:,[0,2,1]]*np.array([1,1,-1])*.001,faces=faces,process=False)
        mesh.visual.face_colors=[165,172,180,255] if index==0 else [223,182,30,255]
        scene.add_geometry(mesh,node_name=name)
        render_items.append({'name':name,'vertices':vertices.tolist(),'faces':faces.tolist()})
        bb=shape.bounding_box();mesh_bounds=np.stack((vertices.min(0),vertices.max(0)))
        err=np.max(np.abs(mesh_bounds-np.array([list(bb.min),list(bb.max)])))
        checks[name]={'valid':shape.is_valid,'solid_count':len(shape.solids()),'volume_mm3':volume(shape),
                     'step_roundtrip_error_mm3':abs(volume(restored)-volume(shape)),
                     'cad_mesh_bounds_error_mm':float(err)}
        assert shape.is_valid and restored.is_valid and len(shape.solids())==1
        assert checks[name]['step_roundtrip_error_mm3']<.02 and err<.5
    b.export_step(b.Compound(children=list(parts.values())),OUT/'engine-oil-dipstick-inserted.step')
    scene.export(OUT/'engine-oil-dipstick-inserted.glb')
    reopened=trimesh.load(OUT/'engine-oil-dipstick-inserted.glb',force='scene')
    assert len(reopened.geometry)==2
    glb_error=float(np.max(np.abs(reopened.bounds-scene.bounds))*1000)
    assert glb_error<.01
    expected_seat_area=math.pi*(5.25**2-4.25**2)
    seating={'stop_tube_gap_mm':handle.distance_to(tube),'stop_tube_contact_mm2':planar_contact(handle,tube,500),
             'stop_tube_overlap_mm3':overlap(handle,tube),'blade_handle_gap_mm':body.distance_to(handle),
             'blade_handle_contact_mm2':planar_contact(body,handle,500),'blade_handle_overlap_mm3':overlap(body,handle),
             'blade_tube_min_clearance_mm':body.distance_to(tube)}
    assert abs(seating['stop_tube_contact_mm2']-expected_seat_area)<.002
    assert seating['blade_handle_contact_mm2']>1.7
    assert seating['stop_tube_gap_mm']<.002 and seating['blade_handle_gap_mm']<.002
    assert seating['blade_tube_min_clearance_mm']>.1
    assert seating['stop_tube_overlap_mm3']<.001 and seating['blade_handle_overlap_mm3']<.001
    static=[];failures=[];selected=set()
    for name,neighbor in tube_parts.items():
        for part,shape in parts.items():
            v=overlap(shape,neighbor)
            static.append({'part':part,'neighbor':name,'overlap_mm3':v})
            if v>.1:failures.append(static[-1])
    boxes={name:s.bounding_box() for name,s in parts.items()}
    definitions={};definition_paths={}
    moving_groups={a['id'] for a in manifest['assemblies'] if (a.get('motion') or {}).get('type') in ('crank','rod','piston')}
    moving=[o for o in manifest['occurrences'] if o['parent'] in moving_groups]
    moving_defs={o['definition'] for o in moving}
    moving_shapes={}
    # Scan complete snapshot for a broad-phase candidate; only relevant files
    # and occurrence ancestry are frozen at the end, so unrelated work can run.
    print('Scanning installed neighbors',flush=True)
    for definition in manifest['definitions']:
        path=ROOT/definition['step'].lstrip('/');digest=sha(path)
        cache=TUBE/'brep-cache'/(digest+'.brep')
        shape=b.import_brep(cache) if cache.exists() else b.import_step(path)
        definitions[definition['id']]=shape;definition_paths[definition['id']]=(path,digest)
    distances={}
    for occ in manifest['occurrences']:
        oid=occ['id']
        if oid in ('block','pushrod-cover-bolt-1'):continue
        neighbor=poses[oid]*definitions[occ['definition']];bb=neighbor.bounding_box()
        for name,shape in parts.items():
            if not bbox_overlap(boxes[name],bb):continue
            selected.add(oid)
            v=overlap(shape,neighbor)
            static.append({'part':name,'neighbor':oid,'overlap_mm3':v})
            if v>.1:failures.append(static[-1])
        if oid=='oil-pan':distances['blade_pan_min_distance_mm']=body.distance_to(neighbor)
    motion_checks=0;motion_failures=[]
    for degrees in range(0,721,10):
        if degrees%180==0:print('Motion',degrees,flush=True)
        at=transforms(manifest,degrees)
        for occ in moving:
            selected.add(occ['id'])
            neighbor=at[occ['id']]*definitions[occ['definition']];bb=neighbor.bounding_box()
            for name,shape in parts.items():
                if not bbox_overlap(boxes[name],bb):continue
                motion_checks+=1;v=overlap(shape,neighbor)
                if v>.1:motion_failures.append({'degrees':degrees,'part':name,'neighbor':occ['id'],'overlap_mm3':v})
    # Independent continuous bounds, using the frozen tube check's derivation.
    radius=manifest['mechanism']['stroke_mm']/2;length=manifest['mechanism']['rod_length_mm']
    crank_radius=max(43,math.hypot(33,radius),radius+37,69)
    envelope=b.Rot(0,90,0)*b.Cylinder(crank_radius,1000)
    continuous=[{'part':name,'neighbor':'crankshaft-envelope','overlap_mm3':overlap(shape,envelope)} for name,shape in parts.items()]
    assembly_map={a['id']:a for a in manifest['assemblies']}
    for occ in moving:
        kind=assembly_map[occ['parent']]['motion']['type']
        if kind not in ('rod','piston'):continue
        bb=(poses[occ['id']]*definitions[occ['definition']]).bounding_box()
        if kind=='rod':
            local=definitions[occ['definition']].bounding_box()
            ly=max(abs(local.min.Y),abs(local.max.Y));lz=max(abs(local.min.Z),abs(local.max.Z))
            by=radius*max(abs(1-local.min.Z/length),abs(1-local.max.Z/length))+ly
            bz=radius+math.hypot(ly,lz)
            env=b.Pos(bb.center().X,0,0)*b.Box(bb.size.X,2*by,2*bz)
        else:env=b.Pos(*bb.center())*b.Box(bb.size.X,bb.size.Y,bb.size.Z+4*radius)
        ebb=env.bounding_box()
        for name,shape in parts.items():
            if bbox_overlap(boxes[name],ebb):continuous.append({'part':name,'neighbor':occ['id']+'-envelope','overlap_mm3':overlap(shape,env)})
    # Clearances must reject incompatible geometry and unseated length changes.
    oversize=b.Pos(-285,170,400)*b.Box(8,.8,10)
    shortened=tube-b.Pos(-285,170,488)*b.Cylinder(8,26)
    controls={'oversize_8mm_section_tube_overlap_mm3':overlap(oversize,tube),
              'short_guide_25mm_stop_gap_mm':handle.distance_to(shortened),
              'short_guide_unchanged_free_route_sum_mm':metadata['route_sum_mm']-25,
              'raised_stop_2mm_gap_mm':(b.Pos(0,0,2)*handle).distance_to(tube)}
    assert controls['oversize_8mm_section_tube_overlap_mm3']>.1
    assert controls['short_guide_25mm_stop_gap_mm']>24.9
    assert abs(controls['short_guide_unchanged_free_route_sum_mm']-candidate.P.blade_axial_length)>24.9
    assert controls['raised_stop_2mm_gap_mm']>1.9
    assert abs(metadata['route_sum_mm']-candidate.P.blade_axial_length)<1e-8
    selected.add('oil-pan')
    for oid in selected:
        occ=next(o for o in manifest['occurrences'] if o['id']==oid)
        path,digest=definition_paths[occ['definition']];frozen[str(path.relative_to(ROOT))]=digest
    dependency=dependency_summary(manifest,selected)
    assert dependency_summary(json.loads(manifest_path.read_text()),selected)==dependency,'Relevant occurrence or motion changed'
    assert all(sha(ROOT/path)==digest for path,digest in frozen.items()),'Relevant source or geometry changed'
    print('Pre-render failures',len(failures),len(motion_failures),'continuous',sum(x['overlap_mm3']>.001 for x in continuous),flush=True)
    # Tube/casting context for a generated review image; no restricted imagery.
    for name,shape in [('tube-context',tube),('block-context',tube_parts['block-candidate'].intersect(b.Pos(-307.5,30,25)*b.Box(85,250,140)))]:
        vv,ff=shape.tessellate(.4) # angular0.1 avoids OCC null triangulation on tiny trimmed faces
        render_items.append({'name':name,'vertices':[list(v) for v in vv],'faces':[list(f) for f in ff]})
    (OUT/'render-mesh.json').write_text(json.dumps(render_items))
    render_code=RENDER_PLOT
    subprocess.run(['python3','-c',render_code,str(OUT)],check=True)
    report={'schema_version':1,'issue':17,'interface_issue':78,'baseline_commit':subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),
        'readiness':'isolated flexed educational pose; not installed or Done',
        'status':'PASS bounded geometry' if not failures and not motion_failures and all(x['overlap_mm3']<.001 for x in continuous) else 'FAIL',
        'snapshot_manifest_sha256':sha_bytes(json.dumps(manifest,sort_keys=True).encode()),
        'manifest_hash_method':'canonical sorted JSON; snapshot context only; unrelated edits allowed',
        'frozen_relevant_inputs_sha256':frozen,'relevant_manifest_subset':dependency,
        'environment':{'python':platform.python_version(),'build123d':b.__version__,'platform':platform.platform()},
        'lengths_and_pose':metadata,'shape_checks':checks,'glb_roundtrip_bounds_error_mm':glb_error,
        'seating':seating,'sump':distances,'static_comparisons':static,'static_failures':failures,
        'motion_degrees':list(range(0,721,10)),'motion_checks':motion_checks,'motion_failures':motion_failures,
        'continuous_bounds':continuous,'negative_controls':controls,
        'limits':['Rigid flexed display pose, not elastic insertion/withdrawal simulation.',
                  '692.15mm is an approximate seller axial comparison; physical material centerline grows with inherited estimated waves.',
                  'Original section, wave, handle and stamp-position dimensions are estimates. No ADD/FULL calibration or owner identity claim.',
                  'Stop seats on tube mouth and blade touches handle; friction fit, attachment strength and retention force unvalidated.',
                  'Whole-engine scan is a snapshot; only named relevant geometry/occurrence dependencies are frozen.'],
        'outputs_sha256':{str(p.relative_to(ROOT)):sha(p) for p in OUT.iterdir() if p.suffix in ('.step','.glb','.png')}}
    assert all(sha(ROOT/path)==digest for path,digest in frozen.items()),'Relevant input changed during rendering'
    REPORT.write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({'status':report['status'],'static_checks':len(static),'motion_checks':motion_checks,'lengths':metadata,'seating':seating}),flush=True)
    assert report['status']=='PASS bounded geometry',failures+motion_failures

def sha_bytes(data):return hashlib.sha256(data).hexdigest()

RENDER_PLOT = '''import sys,json,pathlib,numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
out=pathlib.Path(sys.argv[1]);items=json.loads((out/'render-mesh.json').read_text())
fig=plt.figure(figsize=(13,10),facecolor='#f4f6f8')
for i in [1,2]:
 ax=fig.add_subplot(1,2,i,projection='3d');ax.set_facecolor('#f4f6f8')
 for item in items:
  name=item['name'];v=np.array(item['vertices']);f=np.array(item['faces'])
  color='#e2b322' if 'handle' in name else '#89939c' if 'blade' in name else '#557085'
  alpha=.09 if 'context' in name else 1
  ax.add_collection3d(Poly3DCollection(v[f],facecolor=color,edgecolor='none',alpha=alpha))
 if i==1:
  ax.set(xlim=(-345,-250),ylim=(0,210),zlim=(-175,585));ax.set_box_aspect((95,210,760));ax.set_title('Inserted strip and full free tip')
 else:
  ax.set(xlim=(-310,-265),ylim=(155,185),zlim=(435,578));ax.set_box_aspect((45,30,143));ax.set_title('Pilot waves and seated stop')
 ax.view_init(elev=15,azim=40);ax.set_xlabel('X mm');ax.set_ylabel('Y mm');ax.set_zlabel('Z mm')
fig.suptitle('Dipstick — isolated flexed display pose',fontsize=17)
fig.text(.5,.03,'Axial route692.15mm; wave material length reported separately. No oil-level calibration or elastic simulation.',ha='center',fontsize=10)
plt.tight_layout(rect=(0,.06,1,.94));fig.savefig(out/'inserted-review.png',dpi=160)
'''
if __name__=='__main__':main()
