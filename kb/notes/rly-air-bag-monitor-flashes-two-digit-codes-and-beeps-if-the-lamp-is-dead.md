---
title: "The air bag monitor self-tests the indicator for six seconds and flashes two-digit trouble codes within 30 seconds, or beeps five sets of five if the lamp is dead"
kind: troubleshooting
source: "[[sources/rly-air-bag-diagnostic-monitor|Air Bag Control Module (Air Bag Diagnostic Monitor) — Description and Testing (FSM)]]"
related:
  - "[[notes/rly-air-bag-monitor-diagnoses-but-does-not-deploy-the-air-bag|The air bag diagnostic monitor only diagnoses the SRS; hard-wired sensors deploy the air bag]]"
tags:
  - air-bag-diagnostic-monitor
  - diagnostic-trouble-codes
  - warning-indicators
  - srs
  - troubleshooting
---

At every key-on with the ignition in RUN, the air bag diagnostic monitor lights the air bag
indicator in the instrument cluster for about six seconds and then turns it off — the normal
bulb/self-check. Any deviation is a fault signal: if the indicator fails to light, stays on
continuously, or flashes at any time, the monitor has detected a problem. Because the monitor needs
up to about 30 seconds after RUN to run all its tests and verify faults, a flashing trouble code may
not begin until that window has passed, so do not walk away too early.

Each diagnostic trouble code is a two-digit number flashed out and always displayed at least twice.
The pattern is first-digit flashes, a one-second pause, second-digit flashes, then a three-second
pause; for example, code 32 is three flashes, a one-second pause, two flashes, then a three-second
pause. Multiple faults are prioritized numerically: the highest-priority fault shows first, and the
next appears only after the first is corrected. There is no manual erase — a code clears
automatically once its fault is fixed. A blown internal fuse reports as code 51, after which you
repair all wiring shorts before replacing the monitor.

A special case: if a system fault exists but the indicator itself is inoperative, the monitor sounds
an audible tone of five sets of five beeps — this is NOT a code 55; it means the lamp is dead and
service is required. This reading procedure is the front-line readiness check for `electrical-body`
SRS diagnosis.

> "Each diagnostic trouble code is always displayed at least twice. For example, a diagnostic trouble
> code 32 is displayed as three flashes, followed by a one second pause, then two flashes..."

## Related Concepts

- [[notes/rly-air-bag-monitor-diagnoses-but-does-not-deploy-the-air-bag|The air bag diagnostic monitor only diagnoses the SRS; hard-wired sensors deploy the air bag]]
- [[notes/rst-five-sets-of-five-beeps-means-a-dead-indicator-not-code-55|Five sets of five beeps means a dead air bag indicator with a fault present, not code 55]]
- [[notes/rst-thermal-fuse-disables-deployment-and-must-not-be-jumpered|The diagnostic monitor's thermal fuse disables deployment and must never be jumpered]]
- [[notes/rst-backup-power-supply-depletes-one-minute-after-disconnect|The SRS backup power supply depletes about one minute after the positive cable is disconnected]]
- [[notes/rst-use-the-2-ohm-air-bag-simulator-not-a-zero-ohm-jumper|Diagnose the SRS with a 2-ohm air bag simulator, never a zero-ohm jumper]]

## Source

- [[sources/rly-air-bag-diagnostic-monitor|Air Bag Control Module (Air Bag Diagnostic Monitor) — Description and Testing (FSM)]]
- [[sources/rst-air-bag-diagnostic-monitor|Air Bag Diagnostic Monitor and Trouble Codes — Description, Operation, and Diagnostics (FSM)]]
