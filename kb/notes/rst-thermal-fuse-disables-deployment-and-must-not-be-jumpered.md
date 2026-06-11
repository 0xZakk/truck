---
title: "The diagnostic monitor's thermal fuse disables deployment and must never be jumpered"
kind: concept
source: "[[sources/rst-air-bag-diagnostic-monitor|Air Bag Diagnostic Monitor and Trouble Codes — Description, Operation, and Diagnostics (FSM)]]"
related:
  - "[[notes/rly-air-bag-monitor-diagnoses-but-does-not-deploy-the-air-bag|The air bag diagnostic monitor only diagnoses the SRS; hard-wired sensors deploy the air bag]]"
  - "[[notes/rst-backup-power-supply-depletes-one-minute-after-disconnect|The SRS backup power supply depletes about one minute after the positive cable is disconnected]]"
tags:
  - air-bag
  - diagnostic-monitor
  - thermal-fuse
  - safety
---

The air bag diagnostic monitor contains an internal thermal fuse with a counter-intuitive behavior: it does
NOT blow from excessive current. Instead, if the monitor detects a fault that could cause unwanted air bag
deployment, it deliberately opens the thermal fuse to remove all power from the deployment circuit — a
fail-safe that makes the bag inert rather than letting it fire accidentally.

The critical service caution follows directly: never attempt to jumper out the thermal fuse with a circuit
breaker or any other fuse. Because it is a protective interlock and not an overcurrent device, bypassing it
defeats the safety logic and can re-enable a circuit the monitor intentionally killed. When the fuse is open
the system is down and the underlying fault must be found and corrected, not worked around. This safeguards
the `interior` SRS deployment path.

> "The thermal fuse does not blow (open) because of excessive current flowing through It. DO NOT attempt to
> Jumper out the thermal fuse with a circuit breaker or any other type of fuse."

## Related Concepts

- [[notes/rly-air-bag-monitor-diagnoses-but-does-not-deploy-the-air-bag|The air bag diagnostic monitor only diagnoses the SRS; hard-wired sensors deploy the air bag]]
- [[notes/rst-backup-power-supply-depletes-one-minute-after-disconnect|The SRS backup power supply depletes about one minute after the positive cable is disconnected]]
- [[notes/rst-use-the-2-ohm-air-bag-simulator-not-a-zero-ohm-jumper|Diagnose the SRS with a 2-ohm air bag simulator, never a zero-ohm jumper]]
- [[notes/rly-air-bag-monitor-flashes-two-digit-codes-and-beeps-if-the-lamp-is-dead|The air bag monitor flashes two-digit trouble codes on the indicator, or beeps five sets of five if the lamp is dead]]
- [[notes/rst-five-sets-of-five-beeps-means-a-dead-indicator-not-code-55|Five sets of five beeps means a dead air bag indicator with a fault present, not code 55]]

## Source

- [[sources/rst-air-bag-diagnostic-monitor|Air Bag Diagnostic Monitor and Trouble Codes — Description, Operation, and Diagnostics (FSM)]]
