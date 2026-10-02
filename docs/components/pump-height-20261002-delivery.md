# Pump height candidate — failed integration handoff

## Contract and scope

Issue47 under engine1; root integration owner. Before-CAD scope and baseline are in `pump-height-20261002-handoff.md`; port parameters were frozen separately in `pump-height-20261002-ports-contract.md`. Source contract `pump-metric-20261002-contract.json` supplies replacement-comparison98.43mm and98.552mm conversion sensitivity. Existing147mm face stack is shortened; factory geometry remains unverified. No canonical/shared/frozen edits or commits.

**Readiness: candidate, FAIL integration.** Two complete52-occurrence local STEP proposals include rebuilt housing, shaft and pulley, translated hub/bearing/seal/slinger/fan components, and new estimated large-inlet/heater geometry. Impeller, gasket and mounting screws remain actualv4 neighbors. All assets are WORLD millimeter coordinates atq0; do not apply their existing occurrence transform again. Stable IDs are retained as filenames/report keys. No installation patch is provided.

## Exact assets and reproduction

Selected failed candidate: `cad/engine/pump_height_20261002_ports_trial3.py:parts(height=98.43)`; underlying short core `pump_height_20261002_core_trial3.py`. STEP assets are under `cad/engine/generated/pump-height-20261002-ports-trial3/`, prefixed `nominal-` or `inch-value-`. Report `reference/engine/pump-height-20261002-ports-trial3.json` binds each asset. Nominal GLBs only were produced; sensitivity GLBs NOT RUN. Earlier failed core, ports and portstrial2 assets/reports remain intact.

Run from repository root:

1. `.venv-cad/bin/python scripts/pump-height-20261002-ports-trial3.py`
2. `.venv-cad/bin/python scripts/pump-height-20261002-interfaces-trial3.py`
3. `.venv-cad/bin/python scripts/pump-height-20261002-neighbors-trial3.py`
4. `.venv-cad/bin/python scripts/pump-height-20261002-seats.py`
5. `.venv-cad/bin/python scripts/pump-height-20261002-mesh.py`
6. `python3 scripts/pump-height-20261002-render.py` and `python3 scripts/pump-height-20261002-render-full.py`

Existing CADPython3.13/build123d0.10/trimesh and systemPython3.13/NumPy/Matplotlib; no packages installed. CAD environment lacks Matplotlib and system environment lacks trimesh, so mesh arrays are serialized once and rendered with NumPy. Failed attempts/logs retained. GLB convention matches project: meters, vertexXYZ→X,Z,−Y; checker transforms back to CADmm. Two actual mesh renders reviewed locally at `reference/engine/pump-height-20261002-review.png` and `...-review-full.png`; source originals are not embedded.

## What the finite checks establish

- Both heights export52 valid, individually single-solid STEPs. The initially disconnected four-solid housing is preserved as a failed first trial. Its ShapeList union error was corrected by explicit solid fusion; no threshold relaxed.
- Trial3 local rebuilt-part pairs have no overlaps above0.1mm³ or metric errors. All six seal components and translated fan IDs are preserved. Same rigid translated pairs remain inherited relations, not fresh acceptance.
- Both heater sockets have603.185789mm² named cylindrical seat with zero missing area on housing and tube. Nominal hub/pulley annular seat is2982.934371mm² with zero missing area on both actual faces.
- Both finite inlet/heater lumen witnesses have zero solid obstruction. Deliberately plugged heater control overlaps5.964909mm³. Shaft axial gauge is clear; housing/tube overlap0. These are path probes, not proof of entire fluid containment, hydraulic capacity or pressure sealing.
- Actualv4 nominal audit runs90 fresh affected pairs with2mm padded actualSTEP bounds, zero metric exceptions. Prior bounds are reused only after all sourceSTEP hashes and all occurrenceq0 matrices match the frozen971-pair report.101 same translated rigid pairs are labeled inherited, not rerun or newly accepted. Sensitivity whole-stage audit NOT RUN.

## Exact failures retained

