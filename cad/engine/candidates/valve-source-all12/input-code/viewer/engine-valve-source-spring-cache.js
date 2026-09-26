// Exact-height source-v2 display spring updates. Templates cache connectivity,
// not positions/heights: wire radius and both ground planes update every call.
import {sourceSpringMeshData} from './engine-valve-source.js';
const TOTAL=12*Math.PI,RADIUS=13,WIRE=2;
function topologyKey(height,N,R){
 const pitch=height/TOTAL,den=Math.hypot(RADIUS,pitch);let key=`${N}:${R}:`;
 // Only these end rings can cross a ground plane. The rest are always inside.
 const end=Math.min(N,Math.ceil(2*N/height)+1);
 for(let i=0;i<=N;i++)if(i<=end||i>=N-end)for(let j=0;j<=R;j++){
  const y=(height*i/N-WIRE*RADIUS/den*Math.sin(2*Math.PI*j/R))/1000;
  key+=y < -1e-13?'b':y>height/1000+1e-13?'t':'i';
 }
 return key;
}
function compile(mesh){
 const nodes=[],lookup=new Map();
 function node(recipe){
  const key=JSON.stringify(recipe);if(lookup.has(key))return lookup.get(key);
  let value;
  if(recipe.type==='cut')value={type:2,a:node(recipe.a),b:node(recipe.b),upper:recipe.upper};
  else {const {t,phi=0}=recipe;value={type:recipe.type==='center'?1:0,ct:Math.cos(t),st:Math.sin(t),cp:Math.cos(phi),sp:Math.sin(phi),fraction:t/TOTAL,capSign:recipe.capSign||recipe.sign||0};}
  const index=nodes.length;nodes.push(value);lookup.set(key,index);return index;
 }
 const body=mesh.recipes.filter(v=>!v.fixedNormal),refs=new Uint32Array(body.length);
 body.forEach((v,i)=>{refs[i]=node(v.recipe);});
 const capLoops=mesh.capLoops.map(loop=>({refs:loop.recipes.map(node),normal:loop.normal[1]}));
 return {nodes,refs,capLoops,groundCaps:mesh.groundCaps};
}
function update(template,height){
 const {nodes,refs,capLoops}=template,pitch=height/TOTAL,den=Math.hypot(RADIUS,pitch),values=new Float64Array(nodes.length*6);
 for(let i=0;i<nodes.length;i++){
  const n=nodes[i],o=i*6;
  if(n.type===2){
   const a=n.a*6,b=n.b*6,y=n.upper?height/1000:0,t=(y-values[a+1])/(values[b+1]-values[a+1]);
   for(let k=0;k<6;k++)values[o+k]=values[a+k]+t*(values[b+k]-values[a+k]);values[o+1]=y;
   const norm=Math.hypot(values[o+3],values[o+4],values[o+5]);for(let k=3;k<6;k++)values[o+k]/=norm;
  }else{
   const x=n.ct*n.cp-pitch*n.st/den*n.sp,z=-RADIUS/den*n.sp,y=n.st*n.cp+pitch*n.ct/den*n.sp;
   values[o]=(RADIUS*n.ct+(n.type===0?WIRE*x:0))/1000;
   values[o+1]=(height*n.fraction+(n.type===0?WIRE*z:0))/1000;
   values[o+2]=-(RADIUS*n.st+(n.type===0?WIRE*y:0))/1000;
   if(n.capSign){values[o+3]=-RADIUS*n.st/den*n.capSign;values[o+4]=pitch/den*n.capSign;values[o+5]=-RADIUS*n.ct/den*n.capSign;}
   else{values[o+3]=x;values[o+4]=z;values[o+5]=-y;}
  }
 }
 // Ground-cap concavity changes within a clipping topology interval. Re-ear
 // clip only the small cap polygons at the exact height; reusing old diagonals
 // can invert cap triangles even though the side topology remains unchanged.
 const caps=[];
 const cross=(a,b,c)=>(values[b*6]-values[a*6])*(values[c*6+2]-values[a*6+2])-(values[b*6+2]-values[a*6+2])*(values[c*6]-values[a*6]);
 for(const loop of capLoops){
  const polygon=loop.refs.slice(),sign=loop.normal<0?1:-1;let attempts=0;
  while(polygon.length>3){
   let found=false;
   for(let i=0;i<polygon.length;i++){
    const a=polygon[(i+polygon.length-1)%polygon.length],b=polygon[i],c=polygon[(i+1)%polygon.length];
    if(cross(a,b,c)*sign<1e-16)continue;
    if(polygon.some(p=>p!==a&&p!==b&&p!==c&&cross(a,b,p)*sign>1e-16&&cross(b,c,p)*sign>1e-16&&cross(c,a,p)*sign>1e-16))continue;
    caps.push({refs:[a,b,c],normal:loop.normal});polygon.splice(i,1);found=true;break;
   }
   if(!found){const i=polygon.findIndex((p,i)=>Math.abs(cross(polygon[(i+polygon.length-1)%polygon.length],p,polygon[(i+1)%polygon.length]))<1e-16);if(i>=0)polygon.splice(i,1);else throw new Error('Cannot triangulate spring cap');}
   if(++attempts>loop.refs.length*2)throw new Error('Spring cap triangulation failed');
  }
  if(polygon.length===3)caps.push({refs:polygon,normal:loop.normal});
 }
 const positions=new Float32Array((refs.length+caps.length*3)*3),normals=new Float32Array(positions.length);
 for(let i=0;i<refs.length;i++){
  const src=refs[i]*6,dst=i*3;positions[dst]=values[src];positions[dst+1]=values[src+1];positions[dst+2]=values[src+2];
  normals[dst]=values[src+3];normals[dst+1]=values[src+4];normals[dst+2]=values[src+5];
 }
 let dst=refs.length*3;
 for(const cap of caps)for(const ref of cap.refs){const src=ref*6;positions[dst]=values[src];positions[dst+1]=values[src+1];positions[dst+2]=values[src+2];normals[dst+1]=cap.normal;dst+=3;}
 return {positions,normals,indices:null,groundCaps:template.groundCaps};
}
export function createSourceSpringTemplateCache(maxTemplates=32){
 if(!Number.isInteger(maxTemplates)||maxTemplates<1||maxTemplates>128)throw new RangeError('Invalid template limit');
 const templates=new Map();let hits=0,misses=0;
 return {
  get(height,N=192,R=16){
   if(!Number.isFinite(height)||height<27||height>50||!Number.isInteger(N)||N<48||!Number.isInteger(R)||R<8)throw new RangeError('Invalid spring mesh parameters');
   const key=topologyKey(height,N,R);let template=templates.get(key);
   if(template){hits++;templates.delete(key);templates.set(key,template);}
   else{misses++;template=compile(sourceSpringMeshData(height,N,R,true));templates.set(key,template);if(templates.size>maxTemplates)templates.delete(templates.keys().next().value);}
   return update(template,height);
  },
  get stats(){return {hits,misses,templates:templates.size,maxTemplates};},
  clear(){templates.clear();hits=0;misses=0;},
 };
}
const shared=createSourceSpringTemplateCache();
export const sourceSpringMeshDataFast=(height,N=192,R=16)=>shared.get(height,N,R);
export const sourceSpringCacheStats=()=>shared.stats;
// Optional during the loading state; yield between batches so the page remains
// responsive. A missed topology is still generated correctly on demand.
export async function prewarmSourceSpringCache(N=96,R=12){
 for(let i=0;i<=288;i++){
  shared.get(27.304596147326+(41.656-27.304596147326)*i/288,N,R);
  if(i%12===0)await new Promise(resolve=>setTimeout(resolve,0));
 }
 return shared.stats;
}
