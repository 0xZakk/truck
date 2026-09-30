# Component contract and handoff: timing gear evidence reconciliation

## Contract

Issue #32 under engine #1. Root integration owner assigns evidence-only reconciliation; worker owns this document, `reference/engine/timing-gear-evidence-review.json` and isolated captures in `reference/engine/timing-gear-evidence/`. Cover/gasket investigation belongs to the air-cleaner worker. Initial scope was evidence-only; root subsequently authorized the bounded independent candidate described below, with owned timing candidate/checker/report/render files. No canonical manifest, shared builder or accepted stop dependency changes are authorized.

Branch `engine/runner-stops-and-evr`, code baseline `796b621244d8e341fe2f3c4de7af99488af01548` plus root-managed ongoing integration. Current source explicitly implements 24 crank / 48 cam teaching teeth, 20° involute form and14mm thickness at inherited center distance `hypot(90,72)` mm. These values are not source-supported production dimensions. Task: reconcile competing industrial92 and replacement58/29 count evidence, identify applicable variant and preserve uncertainty before proposing geometry. All local mounting/retention frames remain untouched.

Required source gates: view actual manufacturer catalog row/footnotes, confirm engine/year and material variant, separate a replacement match from owner-installed identity, and avoid using generic catalog photos as a count/dimension source. Purchased manuals and owner photographs are excluded from deliverables. Public catalog captures are local evidence; release authorization must be checked before distribution.

## Delivery / restart

Evidence reconciliation complete; independent candidate diagnostics in progress. No installed or factory-fidelity claim. PDF visual review completed. No source-supported dimensions or factory gear identity accepted yet. Exact commands, hashes, failure attempts and findings will be preserved in the evidence ledger. Browser/CAD/motion/export checks N/A to this evidence-only scope; any later geometry task requires a fresh component contract and all relevant gates. Issue read previously failed API connectivity; no remote status is newly claimed.

## Source reconciliation

