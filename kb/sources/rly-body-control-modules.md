---
title: "Body Control Modules — Warning Chime, Alarm, Keyless Entry, Wiper, PSOM, Starter Relay (FSM)"
source: "manuals/factory-service-manual/1994 Ford F 150 2WD Pickup L6-300 4.9L/Repair%20and%20Diagnosis/Relays%20and%20Modules/Relays%20and%20Modules%20-%20Instrument%20Panel/Audible%20Warning%20Device%20Control%20Module/Description%20and%20Operation/index.html"
type: local
date: 2026-06-11
author: "Ford Factory Service Manual"
tags:
  - warning-chime
  - alarm-module
  - keyless-entry
  - wiper-module
  - psom
  - starter-relay
  - relays-and-modules
processed: true
---

## Summary

This page consolidates the smaller body/instrument-panel relays and modules in the Relays and
Modules system that have brief Description and Operation entries.

The Audible Warning Device Control Module (warning buzzer/chime module) drives the chime for
several conditions: a key-in-ignition ground signal warns the keys are still in the ignition; a
lamps-on input sounds the chime when the driver's door is opened with the lights in PARK or HEAD
(until the door closes or lights are off); a seat-belt-unbuckled input grounds an electronic timer
to sound the chime for six seconds; and a seat-belt lamp output lights the "fasten belts"
indicator for four to eight seconds at START or RUN whether or not the belts are buckled.

The Alarm Module (anti-theft controller) monitors switches throughout the vehicle; when triggered
it sounds the horn and flashes the headlamps and parking lamps at 80 cycles per minute, and it
disables the starting system until disarmed. The Keyless Entry Module arms/disarms the anti-theft
system and locks/unlocks the doors from the remote transmitter or power door lock switch;
UNLOCK/PANIC illuminates interior lamps ~25 seconds (cancelled by LOCK or turning the key to RUN),
and PANIC flashes exterior lights and sounds the horn for ~4 minutes until pressed again.

The Wiper Control Module receives signals from the multi-function switch to perform washer,
low-speed, high-speed, or interval wiper functions. The Programmable Speedometer/Odometer Module
(PSOM) houses the speedometer, odometer, and trip odometer under a programmable microprocessor; it
takes a speed input from the Differential Speed Sensor (anti-lock brake sensor) and converts it to
a standard 8000 pulses-per-mile output, and is serviceable only as a unit. The Starter Relay page
under Starting and Charging contains only a Locations entry (no description text).

## Key Points

- Warning chime: key-in, lamps-on, seat-belt-unbuckled (6 s) inputs; fasten-belts lamp 4-8 s at START/RUN.
- Alarm module flashes head/park lamps at 80 cycles/min, sounds horn, and disables starting until disarmed.
- Keyless entry: ~25 s interior lamps on UNLOCK/PANIC; PANIC flashes lights and horn for ~4 minutes.
- Wiper module decodes multi-function switch for washer, low, high, and interval modes.
- PSOM converts the ABS/differential speed sensor input to 8000 pulses/mile; serviced only as a unit.
- These body modules and the starter relay live in the `electrical-body` and `electrical-starting` networks.

## Notable Excerpts

> "The anti-theft controller module monitors switches located throughout the vehicle, and if
> triggered, it sounds the horn and flashes the headlamps and parking lamps at an intermittent rate
> of 80 cycles per minute. Then anti-theft controller module also disables the starting system
> until the anti-theft system is disarmed."

> "The microprocessor receives a speed signal input from the Differential Speed Sensor (DSS), and
> uses a programmed conversion constant to convert the signal to the standard 8000 pulses per mile
> speed signal output. The Programmable Speedometer/Odometer Module is serviceable only as a unit."

Source: `manuals/factory-service-manual/1994 Ford F 150 2WD Pickup L6-300 4.9L/Repair%20and%20Diagnosis/Relays%20and%20Modules/` (Audible Warning Device Control Module, Alarm Module, Keyless Entry Module, Wiper Control Module, Speedometer Module/PSOM, Starter Relay)
