---
title: "Testing the cruise servo is mostly a connector-pin and broken-wire inspection"
kind: troubleshooting
source: "[[sources/crz-speed-control-servo-and-cable|Speed Control Servo and Actuator Cable — Description, Testing, Adjustment (FSM)]]"
related:
  - "[[notes/crz-servo-cable-needs-0-04-inch-of-slack|The cruise actuator cable must be left with 0.04 inch of slack, never pulled tight]]"
  - "[[notes/crz-diagnose-cruise-with-a-visual-check-first|Cruise control diagnosis starts with a visual check, and ABS must be healthy first]]"
tags:
  - cruise-control
  - servo
  - troubleshooting
---

The FSM's servo "test" is deliberately simple: inspect the speed control servo assembly for
loose or unseated connector pins or broken wires at the connectors. The actuator cable gets a
parallel check — inspect the Bowden cable for improper adjustment (readjust as required) and
check for a broken actuator cable.

The takeaway for the `electrical-body` system is that intermittent or dead cruise frequently
comes down to the servo's connector, not the servo electronics. Before condemning the
servo/amplifier, back-probe and reseat its connector, look for spread or backed-out pins, and
confirm no wires are broken at the connector body. Pair this with the cable inspection: a
broken or maladjusted cable produces the same "won't hold speed" complaint as an electrical
fault, but is far cheaper to fix.

> "Inspect speed control servo assembly for loose or unseated connector pins or broken wires
> at the connectors."

## Related Concepts

- [[notes/crz-servo-cable-needs-0-04-inch-of-slack|The cruise actuator cable must be left with 0.04 inch of slack, never pulled tight]]
- [[notes/crz-diagnose-cruise-with-a-visual-check-first|Cruise control diagnosis starts with a visual check, and ABS must be healthy first]]

## Source

- [[sources/crz-speed-control-servo-and-cable|Speed Control Servo and Actuator Cable — Description, Testing, Adjustment (FSM)]]
