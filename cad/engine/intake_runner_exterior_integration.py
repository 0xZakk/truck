"""Guarded additive runner-skin adapter; reviewed CAD-release fixtures required."""
from pathlib import Path
from functools import lru_cache
import hashlib,json,tempfile
import build123d as b
import numpy as np
import trimesh
import intake_runner_exterior_candidate as candidate
from assembly_math import transforms
from cad_metrics import solid_volume
ROOT=Path(__file__).resolve().parents[2]
STUDY=ROOT/'cad/engine/generated/intake-runner-exterior-study'
ID='efi-upper-intake';SOURCE='upper-intake-runner-exterior-study'
FUNCTION='The upper casting distributes air through six open runners. Broad runner faces and rounded shoulders follow visible casting form; section dimensions, wall distribution and earlier lettering details remain estimates.'
GAPS=['Broad runner faces follow owner/Ford comparisons and a later F5TE-marked specimen; the specimen is not established as the owner1994 casting.', 'Runner widths34–56mm, depths34–46mm, R9 edges and transition stations are inferred exterior estimates. Existing circular air passages are preserved project datums, not measured factory sections.', 'No PCV receiver or unresolved intake support lower anchor is inferred from these exterior faces.']
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def volume(s):
 solids=list(s.solids()) if s else [];assert all(q.is_valid for q in solids)
 return sum(abs(solid_volume(q,'adaptive')) for q in solids)
def compound(s):return b.Compound(children=list(s.solids()))
def difference(a,z):return volume(compound(a)-compound(z))+volume(compound(z)-compound(a))
def normalize(s):
 with tempfile.TemporaryDirectory(prefix='runner-replay-') as directory:
  p=Path(directory)/'shape.step';b.export_step(s,p);result=b.import_step(p)
 assert result.is_valid and len(result.solids())==len(s.solids()) and abs(volume(s)-volume(result))<.1
 return result
def sources():
 p=ROOT/'reference/engine/intake-runner-exterior-review.json'
 return {SOURCE:dict(title='Observed broad runner casting faces and explicitly inferred exterior sections',path='/'+str(p.relative_to(ROOT)),sha256=sha(p),url='https://i.ebayimg.com/images/g/-qoAAOSwDTdlcJqH/s-l1200.jpg')}
@lru_cache(maxsize=1)
def targets():
 proof=json.loads((ROOT/'inventory/engine/intake-runner-exterior-controls-validation.json').read_text());assert proof['status'].startswith('PASS')
 for name in ('baseline.step','runner-exterior.step'):
  p=STUDY/name;assert sha(p)==proof['input_sha256_before'][str(p.relative_to(ROOT))],'Reviewed CAD-release fixture missing/changed'
 baseline=b.import_step(STUDY/'baseline.step');accepted=b.import_step(STUDY/'runner-exterior.step')
 # Rebuild the skins from the durable checked baseline, then compare with the
 # accepted candidate. This fixture is part of the private CAD release, not /tmp.
 target=normalize(candidate.parts(baseline)[0]);error=difference(target,accepted)
 assert error<.1,('Parametric replay differs from accepted CAD',error)
 return baseline,target,error

def export_mesh(shape,path,color):
 vertices,faces=shape.tessellate(.07,.08);xyz=np.array([tuple(v) for v in vertices])[:,[0,2,1]]*np.array([1,1,-1])/1000
 mesh=trimesh.Trimesh(vertices=xyz.astype(np.float32),faces=faces);mesh.update_faces(mesh.area_faces>0);mesh.remove_unreferenced_vertices()
 mesh.visual.vertex_colors=[int(color[i:i+2],16) for i in (1,3,5)]+[255]
 Path(path).write_bytes(trimesh.Scene(mesh).export(file_type='glb'));reopened=trimesh.load(path,force='mesh');reopened.merge_vertices(digits_vertex=8)
 assert reopened.is_watertight and reopened.unique_faces().all() and reopened.nondegenerate_faces().all()
 v=np.asarray(reopened.vertices)[:,[0,2,1]]*np.array([1,-1,1])*1000;box=shape.bounding_box();error=float(np.max(abs(np.array([v.min(0),v.max(0)])-np.array([tuple(box.min),tuple(box.max)]))))
 assert error<.15
 return dict(triangle_count=len(reopened.faces),mesh_bounds_error_mm=error,watertight=True,linear_deflection_mm=.07,angular_deflection_rad=.08)

def install(define,definitions,occurrences,assemblies,shapes,mechanism=None,mesh_dir=None):
 index=next(i for i,d in enumerate(definitions) if d['id']==ID);old=definitions[index]
 occurrence=next(o for o in occurrences if o['id']==ID)
 pose=transforms(dict(definitions=definitions,occurrences=occurrences,assemblies=assemblies,mechanism=mechanism or {}))[ID]
 if occurrence['parent']!='intake-castings' or max(abs(v) for v in (*pose.position,*pose.orientation))>1e-8:raise ValueError('Runner adapter rejects unreviewed local/world frame')
 current=shapes.get(ID)
 if current is None:current=b.import_step(ROOT/old['step'].lstrip('/'))
 baseline,target,replay_error=targets();current=normalize(current)
 # Bounds reject a displaced or scaled local body before costly solid Booleans.
 def bounds(s):q=s.bounding_box();return np.array([tuple(q.min),tuple(q.max)])
 if np.max(abs(bounds(current)-bounds(baseline)))>.01:raise ValueError('Runner adapter rejects unreviewed geometry bounds')
 base_error=difference(current,baseline);target_error=difference(current,target) if base_error>=.1 else None
 if base_error>=.1 and target_error>=.1:raise ValueError('Runner adapter rejects unreviewed geometry')
 definitions.pop(index)
 define(ID,target,old['name'],FUNCTION,old['system'],old['color'],list(dict.fromkeys(old.get('sources',[])+[SOURCE])),list(dict.fromkeys(old.get('unresolved',[])+GAPS)),old.get('dimension_claims',[]),prepared=True)
 row=next(d for d in definitions if d['id']==ID);definitions.remove(row);definitions.insert(index,row)
 row.update(volume_mm3=volume(target),volume_method='adaptive',solid_count=1,model_bounds_mm=list(target.bounding_box().size))
 exported=export_mesh(target,Path(mesh_dir)/(ID+'.glb'),old['color']) if mesh_dir else {}
 if exported:row['triangle_count']=exported['triangle_count']
 occurrence['function']=FUNCTION;shapes[ID]=target
 return dict(changed_definitions=[ID],changed_occurrences=[ID],frame_changes=False,recognized_input='baseline' if base_error<.1 else 'runner-exterior',parametric_replay_difference_mm3=replay_error,**exported)
