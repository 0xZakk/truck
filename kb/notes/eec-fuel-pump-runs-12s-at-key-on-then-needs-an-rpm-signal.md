---
title: "The fuel pump runs 1-2 s at key-on, then the PCM keeps it running only with an rpm signal above 120"
kind: how-it-works
source: "[[sources/eec-fuel-pressure-regulator-and-pump-control|Fuel Delivery — Injectors, Pressure Regulator, and Pump Control (FSM)]]"
related:
  - "[[notes/eec-regulator-references-manifold-vacuum-to-hold-a-constant-injector-pressure-drop|The fuel pressure regulator references manifold vacuum to hold a constant pressure drop across the injectors]]"
tags:
  - fuel-pump
  - fuel-pump-relay
  - inertia-switch
  - safety
  - fuel
---

Fuel pump operation is a PCM-controlled safety interlock, not a simple switch. When the ignition
goes ON, the EEC power relay energizes and the PCM grounds the fuel pump relay to run the pump
for about 1-2 seconds (priming the rail). If the PCM does not receive an ignition (rpm) signal
within roughly one second, a PCM timer opens the relay ground and the pump stops — so a stalled
or non-cranking engine will not keep pumping fuel.

At START the PCM closes the ground again, and during running it keeps the pump on, but it opens
the fuel pump relay ground (killing the pump) if engine speed drops below 120 rpm. Power also
routes through the Inertia Fuel Shutoff (IFS) switch, which cuts the pump in a collision. This
chain — EEC power relay, PCM, fuel pump relay, IFS switch — is the heart of `fuel`-system pump
control and a primary no-start diagnostic path.

## Related Concepts

- [[notes/eec-regulator-references-manifold-vacuum-to-hold-a-constant-injector-pressure-drop|The fuel pressure regulator references manifold vacuum to hold a constant pressure drop across the injectors]]
- [[notes/rly-eec-power-relay-feeds-the-fuel-pump-relay-coil|Power to the fuel pump relay comes from the EEC power relay through the PCM and the inertia switch]]
- [[notes/rly-fuel-pump-relay-is-grounded-by-the-pcm-not-a-simple-switch|The fuel pump relay is grounded by the PCM, so its ground circuit is the real no-start clue]]
- [[notes/sen-tripped-inertia-switch-causes-crank-no-start|A tripped inertia switch is a common crank-no-start cause and must be manually reset]]
- [[notes/sen-inertia-switch-uses-a-magnet-held-ball|The inertia switch cuts fuel-pump power in a crash using a magnet-held ball that breaks loose on impact]]
- [[notes/dtc-fuel-pump-codes-distinguish-relay-from-secondary-circuit|Fuel pump DTCs distinguish a relay primary-circuit fault from a pump secondary-circuit fault]]

## Source

- [[sources/eec-fuel-pressure-regulator-and-pump-control|Fuel Delivery — Injectors, Pressure Regulator, and Pump Control (FSM)]]
