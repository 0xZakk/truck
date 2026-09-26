import assert from 'node:assert/strict';
import {compressorState} from '../viewer/engine-motion.js';

const amplitude=37*Math.tan(18*Math.PI/180);
let checks=0;
for(const engaged of [false,true]){
  for(let cylinder=0;cylinder<5;cylinder++){
    for(let degrees=0;degrees<=720;degrees+=5){
      for(const role of ['pulley','shaft','piston','shoe']){
        const motion={role,cylinder_phase_deg:cylinder*72,stroke_amplitude_mm:amplitude};
        const actual=compressorState(degrees,motion,engaged);
        const phase=(engaged||role==='pulley'?degrees:0)*Math.PI/180;
        const baseline=-amplitude*Math.cos(cylinder*2*Math.PI/5);
        const absolute=-amplitude*Math.cos(cylinder*2*Math.PI/5-phase);
        const translation=['piston','shoe'].includes(role)?absolute-baseline:0;
        assert(Math.abs(actual.translationX-translation)<1e-10);
        assert(Math.abs(actual.rotationX-(role==='piston'?0:phase))<1e-10);
        checks++;
      }
    }
  }
}
assert.throws(()=>compressorState(NaN,{role:'shaft'}),RangeError);
assert.throws(()=>compressorState(0,{role:'invalid'}),RangeError);
assert.throws(()=>compressorState(0,{role:'piston',cylinder_phase_deg:0,stroke_amplitude_mm:-1}),RangeError);
console.log(`Independent compressor phase, rigid piston stroke and clutch-reference behavior: ${checks} cases passed`);
