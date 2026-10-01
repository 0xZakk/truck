# Component contract and handoff: ignition electrical map

Engine #32; root integration owner. Research baseline3dcbd364ac24396e671d5d16b930571713b7be0a; shared branch advanced toe6dc8fcd68e28ff201ee2cd9b69aee0bb8a588eb during review. Own ignition-electrical-map files only. No geometry, wiring, shared inventory or lesson changes. Scope:1994 Ford4.9L gasoline manual-transmission connection evidence, not a harness design or diagnostic procedure.

Primary source is the purchased1994 Bronco/F-Series EVTM, `manuals/evtm/1994-Bronco-F-Series-EVTM.pdf`, SHA1adf3f3fbe35b98746dd4e8ded5c5b32fb9daaec2eb8e6f02ac91d2efb2edb54. Original PDF and page renders remain unredistributed. PDF skill followed: text extraction for navigation, actual complete relevant pages inspected. Tables below contain short derived circuit facts, not copied pages.

## Reviewed page index

| PDF page (1-based) | Printed page | Use |
|---|---|---|
|72|21-1|Gasoline ignition connections, shield/splices, coil and capacitor|
|73|21-2|C178 distributor and C1021 ICM terminal faces|
|77|23-4|4.9L PCM ignition cross-reference|
|79|23-6|Manual/C6/E4OD clutch/start-input branches|
|81|23-8|C185 PCM face; pins4 and16|
|82|23-9|PCM pins30/36/56; C261 clutch switch face|
|298|150-1|C101 male/female terminal mapping|
|313|151-2|4.9L engine component-location view2 of3|

## Short derived connection table

| Circuit / color | Endpoints and intermediate connection | Evidence |
|---|---|---|
|395 GY/O, PIP|Distributor C178/8 → C101/18 → spliceS145; branches to ICM C1021/1 and PCM C185/56|21-1,21-2,23-9,150-1|
|929 PK, SPOUT|PCM C185/36 → removable check connectorC1019 → ICM C1021/2|21-1,21-2,23-9|
|382 Y/BK, function unresolved|PCM C185/4 ↔ ICM C1021/3; schematic labels ICM terminal START, PCM table calls circuit ICM|21-1,21-2,23-8|
|259 O/R, ignition ground|PCM C185/16 ↔ C101/19 ↔ distributor C178/7|21-1,21-2,23-8; color conflict noted below|
|16 R/LG, start/run power|Engine fuseU20A → S148; branches to ICM C1021/4 and through C101/24/S199 to distributor C178/1, coil C1008 BATT and capacitorC1017|21-1,21-2,150-1|
|11 T/Y, switched coil primary|ICM C1021/5 → C101/25 → S171 → coilC1008 switched terminal|21-1,21-2,150-1|
|648 W/PK, tach branch|S171 joins circuit11 to648 → C101/16 → C202 → instrument clusterC250/9|21-1,150-1|
|570 BK/W, ICM/distributor ground link|ICM C1021/6 → C101/30 → distributor C178/3|21-1,21-2,150-1; no additional chassis endpoint invented|
|48, shield (color unspecified)|Distributor ignition shield via C101/31 to distributor C178/2|21-1,21-2,150-1|
|481 GY/Y, manual-transmission input|Clutch C261 switched branch → C202 → PCM C185/30; input side480P/Y supplied from start branchS224/32R/LB|23-6,23-9|

C178 cavities4/5/6 are depicted unused in the reviewed face. C1021 is the six-terminal ICM connector. The EVTM calls it ICM; the map does not assume a particular TFI module construction. C1008 primary terminals are identified by circuit and BATT marking; numeric cavity numbers were not supplied on the reviewed page. C1019's two ends both carry929; no numbered cavity mapping invented. C101 male/female faces are separately shown; preserve keyed-face orientation when later modeling, rather than copying a screen-left position to a rear wire-entry view. Dimensional connector drawings and terminal part numbers remain absent.

## Variant and source conflicts

**Do not choose push-start or CCD from this map.** Circuit382 connects PCM4 to ICM3, but21-1 labels ICM3 START. No reviewed applicable page explicitly labels it IDM. Retain raw endpoint/circuit facts; `IDM` semantic assignment is unresolved pending applicable Ford Powertrain Control/Emissions Diagnosis material and actual module/PCM calibration identification. A manual gearbox does not settle that variant. The actual manual branch is the clutch circuit to PCM30; it is not evidence that ICM3 connects directly to the starter wire.

Circuit259 is O/R on21-1,21-2 and23-8; C101 face table150-1 prints O/Y for the same circuit at cavity19. The map preserves both values and uses circuit/terminal identity to join the path. Confirm on the applicable harness before color-based terminal identification.

The PCM table names pin56 as a crank-position pickup while21-1 identifies the distributor signal as PIP. That naming difference does not justify adding a separate crank sensor or rewiring the signal. General descriptive text on21-1 also loosely attributes distributor high voltage to ICM, whereas the actual drawn secondary goes coil→distributor; preserve the actual circuit topology.

The manual/C6/E4OD branches on23-6 are alternatives. Owner's manual transmission selects the C261 switch branch to481/PCM30, not the automatic jumper. The associated starter interlock and brake/cruise contacts require their own full circuit audit before harness construction. No emissions calibration, module engineering number, dwell law, connector terminal material, wire gauge, shield layup, harness length or three-dimensional route is established here.

## Use for later components and explanations

Confirmed physical interfaces to account for separately: distributorC178, six-way ICM C1021, removable SPOUT jumperC1019, coil primaryC1008, radio-noise capacitorC1017 and its grounded case, PCM60-wayC185, engine/body connectorC101 and shield/splices. Location view151-2 places ICM/C1021 atC9, SPOUT atB9, distributor/C178 atE9, coil/C1008 atF7 and capacitor/C1017 atF7. These are **illustration reference cells, not coordinates or dimensional routes**. Existing engine ignition CAD does not thereby acquire correct electrical terminals or wiring.

Explanations may distinguish speed/position input395, timing command929 and switched primary11 without inventing a waveform. Troubleshooting content should link the named circuit, terminal and supply/return relationships, preserving the382 ambiguity. No resistance, voltage-test threshold, timing setting or module interchange procedure is supplied by this research; the EVTM refers detailed diagnosis to the applicable powertrain diagnostic manual.

## Delivery and gates

Structured terminal/net records: `reference/engine/ignition-electrical-map.json`. Research/source coverage PASS scoped; module variant and conflicting labels/colors remain explicit. CAD/export, installed wiring tests, motion and browser NOT RUN; no learning integration. Reproduce page inspection with `pdftoppm -f 72 -l 73 -scale-to 2600 -png manuals/evtm/1994-Bronco-F-Series-EVTM.pdf /tmp/ignition-electrical-map-ign` and equivalent indexed pages. No purchased page imagery or bulk text is delivered. Root review pending; #32 remains open. No running processes; usage unavailable.
