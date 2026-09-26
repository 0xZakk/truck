import assert from 'node:assert/strict';
import fs from 'node:fs';
import {sourceValveState,sourceOccurrencePose,sourceSpringMeshData} from '../viewer/engine-valve-source.js';
const out='cad/engine/candidates/valve-source-all12';
const fixtures=JSON.parse(fs.readFileSync(out+'/motion-api-fixtures.json'));
let comparisons=0,maxError=0;
function near(a,b,tol=1e-9){const e=Math.abs(a-b);maxError=Math.max(maxError,e);assert.ok(e<tol,`${a} != ${b}`);comparisons++;}
for(const f of fixtures){
 const a=sourceValveState(f.crank_deg,f.cylinder,f.kind),b=f.state;
 near(a.lifterLiftMm,b.lifter_lift);near(a.valveLiftMm,b.valve_lift);near(a.angleRad,b.angle);near(a.padY,b.pad_y);near(a.pivotZ,b.pivot_z);
 for(let i=0;i<2;i++){near(a.top[i],b.top[i]);near(a.bottom[i],b.bottom[i]);}
 for(const fpose of f.poses){
  const p=sourceOccurrencePose(f.crank_deg,fpose.metadata),angle=fpose.rest_angle+p.rotationXDeltaRad;
  for(const [i,q] of [[0,0,0],[1,0,0],[0,1,0],[0,0,1]].entries()){
   const rotated=[q[0],q[1]*Math.cos(angle)-q[2]*Math.sin(angle),q[1]*Math.sin(angle)+q[2]*Math.cos(angle)];
   rotated.forEach((x,j)=>near(x+[10,20,30][j]+p.translationEngineCad[j],fpose.points[i][j]));
  }
 }
 for(const role of ['lifter','valve','rocker','pushrod','spring']){
  const m={role,cylinder:f.cylinder,kind:f.kind,model:'source-sized-v2'};
  const p=sourceOccurrencePose(f.crank_deg,m),q=sourceOccurrencePose(f.crank_deg+720,m);
  p.translationEngineCad.forEach((x,i)=>near(x,q.translationEngineCad[i]));near(p.rotationXDeltaRad,q.rotationXDeltaRad);
 }
}
let triangles=0,minWinding=Infinity,maxBoundError=0,volumes=[];
for(const h of [41.656,37.338,31.623,27.304596147326]){
 const m=sourceSpringMeshData(h),edges=new Map();let volume=0,minY=Infinity,maxY=-Infinity;
 assert.equal(m.groundCaps,2);
 const key=p=>p.map(x=>Math.round(x*1e9)).join(',');
 for(let k=0;k<m.positions.length;k+=9){
  const p=[0,3,6].map(i=>Array.from(m.positions.slice(k+i,k+i+3))),u=p[1].map((x,i)=>x-p[0][i]),v=p[2].map((x,i)=>x-p[0][i]);
  const cross=[u[1]*v[2]-u[2]*v[1],u[2]*v[0]-u[0]*v[2],u[0]*v[1]-u[1]*v[0]],dot=cross.reduce((s,x,i)=>s+x*m.normals[k+i],0);
  minWinding=Math.min(minWinding,dot);assert.ok(dot>0,`inward or degenerate triangle ${k/9}: ${dot}`);triangles++;
  const bc=[p[1][1]*p[2][2]-p[1][2]*p[2][1],p[1][2]*p[2][0]-p[1][0]*p[2][2],p[1][0]*p[2][1]-p[1][1]*p[2][0]];
  volume+=p[0].reduce((s,x,i)=>s+x*bc[i],0)/6;
  for(let i=0;i<3;i++){minY=Math.min(minY,p[i][1]);maxY=Math.max(maxY,p[i][1]);const a=key(p[i]),b=key(p[(i+1)%3]),ek=[a,b].sort().join('|');assert.notEqual(a,b);const e=edges.get(ek)||{count:0,winding:0};e.count++;e.winding+=a<b?1:-1;edges.set(ek,e);}
 }
 for(const [key,e] of edges){assert.equal(e.count,2,`non-manifold edge ${key}`);assert.equal(e.winding,0,`same-directed edge ${key}`);}
 assert.ok(volume>0);volumes.push(volume*1e9);maxBoundError=Math.max(maxBoundError,Math.abs(minY),Math.abs(maxY-h/1000));assert.ok(maxBoundError<5e-9);
}
const result={status:'PASS',fixtures:fixtures.length,comparisons,maxError,triangles,minWinding,maxBoundError,volumesMm3:volumes,scope:'CAD/JS linkage equivalence and closed ground-ended display spring topology; sampled all12 CAD audit is separate.'};
fs.writeFileSync(out+'/motion-api-validation.json',JSON.stringify(result,null,2)+'\n');console.log(result);
