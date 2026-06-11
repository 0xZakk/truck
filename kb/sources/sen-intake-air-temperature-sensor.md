---
title: "Intake Air Temperature (IAT) Sensor — Description, Operation, and DTCs (FSM)"
source: "manuals/factory-service-manual/1994 Ford F 150 2WD Pickup L6-300 4.9L/Repair%20and%20Diagnosis/Sensors%20and%20Switches/Sensors%20and%20Switches%20-%20Powertrain%20Management/Sensors%20and%20Switches%20-%20Computers%20and%20Control%20Systems/Air%20Temperature%20Sensor%20%28%20Ambient%20%2F%20Intake%20%29/Description%20and%20Operation/index.html"
type: local
date: 2026-06-11
author: "Ford Factory Service Manual"
tags:
  - iat
  - air-temperature-sensor
  - thermistor
  - fuel
  - eec-iv
processed: true
---

## Summary

The Intake Air Temperature (IAT) sensor measures the temperature of incoming air in the intake
flow path. It is a two-lead negative-temperature-coefficient thermistor — electrically identical
to the ECT and sharing the same descriptive schematic — and the PCM uses its reading to adjust
fuel injection base pulse width, EGR flow, and ignition timing. Cold, dense air carries more
oxygen per volume, so the PCM leans on IAT to fine-tune fueling and spark for air density.

The PCM applies 5.0 V reference to the signal lead with a common SIG RTN ground. As intake air
warms, resistance and the voltage across the sensor fall; as it cools, both rise. Normal output
runs from about 3.50 V at 50°F to about 1.02 V at 158°F. As with the ECT, the negative
coefficient means added harness or ground resistance makes air look much colder than it is.

Self-test DTCs: 64/112 below the 0.2 V minimum, 54/113 above the 4.6 V maximum, and 24/114 out
of the 0.3–3.7 V self-test range. The resistance/voltage-vs-temperature table is shared with the
ECT and provided only as an image.

## Key Points

- Two-lead negative-coefficient thermistor in the intake air path; same circuit as the ECT.
- 5.0 V VREF, common SIG RTN ground.
- Normal output ~3.50 V at 50°F to ~1.02 V at 158°F.
- Adjusts fuel base pulse width, EGR flow, and ignition timing for air density.
- A high-resistance circuit reads falsely cold, like the ECT.
- DTCs: 64/112 below 0.2 V, 54/113 above 4.6 V, 24/114 out of 0.3–3.7 V range.

## Notable Excerpts

> "As the temperature of the incoming air increases the resistance of the IAT decreases and the
> voltage drop across the IAT decreases."

> "The normal operating range of the IAT is 3.50 volts (50°F) to 1.02 volts (158°F)."

Source: manuals/factory-service-manual/1994 Ford F 150 2WD Pickup L6-300 4.9L/Repair%20and%20Diagnosis/Sensors%20and%20Switches/Sensors%20and%20Switches%20-%20Powertrain%20Management/Sensors%20and%20Switches%20-%20Computers%20and%20Control%20Systems/Air%20Temperature%20Sensor%20%28%20Ambient%20%2F%20Intake%20%29/Description%20and%20Operation/index.html
