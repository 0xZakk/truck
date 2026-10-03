# Intake joint coordinated correction plan

## Contract

- Issue #82 source/host discovery, intake dependency under engine #1. Integration owner: root; contributor: act_second_view. Research only; no CAD or installed approval.
- Baseline `4f1fe9da2ec177e1ff61668df66ca422e37b0b7c`, branch `engine/source-host-interfaces-20261002`. Actual manifest and inspected code hashes are bound in `reference/engine/intake-joint-layout-20261003-scope.json`.
- Owned files: this prefix only in docs/components, reference/engine and scripts. Shared builder, manifest, historical fixtures, KB maps and Git belong to root.
- Inputs: frozen second-view casting, failed registration and independently identified MS93838 gasket packages. Source originals remain excluded; source URLs/hashes and restoration are in those packages. No new source pixels or dimensions were obtained in this phase.
- Objective: implementable coordinated six-port/nine-aperture layout contract, stable repeated-ID correspondence, dependencies and unresolved dimensions. Not a new camera fit, ACT host axis, nine-fastener claim or factory scale derived from the old pitch.

## Evidence and dimensions

Manufacturer Fel-Pro catalog PDF354/printed328 identifies MS93838 upper plenum gasket for 4.9 MFI VIN Y 1991–97; PDF305/printed279 covers 1994 F150 VIN Y. Identified retailer product pixels show six ports and nine small apertures. The source photograph is a replacement comparison, not a dimensioned drawing. Frozen `intake-joint-online-20261003` evidence carries URLs, exact SHA-256 and per-feature extraction.

The terminal short gap divided by the other four mean gaps is 0.893410–0.894019 across accepted extraction thresholds. This narrow interval describes extraction repeatability, NOT full accuracy. Perspective, lens, reproduction stretch, part variation and replacement-to-casting transfer are unbounded systematic errors. Use 0.89 as a source-compared approximate ratio; never interpret the reported decimals as manufacturing tolerance. No trustworthy absolute span, port diameter, hole diameter, flange thickness or ruler was located. The former 113.792 mm equal pitch is an existing model parameter, not factory scale for this joint.

Normalized reference coordinates are in the scope JSON. P1 is the short-gap terminal port, provisionally ACT/front by casting comparison; P6 is the other end. Datum u runs P1→P6. Datum v is the image-derived perpendicular; its mapping to engine Y requires face-side registration. Under the proposed engine convention, u maps to -X, joint normal to +Z. This is an explicit proposed frame, not a solved registration. Set `world_origin_mm`, `absolute_span_mm`, diameters and gasket thickness only from new metric evidence or a separately reviewed educational estimate. Keep those unset now. Formula after review: `world_point = origin + L*u*(-1,0,0) + L*v*(0,signY,0)`, with a separate Z offset for each mating surface. Preserve millimeter units after L is assigned. Do not choose signY, scale, or origin to improve neighbor clearance.

## Stable feature and occurrence correspondence

P1..P6 and H1..H9 are feature labels, not new physical part IDs. Existing castings each remain one occurrence; the gasket remains one occurrence. Associate P1..P6 with runner 1..6 only after confirming short-end identity. Head-port and injector numbering remain their current front-to-rear order; reshaped lower runners connect those fixed head stations to the revised joint stations.

| Existing occurrence | Proposed feature slot | Remaining correspondence issue |
|---|---|---|
| efi-upper-stud-1 | H1, front terminal ear | end/face registration |
| efi-upper-stud-2 | H2, between P1/P2 | end/face registration |
| efi-upper-stud-3 | H3 OR H4, between P2/P3 | which hole is retaining stud; other role unknown |
| efi-upper-stud-4 | H5, offset between P3/P4 | end/face registration |
| efi-upper-stud-5 | H6 OR H7, between P4/P5 | which hole is retaining stud; other role unknown |
| efi-upper-stud-6 | H8, between P5/P6 | end/face registration |
| efi-upper-stud-7 | H9, rear terminal ear | end/face registration |

This is a concrete seven-slot hypothesis, not a verified bolt/dowel assignment. Preserve definition `efi-upper-stud` and all seven occurrence IDs/parent `intake-studs`. Do not create two more studs or delete the two apertures. Visible casting protrusions are insufficient to classify their retention/construction. The existing `intake-head-locating-dowel` is at the HEAD↔LOWER joint; it cannot resolve the two upper-joint extra apertures.

## Exact downstream geometry scope

