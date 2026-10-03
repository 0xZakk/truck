# Carter-only pump registration and coordinated correction proposal

## Contract and scope

Issue47 / engine1, coupled cover issue32 and accessory ownership. Contributor pump_functional_junction; root integration owner. Started from baseline4f1fe9da2ec177e1ff61668df66ca422e37b0b7c on the existing focused branch. Before-work contract: `pump-source-registration-20261003-contract.md`. Research and read-only comparison only. No CAD, shared manifest, installed pose or frozen functional-delivery edits.

Frozen comparison: `reference/engine/pump-functional-20261003-delivery.json`, SHA2565003936ae17bc0aba6b4adcc3e3d360bc10050a420b614b229b47cec3228771f. Root preserved that failed candidate inPR122 during this research. Readiness here is **research**, not a geometry or installation pass.

## Evidence ledger and orientation

Primary source: [Carter W9046M product gallery](https://carterengineered.com/engine-water-pump-w9046m). All six full-resolution static views were independently inspected for this registration. BOT is the rear/impeller view; TOP is shaft-front; FRO/BAC/LEF/RIT are oblique views, not engine-world axis labels. Opposite ends naturally reverse apparent left/right. The page declares24turntable frames; this bounded task did not inspect all24 or run photogrammetry.

The BOT image SHA25681ad70c2137a4b0abf09176f2f43b173aebb799406258d59ebea04877bab0e27 is2000×2000pixels. Its four white apertures were recovered as connected components; fifth opening/shaft center were independently extracted in declared ROIs. Manual cuff/terminal/rim landmarks carry10–15pixel uncertainty. Thresholds, sample rows/columns, URLs and hashes are in the authored landmark ledger.

The candidate bolt pattern comes from approximate **Fel-Pro13816** photo ratios scaled to estimated centralR59, with Gates44009 topology comparison, as documented in `water_pump_gasket_topology_candidate.py` and `water-pump-mounting-topology-reviewed.json`. Thus this is cross-replacement proportional agreement, **not independent verified millimeter evidence**. No GMB silhouette or scale is used in this registration. Carter98.43mm mounting-to-hub reference remains applicable replacement evidence, but the rear image does not expose that axial distance and therefore cannot supply its own metric scale.

## Findings

### Camera roll explains the apparent port-direction discrepancy

Enumerating all24bolt correspondences under both proper and mirrored2Dsimilarities gives a clear best rear-view fit:

- Proper rotation **45.124°**, four-bolt RMS**2.302px**; mathematical rear projection is[-Y,Z] about shaftY−32/Z170.
- Mapped bolt1→photo bottom-right,2→bottom-left,3→top-right,4→top-left.
- Withheld fifth aperture residual**3.086px**, independently extracted shaft-center residual**4.555px**.
- Best mirrored fit has23.412px boltRMS and623.229px fifth residual. It does not explain the observed fifth-opening arrangement.
- An affine diagnostic reduces boltRMS to1.061px with axis-scale ratio1.01193 and fifth residual0.952px. This small flexibility is not proof of camera tilt or correct model dimensions.

The fitted5.196806pixels per **candidate-mm** is only a display conversion tied to estimated bolt coordinates. Do not publish it as a measured Carter scale. A perfect four-point projective fit would add no independent geometric validation and was deliberately not claimed.

Source inlet-axis angle is−4.510° after imageY is flipped upward; registered candidate is−4.876°. Robust near-root heater-axis angle is78.690° versus candidate80.124°. Their relative separation is**83.200° source versus85° candidate**. Ordinary heater least squares gives77.344° because the last sampled row meets the collar flare; all samples and both fits are retained. The robust method does not delete that observation.

Two thousand deterministic±2pixel perturbations yield roll44.845..45.410° and source relative-axis angle79.465..85.807°. These are sensitivity trials, not calibrated statistical confidence or bounds on perspective error. The evidence does **not** support rotating/mirroring the current ports merely because the unregistered render looks different. It also does not prove exact3D azimuth.

### The projected casting is narrower and shorter than Carter

The actual frozen housing GLB was projected with the selected bolt registration. Source outline samples at imageX1100..1600 were measured under four thresholds180/200/220/240; manufacturer pixels are not embedded in the distributable plot.

AtX1200, source casting span is**408px versus254.276px** for the candidate. AtX1250,400px versus251.493px. AtX1400,331px versus250.352px. Farther along the round neck atX1450,263px versus250.351px. Thus the clearest discrepancy is the broad **cast arm transitioning to the narrower round neck**, not a wholesale wrong port direction. The candidate's mostly circular/ruled arm lacks Carter's broad blended exterior.

Manual source rim radius from the registered shaft center is**1.184×** the candidate projected radius; the heater terminal radius is1.059× and visible cuff radius1.029×. Respective image residuals are144.762,105.710 and19.351px. They are projected extents with declared endpoint uncertainty and unknown axial parallax. **Do not multiply the physical inlet length by1.184 or enlarge every cross-section by1.6 from this one view.**

The Carter oblique views also show a continuously tapered/ribbed bearing tower and blended inlet casting. The candidate's long cylindrical nose and abrupt ruled transitions remain simplified. An applicable complete3D tower section has not been established.

A supplementary white-hole area comparison gives source equivalent radii about26.7–27.2px, while the candidateR4.3housing bore projects to22.35px and itsR5.2gasket opening to27.02px. This flags inherited housing-hole versus gasket-hole proportions for review. Obliquity, lip/through-hole distinction and threshold effects prevent turning it into an approved replacement bore size.

### Five clashes divide into two ownership problems

Read-only intersection of the already frozen overlap witnesses with declared pump regions gives:

| Frozen actualv4 pair | Total mm³ | Inside protected pump region mm³ | Consequence |
|---|---:|---:|---|
|Timing cover / housing|746.750|223.253 union; includes152.827 sealing backing|An inlet-only edit cannot resolve it while preserving the current sealing contract.|
|Timing-cover screw3 / housing|19.266|19.266, entirely lower dry boss1|Current fullR11.5boss and actual cover screw cannot coexist at these poses.|
|Thermactor engine bolt1 / housing|427.730|0|An unqualified inlet/bolt-route conflict; no permission to move the fixed anchor or sculpt a clearance pocket.|
|ALT/AP carrier / housing|3012.300|0|Source-compared inlet and explicitly estimated carrier require joint review.|
|ALT/AP carrier / heater tube|217.135|0|Axial tube route/carrier topology remains unresolved; the rear-view azimuth is broadly supported.|

Numbers may differ by a few1e−5mm³ from original reports due fresh adaptive integration of serialized witness solids. Full source/output hashes are recorded; no tolerance changed. “Outside protection” is a location classification, not permission to remove material.

The old `timing-pump-rear-flange-candidate` reduced a lower lug to an estimatedR8.75cap and trimmed a cover boundary atR66.25. It is **not a compatible drop-in fix** for the newer fullR11.5dry-boss contract. Its own gasket separation/tool-access failures also remain. Applying it silently would replace a declared interface and conceal that conflict.

## Coordinated correction proposal — before any geometry edits

1. **Freeze and reuse this registered rear-view evidence.** Preserve the current correct correspondence and relative port order. Use Carter-only oblique/side views with the same98.43mm product height to fit a bounded camera/profile model. First quantify projection sensitivity and rear-to-hub datums; then propose a broader cast inlet arm, distinct circular neck and more continuously tapered/ribbed tower. Keep every new section an estimate unless a dimensional source establishes it. Do not optimize that exterior against the carrier.
2. **Open a joint pump/cover contract revision for the lower mount region.** Required inputs are a re-registered applicable block-front/pump/cover-gasket pattern and sourced or explicitly estimated cover screw head/seat stack. Review which currently assumed quantity is wrong: full cylindrical boss envelope/depth, cover flange outline, relative hole registration or fastener axial stack. The source supports separate mating interfaces, but it does not validate all current millimeter constraints simultaneously. Preserve current regions as negative controls. Do not automatically choose the historicalR8.75cap or move the shaft/hole centers; issue a new explicit contract only after that source comparison.
3. **Rebuild the estimated ALT/AP carrier around source-supported pump context.** Carter currently indicates a broader/longer inlet silhouette, so shrinking the pump to clear the current carrier would worsen the source match. Retain actual engine/accessory anchor evidence and independently named support/head-seat regions; reconsider estimated ribs/bridges and attachment stack only with the carrier owner's source review. Thermactor bolt1 and its tool corridor must be included, not hidden by changing an arbitrary bolt length.
4. **Treat heater depth separately from rear azimuth.** Use same-product oblique views to bound tube axial arch/root depth before choosing a route; current rear angles are not a basis for swinging the tube away from the carrier. Preserve inlet/shaft/seal passages and collar engagement. Hoses/clamps remain separate missing components.
5. **Rerun joint acceptance on actual outputs.** Full named mating faces/backing, dry bosses/seats/bores, fifth route, true rotor sweep,98.43mm stack, walls/connected passages, real screw/tool corridors, final52-part export quality and all actualv4 affected pairs are required. Retain the spring mesh defect independently; a cast-body correction cannot mark it passed. No installation until combined/browser gates pass.

This proposal identifies the source-disfavored assumptions and the ownership boundary. It supplies no unreviewed replacement geometry, no source-certified new radius, and no claim that the five clashes are already resolved.

## Reproduction and review

Commands from repository root:

1. `.venv-cad/bin/python scripts/pump-source-registration-20261003-mesh-data.py`
2. `python3 scripts/pump-source-registration-20261003-measure.py`
3. `MPLCONFIGDIR=/private/tmp/pump-source-registration-20261003-mpl python3 scripts/pump-source-registration-20261003-plot.py`
4. `.venv-cad/bin/python scripts/pump-source-registration-20261003-clash-ownership.py`

The temporary directory is only a disposable font cache, never an input/artifact dependency. The CAD environment lacksPillow, so mesh extraction uses its existingtrimesh while systemPython supplies Pillow/NumPy/SciPy/Matplotlib. No package changes. Original gallery files can be reacquired through the recorded public URLs and must match captured hashes; they remain excluded from Git/releases. Authored landmarks/reports/plot and mesh projection arrays are reusable. Source input absence must be reported, not silently substituted with new pixels.

| Quality gate | Result and scope |
|---|---|
|Application/coverage|PASS bounded Carter replacement research; not owner-truck factory proof|
|Dimensions/coordinates|PASS pixel/normalized units and explicit mapping; absolute3D scale unresolved|
|CAD/export|N/A no new CAD; frozen failed candidate is read-only|
|Source/visual comparison|PASS bounded registration; broader3D source fidelity unresolved|
|Installed interfaces|FAIL inherited; read-only five-witness ownership classification complete|
|Motion/disassembly|NOT RUN; proposed next joint gates|
|Learning/diagnostics|N/A no new installed lesson; source distinctions in this handoff|
|Browser integration|N/A research only; installed component still requires it|
|Reproduction/review|PASS local rerun/hashes; root independent review pending|

Actual authored plot `reference/engine/pump-source-registration-20261003-registration.png` was inspected. It has no manufacturer pixels. No processes remain after freezing. Model/effort and usage unavailable. Issue47 remains active; root owns tracking, preservation and the next coordinated geometry assignment.
