---
title: "Manual-transmission trucks with a gray push-start ICM can be push started"
kind: how-it-works
source: "[[sources/mnt-distributor|Distributor and Distributor Ignition (DI) System (FSM)]]"
related:
  - "[[notes/eng-distributor-uses-hall-effect-pip-no-mechanical-advance|The 4.9L distributor uses a Hall-effect PIP signal and has no mechanical advance]]"
tags:
  - engine
  - ignition
  - driveline
---

The 4.9L Distributor Ignition system comes in two flavors distinguished by ignition control
module (ICM) color. The Push Start system uses a gray ICM and includes a push-start mode that
lets a manual-transmission truck be push started. The Computer Controlled Dwell system uses a
black ICM and has the PCM control coil charge time. Ford cautions never to push start an
automatic-transmission vehicle.

For this M5OD-R2 5-speed truck the distinction is practical: with the manual gearbox on the
`driveline`, a gray-ICM truck retains the ability to bump-start if the battery is dead. The ICM
color is also a quick way to identify which ignition strategy a given truck runs when chasing
`engine` ignition behavior.

## Related Concepts

- [[notes/eng-distributor-uses-hall-effect-pip-no-mechanical-advance|The 4.9L distributor uses a Hall-effect PIP signal and has no mechanical advance]]
- [[notes/rly-icm-color-gray-vs-black-tells-you-the-dwell-strategy|A gray ICM controls its own dwell while a black ICM lets the SPOUT signal set dwell]]

## Source

- [[sources/mnt-distributor|Distributor and Distributor Ignition (DI) System (FSM)]]
