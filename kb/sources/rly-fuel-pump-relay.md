---
title: "Fuel Pump Relay — Description, Operation and Testing (FSM)"
source: "manuals/factory-service-manual/1994 Ford F 150 2WD Pickup L6-300 4.9L/Repair%20and%20Diagnosis/Relays%20and%20Modules/Relays%20and%20Modules%20-%20Powertrain%20Management/Relays%20and%20Modules%20-%20Fuel%20Delivery%20and%20Air%20Induction/Fuel%20Pump%20Relay/Description%20and%20Operation/index.html"
type: local
date: 2026-06-11
author: "Ford Factory Service Manual"
tags:
  - fuel-pump-relay
  - relays-and-modules
  - pcm
  - inertia-switch
  - fuel
processed: true
---

## Summary

The fuel pump relay on the 1994 F-150 is not a simple on/off switch; it is a PCM-controlled
relay whose ground side is opened and closed by the Powertrain Control Module (PCM) as a safety
interlock. When the ignition switch is turned ON, the Electronic Engine Control (EEC) power relay
energizes and supplies power to the fuel pump relay for 1 to 2 seconds through the PCM and an
Inertia Fuel Shutoff (IFS) switch, priming the fuel rail.

Continued pump operation depends on the PCM seeing an ignition (rpm) signal. If the PCM does not
receive an ignition signal within approximately one second of key-on, a timer circuit in the PCM
opens the relay ground, the relay contacts open, and power to the pump stops. Turning the key to
START closes the ground again and the pump resumes; returning to RUN keeps power flowing through
the relay contacts. While running, the PCM opens the fuel pump relay ground circuit if engine
speed drops below 120 rpm.

The FSM directs diagnosis of this circuit through the system-level Diagnostic Routines (Diagnosis
by Symptom) under Powertrain Management / Computers and Control Systems / Testing and Inspection
rather than a standalone component test.

## Key Points

- Power reaches the fuel pump relay via the EEC power relay, through the PCM and the IFS switch.
- Key-on primes the pump for 1-2 seconds, then the PCM requires an rpm signal to keep it running.
- No ignition signal within ~1 second after key-on causes the PCM timer to open the relay ground.
- The PCM opens the relay ground (kills the pump) when engine speed drops below 120 rpm.
- Relevant to truck inventory system `electrical-body` for the wiring/relay distribution side.

## Notable Excerpts

> "When the ignition switch is turned ON, the Electronic Engine Control (EEC) power relay is
> energized, providing power to the fuel pump relay for 1 to 2 seconds through the Powertrain
> Control Module (PCM) and an Inertia Fuel Shutoff (IFS) switch."

> "The PCM monitors engine speed and opens the fuel pump relay ground circuit if the engine speed
> drops below 120 rpm."

Source: `manuals/factory-service-manual/1994 Ford F 150 2WD Pickup L6-300 4.9L/Repair%20and%20Diagnosis/Relays%20and%20Modules/Relays%20and%20Modules%20-%20Powertrain%20Management/Relays%20and%20Modules%20-%20Fuel%20Delivery%20and%20Air%20Induction/Fuel%20Pump%20Relay/`
