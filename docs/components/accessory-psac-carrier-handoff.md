# Component contract and handoff: PS/AC/tensioner matched support

## Contract

- Issues #32/#34, engine; contributor pan_access_resume, root integration/review owner. Creation baseline0861e87558151b4b1bbc0d257edde17013e253f3; branch engine/timing-drive-fit. Private v3 SHA f512d6024ed4d3d0d86c45c39492b4ab525e039a9c50fb71b67940633b8a2055. Pre-build contract and route amendment: `accessory-psac-carrier-contract.md`.
- Isolated estimated load-path prototype, not manufacturing, structural or installed acceptance. Own only new prefixed files. No shared pose/inventory edits, no engine-anchor movement, no neighbor subtraction. Frozen selected centers and opposite ALT/AP trial6 remain unchanged.
- Proposed replacement identity `ps-ac-support-bracket`, parent accessory-support-brackets as existing inventory requires; root must verify original parent/frame in any later guarded patch. Candidate STEP is world-mm, identity local frame; GLB uses existing(X,Z,−Y)/1000 mapping. No automatic installation or explode metadata changes.
- Fixed engine feet and actual hardware; three PS ears, four AC ears, tensioner cartridge/locator. Complete v3 q0 neighbor scope plus proposed frozen ALT/AP trial6, rear-cover candidate and three separate pump hypotheses. Actual shaft/pulley geometry remains translated only in YZ.

## Evidence ledger

| Feature | Datum / value | Evidence class and source | Limit |
|---|---|---|---|
| Shared carrier / four engine attachments | front head, side head, two block studs | applicable Ford TSB94-10-19 Fig4; accessory_carrier_1994.py | detailed casting silhouette/sections/coordinates remain estimated |
| Frozen centers YZ | PS289.501109,346.563747; AC337.435375,140; TENS129.498190,316.277747 | coupled inferred layout | not measured production layout |
| Front head seat | X373,Y90,Z300, annulusR5.5..12 | inherited actual mate | outerR16 flange overhang not claimed fully supported |
| Side engine seats | Y135; X292/340,Z110 and X340,Z310; annulusR5.5..14 | inherited block/head model | no manufacturing threads/load claim |
| Accessory seats | X432.56; PS radius62 angles45/165/285, AC translated four axes | actual illustrative ear geometry | original centers/ears are estimates |
| Tensioner | pivotY129.498190,Z391.277747; rear padX380.56..400.56 | Gates architecture + inherited illustrative stack | optional locator choice, spring/stop/range unknown |
| Ribs/frame | source-topology ring/open frame and connected side spine | explicit estimated prototype | factory silhouette comparison required later; no stiffness/fatigue assessment |
| Tool approach |40mm straight from actual head/nut front; estimated radii | scoped tool proxy | no socket manufacturer identity; installed pulley conflicts remain |

## Delivery

Selected **trial1**, valid single solid, volume484097.984286mm³; bounds X276..446.994127,Y74..436.435375,Z41..425.563747. Parametric entry point `cad/engine/accessory_psac_carrier_trial1.py:carrier()`.

Assets under `cad/engine/generated/accessory-psac-carrier/`:

- `trial1-carrier.step`: SHA11f8047def0f76b43a08e080fc28bd2cac98e661f1612fcca82c82a23d86c8b9.
- `trial1-carrier.glb`: SHA30e1b495a3f3a7894a04f84190f65a038d9b413393e32c81967ecee22057436a.
- `trial1-review.png`: actual STEP front/oblique context, red tool/pulley interference witnesses.
- Rejected trial0 stock, exact overlap witnesses, corrected-tool reports and exact pump-separation partition assets retained.

Reports use `accessory-psac-carrier*` under inventory/engine. Final package binding: `accessory-psac-carrier-delivery.json`. No artifact release URL yet; root owns packaging. Source photographs/manual remain authorized private dependencies, not redistributed.

Reproduce from repository root using macOS Python3.13/build123d0.10 locked environment; NumPy/trimesh; system Python/matplotlib for PNG:

```sh
.venv-cad/bin/python scripts/accessory-psac-carrier-trial1-check.py
.venv-cad/bin/python scripts/accessory-psac-carrier-trial1-fasteners.py
.venv-cad/bin/python scripts/accessory-psac-carrier-distance-diagnostic.py
.venv-cad/bin/python scripts/accessory-psac-carrier-pump-separation.py
.venv-cad/bin/python scripts/accessory-psac-carrier-final-check.py
.venv-cad/bin/python scripts/accessory-psac-carrier-clamp-stacks.py
.venv-cad/bin/python scripts/accessory-psac-carrier-pulley-datums.py
.venv-cad/bin/python scripts/accessory-psac-carrier-render.py trial1 --extract
python3 scripts/accessory-psac-carrier-render.py trial1
python3 scripts/accessory-psac-carrier-freeze.py
```

