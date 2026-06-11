---
title: "The air bag diagnostic monitor only diagnoses the SRS; hard-wired sensors deploy the air bag"
kind: how-it-works
source: "[[sources/rly-air-bag-diagnostic-monitor|Air Bag Control Module (Air Bag Diagnostic Monitor) — Description and Testing (FSM)]]"
related:
  - "[[notes/rly-air-bag-monitor-flashes-two-digit-codes-and-beeps-if-the-lamp-is-dead|The air bag monitor flashes two-digit trouble codes on the indicator, or beeps five sets of five if the lamp is dead]]"
  - "[[notes/chg-disarm-the-air-bag-before-battery-work-on-starting-and-charging|Disarm the air bag system and wait one minute before any battery, steering column, or wheel work]]"
tags:
  - air-bag-diagnostic-monitor
  - srs
  - safety
  - relays-and-modules
---

The Air Bag Control Module on this truck is the Air Bag Diagnostic Monitor, and its primary job is
exactly that — diagnostics. While the ignition is in RUN it continuously monitors all supplemental
restraint system components and wiring for faults and reports them, but it does NOT deploy the air
bag in a crash. Deployment is decided entirely by the center and RH front (frame rail) air bag
sensors together with the RH cowl-side safing sensor, all of which are hard-wired to the air bag.

This separation matters for troubleshooting. The bag can still deploy in a crash even if the monitor
has flagged a fault or lost power, because the firing path does not run through the monitor's logic;
conversely, a dead, removed, or disconnected monitor does not by itself make the bag inert — it only
disables fault reporting and certain protections. What the monitor adds around the fundamentally
electromechanical deployment circuit is fault detection, the warning indicator, the backup power
supply, and the protective thermal fuse. As a fail-safe, if a fault could cause unwanted deployment,
the monitor's internal thermal fuse blows automatically to cut all power to the deployment circuit —
and that fuse must never be jumpered. The monitor is a key node in the safety-system wiring, residing
in the `interior` instrument area.

> "The air bag diagnostic monitor does not deploy the air bag in the event of a crash. The center and RH
> front air bag sensors are 'hard wired' to the air bag..."

## Related Concepts

- [[notes/rly-air-bag-monitor-flashes-two-digit-codes-and-beeps-if-the-lamp-is-dead|The air bag monitor flashes two-digit trouble codes on the indicator, or beeps five sets of five if the lamp is dead]]
- [[notes/chg-disarm-the-air-bag-before-battery-work-on-starting-and-charging|Disarm the air bag system and wait one minute before any battery, steering column, or wheel work]]
- [[notes/rst-backup-power-supply-depletes-one-minute-after-disconnect|The SRS backup power supply depletes about one minute after the positive cable is disconnected]]
- [[notes/rst-thermal-fuse-disables-deployment-and-must-not-be-jumpered|The diagnostic monitor's thermal fuse disables deployment and must never be jumpered]]
- [[notes/rst-use-the-2-ohm-air-bag-simulator-not-a-zero-ohm-jumper|Diagnose the SRS with a 2-ohm air bag simulator, never a zero-ohm jumper]]
- [[notes/rst-two-sensors-must-close-together-to-deploy-the-air-bag|At least two sensors — one primary plus the safing sensor — must close together to deploy the air bag]]

## Source

- [[sources/rly-air-bag-diagnostic-monitor|Air Bag Control Module (Air Bag Diagnostic Monitor) — Description and Testing (FSM)]]
- [[sources/rst-air-bag-diagnostic-monitor|Air Bag Diagnostic Monitor and Trouble Codes — Description, Operation, and Diagnostics (FSM)]]
