---
title: "Heating & A/C"
kind: map
system_id: hvac
tags:
  - hvac
---

Heater core, blower, A/C, ducts, controls.

This map is the entry point for the **heating & a/c** system of the truck. As notes are added
(via `kb-process`), link the load-bearing ones below.

## Key Notes

- [[notes/hvc-charging-from-14-oz-cans-jumper-the-pressure-switch|Charge from cans by jumpering the pressure switch and running the A/C to 2.0 lb]]  ·  _procedure_
- [[notes/hvc-evacuate-to-28-29-in-hg-adjusting-for-altitude|Evacuate the A/C system to 28–29.5 in Hg at sea level, minus 1 in Hg per 1000 ft of altitude]]  ·  _procedure_
- [[notes/hvc-vacuum-reservoir-leak-down-test|Leak-test the HVAC vacuum reservoir: under 0.5 in Hg loss in 60 seconds]]  ·  _procedure_
- [[notes/hvc-oil-charge-meters-replacement-oil-from-drained-amount|Oil charge meters new refrigerant oil from how much drained from the compressor]]  ·  _procedure_
- [[notes/hvc-r-134a-service-ports-are-quick-connect-with-special-sockets|R-134a service ports are a one-piece design needing special socket tools and adapters]]  ·  _spec_
- [[notes/hvc-recover-refrigerant-until-vacuum-holds-two-minutes|Recover refrigerant until the system holds vacuum for two minutes]]  ·  _procedure_
- [[notes/hvc-compressor-clutch-air-gap-spec|The A/C compressor clutch air gap must be 0.018–0.033 in]]  ·  _spec_
- [[notes/hvc-system-uses-r-134a-and-pag-oil|The A/C system holds 2.0 lb of R-134a and 7.0 oz of PAG oil]]  ·  _spec_
- [[notes/hvc-vacuum-harness-is-color-coded-nylon|The HVAC vacuum harness is color-coded nylon tubing repairable with 5/32 or 7/32 rubber hose]]  ·  _spec_
- [[notes/hvc-pcm-trims-idle-air-when-the-ac-clutch-engages|The PCM raises idle air when the A/C clutch engages to keep idle speed from sagging]]
- [[notes/hvc-the-wot-relay-cuts-ac-at-wide-open-throttle|The WOT A/C relay drops the compressor clutch at wide-open throttle]]
- [[notes/hvc-blower-resistor-sets-the-lower-fan-speeds|The blower resistor drops voltage for the lower fan speeds, so a failed resistor leaves only HIGH]]
- [[notes/hvc-control-assembly-runs-blower-air-doors-and-clutch|The dash control assembly runs the blower, air-door vacuum, and (with the PCM) the A/C clutch]]
- [[notes/hvc-the-pressure-switch-protects-the-clutch-coil-at-low-suction|The refrigerant pressure switch cuts the clutch coil below 24.5 psi suction]]
- [[notes/hvc-vacuum-reservoir-holds-air-door-position-under-load|The vacuum reservoir keeps the air doors in position when manifold vacuum drops]]
- [[notes/hvc-manifold-bolt-torque-and-o-ring-leak-test|Torque the compressor manifold bolt to 13–17 ft lb before condemning the O-rings]]  ·  _procedure_
- [[notes/hvc-halogen-leak-detector-probe-under-the-line|Use a halogen leak detector by sweeping under the line at one inch per second]]  ·  _procedure_

## Common Issues

- [[notes/hvc-shaft-seal-leak-vs-center-joint-leak|A compressor shaft-seal leak is reseal-able, but a center-joint leak means a new compressor]]  ·  _troubleshooting_
- [[notes/hvc-a-refrigerant-leak-shows-as-oily-residue|A refrigerant leak usually shows up as oily residue at the leak point]]  ·  _troubleshooting_
- [[notes/hvc-diagnose-ac-by-pressures-and-clutch-cycle-time|Diagnose A/C performance by comparing pressures and clutch cycle time to the FSM charts]]  ·  _troubleshooting_
- [[notes/hvc-r-134a-handling-safety-rules|R-134a is non-flammable but combustible with air under pressure, and freezes skin on contact]]  ·  _troubleshooting_

## Sources

- [[sources/hvc-blower-and-controls|Blower Motor, Resistor, Switch, and Control Assembly (FSM)]]
- [[sources/hvc-compressor-and-clutch|A/C Compressor and Clutch (FSM)]]
- [[sources/hvc-compressor-clutch-controls|A/C Compressor Clutch Controls — Relay and Pressure Switch (FSM)]]
- [[sources/hvc-refrigerant-and-service-specs|A/C Refrigerant, Oil, and Service Port Specifications (FSM)]]
- [[sources/hvc-system-performance-diagnosis|A/C System Performance Test and Pressure Diagnosis (FSM)]]
- [[sources/hvc-system-service-procedures|A/C System Service — Recovery, Evacuation, Charging, Oil and Leak Detection (FSM)]]
- [[sources/hvc-vacuum-control-system|HVAC Vacuum Control System — Reservoir and Harness (FSM)]]