| Pair, nominal actualv4 | Overlap mm³ | Witness location |
|---|---:|---|
|Timing cover / housing|674.697840|X375..385.842,Y−5.123..20.830,Z109.721..130.439|
|Thermactor engine bolt1 / housing|427.729722|X379.065..390.479,Y−107.851..−95.100,Z84.934..99.065|
|ALT/AP common carrier / housing|3011.030497|X379..399.788,Y−130.734..−84,Z74..105.942|
|ALT/AP common carrier / heater tube|217.135106|X396.163..401,Y−141.931..−128,Z251.191..268.972|

Exact witness STEP paths and hashes are in `pump-height-20261002-neighbors-trial3.json`. V4 uses its own existing cover; no silent substitution of the separately proposed rear-cover correction. Other unchanged v4 conflicts/tool failures remain outside this fresh scope.

**Rear preservation FAIL:** portstrial3 adds13428.927226mm³ and removes2078.817820mm³ within the originally protectedX<=389 slice. Inside the analytic original joint footprint, additions598.229422mm³ and removals2078.817820mm³ remain. Clear mounting screws and impeller do not erase this failed contract. The short inlet's annular wall/void crosses the original rear material. A new source/interface review must either preserve that protected stock with a different junction or explicitly revise the contract; no such revision is implied here. Earlier four screw and impeller overlaps were resolved by retaining the original fluid cavity and drilling the declared original axes, not subtracting neighbor shapes.

**Mesh/export FAIL:** all nominal meshes except seal spring are watertight and winding-consistent. Six exceed the existing0.025mm CAD-bounds gate: clutch housing0.040940, drive rotor0.035362, partition0.038011, front cover0.040940, pulley0.033571, seal spring0.800267mm. Spring mesh is also nonwatertight. Coarse tessellation and CAD bounding behavior may contribute, but no tolerance is raised or exported-fidelity pass claimed. Raw mesh arrays and reports preserve these defects.

**Inherited retention gaps remain:** bearingOD23.9 against housingR24 and shaftR8 against bearingbore8.05 imply radial gaps0.1/0.05mm in estimated geometry. No press-fit/load support acceptance. Threads, realistic bearing internals, seal preload, fan/radiator context, hoses/clamps, disassembly access, motion and pressure capability remain unresolved.

## Quality gates and decision

| Gate | Result | Evidence/limit |
|---|---|---|
|Application/coverage|PASS scoped replacement|Primary Carter height; GMB proportion transfer remains conditional|
|Dimensions/coordinates|PARTIAL|Explicit height and WORLD frames; all other contours/internals estimated|
|CAD/export|FAIL aggregate|Valid52STEPs eachheight, sixmesh bound failures and oneopenmesh|
|Source/visual|PARTIAL|Actual whole/cutaway mesh reviewed; no production silhouette validation|
|Installed interfaces|FAIL|Four fresh overlaps; rear-preservation violation; retention gaps|
|Motion/disassembly|NOT RUN|No production or installation claim|
|Learning/diagnostics|N/A unchanged|New source notes delivered separately in metric research|
|Browser|NOT RUN|No installation|
|Reproduction/review|PASS local; root pending|Hash-bound scripts/sourceinputs/reports/assets/logs; failed trials retained|

Next action: root review of short-chamber inlet topology and conflict witnesses against the explicitly estimated carrier, while retaining the primary mounting-to-pulley height. Do not move engine anchors, return to143mm merely for clearance, carve carrier clearance into the pump, or install this candidate. No further unsupported contour search was performed. The source-side heater metric/radial ambiguity remains open.

Completed processes: core97284, correctedcore97534, ports51546, portstrial25130, interfaces95327, originalneighbors10405, finalportstrial365471, finalinterfaces91831, finalneighbors83289, mesh14135, seats97512, renders89893/73108. All completed; no live process remains. Earlier failed syntax/import/ShapeList attempts are retained in logs. Model/effort/usage unavailable. Issue47 remains open; root owns tracking and publication.
