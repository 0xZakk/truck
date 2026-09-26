# Throttle linkage research and next modeling contract

## Contract

Research preparation for [component #43](https://github.com/0xZakk/truck/issues/43), engine parent #1. Baseline commit 24a023b5313bda64a50f0a36356220f05a731eb8; current read-manifest hash and source hashes are recorded in `reference/engine/throttle-linkage-review.json`. Contributor: bracket/linkage research worker; integration owner: coordinating agent. Owned files are this handoff and that new review JSON only. No current CAD, assembly, bracket or validation reports were changed.

Scope is evidence discovery and a concrete interface proposal for the lever, return spring and plate fasteners. It does not authorize declaring the assembly complete. Critical dimensions, spring preload, stops, screw count and exact 1994 manual specimen identity remain unresolved.

## Findings and evidence limits

The [1994 factory service procedure](https://charm.li/Ford/1994/F%20150%202WD%20Pickup%20L6-300%204.9L/Repair%20and%20Diagnosis/Powertrain%20Management/Fuel%20Delivery%20and%20Air%20Induction/Throttle%20Body/Service%20and%20Repair/) establishes a cable ball stud, a linkage shield, throttle/speed-control cable connections and shared bracket/body retention. It does not reveal spring retention or the number of butterfly screws. Its [linked diagram](https://charm.li/images/DM05Q313/ford10/690090240/) was subsequently found and visually inspected in the local factory archive; the initial web failure is superseded by the local review below.

The exact-manual research lead is [F2TE-EA specimen listing 257472725875](https://www.ebay.com/itm/257472725875), titled 1992–96 F150/E150 4.9 MT. Its gallery was inaccessible in this session, so its 8 listed images have not been inspected. Seller applicability is not a verified engineering interchange. A [dealer catalog comparison](https://www.oemfordpartsoutlet.com/v-1996-ford-e-150-econoline--xl--4-9l-l6-gas/fuel-system--throttle-body) distinguishes manual/C6 service assembly F6PZ-9E926-GA from E4OD F6PZ-9E926-DA; that 1996 E150 indexed page is insufficient to certify an exact 1994 engineering number.

Two public specimen photographs were actually inspected, and their direct URLs and hashes are preserved in the review JSON:

- [F2TE-FA comparison photo](https://i.ebayimg.com/images/g/-wwAAeSw4UtouIZQ/s-l1200.jpg): a formed lever carrying an outward ball stud sits beside a coaxial coil spring bank. A bent wire leg runs beside and around this region, but its hidden endpoints prevent determining both retention points. A stop screw sits on an adjacent casting pad. The black sensor/connector occupies the opposite shaft end. The seller's 1993–96/4.9 title does not establish manual applicability.
- [F2TE-MA rear comparison photo](https://i.ebayimg.com/images/g/FdUAAOSwtF1l9dRD/s-l960.jpg): two screw-head-like features are visible on the right plate and one clearly visible at the inner side of the left plate. The remaining area is too dark to establish total count. Do not record three as a production quantity or silently assume four. The listing's broad 1987–93/4.9/5.0/5.8 claims make this a topology comparison only.

The local factory review below adds applicable topology and service identities. No source-supported production dimensions were recovered. The number of nested springs, coil turns, tang anchors, lever-to-shaft retention, plate-screw size/spacing/staking, bushings/seals and angular calibration remain unknown. Older carburetor and other-engine spring/screw procedures found in search were excluded.

## Concrete next-round component breakdown

| Proposed item | Physical interface | Evidence/readiness |
|---|---|---|
| Throttle lever | Rigid attachment to shaft's cable-side end | Factory and specimen views support formed lever topology; contour and retention unknown |
| Cable ball stud | Lever to cable socket | Applicable procedure supports existence; size and whether integral/separate unknown |
| Coaxial return spring(s) | One stationary anchor and one moving lever anchor | Factory coil-bank topology; quantity and tang retention need better views |
| Stop screw/contact | Stationary casting seat against moving lever | Factory set-screw label and preset WOT stop; calibration unknown |
| Butterfly screws | Through each plate into shaft | Count/spacing not verified; four-instance candidate would require explicit inferred-count designation |
| Linkage shield | Stationary guard around moving cable hardware | Factory shield9E766 and pushpinN804527-S; contour/attachment dimensions missing |
| Speed-control attachment | Second cable interface where fitted | Procedure lists connection; owner equipment and lever details need confirmation |

Use the existing `throttle-moving` frame at world (394,25,490), with Y-axis shaft. Its current local ends Y±62 are world Y−37/87. Reserve negative Y for existing TPS and propose positive Y for lever/spring, consistent with factory and comparison topology but still an inherited installation estimate. Parent lever and plate screws under the moving group; keep casting anchors and shield stationary. A deforming torsion spring needs separate stationary/moving endpoint constraints, not a rigid rotation with the shaft.

Current plate centers are world Y−2/52, and the closed plate normal is approximately X. Screw bores should be solved through actual plate/shaft solids after selecting an explicitly classified spacing/count. Current bracket cable-hole centers are roughly X465,Y110,Z467/488. These are estimates, not measured cable endpoints; do not use them to invent lever arm length or bend cables until they appear connected. Agree shaft end, lever plane, ball-stud path and fixed housing-exit datums together before detailed geometry.

## Acceptance plan and handoff

The next modeling task must first obtain exact-variant front/rear and both shaft-end views with a scale; count every plate fastener; identify both spring tang anchors; and distinguish throttle/speed-control attachments from automatic-transmission controls. If unavailable, explicitly bound the next deliverable as an estimated educational mechanism.

Required checks: lever-to-shaft connection; screw clearance and nominal engagement; stationary spring anchor and moving tang continuity across travel; contact at modeled stop endpoints; plate/casting and linkage/shield sweep; cable alignment with fixed housing seat. Include disconnected-lever, wrong-spring-anchor and shifted-screw negative controls. Existing idealized 0–90° motion is not verified production travel.

| Quality gate | Research-stage outcome |
|---|---|
| Application/coverage | Applicable factory procedure and drawings reviewed; exact-manual specimen gallery unavailable |
| Dimensions/coordinates | Proposed inherited frame documented; production dimensions unknown |
| CAD/export and installed interfaces | N/A: this assignment creates evidence/contract only, no geometry |
| Source/visual comparison | Nine applicable factory/TSB figures and two specimen photographs inspected; exact-manual specimen comparison NOT RUN |
| Motion/disassembly | NOT RUN; explicit next-round constraints above |
| Learning/diagnostics | Function and source limitations recorded; no repair adjustment specification supplied |
| Browser integration | N/A for research-only files |
| Reproduction/review | JSON stores source URLs, image hashes, observations and local input hashes; root review pending |

Public specimen images were inspected transiently and are not redistributed. Another reviewer can fetch the direct URLs and verify hashes; observations survive without temporary files. No purchased manual originals, owner photographs, external posts or commits were created. Readiness remains research; issue #43 stays open. Next action: review the source ledger, resolve exact specimen and spring/fastener gaps, then assign a separate bounded modeling contract. Model/effort and usage unavailable; no background research process remains running.

## Local factory archive review: supersedes web-image gap

The ignored archive was discovered with `rg --files --no-ignore manuals/factory-service-manual`. Its vehicle root is `manuals/factory-service-manual/1994 Ford F 150 2WD Pickup L6-300 4.9L/`; diagram paths below are under `images/DM05Q313/ford10/`. Authorized access to this uncommitted archive is an explicit review dependency. The JSON records every inspected image and relevant HTML SHA-256; no manual original was copied into Git.

- `690090240.png`, `690365451.png` (V5652-D), and `690370320.png` (V5942-F): factory throttle service views show the lever/coil spring bank opposite TPS9B989, with separate IAC. V5652-D explicitly calls out four mounting nuts; this does **not** establish butterfly screw count.
- `689805816.png` (V4752-G): labels the throttle plate set screw, TPS9B989, IAC9F715 and canister purge ports. The description text establishes a preset WOT stop. Do not confuse the external set screw with screws retaining plates to the shaft.
- `692036165.png` (V6832-F) and legend `692057936.png`: the main cable diagram includes manual, C6 and E4OD applications. ViewY depicts bracket9728 and stationary splash shield9E766 with pushpinN804527-S. ViewZ is explicitly C6-only: kickdown control shaft rod7A187 and gearshift inner bracket7C431 must not be added to the manual truck from that inset.
- TSB94-15-16 (1994-07-27), images `693289419.png`, `693295768.png`, `693298821.png`: diagnosis separates pedal/cable restriction from throttle-body restriction by disconnecting the cable for checks. The service page also requires unobstructed return to idle through slow pedal release from WOT. These support meaningful motion/return checks, not a guessed production spring specification.

Factory drawings strengthen the side/topology assignment and shield breakdown. They do not establish spring quantity, both tang anchors, preload, turn count, plate fastener count or dimensions. The positive-Y lever plan remains a mapping into the existing estimated CAD frame, not a coordinate measured from a factory drawing. Exact manual specimen views are still needed for spring retention and butterfly hardware.
