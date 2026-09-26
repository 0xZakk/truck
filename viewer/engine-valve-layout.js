// Coordinated installed-coordinate candidate API. Must only be wired to regenerated
// all12-station geometry after root's whole-engine QC. See VALVETRAIN-CANDIDATE.md.
import {valveState} from './engine-valve-motion.js';
export const valveLayout=Object.freeze({pivotY:51.62143599494969,pivotZ:383.5,valveY:-12,
 pushrodY:90,pushrodLength:226.6,lowerCupRestZ:140.9,pushrodRestCenterZ:254.2,
 cupOffsetZ:-16,padCenterZ:-1.5,maxCamLift:.247*25.4,maxValveLift:.395*25.4});
export function layoutRockerState(lift){
 if(!Number.isFinite(lift)||lift<0||lift>valveLayout.maxCamLift+1e-9)throw new RangeError('Lift outside candidate range');
 const p=valveLayout,a=p.pushrodY-p.pivotY,v=p.pivotY-p.valveY,L=p.pushrodLength;
 let low=0,high=.3;
 for(let i=0;i<60;i++){
  const t=(low+high)/2,dy=a*(Math.cos(t)-1)-p.cupOffsetZ*Math.sin(t);
  const lowerLift=a*Math.sin(t)-p.cupOffsetZ*(1-Math.cos(t))+L-Math.sqrt(L*L-dy*dy);
  if(lowerLift<lift)low=t;else high=t;
 }
 const angle=(low+high)/2,top=[p.pivotY+a*Math.cos(angle)-p.cupOffsetZ*Math.sin(angle),p.pivotZ+a*Math.sin(angle)+p.cupOffsetZ*Math.cos(angle)];
 const bottom=[p.pushrodY,p.lowerCupRestZ+lift];
 return {angleRad:angle,lifterLiftMm:lift,valveLiftMm:v*Math.sin(angle)-p.padCenterZ*(Math.cos(angle)-1),
   top,bottom,pushrodRotationXRad:-Math.atan2(top[0]-bottom[0],top[1]-bottom[1]),
   pushrodDeltaCad:[0,(top[0]+bottom[0])/2-p.pushrodY,(top[1]+bottom[1])/2-p.pushrodRestCenterZ]};
}
export function valveLayoutState(crankDeg,cylinder,kind){return layoutRockerState(valveState(crankDeg,cylinder,kind).liftMm);}
export function occurrenceValvePose(crankDeg,metadata){
 const s=valveLayoutState(crankDeg,metadata.cylinder,metadata.kind);
 switch(metadata.role){
 case 'lifter':return {translationCad:[0,0,s.lifterLiftMm],rotationXRad:0};
 case 'valve':return {translationCad:[0,0,-s.valveLiftMm],rotationXRad:0};
 case 'rocker':return {translationCad:[0,0,0],rotationXRad:s.angleRad};
 case 'pushrod':return {translationCad:s.pushrodDeltaCad,rotationXRad:s.pushrodRotationXRad};
 case 'spring':return {translationCad:[0,0,0],rotationXRad:0,springHeightMm:51-s.valveLiftMm};
 default:throw new RangeError('Unknown valvetrain role');
 }
}
// Solid circular-wire helix with end caps, in GLB metres and Y-up display axes.
// Vertex topology stays fixed as pitch changes. No spring-axis scaling is used.
export function springMeshData(heightMm,tubularSegments=192,radialSegments=16){
 if(!Number.isFinite(heightMm)||heightMm<51-valveLayout.maxValveLift-1e-8||heightMm>51||!Number.isInteger(tubularSegments)||tubularSegments<24||!Number.isInteger(radialSegments)||radialSegments<8)throw new RangeError('Invalid spring parameters');
 const positions=[],normals=[],indices=[],total=12*Math.PI,pitch=heightMm/total,r=13,wire=2,denom=Math.hypot(r,pitch),stride=radialSegments+1;
 const append=(p,n)=>{positions.push(p[0]/1000,p[2]/1000,-p[1]/1000);normals.push(n[0],n[2],-n[1]);};
 const point=(t,phi)=>{
   const ct=Math.cos(t),st=Math.sin(t),cp=Math.cos(phi),sp=Math.sin(phi);
   const normal=[ct*cp-pitch*st/denom*sp,st*cp+pitch*ct/denom*sp,-r/denom*sp];
   return {position:[r*ct+wire*normal[0],r*st+wire*normal[1],pitch*t+wire*normal[2]],normal};
 };
 for(let i=0;i<=tubularSegments;i++)for(let j=0;j<=radialSegments;j++){
   const q=point(total*i/tubularSegments,2*Math.PI*j/radialSegments);append(q.position,q.normal);
 }
 for(let i=0;i<tubularSegments;i++)for(let j=0;j<radialSegments;j++){
   const a=i*stride+j,b=a+1,c=a+stride,d=c+1;indices.push(a,b,c,b,d,c);
 }
 for(const end of [0,1]){
   const t=total*end,sign=end?1:-1,n=[-r*Math.sin(t)/denom*sign,r*Math.cos(t)/denom*sign,pitch/denom*sign];
   const center=positions.length/3;append([r*Math.cos(t),r*Math.sin(t),pitch*t],n);
   for(let j=0;j<=radialSegments;j++)append(point(t,2*Math.PI*j/radialSegments).position,n);
   for(let j=0;j<radialSegments;j++){
     const a=center+1+j,b=a+1;indices.push(...(end?[center,a,b]:[center,b,a]));
   }
 }
 return {positions:new Float32Array(positions),normals:new Float32Array(normals),indices:new Uint32Array(indices)};
}
