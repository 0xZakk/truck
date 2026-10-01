# Component contract and handoff: waterpump-heater-route-evidence

## Contract

Issue32/47 cooling interface. Worker pump_foot_resume; root integration owner. Read-only source/datums reconciliation following frozen heater-route FAIL. Own only new waterpump-heater-route-evidence files. Preserve candidate STEP/GLB, private v3, all five actual route conflicts and main3 failure; no new CAD. Baseline e6dc8fcd68e28ff201ee2cd9b69aee0bb8a588eb and v3 SHA f512d6024ed4d3d0d86c45c39492b4ab525e039a9c50fb71b67940633b8a2055.

Questions: whether source tube identity is mistaken; whether side photo gives worldX; whether owner photos identify the full tube route; whether a source-supported replacement route exists. Review actual three Gates44009 product images, primary Gates2011 catalog and both authorized owner bay photos. Source originals remain excluded from redistribution. Report photographed topology separately from inferred dimensions and camera assumptions.

## Findings

The long formed tube is genuinely shown on Gates44009 in the manufacturer's own2011 catalog, printed289/PDF309 (top-left product). It is not just a mislabeled loose pipe in the retailer gallery. The manufacturer application table lists44009 for1993–1996 Ford F-series4.9L; this supports replacement applicability, not the owner's exact installed specimen or a dimensioned tube route. The catalog shows two bends and a long terminal portion. It does not specify axial reach, clocking, tube dimensions or flange-to-hub dimensions.

The frozen candidate converted one side photo's vertical image coordinates directly to worldX by mapping rear plane375 to hub518. That conversion silently set both radial contributions to the vertical projection to zero. An uncalibrated oblique camera generally gives image position = aX+bY+cZ+translation (and perspective adds depth-dependent scaling). The hub face and rear/impeller shapes are visibly oblique; the heater tip lies far from the shaft axis, so its radial projection can contaminate the inferredX. The retained143mm hub/rear span is itself estimated geometry. RootX409 and endpointX236 were study parameters, not identifiable measurements.

An independent catalog photograph gives a different result under the *same inadequate image-up calibration*: approximately rootX416/tipX329, compared with retailer rootX409/tipX236. That93mm endpoint disagreement is evidence against using either conversion as a unique3D route. Catalog rear-plane pixel selection is partly obscured and approximate; no new authoritative endpoint is inferred from it. The interval between these two numbers is a photographic-estimator spread, **not** a conservative physical envelope, confidence interval or manufacturing tolerance.

Correctly handed front/rear registrations agree on the visible root localYZ within0.60mm in inherited model scale, but their tube-tip projections differ by about52mm. Thus the root sector128.3–128.7° and initial stem sector144.0–146.7° are better supported than the entire centerline. Keep the radial root angle distinct from the tube tangent. Pixel uncertainty, perspective, specimen/camera differences and axial parallax remain unresolved; averaging two projected tips cannot triangulate a physical point.

Both owner bay photos were re-viewed. They show paired red/orange hoses running from the firewall toward the engine front, with short exposed metal portions near the front. The fan/shroud, hoses and upper engine obscure the pump's casting insertion and complete formed tube. Neither view allows a reliable one-to-one trace from a particular hose to this pump boss or a measured rearward tube reach. They do not validate either the old boundary(438,−132,270) or the failed new boundary(236,−171,415). No pump/stem identity is assigned solely from hose color.

## Decision and next contract

No new route is sufficiently constrained for CAD in this task. Preserve the stronger root/interface evidence separately; preserve the five whole-engine route conflicts as physical failures. A shallower-backward tube is a source-consistent **hypothesis to investigate**, not an approved correction or a claim of clearance. Its actual terminal pose and intermediate bends require either identifiable assembled pump/tube source imagery, calibrated multi-view imagery with shaft/flange datums, or physical tube/flange measurements. No neighbor may be moved or carved to force this uncertain route to pass.

A future contract should jointly fit all available source views using explicit camera nuisance parameters, retain known pump mounting/shaft datums, and report an ensemble of possible3D routes before selecting any candidate. Current images do not support a finite guaranteed physical ambiguity envelope. The report therefore records the observed estimator spread and marks the physical envelope UNKNOWN. Vehicle heater-hose routing remains a separate missing interface.

## Reproduction and validation

Run `python3 scripts/waterpump-heater-route-evidence.py`; source-only diagram and hash-bound report use the same prefix. Manufacturer PDF is `reference/engine/research-2026-09-23/gates-water-pumps-2011.pdf`; inspect printed289/PDF309 with `pdftoppm -f 309 -l 309 -png`, and optionally inspect its first embedded image using `pdfimages -f 309 -l 309 -png`. No source original is copied to deliverables. Gates catalog URL: https://cms.gates.com/~/media/Files/Gates/Industrial/Fluid%20Power/Catalogs/Water%20Pump%20Catalog%20Full%20Version.pdf . Application text uses printed35/PDF55; product photo printed289/PDF309.

Source/application/topology review complete with replacement limits; dimensional route UNKNOWN; installed fit remains frozen FAIL; CAD/export/motion/browser N/A because this is a read-only evidence audit. Source-only diagram reviewed separately; Python/system NumPy/Matplotlib, no CAD changes. Root reviewer owns next routing decision. Usage unavailable. No background process after delivery.
