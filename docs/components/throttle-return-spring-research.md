# Throttle return spring evidence and interface research

## Contract

Research-only preparation for component #43 under engine #1. Baseline commit `5567d751abcf6a9bfac84bdf87ce0d7f0d4dac5c`; exact candidate/source hashes in `reference/engine/throttle-return-spring-review.json`. Contributor: spring research worker; integration owner: root. Owned files are this handoff and the new review JSON only. No CAD or shared installation edits.

The question is physical spring count, configuration and stationary/moving anchors. Applicable factory drawings and the available public specimen do **not** resolve all three. Readiness remains research; do not infer two shaft springs from two coil-looking regions.

## Findings

Factory figures690090240 and690365451 show upper and lower coil-looking regions on the cable side. Figure689805816 separately labels a throttle plate set screw;690370320 establishes the opposite TPS side. These are perspective assembly views, not a spring exploded drawing. They do not trace each wire from one end to the other, expose both anchors or establish whether the regions are nested, divided, screw-associated or on different axes. Counting visible curved lines would invent a physical spring count.

The [F2TE-FA comparison photograph](https://i.ebayimg.com/images/g/-wwAAeSw4UtouIZQ/s-l1200.jpg) was reinspected. It shows a large coil bank, a bent external wire/leg, a smaller upper coil-looking region and adjacent stop hardware. Occluded endpoints remain ambiguous; exact1994 manual applicability is unverified. The [F2TE-EA MT listing](https://www.ebay.com/itm/257472725875) still could not be retrieved for image inspection. Other-engine/carburated procedures found in search were excluded.

New applicable evidence comes from the local [1994 cable Test C](https://charm.li/Ford/1994/F%20150%202WD%20Pickup%20L6-300%204.9L/Repair%20and%20Diagnosis/Powertrain%20Management/Fuel%20Delivery%20and%20Air%20Induction/Throttle%20Cable%2FLinkage/Testing%20and%20Inspection/Pinpoint%20Tests/Test%20C/): after disconnecting the cable from the body, it checks cable travel/return and a spring at the throttle-body end of the cable. That establishes a **separate cable-end compression spring function**. It does not establish the number of springs surrounding the throttle shaft. A cable spring must not be duplicated as a second shaft torsion spring merely to match an ambiguous illustration.

| Question | Evidence status |
|---|---|
| External cable-side coil topology | Supported by factory views and specimen |
| Exact shaft spring count | Unknown |
| Nested versus split versus separate-axis coils | Unknown |
| Cable-end compression spring | Supported separately by applicable Test C |
| Fixed/moving shaft-spring anchors | Endpoints occluded; production locations unknown |
| Wire diameter, turns, preload, rate, handedness and material | Unknown |

## Grounded candidate datum proposal

A future explicitly estimated spring study can use the existing Y-axis shaft at worldX394,Z490. This is a model-coordinate mapping, not a factory measurement.

Two material probes were checked against actual candidate CAD, without changing it:

- Fixed anchor candidate: world(389,104,503) lies inside the revised bracket web. A proposed seat on its inboard face is(389,103,503). It would require a new dedicated tang slot/hole, not an anchor suspended in air. This is below the shield ear'sZ508 lower edge and separate from the shield pushpin at(389,104,514). Slot size, local edge margin and spring route still need modeling/checks.
- Moving anchor candidate: local(0,65,18) lies inside the current lever plate. World position is(394,90,508) closed and(412,90,490) at the inherited90° pose. A future tang capture would need a new opening/tab and must remain distinct from the ball stud at24 mm radius. Containment establishes available material only, not strength or full clearance.

An exploratory coil region around that axis, Y94–101 and roughly7.5–10 mm radial distance, would be outboard of the hub/pin and inboard of the bracket web. These are **unchecked search envelopes**, not spring dimensions. A supported coil guide, actual wire profile, moving tang transition and fixed hook must be resolved together; fitting a decorative helix into this region would not complete retention.

## Dynamics and acceptance plan

The fixed tang must remain in `throttle-assembly`; the moving capture follows `throttle-moving`. The spring itself needs deformation or a justified analytical representation. Rigidly rotating the whole spring would move its fixed anchor and falsely suggest connectivity.

For an agreed candidate, check0–90° at2° increments, refining worst-gap regions. Verify both endpoints continuously remain seated, wire path continuity, approximately conserved wire length, coil spacing/self-clearance, guide clearance and no contact with shaft, retaining pin, lever, bracket, hood, pushpin or cable envelope. Winding direction must oppose opening. Preload and torque magnitude remain unknown; use no invented force or spring-rate calibration.

Negative controls should rotate the fixed anchor with the shaft, detach the moving tang, reverse torque direction and force a coil/hub interference. A rendered coil that moves smoothly does not establish reliable return against friction; physical return/strength claims require material and load evidence.

Before manufacturing-fidelity modeling, obtain views that expose both anchors and trace each separate wire. Record count, coil diameter, wire gauge, axial stack, winding direction and free/preloaded positions. Alternatively the integration owner may explicitly authorize one estimated educational spring abstraction, with the unknown production count prominently retained. This research does not itself approve that abstraction.

## Handoff and quality gates

Applicable source review and CAD material probes are complete. Production topology/count remains unresolved. CAD/export, motion, installed interfaces and browser checks are NOT RUN for a spring because no spring was authored. This is a justified research-only deliverable, not a failed or completed installed part. Root review is pending; issue #43 remains open.

The JSON contains exact repository-relative manual paths, SHA-256 hashes, specimen URL/hash, source conclusions and the datum proposal. Factory originals stay in ignored `manuals/factory-service-manual/`; discover them with `rg --files --no-ignore manuals/factory-service-manual`. Authorized archive access is a dependency; no original is redistributed. No temporary files are required for the findings, no posts/commits were made and no background process remains running. Model/effort and usage unavailable.
