# Airbox/body and paired-duct interface contract

## Contract

- Issue #80, engine air induction; worker `/root/inclined_linkage_resume`, integration owner root. Research-only delivery. No geometry, pose, manifest, source-original or frozen-candidate edits.
- Baseline at evidence review: `7f7788ce5d9b87865138f9fff412a5d023bfb369`; shared branch controlled by root. No manifest consumed or changed, so manifest hash is N/A. Prior candidate/interface input hashes are in `reference/engine/airbox-host-online-20261002.json`.
- Owned: that ledger, this contract, three `kb/sources/airbox-host-online-20261002-*` source pages and three same-prefix atomic notes. Source originals stay outside deliverables. No shared KB index writer run.
- Evidence level: exact-year Ford service architecture, manufacturer replacement screw dimensions and identified salvage shape comparison. Full bracket number, grommet construction, receiving clips and vehicle coordinates remain unknown.
- Units: millimeters/degrees. No new CAD origin, parent transform, world registration or explode convention. All proposed IDs below are reservations, not installed occurrences.

## Evidence and physical breakdown

| Interface or part | Supported fact | Source/class | Boundary |
|---|---|---|---|
| Box-to-bracket | Two N611062-S2 screw/washer assemblies and two base-17C431 grommets | Exact 1994 2WD 4.9 service figure 190226466, items 2–3 | No complete grommet number, seat dimensions or hidden sleeve asserted |
| Bracket-to-body | Four N610959-S2 screws; formed bracket base 9647 beside left fender/radiator support | Same figure, items 5–9 | Four screws are not four invented coordinate points; exact mapping to specimen openings unresolved |
| Body screw | Auveco 13019 cross-reference: tapping 6.3 × 1.81 × 19, washer-head OD 11.5, hex 8 | Manufacturer catalog printed 102/PDF 2, replacement | Point length, head height, root/thread profile and host pilot remain unknown |
| Bracket contour | Upright formed wall, bent slotted foot, box isolator stacks | Salvage listing 257361997805 photos 9/12/18 | Unscaled comparison; individual protruding studs not relabeled as the four service screws |
| Specimen identity | Molded E7TE-9643-CA-DA | Actual photo 24 | Engineering marking, not complete bracket service number or exact owner application proof |
| Two throttle joints | Full-circumference end seating on stop flanges; arrows align with locators | Service notes A/C | No actual stop location, cuff diameter or insertion distance given |
| Two lid joints | Hose arrows align with lid arrows within ±2°; four total clamps | Service note B/item 10 | No measured center spacing or angular installed frame |
| Fresh inlet | Base 9A675 feeds lower airbox, separate from paired clean-air 9R504 outlet assembly | Service items 1/8 | Source shape does not establish installed body clearance |

All URLs, original hashes and page/image locators are in the ledger. No pixel scale was inferred from a screw head: the visible hardware is not established as the catalog body screw in a coplanar view. The service figure's 1–2 N·m clamp annotation is not a bracket torque specification.

## Usable datum contract

Maintain three distinct frame families before any world placement:

1. **Body bracket:** identify the left-fender and radiator-support receiving surfaces, their normals and all four fastener axes. The specimen upright return and bent foot are candidate surface families, not solved coordinates. Supply at least three noncollinear metric body reference points and the corresponding bracket reference points; then solve and report the rigid transform and residuals. Do not fit a bracket by moving the airbox until hoses look plausible.
2. **Isolated box:** identify both grommet axes, upper/lower bearing faces and the box/bracket stack. The box rests through these compliant joints. Two axes alone do not establish all rigid-body orientation without a seat plane/clock datum. Unknown grommet compression and construction must remain parameters.
3. **Four duct ends:** name throttle stop planes `T1/T2`, corresponding axes and locator rays; name lid mouths `L1/L2`, insertion seats and arrow rays. Tube correspondence must be traced through an identified assembled specimen, not selected to minimize bend. Require full annular seating at both throttle stops and source clock agreement. Lid insertion depth and actual cuff dimensions remain unsolved. Preserve separate lumens, four clamps and the independent fresh-air inlet.

