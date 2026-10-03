# Pump/cover candidate: deck datum amendment

Research amendment under engine #47/#32, parent #1, reviewed numerically by integration owner root on 2026-10-03. Resume baseline `5584306a595f87b60b29eca9ea82b527ade5ae98`, branch `engine/resume-integrations-20261003`. Candidate geometry and option B datums remain frozen; this document does not authorize a new integrated pose.

The upper screw center is Z260.259 mm, above the existing block deck at254. New independent gasket backing and block supports extend toZ279.711. They add10,904.370mm³ of block/head interference and1,034.479mm³ with the head gasket; these were zero before the feature replacement. The head/outlet conflicts therefore expose a bad joint registration assumption. Removing overlapping land, thinning the full dry boss, moving only the outlet, or changing the head height would conceal this conflict.

Ford's manufacturer reference now independently supports the nominal deck: the `300 I-6,1965–96` row gives10.000in=254mm. The source URL, download hash, PDF page, full nominal row and applicability limits are preserved in `kb/sources/pump-deck-height-20261003-ford-nominal.md`; its atomic note is `kb/notes/pump-deck-height-20261003-preserve-nominal-deck.md`. Actual PDF raster and column alignment were inspected. The table contains no production tolerance. Raw PDF/pixels remain excluded.

## Held-out source observations

`reference/engine/pump-cover-candidate-20261003-deck-registration.json` freezes manual seam, pan and outlet-aperture observations on the already identified ATK DFF8 front photograph. The visible head/block seam is above the fifth opening and top pump screw. Root separately inspected the local source overlay and considered its identification plausible. Exact coplanarity and recess depth remain unknown. The source is an applicable replacement-family photograph, not the owner's engine.

The unchanged source homography maps the seam to meanZ289.84487 and pan points to approximately−24.48. Its normalized matrix condition number is7.81686; local inverse-Jacobian metrics, original training RMS1.0409px, fifth held-out error2.0415px and leave-one-cover-out errors are recorded. No new landmark refits the camera. A20px seam shift is a sensitivity control. Two thousand independent±3px picks quantify only selection sensitivity under the frozen camera, excluding source-pattern/depth/scale/systematic uncertainty.

A **conditional sensitivity hypothesis**, fitting a uniform coupled source footprint to deck254 and the inherited pan−24.5, yields scale0.88602454 relative to option B and Ztranslation−2.809667. Root explicitly declined to treat the unverified pan datum as sufficient calibration. It also gives a−7.2126mm sampled cam-plus-wall outer-arch margin. This is the same360point ring/45point outline screen as the earlier options, not a fresh CAD collision check. No shaft, gear, hardware, spring or seal geometry may be scaled to make this hypothesis fit.

## Next source-led remedy

Establish a coplanar crank or seal-axis datum independently, then combine it with Ford's nominal254mm deck and a checked block-front mounting pattern. Refactor the common source registration only after that evidence review. Preserve actual crank/cam axes, gear diameters and mechanical relations as separate constraints; report any contradiction rather than hiding it in the pump shell. A dimensioned gasket/cover drawing or bare-front photograph with an unambiguous machined crank-axis feature is preferable to forward gear hubs.

The second-source search located Jackson Campbell/trozei's bare C6AE block photograph at `https://i.imgur.com/INqRtLh.jpg`, linked by the builder's2014-12-08 post at `https://www.fordification.com/forum/viewtopic.php?start=15&t=77609`. It corroborates front architecture but exposes only a dark partial crankcase arch and recessed main saddle; no unambiguous coplanar crank center was accepted. Earlier engine-family transfer is also limited. Four seller photographs of an1987 bare block (`https://www.ebay.com/itm/125120295193`) show underside/recessed saddles and were rejected for front-plane calibration. These negative findings prevent a future worker from confusing search captions with dimensional evidence.

## Reproduction and disposition

Run `python3 scripts/pump-cover-candidate-20261003-deck-registration.py`, then `python3 scripts/pump-cover-candidate-20261003-resume-audit.py`. Matplotlib/NumPy are required. The authored observations and committed reports suffice without source pixels. If the original hash-matched ATK image is present, the script additionally creates ignored `cad/engine/generated/pump-cover-candidate-20261003/deck-source-overlay.png` for local review only. **Exclude that overlay from release archives** because it contains seller pixels. The committed three-panel figure contains only authored landmarks and actual candidate STEP display triangles.

Readiness remains candidate FAIL, issue open. No coupled CAD or shared assembly changes in this amendment. Root owns shared KB semantic/index updates and GitHub issue/PR integration. Model/effort/usage unavailable. See the full candidate handoff for the remaining flow, source exterior, accessory, motion and browser gates.
