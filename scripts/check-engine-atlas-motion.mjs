import assert from 'node:assert/strict';
import {readFile} from 'node:fs/promises';
import {sliderCrank} from '../viewer/engine-motion.js';
const m=JSON.parse(await readFile(new URL('../inventory/engine/full-assembly.json',import.meta.url)));
const R=m.mechanism.stroke_mm/2,L=m.mechanism.rod_length_mm;
const phases=m.mechanism.cylinder_phases_deg;
let maxError=0;
for(let angle=0;angle<=720;angle+=.5){
  const states=phases.map(p=>sliderCrank(angle+p,R,L));
  for(const s of states){
    const length=Math.hypot(s.pistonY-s.journalY,s.journalZ);
    maxError=Math.max(maxError,Math.abs(length-L));
    assert(Math.abs(length-L)<1e-8);
    assert(s.pistonY>=L-R-1e-8 && s.pistonY<=L+R+1e-8);
  }
  for(const [a,b] of [[0,5],[1,4],[2,3]])assert(Math.abs(states[a].pistonY-states[b].pistonY)<1e-8);
}
for(const [index,cylinder] of m.mechanism.firing_order.entries()){
  const state=sliderCrank(index*120+phases[cylinder-1],R,L);
  assert(Math.abs(state.pistonY-(R+L))<1e-8,`Cylinder ${cylinder} must be at TDC at its declared firing event`);
}
console.log(JSON.stringify({cylinders:6,cycle_degrees:720,samples:1441,maxRodClosureError_mm:maxError,firing_order:m.mechanism.firing_order,scope:'Idealized zero-offset rotating mechanism; no combustion or valve-event simulation'},null,2));
