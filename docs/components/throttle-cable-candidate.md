# Component contract and handoff: accelerator cable engine end

## Contract

Issue #43 under engine #1 remains open. The integration lead owns canonical installation. This worker owns only `cad/engine/throttle_cable_candidate.py`, `scripts/check-throttle-cable-candidate.py`, `scripts/check-throttle-cable-current-neighbors.py`, `inventory/engine/throttle-cable-candidate-validation.json`, `reference/engine/throttle-cable-review.json` and this handoff. No canonical assembly or viewer changes. Candidate work began from `fb2a1e756cf5e0d6ed925975312231406fce18ed`; integration advanced independently to `3e53f117146fe1746ef882abbeabf6542bcba0d2`. The validation report records the actual current manifest and relevant STEP hashes used.

Scope is an isolated educational engine-end cable mechanism. Preserve existing ball stud, mounting studs/ears, shield and shaft-return-spring anchors. A coordinated replacement of the inferred bracket's distal web/flange is proposed. Exclude automatic C6 kickdown, unverified cruise equipment, firewall/pedal routing and manufacturing/strength/rate claims. Ford identifies accelerator cable assembly 9A758; F4TZ9A758M is a catalog replacement cross-reference, not a verified owner-installed identity. The internal decomposition is educational, not a service procedure for the nonserviceable cable assembly.

Millimeter CAD, original throttle parent-local coordinates. All eight exported definitions use `throttle-assembly` coordinates and identity occurrence transforms at neutral; dynamic components require the articulation described below. Apply the current ancestor transform once: currently −167X. Existing ball center is `(394+24 sin θ,95,490+24 cos θ)` in that local frame. Never permanently bake the ancestor shift into the cable geometry. Explode direction is separate from operating motion and is not supplied here.

## Evidence ledger

Full URLs, local hashes and actual observations are in `reference/engine/throttle-cable-review.json`. Source originals and the source-photo comparison are local research only and must not enter Git or shared CAD archives.

| Claim / feature | Evidence class and source | Applicability / uncertainty |
|---|---|---|
| Accelerator cable, bracket, ball attachment and core wire | Exact 1994 4.9 manual Service and Repair, figures 692036165/692057936 | Applicable overall figure includes manual transmission. View Y item 7 is C6 kickdown rod 7A187, excluded here. |
| Distinct cable-end compression spring | Exact application Test C, figure 693302607 | Separate from shaft torsion spring. No spring dimensions, rate or seat construction established. |
| Long black terminal stem, substantial overlapping coil and snap retainer | Directly viewed CAHSA FO149 and Pioneer CA-8806 replacement photographs | Manufacturer catalogs cross-reference F4TZ9A758M. Catalog rows lack explicit transmission qualifiers; owner-installed identity unverified. |
| Coil close to/slightly wider than moving stem; stem and exposed coil comparable lengths | Replacement image proportions | Images have no dimensional scale; all selected dimensions remain estimates. |
| Exact socket, guide and swivel retention internals | Educational construction | Hidden in photographs and not established by manual. Four snap fingers, hollow spherical pivot and flanged guide insert are hypotheses. |
| Cruise equipment and actual original fitting | Unknown | Owner engine-bay overview photographs obscure the engine-end fitting. |

The rejected initial 2.36–2.46 mm OD spring passed a limited clearance check but failed the specimen comparison. It was not promoted. Its local checkpoint remains under `generated/throttle-cable-candidate/rejected-narrow/`. The revised stem/coil proportions were directly reviewed by the integration lead before authorizing the full sweep.

## Geometry and interfaces

Seven new illustrative definitions plus replacement of the existing bracket:

- Snap retainer and captured sheath stub stay fixed. Rear flange and slotted front barbs straddle the actual 2 mm bracket flange. The sheath's bead is seated in a matching retainer receiver.
- Socket/long moving stem captures the unchanged ball. The socket contains a seated inner-core terminal and extends 36 mm toward the fixed end. Its 6.8 mm main stem OD is an estimate.
- Fixed-end swivel seat captures a hollow stationary ball; a separate flanged guide is physically retained in that seat. The moving hollow stem telescopes over the guide. This inferred articulation avoids passing a diagonal rigid cable through a solid ferrule.
- Inner core is one continuous swept path: a straight moving segment, tangent cubic bend through the hollow pivot and fixed-axis sheath segment. Its visible length changes as material feeds through the open sheath cut boundary; that boundary is not a fixed material endpoint. No full cable-length or strain model is claimed.
- Compression spring is a continuous swept helix between actual moving/fixed seat planes. It compresses from about 47.673 to 15.875 mm over 0–90 degrees. Illustrative 24 turns, 0.5 mm wire and 8 mm neutral OD; a small radius change preserves centerline length. Spring-end profiles are ground at the seat planes. No force, preload, fatigue, spring-rate or reliable vehicle-return claim.

The cable exit moves from `(465,110,467)` to `(470,112,467)`: **+5X,+2Y,0Z**. The distal flange moves from X463–465 to X468–470; its new cable hole is 11 mm diameter. A 5 mm web extension and four intersecting web reliefs clear the thicker articulated mechanism. The inherited secondary window stays at Y110/Z488. The protected region X377.5–410.5 contains mounting ears, shield fastener and shaft-spring anchor. Exact symmetric-difference testing proves that region unchanged. Ball, lever, shield, stud and shaft-spring shapes are not altered.

`state(angle)` returns ball center, cable unit direction, moving/fixed articulation planes and axial spring length. `stationary()` returns fixed parts. `moving(angle, include_spring=True)` returns moving part shapes and centerline metrics. `bracket_proposal(existing)` accepts the current bracket shape in throttle parent coordinates. A later viewer must regenerate/deform the core and coil from these same centerlines; rigidly rotating the complete cable or spring is incorrect. Current candidate supplies exact CAD at arbitrary angles but no viewer deformation table yet.

