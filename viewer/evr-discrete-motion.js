/** Exactly five CAD-derived EVR poses. No duty-cycle/pressure mapping.
 * applyPose receives one atomic update: replace the spring's LOCAL geometry;
 * set the disc mesh LOCAL translation from its captured base (never accumulate).
 * Preserve both occurrence wrappers, all parent transforms and materials.
 * CAD mm [x,y,z] -> viewer metres [x,z,-y]. Baseline travel is0.8mm.
 */
export function validateEvrMotionData(data) {
  const travels=[0,0.2,0.4,0.6,0.8];
  if(data.schema_version!==1 || data.baseline_travel_mm!==0.8 || data.poses?.length!==5) throw new Error('Invalid EVR pose set');
  data.poses.forEach((p,i)=>{
    const delta=(0.8-travels[i])/1000;
    if(p.index!==i || p.travel_mm!==travels[i] || !p.spring_glb || !p.spring_sha256 || p.disc_offset_cad_mm?.length!==3 || p.disc_offset_cad_mm.some((v,j)=>!Number.isFinite(v)||Math.abs(v-(j===2?0.8-travels[i]:0))>1e-12) || p.disc_offset_viewer_m?.length!==3 || p.disc_offset_viewer_m.some((v,j)=>!Number.isFinite(v)||Math.abs(v-(j===1?delta:0))>1e-12)) throw new Error('Unvalidated EVR pose');
  });
  return data;
}
export function createEvrDiscreteMotion(data,{loadSpring,applyPose}) {
  validateEvrMotionData(data);let sequence=0,current=4;const cache=new Map();
  return {
    get index(){return current;},
    async setIndex(index){
      if(!Number.isInteger(index)||index<0||index>4) throw new Error('EVR requires an integer pose index0–4');
      const ticket=++sequence,p=data.poses[index];
      if(!cache.has(index))cache.set(index,Promise.resolve(loadSpring(p.spring_glb,p.spring_sha256)).catch(e=>{cache.delete(index);throw e;}));
      const spring=await cache.get(index);if(ticket!==sequence)return false;
      applyPose({spring,discOffsetCadMm:[...p.disc_offset_cad_mm],discOffsetViewerM:[...p.disc_offset_viewer_m],travelMm:p.travel_mm,index,label:`Illustrative vent opening: ${p.travel_mm.toFixed(1)} mm`});current=index;return true;
    },
    cancel(){sequence++;}
  };
}
