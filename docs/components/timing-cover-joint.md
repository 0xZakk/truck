# Component contract and handoff: timing-cover joint

## Contract

- Assignment: missing cover-to-block gasket and coordinated sealing-joint study under issue #32, Engine #1. Issue #32 includes gasket/attachment reconciliation, timing marks, gear retention and all shared quality gates; this bounded study does not complete that issue. Parent supplied current issue text after direct GitHub fetch failed.
- Contributor: air_cleaner_candidate agent. Integration owner: root. Branch `engine/runner-stops-and-evr`; baseline `796b621244d8e341fe2f3c4de7af99488af01548`. Source baseline manifest SHA-256 `0656841ba587a3f05d193aa75fb711f320ddf732cc0343c68504836c9ea7537d`; current worktree inventory may include other coordinated work.
- Scope: isolated source-proportioned main gasket topology candidate and interface revision proposal. No shared geometry, installation, guessed lower-strip role or guessed pan bridge. Actual manufacturer outline must precede geometry.
- Owned: `cad/engine/timing_cover_joint_candidate.py`, `scripts/check-timing-cover-joint-candidate.py`, `reference/engine/timing-cover-joint-review.json`, `inventory/engine/timing-cover-joint-validation.json`, this handoff, and `cad/engine/generated/timing-cover-joint-candidate/`.
- Evidence: exact 1994 service instructs discarding the cover gasket and coordinating removal with front oil-pan fasteners. Manufacturer VIN-Y catalog lists TCS 45829 and TCS 45830, both requiring OS 34601 R. Actual primary images of both kits independently inspected: asymmetric open-bottom main gasket with seven holes, separate shallow five-hole strip, separate crankshaft seal. The second kit also depicts sleeve and consumables. Kit photos are not installation drawings.
- Local mm frame: sheet in YZ, X normal. Source-view coordinate origin is pixel (800,1030) of the 1600-pixel display view; Y increases with image horizontal, Z upward. Illustrative scale 0.2 mm/pixel, thickness 0.8 mm. Neither is measured. Engine registration UNKNOWN. Identity display transform is not an installed transform.
- Keep canonical geometry unchanged during research. Existing crank/cam axes and gear/seal axial stations are provisional and may require coordinated revision; they are not immutable. Current cover root X = 403 mm gives rear wall X = 391 mm; cam retention block face X = 373 mm; v9 front pan land spans X = 365–381 mm. These are provisional model coordinates, not production dimensions. No seven-hole cover mounting pattern is established in current source. Do not bridge the 18 mm cover-rear/block-face discrepancy by stretching gasket thickness.
- Inputs verified locally: exact-year cover service HTML, saved Fel-Pro master catalog and reviewed VIN-Y row, canonical cover/cam-retention/pan-joint source. Retrieved public manufacturer part-finder metadata and primary image assets. Original imagery stays ignored and excluded from Git/releases.
- Planned checks: single valid solid; seven open fastener passages and deliberate plugs; open-bottom cavity witness and bridge fault; STEP roundtrip volume delta < 0.01 mm³; mesh watertightness and bounds error < 0.2 mm. Local outline gates only. Continuous installed seating, pan terminals, cavity/gear clearance and browser acceptance remain NOT RUN until a registered joint exists.

## Evidence ledger

| Claim | Class | Evidence / limit |
|---|---|---|
| Gasket is a separate service part | Verified application | Exact 1994 timing-cover removal text says discard gasket; source hash in review JSON |
| TCS 45829 / TCS 45830 apply to VIN Y and require OS 34601 R | Replacement comparison | Manufacturer master catalog, printed pages 327–328, previously reviewed VIN-Y row |
| Main gasket is open-bottom and has seven holes | Replacement specimen topology | Both exact manufacturer-returned kit images visually inspected; not a factory drawing |
| Separate shallow five-hole strip appears in both kits | Replacement specimen observation | Installed identity and junction role remain unknown |
| Outline and hole proportions | Inferred from specimen image | Primary data are dimensionless normalized coordinates; manual center uncertainty ±3/1600 per axis, edge uncertainty ±8/1600 |
| Display dimensions and 0.8 mm thickness | Arbitrary illustration | 320 mm assigned to full image edge solely for CAD display; no actual part scale inferred |
| Joint plane X = 373 mm | Current model datum only | `full_engine.py` LENGTH = 746 mm and `cam_retention.py` BLOCK_FACE = 373 mm; not a factory datum |