1. `efi-lower-intake`: replace upper flange outline, six upper port mouths, connecting runner paths, seven confirmed fastening bosses/bores and the two extra aperture interfaces when identified. Preserve head face/ports, injector seats and rail mount datums as explicit protected geometry. Lower base currently connects head stations `(x-25,-140.5,277.5)` to equal upper stations `(x,-228,355)` in `cad/engine/efi_intake.py`; endpoint correction cannot be performed by translating the whole casting.
2. `efi-upper-intake-gasket`: regenerate one connected gasket with six ports and all nine observed small apertures, shared XY with both castings. Existing 734×56×1.5 mm strip, circular openings and seven inline bores are provisional; thickness remains unknown. Port and hole diameters must be independent parameters, not copied from image pixels as exact mm.
3. `efi-upper-intake`: regenerate lower flange, six runner starts, passages and related exterior shoulders together. The installed geometry comes through compact intake/cap coordination, exterior detail and runner-exterior adapters; changing only `efi_intake.py` is insufficient. `upper_intake_clearance_candidate.PORTS/MAINS`, both exterior candidates' air/runner paths and protected flange checks encode equal spacing. Existing hash-guarded fixtures reject altered inputs; preserve those historical fixtures and create a separately versioned coordinated successor.
4. `efi-upper-stud-1..7`: reposition confirmed axes and revise stack checks. Existing shank/hex definition is estimated; preserve its identity but do not assert factory thread/engagement. Terminal ears and central off-row hole require Y offsets. Studs 3/5 cannot receive definitive holes until paired roles resolve.
5. Protected lower/head dependencies: `efi-head-intake-gasket`, head ports, `intake-head-locating-dowel`, front lifting-eye attachment relief and rear manifold attachments. Preserve the `define()` adapter effects for `manifold_lifting_eye`, `intake_locating_dowel` and applicable `rear_manifold_mounts_desktop_candidate` interfaces. Rebuilding raw lower geometry must not erase installed corrections.
6. Protected adjacent systems: six `fuel-injector-*` assemblies and their seals, rail cups/mounts and regulator use existing lower/head-side stations. They need no intentional movement when those datums are preserved, but lower-runner changes invalidate their casting-clearance/seat context checks. Upper plenum endpoints, throttle assembly frame, EGR frame and connections, regulator vacuum receiver, oil-fill/cap access, rocker motion and support pad must be retained or explicitly reopened. No relocation is authorized by the gasket evidence. The upper support's other anchor remains unresolved in its separate research contract.

No part-count increase is established. Direct intended changes are three casting/gasket occurrences plus seven stud placements; a stud definition revision is conditional on later stack evidence. Protected neighboring geometry is checked rather than silently moved.

## Implementation sequence and acceptance plan

1. Freeze one new layout data object with the normalized features, shared frame, independently chosen scale and evidence class for every numerical parameter. Resolve paired-hole roles and end/face correspondence before promoting a fastened assembly. If estimates are explicitly accepted, record value/range/reason independently of clearance and label all resulting geometry accordingly.
2. Create isolated coordinated upper/lower/gasket candidate functions consuming that single object. Preserve final installed baseline as comparison and transfer only reviewed existing non-joint geometry. Rebuild complete air passages and exterior surfaces from new paths. Do not patch frozen guards or claim their former passes for the new candidate.
3. Preserve stable IDs and current zero occurrence frames for the three large parts; bake/localize with existing assembly helpers. Explicitly compute stud transforms from mapped holes and stack. Publish candidate files only; root chooses integration adapter order after reviewing all three geometries together.
4. Run six-port coaxial/continuity checks, shared hole-axis and gasket-contour checks, connected sealing-land checks, fastener stack/engagement and STEP/GLB unit/bounds checks. Use existing numerical tolerances where applicable; specify new physical clearance/land requirements only when supported. A shifted port, mirrored gasket, wrong paired hole and blocked passage must each produce the expected failure. Do not force nine-hole roles merely to make checks pass.
5. Render attachment face, opposite side and assembled context beside identified gasket/casting sources; inspect exported GLB. Audit whole changed castings against current neighbors, not only added material, because material will be removed and replaced. Recheck throttle/cable motion, cap removal, rocker clearance and exploded/reassembly behavior affected by the new bounds. Old exterior added-material proofs do not cover reshaped runners.
6. Root reviews candidate before shared installation; installed browser selection/isolation/reset and combined assembly acceptance remain separate gates. ACT boss axis stays unapproved until corrected source/geometry registration independently constrains it.

## Focused metric lead log

Nine queries sought MS93838 dimensions/ruler/measurement, E7TZ9H486B ruler, 4.9 EFI lower intake ruler/overall length and E7TE9K461 dimensions. No applicable part measurement was verified. NPD `https://www.npdlink.com/product/intake-manifold-gasket-upper/136567/60347` identified a potential 1987–96 300 EFI gasket listing; web open returned cache miss, not dimensional evidence. Mr Gasket 260 1.25×1.75 inch port claims concern the head joint/earlier application; Pierce four-barrel manifold dimensions and a carbureted manifold ruler listing concern the wrong architecture. Ford M9486A50 is 5.0 V8. All rejected as scale sources. No repeated blocked-host attempts and no owner-photo dependency were introduced.

## Delivery and quality gates

Readiness **research**, implementable correction plan. No CAD/export, installed-interface, motion, browser or source-versus-new-CAD checks run: **NOT RUN**, because no geometry is generated or approved. Application/coverage: **PASS for replacement joint identification and 6/9 visible topology**, paired roles still unknown. Dimensions/coordinates: **NOT RUN for metric acceptance**; dimensionless extraction and IDs are checked. Learning/diagnostics: **N/A**, this package is a geometry correction contract, not a diagnostic component delivery. Reproduction: read-only audit command below reproduces the manifest/feature scope; root review pending. No STEP/GLB/release artifacts. Python version and exact dependencies are recorded in scope JSON; CAD runtime N/A; model usage unavailable.

Run `python3 scripts/intake-joint-layout-20261003-audit.py` and compare its JSON with `reference/engine/intake-joint-layout-20261003-scope.json`. The audit changes no files. It asserts six ports/nine holes/seven existing stud IDs and hashes inspected sources; it does not prove source geometry or fastening roles. Issue remains open. Next useful evidence is an identified gasket/casting actual span or dimensioned outline, plus correspondence of paired casting holes. Alternatively root can review a clearly estimated educational scale contract without claiming factory millimeters. No process remains running.
