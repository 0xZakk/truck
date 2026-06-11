---
title: "Anti-Theft / Alarm System — Alarm Module and Arm/Disarm Switch (FSM)"
source: "manuals/factory-service-manual/1994 Ford F 150 2WD Pickup L6-300 4.9L/Repair%20and%20Diagnosis/Accessories%20and%20Optional%20Equipment/Antitheft%20and%20Alarm%20Systems/Alarm%20Module/Description%20and%20Operation/index.html"
type: local
date: 2026-06-11
author: "Ford Factory Service Manual"
tags:
  - anti-theft
  - alarm
  - alarm-module
  - arm-disarm-switch
  - electrical-body
processed: true
---

## Summary

The optional anti-theft system on the 1994 F-150 is built around an anti-theft controller
module (the "alarm module") that watches a set of switches distributed throughout the
vehicle. When the system is armed and a monitored switch is triggered, the module sounds an
audible/visual alarm and also disables the starting system so the truck cannot be driven away.
The same Description and Operation content is duplicated under the manual's "Antitheft and
Alarm Systems", "Relays and Modules - Accessories and Optional Equipment", and "Sensors and
Switches - Accessories and Optional Equipment" sections.

The arm/disarm side is handled by door disarm switches. Each switch closes (provides a ground
input to the controller) when its door is unlocked with the key, which is how a legitimate
key-holder disables the alarm. This system maps to the truck inventory `electrical-body` and
`interior` ids.

## Key Points

- The anti-theft controller module monitors switches located throughout the vehicle.
- When triggered (armed), it sounds the horn and flashes the headlamps and parking lamps at an
  intermittent rate of 80 cycles per minute.
- The module also disables the starting system until the anti-theft system is disarmed.
- The door disarm switches are closed when either door is unlocked with the key; closing a
  switch provides a ground input to the controller module, which disables the anti-theft system.
- Arming the system (via the keyless entry module's LOCK command) is documented under the
  Keyless Entry pages; the alarm module is the output stage that actually flashes lights, sounds
  the horn, and inhibits the starter.

## Notable Excerpts

> "The anti-theft controller module monitors switches located throughout the vehicle, and if
> triggered, it sounds the horn and flashes the headlamps and parking lamps at an intermittent
> rate of 80 cycles per minute."

> "Then anti-theft controller module also disables the starting system until the anti-theft
> system is disarmed."

> "Closed when either door is unlocked with the key, the door disarm switches provide a ground
> input to the anti-theft controller module, which disables the anti-theft system."

Source: manuals/factory-service-manual/1994 Ford F 150 2WD Pickup L6-300 4.9L/Repair%20and%20Diagnosis/Accessories%20and%20Optional%20Equipment/Antitheft%20and%20Alarm%20Systems/Alarm%20Module/Description%20and%20Operation/index.html (and Arm/Disarm Switch/Description and Operation/index.html)
