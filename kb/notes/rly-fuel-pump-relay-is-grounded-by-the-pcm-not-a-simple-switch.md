---
title: "The fuel pump relay is grounded by the PCM, so its ground circuit is the real no-start clue"
kind: how-it-works
source: "[[sources/rly-fuel-pump-relay|Fuel Pump Relay — Description, Operation and Testing (FSM)]]"
related:
  - "[[notes/rly-eec-power-relay-feeds-the-fuel-pump-relay-coil|Power to the fuel pump relay comes from the EEC power relay through the PCM and the inertia switch]]"
  - "[[notes/eec-fuel-pump-runs-12s-at-key-on-then-needs-an-rpm-signal|The fuel pump runs 1-2 s at key-on, then the PCM keeps it running only with an rpm signal above 120]]"
tags:
  - fuel-pump-relay
  - pcm
  - no-start
  - fuel
---

The fuel pump relay on this truck is a PCM-switched relay: battery voltage is on its contact side,
but the PCM controls whether the relay closes by completing (or opening) the relay's ground
circuit. Because the high side can be live while the pump is dead, the relay coil ground from the
PCM is the more diagnostic node. If the PCM never grounds the relay — for example because it sees
no rpm signal within about a second of key-on — the contacts open and the pump stops even though
power is present.

This is why a fuel-pump no-start is best chased at the relay's PCM-side ground rather than by
assuming the relay or pump is bad. The behavior is a deliberate safety interlock in the
`electrical-body` and `electrical-starting` wiring: the PCM also opens the ground if engine speed
falls below 120 rpm, so the pump cannot keep running into a stalled or crashed engine.

## Related Concepts

- [[notes/rly-eec-power-relay-feeds-the-fuel-pump-relay-coil|Power to the fuel pump relay comes from the EEC power relay through the PCM and the inertia switch]]
- [[notes/eec-fuel-pump-runs-12s-at-key-on-then-needs-an-rpm-signal|The fuel pump runs 1-2 s at key-on, then the PCM keeps it running only with an rpm signal above 120]]
- [[notes/dtc-fuel-pump-codes-distinguish-relay-from-secondary-circuit|Fuel pump DTCs distinguish a relay primary-circuit fault from a pump secondary-circuit fault]]
- [[notes/rly-pcm-power-relay-supplies-bplus-and-gives-reverse-battery-protection|The PCM power relay supplies B+ to the PCM and protects it against reverse battery polarity]]
- [[notes/sen-tripped-inertia-switch-causes-crank-no-start|A tripped inertia switch is a common crank-no-start cause and must be manually reset]]

## Source

- [[sources/rly-fuel-pump-relay|Fuel Pump Relay — Description, Operation and Testing (FSM)]]
