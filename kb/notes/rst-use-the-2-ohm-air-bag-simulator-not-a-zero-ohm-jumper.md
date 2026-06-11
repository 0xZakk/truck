---
title: "Diagnose the SRS with a 2-ohm air bag simulator, never a zero-ohm jumper"
kind: procedure
source: "[[sources/rst-air-bag-diagnostic-monitor|Air Bag Diagnostic Monitor and Trouble Codes — Description, Operation, and Diagnostics (FSM)]]"
related:
  - "[[notes/rst-air-bag-module-is-serviced-only-as-a-complete-assembly|The driver air bag module is serviced only as a complete assembly]]"
  - "[[notes/chg-disarm-the-air-bag-before-battery-work-on-starting-and-charging|Disarm the air bag system and wait one minute before any battery, steering column, or wheel work]]"
tags:
  - air-bag
  - diagnosis
  - special-tools
  - srs
---

Most SRS diagnostics begin by deactivating the system and removing the driver air bag module so it cannot
deploy while you work. With the module out, the harness must be terminated with the Rotunda Air Bag
Simulator 105-0008 (or equivalent), which is a 2-ohm resistor that mimics the resistance of the air bag
connection.

The value matters: do NOT bridge the air bag connection with a zero-ohm jumper wire. A zero-ohm link does
not match the bag's expected resistance, so the monitor reads it as a fault and may display a code per its
priority scheme, sending you chasing a problem you created. Using the correct 2-ohm simulator lets the
monitor see a "good" bag and report only the genuine fault you are diagnosing. This keeps SRS troubleshooting
in the `interior` accurate and safe.

> "The air bag simulator is a 2-ohm resistor that must be used to simulate an air bag connection in the
> system. It is not acceptable to jump the air bag connection with a zero ohm jumper wire."

## Related Concepts

- [[notes/rst-air-bag-module-is-serviced-only-as-a-complete-assembly|The driver air bag module is serviced only as a complete assembly]]
- [[notes/chg-disarm-the-air-bag-before-battery-work-on-starting-and-charging|Disarm the air bag system and wait one minute before any battery, steering column, or wheel work]]
- [[notes/rst-thermal-fuse-disables-deployment-and-must-not-be-jumpered|The diagnostic monitor's thermal fuse disables deployment and must never be jumpered]]
- [[notes/rly-air-bag-monitor-diagnoses-but-does-not-deploy-the-air-bag|The air bag diagnostic monitor only diagnoses the SRS; hard-wired sensors deploy the air bag]]
- [[notes/rst-backup-power-supply-depletes-one-minute-after-disconnect|The SRS backup power supply depletes about one minute after the positive cable is disconnected]]
- [[notes/rly-air-bag-monitor-flashes-two-digit-codes-and-beeps-if-the-lamp-is-dead|The air bag monitor self-tests the indicator for six seconds and flashes two-digit trouble codes within 30 seconds, or beeps five sets of five if the lamp is dead]]
- [[notes/rst-two-sensors-must-close-together-to-deploy-the-air-bag|At least two sensors — one primary plus the safing sensor — must close together to deploy the air bag]]

## Source

- [[sources/rst-air-bag-diagnostic-monitor|Air Bag Diagnostic Monitor and Trouble Codes — Description, Operation, and Diagnostics (FSM)]]
