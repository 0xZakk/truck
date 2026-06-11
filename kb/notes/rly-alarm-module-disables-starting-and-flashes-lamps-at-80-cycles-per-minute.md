---
title: "The alarm module disables the starting system and flashes the lamps at 80 cycles per minute when triggered"
kind: how-it-works
source: "[[sources/rly-body-control-modules|Body Control Modules — Warning Chime, Alarm, Keyless Entry, Wiper, PSOM, Starter Relay (FSM)]]"
related:
  - "[[notes/rly-warning-chime-module-sounds-for-key-in-lights-on-and-unbuckled-belt|The warning chime module sounds for key-in-ignition, lights-on-with-door-open, and unbuckled belt]]"
  - "[[notes/lgt-drl-module-runs-high-beams-dimly-only-with-park-brake-off|The DRL module runs the high beams at reduced intensity only with ignition in RUN, park brake released, and headlamps off]]"
tags:
  - alarm-module
  - anti-theft
  - keyless-entry
  - relays-and-modules
---

The Alarm Module (anti-theft controller) monitors switches throughout the vehicle. When triggered,
it sounds the horn and flashes the headlamps and parking lamps at an intermittent rate of 80 cycles
per minute, and — important for diagnosis — it disables the starting system until the system is
disarmed. So an armed/triggered anti-theft system is a legitimate cause of a crank-no-start that
should be ruled out before condemning the starter relay or `electrical-starting` circuit.

The Keyless Entry Module works alongside it: pressing LOCK on the remote or the power door lock
switch arms the anti-theft system, UNLOCK/PANIC lights the interior lamps for about 25 seconds, and
PANIC flashes the exterior lights and sounds the horn for about four minutes until pressed again.
Both modules sit in the `electrical-body` security network.

## Related Concepts

- [[notes/rly-warning-chime-module-sounds-for-key-in-lights-on-and-unbuckled-belt|The warning chime module sounds for key-in-ignition, lights-on-with-door-open, and unbuckled belt]]
- [[notes/lgt-drl-module-runs-high-beams-dimly-only-with-park-brake-off|The DRL module runs the high beams at reduced intensity only with ignition in RUN, park brake released, and headlamps off]]
- [[notes/acc-anti-theft-module-monitors-switches-and-flashes-lamps-at-80-cpm|The anti-theft controller module monitors vehicle switches and, when triggered, sounds the horn and flashes the lamps at 80 cycles per minute]]
- [[notes/acc-anti-theft-disables-the-starting-system-until-disarmed|The anti-theft system disables the starting system until it is disarmed]]
- [[notes/acc-door-disarm-switch-grounds-the-controller-when-the-door-is-key-unlocked|A door disarm switch grounds the controller when its door is unlocked with the key, disabling the anti-theft system]]
- [[notes/bdy-keyless-module-coordinates-locks-anti-theft-lamps-and-panic|The keyless entry module coordinates door locks, anti-theft arming, interior lamps, and the panic alarm]]

## Source

- [[sources/rly-body-control-modules|Body Control Modules — Warning Chime, Alarm, Keyless Entry, Wiper, PSOM, Starter Relay (FSM)]]
