import fs from 'node:fs';
import crypto from 'node:crypto';
import assert from 'node:assert/strict';
import {createThrottleCableMotion,cableAngle} from '../viewer/throttle-cable-motion.js';
const root=new URL('../',import.meta.url),read=p=>fs.readFileSync(new URL(p,root)),hash=b=>crypto.createHash('sha256').update(b).digest('hex');
const raw=read('viewer/throttle-cable-motion.json'),data=JSON.parse(raw),cad=JSON.parse(read('inventory/engine/throttle-cable-motion-validation.json')),motion=createThrottleCableMotion(data);
assert.equal(cad.status,'PASS');assert.equal(hash(raw),cad.output_sha256);assert.deepEqual(motion.cachedAngles(),[]);assert.equal(cableAngle(45.49),45);assert.equal(cableAngle(45.5),46);assert.equal(cableAngle(-2),0);assert.equal(cableAngle(95),90);assert.throws(()=>cableAngle(NaN));
const distance=(a,b)=>Math.hypot(...a.map((x,i)=>x-b[i])),apply=(p,d)=>d.rotation_cad_matrix.map((row,i)=>row.reduce((s,x,j)=>s+x*p[j],d.translation_cad_mm[i]));
let maxAnchor=0,maxBounds=0;const rows=[];
for(let angle=0;angle<=90;angle++){
 const frame=await motion.frame(angle);assert.strictEqual(await motion.frame(angle),frame);const source=data.frames[angle];
 const errors=[distance(apply(data.frames[0].ball_center_cad_mm,frame.rigid.socket),frame.ball_center_cad_mm),...['seat','guide'].map(k=>distance(apply(frame.fixed_pivot_cad_mm,frame.rigid[k]),frame.fixed_pivot_cad_mm))];maxAnchor=Math.max(maxAnchor,...errors);assert.ok(Math.max(...errors)<1e-7);
 const row={angle_deg:angle,meshes:{}};
 for(const [kind,mesh] of Object.entries(frame.meshes)){
  assert.equal(hash(mesh.packedBytes),source.meshes[kind].packed_sha256);assert.ok([...mesh.positions,...mesh.normals].every(Number.isFinite));
  const edges=new Map();let volume=0;const lo=[Infinity,Infinity,Infinity],hi=[-Infinity,-Infinity,-Infinity];
  for(let i=0;i<mesh.positions.length;i+=3){const p=[mesh.positions[i]*1000,-mesh.positions[i+2]*1000,mesh.positions[i+1]*1000];for(let j=0;j<3;j++){lo[j]=Math.min(lo[j],p[j]);hi[j]=Math.max(hi[j],p[j]);}}
  for(let i=0;i<mesh.indices.length;i+=3){const t=Array.from(mesh.indices.slice(i,i+3));assert.equal(new Set(t).size,3);for(let j=0;j<3;j++){const a=t[j],b=t[(j+1)%3],key=a<b?`${a},${b}`:`${b},${a}`;const old=edges.get(key)||[0,0];edges.set(key,[old[0]+1,old[1]+(a<b?1:-1)]);}const [a,b,c]=t.map(k=>Array.from(mesh.positions.slice(k*3,k*3+3)));volume+=a[0]*(b[1]*c[2]-b[2]*c[1])+a[1]*(b[2]*c[0]-b[0]*c[2])+a[2]*(b[0]*c[1]-b[1]*c[0]);}
  assert.ok([...edges.values()].every(([count,balance])=>count===2&&balance===0));assert.ok(volume>0);
  const expected=cad.frames[angle].meshes[kind].cad_bounds_mm;const error=Math.max(...[lo,hi].flatMap((p,i)=>p.map((x,j)=>Math.abs(x-expected[i][j]))));assert.ok(error<.2);maxBounds=Math.max(maxBounds,error);
  row.meshes[kind]={vertices:mesh.positions.length/3,triangles:mesh.indices.length/3,closed_oriented_topology:true,bounds_error_mm:error};
 }
 rows.push(row);
}
const fixed=data.frames[0].fixed_pivot_cad_mm,t=Math.PI/4,wrong=[394+(fixed[0]-394)*Math.cos(t)+(fixed[2]-490)*Math.sin(t),fixed[1],490-(fixed[0]-394)*Math.sin(t)+(fixed[2]-490)*Math.cos(t)];assert.ok(distance(wrong,fixed)>1);motion.clear();assert.deepEqual(motion.cachedAngles(),[]);
const report={status:'PASS',scope:'91 exact-CAD-derived mesh poses; integer snapping, no incompatible-topology interpolation. Neighbor CAD sweep remains47 poses. Lazy frame cache validated.',table_sha256:hash(raw),module_sha256:hash(read('viewer/throttle-cable-motion.js')),checker_sha256:hash(fs.readFileSync(new URL(import.meta.url))),table_bytes:raw.length,max_anchor_error_mm:maxAnchor,max_viewer_mesh_bounds_error_mm:maxBounds,wrong_fixed_anchor_negative_error_mm:distance(wrong,fixed),frames:rows};
fs.writeFileSync(new URL('inventory/engine/throttle-cable-viewer-validation.json',root),JSON.stringify(report,null,2)+'\n');console.log(JSON.stringify({...report,frames:rows.length},null,2));
