// Compare browser candidate with independent Python CAD solver, not JS self replay.
import {execFileSync} from 'node:child_process';
import {readFileSync,writeFileSync} from 'node:fs';
import {createHash} from 'node:crypto';
import assert from 'node:assert/strict';
import {clockwiseValveState,clockwiseOccurrencePose,effectiveEvent,clockwiseLayout,clockwiseSlider,clockwiseShaftAngles} from '../viewer/engine-clockwise-motion-candidate.js';
import {sourceValveState} from '../viewer/engine-valve-source.js';
const reference=JSON.parse(execFileSync('.venv-cad/bin/python',['scripts/export-clockwise-motion-reference.py'],{maxBuffer:32*1024*1024,env:{...process.env,XDG_CACHE_HOME:'/tmp/truck-cache'}}));
let maximum=0,closure=0,legacyDifference=0,axialDifference=0;
for(const [q,axial,cylinder,kind,r] of reference.rows){
 const s=clockwiseValveState(q,cylinder,kind,axial);
 const pairs=[[s.lifterLiftMm,r.lifter_lift],[s.valveLiftMm,r.valve_lift],[s.angleRad,r.angle],[s.pivotZ,r.pivot_z],...s.top.map((x,i)=>[x,r.top[i]]),...s.bottom.map((x,i)=>[x,r.bottom[i]])];
 for(const [a,b] of pairs)maximum=Math.max(maximum,Math.abs(a-b));
 closure=Math.max(closure,Math.abs(Math.hypot(s.top[0]-s.bottom[0],s.top[1]-s.bottom[1])-clockwiseLayout.pushrodLength));
 legacyDifference=Math.max(legacyDifference,Math.abs(sourceValveState(q,cylinder,kind).bottom[0]-s.bottom[0]));
 axialDifference=Math.max(axialDifference,Math.abs(clockwiseValveState(q,cylinder,kind,0).lifterLiftMm-s.lifterLiftMm));
 for(const role of ['lifter','valve','rocker','pushrod','spring']){
  const pose=clockwiseOccurrencePose(q,{model:'clockwise-inclined-v1',role,cylinder,kind},axial);
  assert(pose.translationEngineCad.every(Number.isFinite)&&Number.isFinite(pose.rotationXDeltaRad));
  if(role==='spring')assert(pose.springHeightMm>27);
 }
}
let sliderMaximum=0;
for(const [q,p,r,l,x,measured,frames,angle] of reference.sliders){
 const s=clockwiseSlider(q,p,r,l,x,measured);
 for(const [actual,expected] of [[s.rodPositionCad,frames.rod],[s.pistonPositionCad,frames.piston]])for(let i=0;i<3;i++)sliderMaximum=Math.max(sliderMaximum,Math.abs(actual[i]-expected[i]));
 sliderMaximum=Math.max(sliderMaximum,Math.abs(s.rodAngleRad-angle));
 assert(Math.abs(clockwiseShaftAngles(q).crankRad+q*Math.PI/180)<1e-12);
}
let shaftMaximum=0;
for(const [q,x,cam,distributor] of reference.shafts){
 const s=clockwiseShaftAngles(q,x);
 shaftMaximum=Math.max(shaftMaximum,Math.abs(s.camRad-cam*Math.PI/180),Math.abs(s.distributorRad-distributor*Math.PI/180));
}
assert(shaftMaximum<1e-12);
assert(sliderMaximum<1e-9);
assert.throws(()=>clockwiseSlider(0,120,50,180,0,120));
assert(maximum<1e-9);assert(closure<1e-9);assert(legacyDifference>5);assert(axialDifference>.001);
for(const args of [[NaN,0],[0,.1],[0,-.11]])assert.throws(()=>effectiveEvent(...args));
assert.throws(()=>clockwiseOccurrencePose(0,{model:'source-sized-v2'}));
const bindings={...reference.bindings};
for(const p of ['viewer/engine-clockwise-motion-candidate.js','viewer/engine-valve-motion.js','viewer/engine-valve-source.js','scripts/check-clockwise-browser-motion.mjs','scripts/export-clockwise-motion-reference.py'])bindings[p]=createHash('sha256').update(readFileSync(p)).digest('hex');
const report={status:'PASS',scope:'Isolated numerical browser helper versus CAD candidate; not loaded or browser-accepted',rows:reference.rows.length,sliderRows:reference.sliders.length,sliderMaximum,shaftRows:reference.shafts.length,shaftMaximum,maximumNumericDifference:maximum,maximumClosureMm:closure,legacyLowerBallFaultMm:legacyDifference,omittedAxialPhaseFaultMm:axialDifference,bindings,limitations:['No live browser check','No installed manifest/geometry revision','No spring mesh/contact verification','Atlas runtime and installation remain pending']};
writeFileSync('inventory/engine/clockwise-browser-motion-validation.json',JSON.stringify(report,null,2)+'\n');console.log(JSON.stringify(report));
