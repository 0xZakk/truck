# Component contract and handoff: engine control electrical map

## Contract

Engine #32; research-only assignment from root, sole integration owner. Baseline `fbd453c66cff813cfc84fb18f88e1d1ecc560ee4`, shared branch `engine/timing-drive-fit`. Owned files are this handoff and `reference/engine/engine-control-electrical-map.json`. Existing ignition map, geometry, inventory and shared manifest remain unchanged. No dimensions, poses, CAD, wire routing or installation are authorized by this delivery; coordinate and mesh gates are N/A.

Application: purchased 1994 Ford Bronco/F-Series EVTM, 4.9L engine sheets, F-Series/manual branches for the owner's VIN-Y truck. Emissions calibration and actual harness condition remain unknown. Input `manuals/evtm/1994-Bronco-F-Series-EVTM.pdf`, SHA-256 `1adf3f3fbe35b98746dd4e8ded5c5b32fb9daaec2eb8e6f02ac91d2efb2edb54`, available locally but intentionally not distributed. PDF skill used: extracted text for navigation and actual page renders for connections. This is a short derived interface map, not redistribution of purchased diagrams.

## Evidence ledger

| PDF page, 1-based | Printed page | Reviewed evidence |
|---|---|---|
|74|23-1|PCM relay supply and supply splice|
|75|23-2|IAC, EGR solenoid and shared supply|
|76|23-3|Six injectors and single heated oxygen sensor|
|77|23-4|MAP, EVP, TPS; reference and signal return|
|78|23-5|ECT, IAT and shared return|
|81|23-8|C185 face and PCM pins1–30|
|82|23-9|PCM pins30–60 and injector groups|
|298|150-1|C101 cavity/circuit mapping|

All are primary diagram facts. The following numbers after C185/C101 are actual connector cavities. Component connector cavities are **unknown**, not assigned by the vertical position of a schematic terminal. C125 and C1003 intermediate cavity numbers remain unknown.

| Physical interface | Circuit/color and PCM connection | Shared path |
|---|---|---|
|Injector1 C190,3 C192,5 C194; each two contacts|361 R supply;555 T → C185/58|Supply S158; driver S160 → C125 → C101/12|
|Injector2 C191,4 C193,6 C195; each two contacts|361 R supply;556 W → C185/59|Supply S158; driver S159 → C125 → C101/13|
|IAC C1007; two contacts|361 R;264 W/LB → C185/21|S144 supply; control C101/4|
|EVR/EGR control solenoid C180; two contacts|361 R;360 BR/PK → C185/33|S144 supply; control C101/3|
|MAP C1011; three contacts|351 BR/W → C185/26;359 GY/R → C185/46;358 LG/BK → C185/45|Reference S163 and return S137; no C101 crossing drawn on these MAP branches|
|EVP C182; three contacts|351 BR/W → C185/26;359 GY/R → C185/46;352 BR/LG → C185/27|Reference S135 → C101/38 → S163; return S161 → C101/39 → S137; signal C101/27|
|TPS C1026; three contacts|Same351/359;355 GY/W → C185/47|Same reference/return paths as EVP; signal C101/37|
|ECT C183; two contacts|359 GY/R → C185/46;354 LG/R → C185/7|Return S138 → C125 → S161 → C101/39 → S137; signal C125 → C101/5|
|IAT C164; two contacts|359 GY/R → C185/46;743 GY → C185/25|Same return as ECT; signal C125 → C101/6|
|HO2S C1025; four contacts|298 P/O heater supply;57 BK heater ground;74 GY/LB → C185/29;89 O → C185/49|All through inline C1003. Supply S105/fuseE15A hot in RUN; heater return S100/G101; signal S165; oxygen ground S122 on23-4|

Injector supply reaches S158 through C125 from the361 continuation. The upstream361 supply passes C101/23 and S144. It is shared with additional solenoid branches, not exclusive to the requested components. The diagrams establish two injector driver groups; they do not establish injection timing or a separate driver per cylinder.

There are **14 target component connector interfaces and33 drawn component contacts**, before counting shared C101/C125/C1003 and PCM C185. Connector IDs denote mating interfaces, not a complete purchasable connector BOM: housing halves, locks, seals, individual terminals and spare cavities require separate evidence. C1003 is inline in the oxygen harness, not a second sensor. IAT is this source's name for the requested ACT/IAT function; do not create two temperature sensors from the aliases. EVP and EVR are genuinely separate sensor and actuator interfaces.

## Source conflicts and variant boundaries

23-2 continuationK says FROM S122 ON PAGE23-1. Actual23-1 shows the361 R relay supply splice as **S136**. S122 on23-4 is89 O oxygen-sensor ground. Preserve the printed discrepancy: continuationK/circuit361 establishes the supply path, but the conflicting splice label must never merge supply361 and oxygen-ground89. No silent source correction is made in the structured record.

23-9 calls PCM33 EGR Control Solenoid Input, while23-2 depicts its connection to the solenoid winding. The map retains the connection as actuator control without inferring a waveform from that inconsistent direction label.

359 is PCM46 **sensor signal return**;89 is PCM49 **oxygen-sensor ground**;57 is heater/chassis ground throughG101. Do not collapse these into one external chassis wire. The diagram also shows diagnostic branches:74 atS165 goes to unusedC103;89 atS122 goes toC103 with an all-except-Bronco applicability label. F-Series retains that unused branch, not another oxygen sensor.359 also feeds diagnosticC198; its E4OD branch is not selected for this manual truck.

The E4OD-only wiring on23-2 is excluded. AIRD/AIRB, canister purge and knock connections are adjacent drawn branches, outside this target count; omission here is not a vehicle absence claim. MAP's descriptive box mentions atmospheric pressure and transmission operation, but its circuit is explicitly labeled MAP. It does not resolve vacuum-hose routing or justify replacing the device with a different calibration. No wire gauge, connector terminal part number, seal, harness length, physical route, resistance table or diagnostic test threshold is inferred.

## Delivery, validation and restart

Structured delivery: `reference/engine/engine-control-electrical-map.json`; one record per target connector with one record per contact, explicit null component cavity values and source page index. JSON syntax, unique14 component connectors and33 contact count checked. Source/application review PASS within the stated common4.9L/manual scope; connector-specific cavity orientation and actual calibration unresolved. Installed wiring tests, learning integration and browser NOT RUN. CAD/export, physical motion and dimensions N/A for this research delivery. Original ignition research is untouched.

Reproduce visual review with `pdftoppm -f 74 -l 78 -scale-to 2400 -png manuals/evtm/1994-Bronco-F-Series-EVTM.pdf /tmp/engine-control-electrical-map` and the other indexed pages. Temporary images are not delivery dependencies; authorized source access is. Python3 JSON parser supplies structural verification. Root review pending; no model or installed acceptance. Next action: root reviews source paths and conflict handling, then obtains applicable keyed connector faces/terminal service details before harness CAD. No running processes. Usage unavailable; #32 remains open.

## Integration-owner review

Root independently rendered and inspected all eight indexed pages, verified the purchased source hash, and compared all33 circuit/color/PCM/C101 tuples. Bounded research accepted; `inventory/engine/engine-control-electrical-map-root-review.json` binds this revision. The conflicting supply-splice label remains explicit, and no component cavity number was invented. Physical connector internals, wire routes and installed/browser gates remain open. This review does not install wiring or close #32.
