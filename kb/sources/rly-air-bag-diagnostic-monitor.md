---
title: "Air Bag Control Module (Air Bag Diagnostic Monitor) — Description and Testing (FSM)"
source: "manuals/factory-service-manual/1994 Ford F 150 2WD Pickup L6-300 4.9L/Repair%20and%20Diagnosis/Relays%20and%20Modules/Relays%20and%20Modules%20-%20Restraints%20and%20Safety%20Systems/Air%20Bag%20Control%20Module/Description%20and%20Operation/index.html"
type: local
date: 2026-06-11
author: "Ford Factory Service Manual"
tags:
  - air-bag-diagnostic-monitor
  - relays-and-modules
  - srs
  - safety
  - diagnostic-trouble-codes
processed: true
---

## Summary

The Air Bag Control Module on this truck is the Air Bag Diagnostic Monitor. Its main purpose is
system diagnostics: it continuously monitors all supplemental air bag restraint system components
and wiring connections for faults. Importantly, the diagnostic monitor does NOT deploy the air bag
in a crash — the center and RH front air bag sensors are hard-wired to the air bag and determine
deployment.

When a fault is detected with the ignition in RUN, a diagnostic trouble code is flashed on the air
bag indicator in the instrument cluster. At key-on the monitor illuminates the indicator for about
six seconds as a bulb/function check, then turns it off; an indicator that fails to light, stays
on, or flashes signals a fault. Trouble codes may not display for about 30 seconds after RUN while
the monitor completes its tests. Each code is a two-digit number shown as flashes and pauses,
repeated at least twice. If the indicator itself is inoperative and a fault exists, an audible tone
of five sets of five beeps is heard (this is not code 55).

If a fault makes unwanted deployment possible, an internal thermal fuse blows automatically,
removing all power to the deployment circuit; this fuse does not blow from excessive current and
must not be jumpered. The monitor also contains an internal backup power supply able to deploy the
air bag if the battery or cables are damaged before the sensors close — and that backup energy
depletes about one minute after the positive battery cable is disconnected.

For service, the FSM warns the backup power supply energy must be depleted before any air bag
component service: disconnect the positive battery cable and wait one minute. For a blown internal
fuse (DTC 51), find and repair all wire damage/shorts first; a blown monitor can be used to locate
faults without unnecessary part replacement, then replaced once repairs are verified.

## Key Points

- The diagnostic monitor performs diagnostics; it does NOT deploy the air bag (sensors do).
- Key-on lights the indicator ~6 seconds as a self-check; abnormal behavior indicates a fault.
- Codes may take ~30 seconds to display; each two-digit code repeats at least twice.
- An indicator-out fault with a system fault produces a tone of five sets of five beeps.
- An internal thermal fuse blows to prevent unwanted deployment; never jumper it.
- Backup power depletes ~1 minute after disconnecting the positive battery cable — wait before service.
- This SRS module is part of the `electrical-body` safety-system wiring.

## Notable Excerpts

> "The air bag diagnostic monitor does not deploy the air bag in the event of a crash. The center
> and RH front air bag sensors are 'hard wired' to the air bag..."

> "The backup power supply will deplete its stored energy approximately one minute after the
> positive battery cable is disconnected."

> "If a fault exists that makes unwanted air bag deployment possible, the air bag diagnostic
> monitor has an internal thermal fuse that will blow (open) automatically. ... DO NOT attempt to
> Jumper out the thermal fuse..."

Source: `manuals/factory-service-manual/1994 Ford F 150 2WD Pickup L6-300 4.9L/Repair%20and%20Diagnosis/Relays%20and%20Modules/Relays%20and%20Modules%20-%20Restraints%20and%20Safety%20Systems/Air%20Bag%20Control%20Module/`
