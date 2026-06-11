---
title: "The DRL module runs the high beams at reduced intensity only with ignition in RUN, park brake released, and headlamps off"
kind: how-it-works
source: "[[sources/lgt-daytime-running-lamp|Daytime Running Lamp (DRL) Control Unit — Description and Operation (FSM)]]"
related: []
tags:
  - daytime-running-lamp
  - drl
  - drl-module
  - high-beam
  - lighting
  - diode
---

The Daytime Running Lamp (DRL) control unit on the 1994 F-150 illuminates the high-beam
headlamps at reduced intensity for daytime visibility by feeding them a pulsing voltage,
which is how it dims them rather than running them at full brightness. It activates only
when three conditions hold at once: the ignition switch is in RUN, the parking brake is
released, and the headlamps are switched off. Releasing the park brake is therefore part
of what arms the DRLs, and setting it turns them off.

A useful detail for diagnosis: a diode inside the module isolates the DRL function from the
low-brake-fluid warning circuit, so even though the park-brake/brake-warning circuit is part
of the activation logic, a low brake fluid level will not disable the DRLs. If the high beams
glow dimly while driving with the lights off, that is the DRL system working as designed, not
a wiring fault. This module is part of the truck's `electrical-body` lighting distribution.

> "With the ignition switch in 'RUN', the park brake released, and the head lamps turned
> off, the Daytime Running Lamps (DRL) module outputs a pulsing voltage to operate the
> hi-beam headlamps at reduced intensity."

## Related Concepts

## Source

- [[sources/lgt-daytime-running-lamp|Daytime Running Lamp (DRL) Control Unit — Description and Operation (FSM)]]
- [[sources/rly-daytime-running-lamp-module|Daytime Running Lamp (DRL) Control Unit — Description and Operation (FSM)]]
