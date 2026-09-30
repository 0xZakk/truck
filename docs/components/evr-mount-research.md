# EVR mounting support evidence discovery

## Contract

- Issue58; engine parent1 and emissions boundary7. Worker `evr_install_resume`; root is integration owner. Research-only follow-up authorized after the frozen illustrative EVR mechanism stage; no geometry or canonical edits.
- Baseline commit `796b621244d8e341fe2f3c4de7af99488af01548`, branch `engine/runner-stops-and-evr`. Historical runner-stage input manifest `2df0e1b64ae048a5f4c57d518bf9104936d7a1bcba8c87dd89850b54921f41c4`. Root is concurrently integrating components; this report does not certify the current manifest.
- Owned files: this handoff, `reference/engine/evr-mount-research-review.json`, ignored captures under `cad/engine/generated/evr-mount-reference/`.
- Scope: identify the regulator support, engine-side receiver, mounting hardware decomposition and dimensional evidence. Harness and full hose routing, internal mechanism, production calibration and any change to the existing occurrence are excluded.
- Required interfaces: two regulator ears, their receiving surface, any intervening pad or separate support, support-to-engine attachment, removal/tool access. All engine receiver and hardware identities remain unknown.

## Verdict

**Research completed; mounting candidate blocked by missing receiver and bracket evidence.** The exact-year location is established. A separate bracket's geometry, part identity, engine attachment and hardware stack are not established by the reviewed evidence. No new support or fastener is justified yet.

The 1994 EVTM actually labels the 4.9L device **EGR control solenoid, C180, base9D474**, below the EVP near the valve cover at the engine's left rear. Printed151-1 is an assembled location drawing, not a mounting detail. Its arrow terminates in the crowded area under the throttle/EGR region; it does not expose a complete bracket or named attachment boss. Printed152-4's nearby **5.0/5.8L** row explicitly names an ignition-coil support bracket. That statement does not belong to the4.9L row. A separate C181/9D475 entry points to151-7, also not the4.9L location. Preserve these distinctions when searching catalogs despite the project's broad EVR naming.

The two existing owner engine-bay photographs were inspected at their supplied resolution. Hoses, intake/throttle hardware and viewing angle obscure the regulator mount; neither supports a hardware count, receiver identity or dimension. The VS52 replacement's actual back and underside photographs show two molded feet with through openings. They show neither the truck's support nor loose mounting hardware. Two openings do not prove two particular screws, washers, nuts or isolators. The actual truck's regulator identity remains unknown.

## Evidence ledger

Full hashes, acquisition URLs and access limits are in `reference/engine/evr-mount-research-review.json`.

| Evidence | Classification | Observation and limit |
|---|---|---|
| Purchased1994 Bronco/F-Series EVTM, PDF312/printed151-1 | Verified application location evidence | Actual full page inspected:4.9L engine location, C180 below EVP. No scale, bracket section or fastener specification. |
| Same EVTM, PDF339/printed152-4 | Verified application location evidence | Separates4.9L location from5.0/5.8L ignition-coil bracket and C181 entry. Base number is not a complete service-part identification. |
| Owner engine-bay driver/passenger photographs,2026-09-23 | Owner-vehicle photographic evidence | Actual images inspected; mounting area occluded and no reference scale. |
| FleetPride-hosted Standard VS52 back/bottom photographs | Replacement comparison | Two molded mounting feet/openings. Not independently identified as owner's installed unit; no truck bracket. |
| Local exact-vehicle service archive, EVR description/operation and parts page | Application text, subject to archive selection limits | Describes function and lists FOTZ9J459A regulator. Neither is a mount drawing; description alone does not resolve EVTM base-number naming. |
| Dealer1994 F-1504.9L5MT EGR and wiring category pages | Catalog search evidence only | Captured pages did not identify the EVR receiver or mounting stack. Catalog categories contain alternatives; category fit heading does not prove each row applies. |
| Existing `reference/engine/ford-efi-intake-parts.jpg` | Historical contextual illustration only | Actual pixels inspected. Intake/EGR valve/external hardware drawing does not identify an EVR mount; no dimensional transfer. |

Local service HTML was searched with tags stripped for EVR/EGR-solenoid terms near bracket/mounting/screw/bolt. Returned diagnostic mentions concerned EGR valve/EVP fastening or generic visual inspection, not an EVR mounting procedure. This records the search result, not proof that no factory procedure exists. Remote searches for4.9L EVR bracket and base-number leads9H472/9S430/9F461 did not produce an applicable dimensioned mount. Other-engine, later European Ford, carbureted and7.5L results were excluded.

