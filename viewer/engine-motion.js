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
