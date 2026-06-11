---
title: "EEC DTCs 112-195 — Air, Fuel, and Sensor Input Codes (FSM)"
source: "manuals/factory-service-manual/1994 Ford F 150 2WD Pickup L6-300 4.9L/Repair%20and%20Diagnosis/A%20L%20L%20%20Diagnostic%20Trouble%20Codes%20%28%20DTC%20%29/Testing%20and%20Inspection/Manufacturer%20Code%20Charts/111-128/index.html"
type: local
date: 2026-06-11
author: "Ford Factory Service Manual"
tags: [dtc, iat, ect, tps, map, maf, oxygen-sensor, adaptive-fuel, fuel]
processed: true
---

## Summary

The 100-series and low-100s DTCs cover the analog sensor inputs the PCM uses to meter fuel
and the closed-loop fuel feedback from the heated oxygen sensors. Temperature sensor codes
appear in pairs: a "below minimum voltage / 254°F indicated" code (a shorted circuit, since
these sensors drop voltage as they warm) and an "above maximum voltage / -40°F indicated"
code (an open circuit). For the Intake Air Temperature sensor these are DTC 112 (low) and
113 (high); for the Engine Coolant Temperature sensor they are 117 (low) and 118 (high).
Codes 114 and 116 flag IAT/ECT readings that are simply higher or lower than expected.

The Throttle Position sensor follows the same low/high pattern: DTC 122 (below minimum
voltage) and 123 (above maximum voltage) are circuit faults, while 121, 124, and 125 are
"voltage higher/lower than expected" rationality codes (124/125 route to the in-range G
pinpoint test). The Manifold Absolute Pressure / Barometric Pressure sensor produces 126
(out of expected range), 128 (vacuum hose damaged or disconnected), and 129 (insufficient
change during the KOER dynamic response test). Mass Air Flow sensor codes are 157 (below
minimum voltage), 158 (above maximum voltage), 159 (signal out of expected range), plus the
rationality pair 184 (higher than expected) and 185 (lower than expected).

The heated oxygen sensor and adaptive-fuel codes (136, 137, 171-189) report that the fuel
system has run to its adaptive limit and the HO2S can no longer switch, split by bank
(#1 / #2) and by lean/rich indication. These route to the H (Fuel Control) and HA (Adaptive
Fuel) pinpoint tests; DTC 171 and 175, for example, mean the fuel system is at its adaptive
limit and the oxygen sensor is unable to switch.

## Key Points

- Temperature codes pair low (shorted, 254°F) with high (open, -40°F): IAT 112/113, ECT 117/118.
- 114/116 = IAT/ECT higher or lower than expected (rationality), route to DA1.
- TP sensor: 122 low voltage, 123 high voltage; 121/124/125 = voltage out of expected range.
- MAP/BP: 126 out of range, 128 vacuum hose off, 129 insufficient change in KOER dynamic test.
- MAF: 157 low, 158 high, 159 out of range; 184 high / 185 low rationality.
- HO2S / adaptive fuel: 171-189 = fuel system at adaptive limit, sensor can't switch, by bank.

## Notable Excerpts

> "DTC 112 — Intake Air Temperature sensor circuit below minimum voltage, 254 degrees F indicated."

> "DTC 118 — Engine coolant temperature sensor circuit above maximum voltage / -40 degrees F indicated."

> "DTC 171 — Fuel system at adaptive limits, heated oxygen sensor unable to switch (Bank #1)."

> "DTC 128 — Manifold absolute pressure sensor vacuum hose damaged or disconnected."

Source: manuals/factory-service-manual/1994 Ford F 150 2WD Pickup L6-300 4.9L/Repair%20and%20Diagnosis/A%20L%20L%20%20Diagnostic%20Trouble%20Codes%20%28%20DTC%20%29/Testing%20and%20Inspection/Manufacturer%20Code%20Charts/ (pages 111-128, 129-171, 172-181, 184-219)
