---
title: "The air bag indicator self-tests for six seconds and flashes two-digit fault codes within 30 seconds"
kind: troubleshooting
source: "[[sources/rst-air-bag-diagnostic-monitor|Air Bag Diagnostic Monitor and Trouble Codes — Description, Operation, and Diagnostics (FSM)]]"
related:
  - "[[notes/rst-diagnostic-monitor-does-not-deploy-the-bag|The air bag diagnostic monitor never deploys the bag — the hard-wired sensors do]]"
  - "[[notes/rst-five-sets-of-five-beeps-means-a-dead-indicator-not-code-55|Five sets of five beeps means a dead indicator, not code 55]]"
tags:
  - air-bag
  - warning-indicators
  - trouble-codes
  - diagnosis
---

At every key-on the diagnostic monitor lights the air bag indicator in the instrument cluster for about six
seconds, then turns it off — that is the normal bulb/self-test. Any deviation is a fault signal: the
indicator failing to light, staying on continuously, or flashing all mean the monitor has detected a
problem. Because the monitor needs up to about 30 seconds after key-on to run all tests and verify faults,
a flashing trouble code may not begin until that window has passed, so do not walk away too early.

Codes are two-digit and flashed out, each displayed at least twice. The pattern is first-digit flashes, a
one-second pause, second-digit flashes, then a three-second pause — for example code 32 is three flashes,
pause, two flashes, pause. Multiple faults are prioritized numerically: the highest-priority fault shows
first, and the next appears only after the first is corrected. There is no manual erase — a code clears
automatically once its fault is fixed. This is the front-line readiness check for the SRS in the `interior`.

> "Each diagnostic trouble code is always displayed at least twice. For example, a diagnostic trouble code
> 32 is displayed as three flashes, followed by a one second pause, then two flashes..."

## Related Concepts

- [[notes/rst-diagnostic-monitor-does-not-deploy-the-bag|The air bag diagnostic monitor never deploys the bag — the hard-wired sensors do]]
- [[notes/rst-five-sets-of-five-beeps-means-a-dead-indicator-not-code-55|Five sets of five beeps means a dead indicator, not code 55]]
- [[notes/rly-air-bag-monitor-flashes-two-digit-codes-and-beeps-if-the-lamp-is-dead|The air bag monitor flashes two-digit trouble codes on the indicator, or beeps five sets of five if the lamp is dead]]
- [[notes/rst-backup-power-supply-depletes-one-minute-after-disconnect|The SRS backup power supply depletes about one minute after the positive cable is disconnected]]
- [[notes/rly-air-bag-monitor-diagnoses-but-does-not-deploy-the-air-bag|The air bag diagnostic monitor only diagnoses the SRS; hard-wired sensors deploy the air bag]]

## Source

- [[sources/rst-air-bag-diagnostic-monitor|Air Bag Diagnostic Monitor and Trouble Codes — Description, Operation, and Diagnostics (FSM)]]
