// Private candidate numeric adapter. Millimeter engine CAD XYZ; no viewer dispatch.
// Replacement dimensions + inferred end contract, not a factory-exact spring.
// Provenance: reference/engine/valve-spring-reconciliation-20261003-browser-fixtures.json.
export const springCandidateParameters=Object.freeze({
 intake:Object.freeze({radius:15.2908,wire:4.699,free:49.784,solid:28.956,freeTurns:6.2,endPitch:4.704630596565859,grind:2.493090753976743,wireLength:597.9009470133933}),
 exhaust:Object.freeze({radius:15.2527,wire:4.6228,free:45.212,solid:25.654,freeTurns:5.87,endPitch:4.628187639981552,grind:3.10247093074141,wireLength:564.6340579925345}),
});
const END=.75,TRANSITION=.25;
function integral(f){
 const fa=f(0),fm=f(.5),fb=f(1),whole=(fa+4*fm+fb)/6;
 function step(a,b,fa,fm,fb,whole,tol,depth){
  const m=(a+b)/2,l=f((a+m)/2),r=f((m+b)/2);
  const left=(m-a)*(fa+4*l+fm)/6,right=(b-m)*(fm+4*r+fb)/6,delta=left+right-whole;
  if(Math.abs(delta)<=15*tol)return left+right+delta/15;
  if(depth===0)throw new Error('Spring quadrature did not converge');
  return step(a,m,fa,l,fm,left,tol/2,depth-1)+step(m,b,fm,r,fb,right,tol/2,depth-1);
 }
 return step(0,1,fa,fm,fb,whole,1e-10,20);
}
function pitch(s,turns,height){return s.endPitch+(height-s.wire+2*s.grind-s.endPitch*turns)/(turns-2*END-TRANSITION);}
function length(s,turns,p){
 const circumference=2*Math.PI*s.radius;
 const transition=integral(x=>Math.hypot(circumference,s.endPitch+(p-s.endPitch)*(3*x*x-2*x*x*x)));
 return 2*END*Math.hypot(circumference,s.endPitch)+2*TRANSITION*transition+(turns-2*END-2*TRANSITION)*Math.hypot(circumference,p);
}
export function springCandidateState(kind,height){
 const s=springCandidateParameters[kind];
 if(!s||!Number.isFinite(height)||height<=s.solid||height>s.free+1e-10)throw new RangeError('Spring kind/height outside candidate domain');
 let lo=s.freeTurns*.9,hi=s.freeTurns*1.1;
 const residual=t=>length(s,t,pitch(s,t,height))-s.wireLength;
 if(!(residual(lo)<0&&residual(hi)>0))throw new Error('Spring length root not bracketed');
 for(let i=0;i<52;i++){const mid=(lo+hi)/2;if(residual(mid)>0)hi=mid;else lo=mid;}
 const turns=(lo+hi)/2,p=pitch(s,turns,height);
 return Object.freeze({kind,height,turns,pitch:p,wireLength:length(s,turns,p)});
}
export function springCandidatePoint(state,u){
 const s=springCandidateParameters[state.kind],T=state.turns;
 if(!s||!Number.isFinite(u)||u<0||u>T)throw new RangeError('Invalid spring path coordinate');
 const w=Math.min(u,T-u),d=state.pitch-s.endPitch,t=Math.max(0,Math.min(1,(w-END)/TRANSITION));
 let z=s.endPitch*w+(w<=END?0:w<END+TRANSITION?d*TRANSITION*(t*t*t-.5*t*t*t*t):d*(w-END-TRANSITION/2));
 const total=s.endPitch*T+d*(T-2*END-TRANSITION);
 if(u>T/2)z=total-z;
 return [s.radius*Math.cos(-2*Math.PI*u),s.radius*Math.sin(-2*Math.PI*u),z+s.wire/2-s.grind];
}
