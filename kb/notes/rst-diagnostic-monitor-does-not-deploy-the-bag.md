---
title: "The air bag diagnostic monitor never deploys the bag — the hard-wired sensors do"
kind: how-it-works
source: "[[sources/rst-air-bag-diagnostic-monitor|Air Bag Diagnostic Monitor and Trouble Codes — Description, Operation, and Diagnostics (FSM)]]"
related:
  - "[[notes/rst-two-sensors-must-close-together-to-deploy-the-air-bag|At least two sensors must close together to deploy the air bag]]"
  - "[[notes/rst-air-bag-indicator-self-test-and-flash-codes|The air bag indicator self-tests for six seconds and flashes two-digit fault codes]]"
tags:
  - air-bag
  - diagnostic-monitor
  - srs
---

It is easy to assume the air bag diagnostic monitor is the "brain" that fires the bag, but it is not. Its
job is purely diagnostic: it continuously watches every SRS component and wiring connection for faults while
the ignition is in RUN. Deployment is decided entirely by the center and RH front (frame rail) air bag
sensors and the RH cowl-side safing sensor, which are hard-wired to the air bag.

This separation explains a lot of behavior. The bag can still deploy in a crash even if the monitor has
flagged a fault or lost power, because the firing path does not run through the monitor's logic. Conversely,
a dead or disconnected monitor does not by itself make the bag inert. What the monitor adds is fault
detection, the warning indicator, the backup power supply, and the protective thermal fuse — readiness
features around a deployment circuit that is fundamentally electromechanical. The monitor lives in the
`interior` instrument area.

> "The air bag diagnostic monitor does not deploy the air bag in the event of a crash. The center and RH
> front air bag sensors are 'hard wired' to the air bag..."

## Related Concepts

- [[notes/rst-two-sensors-must-close-together-to-deploy-the-air-bag|At least two sensors must close together to deploy the air bag]]
- [[notes/rst-air-bag-indicator-self-test-and-flash-codes|The air bag indicator self-tests for six seconds and flashes two-digit fault codes]]
- [[notes/rly-air-bag-monitor-diagnoses-but-does-not-deploy-the-air-bag|The air bag diagnostic monitor only diagnoses the SRS; hard-wired sensors deploy the air bag]]
- [[notes/rst-backup-power-supply-depletes-one-minute-after-disconnect|The SRS backup power supply depletes about one minute after the positive cable is disconnected]]
- [[notes/rst-thermal-fuse-disables-deployment-and-must-not-be-jumpered|The diagnostic monitor's thermal fuse disables deployment and must never be jumpered]]
- [[notes/rly-air-bag-monitor-flashes-two-digit-codes-and-beeps-if-the-lamp-is-dead|The air bag monitor flashes two-digit trouble codes on the indicator, or beeps five sets of five if the lamp is dead]]

## Source

- [[sources/rst-air-bag-diagnostic-monitor|Air Bag Diagnostic Monitor and Trouble Codes — Description, Operation, and Diagnostics (FSM)]]