## Existing interface inventory — estimates, not measurements

These values are read from the unchanged `cad/engine/evr.py` exterior preserved by the mechanism candidate. They document what a future integration must reconcile; they are not proposed factory specifications.

| Interface | Current model value | Evidence status |
|---|---|---|
| Local regulator axis | +Z, millimeters | Modeling convention |
| Ear bore centers | `[0,-23,27]`, `[0,23,27]`mm | Estimated;46mm spacing |
| Ear bore axes and diameter | Parallel localX;6.6mm diameter | Estimated |
| Ear blocks | 5mm alongX,22mm alongY,14mm alongZ | Estimated; not a photographed thickness measurement |
| Original occurrence frame | Position `[-420,-65,395]`mm, rotation `[0,0,90]`degrees under `egr-vacuum-regulator` | Provisional placement, unchanged by this task |
| Receiving plane/holes, engine parent part | Unknown | No interface can be accepted |
| Separate support, pad, clips, fastener type/count, thread engagement | Unknown | No physical BOM asserted |

Do not create hardware from the6.6mm modeled bore or use the provisional pose to place a brace by eye. A future measured interface may require explicit reconciliation of the current ears and location through the integration owner.

## Delivery and checks

Readiness: **research**. No CAD source, mesh, STEP or assembled visual was generated. No new component passed installation, motion or browser gates. No changed source was supplied to the running EVR installer.

| Gate | Status | Scope |
|---|---|---|
| Application/coverage | Partial; mount identity unresolved | Exact4.9L location verified; hardware BOM unknown |
| Dimensions/coordinates | NOT RUN for physical mount | Existing estimated model interface recorded only |
| CAD/export | N/A | No candidate created |
| Source/visual comparison | PASS for bounded evidence inspection | Actual manual pages, owner photos and VS52 images inspected; no CAD comparison |
| Installed interfaces | NOT RUN | Engine receiver unidentified |
| Motion/disassembly | NOT RUN | Removal path and tool access unknown |
| Learning/diagnostics | N/A | Research handoff only; no lesson changes |
| Browser integration | N/A | No installed change |
| Reproduction/review | Source hashes verified; root review pending | Restricted originals remain access dependencies |

Reproduce the manual views from repository root with system Poppler:

```sh
mkdir -p cad/engine/generated/evr-mount-reference
pdftotext -layout manuals/evtm/1994-Bronco-F-Series-EVTM.pdf cad/engine/generated/evr-mount-reference/evtm.txt
pdftoppm -f 312 -l 312 -scale-to 2400 -png -singlefile manuals/evtm/1994-Bronco-F-Series-EVTM.pdf cad/engine/generated/evr-mount-reference/evtm-151-1
pdftoppm -f 339 -l 339 -scale-to 2400 -png -singlefile manuals/evtm/1994-Bronco-F-Series-EVTM.pdf cad/engine/generated/evr-mount-reference/evtm-152-4
```

Hashes are SHA-256 of exact original bytes. macOS, systemPython3 and Poppler; no CAD execution needed. Owner photos and purchased/manual figures must not be committed or included in distributed artifacts. Another developer needs authorized local access to those originals; the ledger identifies them without copying personal paths or credentials. Public catalog URLs and prior VS52 captures are supplementary, not replacements for the missing on-vehicle view.

## Exact next evidence and tracking

Keep issue58 open. Next action is evidence acquisition, not geometry:

1. Obtain a clear left-rear view beneath the EVP showing the regulator body and both feet, then an underside/rear view tracing the support continuously to its engine receiver. Include a wider context view; document any removals.
2. Record the installed regulator and bracket markings, attachment locations and every removed fastener/pad separately. Use an applicable factory parts illustration to confirm receiver and hardware identities.
3. Measure ear spacing/bore size, bracket thickness and offsets, receiver-hole centers, fastener thread/length and engagement relative to named engine datums. State measurement method and uncertainty; photographs without a scale establish appearance only.

After those inputs exist, agree an interface contract and a separate candidate scope. Preserve current EVR placement until that review. No process running at handoff; no issue comment/PR/commit performed by this worker. Usage/billing unavailable.
