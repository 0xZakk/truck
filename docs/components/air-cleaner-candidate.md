# Component contract and handoff: air-cleaner-candidate

## Contract

- Issue #80 under Engine #1. Contributor: air_cleaner_candidate agent; integration owner: root agent. Shared branch `engine/runner-stops-and-evr`, serialized integration owned by root.
- Baseline `796b621244d8e341fe2f3c4de7af99488af01548`; baseline manifest SHA-256 `0656841ba587a3f05d193aa75fb711f320ddf732cc0343c68504836c9ea7537d`.
- Isolated candidate: molded lower dirty-air tray, twin-outlet clean-air lid, treated pleated paper representation and separate perimeter seal. No body placement, bracket, ducts, breather port or assumed cover hardware. Exact cover screw pattern remains unknown and retention gate open.
- Owned files: `cad/engine/air_cleaner_candidate.py`, `scripts/check-air-cleaner-candidate.py`, this handoff, `reference/engine/air-cleaner-candidate-review.json`, `inventory/engine/air-cleaner-candidate-validation.json`, `inventory/engine/air-cleaner-candidate-learning.json`, `cad/engine/generated/air-cleaner-candidate/`. No canonical files.
- Identity: housing base 9600, filter E7TZ-9601-B/FA-1046 leads; federal catalog F4TZ-9600-C not confirmed for owner. Exact-year service identifies paper media and assembly topology.
- Millimeters. Local origin filter seal top center; X long side, Y width, Z up. Twin outlets toward -X. Parent/body transform UNKNOWN. Isolated identity transform is not an engine installation. Explode lid +Z, seal/media +Z then tray fixed.
- Comparison sizing: WIX 46174 326.7 × 148.7 × 43.5 mm used as one explicitly unconfirmed replacement envelope. K&N 33-2023 325 × 146 × 30 mm remains separate; no averaged dimensions.
- Estimated tray top 346 × 170 mm, bottom 310 × 140 mm, depth 100 mm; lid roof 58 mm; outlet bore 54 mm, centers Y ±37 mm. All wall, rib, seat and inlet dimensions inferred. No measured OEM dimensions.
- Available local sources: exact-year archived 190226466 and dealer drawing from research ledger, pixels independently inspected. Restricted source originals never distributed. Public links and capture hashes retained in research ledger. GitHub issue fetch failed network; parent assigned issue 80 scope.
- Planned checks: `.venv-cad/bin/python scripts/check-air-cleaner-candidate.py`; validity, intended one solid each, STEP roundtrip volume tolerance 0.01 mm³; mesh bounds 0.2 mm and watertightness; passage witnesses obstruction<0.001mm³ with blocking fault>1mm³; seal annulus coverage gap<0.001mm³ with shifted/missing seal fault>1mm³. These are design verification tolerances, not production specs. Actual CAD mesh render before further detail; installed/browser gates NOT RUN.

## Evidence ledger

See `reference/engine/air-cleaner-research-review.json` for source URLs, hashes, applicability, counts and uncertainties. Independent inspection confirmed deep tapered tray, rectangular side inlet, ribbed upper and lower molding, two circular outlets on one short face, separate rectangular element and formed body bracket. Cover screws are source-supported but count/location unknown; no clips invented. Housing mounting screws 2 and grommets 2 are distinct from unknown cover screws. Four bracket screws and four duct clamps apply to future interfaces.

## Delivery

- Readiness: **candidate only**, not integration-ready. Branch above; root owns commit/PR. Four isolated physical representations, no installed definitions added.
- Entry point: `air_cleaner_candidate.build() -> dict[str, build123d.Shape]`; call from repository `cad/engine` import path. `seal()` returns separate seal; mm-to-viewer conversion `(x,z,-y)/1000` in checker follows existing engine convention.
- Outputs: `cad/engine/generated/air-cleaner-candidate/` has four STEP and four GLB files, combined `candidate.glb`, mesh `preview.npz`, `candidate-review.png`, and `check.log`. No source images embedded. Regenerate rather than depend on a personal/temp path. Private release upload remains integration owner's action; no release URL claimed.
- Commands: `.venv-cad/bin/python scripts/check-air-cleaner-candidate.py` then `python3 scripts/check-air-cleaner-candidate.py --render`. CAD environment Python 3.13.12 / build123d 0.10.0 / trimesh 4.7.4 on macOS 15.6.1; render environment requires numpy and matplotlib (tested 3.10.9). CAD venv does not contain matplotlib; two-stage command is intentional.
- Validation: `inventory/engine/air-cleaner-candidate-validation.json`. Evidence/review: `reference/engine/air-cleaner-candidate-review.json`. Learning: `inventory/engine/air-cleaner-candidate-learning.json`.
- Existing throttle has provisional 40 mm bores, 48 mm outside spigots, 54 mm center spacing. Candidate housing 54 mm bores / 60 mm necks / 74 mm centers are estimated. Future flexible ducts must transition and allow engine-to-body motion; no equality or rigid engine-mounted box assumed.

