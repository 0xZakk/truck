/** Pure tube mesh for the explicitly illustrative single throttle spring.
 * No Three dependency. Input is an exact-CAD-derived integer-angle frame.
 * Output positions use viewer meters [X,Z,-Y]; normals use the same axes.
 */
export function buildThrottleSpringMesh(frame, wireRadiusMm = 0.45, sides = 12) {
  const points = frame.points_cad_mm;
  if (points.length < 3 || !Number.isInteger(sides) || sides < 6) throw new Error('Invalid spring mesh input');
  const subtract = (a,b) => a.map((v,i)=>v-b[i]);
  const dot = (a,b) => a.reduce((sum,v,i)=>sum+v*b[i],0);
  const unit = a => { const n=Math.hypot(...a); if(n<1e-10) throw new Error('Repeated spring point'); return a.map(v=>v/n); };
  const cross = (a,b) => [a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0]];
  const count=points.length*sides+2, positions=new Float32Array(count*3), normals=new Float32Array(count*3), indices=[];
  let normal=null,firstTangent,lastTangent;
  function store(index,p,n) { positions.set([p[0]/1000,p[2]/1000,-p[1]/1000],index*3); normals.set([n[0],n[2],-n[1]],index*3); }
  for(let i=0;i<points.length;i++) {
    const tangent=unit(subtract(points[Math.min(i+1,points.length-1)],points[Math.max(i-1,0)]));
    if(!normal) { const ref=Math.abs(tangent[1])<.9?[0,1,0]:[1,0,0];normal=unit(cross(tangent,ref));firstTangent=tangent; }
    else normal=unit(normal.map((v,j)=>v-dot(normal,tangent)*tangent[j]));
    const binormal=cross(tangent,normal);
    for(let j=0;j<sides;j++) {
      const angle=2*Math.PI*j/sides,n=normal.map((v,k)=>v*Math.cos(angle)+binormal[k]*Math.sin(angle));
      store(i*sides+j,points[i].map((v,k)=>v+wireRadiusMm*n[k]),n);
      if(i<points.length-1) { const a=i*sides+j,c=i*sides+(j+1)%sides,b=a+sides,d=c+sides;indices.push(a,c,b,c,d,b); }
    }
    lastTangent=tangent;
  }
  const firstCenter=count-2,lastCenter=count-1,lastRing=(points.length-1)*sides;
  store(firstCenter,points[0],firstTangent.map(v=>-v));store(lastCenter,points.at(-1),lastTangent);
  for(let j=0;j<sides;j++) { indices.push(firstCenter,(j+1)%sides,j,lastCenter,lastRing+j,lastRing+(j+1)%sides); }
  return {positions,normals,indices:new Uint32Array(indices)};
}
