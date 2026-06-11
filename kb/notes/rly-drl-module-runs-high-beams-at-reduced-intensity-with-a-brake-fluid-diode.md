---
title: "The DRL module pulses the high beams at reduced intensity and uses a diode so low brake fluid cannot disable it"
kind: how-it-works
source: "[[sources/rly-daytime-running-lamp-module|Daytime Running Lamp (DRL) Control Unit — Description and Operation (FSM)]]"
related:
  - "[[notes/rly-alarm-module-disables-starting-and-flashes-lamps-at-80-cycles-per-minute|The alarm module disables the starting system and flashes the lamps at 80 cycles per minute when triggered]]"
tags:
  - daytime-running-lamps
  - drl-module
  - lighting
  - diode
---

The Daytime Running Lamp control unit runs the high-beam headlamps at reduced intensity for
daytime visibility. It activates only with three conditions met: ignition in RUN, parking brake
released, and headlamps off. Under those conditions the module outputs a pulsing voltage to the
high beams, which is how it dims them rather than running them at full brightness.

A subtle design detail aids diagnosis: a diode inside the module prevents a low brake fluid level
condition from disabling the DRL system, even though the park-brake/brake-warning circuit is part
of the activation logic. So a low-fluid warning will not extinguish the DRLs. This module is part
of the `electrical-body` lighting distribution.

## Related Concepts

- [[notes/rly-alarm-module-disables-starting-and-flashes-lamps-at-80-cycles-per-minute|The alarm module disables the starting system and flashes the lamps at 80 cycles per minute when triggered]]
- [[notes/lgt-drl-module-runs-high-beams-dimly-only-with-park-brake-off|The DRL module runs the high beams dimly only with ignition in RUN, park brake off, and headlamps off]]

## Source

- [[sources/rly-daytime-running-lamp-module|Daytime Running Lamp (DRL) Control Unit — Description and Operation (FSM)]]
