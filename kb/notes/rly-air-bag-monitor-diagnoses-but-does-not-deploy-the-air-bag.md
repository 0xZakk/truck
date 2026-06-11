---
title: "The air bag diagnostic monitor only diagnoses the SRS; hard-wired sensors deploy the air bag"
kind: how-it-works
source: "[[sources/rly-air-bag-diagnostic-monitor|Air Bag Control Module (Air Bag Diagnostic Monitor) — Description and Testing (FSM)]]"
related:
  - "[[notes/rly-air-bag-monitor-flashes-two-digit-codes-and-beeps-if-the-lamp-is-dead|The air bag monitor flashes two-digit trouble codes on the indicator, or beeps five sets of five if the lamp is dead]]"
  - "[[notes/sus-disarm-the-air-bag-and-wait-one-minute-before-column-work|Disarm the air bag and wait one minute before steering column or wheel work]]"
tags:
  - air-bag-diagnostic-monitor
  - srs
  - safety
  - relays-and-modules
---

The Air Bag Control Module on this truck is the Air Bag Diagnostic Monitor, and its primary job is
exactly that — diagnostics. It continuously monitors all supplemental restraint system components
and wiring for faults and reports them, but it does NOT deploy the air bag in a crash. Deployment
is decided by the center and RH front air bag sensors, which are hard-wired to the air bag.

This separation matters for troubleshooting: a failed or removed diagnostic monitor disables fault
reporting and certain protections but is not the deployment decision-maker. As a fail-safe, if a
fault could cause unwanted deployment, the monitor's internal thermal fuse blows automatically to
cut all power to the deployment circuit — and that fuse must never be jumpered. The monitor is a
key node in the `electrical-body` safety-system wiring.

## Related Concepts

- [[notes/rly-air-bag-monitor-flashes-two-digit-codes-and-beeps-if-the-lamp-is-dead|The air bag monitor flashes two-digit trouble codes on the indicator, or beeps five sets of five if the lamp is dead]]
- [[notes/sus-disarm-the-air-bag-and-wait-one-minute-before-column-work|Disarm the air bag and wait one minute before steering column or wheel work]]
- [[notes/rst-diagnostic-monitor-does-not-deploy-the-bag|The air bag diagnostic monitor never deploys the bag — the hard-wired sensors do]]
- [[notes/rst-backup-power-supply-depletes-one-minute-after-disconnect|The SRS backup power supply depletes about one minute after the positive cable is disconnected]]
- [[notes/rst-thermal-fuse-disables-deployment-and-must-not-be-jumpered|The diagnostic monitor's thermal fuse disables deployment and must never be jumpered]]
- [[notes/rst-use-the-2-ohm-air-bag-simulator-not-a-zero-ohm-jumper|Diagnose the SRS with a 2-ohm air bag simulator, never a zero-ohm jumper]]
- [[notes/rst-air-bag-indicator-self-test-and-flash-codes|The air bag indicator self-tests for six seconds and flashes two-digit fault codes within 30 seconds]]

## Source

- [[sources/rly-air-bag-diagnostic-monitor|Air Bag Control Module (Air Bag Diagnostic Monitor) — Description and Testing (FSM)]]
