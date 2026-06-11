---
title: "Adaptive-fuel-limit DTCs mean fuel trim hit its correction ceiling and the oxygen sensor can no longer keep the mixture balanced"
kind: troubleshooting
source: "[[sources/dtc-air-fuel-sensor-codes|EEC DTCs 112-195 — Air, Fuel, and Sensor Input Codes (FSM)]]"
related:
  - "[[notes/dtc-rationality-codes-flag-readings-that-disagree-with-other-sensors|Rationality DTCs flag a sensor reading that disagrees with the rest of the engine picture rather than a broken circuit]]"
  - "[[notes/eng-fuel-pressure-is-50-60-psi-koeo-and-45-60-running|Fuel pressure is 50-60 PSI key-on/engine-off and 45-60 PSI running at idle]]"
tags:
  - dtc
  - oxygen-sensor
  - adaptive-fuel
  - fuel-trim
  - fuel
---

The EEC continuously adjusts fuel delivery to keep the heated oxygen sensors switching
around stoichiometric — that adjustment is the adaptive fuel (fuel trim) strategy. The
171-189 block of DTCs fires when that strategy runs **out of room**: the PCM has pushed trim
to its maximum correction in one direction and the oxygen sensor still cannot be made to
switch. DTC 171 and 175 are phrased exactly that way — "fuel system at adaptive limits,
heated oxygen sensor unable to switch" — split by bank (#1 / #2). Codes 179/181 and 188/189
add whether the system reached the lean or rich adaptive limit at part throttle.

A code that says the trims maxed out trying to richen the mixture (system running lean)
points toward unmetered air or insufficient fuel: a vacuum leak, low fuel pressure, or a
weak injector. The opposite — trims maxed out trying to lean it (system running rich) —
points toward excess fuel: high fuel pressure, a leaking injector, or a contaminated MAF.
This is why these codes route to the H (Fuel Control) and HA (Adaptive Fuel) pinpoint tests,
and why H1 begins by checking for diluted engine oil, which can fool the oxygen sensor.

These codes tie the truck's `fuel` system behavior directly to the oxygen-sensor feedback
loop; confirming fuel pressure is an early step.

## Related Concepts

- [[notes/dtc-rationality-codes-flag-readings-that-disagree-with-other-sensors|Rationality DTCs flag a sensor reading that disagrees with the rest of the engine picture rather than a broken circuit]]
- [[notes/eng-fuel-pressure-is-50-60-psi-koeo-and-45-60-running|Fuel pressure is 50-60 PSI key-on/engine-off and 45-60 PSI running at idle]]

## Source

- [[sources/dtc-air-fuel-sensor-codes|EEC DTCs 112-195 — Air, Fuel, and Sensor Input Codes (FSM)]]