No package installation; harmless local cache warnings. Model/effort/usage unavailable.

## Validation and review

| Gate | Result | Evidence / remaining limits |
|---|---|---|
| Application/coverage | PARTIAL | applicable attachment topology; factory casting comparison remains required |
| Dimensions/coordinates | PASS conditional | fixed anchors and frozen centers; actual CAD cylindrical axes match selected centers; all three crest midplanesX473.56 and axial envelopes unchanged; production/effective belt alignment unknown |
| CAD/export | PASS | one valid solid; one watertight, consistent mesh component; bounds error0.018114mm with0.08mm tessellation |
| Source/visual comparison | PARTIAL | actual render inspected; load-path prototype only |
| Installed interfaces | PASS bounded q0 geometry; not installed |172 exact neighbor pairs zero overlap;12 named support seats,15 named fastener bearing annuli fully backed; actual bolt/hole geometry checked |
| Motion/disassembly | FAIL installed straight access |3PS and4AC approaches hit pulleys; prerequisite/removal sequence unresolved; tensioner travel NOT RUN |
| Learning/diagnostics | NOT RUN | no user-facing lesson; checker controls are not learning acceptance |
| Browser integration | NOT RUN | canonical unchanged |
| Reproduction/review | hash-bound; root pending | frozen code/reports/assets, failures preserved |

Twelve support witnesses: front head, three side engine seats, three PS ears, four AC ears and tensioner cartridge rear face. The cartridge annulus excludes the declared locator bore. All have zero missing material on both owners. Fifteen independent clamp witnesses cover engine head faces, stud washers/nuts, PS/AC bolt heads, and tensioner head-to-arm/sleeve. Witness radii lie inside actual hex inscribed circles; they do not claim unsupported outer flange material. The1mm deliberately shifted front-head seat loses7.147123mm³ of witness, detecting contact loss.

Actual stack estimates: front engine engagement14mm; side engine insertion20mm; side carrier28mm, washer2mm, nut9mm, exposed stud2mm; PS ear insertion7.8mm, AC11.8mm, accessory carrier10mm. Tensioner insertion14mm and2mm tip clearance; two explicit2mm floor witnesses and both tip voids pass. Smooth shafts/bores and illustrated nuts do not establish actual threaded retention, grade, clamp load or strength.

Nonmating spacing retains1mm, intersection threshold0.1mm³. Named seats and prescribed fit clearances are distinct from nonmating space. Frozen ALT/AP trial6 is separated by a rigorous158mm Y-bound gap. Rear-cover variant clears by17.56mm. Three new pump variants clear; their reported distance96.043555mm does not install them or waive ALT/AP's separate lower-bolt access failure.

**Raw distance defect preserved:** OCC reports zero between carrier and v3 pump with closest pointX289.627/Y161/Z125.823, impossible because pump bounds beginX375 and endY113. This raw result is not accepted. An independent exact-CAD split atY120 partitions all carrier stock into valid pieces; summed volume differs by0.00002845mm³. Low-Y stock is at least33.5mm above pump; high-Y stock is at least7mm to its side. Thus a conservative7mm clearance certificate passes the unchanged1mm gate without trusting that defective distance call.

**Tool failures retained:** R10 PS approaches intersect the PS pulley approximately2464.373mm³ at each of three bolts. R11 AC approaches intersect its clutch pulley approximately374.547mm³ at each of four bolts. All carrier-only approaches clear, as do the other five modeled approaches. Removing the two obstructing pulleys leaves these checked envelopes clear of remaining modeled neighbors, but that is only a conditional access observation: installed removal/refitting tools and source-supported bracket service sequence remain unverified. The applicable PS manual begins bench pump disassembly with pulley removal; it does not prove this bracket procedure. Source locator/hash is in service-evidence report.

Initial solid nut-tool proxy falsely included2mm exposed stud tips; trial1 explicitly reserves an estimatedR5.2/3mm socket cavity. Both original proxy failure and correction remain recorded. No tolerance changed. Rejected trial0 also preserves cover1046.505mm³, cartridge497.061mm³ and side-head tool11.628mm³ interference; trial1 reroutes only estimated ribs and extends analytic tool relief. No neighboring solid is used as a cutting tool.

## Tracking and restart

Root reviews assets/render before any assembly proposal. Factory silhouette, structural adequacy, threaded retention, actual service tools/sequence, tensioner sweep, belt installation and hoses/wiring remain open. No canonical changes or installation. No process remains running at final freeze. Next action is root review, not automatic promotion. Usage unavailable.
