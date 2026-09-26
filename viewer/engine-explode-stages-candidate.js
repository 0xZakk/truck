/** Piecewise-linear educational display separation; not a removal procedure. */
export function explodeOffset(occurrence, amount) {
  amount = Math.max(0, Math.min(1, Number(amount)));
  const stages = occurrence.explode_stages;
  if (!stages?.length) return (occurrence.explode_cad_mm ?? [0, 0, 0]).map(x => amount * x);
  if (stages.length < 2 || stages[0].at !== 0 || stages.at(-1).at !== 1 ||
      stages.some((s, i) => s.offset_cad_mm.length !== 3 || (i && s.at <= stages[i-1].at))) {
    throw new Error('Invalid explode stages');
  }
  for (let i = 1; i < stages.length; i++) {
    const a = stages[i-1], b = stages[i];
    if (amount <= b.at) {
      const t = (amount - a.at) / (b.at - a.at);
      return a.offset_cad_mm.map((x, axis) => x + (b.offset_cad_mm[axis] - x) * t);
    }
  }
  return [...stages.at(-1).offset_cad_mm];
}
