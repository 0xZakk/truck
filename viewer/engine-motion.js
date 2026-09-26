// Pure zero-offset slider-crank solver in display axes (Y up, X shaft).
// Geometry follows the declared dimensions; their evidence lives in the manifest.
export function sliderCrank(degrees, radius, rodLength) {
  if (![degrees, radius, rodLength].every(Number.isFinite) || radius <= 0 || rodLength <= radius) {
    throw new RangeError('Finite angle and rod length > crank radius > 0 are required');
  }
  const angle=degrees*Math.PI/180;
  const journalY=radius*Math.cos(angle), journalZ=radius*Math.sin(angle);
  const rise=Math.sqrt(rodLength**2-journalZ**2);
  return {angle,journalY,journalZ,pistonY:journalY+rise,rodAngle:-Math.asin(journalZ/rodLength)};
}

export function rotaryViewRotation(degrees, motion) {
  const rotation=(degrees*motion.ratio+(motion.phase_deg??0))*Math.PI/180;
  if(!['x','y','z'].includes(motion.axis)||!Number.isFinite(rotation))throw new RangeError('Rotary motion requires a CAD axis and finite angle');
  return motion.axis==='x'?[rotation,0,0]:motion.axis==='y'?[0,0,-rotation]:[0,rotation,0];
}

export function compressorState(degrees, motion, engaged=true) {
  if(!Number.isFinite(degrees)||!['pulley','shaft','piston','shoe'].includes(motion.role))throw new RangeError('Finite compressor phase and a supported role are required');
  const phase=(engaged||motion.role==='pulley'?degrees:0)*Math.PI/180;
  if(motion.role==='pulley'||motion.role==='shaft')return {translationX:0,rotationX:phase};
  const cylinderPhase=motion.cylinder_phase_deg*Math.PI/180;
  const amplitude=motion.stroke_amplitude_mm;
  if(!Number.isFinite(cylinderPhase)||!Number.isFinite(amplitude)||amplitude<0)throw new RangeError('Finite cylinder phase and nonnegative stroke amplitude are required');
  return {translationX:amplitude*(Math.cos(cylinderPhase)-Math.cos(cylinderPhase-phase)),rotationX:motion.role==='shoe'?phase:0};
}
