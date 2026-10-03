import fs from 'node:fs';
import crypto from 'node:crypto';
import assert from 'node:assert/strict';
import {springCandidateState,springCandidatePoint,springCandidateParameters} from '../viewer/engine-spring-c1-candidate.js';
const path='reference/engine/valve-spring-reconciliation-20261003-browser-fixtures.json';
const f=JSON.parse(fs.readFileSync(path));
const hash=p=>crypto.createHash('sha256').update(fs.readFileSync(p)).digest('hex');
for(const [p,h] of Object.entries(f.inputs))assert.equal(hash(p),h,`Stale fixture: ${p}`);
let maxPointError=0,maxLengthError=0,maxTurnsError=0;
for(const [kind,p] of Object.entries(f.parameters))for(const [key,v] of Object.entries(p))assert.ok(Math.abs(springCandidateParameters[kind][key]-v)<1e-10,`${kind}/${key}`);
for(const row of f.fixtures){
 const s=springCandidateState(row.kind,row.height);
 maxTurnsError=Math.max(maxTurnsError,Math.abs(s.turns-row.turns));
 maxLengthError=Math.max(maxLengthError,Math.abs(s.wireLength-f.parameters[row.kind].wireLength));
 row.u.forEach((u,i)=>{const point=springCandidatePoint(s,Math.min(u,s.turns));point.forEach((v,j)=>{maxPointError=Math.max(maxPointError,Math.abs(v-row.points[i][j]));});});
}
assert.ok(maxPointError<1e-7);assert.ok(maxTurnsError<1e-10);assert.ok(maxLengthError<1e-8);
for(const kind of ['intake','exhaust'])for(const h of [NaN,Infinity,0,springCandidateParameters[kind].solid,springCandidateParameters[kind].free+1])assert.throws(()=>springCandidateState(kind,h));
assert.throws(()=>springCandidateState('unknown',40));
const report={status:'PASS numeric adapter only',fixtures:f.fixtures.length,maxPointErrorMm:maxPointError,maxWireLengthErrorMm:maxLengthError,maxTurnsError,fixtureSha256:hash(path),moduleSha256:hash('viewer/engine-spring-c1-candidate.js'),limits:['No mesh generation or end-cap clipping yet','No installed viewer dispatch','Agreement with inferred contract does not prove factory geometry']};
fs.writeFileSync('reference/engine/valve-spring-reconciliation-20261003-browser-numeric-check.json',JSON.stringify(report,null,2)+'\n');console.log(report);
