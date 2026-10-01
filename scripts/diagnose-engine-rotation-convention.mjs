// Read-only numeric proposal: no installed transforms or CAD changes.
import fs from 'node:fs';
import crypto from 'node:crypto';
import {sliderCrank} from '../viewer/engine-motion.js';
import {valveStudy, valveState, camProfilePoint} from '../viewer/engine-valve-motion.js';
const manifest=JSON.parse(fs.readFileSync('inventory/engine/full-assembly.json'));
const {stroke_mm,rod_length_mm:L,cylinder_phases_deg:phases,firing_order:order}=manifest.mechanism;
const R=stroke_mm/2,rad=Math.PI/180;
const max={pistonHeightDifferenceMm:0,rodLengthErrorMm:0,rephasedJournalClosureMm:0,camSupportDifferenceMm:0,camContactReflectionErrorMm:0,camEventLiftErrorMm:0};
const faults={crankOnlySignJournalMismatchMm:0,blanketTimeReverseLiftDifferenceMm:0};
function world(p,a){a*=rad;return {y:p.y*Math.cos(a)-p.z*Math.sin(a),z:p.y*Math.sin(a)+p.z*Math.cos(a)};}
for(let q=0;q<=720;q++){
  for(const phase of phases){
    const old=sliderCrank(q+phase,R,L), next=sliderCrank(-q-phase,R,L);
    const physical=-q-phase;
    const jy=-R*Math.sin(physical*rad),jz=R*Math.cos(physical*rad);
    max.pistonHeightDifferenceMm=Math.max(max.pistonHeightDifferenceMm,Math.abs(old.pistonY-next.pistonY));
    max.rodLengthErrorMm=Math.max(max.rodLengthErrorMm,Math.abs(Math.hypot(next.journalZ,next.pistonY-next.journalY)-L));
    max.rephasedJournalClosureMm=Math.max(max.rephasedJournalClosureMm,Math.hypot(jy+next.journalZ,jz-next.journalY));
    const naive=sliderCrank(-q+phase,R,L);
    faults.crankOnlySignJournalMismatchMm=Math.max(faults.crankOnlySignJournalMismatchMm,Math.hypot(old.journalZ-naive.journalZ,old.journalY-naive.journalY));
  }
  for(const cylinder of order)for(const kind of ['intake','exhaust']){
    const center=(kind==='intake'?468:246)+order.indexOf(cylinder)*120;
    const a=(center-q)/2;
    const old=world(camProfilePoint(a),a),next=world(camProfilePoint(-a),-a);
    max.camSupportDifferenceMm=Math.max(max.camSupportDifferenceMm,Math.abs(old.z-next.z));
    max.camContactReflectionErrorMm=Math.max(max.camContactReflectionErrorMm,Math.abs(old.y+next.y));
    max.camEventLiftErrorMm=Math.max(max.camEventLiftErrorMm,Math.abs(next.z-valveStudy.baseCircleRadiusMm-valveState(q,cylinder,kind).liftMm));
    faults.blanketTimeReverseLiftDifferenceMm=Math.max(faults.blanketTimeReverseLiftDifferenceMm,Math.abs(valveState(q,cylinder,kind).liftMm-valveState(-q,cylinder,kind).liftMm));
  }
}
const firing=order.map((c,i)=>{const q=i*120,phase=phases[c-1];return {cylinder:c,eventDeg:q,proposedTdcErrorMm:Math.abs(sliderCrank(-q-phase,R,L).pistonY-R-L),unrephasedReverseTdcErrorMm:Math.abs(sliderCrank(-q+phase,R,L).pistonY-R-L)};});
const inputs=['viewer/engine-motion.js','viewer/engine-valve-motion.js','viewer/atlas.js','viewer/engine.js','cad/engine/assembly_math.py','cad/engine/full_engine.py','cad/engine/valve_layout_candidate.py','cad/engine/timing_coupled_core_candidate.py','cad/engine/distributor.py','inventory/engine/full-assembly.json','reference/engine/engine-rotation-convention-review.json','scripts/diagnose-engine-rotation-convention.mjs'];
const report={schema_version:1,baseline:'a66b33c',status:Object.values(max).every(v=>v<1e-9)&&firing.every(v=>v.proposedTdcErrorMm<1e-9)&&faults.crankOnlySignJournalMismatchMm>100&&faults.blanketTimeReverseLiftDifferenceMm>6&&firing.some(v=>v.unrephasedReverseTdcErrorMm>70)?'PASS':'FAIL',scope:'Numeric coordinated proposal only; no CAD/export/installed/browser validation.',sampleCoverage:{eventRangeDeg:[0,720],stepDeg:1,poses:721,sliderBranches:6,camBranches:12},maxima:max,negativeControls:faults,firing,distributor:{currentAndProposed:'-q/2 about CAD +Z; clockwise viewed from cap +Z',blanketTimeReverse:'would become counterclockwise; rejected',absoluteTerminalClocking:'unverified'},continuousAlgebra:['cos(-t)=cos(t), sin(-t)=-sin(t): piston height unchanged and journal/rod coordinates reflected for all real q.','Rephased throw -phi and crank -q equal solver -(q+phi) identically.','Current support h is even and derivative odd: rephased oppositely rotating cam preserves height and reflects tangent contact for all q. This is specific to current symmetric profile.'],notRun:['Rebuilt actual crank/cam geometry','Revised helical timing/distributor/pump contact','Whole-engine endplay','Browser and rendered corrected motion'],inputSha256:Object.fromEntries(inputs.map(p=>[p,crypto.createHash('sha256').update(fs.readFileSync(p)).digest('hex')]))};
fs.writeFileSync('inventory/engine/engine-rotation-convention-diagnostic.json',JSON.stringify(report,null,2)+'\n');
console.log(JSON.stringify({status:report.status,maxima:max,negativeControls:faults,firing},null,2));
if(report.status!=='PASS')process.exitCode=1;
