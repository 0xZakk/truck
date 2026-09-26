import assert from 'node:assert/strict';import fs from 'node:fs';import {performance} from 'node:perf_hooks';
import {sourceSpringMeshData,sourceValveState,sourceLayout} from '../viewer/engine-valve-source.js';
import {createSourceSpringTemplateCache} from '../viewer/engine-valve-source-spring-cache.js';
let maxPositionError=0,maxNormalError=0,meshes=0,cacheStats=[];
for(const [N,R] of [[96,12],[192,16]]){
 const cache=createSourceSpringTemplateCache(32);
 for(let i=0;i<=288;i++){
  const h=27.304596147326+(41.656-27.304596147326)*i/288,a=sourceSpringMeshData(h,N,R),b=cache.get(h,N,R);meshes++;
  assert.equal(a.positions.length,b.positions.length,`length ${h}`);
  for(let j=0;j<a.positions.length;j++){maxPositionError=Math.max(maxPositionError,Math.abs(a.positions[j]-b.positions[j]));maxNormalError=Math.max(maxNormalError,Math.abs(a.normals[j]-b.normals[j]));}
 }
 cacheStats.push({N,R,...cache.stats});
}
assert.ok(maxPositionError<5e-9,`position error ${maxPositionError}`);assert.ok(maxNormalError<1e-6,`normal error ${maxNormalError}`);
// Arbitrary continuous heights, not a rounded angle/height-result cache.
const benchmarks=[];
for(const [N,R] of [[96,12],[192,16]]){
 const cache=createSourceSpringTemplateCache(32),warmStart=performance.now();
 for(let i=0;i<=288;i++)cache.get(27.304596147326+(41.656-27.304596147326)*i/288,N,R);
 const warmMs=performance.now()-warmStart,timings=[];
 for(let frame=0;frame<240;frame++){
  const angle=frame*3.173129;const t=performance.now();
  for(let c=1;c<=6;c++)for(const kind of ['intake','exhaust'])cache.get(sourceLayout.installed[kind]-Math.max(0,sourceValveState(angle,c,kind).valveLiftMm),N,R);
  timings.push(performance.now()-t);
 }
 timings.sort((a,b)=>a-b);benchmarks.push({N,R,warmMs,meanMs:timings.reduce((s,x)=>s+x,0)/timings.length,p50Ms:timings[120],p95Ms:timings[228],maxMs:timings.at(-1),cache:cache.stats});
}
const report={status:'PASS',meshes,maxPositionError,maxNormalError,cacheStats,benchmarks,scope:'Accelerated connectivity templates compared to canonical clipped meshes at289 heights per resolution; benchmark regenerates all12 springs at exact arbitrary crank phases. Node CPU geometry only, excludes THREE/GPU upload.'};fs.writeFileSync('cad/engine/candidates/valve-source-all12/spring-cache-validation.json',JSON.stringify(report,null,2)+'\n');console.log(report);
