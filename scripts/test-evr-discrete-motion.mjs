import assert from 'node:assert/strict';
import fs from 'node:fs/promises';
import {createHash} from 'node:crypto';
const source=await fs.readFile(new URL('../viewer/evr-discrete-motion.js',import.meta.url),'utf8');
const {validateEvrMotionData,createEvrDiscreteMotion}=await import(`data:text/javascript;base64,${Buffer.from(source).toString('base64')}`);
// These are required viewer assets, not optional local CAD intermediates.
const installed=validateEvrMotionData(JSON.parse(await fs.readFile(new URL('../models/engine/evr-motion/poses.json',import.meta.url))));
for(const pose of installed.poses){
  assert.equal(pose.spring_glb,`/models/engine/evr-motion/spring-${pose.index}.glb`);
  const bytes=await fs.readFile(new URL(`..${pose.spring_glb}`,import.meta.url));
  assert.equal(createHash('sha256').update(bytes).digest('hex'),pose.spring_sha256,'Committed spring must match the validated pose');
}
const data={schema_version:1,baseline_travel_mm:.8,poses:[0,.2,.4,.6,.8].map((t,i)=>({index:i,travel_mm:t,spring_glb:`spring-${i}.glb`,spring_sha256:'fixture',disc_offset_cad_mm:[0,0,.8-t],disc_offset_viewer_m:[0,(.8-t)/1000,0]}))};
validateEvrMotionData(data);
for(const mutate of [d=>d.poses.pop(),d=>d.poses[0].disc_offset_cad_mm[0]=1,d=>d.poses[0].disc_offset_viewer_m[1]=NaN,d=>d.poses[2].travel_mm=.3]){const bad=structuredClone(data);mutate(bad);assert.throws(()=>validateEvrMotionData(bad));}
const pending=new Map(),applied=[];let loads=0;
const control=createEvrDiscreteMotion(data,{loadSpring:url=>{loads++;return new Promise(resolve=>pending.set(url,resolve));},applyPose:p=>applied.push(p)});
const first=control.setIndex(0),second=control.setIndex(4);pending.get('spring-4.glb')('open');assert.equal(await second,true);pending.get('spring-0.glb')('seated');assert.equal(await first,false);assert.equal(applied.length,1);assert.equal(control.index,4);
await control.setIndex(0);assert.equal(loads,2);assert.deepEqual(applied.at(-1).discOffsetCadMm,[0,0,.8]);assert.deepEqual(applied.at(-1).discOffsetViewerM,[0,.0008,0]);
await assert.rejects(control.setIndex(.5));await assert.rejects(control.setIndex(5));
const cancelled=control.setIndex(2);control.cancel();pending.get('spring-2.glb')('mid');assert.equal(await cancelled,false);assert.equal(control.index,0);
console.log('PASS: exactly five poses; axes/finite guards; cached absolute offsets; stale/cancelled load suppression.');
const beforeSame=loads;await control.setIndex(0);assert.equal(loads,beforeSame);assert.deepEqual(applied.at(-1).discOffsetViewerM,[0,.0008,0]);
const stale=control.setIndex(1);control.cancel();await control.setIndex(0);pending.get('spring-1.glb')('stale');assert.equal(await stale,false);assert.equal(control.index,0);assert.equal(applied.at(-1).index,0);
let attempts=0;const committed=[];
const retry=createEvrDiscreteMotion(data,{loadSpring:async()=>{if(++attempts===1)throw new Error('fetch failed');return 'retried';},applyPose:p=>committed.push(p)});
await assert.rejects(retry.setIndex(0),/fetch failed/);assert.equal(retry.index,4);assert.equal(committed.length,0);assert.equal(await retry.setIndex(0),true);assert.equal(attempts,2);assert.equal(retry.index,0);assert.equal(committed.length,1);
console.log('PASS: same-index cache; reset defeats late load; failed fetch retains last complete frame and retries.');
