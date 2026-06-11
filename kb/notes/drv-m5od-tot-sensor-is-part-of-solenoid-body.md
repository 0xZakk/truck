---
title: "The transmission temperature (TOT) sensor is a thermistor in the solenoid body, replaced only as an assembly"
kind: how-it-works
source: "[[sources/drv-manual-transmission-m5od-r2|Manual Transmission (M5OD-R2) — Component Inspection, Technical & Torque Data (FSM)]]"
related:
  - "[[notes/drv-m5od-takes-mercon-v-not-gear-oil|The F-150's M5OD 5-speed is filled with Mercon V ATF, not gear oil, and holds 7.6 pints]]"
tags:
  - transmission
  - sensor
  - tot-sensor
  - how-it-works
---

The Transmission Operating Temperature (TOT) sensor is a **thermistor** — a temperature-sensitive
resistor — located in the transmission's **solenoid body assembly**. It sends a voltage signal
that varies with transmission fluid temperature to the Powertrain Control Module (PCM).

The PCM uses that signal to pick the shift schedule and Electronic Pressure Control (EPC) settings:
when the fluid is cold, it switches to a cold-start schedule that lowers shift speeds to suit the
reduced performance of a cold engine. The TOT is **not serviced separately** — if it fails, the
whole transmission solenoid assembly is replaced. Note that this is fundamentally an electronically
controlled (automatic) transmission feature; on the manual-transmission F-150 the relevant
`driveline` takeaway is that temperature-based control logic lives in the solenoid pack, not as a
standalone sensor.

> "The Transmission Operating Temperature (TOT) sensor is a temperature-sensitive device called a
> thermistor... it is part of the transmission solenoid assembly and is not replaced separately."

## Related Concepts

- [[notes/drv-m5od-takes-mercon-v-not-gear-oil|The F-150's M5OD 5-speed is filled with Mercon V ATF, not gear oil, and holds 7.6 pints]]
- [[notes/dtc-temperature-sensor-codes-pair-low-and-high-voltage|Temperature sensor DTCs come in low/high pairs that mean shorted (254°F) or open (-40°F)]]
- [[notes/eec-ect-and-iat-are-ntc-thermistors-on-a-5v-reference|The ECT and IAT are identical two-lead NTC thermistors on a 5.0 V reference whose voltage drops as temperature rises]]
- [[notes/eec-ntc-temp-sensors-read-falsely-cold-with-bad-grounds|A bad ground or added resistance makes the NTC ECT and IAT read falsely cold, driving a needless rich condition]]

## Source

- [[sources/drv-manual-transmission-m5od-r2|Manual Transmission (M5OD-R2) — Component Inspection, Technical & Torque Data (FSM)]]
