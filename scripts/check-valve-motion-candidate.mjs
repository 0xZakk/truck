import assert from 'node:assert/strict';
import {readFileSync,writeFileSync,mkdirSync} from 'node:fs';
import {createHash} from 'node:crypto';
import {valveStudy as s,lobeState,valveState,camProfilePoint,rockerState} from '../viewer/engine-valve-motion.js';
const manifestBytes=readFileSync(new URL('../inventory/engine/full-assembly.json',import.meta.url));
const m=JSON.parse(manifestBytes);
const occurrence=id=>m.occurrences.find(o=>o.id===id);
let minCurvature=Infinity,maxContactOffset=0,maxClosureError=0,maxPeriodicError=0;
const profile=[];
for(let deg=-180;deg<180;deg+=.25){
  const p=camProfilePoint(deg);profile.push([p.y,p.z]);minCurvature=Math.min(minCurvature,p.radiusOfCurvatureMm);
  maxContactOffset=Math.max(maxContactOffset,Math.abs(lobeState(deg*2).slopeMmPerCamRad));
}
assert.ok(minCurvature>0,'Flat tappet profile must remain convex');
assert.equal(lobeState(135).liftMm,0);
assert.equal(lobeState(-135).liftMm,0);
assert.ok(Math.abs(lobeState(96).liftMm-1.27)<1e-10);
assert.ok(Math.abs(lobeState(-96).liftMm-1.27)<1e-10);
assert.equal(lobeState(0).liftMm,s.camLiftMm);
let poses=0;
for(let deg=0;deg<=720;deg+=.5)for(let cylinder=1;cylinder<=6;cylinder++)for(const kind of ['intake','exhaust']) {
  const a=valveState(deg,cylinder,kind),b=valveState(deg+720,cylinder,kind);
  maxPeriodicError=Math.max(maxPeriodicError,Math.abs(a.liftMm-b.liftMm));
  const rocker=rockerState(a.liftMm);maxClosureError=Math.max(maxClosureError,Math.abs(rocker.closureErrorMm));poses++;
}
assert.ok(maxPeriodicError<1e-10);assert.ok(maxClosureError<1e-10);
// Physical, independently interpretable events: intake center108° after exchange
// TDC, exhaust center114° before it; each cylinder's .050 window is192° crank.
for(let i=0;i<6;i++) {
  const c=s.firingOrder[i],fire=i*120;
  assert.ok(Math.abs(valveState(fire+468,c,'intake').liftMm-s.camLiftMm)<1e-10);
  assert.ok(Math.abs(valveState(fire+246,c,'exhaust').liftMm-s.camLiftMm)<1e-10);
  for(const [kind,center] of [['intake',468],['exhaust',246]])for(const sign of [-1,1])assert.ok(Math.abs(valveState(fire+center+sign*96,c,kind).liftMm-1.27)<1e-10);
  assert.equal(valveState(fire,c,'intake').liftMm,0);assert.equal(valveState(fire,c,'exhaust').liftMm,0);
}
assert.throws(()=>valveState(NaN,1,'intake'),RangeError);assert.throws(()=>valveState(0,7,'intake'),RangeError);assert.throws(()=>rockerState(-1),RangeError);
const vY=occurrence('c1-intake-valve').position_cad_mm[1];
const rY=occurrence('c1-intake-rocker').position_cad_mm[1];
const pY=occurrence('c1-intake-pushrod').position_cad_mm[1];
const max=rockerState(s.camLiftMm);
const report={status:'PASS isolated teaching candidate; NOT installed-motion clearance',
  manifest_sha256:createHash('sha256').update(manifestBytes).digest('hex'),
  poses,min_profile_curvature_radius_mm:minCurvature,max_flat_tappet_contact_offset_mm:maxContactOffset,
  max_pushrod_closure_error_mm:maxClosureError,max_periodic_error_mm:maxPeriodicError,
  catalog_cam_lift_mm:s.camLiftMm,catalog_valve_lift_mm:s.catalogValveLiftMm,
  solved_valve_lift_mm:max.valveLiftMm,catalog_rounding_difference_mm:max.valveLiftMm-s.catalogValveLiftMm,
  max_valve_pad_slide_mm:max.padSlideMm,
  installed_lateral_lever_ratio:Math.abs((rY-vY)/(pY-rY)),candidate_lever_ratio:s.rockerRatio,
  candidate_pivot_y_mm:max.pivotY,required_pivot_shift_mm:max.pivotY-rY,
  limits:['No production cam curve, acceleration or advertised checking height supplied.270° zero-lift support is an explicit hypothesis.','1.6 ratio and lift are an applicable Melling replacement comparison, not identification of the truck cam.','This solver proves link closure and profile convexity only, not installed STEP clearance, spring coil bind or piston-to-valve clearance.','Existing head pedestal/bolt socket and fulcrum require movement; fixed installed valve/lifter/rocker geometry must not simply be animated with this solver.'],failures:[]};
writeFileSync(new URL('../inventory/engine/valve-motion-candidate-validation.json',import.meta.url),JSON.stringify(report,null,2)+'\n');
const candidateDir=new URL('../cad/engine/candidates/valve-motion/',import.meta.url);
mkdirSync(candidateDir,{recursive:true});
writeFileSync(new URL('profile.json',candidateDir),JSON.stringify({profile,parameters:s,rocker:max},null,2)+'\n');
console.log(JSON.stringify(report,null,2));
