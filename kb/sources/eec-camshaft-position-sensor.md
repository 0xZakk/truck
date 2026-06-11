---
title: "Camshaft Position (CMP) Sensor and PIP Signal — Operation and Specs (FSM)"
source: "manuals/factory-service-manual/1994 Ford F 150 2WD Pickup L6-300 4.9L/Repair%20and%20Diagnosis/Powertrain%20Management/Computers%20and%20Control%20Systems/Camshaft%20Position%20Sensor/Description%20and%20Operation/index.html"
type: local
date: 2026-06-11
author: "Ford Factory Service Manual"
tags:
  - cmp
  - camshaft-position-sensor
  - pip
  - hall-effect
  - distributor
  - ignition
processed: true
---

## Summary

On the 4.9L the Camshaft Position (CMP) sensor lives inside the distributor and uses a Hall
effect switch with a camshaft-driven 6-bladed shutter plate to provide crankshaft position,
base timing, and engine speed. It feeds the Ignition Control Module (ICM), which converts it
into the Profile Ignition Pickup (PIP) signal supplied to the PCM. The PCM uses PIP for fuel
injector timing and for calculating ignition timing advance and dwell.

Each shutter blade corresponds to a crankshaft position. As the plate passes through the Hall
switch, the output alternates between 0.0 and 12.0 V in a square wave; the ICM derives PIP from
this. Because the CMP/distributor drives both injector timing and spark, it sits at the heart
of both the ignition and fuel subsystems.

## Key Points

- Hall effect switch + 6-blade shutter plate inside the distributor.
- Provides crank position, base timing, engine speed to the ICM; ICM produces PIP for the PCM.
- PCM uses PIP for injector timing and ignition advance/dwell.
- Output is a 0.0-12.0 V square wave as blades pass the Hall switch.
- PIP spec KOEO: >8.0 V DC with Hall switch shut. PIP while cranking: 3.0-8.5 V AC.

## Notable Excerpts

> "As the shutter plate passes through the hall effect switch the output of the sensor alternates from 0.0 to 12.0 volts in a square wave pattern. This output is sent to the ICM where it is converted to the PIP signal."

Relates to truck inventory systems `ignition` and `fuel`.

Source: manuals/factory-service-manual/1994 Ford F 150 2WD Pickup L6-300 4.9L/Repair%20and%20Diagnosis/Powertrain%20Management/Computers%20and%20Control%20Systems/Camshaft%20Position%20Sensor/Description%20and%20Operation/index.html
