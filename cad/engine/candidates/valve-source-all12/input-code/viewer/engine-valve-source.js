// Coordinated source-sized candidate. Only pair with regenerated source-v2 CAD.
import {valveState} from './engine-valve-motion.js';
export const sourceLayout=Object.freeze({pivotY:51.0718402496357,valveY:-12,pushrodY:90,
 lengths:{intake:120.6246,exhaust:120.65},installed:{intake:41.656,exhaust:37.338},
 pushrodLength:250.00335443437204,lowerBallZ:139.7,padZ:-1.5,padRadius:12,
 cupZ:-5.421245565627949,maxCamLift:.247*25.4});
export function sourceRest(kind){
 const p=sourceLayout;if(!(kind in p.lengths))throw new RangeError('Unknown valve kind');
 const tip=261+p.lengths[kind],a=p.pushrodY-p.pivotY,v=p.pivotY-p.valveY;
 let lo=-.02,hi=.02,t,pivotZ,top;
 for(let i=0;i<65;i++){
  t=(lo+hi)/2;pivotZ=tip+v*Math.sin(t)-p.padZ*Math.cos(t)+p.padRadius;
  top=[p.pivotY+a*Math.cos(t)-p.cupZ*Math.sin(t),pivotZ+a*Math.sin(t)+p.cupZ*Math.cos(t)];
  if(Math.hypot(top[0]-p.pushrodY,top[1]-p.lowerBallZ)<p.pushrodLength)lo=t;else hi=t;
 }
 return {angleRad:t,pivotZ,top,tipZ:tip};
}
export function sourceLinkage(lift,kind){
 const p=sourceLayout;if(!Number.isFinite(lift)||lift<0||lift>p.maxCamLift+1e-9)throw new RangeError('Invalid cam lift');
 const r=sourceRest(kind),a=p.pushrodY-p.pivotY,v=p.pivotY-p.valveY,bottom=[p.pushrodY,p.lowerBallZ+lift];
 let lo=r.angleRad-.001,hi=r.angleRad+.3,t,top;
 for(let i=0;i<65;i++){
  t=(lo+hi)/2;top=[p.pivotY+a*Math.cos(t)-p.cupZ*Math.sin(t),r.pivotZ+a*Math.sin(t)+p.cupZ*Math.cos(t)];
  if(Math.hypot(top[0]-bottom[0],top[1]-bottom[1])<p.pushrodLength)lo=t;else hi=t;
 }
 return {lifterLiftMm:lift,angleRad:t,pivotZ:r.pivotZ,top,bottom,
 valveLiftMm:r.tipZ-(r.pivotZ-v*Math.sin(t)+p.padZ*Math.cos(t)-p.padRadius),
 padY:p.pivotY-v*Math.cos(t)-p.padZ*Math.sin(t)};
}
export function sourceValveState(crank,cylinder,kind){return sourceLinkage(valveState(crank,cylinder,kind).liftMm,kind);}
export function sourceOccurrencePose(crank,m){
 if(m.model!=='source-sized-v2')throw new RangeError('Source-v2 occurrence required');
 const s=sourceValveState(crank,m.cylinder,m.kind),r=sourceLinkage(0,m.kind);
 let translationEngineCad=[0,0,0],rotationXDeltaRad=0;
 if(m.role==='lifter')translationEngineCad=[0,0,s.lifterLiftMm];
 else if(m.role==='valve')translationEngineCad=[0,0,-s.valveLiftMm];
 else if(m.role==='rocker')rotationXDeltaRad=s.angleRad-r.angleRad;
 else if(m.role==='pushrod'){
  translationEngineCad=[0,(s.top[0]+s.bottom[0]-r.top[0]-r.bottom[0])/2,(s.top[1]+s.bottom[1]-r.top[1]-r.bottom[1])/2];
  const a=q=>-Math.atan2(q.top[0]-q.bottom[0],q.top[1]-q.bottom[1]);rotationXDeltaRad=a(s)-a(r);
 }else if(m.role!=='spring')throw new RangeError('Unknown motion role');
 return {translationEngineCad,rotationXDeltaRad,...(m.role==='spring'?{springHeightMm:sourceLayout.installed[m.kind]-Math.max(0,s.valveLiftMm)}:{})};
}
// Display-space metres,Y-up. Truncate actual tube triangles at the two ground
// planes, then close their boundaries. Wire is not squashed or axis-scaled.
export function sourceSpringMeshData(heightMm,N=192,R=16,captureRecipe=false){
 if(!Number.isFinite(heightMm)||heightMm<27||heightMm>50||!Number.isInteger(N)||N<48||!Number.isInteger(R)||R<8)throw new RangeError('Invalid spring mesh parameters');
 const total=12*Math.PI,pitch=heightMm/total,r=13,wire=2,den=Math.hypot(r,pitch),grid=[],faces=[],stride=R+1;
 const point=(t,phi)=>{const ct=Math.cos(t),st=Math.sin(t),cp=Math.cos(phi),sp=Math.sin(phi),n=[ct*cp-pitch*st/den*sp,st*cp+pitch*ct/den*sp,-r/den*sp];return {p:[(r*ct+wire*n[0])/1000,(pitch*t+wire*n[2])/1000,-(r*st+wire*n[1])/1000],n:[n[0],n[2],-n[1]],...(captureRecipe?{recipe:{type:'tube',t,phi}}:{})};};
 for(let i=0;i<=N;i++)for(let j=0;j<=R;j++)grid.push(point(total*i/N,2*Math.PI*j/R));
 for(let i=0;i<N;i++)for(let j=0;j<R;j++){const a=i*stride+j,b=a+1,c=a+stride,d=c+1;faces.push([grid[a],grid[b],grid[c]],[grid[b],grid[d],grid[c]]);}
 for(const end of [0,1]){
  const t=total*end,sign=end?1:-1,n=[-r*Math.sin(t)/den*sign,pitch/den*sign,-r*Math.cos(t)/den*sign],center={p:[r*Math.cos(t)/1000,pitch*t/1000,-r*Math.sin(t)/1000],n,...(captureRecipe?{recipe:{type:'center',t,sign}}:{})};
  for(let j=0;j<R;j++){const a={...point(t,2*Math.PI*j/R),n},b={...point(t,2*Math.PI*(j+1)/R),n};if(captureRecipe){a.recipe={...a.recipe,capSign:sign};b.recipe={...b.recipe,capSign:sign};}faces.push(end?[center,a,b]:[center,b,a]);}
 }
 const clip=(poly,h,keepAbove)=>{
  const output=[];
  for(let i=0;i<poly.length;i++){
   const a=poly[i],b=poly[(i+1)%poly.length],da=(a.p[1]-h)*(keepAbove?1:-1),db=(b.p[1]-h)*(keepAbove?1:-1),ain=da>=-1e-13,bin=db>=-1e-13;
   if(ain)output.push(a);
   if(ain!==bin){const t=da/(da-db),p=a.p.map((x,k)=>x+t*(b.p[k]-x)),n=a.n.map((x,k)=>x+t*(b.n[k]-x)),norm=Math.hypot(...n);p[1]=h;output.push({p,n:n.map(x=>x/norm),...(captureRecipe?{recipe:{type:'cut',a:a.recipe,b:b.recipe,upper:h!==0}}:{})});}
  }
  return output;
 };
 const triangles=[];
 for(const tri of faces){const poly=clip(clip(tri,0,true),heightMm/1000,false);for(let i=1;i+1<poly.length;i++){const a=poly[0].p,b=poly[i].p,c=poly[i+1].p,u=b.map((x,k)=>x-a[k]),v=c.map((x,k)=>x-a[k]),area=Math.hypot(u[1]*v[2]-u[2]*v[1],u[2]*v[0]-u[0]*v[2],u[0]*v[1]-u[1]*v[0]);if(area>1e-18)triangles.push([poly[0],poly[i],poly[i+1]]);}}
 // Geometric edge identities deliberately ignore normal discontinuities.
 const key=p=>p.map(x=>Math.round(x*1e10)).join(','),edgeMap=new Map(),points=new Map(),pointRecipes=new Map();
 for(const tri of triangles)for(let i=0;i<3;i++){
  const a=tri[i].p,b=tri[(i+1)%3].p,ka=key(a),kb=key(b);if(captureRecipe){pointRecipes.set(ka,tri[i].recipe);pointRecipes.set(kb,tri[(i+1)%3].recipe);}if(ka===kb)continue;points.set(ka,a);points.set(kb,b);
  const ek=[ka,kb].sort().join('|');if(edgeMap.has(ek))edgeMap.get(ek).count++;else edgeMap.set(ek,{a:ka,b:kb,count:1});
 }
 const capPolygons=[];
 for(const [h,normal] of [[0,[0,-1,0]],[heightMm/1000,[0,1,0]]]){
  const adjacency=new Map();
  for(const e of edgeMap.values())if(e.count===1&&Math.abs(points.get(e.a)[1]-h)<1e-10&&Math.abs(points.get(e.b)[1]-h)<1e-10){
   for(const [a,b] of [[e.a,e.b],[e.b,e.a]]){if(!adjacency.has(a))adjacency.set(a,[]);adjacency.get(a).push(b);}
  }
  const unused=new Set(adjacency.keys());
  while(unused.size){
   const start=unused.values().next().value,loop=[];let previous=null,current=start;
   do{loop.push(points.get(current));unused.delete(current);const choices=adjacency.get(current);if(choices.length!==2)throw new Error('Spring cap boundary not manifold');const next=choices.find(x=>x!==previous);previous=current;current=next;}while(current!==start&&loop.length<=adjacency.size+1);
   if(current!==start)throw new Error('Open spring cap boundary');
   const signed=loop.reduce((sum,p,i)=>{const q=loop[(i+1)%loop.length];return sum+p[0]*q[2]-q[0]*p[2];},0);
   if((signed>0)!==(normal[1]<0))loop.reverse();
   capPolygons.push({loop,normal});
  }
 }
 const cross=(a,b,c)=>(b[0]-a[0])*(c[2]-a[2])-(b[2]-a[2])*(c[0]-a[0]);
 for(const {loop,normal} of capPolygons){
  const polygon=loop.slice(),sign=normal[1]<0?1:-1;let attempts=0;
  while(polygon.length>3){
   let found=false;
   for(let i=0;i<polygon.length;i++){
    const a=polygon[(i+polygon.length-1)%polygon.length],b=polygon[i],c=polygon[(i+1)%polygon.length],area=cross(a,b,c)*sign;
    if(area<1e-16)continue;
    if(polygon.some(p=>p!==a&&p!==b&&p!==c&&cross(a,b,p)*sign>1e-16&&cross(b,c,p)*sign>1e-16&&cross(c,a,p)*sign>1e-16))continue;
    triangles.push([a,b,c].map(p=>({p,n:normal})));polygon.splice(i,1);found=true;break;
   }
   if(!found){const i=polygon.findIndex((p,i)=>Math.abs(cross(polygon[(i+polygon.length-1)%polygon.length],p,polygon[(i+1)%polygon.length]))<1e-16);if(i>=0)polygon.splice(i,1);else throw new Error('Cannot triangulate spring cap');}
   if(++attempts>loop.length*2)throw new Error('Spring cap triangulation failed');
  }
  if(polygon.length===3)triangles.push(polygon.map(p=>({p,n:normal})));
 }
 const positions=[],normals=[];for(const tri of triangles)for(const v of tri){positions.push(...v.p);normals.push(...v.n);}
 return {positions:new Float32Array(positions),normals:new Float32Array(normals),indices:null,groundCaps:capPolygons.length,...(captureRecipe?{capLoops:capPolygons.map(({loop,normal})=>({recipes:loop.map(p=>pointRecipes.get(key(p))),normal})),recipes:triangles.flatMap(tri=>tri.map(v=>({recipe:v.recipe||pointRecipes.get(key(v.p)),...(v.recipe?{}:{fixedNormal:v.n})})))}:{})};
}
