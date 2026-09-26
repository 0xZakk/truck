/** Exact-CAD cable pose lookup. No Three dependency or geometry interpolation.
 * Parent-local meshes use meters [X,Z,-Y]. Rigid deltas act on neutral GLBs.
 * Lazy decompression: request only visible angles; pending promises are cached.
 */
export function cableAngle(degrees) {
  if(!Number.isFinite(degrees))throw new Error('Nonfinite cable angle');
  return Math.max(0,Math.min(90,Math.round(degrees)));
}
async function unpackMesh(entry) {
  const binary=atob(entry.deflate_base64),compressed=Uint8Array.from(binary,c=>c.charCodeAt(0));
  const stream=new Blob([compressed]).stream().pipeThrough(new DecompressionStream('deflate'));
  const raw=await new Response(stream).arrayBuffer(),expected=entry.vertex_count*12+entry.triangle_count*12;
  if(raw.byteLength!==expected)throw new Error('Cable mesh byte count mismatch');
  const view=new DataView(raw),positions=new Float32Array(entry.vertex_count*3),normals=new Float32Array(positions.length),indices=new Uint32Array(entry.triangle_count*3);
  for(let i=0;i<entry.vertex_count;i++){
    const x=view.getInt32(i*12,true)/1e7,y=view.getInt32(i*12+4,true)/1e7,z=view.getInt32(i*12+8,true)/1e7;
    positions.set([x,z,-y],i*3);
  }
  for(let i=0;i<indices.length;i++){indices[i]=view.getUint32(entry.vertex_count*12+i*4,true);if(indices[i]>=entry.vertex_count)throw new Error('Cable mesh index out of range');}
  for(let i=0;i<indices.length;i+=3){
    const a=indices[i]*3,b=indices[i+1]*3,c=indices[i+2]*3;
    const u=[0,1,2].map(j=>positions[b+j]-positions[a+j]),v=[0,1,2].map(j=>positions[c+j]-positions[a+j]);
    const n=[u[1]*v[2]-u[2]*v[1],u[2]*v[0]-u[0]*v[2],u[0]*v[1]-u[1]*v[0]];
    for(const k of [a,b,c])for(let j=0;j<3;j++)normals[k+j]+=n[j];
  }
  for(let i=0;i<normals.length;i+=3){const length=Math.hypot(normals[i],normals[i+1],normals[i+2]);if(length<1e-15)throw new Error('Degenerate cable normal');for(let j=0;j<3;j++)normals[i+j]/=length;}
  return {positions,normals,indices,packedBytes:new Uint8Array(raw)};
}
export function createThrottleCableMotion(data) {
  if(data.schema!=='illustrative-throttle-cable-motion-v1'||data.frames.length!==91)throw new Error('Invalid cable pose table');
  const cache=new Map();
  return {
    angle:cableAngle,
    frame(degrees){
      const angle=cableAngle(degrees);
      if(!cache.has(angle))cache.set(angle,(async()=>{
        const source=data.frames[angle];if(source.angle_deg!==angle)throw new Error('Cable frame order mismatch');
        const meshes={};for(const [kind,entry] of Object.entries(source.meshes))meshes[kind]=await unpackMesh(entry);
        return {angle_deg:angle,rigid:source.rigid,meshes,ball_center_cad_mm:source.ball_center_cad_mm,fixed_pivot_cad_mm:source.fixed_pivot_cad_mm};
      })());
      return cache.get(angle);
    },
    cachedAngles(){return [...cache.keys()].sort((a,b)=>a-b);},
    clear(){cache.clear();}
  };
}