`reference/engine/timing-cover-joint-review.json` stores exact manufacturer asset and public API URLs, captures/hashes, seven normalized hole centers, aspect ratio, uncertainty, separate-kit comparison and interface proposal. Source originals are in the ignored generated reference subfolder and must be excluded from release artifacts.

## Delivery

- Candidate API: `timing_cover_joint_candidate.build() -> dict[str, build123d.Shape]`. One main-gasket sheet. Dimensionless coordinates in `OUTLINE_NORMALIZED` and `HOLES_NORMALIZED` are the primary geometry data; the arbitrary mm display scale can change independently of those proportions.
- This is **not a coordinated sealing-joint solution**. Root approved the reduced outline-study scope after inspecting the evidence discovery. The five-hole strip is not modeled until its function is identified. Existing seal, gear, cover, block and pan definitions are unchanged.
- Commands from root: `.venv-cad/bin/python scripts/check-timing-cover-joint-candidate.py`, then `python3 scripts/check-timing-cover-joint-candidate.py --render` using numpy/matplotlib. CAD environment: Python 3.13.12, build123d 0.10.0, trimesh 4.7.4; render matplotlib 3.10.9, macOS 15.6.1.
- Outputs: `cad/engine/generated/timing-cover-joint-candidate/main-gasket.step`, `main-gasket.glb`, `preview.npz`, `candidate-review.png`, `check.log`. Asset hashes in the review JSON. No release published by worker; source coordinates reproduce exports without the private/local image capture.
- Validation: `inventory/engine/timing-cover-joint-validation.json`. Submitted branch above; commit/PR and independent acceptance remain root-owned. Model/effort and usage unavailable.

## Concrete interface revision proposal

The following coordinates describe the current model only: crank axis (Y,Z) = (0,0), cam axis (90,72), gear center X = 385.259375, seal occurrence X = 414, cover root X = 403 and cover front face X = 415. The axis-freeze portion of this initial proposal is superseded by the gear coordination below; no current datum is promoted to a factory constraint. Current cover back is X = 391, leaving an 18 mm axial discrepancy to the current model block plane X = 373. A thick gasket is not a valid resolution.

For a coordinated follow-up, first review registration of the normalized seven-hole outline against the current model crank/cam axes and actual gasket terminals. Subject to that review, use the **model's** X = 373 face as a proposed block seat, gasket from 373 to 373 + t, and cover seat at 373 + t. Relative to the existing cover root, that is local X = −30 + t. Thickness t is unknown; the isolated sheet's 0.8 mm display thickness is not approved for the installed stack. The cover would need a reconstructed rear skirt/flange reaching that seat, plus a corresponding continuous block land and seven mounting axes. Existing cam-thrust fasteners must not be relabeled as these seven cover fasteners.

The v9 oil-pan front support lies at X = 365–381 with provisional end contours. Neither the manufacturer's flat kit photograph nor current model proves how the main gasket's two open terminals meet that support or the separate five-hole strip. Identify those interfaces before adding a bridge, changing pan shape or claiming continuous sealing. Recheck pump/brackets, shaft seals, gear cavity/motion and all affected static contacts after any future coordinated change.

## Validation and review

| Gate | Result | Evidence / remaining limitation |
|---|---|---|
| Application/coverage | PASS isolated outline only | Manufacturer application row and two exact specimen assets; full issue #32 remains open |
| Dimensions/coordinates | PASS explicit classification | Dimensionless shape plus arbitrary display scale; engine registration unknown |
| CAD/export | PASS | Valid single solid, watertight mesh, STEP volume roundtrip, GLB reimport bounds |
| Source/visual comparison | PASS topology comparison only | Actual frontal/oblique mesh viewed against manufacturer pixels; polygon facets remain; no production-contour claim |
| Installed interfaces | NOT RUN | No matched cover/block land or registered fastener/pan junction |
| Motion/disassembly | NOT RUN | No installed geometry or sweep; existing shafts/gears unchanged |
| Learning/diagnostics | NOT RUN delivery scope | No lesson added for an unresolved installed joint; report explains why open ends cannot imply a sealed assembly |
| Browser integration | NOT RUN | No installed candidate |
| Reproduction/review | PASS reproduction; independent review pending | Source coordinates, commands, hashes and artifact paths present; root reviews before any installation work |

