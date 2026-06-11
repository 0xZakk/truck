---
title: "The air bag monitor flashes two-digit trouble codes on the indicator, or beeps five sets of five if the lamp is dead"
kind: troubleshooting
source: "[[sources/rly-air-bag-diagnostic-monitor|Air Bag Control Module (Air Bag Diagnostic Monitor) — Description and Testing (FSM)]]"
related:
  - "[[notes/rly-air-bag-monitor-diagnoses-but-does-not-deploy-the-air-bag|The air bag diagnostic monitor only diagnoses the SRS; hard-wired sensors deploy the air bag]]"
tags:
  - air-bag-diagnostic-monitor
  - diagnostic-trouble-codes
  - srs
  - troubleshooting
---

At key-on with the ignition in RUN, the air bag indicator should light for about six seconds and
then go out — a normal self-check. If the indicator does not light, stays on, or flashes at any
time, the monitor has detected a fault. Note that codes may not appear for about 30 seconds after
RUN, the time the monitor needs to run its tests.

Each diagnostic trouble code is a two-digit number shown as flashes and pauses and is always
repeated at least twice; for example, code 32 is three flashes, a one-second pause, two flashes,
then a three-second pause. Codes are prioritized numerically, with the highest-priority fault shown
first. A special case: if a system fault exists but the indicator itself is inoperative, the
monitor sounds an audible tone of five sets of five beeps — this is NOT a code 55, it means the
lamp is dead and service is required. A blown internal fuse reports as code 51, after which you
repair all wiring shorts before replacing the monitor. This reading procedure is the front line of
`electrical-body` SRS diagnosis.

## Related Concepts

- [[notes/rly-air-bag-monitor-diagnoses-but-does-not-deploy-the-air-bag|The air bag diagnostic monitor only diagnoses the SRS; hard-wired sensors deploy the air bag]]
- [[notes/rst-air-bag-indicator-self-test-and-flash-codes|The air bag indicator self-tests for six seconds and flashes two-digit fault codes within 30 seconds]]
- [[notes/rst-five-sets-of-five-beeps-means-a-dead-indicator-not-code-55|Five sets of five beeps means a dead air bag indicator with a fault present, not code 55]]
- [[notes/rst-diagnostic-monitor-does-not-deploy-the-bag|The air bag diagnostic monitor never deploys the bag — the hard-wired sensors do]]
- [[notes/rst-backup-power-supply-depletes-one-minute-after-disconnect|The SRS backup power supply depletes about one minute after the positive cable is disconnected]]
- [[notes/rst-thermal-fuse-disables-deployment-and-must-not-be-jumpered|The diagnostic monitor's thermal fuse disables deployment and must never be jumpered]]

## Source

- [[sources/rly-air-bag-diagnostic-monitor|Air Bag Control Module (Air Bag Diagnostic Monitor) — Description and Testing (FSM)]]
