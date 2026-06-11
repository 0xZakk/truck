---
title: "Knock Sensor (KS) — Operation, DTC, and Specs (FSM)"
source: "manuals/factory-service-manual/1994 Ford F 150 2WD Pickup L6-300 4.9L/Repair%20and%20Diagnosis/Powertrain%20Management/Computers%20and%20Control%20Systems/Knock%20Sensor/Description%20and%20Operation/index.html"
type: local
date: 2026-06-11
author: "Ford Factory Service Manual"
tags:
  - knock-sensor
  - detonation
  - piezoelectric
  - ignition
  - eec-iv
processed: true
---

## Summary

The Knock Sensor (KS) senses ignition detonation (ping) and reports it to the PCM, which uses
the input to optimize ignition timing while reducing detonation and minimizing NOx. It is a
thin piezoelectric ceramic disc bonded to a metal diaphragm with a two-pin connector, tuned to
resonate at roughly engine-knock frequency (5-6 kHz). As it resonates it converts the vibration
to a voltage of equal frequency sent directly to the PCM.

The KS is self-generating — it needs no power supply; the PCM provides its ground through SIG
RTN. The single related self-test code (25/225) is set when the PCM does not sense a KS signal
during the dynamic-response (snap-throttle) portion of the KOER self-test, where the PCM
advances timing and checks for a corresponding KS output.

## Key Points

- Piezoelectric ceramic disc on a metal diaphragm, two-pin connector, tuned to ~5-6 kHz.
- Self-generating voltage; no power supply; PCM grounds it via SIG RTN.
- PCM retards/optimizes ignition timing from KS input, reducing detonation and NOx.
- DTC 25/225: KS signal not sensed during KOER (snap-throttle advances timing to provoke knock).
- Electrical: pin 23 to pin 46 reads 2.4-2.6 V DC at KOEO. Torque: 20-27 Nm (15-20 ft lb).

## Notable Excerpts

> "The sensor is designed to resonate at approximately the same frequency as the engine knock (5-6 KHz)... it converts the sound vibration to an electrical voltage with an equal frequency."

> "The KS generates its own voltage and does not require a separate power supply."

Relates to truck inventory systems `ignition` and `engine`.

Source: manuals/factory-service-manual/1994 Ford F 150 2WD Pickup L6-300 4.9L/Repair%20and%20Diagnosis/Powertrain%20Management/Computers%20and%20Control%20Systems/Knock%20Sensor/Description%20and%20Operation/index.html
