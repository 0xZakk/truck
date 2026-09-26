#!/usr/bin/env python3
"""Isolated source-compared rotor leaf: geometry, movement and export checks."""
from pathlib import Path
import json,hashlib,sys,math,itertools,platform,struct,zlib,base64
import numpy as np
import trimesh
import build123d as b
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'cad/engine'))
from assembly_math import transforms
import distributor_center_contact_candidate as c
OUT=ROOT/'cad/engine/generated/distributor-center-contact-study';OUT.mkdir(exist_ok=True)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def vol(s):return sum(x.volume for x in s.solids()) if s else 0.
def hit(a,z):return vol(a.intersect(z))
def bbox_hit(a,z):
 aa=a.bounding_box();zz=z.bounding_box()
 return all(min(getattr(aa.max,k),getattr(zz.max,k))-max(getattr(aa.min,k),getattr(zz.min,k))>1e-6 for k in 'XYZ')
def main():
 mp=ROOT/'inventory/engine/full-assembly.json';m=json.loads(mp.read_text());ds={d['id']:d for d in m['definitions']}
 occ=[o for o in m['occurrences'] if o['parent'] in ('distributor-assembly','distributor-rotation')]
 paths={ROOT/ds[o['definition']]['step'].lstrip('/') for o in occ}
 paths|={mp,Path(__file__),ROOT/'cad/engine/distributor_center_contact_candidate.py',ROOT/'cad/engine/assembly_math.py',ROOT/'reference/engine/distributor-center-contact-review.json'}
 before={str(p.relative_to(ROOT)):sha(p) for p in paths}
 original={o['id']:b.import_step(ROOT/ds[o['definition']]['step'].lstrip('/')) for o in occ}
 parametric=c.baseline_parts()
 for ident,s in parametric.items():assert vol(s-original[ident])+vol(original[ident]-s)<.01,ident
 pieces=c.parts(original['distributor-rotor'],original['distributor-rotor-contact'])
 z=original['distributor-rotor-contact'].bounding_box().min.Z-83
 assert abs(z-50)<1e-6,'Current installed reference changed; review datums'
 leaf=pieces['distributor-rotor-center-leaf'];rotor=pieces['distributor-rotor'];metal=pieces['distributor-rotor-contact'];brush=original['distributor-center-contact']
 checks={}
 for name,a,zshape in [('leaf_to_center',leaf,brush),('leaf_to_conductor',leaf,metal),('leaf_to_insulator',leaf,rotor),('conductor_to_insulator',metal,rotor)]:
  checks[name]={'distance_mm':a.distance_to(zshape),'overlap_mm3':hit(a,zshape)}
  assert checks[name]['distance_mm']<1e-5 and checks[name]['overlap_mm3']<.1,(name,checks[name])
 protected={}
 for name,key,region in [('shaft_seat','distributor-rotor',b.Pos(0,0,119)*b.Box(50,50,22)),('outer_tip','distributor-rotor-contact',b.Pos(30,0,134)*b.Box(6,20,8))]:
  a=pieces[key]&region;old=original[key]&region;v=vol(a-old)+vol(old-a);protected[name]=v;assert v<.1
 # New geometry remains wholly inside the unchanged insulating cap envelope.
 interior=b.Pos(0,0,120)*b.Cylinder(39,46)
 for key,s in pieces.items():assert vol(s-interior)<.1,key
 # Nominal axial capture: leaf foot is below conductor, stake head is above.
 capture={'leaf_lift_0_2_into_conductor_mm3':hit(b.Pos(0,0,.2)*leaf,metal),'conductor_lift_0_2_into_stake_mm3':hit(b.Pos(0,0,.2)*metal,rotor)}
 assert min(capture.values())>.1
 bad={'leaf_lowered_0_5_center_gap_mm':(b.Pos(0,0,-.5)*leaf).distance_to(brush),'leaf_raised_0_5_center_overlap_mm3':hit(b.Pos(0,0,.5)*leaf,brush)}
 assert bad['leaf_lowered_0_5_center_gap_mm']>.49 and bad['leaf_raised_0_5_center_overlap_mm3']>.1
 allparts=original|pieces;fail=[];count=0;distance=[]
 for crank in range(0,721,20):
  poses=transforms(m,crank);poses['distributor-rotor-center-leaf']=poses['distributor-rotor-contact']
  # Check relative native geometry. All distributor actors share the same rigid
  # leaned root frame; relative rotation is clockwise at half crank speed.
  ref=poses['distributor-cap'].inverse()
  placed={k:ref*poses[k]*s for k,s in allparts.items()}
  distance.append(placed['distributor-rotor-center-leaf'].distance_to(placed['distributor-center-contact']))
  for a,zid in itertools.combinations(placed,2):
   if not ({a,zid}&pieces.keys()) or not bbox_hit(placed[a],placed[zid]):continue
   count+=1;v=hit(placed[a],placed[zid])
   if v>.1:fail.append({'crank_deg':crank,'a':a,'b':zid,'overlap_mm3':v})
 assert max(distance)<1e-5
 # Axial cap withdrawal keeps attached brush/terminals together; no tilt assumed.
 removal=[]
 for lift in (0,.1,.5,1,2,5,10,20,40,80):
  for cap_id in ['distributor-cap','distributor-center-contact','distributor-coil-terminal']+[f'distributor-terminal-{i}' for i in range(1,7)]:
   for k,s in pieces.items():
    v=hit(b.Pos(0,0,lift)*original[cap_id],s)
    if v>.1:removal.append({'lift_mm':lift,'a':cap_id,'b':k,'overlap_mm3':v})
 exports=[];render=[]
 for k,s in pieces.items():
  assert s.is_valid and len(s.solids())==1
  sp=OUT/(k+'.step');b.export_step(s,sp);rt=b.import_step(sp);assert rt.is_valid and abs(vol(rt)-vol(s))<.01
  vertices,faces=rt.tessellate(.025,.1);v=np.array([tuple(p) for p in vertices]);mesh=trimesh.Trimesh(vertices=v[:,[0,2,1]]*np.array([1,1,-1])/1000,faces=faces)
  gp=OUT/(k+'.glb');gp.write_bytes(trimesh.Scene(mesh).export(file_type='glb'));gm=trimesh.load(gp,force='mesh');gm.merge_vertices(digits_vertex=8)
  error=float(np.max(abs(gm.bounds-mesh.bounds))*1000);assert gm.is_watertight and error<.01
  exports.append({'id':k,'valid':True,'solid_count':1,'step_sha256':sha(sp),'glb_sha256':sha(gp),'watertight':True,'bounds_error_mm':error})
  render.append((k,gm))
 # Actual exported-mesh triangle render in two useful views, not a concept image.
 svg=['<svg xmlns="http://www.w3.org/2000/svg" width="1300" height="680"><rect width="100%" height="100%" fill="#f5f7f8"/>']
 colors={'distributor-rotor':(157,169,177),'distributor-rotor-contact':(194,163,89),'distributor-rotor-center-leaf':(205,211,216)}
 pixels=np.full((680,1300,3),(245,247,248),dtype=np.uint8);depths=np.full((680,1300),-np.inf)
 for panel,view in enumerate([np.array([.5,-.8,.8]),np.array([0,-1,.13])]):
  view=view/np.linalg.norm(view);right=np.cross([0,0,1],view);right/=np.linalg.norm(right);up=np.cross(view,right);tris=[]
  for k,mesh in render:
   if panel==1 and k=='distributor-rotor':continue
   v=np.asarray(mesh.vertices);v=np.column_stack((v[:,0],-v[:,2],v[:,1]))*1000
   for t in v[mesh.faces]:
    norm=np.cross(t[1]-t[0],t[2]-t[0]);norm/=max(np.linalg.norm(norm),1e-12)
    if norm@view<0:continue
    q=t-np.array([12,0,130]);uv=np.column_stack((q@right,-q@up))*11+[330+panel*640,340]
    shade=.5+.5*max(norm@np.array([.2,-.4,.89]),0);color=tuple(int(x*shade) for x in colors[k]);tris.append((q@view,uv,color))
  for dep,uv,color in tris:
   xmin=max(0,int(uv[:,0].min()));xmax=min(1299,int(uv[:,0].max())+1);ymin=max(0,int(uv[:,1].min()));ymax=min(679,int(uv[:,1].max())+1)
   if xmin<=xmax and ymin<=ymax:
    xx,yy=np.meshgrid(np.arange(xmin,xmax+1)+.5,np.arange(ymin,ymax+1)+.5)
    (x0,y0),(x1,y1),(x2,y2)=uv;den=(y1-y2)*(x0-x2)+(x2-x1)*(y0-y2)
    if abs(den)>1e-10:
     w0=((y1-y2)*(xx-x2)+(x2-x1)*(yy-y2))/den;w1=((y2-y0)*(xx-x2)+(x0-x2)*(yy-y2))/den
     dz=w0*dep[0]+w1*dep[1]+(1-w0-w1)*dep[2];target=depths[ymin:ymax+1,xmin:xmax+1];mask=(w0>=0)&(w1>=0)&(w0+w1<=1)&(dz>target)
     target[mask]=dz[mask];pixels[ymin:ymax+1,xmin:xmax+1][mask]=color
   svg.append('<polygon points="'+' '.join(f'{x:.2f},{y:.2f}' for x,y in uv)+'" fill="rgb'+str(color)+'"/>')
 svg+=['<text x="25" y="35" font-size="23" font-family="sans-serif">Actual GLB: source-compared rotor leaf candidate</text>','<text x="25" y="620" font-size="18" font-family="sans-serif">Left: assembled rotor. Right: leaf and conductor isolated. Bend dimensions, stake and preload are inferred.</text>','<text x="25" y="650" font-size="18" font-family="sans-serif">Cap center-contact envelope unchanged; hidden brush attachment and preload remain unresolved.</text>','</svg>'];(OUT/'rotor-contact-render.svg').write_text('\n'.join(svg))
 def chunk(name,data):return struct.pack('!I',len(data))+name+data+struct.pack('!I',zlib.crc32(name+data)&0xffffffff)
 png=b'\x89PNG\r\n\x1a\n'+chunk(b'IHDR',struct.pack('!2I5B',1300,680,8,2,0,0,0))+chunk(b'IDAT',zlib.compress(b''.join(b'\x00'+row.tobytes() for row in pixels)))+chunk(b'IEND',b'')
 (OUT/'rotor-contact-render.png').write_bytes(png)
 svg=[line for line in svg if not line.startswith('<polygon')]
 svg.insert(1,'<image width="1300" height="680" href="data:image/png;base64,'+base64.b64encode(png).decode()+'"/>')
 (OUT/'rotor-contact-render.svg').write_text('\n'.join(svg))
 after={str(p.relative_to(ROOT)):sha(p) for p in paths};assert before==after,'Input mutation'
 report={'status':'PASS bounded rotor leaf study' if not fail and not removal else 'FAIL','input_sha256_before':before,'input_sha256_after':after,'input_guard_pass':True,'native_z_shift_mm':z,'contacts':checks,'protected_regions_difference_mm3':protected,'capture_negative_controls':capture,'center_negative_controls':bad,'motion':{'crank_samples':list(range(0,721,20)),'exact_pairs':count,'maximum_center_gap_mm':max(distance),'failures':fail,'scope':'Relative local-frame rigid rotor motion through full cycle; no spring deflection or electrical analysis.'},'cap_removal_failures':removal,'exports':exports,'render':'cad/engine/generated/distributor-center-contact-study/rotor-contact-render.svg','limits':['All geometry dimensions inferred; source photo establishes topology only.','Existing cap center envelope retained; actual brush material, retention and hidden connection unverified.','Idealized molded stake retention, no manufacturing process or interference/preload claim.','Outer tip and shaft seating preserve existing estimates; electrical gap not factory verified.','Browser and integrated full-neighbor check NOT RUN.'],'environment':{'python':platform.python_version(),'build123d':b.__version__}}
 (ROOT/'inventory/engine/distributor-center-contact-candidate-validation.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({k:report[k] for k in ('status','contacts','protected_regions_difference_mm3','capture_negative_controls','center_negative_controls','motion','cap_removal_failures')},indent=2));assert not fail and not removal
if __name__=='__main__':main()
