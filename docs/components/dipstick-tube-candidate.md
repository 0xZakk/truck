# Component contract and handoff: engine-oil-dipstick-tube feasibility

## Contract

- Issue: [#78](https://github.com/0xZakk/truck/issues/78), engine parent #1. Integration owner: root; contributor: pump_seal_finish.
- Baseline: `2cc2000f876901d76a12fbe251f03103a0e516de`, branch `engine/next-interface-contracts`. Manifest SHA-256: `f725260d8f1497a1b6f2aed9d41d01155bf2a82e7391d24ce866f352bb50cd5b`. Report hashes actual current inputs, including root's later export-only builder edit.
- Scope: an isolated educational candidate with proposed block receiver, formed hollow tube, lower nut envelope, replacement cover retainer, bracket and support nut. No installed block/pan/manifest or existing dipstick pilot changes. Root authorized estimated upstream interfaces after reviewing the baseline's missing receiver.
- Owned files: `cad/engine/dipstick_tube_candidate.py`, `scripts/check-dipstick-tube-candidate.py`, `inventory/engine/dipstick-tube-candidate-validation.json`, and this handoff. Ignored isolated outputs: `cad/engine/generated/dipstick-tube-feasibility/`.
- Units/axes: mm, installed engine CAD coordinates; front +X, cover side +Y, up +Z. No occurrence or explosion has been published.
- Identity: 6754 is the service base number; exact 1994 application, part identity and factory dimensions remain unknown. Adjacent1995 threaded lower retention/upper pushrod-cover support is architecture evidence, not dimension authority.
- Inputs: installed STEP definitions, manifest/transforms, block/cover builders, research ledger and existing blade pilot. No new online reference or restricted image was copied.

## Evidence ledger and design rationale

The baseline audit found no identifiable engine-oil tube receiver. It inventories58 rear/+Y cylindrical surfaces and tests36 lower-side paths, all obstructed; those finite probes do not prove absence of every possible angled opening. All six existing cover receivers are blind radius4 mounting bores at X=-285,-171,-57,57,171,285; Z185; Y109.4–117.5. Their plain headed bolts have no external support stud. These are current model facts, not factory measurements.

The new receiver was selected from the block section independently of the rejected blade pose. Its passage line intersects the rear +Y skirt at approximately(-315,111,0), with outward axis(0,0.5,0.8660254). X=-315 lies forward of the rear main support's forward edge X=-325.876 and behind rear cylinder center X=-284.48. The radius5 cut leaves5.876mm axial separation from that main-support envelope and stays below the cylinder/lifter protection zone. The entry descends inward to the existing crankcase and rear sump.

The external seat moved outward **along that same line** to clear the nut against the casting: **(-315,129,31.176915)mm**. This is an estimated seat, not a measured production port. The boss joins the existing casting; the modified block remains one solid. The cut removes1413.716693mm³; new material adds10574.806655mm³. Protected main/cylinder/lifter regions lose zero volume. The receiver cutter also has zero overlap with the installed pan and molded pan gasket.

| Candidate feature | Value / datum | Evidence class and limit |
|---|---|---|
| Receiver | Outward axis(0,.5,.8660254), seat(-315,129,31.176915), radius5 passage | Educational estimate from existing block section; not machining instructions |
| Boss | Radius10 body, radius8 upper retention envelope | Educational estimate; casting strength/thread specification unknown |
| Upper anchor | Rear existing cover station X=-285,Z185; head outer plane Y144.292 | Reuses installed model datum; actual truck's bracket station unresolved |
| Retainer | Existing lower bolt envelope plus exposed radius4 stud | Educational proposal, not verified6C517 dimensions; upper thread surfaces absent |
| Tube |9mm OD /7mm ID, curved lower route and straight upper section | Estimated clearance design; actual bend radii, material and routing unmeasured |
| Expanded mouth |10.5mm OD /8.5mm ID for upper60mm; mouth(-285,170,500) | Estimated compatibility with pilot's near-stop waves; factory height unknown |
| Blade study | Existing pilot6.5×0.8mm tip,2.2mm stem,3mm wave amplitude; approximate692.15mm axial length | Pilot estimates / seller comparison; no source-verified matched pair or calibration |
| Retention architecture | Lower nut; upper bracket retained at cover stud | Adjacent1995 Ford text; exact1994 applicability unresolved |

The support bracket has a plate bearing on the cover-retainer head, a bent tongue and a collar contacting the tube. The tube's lower shoulder contacts the boss and nut shoulder. Both nuts use clearance envelopes for their threads. Those surfaces explain the stack but do **not** establish threaded engagement, clamp load or strength.

The blade check uses a circle enclosing the pilot's6.5×0.8mm tip along the full guide, a larger circle enclosing its near-stop waves in the expanded mouth, and a free-tip continuation using the remaining approximate692.15mm length. The resulting guide length is558.476126mm and free-tip length133.673874mm. This checks dimensional space and a proposed seated path. It does not simulate elasticity, withdrawal, twist, wave compression, handle operation or oil-level calibration. The old -8.5° trial pose is unused.

## Delivery and reproduction

Readiness: **isolated educational feasibility candidate; not installed, not production-accurate, not Done**. `candidate(block, installed_bolt)` returns proposed solids and diagnostic probes in CAD world coordinates. `passage_evidence(...)` separately audits passage obstruction. No inert builder guard remains.

From repository root:

```sh
.venv-cad/bin/python scripts/check-dipstick-tube-candidate.py --render
```

The CAD environment is recorded in the JSON. Optional rendering additionally uses system `python3` with matplotlib/numpy. Hashed BREP caches under the ignored output directory accelerate repeated STEP loading and may be deleted freely. Every report still hashes installed STEP inputs and checks they remain unchanged.

Outputs include6 isolated STEP parts, diagnostic probes, positive/obstruction fixtures, and `candidate-review.png`. The final render was visually inspected: the connected lower route, upper support and expanded mouth are visible. The render shows the estimated route and a sectioned rear casting; it is generated geometry, not an owner photograph or factory comparison. No GLB/learning/browser occurrence was installed. Model/effort/usage unavailable.

## Validation and review

The numerical report is authoritative for current source hashes and values. The evaluated revision has:

- Six valid, single-solid parts; STEP roundtrip volume discrepancies below0.003mm³.
- Fifteen internal pairs clear at0.1mm³ overlap threshold; five intended contact pairs within0.002mm.
- 62 exact static comparisons selected from all1310 installed occurrences; no detected collisions above0.1mm³.
- 73 crank poses from0–720° at10° increments,175 exact moving comparisons; no detected collisions.
- Continuous conservative clearance checks in addition to sampling: full-X crank cylinder radius87.546mm derived from modeled crank primitives; rod bounds from `world_y = jy*(1-local_z/L) + local_y*cos(theta)`; piston boxes expanded through full stroke. All relevant intersections are zero.
- Clear proposed receiver and blade passage envelopes. Deliberately offset tube fails at666.573672mm³; shifted upper nut fails at97.878756mm³; the uncut block obstructs the same receiver probe at508.938010mm³. Synthetic plugged and offset bores also fail.

| Quality gate | Result | Remaining limit |
|---|---|---|
| Application/coverage | PARTIAL | Adjacent1995 architecture; exact1994 identity unresolved |
| Dimensions/coordinates | PASS educational contract | New coordinates/dimensions estimated; existing anchor reused explicitly |
| CAD/export | PASS isolated STEP | No installed GLB, rendering fidelity or factory contour acceptance |
| Source/visual comparison | PARTIAL | Generated review image inspected; applicable source image pixels/specimen still missing |
| Installed interfaces | NOT RUN installed; PASS bounded isolated geometry | Retention threads remain envelopes; actual clamping/sealing not validated |
| Motion/disassembly | PARTIAL | Model rotating/reciprocating clearance passed; elastic blade motion and removal sequence unvalidated |
| Learning/diagnostics | PASS geometric fault sensitivity; teaching UI NOT RUN | No calibration or service specification claims |
| Browser integration | NOT RUN | No component installed |
| Reproduction/review | PASS reproducible candidate; root review pending | Input/output hashes and commands included |

No prior installed acceptance is superseded. Candidate code may be reviewed independently of any decision to install it. Root must review proposed block changes, source applicability, actual thread/seat topology and the bracket construction before shared assembly edits.

## Exact integration proposal and restart

If this educational geometry is accepted for further work, adapt the shared block builder through a dedicated interface function using this candidate's seat/axis contract, preserving its one-solid receiver and protected-zone checks. Replace only occurrence `pushrod-cover-bolt-1` with the candidate retainer and preserve the other five bolts. Proposed IDs are `engine-oil-dipstick-tube`, `engine-oil-dipstick-tube-retaining-nut`, `engine-oil-dipstick-tube-bracket` and `engine-oil-dipstick-tube-support-nut`; their service association remains6754. The bracket is physically separate in the feasibility model; its real manufactured joint/captivity is unknown.

Next geometry work should specify mating threads and sealing-seat construction, then validate physical retention and disassembly. Next evidence work should confirm the actual tube/retainer station and matched blade mouth/stop dimensions. Recheck calibration only against independently established oil-level evidence. Do not propagate the present seat, bore or mouth estimates into factory specifications.

Issue#78 remains open. No shared geometry has changed. No process remains running after delivery. Root review and any future installation/browser acceptance are separate tasks.
