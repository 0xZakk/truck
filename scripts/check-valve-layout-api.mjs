import assert from 'node:assert/strict';
import fs from 'node:fs';
import {valveLayoutState,occurrenceValvePose,springMeshData} from '../viewer/engine-valve-layout.js';
const fixtures=JSON.parse(fs.readFileSync('cad/engine/candidates/valve-layout/motion-api-fixtures.json'));
let comparisons=0,maxError=0;
function near(a,b,tol=1e-9){const e=Math.abs(a-b);maxError=Math.max(maxError,e);assert.ok(e<tol,`${a} != ${b}`);comparisons++;}
for(const f of fixtures){
 const a=valveLayoutState(f.crank_deg,f.cylinder,f.kind),b=f.state;
 near(a.lifterLiftMm,b.lifter_lift);near(a.valveLiftMm,b.valve_lift);near(a.angleRad,b.angle);
 for(let i=0;i<2;i++){near(a.top[i],b.top[i]);near(a.bottom[i],b.bottom[i]);}
 for(const role of ['lifter','valve','rocker','pushrod','spring']){
  const m={role,cylinder:f.cylinder,kind:f.kind};
  const p=occurrenceValvePose(f.crank_deg,m),q=occurrenceValvePose(f.crank_deg+720,m);
  p.translationCad.forEach((x,i)=>near(x,q.translationCad[i]));near(p.rotationXRad,q.rotationXRad);
 }
}
let triangles=0,minWinding=Infinity,maxWireError=0;
for(const h of [51,46,40.967]){
 const m=springMeshData(h),N=192,R=16,stride=R+1;
 for(let i=0;i<=N;i++)for(let j=0;j<=R;j++){
  const k=(i*stride+j)*3,t=12*Math.PI*i/N,c=[13*Math.cos(t)/1000,h*i/N/1000,-13*Math.sin(t)/1000];
  const radius=Math.hypot(...c.map((v,a)=>m.positions[k+a]-v));maxWireError=Math.max(maxWireError,Math.abs(radius-.002));assert.ok(Math.abs(radius-.002)<5e-9);
  assert.ok(Math.abs(Math.hypot(...m.normals.slice(k,k+3))-1)<1e-6);
 }
 for(let k=0;k<m.indices.length;k+=3){
  const [ia,ib,ic]=Array.from(m.indices.slice(k,k+3),x=>x*3),u=[0,1,2].map(i=>m.positions[ib+i]-m.positions[ia+i]),v=[0,1,2].map(i=>m.positions[ic+i]-m.positions[ia+i]);
  const cross=[u[1]*v[2]-u[2]*v[1],u[2]*v[0]-u[0]*v[2],u[0]*v[1]-u[1]*v[0]],dot=cross.reduce((s,x,i)=>s+x*m.normals[ia+i],0);
  minWinding=Math.min(minWinding,dot);assert.ok(dot>0,`inward triangle ${k/3}: ${dot}`);triangles++;
 }
}
const result={status:'PASS',fixtures:fixtures.length,comparisons,maxError,triangles,minWinding,maxWireError,limits:'API equivalence and constant-wire mesh only; not all12 installed CAD clearance or positive spring seating.'};
fs.writeFileSync('cad/engine/candidates/valve-layout/motion-api-validation.json',JSON.stringify(result,null,2)+'\n');console.log(result);
