---
title: "Disarm the air bag system before disconnecting the battery for starting/charging work"
kind: procedure
source: "[[sources/chg-service-precautions|Starting and Charging — Service Precautions (FSM)]]"
related:
  - "[[notes/chg-disconnecting-the-battery-erases-the-pcm-adaptive-strategy|Disconnecting the battery erases the PCM adaptive strategy and may need 10+ miles to relearn]]"
tags:
  - starting-system
  - charging-system
  - airbag
  - safety
  - procedure
---

Because starting and charging work means disconnecting the battery, the factory service
manual requires disarming the air bag (supplemental restraint) system first. **Disarm:**
disconnect the battery negative then positive cable, **wait at least one minute** for the
back-up power supply to deplete, remove the air bag module retaining nuts, disconnect the
driver-side air bag connector, connect the Rotunda Air Bag Simulator 105-00010 to the
harness, then reconnect the battery.

**Arm** by reversing it: disconnect the battery again (negative then positive), wait one
minute, remove the simulator, reconnect the air bag module connector, install the module,
and reconnect the battery. The one-minute wait for the back-up capacitor to bleed down is
the load-bearing safety step — it prevents an accidental deployment while the connector is
open.

> "Disconnect battery negative, then positive cable. Wait at least one minute for back-up
> power supply to deplete its stored energy."

This relates to truck inventory systems `electrical-starting` and `electrical-charging`.

## Related Concepts

- [[notes/chg-disconnecting-the-battery-erases-the-pcm-adaptive-strategy|Disconnecting the battery erases the PCM adaptive strategy and may need 10+ miles to relearn]]
- [[notes/sus-disarm-the-air-bag-and-wait-one-minute-before-column-work|Disarm the air bag and wait one minute before steering column or wheel work]]
- [[notes/wpr-disarm-the-air-bag-before-working-on-the-column-switch|Disarm the air bag before removing the column-mounted wiper/washer switch]]
- [[notes/crz-disarm-the-air-bag-before-working-on-the-cruise-switches|Disarm the air bag before servicing the steering-wheel cruise switches]]
- [[notes/gls-glass-work-near-the-column-requires-disarming-the-air-bag|Glass or window work that touches the steering column requires disarming the air bag and waiting one minute]]
- [[notes/bdy-battery-disconnect-forces-the-pcm-to-relearn-over-ten-miles|Any cab battery disconnect forces the PCM to relearn its adaptive strategy over about ten miles]]

## Source

- [[sources/chg-service-precautions|Starting and Charging — Service Precautions (FSM)]]
