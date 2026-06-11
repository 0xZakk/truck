---
title: "The DRL module runs the high beams dimly only with ignition in RUN, park brake off, and headlamps off"
kind: how-it-works
source: "[[sources/lgt-daytime-running-lamp|Daytime Running Lamp (DRL) Control Unit — Description and Operation (FSM)]]"
related:
  - "[[notes/lgt-turn-signal-hazard-and-dimmer-are-one-multifunction-switch|Turn signal, hazard and high/low dimmer are all one steering-column multi-function switch]]"
tags:
  - daytime-running-lamp
  - drl
  - high-beam
  - lighting
---

The Daytime Running Lamp (DRL) control unit on the 1994 F-150 illuminates the high-beam
headlamps at reduced intensity by feeding them a pulsing voltage. It activates only when
three conditions hold at once: the ignition switch is in RUN, the parking brake is released,
and the headlamps are switched off. Releasing the park brake is therefore part of what arms
the DRLs, and setting it turns them off.

A useful detail for diagnosis: a diode inside the module isolates the DRL function from the
low-brake-fluid warning circuit, so a low brake fluid level will not disable the DRLs. If
the high beams glow dimly while driving with the lights off, that is the DRL system working
as designed, not a wiring fault. This is part of the truck's `electrical-body` system.

> "With the ignition switch in 'RUN', the park brake released, and the head lamps turned
> off, the Daytime Running Lamps (DRL) module outputs a pulsing voltage to operate the
> hi-beam headlamps at reduced intensity."

## Related Concepts

- [[notes/lgt-turn-signal-hazard-and-dimmer-are-one-multifunction-switch|Turn signal, hazard and high/low dimmer are all one steering-column multi-function switch]]
- [[notes/rly-drl-module-runs-high-beams-at-reduced-intensity-with-a-brake-fluid-diode|The DRL module pulses the high beams at reduced intensity and uses a diode so low brake fluid cannot disable it]]

## Source

- [[sources/lgt-daytime-running-lamp|Daytime Running Lamp (DRL) Control Unit — Description and Operation (FSM)]]
