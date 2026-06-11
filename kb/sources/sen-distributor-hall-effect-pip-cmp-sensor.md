---
title: "Distributor Hall-Effect Sensor — PIP, Camshaft Position, and Cylinder Identification (FSM)"
source: "manuals/factory-service-manual/1994 Ford F 150 2WD Pickup L6-300 4.9L/Repair%20and%20Diagnosis/Sensors%20and%20Switches/Sensors%20and%20Switches%20-%20Powertrain%20Management/Sensors%20and%20Switches%20-%20Ignition%20System/Hall%20Effect%20Sensor/Description%20and%20Operation/index.html"
type: local
date: 2026-06-11
author: "Ford Factory Service Manual"
tags:
  - hall-effect-sensor
  - pip
  - camshaft-position-sensor
  - cylinder-identification
  - ignition
processed: true
---

## Summary

The 1994 4.9L's primary engine-position signal comes from a single Hall-effect sensor inside the
distributor, called the Profile Ignition Pickup (PIP). A camshaft-driven 6-bladed (6-vane)
shutter plate passes through the Hall switch; as each vane enters the stator gap it alters the
magnetic field and switches the output, producing a square wave that swings 0.0 to 12.0 V. This
signal carries crankshaft position, base timing, and engine speed.

The FSM describes this one sensor under three names because it serves three roles. As the
**Hall Effect Sensor / PIP** it provides the basic on/off position pulse. As the **Camshaft
Position (CMP) sensor** it supplies crankshaft position, base timing, and engine-speed
information to the Ignition Control Module (ICM), which converts it into the PIP signal sent to
the PCM for fuel-injector timing and spark advance/dwell. As the **Cylinder Identification
(CID) sensor**, the shutter for number 1 cylinder is made narrower than the others, producing a
"signature" PIP pulse the PCM uses to identify when #1 is on its compression stroke and to
sequence the two injector banks correctly.

Because it is the camshaft-driven part inside the distributor, the CMP/CID can be serviced
separately. Related DTC: 214, Cylinder Identification (CID) circuit failure.

## Key Points

- One distributor Hall-effect sensor (PIP) does crankshaft position, base timing, and rpm.
- 6-vane camshaft-driven shutter plate switches the Hall output 0.0–12.0 V as a square wave.
- The ICM processes the Hall signal into the PIP signal for the PCM.
- Number 1 cylinder's shutter is narrower, creating a "signature" PIP for cylinder identification.
- CID lets the PCM time sequential/banked injector firing to compression stroke on #1.
- CMP/CID is inside the distributor and serviceable separately; DTC 214 = CID circuit failure.

## Notable Excerpts

> "When a rotor vane ENTERS the space between the two halves of the stator pick-up, the magnetic
> field is altered, turning ON the signal to the PCM. When the vane LEAVES the stator gap, the
> magnetic field returns to normal, and the signal to the PCM is turned OFF."

> "The shutter corresponding to number 1 cylinder has a narrower width than the others. This
> produces a signature Profile Ignition Pickup (PIP) signal, which allows the PCM to distinguish
> number 1 cylinder from the rest."

Source: manuals/factory-service-manual/1994 Ford F 150 2WD Pickup L6-300 4.9L/Repair%20and%20Diagnosis/Sensors%20and%20Switches/Sensors%20and%20Switches%20-%20Powertrain%20Management/Sensors%20and%20Switches%20-%20Ignition%20System/Hall%20Effect%20Sensor/Description%20and%20Operation/index.html ; and ../Computers%20and%20Control%20Systems/Camshaft%20Position%20Sensor/Description%20and%20Operation/index.html ; and ../Computers%20and%20Control%20Systems/Cylinder%20Identification%20Sensor/Description%20and%20Operation/index.html
