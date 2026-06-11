---
title: "Disarm the air bag system and wait one minute before any battery, steering column, or wheel work"
kind: procedure
source: "[[sources/chg-service-precautions|Starting and Charging — Service Precautions (FSM)]]"
related:
  - "[[notes/chg-disconnecting-the-battery-erases-the-pcm-adaptive-strategy|Disconnecting the battery erases the PCM adaptive strategy and may need 10+ miles to relearn]]"
tags:
  - starting-system
  - charging-system
  - steering
  - airbag
  - safety
  - procedure
---

Any work that disconnects the battery (starting/charging service) or touches the steering
column, wheel, or gear lash requires disarming the air bag (supplemental restraint) system
first, because the driver air bag lives in the steering-wheel hub. **Disarm:** record the
radio presets, disconnect the battery NEGATIVE cable then the positive cable, **wait at
least one minute** for the back-up power supply to deplete its stored energy, then remove
the air bag module retaining nuts, disconnect the driver-side module connector, and connect
the Rotunda Air Bag Simulator 105-00010 (or equivalent) to the harness at the top of the
wheel. Reconnect the battery once the simulator is in place.

**Arm** by reversing it: disconnect the battery again (negative then positive), wait one
minute, remove the simulator, reconnect the air bag module connector, install the module,
and reconnect the battery. The one-minute wait for the back-up capacitor to bleed down is
the load-bearing, non-negotiable safety step — it prevents an accidental deployment while
the connector is open and your hands are on the module. Because the battery was
disconnected, the PCM also loses its adaptive strategy and the truck may drive abnormally
until it relearns, often over 10 or more miles.

> "Disconnect battery negative, then positive cable. Wait at least one minute for back-up
> power supply to deplete its stored energy."

This relates to truck inventory systems `electrical-starting`, `electrical-charging`, and
`steering`.

## Related Concepts

- [[notes/chg-disconnecting-the-battery-erases-the-pcm-adaptive-strategy|Disconnecting the battery erases the PCM adaptive strategy and may need 10+ miles to relearn]]
- [[notes/bdy-battery-disconnect-forces-the-pcm-to-relearn-over-ten-miles|Any cab battery disconnect forces the PCM to relearn its adaptive strategy over about ten miles]]
- [[notes/crz-disarm-the-air-bag-before-working-on-the-cruise-switches|Disarm the air bag before servicing the steering-wheel cruise switches]]
- [[notes/wpr-disarm-the-air-bag-before-working-on-the-column-switch|Disarm the air bag before removing the column-mounted wiper/washer switch]]
- [[notes/gls-glass-work-near-the-column-requires-disarming-the-air-bag|Glass or window work that touches the steering column requires disarming the air bag and waiting one minute]]

## Source

- [[sources/chg-service-precautions|Starting and Charging — Service Precautions (FSM)]]
- [[sources/sus-steering-column|Energy-Absorbing Steering Column and Air Bag Service (FSM)]]