Primary rows and actual page pixels were reviewed, not accepted from search snippets. [PBM catalog](https://www.pbm-erson.com/documents/d/prod/pbmcatalog02-03-2025), physical PDF204 / printed205, reference108 identifies the4.9L six-cylinder truck application. Its aluminum TG2766S entry gives58/29 and D3TZ6256C with1984–97 footnote; the heading ends1996, but1994 lies within both. Earlier steel TG2764S also lists58/29 with1965–83 footnote. These are replacement comparisons, not owner-installed identities.

The Ford industrial scan PDF13 / printed10 visibly gives C5TZ-6256-A92teeth cast iron, year marker70/. That is a distinct earlier industrial part, not a misread58. Its crank row lacks a count. Do not derive a92/46 truck pair from this alone.

[Melling manufacturer catalog mirror](https://images.carid.com/melling/info/pdf/melling-engine-parts-catalog.pdf), PDF111 / printed116, row18 applies to the Ford4.9L six-cylinder truck. It distinguishes2750AS aluminum standard-duty,2764S cast iron,2766AS aluminum heavy-duty and2766S fiber. All require matched-pair replacement. Similar part-number suffixes across manufacturers do not prove the same material or tooth profile.

[Elgin C-2766S manufacturer page](https://catalog.elginind.com/partno-search/?partno=C-2766S) labels an1984–96 matched set for Ford300, with cam/crank gear diameters6.610/3.400in (167.894/86.36mm). Its specifically identified photo shows opposite helical hands, two circular cam web holes, bore keyways and paired rim marks. Numeric helix angle, mark phase and face width remain unknown. Fiber-colored teeth are an appearance observation, not material analysis. Treating the published diameter as tip diameter is explicitly an assumption; the label does not specify a datum.

Evidence hashes, exact rows, observation limits and failed attempts are saved in `reference/engine/timing-gear-evidence-review.json`. Third-party captures are locally ignored and excluded from shared CAD releases. Refetch by ledger URL and verify hashes. Existing24/48 gear source remains explicitly illustrative and unchanged.

## Envelope and datum finding

Reproduce with `python3 scripts/check-timing-gear-evidence.py`; report `inventory/engine/timing-gear-evidence-validation.json`. Current center is115.256236mm. A standard unshifted58/29 pair on those axes implies158.974/82.137mm tips, substantially smaller than the comparison envelopes. Do not shrink source envelopes to make the current axes fit.

If comparison diameters are tips, separate standard-addendum inferences give transverse modules2.798233/2.785806mm and center distances121.723150/121.182581mm. These do not form one exact unshifted specification. Profile shifts, addenda, tooth-tip definition and cross-brand differences remain unresolved; the range is conditional arithmetic, not an authoritative target.

Root authorized an independent hypothesis with transverse module2.8mm, center121.8mm,20° transverse pressure angle, opposite25° helix,14mm width and0.12mm nominal backlash. It retains the comparison diameters via estimated addenda2.747/2.580mm. Normal module would be2.537662mm; lead magnitudes1094.115951/547.057976mm preserve the2:1 lead ratio. These values are estimates, not measured source dimensions. The hypothetical cam center isY95.109821/Z76.087857 when keeping the prior centerline direction and crank origin. Neither that direction nor121.8mm is a production datum.

The current cam axisY90/Z72 must not be translated alone. A coherent revision would affect block cam bores/bearings and rear plug, camshaft/lobes, spacer/key/thrust plate and its block bolt sockets, lifter tracks/contact, pushrod lengths/angles, valve actuation geometry, cam-to-distributor/oil-pump drive engagement, and timing-cover cavity/flange/seal relationship. Their current acceptance reports would need affected-scope reruns. Crank origin and all canonical parts remain unchanged.

## Independent pair scope and pending gates

`cad/engine/timing_gear_pair_candidate.py` builds a separately framed58/29 helical pair. `parts()` returns local `crank` and `cam`; `posed(parts, crank_degrees=0, center=CENTER)` positions the hypothetical pair with opposite half-speed cam rotation. Existing local bore sizes and cam rear relief/key region remain inherited interface studies. Two estimated cam web holes lie outside the protected central47mm region. Numeric timing-mark indexing and a production crank-key reconstruction remain outstanding.

Checker `scripts/check-timing-gear-pair-candidate.py` exports isolated STEP/GLBs, tests25 samples of one tooth period, deliberate half-tooth wrong phase and old-axis overlap, preserved local core, and conflicts against unchanged current shafts/spacer/key/cover. Root review must distinguish independent pair construction from current-engine installation. Positive clearance during unloaded backlash is not a loaded-contact proof. Loaded contact, continuous sweep, exact production tooth form, source-shaped reliefs and installed/browser acceptance remain NOT RUN.

Commands:

```sh
XDG_CACHE_HOME=/tmp/truck-cache .venv-cad/bin/python scripts/check-timing-gear-pair-candidate.py
```

Outputs under `cad/engine/generated/timing-gear-pair-candidate/`, report `inventory/engine/timing-gear-pair-candidate-validation.json`. The cover worker has received the conditional121.18–121.72mm standard-assumption range and separate121.8mm hypothesis; registered cover geometry is held for coordinated review. No canonical/shared edits are part of this task.


## Root visual review and bounded next refinement

Root directly viewed `cad/engine/generated/timing-gear-pair-candidate/pair-render.png` and accepted it as a useful bounded tooth-count/helix hypothesis, while identifying simplified web/hub shoulders and absent crank keyway. This is not installed acceptance. The identified Elgin photograph visibly contains those features; their numeric dimensions and actual installed identity are still unknown.

After current pair diagnostics finish, root authorized refinement confined to interior shoulders/keyway, preserving the frozen external tooth geometry. Any inherited sweep must bind archived original STEP/module/report hashes and demonstrate exact unchanged tooth rings; merely retaining tooth count or reusing a filename is insufficient. No canonical camshaft/casting translation is authorized. The independent core preservation check currently applies to the first shape; a newly cut keyway changes that bounded interface and must be reported explicitly rather than reusing its old zero-difference result.

## Completed independent diagnostics

`inventory/engine/timing-gear-pair-candidate-validation.json`: **PASS independent sampled pair; NOT INSTALLABLE at unchanged current axes**. Both exports are valid one-solid shapes with watertight meshes; STEP volume errors are below0.00000002mm³. All25 samples over one crank-tooth period produce zero exact overlap. Deliberate half-cam-tooth misphase produces574.806447mm³ overlap; forcing the old115.256236mm center produces1903.139238mm³ overlap. The first candidate's protected local bore/relief core differences are zero.

To avoid expensive whole-body extrema calculations, the checker clips exact shapes to a mathematically bounded tip-cylinder engagement lens. The bounds contain every possible pair overlap; clipped distances are local clearance measurements and upper bounds on global minimum distance. The first result exactly matches the retained full-body query. This changes computation cost, not overlap thresholds or sampled angles. The interrupted original log is retained under `slow-full-body-check.log`.

The proposed cam directly conflicts with the **unchanged** actual camshaft by2252.854957mm³ and current timing cover by520.175534mm³. These are expected installation failures and cannot be waived as intentional contacts. The crank clears its current shaft by0.025mm and current cover by4.82mm. The candidate is an independent pair, not a translated installed cam assembly.

`inventory/engine/timing-gear-contact-diagnostic.json`: **PASS finite first-contact bracket**. At both neutral and half a tooth period, additional cam phase0.08° retains a gap and0.09° causes positive overlap, bounding first drive-flank contact between those phases. This establishes nearby engagement sensitivity, not an exact loaded phase, continuous contact sweep, force/stress result or service backlash specification.

Source/visual and reproduction gates are bounded PASS; dimensional applicability remains replacement comparison; installed interface gate FAIL as quantified above; browser and production/load/contact calibration NOT RUN. The proposed interior refinement must preserve original tooth STEP hashes and exact external equivalence. Root and cover worker received these results. Canonical parts remain unchanged.

## Interior refinement delivery

Root's merged integration checkpoint is PR #94, commit `124aa7c345af352459a800343ffc50f1e931367c`; ongoing isolated timing work now resides on `engine/exhaust-timing-joints`. The timing study does not alter canonical741/1,349 geometry.

`timing_gear_pair_refinement.parts(frozen)` subtracts estimated shallow front web recesses, a crank keyway, and circular/triangular rim marks from the frozen original pair. All dimensions are in the refinement module's `PARAMS`; mark registration follows the hypothetical pair's reference mesh, not a claimed Ford key-to-mark angle. Material/color cues are illustrative. No matching crankshaft key/seat is supplied, and the old zero core-difference result is not reused for the revised key region.

`inventory/engine/timing-gear-pair-refinement-validation.json` **PASS interior refinement; inherited independent pair diagnostics; UNINSTALLED**, SHA256 `c5c6b5212b146b5bda89e854df1c38b7c4d1506199fb36f4a414097589edb19a`. Exact differences prove zero added solids and zero removed material outside radii37.05mm(crank)/77.65mm(cam), both below their tooth roots. Thus external tooth surfaces are unchanged; the original25pose sweep and two contact-bracket diagnostics are inherited by exact geometry and report hashes rather than rerun.

Both refined STEP exports are valid one-solid bodies; reopened GLBs are watertight without duplicate/degenerate faces. Maximum mesh/CAD bounds error0.011858mm; STEP volume errors below0.000000001mm³. Triangle counts6,864/9,372. Original exports remain frozen; new outputs are under `cad/engine/generated/timing-gear-pair-refined/`. Removed interior volumes are1,845.295746mm³(crank) and31,605.491218mm³(cam). Those modifications cannot establish installation compatibility; exact current-shaft/cover conflict numbers above describe the original pair and must not be quoted as rechecked refined values.

Reproduce:

```sh
XDG_CACHE_HOME=/tmp/truck-cache .venv-cad/bin/python scripts/check-timing-gear-pair-refinement.py
MPLCONFIGDIR=/tmp/truck-gear-mpl python3 scripts/render-timing-gear-pair-candidate.py --refined
```

Pure-CAD render `cad/engine/generated/timing-gear-pair-refined/pair-render.png` includes oblique/front views and a timing-mark detail. It uses backface culling and depth shading to clarify geometric recesses; colors do not identify production material. Worker directly compared actual exported geometry with the identified Elgin photograph. Root review of this refined revision is pending. Further work should establish a coherent cam/shaft/block/valvetrain datum proposal before any installation, and retain cover-worker coordination. No CAD process remains running at this checkpoint; usage/model-effort unavailable.

## Separate center-distance research lead

`reference/engine/timing-axis-datum-leads.json` records the Inliners 4.804-inch assertion (122.0216 mm by unit conversion) as an unverified forum lead. Post 83110 is dated November 17, 2014; repeat 83128 is the same author, not independent corroboration. No drawing, identified specimen, measurement method or uncertainty accompanies it. A bounded follow-up search recovered no applicable primary numeric datum. Search matches for Ford V8 timing chains, the 1963 Ford 300 vehicle model, and Model A block drawings are explicitly rejected by application. The frozen 121.8 mm candidate and manufacturer evidence remain unchanged.

The latest refined render was directly inspected after depth shading: both keyed bores, hub/rim shoulders and the circular/triangular marks are visible. Root was sent the render and passing refinement report for review.

## Scoped root refinement review

Root directly reviewed the refined `pair-render.png` and validation report SHA256 `c5c6b5212b146b5bda89e854df1c38b7c4d1506199fb36f4a414097589edb19a`. Hubs/recesses, keyed bores and paired marks were visible. Root accepts this isolated refinement for preservation, **not installation**. Dimensional/indexing estimates and unresolved shaft/cover interfaces remain; frozen proof files were not modified. Follow-on dependency and numeric feasibility studies are recorded separately in `timing-axis-migration-plan.md` and `timing-axis-kinematic-candidate.md`.
