---
title: "Knock Sensor (KS) — Description, Operation, and DTC (FSM)"
source: "manuals/factory-service-manual/1994 Ford F 150 2WD Pickup L6-300 4.9L/Repair%20and%20Diagnosis/Sensors%20and%20Switches/Sensors%20and%20Switches%20-%20Powertrain%20Management/Sensors%20and%20Switches%20-%20Ignition%20System/Knock%20Sensor/Description%20and%20Operation/index.html"
type: local
date: 2026-06-11
author: "Ford Factory Service Manual"
tags:
  - knock-sensor
  - detonation
  - ignition
  - eec-iv
processed: true
---

## Summary

The Knock Sensor (KS) senses ignition detonation (ping) and reports it to the PCM, which uses
the signal to optimize ignition timing while limiting spark detonation and minimizing NOx. It
is a self-generating sensor: a thin circular piezoelectric ceramic disc bonded to a metal
diaphragm, with a two-pin integral connector. It needs no power supply — the PCM only provides
the sensor ground through the SIG RTN circuit.

The sensor is tuned to resonate at roughly the same frequency as engine knock (5–6 kHz). When
that vibration reaches the disc it resonates and converts the sound to a voltage of equal
frequency, sent directly to the PCM. The PCM responds by retarding timing to stop the knock.

Only one DTC is associated: 25/225, set when the KS signal is not detected during the Key On
Engine Running (KOER) self-test. During the snap-throttle portion of KOER the PCM deliberately
advances timing to induce a little knock and watches for the corresponding KS output — so a
silent sensor or open circuit shows up as 25/225.

## Key Points

- Self-generating piezoelectric sensor; needs no power, only a SIG RTN ground.
- Tuned to resonate at the ~5–6 kHz frequency of engine knock.
- Converts knock vibration to a voltage of equal frequency sent straight to the PCM.
- PCM retards timing on knock and uses KS to limit detonation and NOx.
- DTC 25/225: no KS signal sensed during KOER self-test (PCM advances timing to provoke knock).

## Notable Excerpts

> "The sensor is designed to resonate at approximately the same frequency as the engine knock
> (5-6 KHz). As the piezoelectric disk resonates it converts the sound vibration to an electrical
> voltage with an equal frequency."

> "The KS generates its own voltage and does not require a separate power supply. The PCM
> supplies the sensor ground through the SIG RTN circuit."

Source: manuals/factory-service-manual/1994 Ford F 150 2WD Pickup L6-300 4.9L/Repair%20and%20Diagnosis/Sensors%20and%20Switches/Sensors%20and%20Switches%20-%20Powertrain%20Management/Sensors%20and%20Switches%20-%20Ignition%20System/Knock%20Sensor/Description%20and%20Operation/index.html