The seven hole probes are unobstructed; deliberate plugs obstruct each. An open-bottom/cavity probe is clear; an added bottom bridge is detected. These local negative controls establish geometric topology sensitivity only. They do not establish continuous seating, oil sealing, shaft clearance or pan compatibility. No threshold was reduced.

## Tracking and restart

Issue #32 remains open. Next action: review `reference/engine/timing-cover-joint-review.json` and the source-free render, identify the five-hole strip and terminal contact topology, then agree registration before coordinated cover/block/pan CAD. No automatic installation or promotion. No process remains running at handoff; no source images/manual pages may enter release artifacts.

## Cover evidence and gear coordination follow-up

Root reviewed the actual candidate render and accepted it only as a useful topology/reference study. The angular polygon and arbitrary scale are not finished-part fidelity. Once registration is supported, use smooth source-supported contours and simplify the render's thickness-axis ticks. Cosmetic refinement is deferred until the joint is resolved.

Actual manufacturer cover evidence now exists. Dorman 635-109 lists OE cross-reference **E5TZ 6019-H** and provides front, back, oblique and separate main-gasket photos. Pioneer 500300's manufacturer catalog explicitly includes 1965–96 F-150 L6 4.9 L in the application table (printed page 15); its illustration on page 31 gives **E5TE-6019-H**. Preserve the E5TZ/E5TE distinction rather than silently treating the strings as identical. These are replacement references, not identification of the owner's cover. Dorman's unlocated 14-inch/2-inch fields are not used as dimensional evidence.

The actual backside photo shows seven perimeter bosses, a recessed cavity and raised sealing land. The open main-gasket path runs around the broad lobe and elongated leg; the remaining lower edge forms a pan-sealing bridge around the crank seal. Front views show ribs and cross-axis threaded holes at that bridge. A seven-hole ordinal correspondence is recorded in the review JSON with approximate photo coordinates and uncertainty; perspective prevents metric registration. Neither casting's circular surface mark is assumed to locate the camshaft.

The separate five-hole Fel-Pro strip remains unidentified. Dorman's separate gasket image shows only the seven-hole main gasket. No inspected manufacturer instruction assigns the five-hole strip to this truck's one-piece OS 34601 R joint. Do not add it on top of that gasket or convert its hole count into a claimed pan-fastener count. The next useful source is a kit component/instruction sheet or applicable factory junction drawing.

Direct coordination with `stops_install_resume` established a material dependency: the current 115.256 mm crank/cam center distance is unverified and forces gear diameters smaller than the newly reviewed PBM/Elgin replacement evidence. The worker's explicitly estimated alternative uses transverse module 2.8 mm, center distance 121.8 mm and cam (Y,Z) = (95.109821,76.087857), with crank at (0,0). Comparison tip radii are 43.18 and 83.947 mm. Source outside diameters do not uniquely determine pitch or helix; these are not accepted factory centers. See `inventory/engine/timing-gear-evidence-validation.json`, whose reviewed hash is recorded in the cover review.

**No registered flange should use the current axes as immutable.** First review the gear/bore-center consistency proposal. Then register a smooth cover/main-gasket outline relative to the reviewed crank seal and gear cavity. Rebuild rear land, seven bosses and the formed pan bridge together. X = 373 remains only the current model block plane: no independent source found establishes that plane or the blockface-to-seal depth. The 18 mm discrepancy to the current cover rear face is still unresolved; no thick gasket or arbitrary bridge is proposed.

This follow-up changed only this handoff, the review ledger and isolated reference captures. No geometry, canonical source or validation checks were rerun. All new photographs and catalog pages/PDF remain reference-only and must be excluded from Git/releases. URLs, exact pages, observations, limitations and hashes are in `cover_evidence_followup` in the review JSON.
