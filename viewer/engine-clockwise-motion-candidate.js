// Isolated corrected-crank/inclined-linkage candidate; not loaded by atlas.
// Requires coordinated negative lobe phases and corrected rest transforms.
import {valveState} from './engine-valve-motion.js';
export const clockwiseLayout=Object.freeze({pivotY:50.89473678378863,valveY:-12,pushrodY:90,
 lengths:{intake:120.6246,exhaust:120.65},installed:{intake:41.656,exhaust:37.338},
 pushrodLength:250.00335443437204,lowerBallY:95.1098209901611,lowerBallZ:143.78785679212888,padZ:-1.5,padRadius:12,
 cupZ:-1.3856140688197343,maxCamLift:.247*25.4});
export function clockwiseRest(kind){
 const p=clockwiseLayout;if(!(kind in p.lengths))throw new RangeError('Unknown valve kind');
 const tip=261+p.lengths[kind],a=p.pushrodY-p.pivotY,v=p.pivotY-p.valveY;
 let lo=-.02,hi=.02,t,pivotZ,top;
 for(let i=0;i<65;i++){
  t=(lo+hi)/2;pivotZ=tip+v*Math.sin(t)-p.padZ*Math.cos(t)+p.padRadius;
  top=[p.pivotY+a*Math.cos(t)-p.cupZ*Math.sin(t),pivotZ+a*Math.sin(t)+p.cupZ*Math.cos(t)];
  if(Math.hypot(top[0]-p.lowerBallY,top[1]-p.lowerBallZ)<p.pushrodLength)lo=t;else hi=t;
 }
 return {angleRad:t,pivotZ,top,tipZ:tip};
}
export function clockwiseLinkage(lift,kind){
 const p=clockwiseLayout;if(!Number.isFinite(lift)||lift<0||lift>p.maxCamLift+1e-9)throw new RangeError('Invalid cam lift');
 const r=clockwiseRest(kind),a=p.pushrodY-p.pivotY,v=p.pivotY-p.valveY,bottom=[p.lowerBallY,p.lowerBallZ+lift];
 let lo=r.angleRad-.001,hi=r.angleRad+.3,t,top;
 for(let i=0;i<65;i++){
  t=(lo+hi)/2;top=[p.pivotY+a*Math.cos(t)-p.cupZ*Math.sin(t),r.pivotZ+a*Math.sin(t)+p.cupZ*Math.cos(t)];
  if(Math.hypot(top[0]-bottom[0],top[1]-bottom[1])<p.pushrodLength)lo=t;else hi=t;
 }
 return {lifterLiftMm:lift,angleRad:t,pivotZ:r.pivotZ,top,bottom,
 valveLiftMm:r.tipZ-(r.pivotZ-v*Math.sin(t)+p.padZ*Math.cos(t)-p.padRadius),
 padY:p.pivotY-v*Math.cos(t)-p.padZ*Math.sin(t)};
}
export function effectiveEvent(crank, axialMm=0){
 if(!Number.isFinite(crank)||!Number.isFinite(axialMm)||axialMm < -.1||axialMm > 0)throw new RangeError('Finite event and candidate axial range [-0.1,0] required');
 return crank+2*(-Math.tan(25*Math.PI/180)/81.2)*axialMm*180/Math.PI;
}
export function clockwiseValveState(crank,cylinder,kind,axialMm=0){return clockwiseLinkage(valveState(effectiveEvent(crank,axialMm),cylinder,kind).liftMm,kind);}
export function clockwiseOccurrencePose(crank,m,axialMm=0){
 if(m.model!=='clockwise-inclined-v1')throw new RangeError('Clockwise inclined occurrence required');
 const s=clockwiseValveState(crank,m.cylinder,m.kind,axialMm),r=clockwiseLinkage(0,m.kind);
 let translationEngineCad=[0,0,0],rotationXDeltaRad=0;
 if(m.role==='lifter')translationEngineCad=[0,0,s.lifterLiftMm];
 else if(m.role==='valve')translationEngineCad=[0,0,-s.valveLiftMm];
 else if(m.role==='rocker')rotationXDeltaRad=s.angleRad-r.angleRad;
 else if(m.role==='pushrod'){
  translationEngineCad=[0,(s.top[0]+s.bottom[0]-r.top[0]-r.bottom[0])/2,(s.top[1]+s.bottom[1]-r.top[1]-r.bottom[1])/2];
  const a=q=>-Math.atan2(q.top[0]-q.bottom[0],q.top[1]-q.bottom[1]);rotationXDeltaRad=a(s)-a(r);
 }else if(m.role!=='spring')throw new RangeError('Unknown motion role');
 return {translationEngineCad,rotationXDeltaRad,...(m.role==='spring'?{springHeightMm:clockwiseLayout.installed[m.kind]-Math.max(0,s.valveLiftMm)}:{})};
}
// CAD-frame numeric positions/angles; no Three.js axis conversion is hidden here.
export function clockwiseSlider(q,phase,radius,length,stationX,measuredRestPhase){
 if(![q,phase,radius,length,stationX,measuredRestPhase].every(Number.isFinite)||radius<=0||length<=radius)throw new RangeError('Finite slider dimensions and length > radius > 0 required');
 const mismatch=((measuredRestPhase+phase+180)%360+360)%360-180;
 if(Math.abs(mismatch)>1e-7)throw new RangeError('Crank asset requires negative event rest phases');
 const t=(-q-phase)*Math.PI/180,y=-radius*Math.sin(t),z=radius*Math.cos(t);
 return {rodPositionCad:[stationX,y,z],rodAngleRad:Math.asin(y/length),pistonPositionCad:[stationX,0,z+Math.sqrt(length*length-y*y)]};
}
export function clockwiseShaftAngles(q,axialMm=0){
 const event=effectiveEvent(q,axialMm),rad=Math.PI/180;
 return {crankRad:-q*rad,camRad:event*rad/2,distributorRad:-q*rad/2+(1/18+Math.tan(25*rad)/81.2)*axialMm};
}