## Delivery

Candidate only; no commit, PR, canonical installation or Done claim by this worker. Entry point `cad/engine/throttle_cable_candidate.py`; checker exports STEP/GLB to ignored `cad/engine/generated/throttle-cable-candidate/`. Validation JSON records input/output hashes. Pure CAD views are `candidate-neutral.png` and three-pose `candidate-motion.png`; local-only source comparison is `feasibility-reference-comparison.png`. No asset release uploaded. Learning/browser integration is not included.

Commands from repository root:

```sh
XDG_CACHE_HOME=/tmp/truck-cache .venv-cad/bin/python scripts/check-throttle-cable-candidate.py --full
XDG_CACHE_HOME=/tmp/truck-cache .venv-cad/bin/python scripts/check-throttle-cable-current-neighbors.py
MPLCONFIGDIR=/tmp/truck-cable-mpl python3 scripts/check-throttle-cable-candidate.py --render
```

Without `--full`, only the initial 0/45/90 smoke test runs. `--render` needs the locally held replacement photo and outputs a nonredistributable comparison. CAD reproduction does not require that photo. Environment: macOS, Python 3.13.12, build123d 0.10.0, trimesh 4.7.4; system Python matplotlib 3.10.9 for rendering. Model/effort and usage unavailable. Manual archive and owner photographs stay ignored; source URLs allow another researcher to find the evidence without private temporary files.

## Validation and review

**Candidate full sweep PASS:** 47 poses (0–90 every 2 degrees plus 45), 2,360 exact collision pairs, zero collisions or invalid shapes, original 1,330-occurrence broad phase. All eight neutral exports are valid one-solid, watertight STEP/GLB; maximum actual bounds error 0.008652 mm, maximum STEP volume error 1.97e-6 mm³. Exact CAD helix centerline variation is 7.39e-12 mm; minimum adjacent-turn surface gap over all 91 integer poses is 0.161186 mm. The closing-force direction projection is negative at all 91 angles; this is a geometric sign check, not a spring-force guarantee.

**Final-current addendum PASS:** current manifest `4f98bbdad7fb1996487d17c4a651de588cef39254efe24e96384375dbdce0c07`, 725 definitions / 1,333 occurrences. Every occurrence was broad-phased again. The 20 selected nearby occurrence IDs, their STEP hashes and all 47 transforms match the original sweep scope. New/changed IAC electrical parts lie outside the conservative complete cable envelope, so zero additional exact pairs were required.

Temporal provenance limitation is explicit: the preserved original checker reads the manifest hash at finish rather than at load. Its top-level `manifest_sha256` must not be interpreted as the original snapshot hash. The integration lead identified pre-electrical snapshot `cad/engine/generated/iac-closure-integration-stage/full-assembly.json`, SHA `80060a6dabed8f1f909e49852423fae03693aa3066e43a139438e240056aa8b2`; the electrical staging before-hash agrees. The separate addendum binds scope using that snapshot's poses, original selected STEP hashes and final current mesh hashes. The checker used for the original run is preserved unchanged, and the addendum explains the limitation rather than rewriting its history.

| Gate | State / method | Limits |
|---|---|---|
| Application / coverage | Source-backed topology; exact manual and two replacement specimens inspected | Dimensions, internal construction and exact installed cable identity unresolved |
| Dimensions / coordinates | Explicit estimated mm coordinates; protected-region exact difference zero in initial check | No production dimensional claim |
| CAD / export | PASS: all eight exports valid one-solid and watertight; STEP roundtrip checked | Trimmed socket's conservative OCC bounding box requires exact planar-support bounds; report preserves both measurements |
| Source / visual comparison | Revised comparison reviewed by integration lead | Coil turns and guide construction illustrative |
| Interfaces | PASS: seated contacts, positive withdrawal/capture and detached negative controls | Snap insertion deformation, manufacturing and strength not modeled |
| Motion / disassembly | PASS: full 47-pose sweep; all 91 integer helix spacings and closing-direction signs checked | Sampled collision check, not a continuous mathematical sweep; capture probes are not full disassembly animation |
| Learning / diagnostics | NOT RUN | Future lesson must separate cable spring from shaft torsion spring and state missing firewall/pedal interfaces |
| Browser integration | NOT RUN | No canonical/viewer edits authorized |
| Reproduction / review | Deterministic CAD/checker and hash-bound report | Asset release and installed checker remain integration work |

No generic collision exclusions: the candidate bracket, all seven cable parts and actual nearby occurrences are checked. Intentional seated contacts have zero nominal intersecting volume and are separately measured by contact area. Exact overlap threshold is 1e-5 mm³; export bounds tolerance is 0.2 mm, STEP volume difference 0.001 mm³. Relevant neighbor STEP files are hash guarded. The report records all-occurrence broad-phase coverage and selected exact neighbors, including the live deforming shaft spring, installed plate screws, shield and unchanged ball. Detached-retainer and detached-socket negative controls must fail attachment; offset probes must penetrate their actual retaining lips/seats.

## Tracking and restart

Issue #43 remains open. Next action: integration lead reviews the final report and motion render, then decides whether to stage seven new definitions/occurrences plus the coordinated bracket replacement. Installation, viewer deformation and browser checks are separate acceptance gates. No worker processes remain running. Full-run and final-current logs are `cad/engine/generated/throttle-cable-candidate/full-check.log` and `current-neighbors.log`. Do not promote a neutral-only geometry export as working installed motion.