The inherited candidate values are explicitly **CAD estimates**: box local tips X −198, Y ±37, Z 30, OD/ID 60/54; throttle canonical/v3 world tips X 255.5, Y −2/+52, Z 490, OD/ID 48/40. They are retained only as a record of current interfaces. Neither they nor the refined free-state duct specimen solve physical mating or box world pose. Engine movement relative to the body-mounted box needs a later flex envelope; no travel range is sourced here.

## Supported next model step and guardrails

After root review, an isolated N610959-S2 replacement-envelope component is independently buildable with the five catalog dimensions; head height, point geometry and exact thread profile must be estimated or omitted explicitly. Proposed definition `air-cleaner-body-bracket-screw`, eventual four occurrences. Do not call an approximate thread manufacturing-accurate or install it in guessed pilot bores.

The next bracket study can encode formed topology and separate `air-cleaner-box-mount-grommet` (2), `air-cleaner-box-mount-screw` (2) and `air-cleaner-body-bracket` (1) identities. Detailed metric/installed geometry is gated on an applicable bracket drawing or public donor photographs with a ruler in each mounting plane plus orthogonal views. A body-hole diagram or identified donor body measurement can supply registration without owner photographs. Current unscaled photos improve decomposition but do not justify that transform.

Explicit rejected transfers: 1996 California automatic single-duct/MAF architecture and three-mount counts; 1996 F350 F6TZ9647EA identity as proven 1994; catalog M6.3 tapping fastener as M6 × 1 machine bolt; 19 mm body-screw length assigned to N611062 box screws; seller package dimensions as a part drawing. No neighbor cut or eye-placed installation is proposed.

## Delivery and validation

- Readiness: research/interface contract for review, not CAD or installed acceptance. No submitted commit/PR; root owns integration. No active process.
- Parametric API, STEP/GLB, renders, asset release: N/A, no geometry built. Source pixels were inspected directly; no source images redistributed.
- Evidence capture: public catalog downloaded using HTTP/1.1 after an HTTP/2 transport failure; Poppler text extraction and PDF page-2 raster inspection succeeded. Direct PDF ingestion lacked `pypdf`; bounded authored observations instead passed through `python3 tools/ingest.py <observations.txt> --type local --title 'Airbox host online 20261002 observations'`. Raw capture is ignored and excluded. The repository source pages contain the reusable derived facts and original locators; no temporary path is a required downstream input.
- Environment: macOS, system Python/Poppler. Model/effort and billing unavailable. No CAD runtime used.

| Gate | Status | Evidence and limit |
|---|---|---|
| Application/coverage | PASS scoped research | Exact-year diagram distinguished from later automatic variant and seller comparison |
| Dimensions/coordinates | PARTIAL | Five replacement screw dimensions; body/cuff coordinates unknown |
| CAD/export | N/A | No model |
| Source/visual | PASS scoped observations | Actual service/catalog/salvage pixels; no render comparison required for research |
| Installed interfaces | NOT RUN | Unsourced metric host frame; installation forbidden in this delivery |
| Motion/disassembly | NOT RUN | Body/engine flex and service removal not modeled |
| Learning | PASS content/links | Three source pages, three atomic notes; no unsupported repair thresholds |
| Browser | NOT RUN | No runtime integration |
| Reproduction | PASS scoped metadata | Input hashes, public locators and applicability preserved; exact-year mirror availability is not guaranteed |

Negative controls are source distinctions, not automated solid checks: reject swapped box/body screw identity, reject M6 × 1 substitution, reject later single-duct figure for target counts. Root review pending. No previous geometric checks are invalidated. Issue #80 remains open; next action is review this contract, then authorize the isolated screw envelope or acquire donor/drawing mounting data. No additional modeling begins automatically.
