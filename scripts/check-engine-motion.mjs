import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {sliderCrank} from '../viewer/engine-motion.js';

const manifest=JSON.parse(readFileSync(new URL('../inventory/engine/first-assembly.json',import.meta.url)));
const {stroke_mm:stroke,rod_length_mm:L}=manifest.mechanism;
const R=stroke/2;
let maxClosureError=0, maxLengthError=0, min=Infinity,max=-Infinity;
for(let angle=0;angle<=360;angle+=0.25){
  const s=sliderCrank(angle,R,L);
  const endY=s.journalY+Math.cos(s.rodAngle)*L;
  const endZ=s.journalZ+Math.sin(s.rodAngle)*L;
  maxClosureError=Math.max(maxClosureError,Math.abs(endY-s.pistonY),Math.abs(endZ));
  maxLengthError=Math.max(maxLengthError,Math.abs(Math.hypot(s.pistonY-s.journalY,s.journalZ)-L));
  min=Math.min(min,s.pistonY);max=Math.max(max,s.pistonY);
}
assert.ok(maxClosureError<1e-9);
assert.ok(maxLengthError<1e-9);
assert.ok(Math.abs(max-min-stroke)<1e-9);
assert.throws(()=>sliderCrank(0,R,R),RangeError);
assert.throws(()=>sliderCrank(NaN,R,L),RangeError);
const partIds=manifest.occurrences.map(o=>o.id);
assert.equal(new Set(partIds).size,partIds.length);
assert.equal(manifest.occurrences.filter(o=>o.definition==='compression-ring').length,2);
assert.equal(manifest.occurrences.filter(o=>o.definition==='oil-rail').length,2);
assert.ok(manifest.occurrences.every(o=>manifest.definitions.some(d=>d.id===o.definition)));
console.log(JSON.stringify({poses:1441,stroke_mm:max-min,maxClosureError,maxLengthError,occurrences:partIds.length},null,2));
