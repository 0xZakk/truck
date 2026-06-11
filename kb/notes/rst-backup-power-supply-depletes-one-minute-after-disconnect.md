---
title: "The SRS backup power supply depletes about one minute after the positive cable is disconnected"
kind: how-it-works
source: "[[sources/rst-air-bag-diagnostic-monitor|Air Bag Diagnostic Monitor and Trouble Codes — Description, Operation, and Diagnostics (FSM)]]"
related:
  - "[[notes/chg-disarm-the-air-bag-before-battery-work-on-starting-and-charging|Disarm the air bag system and wait one minute before any battery, steering column, or wheel work]]"
  - "[[notes/rst-thermal-fuse-disables-deployment-and-must-not-be-jumpered|The diagnostic monitor's thermal fuse disables deployment and must never be jumpered]]"
tags:
  - air-bag
  - diagnostic-monitor
  - backup-power
  - safety
---

The diagnostic monitor includes an internal backup power supply whose purpose is to keep the bag deployable
if the battery or its cables are damaged in a crash before the crash sensors close. It stores enough energy
to fire the igniter even with the vehicle's main power gone for that brief window.

That stored energy is also why air bag service has a mandatory wait. After the positive battery cable is
disconnected, the backup supply takes about one minute to bleed off its stored charge. Until it does, the
deployment circuit can still fire, so any module, column, or wheel work must pause for at least that minute
before touching the bag. This one-minute depletion figure is the technical reason behind the disarm
procedure used throughout the `interior` and steering work.

> "The backup power supply will deplete its stored energy approximately one minute after the positive
> battery cable is disconnected."

## Related Concepts

- [[notes/chg-disarm-the-air-bag-before-battery-work-on-starting-and-charging|Disarm the air bag system and wait one minute before any battery, steering column, or wheel work]]
- [[notes/rst-thermal-fuse-disables-deployment-and-must-not-be-jumpered|The diagnostic monitor's thermal fuse disables deployment and must never be jumpered]]
- [[notes/rly-air-bag-monitor-diagnoses-but-does-not-deploy-the-air-bag|The air bag diagnostic monitor only diagnoses the SRS; hard-wired sensors deploy the air bag]]
- [[notes/rly-air-bag-monitor-flashes-two-digit-codes-and-beeps-if-the-lamp-is-dead|The air bag monitor flashes two-digit trouble codes on the indicator, or beeps five sets of five if the lamp is dead]]
- [[notes/rst-use-the-2-ohm-air-bag-simulator-not-a-zero-ohm-jumper|Diagnose the SRS with a 2-ohm air bag simulator, never a zero-ohm jumper]]

## Source

- [[sources/rst-air-bag-diagnostic-monitor|Air Bag Diagnostic Monitor and Trouble Codes — Description, Operation, and Diagnostics (FSM)]]
