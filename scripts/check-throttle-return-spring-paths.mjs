import fs from 'node:fs';
import crypto from 'node:crypto';
import assert from 'node:assert/strict';
import {buildThrottleSpringMesh} from '../viewer/throttle-return-spring-mesh.js';
const path=new URL('../viewer/throttle-return-spring-paths.json',import.meta.url),raw=fs.readFileSync(path),data=JSON.parse(raw);
assert.equal(data.frames.length,91);assert.ok(data.samples_per_frame>=401);
const distance=(a,b)=>Math.hypot(...a.map((x,i)=>x-b[i]));
const fixed=data.frames[0].points_cad_mm[0],moving=data.frames[0].points_cad_mm.at(-1),rows=[];
let worstLength=0,worstAnchor=0,minimumNonlocal=Infinity;
for(const frame of data.frames) {
  const angle=frame.angle_deg,theta=angle*Math.PI/180,p=frame.points_cad_mm;
  assert.equal(p.length,data.samples_per_frame);assert.ok(p.flat().every(Number.isFinite));
  const expected=[394+(moving[0]-394)*Math.cos(theta)+(moving[2]-490)*Math.sin(theta),moving[1],490-(moving[0]-394)*Math.sin(theta)+(moving[2]-490)*Math.cos(theta)];
  const anchorError=Math.max(distance(p[0],fixed),distance(p.at(-1),expected));assert.ok(anchorError<1e-4);
  let length=0;for(let i=1;i<p.length;i++)length+=distance(p[i-1],p[i]);
  worstLength=Math.max(worstLength,Math.abs(length-frame.cad_length_mm));worstAnchor=Math.max(worstAnchor,anchorError);
  assert.ok(Math.abs(length-frame.cad_length_mm)<.05);assert.ok(frame.coil_turn_surface_gap_mm>0);
  // Nonlocal sampled self-spacing sanity. Skip four0.5 mm steps because
  // neighboring cross-sections of a bent tube are locally connected.
  let gap=Infinity;for(let i=0;i<p.length;i+=4)for(let j=i+20;j<p.length;j+=4)gap=Math.min(gap,distance(p[i],p[j]));
  assert.ok(gap>2*data.wire_radius_mm,`Nonlocal self approach at${angle}`);minimumNonlocal=Math.min(minimumNonlocal,gap);
  if([0,45,90].includes(angle)) {
    const mesh=buildThrottleSpringMesh(frame,data.wire_radius_mm);assert.ok([...mesh.positions,...mesh.normals].every(Number.isFinite));
    const edges=new Map();
    for(let i=0;i<mesh.indices.length;i+=3) { const tri=Array.from(mesh.indices.slice(i,i+3));assert.equal(new Set(tri).size,3);for(let j=0;j<3;j++){const a=tri[j],b=tri[(j+1)%3],key=a<b?`${a},${b}`:`${b},${a}`;const old=edges.get(key)||[0,0];edges.set(key,[old[0]+1,old[1]+(a<b?1:-1)]);} }
    assert.ok([...edges.values()].every(([count,balance])=>count===2&&balance===0));
    rows.push({angle_deg:angle,vertices:mesh.positions.length/3,triangles:mesh.indices.length/3,closed_oriented_topology:true});
  }
}
const angle=Math.PI/4,wrong=[394+(fixed[0]-394)*Math.cos(angle)+(fixed[2]-490)*Math.sin(angle),fixed[1],490-(fixed[0]-394)*Math.sin(angle)+(fixed[2]-490)*Math.cos(angle)];
assert.ok(distance(wrong,fixed)>.05);
const report={checker_sha256:crypto.createHash('sha256').update(fs.readFileSync(new URL(import.meta.url))).digest('hex'),status:'PASS',scope:'Exact-CAD-derived91 integer paths and pure tube mesh; sampled self-spacing sanity, not CAD continuous collision or physical spring validation.',table_sha256:crypto.createHash('sha256').update(raw).digest('hex'),module_sha256:crypto.createHash('sha256').update(fs.readFileSync(new URL('../viewer/throttle-return-spring-mesh.js',import.meta.url))).digest('hex'),samples_per_pose:data.samples_per_frame,max_polyline_length_loss_mm:worstLength,max_endpoint_error_mm:worstAnchor,min_sampled_nonlocal_centerline_distance_mm:minimumNonlocal,wrong_fixed_anchor_negative_error_mm:distance(wrong,fixed),meshes:rows};
fs.writeFileSync(new URL('../inventory/engine/throttle-return-spring-path-validation.json',import.meta.url),JSON.stringify(report,null,2)+'\n');console.log(JSON.stringify(report,null,2));
