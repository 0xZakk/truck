---
title: "Power to the fuel pump relay comes from the EEC power relay through the PCM and the inertia switch"
kind: how-it-works
source: "[[sources/rly-fuel-pump-relay|Fuel Pump Relay — Description, Operation and Testing (FSM)]]"
related:
  - "[[notes/rly-fuel-pump-relay-is-grounded-by-the-pcm-not-a-simple-switch|The fuel pump relay is grounded by the PCM, so its ground circuit is the real no-start clue]]"
  - "[[notes/rly-pcm-power-relay-supplies-bplus-and-gives-reverse-battery-protection|The PCM power relay supplies B+ to the PCM and protects it against reverse battery polarity]]"
tags:
  - fuel-pump-relay
  - eec-power-relay
  - inertia-switch
  - fuel
---

When the ignition switch is turned ON, the Electronic Engine Control (EEC) power relay energizes
and supplies power to the fuel pump relay for 1 to 2 seconds, routed through the PCM and an
Inertia Fuel Shutoff (IFS) switch. Knowing this chain — EEC power relay → PCM → IFS switch → fuel
pump relay — turns a "no fuel pump" symptom into a sequence of checkpoints rather than a guess.

Each link fails differently: a tripped IFS switch (after a jolt or collision) opens the supply
even though the relay and PCM are fine, while a dead EEC power relay removes power upstream of
everything. This power-distribution chain is core `electrical-body` wiring, and it feeds the
`electrical-starting`/run logic the engine depends on to make fuel pressure.

## Related Concepts

- [[notes/rly-fuel-pump-relay-is-grounded-by-the-pcm-not-a-simple-switch|The fuel pump relay is grounded by the PCM, so its ground circuit is the real no-start clue]]
- [[notes/rly-pcm-power-relay-supplies-bplus-and-gives-reverse-battery-protection|The PCM power relay supplies B+ to the PCM and protects it against reverse battery polarity]]
- [[notes/eec-fuel-pump-runs-12s-at-key-on-then-needs-an-rpm-signal|The fuel pump runs 1-2 s at key-on, then the PCM keeps it running only with an rpm signal above 120]]
- [[notes/sen-tripped-inertia-switch-causes-crank-no-start|A tripped inertia switch is a common crank-no-start cause and must be manually reset]]
- [[notes/dtc-fuel-pump-codes-distinguish-relay-from-secondary-circuit|Fuel pump DTCs distinguish a relay primary-circuit fault from a pump secondary-circuit fault]]

## Source

- [[sources/rly-fuel-pump-relay|Fuel Pump Relay — Description, Operation and Testing (FSM)]]