## Validation and review

| Gate | Result | Method / record | Remaining limits |
|---|---|---|---|
| Application/coverage | PASS bounded study | Exact-year drawing and owner/dealer images independently inspected; review ledger | Full issue 80 hardware/duct/snorkel/bracket scope incomplete |
| Dimensions/coordinates | PASS documentation only | Explicit local frame and replacement vs estimates | Factory dimensions and body transform unknown |
| CAD/export | PASS | Checker report hashes; four valid single solids, STEP roundtrip, watertight meshes, GLB roundtrip bounds | Local candidate only |
| Source/visual comparison | PASS limited comparison | Actual assembled/exploded mesh render inspected against source pixels | Estimated contours and missing hardware; no fidelity acceptance |
| Installed interfaces | NOT RUN | Body neighbors unavailable | Cover fasteners, mounting datums, breather and duct transitions unresolved |
| Motion/disassembly | NOT RUN | Exploded render only | No removal sweep/retention or engine-motion proof |
| Learning/diagnostics | PASS bounded content | Learning JSON | Fault mechanisms clearly inferred; no invented service interval |
| Browser integration | NOT RUN | Isolated candidate not installed | No navigation/selection acceptance |
| Reproduction/review | PASS rebuild; review pending | Source/checker plus validation hashes and generated artifacts | Root independent review and artifact publication pending |

Flow tests witness open lower inlet and each upper outlet separately; they do not simulate porous flow or establish filtration performance. Perimeter test detects absent/shifted seal; it is not a pressure-leak test. Seat probes verify annular material at both seats, not factory compression. First cheap test caught 5208 mm³ paper/frame-to-tray flange overlap; aperture was corrected before passing. Rounded cover shoulders and triangular ribs were added after the first actual render; the cheap tests were rerun unchanged.

Source/render comparison: twin circular short-face outlets, rolled roof shoulders, molded side ribs, tapered tray and rectangular inlet align with source topology. Pleat count, all molding dimensions, media carrier and seal section remain estimated. Actual owner overhead photo supports the broad flat roof and paired ducts but cannot establish hidden geometry. Cover screw bosses are deliberately absent because their pattern is unresolved; this is an explicit missing retention interface, not a completed cover.

## Tracking and restart

- Issue 80 stays open. Parent read issue scope (zero installed definitions; housing/lid/filter/hardware, ducts/clamps, snorkel/body mounting; boundaries #7 / #12). No board status observed by this worker.
- Next: integration owner reviews candidate render/report, preserve generated artifacts per CAD policy, then research cover screws, body bracket datums, breather port and twin duct transition before any installation.
- No long-running process at handoff. No canonical inputs changed; no installed checks invalidated. Model/effort and usage unavailable to worker; no cost figures invented.

## Section and retention follow-up

`python3 scripts/render-air-cleaner-section.py` renders three actual mesh sections without rebuilding or rerunning unchanged CAD checks: full longitudinal section, pleat detail and transverse seal/seat detail. Outputs are `cad/engine/generated/air-cleaner-candidate/candidate-section-review.png` and `section-render.json` with mesh/script/output hashes. The existing candidate source, checker, validation and review were copied to the same generated directory's `frozen-first-candidate/` before this follow-up. Geometry and the original validation inputs remain unchanged.

The section exposes the paper carrier's contact with the seal and both housing seats. The paper profile uses a 0.65 mm vertical offset, **not** a constant 0.65 mm stock thickness; fold spacing/depth and thickness remain illustrative estimates. The section is an inspection aid, not a new seal-pressure or filtration acceptance test.

Retention research remains unresolved. Exact-year service instructions distinguish cover screws from the two housing-to-bracket fasteners, but supply no cover screw count, positions or boss construction. The alternative procedure drawing 13268245 repeats the existing assembly view rather than exposing the cover underside. The owner overview photos do not reveal a complete perimeter. No screw geometry was added.

Breather topology is supported at the system level: the exact-year hose procedure connects the valve cover to the engine air cleaner; housing service names a closure hose/filter pack; assembly item 11 is the crankcase ventilation hose. The generic PCV diagram 620350918 distinguishes this fresh-air route from the PCV return to the intake manifold. It does not establish this truck's housing penetration or whether the separate filter pack draws from the main element's dirty or clean side. Both owner engine-bay views were inspected; neither resolves that endpoint. No port was placed.

Compact findings and source hashes are in `reference/engine/air-cleaner-candidate-review.json` under `retention_breather_followup`. Next useful evidence is an identified applicable cover underside/perimeter and closure/filter-pack specimen view. There is currently insufficient evidence for new retention or breather geometry. Source originals remain excluded from Git and release artifacts.
