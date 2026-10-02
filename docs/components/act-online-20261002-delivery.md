# ACT online specimen — delivery and review

## Contract and evidence

Issue82, engine sensor/harness coverage; root owns integration. Baseline `54c2abf7aae73a8a5818321ee48ad81c8b7346ad`. Pre-build contract: `act-online-20261002-specimen.md`. This delivery is a **local candidate**, not installed or factory-exact. It uses MTE5041 as the identified F2DZ12A697A comparison. Original sensor tag remains unknown. No host port, vehicle transform, harness cavity or shared model was edited.

New evidence is actual manufacturer side, oblique and connector-face imagery. `reference/engine/act-online-20261002-evidence.json` binds URLs, hashes and explicit pixel landmarks. Hex25mm and18TPI are replacement specifications; other geometry is inferred. Source originals live outside Git and must be reacquired using those URLs for independent source review. The PDF page269/printed267 is supplementary and its regional fitment is not the exact-year identity bridge.

## Delivered physical regions and explanations

| Stable local ID | Function and relationship | Explicit limitation |
|---|---|---|
| `act-online-metal-shell` | Threaded metal shell and hex provide the mechanical mounting envelope; the open guard surrounds the visible sensing tip while admitting surrounding air. | Photo-shaped guard; estimated thread length/runouts and cavity. No installed engagement, strength or sealing proof. |
| `act-online-insulator` | White keyed body separates the contacts and locates the connector mouth within the metal shell. External keys follow visible asymmetry. | Internal core and supporting neck are inferred; molding/retention and mating harness unknown. |
| `act-online-contact-1` | First of the two visible round electrical contact ends, supported by the insulating body. | No assignment to signal743 or return359 from photo orientation. Hidden lead absent. |
| `act-online-contact-2` | Second electrically separate contact end; it is not joined to the first inside this model. | Hidden lead absent. Complete circuit continuity is NOT claimed. |
| `act-online-mouth-liner` | Distinct dark annular region visible around the connector mouth. | Material, manufacturing separation and sealing function unknown; never described as a verified pressure seal. |
| `act-online-visible-sensing-encapsulation` | Blue external envelope visible within the open guard; represents the exposed encapsulated sensing element. | No fabricated semiconductor chip, internal composition, calibration, lead routing or potting. Its inferred support is geometric only. |

The existing NTC function note explains temperature sensing. These six material regions do not assert six separately manufactured service parts, or a complete electrical pressure boundary.

## Revision and preserved failures

The first valid metal solid was incorrectly smooth: a conical cutter crossing both end planes removed no material. Actual render review and radial inspection caught this, so the earlier local PASS is superseded specifically for thread coverage. Preserved `act-online-20261002-rejected-smooth-thread.step`, corresponding module and historical validation retain the defect. No threshold was relaxed.

A bounded cutter contained within the15mm threaded envelope now creates real helical grooves. The selected12mm cutting span leaves estimated1.5mm runout regions; these are explicit representation choices, not manufacturer dimensions. Actual removed volume is102.4705467mm³. At eight angular stations and67 axial samples,345 probes hit crests and191 lie in grooves. The smooth blank fails the same predicate. Generic NPTF taper/pitch/flank information does not verify truncations, gauge plane or a dryseal fit.

Earlier logs preserve the one degenerate bead mesh triangle and two local interference failures. Zero-area triangle cleanup produces a watertight mesh. An explicit estimated feedthrough seat and raised key root resolve the material intersections; no host or neighboring part was carved. Historical pre-feedthrough code remains preserved.

## Commands and outputs

```sh
.venv-cad/bin/python scripts/act-online-20261002-check.py
MPLCONFIGDIR=/tmp/act-online-20261002-mpl python3 scripts/act-online-20261002-render.py
```

Module API: `cad/engine/act_online_20261002_specimen.py:build()` returns six named build123d solids in the declared local millimeter frame. Generated STEP/GLB and authored render are under `cad/engine/generated/act-online-20261002-specimen/`. Final hashes and the exact authored allowlist are in `reference/engine/act-online-20261002-delivery.json`. Standard project CAD environment, system Python/Matplotlib renderer; source rendering used Poppler. No network dependency to rebuild geometry. Excluded source originals are required only for independent photo review. No original photo pixels appear in the delivered render.

## Validation and limitations

| Gate | Result | Scope |
|---|---|---|
| Application | PASS qualified comparison | Ford tag-qualified listing plus manufacturer interchange; no original stamp claim |
| Dimensions | PARTIAL | Hex/pitch supported; lengths, keys, contacts, walls and guard inferred |
| CAD/export | PASS local | Six valid one-solid STEP round trips; six watertight positive consistently wound meshes; maximum bounds error0.001503mm against0.05mm gate |
| Local interfaces | PASS bounded |15 actual part pairs, zero measured overlap; shell/insulator, pins/insulator and bead/support distance contact; no preload/strength/retention certification |
| Surface/controls | PASS | Actual removed thread material,536 sampled crest/root checks; smooth, bridged-contact and filled-window controls detected |
| Source/visual | PASS topology comparison only | Side/oblique/end actual exported meshes inspected beside named manufacturer views; simplified flat guard, sharp collar/keys, estimated recession and runouts differ from rounded source features |
| Installed contact/flow/tool | NOT RUN | No manifold port, installed gauge datum or harness pose |
| Motion/disassembly | NOT RUN | No installed neighbors or removal corridor |
| Learning | Scoped text delivered | Table above; two new KB pages; hidden internals and incomplete circuit explicit |
| Browser integration | NOT RUN | No installation or shared viewer edits |
| Reproduction/review | Worker checks complete; root review pending | Exact hashes/commands and preserved failures; root independently reviews |

No commit or publication from this worker. Next integration contract needs lower-intake source port/frame, supported engagement and harness mating geometry. The local candidate can be preserved without claiming those interfaces. No running process. Usage accounting unavailable.
