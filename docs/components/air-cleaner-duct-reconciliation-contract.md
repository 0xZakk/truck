# Air-cleaner duct reconciliation contract

Engine #32/#80, root integration owner. Own this handoff and `inventory/engine/air-cleaner-duct-reconciliation-contract.json`. No existing airbox, throttle, source, manifest or geometry changes. Exact baseline and dependency hashes are in the JSON.

**Installed duct CAD is not yet justified: the airbox-to-vehicle transform is unknown.** The frozen four-part candidate explicitly has no body placement or bracket. Canonical andv3 contain neither an installed box nor a body frame that locates it. Building tubes now would silently choose a box pose from routing convenience. This delivery therefore supplies the required vehicle-interface contract before CAD, as directed.

## Actual endpoint evidence

The candidate source and actual exported STEP end faces were inspected. These dimensions describe current estimated CAD, not Ford measurements.

| Owner / face | Frame and axis | Current dimensions |
|---|---|---|
|air-cleaner-twin-outlet-cover-candidate, two outlet tip annuli|Box-local tip planeX−198, centersY−37/+37,Z30; outward−X|OD60, lumen54, spacing74mm. Each actual tip face537.212344mm². BeadOD64 atX−192..−189.|
|throttle-housing, two inlet tip annuli|DefinitionX422.5,Y−2/+52,Z490; outward+X. Parent−167X makes world tipsX255.5 in canonical andv3.|OD48, lumen40, spacing54mm. Each actual tip face552.920307mm².|

The airbox local origin is filter-seal top center; X is long side, Y width, Z up. **Identity is not an installed box transform.** The box and throttle dimensions differ intentionally as inherited estimates. A future duct must transition, rather than force equal bores or move either owner to make its ends meet.

The current throttle has straight cylindrical mouths. The exact-year requirement to seat the hose around the full stop flange does not establish a near-mouth stop plane or valid insertion length in this model. The inlet tip annulus is not automatically a hose stop. Existing box beads provide a modeled retention feature, but their dimensions and the required insertion beyond them remain estimates. Clamp widths, closure mechanisms, clocking and contact compression are unknown.

## Source appearance and topology

Actual owner driver/passenger photos, exact-year drawing190226466 and the preserved actual airbox candidate render were compared. The broad rectangular box, paired circular exits and two partly corrugated flexible tubes agree qualitatively. The source supports four clamps and two distinct end interfaces per tube. It also shows body-supported box/bracket context and orientation/stop seating requirements. The render contains only box/filter/seal; it cannot prove installed routing or hose appearance.

Existing source views do not establish tube centerlines, bend radii, rib pitch/count, wall thickness, exact box pose or clearance under engine movement. The owner's view locates the assembly broadly on the driver side but is uncalibrated and partly obscures the endpoints. No source images were copied into deliverables. Refer to `reference/engine/air-cleaner-candidate-review.json` and the previous exterior audit for bound source identities.

## Proposed vehicle interface before modeling

Root should establish the following shared contract, leaving unresolved values null rather than selecting plausible defaults:

1. **Box rigid frame:** body mounting anchors on the left fender/radiator-support bracket, tied to the existing engine frame. Three noncollinear anchor coordinates or an equivalent six-degree-of-freedom survey; lid clocking and outlet pairing explicit. A measured replacement bracket/box can define a comparison; exact installed placement still needs vehicle registration.
2. **Throttle seating frame:** actual or explicitly estimated full-circumference hose-stop shoulder, insertion length and host sealing cylinder. Any throttle feature correction is a separate coordinated change; preserve throttle/intake position and bore interfaces.
3. **Box seating frame:** insertion length relative to tip/bead and lid wall, plus assigned tube correspondence. Preserve the frozen box unless a separately reviewed interface correction is needed.
4. **Flexible path and clamps:** source-supported route family with stated estimated bends/corrugations; nominal wall and endpoint transition, four clamp locations/type/width and sealing/retention model. Do not use a cosmetic exterior rib to stand in for a continuous duct wall.
5. **Body/engine relationship:** surrounding body, hood, booster and hose boundaries plus declared relative engine movement. A static fit is not a proof that a body-mounted airbox can follow engine motion without strain or contact.

An explicitly estimated body pose could support a separate educational proposal only after root accepts its evidence and uncertainty. This contract proposes the required fields, not a numeric pose or automatic authorization to install a guessed box.

## Future candidate gates

Once endpoints are accepted, build two distinct ducts and four separately identifiable clamps with stable proposed IDs `air-cleaner-outlet-duct-1/2` and `air-cleaner-outlet-clamp-1..4`. No IDs are installed now. Keep smooth endpoint sealing bands; show inferred flexible sections separately from source-supported topology.

Require continuous lumen through both transitions/bends; minimum wall checks using independent sections and boundary probes; complete circumferential end backing and declared insertion contact; clamp-band support; actual STEP/GLB validity and frame checks; and actual source-view render. Wrong endpoint, blocked lumen and locally thinned-wall controls must fail. Check real engine neighbors at the fixed accepted frames and explicitly list missing body neighbors. Continuous engine/body motion needs its own declared range; no arbitrary clearance carving or endpoint movement.

## Delivery and restart

Contract only. Local STEP face dimensions PASS as measured model facts; source topology comparison PASS qualitatively. Vehicle placement, insertion/sealing and installed neighbor gates unresolved. Duct CAD/export/motion/browser NOT RUN because the prerequisite frame is absent. No new CAD module was created to conceal that gap.

Reproduce endpoint inspection with build123d import_step of the two bound STEP files, selecting planar faces atX422.5 for throttle andX−198/−192/−189 for lid; compare bounds and areas in the JSON. The model source supplies the cited radii and local frames. Verify hashes before reuse. Root review pending; next action is body-frame and hose-stop definition, not a corrugated tube generation cycle. No running process; usage unavailable.
