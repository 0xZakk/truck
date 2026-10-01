import assert from 'node:assert/strict';
import fs from 'node:fs';
import {clockwiseLinkage,clockwiseLayout} from '../viewer/engine-clockwise-motion-candidate.js';
import {createHash} from 'node:crypto';
import {sourceSpringMeshData} from '../viewer/engine-valve-source.js';
let triangles=0,meshes=0,maxBoundsError=0,minWinding=Infinity;
const heights=['intake','exhaust'].flatMap(kind=>[0,.247*25.4/2,.247*25.4].map(lift=>clockwiseLayout.installed[kind]-clockwiseLinkage(lift,kind).valveLiftMm));
for(const [N,R] of [[96,12],[192,16]])for(const h of heights){
 const m=sourceSpringMeshData(h,N,R),edges=new Map();meshes++;
 const key=p=>p.map(x=>Math.round(x*1e9)).join(',');
 for(let j=0;j<m.positions.length;j+=9){
  const p=[0,3,6].map(k=>Array.from(m.positions.slice(j+k,j+k+3))),u=p[1].map((x,k)=>x-p[0][k]),v=p[2].map((x,k)=>x-p[0][k]);
  const cross=[u[1]*v[2]-u[2]*v[1],u[2]*v[0]-u[0]*v[2],u[0]*v[1]-u[1]*v[0]],dot=cross.reduce((s,x,k)=>s+x*m.normals[j+k],0);minWinding=Math.min(dot,minWinding);assert.ok(dot>0,`winding h${h} tri${j/9}`);triangles++;
  for(let k=0;k<3;k++){
   maxBoundsError=Math.max(maxBoundsError,-p[k][1],p[k][1]-h/1000);const a=key(p[k]),b=key(p[(k+1)%3]);assert.notEqual(a,b);const ek=[a,b].sort().join('|'),row=edges.get(ek)||{count:0,direction:0};row.count++;row.direction+=a<b?1:-1;edges.set(ek,row);
  }
 }
 assert.equal(m.groundCaps,2);for(const e of edges.values()){assert.equal(e.count,2);assert.equal(e.direction,0);}
}
assert.ok(maxBoundsError<5e-9);const report={status:'PASS',meshes,triangles,minWinding,maxBoundsError,heights,scope:'Actual corrected-linkage rest/half/peak compression at both display resolutions. Mesh topology/winding/ground bounds only; no collision or continuous proof.',bindings:Object.fromEntries(['viewer/engine-valve-source.js','viewer/engine-clockwise-motion-candidate.js','scripts/check-clockwise-spring-mesh.mjs'].map(p=>[p,createHash('sha256').update(fs.readFileSync(p)).digest('hex')]))};
fs.writeFileSync('inventory/engine/clockwise-spring-mesh-validation.json',JSON.stringify(report,null,2)+'\n');console.log(report);
