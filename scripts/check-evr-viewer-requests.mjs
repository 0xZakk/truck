// Exercise the real viewer coordinator when a slow/failed request outlives reset.
import assert from 'node:assert/strict';
import {readFile} from 'node:fs/promises';
const source=await readFile(new URL('../viewer/atlas.js',import.meta.url),'utf8');
const body=source.slice(source.indexOf('async function requestEvrPose('),source.indexOf('async function initializeEvrMotion('));
const requests=[],errorNode={hidden:true,textContent:''};
const motion={setIndex:index=>new Promise((resolve,reject)=>requests.push({index,resolve,reject}))};
const init=new Function('evrMotion','errorNode',`
 let evrRequestSerial=0,evrPending=false,poses=0;
 const pose=()=>poses++, $=()=>errorNode, console={error(){}};
 ${body}
 return {request:requestEvrPose,state:()=>({pending:evrPending,poses})};
`);
const app=init(motion,errorNode);
const open=app.request(4),reset=app.request(0);
assert.equal(app.state().pending,true);
requests[1].resolve(true);await reset;
assert.equal(app.state().pending,false);
requests[0].reject(new Error('Older request failed after reset'));await open;
assert.equal(errorNode.hidden,true,'Stale failure must not overwrite reset with an error');
const failed=app.request(2);requests[2].reject(new Error('Current request failed'));await failed;
assert.equal(app.state().pending,false);assert.equal(errorNode.hidden,false);
assert.match(errorNode.textContent,/last complete pose/);
const retry=app.request(2);requests[3].resolve(true);await retry;
assert.equal(app.state().pending,false);
assert.equal(errorNode.hidden,true,'Successful retry clears its previous motion error');
console.log('PASS: actual EVR viewer coordinator preserves reset, ignores stale failures and releases loading state.');
