// Exercise the actual viewer request coordinator with deliberately reordered replies.
import assert from 'node:assert/strict';
import {readFile} from 'node:fs/promises';
const source=await readFile(new URL('../viewer/atlas.js',import.meta.url),'utf8');
const coordinator=source.slice(source.indexOf('function requestCablePose('),source.indexOf('function setCablePose('));
function harness(){
 const pending=new Map();let fetches=0;
 const motion={frame:index=>new Promise((resolve,reject)=>pending.set(index,{resolve,reject}))};
 const init=new Function('fetch','createThrottleCableMotion','cableAngle',`
 let data={occurrences:[{throttle_cable:{}}]},cableMotionFailed=false,cableFrame=null,cableRequested=null,cableRequestSerial=0,cableMotionPromise=null,modelRevision='test',throttleAngle=0;
 let poses=0;const errorNode={};const $=()=>errorNode;const pose=()=>poses++;const console={error(){}};
 ${coordinator}
 return {request:requestCablePose,state:()=>({frame:cableFrame?.angle_deg??null,requested:cableRequested,failed:cableMotionFailed,poses,error:errorNode})};`);
 const api=init(async()=>{fetches++;return {ok:true,json:async()=>({})};},()=>motion,x=>x);
 return {...api,pending,fetches:()=>fetches};
}
const flush=async()=>{for(let i=0;i<12;i++)await Promise.resolve();};
const h=harness();h.request(45);h.request(90);await flush();
h.pending.get(90).resolve({angle_deg:90});await flush();h.pending.get(45).resolve({angle_deg:45});await flush();
assert.equal(h.state().frame,90,'Late older response must not replace latest pose');assert.equal(h.fetches(),1);
h.request(30);await flush();h.request(0);h.pending.get(30).resolve({angle_deg:30});await flush();assert.equal(h.state().frame,null,'Reset invalidates in-flight pose');
h.request(45);await flush();h.pending.get(45).resolve({angle_deg:45});await flush();h.request(90);await flush();h.request(45);h.pending.get(90).resolve({angle_deg:90});await flush();
assert.equal(h.state().frame,45,'Returning to displayed pose cancels pending different pose');assert.equal(h.state().requested,null);
const f=harness();f.request(15);await flush();f.pending.get(15).reject(new Error('deliberate load failure'));await flush();f.request(30);await flush();
assert.equal(f.state().failed,true);assert.equal(f.state().frame,null);assert.equal(f.fetches(),1);assert.equal(f.pending.has(30),false);assert.equal(f.state().error.hidden,false);
console.log('Cable request ordering: reverse completion, reset, return-to-current and failure controls pass.');
