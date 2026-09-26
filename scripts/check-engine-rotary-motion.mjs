import assert from 'node:assert/strict';
import {rotaryViewRotation} from '../viewer/engine-motion.js';

for(const axis of ['x','y','z']){
  for(const ratio of [-.5,-.4,1]){
    for(let degrees=0;degrees<=720;degrees+=5){
      const expected=(degrees*ratio+13)*Math.PI/180;
      const actual=rotaryViewRotation(degrees,{axis,ratio,phase_deg:13});
      assert.deepEqual(actual,axis==='x'?[expected,0,0]:axis==='y'?[0,0,-expected]:[0,expected,0]);
    }
  }
}
for(const motion of [{axis:'q',ratio:1},{axis:'z',ratio:NaN},{axis:'x',ratio:Infinity}])assert.throws(()=>rotaryViewRotation(30,motion),RangeError);
console.log('Generic shaft ratios, phase and CAD-to-view axes: 1305 cases passed');
