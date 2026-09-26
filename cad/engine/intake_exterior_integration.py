"""Bounded exterior replacement after the coordinated compact-intake adapter."""
from pathlib import Path
import hashlib
import build123d as b
import trimesh
import numpy as np
import intake_exterior_candidate as candidate
from assembly_math import transforms
ROOT=Path(__file__).resolve().parents[2]
ID='efi-upper-intake'
SOURCE='upper-intake-exterior-study'
GAPS=['Visible border ribs, Ford oval/word and ELECTRONIC/FUEL INJECTION wording follow owner/specimen photos; all new dimensions and font outlines are inferred.',
      'Arial Bold and Brush Script are explicit system-font approximations, not traced factory lettering. Casting texture, lower mounting bosses and exact wall distribution remain incomplete.',
      'Protected flange/port/air regions and cap clearance remain those of the coordinated compact casting; this exterior detail does not establish factory dimensions.']

def sources():
    path=ROOT/'reference/engine/intake-exterior-review.json'
    return {SOURCE:{'title':'Owner and specimen observations for upper intake casting exterior','path':'/'+str(path.relative_to(ROOT)),
                    'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'url':'https://i.ebayimg.com/images/g/-qoAAOSwDTdlcJqH/s-l1200.jpg'}}

def clean_export(path,shape):
    """Drop only zero-area GLB triangles; retain normals/material and surfaces."""
    mesh=trimesh.load(path,force='mesh');before=len(mesh.faces);mask=mesh.area_faces>0
    if not mask.all():
        mesh.update_faces(mask);mesh.remove_unreferenced_vertices()
        path.write_bytes(trimesh.Scene(mesh).export(file_type='glb',include_normals=True))
    check=mesh.copy();check.merge_vertices(digits_vertex=8)
    assert check.is_watertight,'Exterior mesh has a real non-manifold/open edge'
    v=np.asarray(mesh.vertices);xyz=np.column_stack((v[:,0],-v[:,2],v[:,1]))*1000;box=shape.bounding_box()
    error=float(np.max(np.abs(np.array([xyz.min(0),xyz.max(0)])-np.array([tuple(box.min),tuple(box.max)]))))
    assert error<.2,'Exterior mesh bounds disagree with local CAD'
    return {'mesh_bounds_error_mm':error,'zero_area_faces_removed':before-len(mesh.faces),'triangle_count':len(mesh.faces),'watertight_after_coincident_vertex_weld':True}

def install(define,definitions,occurrences,assemblies,shapes,mechanism,mesh_dir):
    old=next(d for d in definitions if d['id']==ID)
    pose=transforms({'definitions':definitions,'occurrences':occurrences,'assemblies':assemblies,'mechanism':mechanism})[ID]
    current=shapes[ID] if ID in shapes else b.import_step(ROOT/old['step'].lstrip('/'))
    current=pose*current
    revised,base,_,_,_=candidate.parts()
    def vol(s):return sum(z.volume for z in s.solids()) if s else 0.
    base_error=vol(current-base)+vol(base-current)
    target_error=vol(current-revised)+vol(revised-current)
    if min(base_error,target_error)>=.1:raise ValueError('Exterior adapter requires the reviewed compact casting or its exact detailed successor')
    definitions[:]=[d for d in definitions if d['id']!=ID]
    function='A source-compared compact casting distributes air through six open runners. Rounded shoulders, raised borders and observed wording improve exterior recognition; their dimensions and font shapes remain inferred.'
    local=pose.inverse()*revised
    define(ID,local,old['name'],function,old['system'],old['color'],
           list(dict.fromkeys(old.get('sources',[])+[SOURCE])),list(dict.fromkeys(old.get('unresolved',[])+GAPS)),old.get('dimension_claims',[]),prepared=True)
    result=clean_export(Path(mesh_dir)/(ID+'.glb'),local)
    row=next(d for d in definitions if d['id']==ID);row['triangle_count']=result['triangle_count']
    size=local.bounding_box().size;row['model_bounds_mm']=[size.X,size.Y,size.Z]
    next(o for o in occurrences if o['id']==ID)['function']=function
    return {'changed_definitions':[ID],'changed_occurrences':[ID],'frame_changes':False,'recognized_input':'compact' if base_error<.1 else 'detailed',**result}
