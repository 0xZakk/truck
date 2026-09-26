// Isolated replacement-catalog teaching candidate. NOT the installed Ford cam law.
export const valveStudy = Object.freeze({
  camLiftMm: .247 * 25.4, catalogValveLiftMm: .395 * 25.4,
  durationAt050CrankDeg: 192, assumedZeroLiftDurationCrankDeg: 270,
  rockerRatio: 1.6, baseCircleRadiusMm: 18,
  intakeCenterAfterFiringTdcDeg: 468, exhaustCenterAfterFiringTdcDeg: 246,
  firingOrder: Object.freeze([1, 5, 3, 6, 2, 4]),
  valveAxisY: -16, pushrodAxisY: 90, pushrodLengthMm: 226.6,
});
const rad = Math.PI / 180;
const mod = (v, n) => ((v % n) + n) % n;
const halfWidth = valveStudy.assumedZeroLiftDurationCrankDeg / 2;
const thresholdT = (valveStudy.durationAt050CrankDeg / 2) / halfWidth;
const bumpK = -Math.log(.050 / .247) * (1 - thresholdT ** 2) / thresholdT ** 2;
// Smooth compact bump: endpoints are assumed zero-lift, since catalog advertised
// duration's checking height is unknown. Entire shape between catalog points is assumed.
export function lobeState(offsetCrankDeg) {
  if (!Number.isFinite(offsetCrankDeg)) throw new RangeError('Finite crank angle required');
  const t = offsetCrankDeg / halfWidth;
  if (Math.abs(t) >= 1) return {liftMm: 0, slopeMmPerCamRad: 0, curvatureMmPerCamRad2: 0};
  const v = 1 - t * t;
  const liftMm = valveStudy.camLiftMm * Math.exp(-bumpK * t * t / v);
  const first = -2 * bumpK * t / v ** 2;
  const second = -2 * bumpK * (1 + 3 * t * t) / v ** 3;
  const halfCamRad = halfWidth * rad / 2;
  return {liftMm, slopeMmPerCamRad: liftMm * first / halfCamRad,
    curvatureMmPerCamRad2: liftMm * (first * first + second) / halfCamRad ** 2};
}
export function valveState(crankDeg, cylinder, kind) {
  if (!Number.isFinite(crankDeg) || !valveStudy.firingOrder.includes(cylinder) || !['intake','exhaust'].includes(kind)) throw new RangeError('Finite angle, cylinder 1–6 and intake/exhaust required');
  const firingDeg = valveStudy.firingOrder.indexOf(cylinder) * 120;
  const center = kind === 'intake' ? valveStudy.intakeCenterAfterFiringTdcDeg : valveStudy.exhaustCenterAfterFiringTdcDeg;
  const offset = mod(crankDeg - firingDeg - center + 360, 720) - 360;
  return {...lobeState(offset), cylinder, kind, firingDeg, cycleDeg: mod(crankDeg-firingDeg,720)};
}
// Envelope of support lines for a flat translating tappet: p=h*n + dh/dφ*t.
// Merely plotting radius=base+lift would be wrong for a flat tappet.
export function camProfilePoint(camDeg) {
  if (!Number.isFinite(camDeg)) throw new RangeError('Finite cam angle required');
  const angle = (mod(camDeg + 180, 360) - 180) * rad;
  const s = lobeState(angle / rad * 2);
  const h = valveStudy.baseCircleRadiusMm + s.liftMm;
  return {y: h*Math.sin(angle)+s.slopeMmPerCamRad*Math.cos(angle),
    z: h*Math.cos(angle)-s.slopeMmPerCamRad*Math.sin(angle),
    radiusOfCurvatureMm: h+s.curvatureMmPerCamRad2};
}
// Solves rigid pushrod closure with its lower end constrained to a vertical lifter
// axis. Rocker pad slides on valve tip; no spring dynamics or lash simulation.
export function rockerState(lifterLiftMm) {
  if (!Number.isFinite(lifterLiftMm) || lifterLiftMm < 0 || lifterLiftMm > valveStudy.camLiftMm + 1e-9) throw new RangeError('Lift outside candidate profile');
  const pivotY = (valveStudy.rockerRatio*valveStudy.pushrodAxisY+valveStudy.valveAxisY)/(1+valveStudy.rockerRatio);
  const pushArm = valveStudy.pushrodAxisY-pivotY, valveArm = pivotY-valveStudy.valveAxisY;
  const length=valveStudy.pushrodLengthMm;
  let low=0, high=.3;
  for(let i=0;i<60;i++) {
    const a=(low+high)/2, dy=pushArm*(Math.cos(a)-1);
    const lowerLift=pushArm*Math.sin(a)+length-Math.sqrt(length*length-dy*dy);
    if(lowerLift<lifterLiftMm)low=a;else high=a;
  }
  const angle=(low+high)/2;
  const pushrodTop=[pivotY+pushArm*Math.cos(angle),pushArm*Math.sin(angle)];
  const pushrodBottom=[valveStudy.pushrodAxisY,-length+lifterLiftMm];
  return {pivotY, angleRad:angle, pushArmMm:pushArm, valveArmMm:valveArm,
    valveLiftMm:valveArm*Math.sin(angle), padSlideMm:valveArm*(1-Math.cos(angle)),
    pushrodTop,pushrodBottom,
    closureErrorMm:Math.hypot(pushrodTop[0]-pushrodBottom[0],pushrodTop[1]-pushrodBottom[1])-length};
}
