---
title: "Keyless Entry System (Module + Transmitter) — Description, Operation and Programming (FSM)"
source: "manuals/factory-service-manual/1994 Ford F 150 2WD Pickup L6-300 4.9L/Repair%20and%20Diagnosis/Body%20and%20Frame/Locks/Keyless%20Entry/Keyless%20Entry%20Module/Description%20and%20Operation/index.html"
type: local
date: 2026-06-11
author: "Ford Factory Service Manual"
tags:
  - keyless-entry
  - anti-theft
  - door-locks
  - remote-transmitter
  - body
processed: true
---

## Summary

The 1994 F-150's optional remote keyless entry is run by a keyless entry (electronic door
lock control) module that ties together the remote transmitter, the power door lock switch,
the anti-theft system, the interior lamps, the horn, and the exterior lights. The same
module content appears under both the "Locks" and the "Relays and Modules - Body and Frame"
sections of the manual.

Pressing the remote transmitter's buttons sends signals to the module, which then drives the
lock actuators, arms or disarms the anti-theft system, and flashes/sounds the panic alarm.
Up to four transmitters can be programmed into the module using a two-pin program connector
beneath the driver's side of the instrument panel. This system maps to the truck inventory
`body-cab` and `exterior-trim` ids (locks, lamps, and exterior light/horn outputs).

## Key Points

- LOCK (transmitter or power door lock switch) arms the anti-theft system and locks the doors.
- UNLOCK or PANIC illuminates the interior lamps for ~25 seconds; LOCK or turning the ignition
  to RUN turns them off immediately.
- PANIC flashes the exterior lights and sounds the horn for ~4 minutes; a second press cancels.
- The module both arms/disarms anti-theft and locks/unlocks based on the transmitter or door
  lock switch signal.
- Programming: ignition ON, short the two terminals of program connector J2 (a two-pin
  connector below the driver's side of the instrument panel at the base of the steering
  column); doors lock then unlock to confirm program mode.
- Press a button on each transmitter, one at a time (up to 3 tries each); up to 4 transmitters
  maximum; turn ignition off and remove the short to finish.
- All of the customer's transmitters must be reprogrammed together — programming a new one
  does not preserve previously learned transmitters unless they are re-presented.

## Notable Excerpts

> "When the UNLOCK or PANIC button of the remote transmitter is pushed, the module illuminates
> the interior lamps for approximately 25 seconds."

> "When the PANIC button of the remote transmitter is pushed, a signal is sent to the
> anti-theft module to flash the exterior lights and sound the horn for approximately four
> minutes. Pressing the button a second time will de-activate the antitheft module."

> "Turn the ignition switch to the ON or ON/ACC position and short the two terminals of the
> program connector (J2)... All doors should lock and then unlock."

Source: manuals/factory-service-manual/1994 Ford F 150 2WD Pickup L6-300 4.9L/Repair%20and%20Diagnosis/Body%20and%20Frame/Locks/Keyless%20Entry/Keyless%20Entry%20Module/Description%20and%20Operation/index.html (and Keyless Entry Transmitter/Service and Repair/index.html)
