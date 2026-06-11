---
title: "Main Relay (Computer/Fuel System) / PCM Power Relay — Description and Operation (FSM)"
source: "manuals/factory-service-manual/1994 Ford F 150 2WD Pickup L6-300 4.9L/Repair%20and%20Diagnosis/Relays%20and%20Modules/Relays%20and%20Modules%20-%20Powertrain%20Management/Relays%20and%20Modules%20-%20Fuel%20Delivery%20and%20Air%20Induction/Main%20Relay%20%28Computer%2FFuel%20System%29/Description%20and%20Operation/index.html"
type: local
date: 2026-06-11
author: "Ford Factory Service Manual"
tags:
  - pcm-power-relay
  - main-relay
  - relays-and-modules
  - reverse-polarity-protection
  - pcm
processed: true
---

## Summary

The Main Relay (Computer/Fuel System), referred to in the FSM as the PCM power relay, supplies
battery voltage to the Powertrain Control Module (PCM). Its purpose is to power the PCM and, by
its design, to provide reverse battery (reverse polarity) protection for the PCM and the related
actuator assemblies it drives.

Mechanically the relay is a single-pole double-throw (SPDT) type. Notably, this relay does not
contain an internal diode; it is used together with a separate stand-alone diode for coil
suppression. In operation, the relay is energized in RUN or START through the ignition switch.
When energized, battery voltage (B+) flows through the relay to power the PCM and its outputs.
When the ignition switch is turned OFF, the relay de-energizes and B+ to the PCM is removed.

The FSM does not provide a standalone pinpoint test on the component page; pinpoint testing is
located at the system level under Powertrain Management / Computers and Control Systems / Testing
and Inspection / Pinpoint Tests / B - Vehicle Battery.

## Key Points

- The PCM power relay supplies B+ to the PCM and provides reverse-battery protection.
- Construction is single-pole double-throw; it has no internal diode and uses a separate diode.
- It is energized in RUN or START through the ignition switch and de-energizes at key OFF.
- Pinpoint testing lives at the system level (Pinpoint Test B - Vehicle Battery).
- This relay belongs to the `electrical-body` power-distribution and `electrical-starting` chains.

## Notable Excerpts

> "The PCM power relay also provides reverse battery protection for the PCM and related actuator
> assemblies."

> "The relay is a single pole double throw type. This relay does not have an internal diode and is
> used with a separate stand alone diode."

Source: `manuals/factory-service-manual/1994 Ford F 150 2WD Pickup L6-300 4.9L/Repair%20and%20Diagnosis/Relays%20and%20Modules/Relays%20and%20Modules%20-%20Powertrain%20Management/Relays%20and%20Modules%20-%20Fuel%20Delivery%20and%20Air%20Induction/Main%20Relay%20%28Computer%2FFuel%20System%29/`
