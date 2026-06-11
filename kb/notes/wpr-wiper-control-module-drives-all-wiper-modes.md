---
title: "The wiper control module, not the switch, drives all wiper and washer modes from switch signals"
kind: how-it-works
source: "[[sources/wpr-wiper-control-module|Wiper Control Module and Interval Wipe Operation (FSM)]]"
related:
  - "[[notes/wpr-interval-first-wipe-can-lag-up-to-12-seconds|The first interval wipe can lag up to 12 seconds, which is normal]]"
  - "[[notes/wpr-wiper-and-washer-switch-are-one-multi-function-switch|The wiper switch and washer switch are a single multi-function switch on the steering column]]"
tags:
  - wiper-control-module
  - interval-wipers
  - electrical-body
---

On the 1994 F-150 the wiper switch does not directly power the wiper motor through
all of its speeds. Instead, an electronic wiper control module receives signals from
the multi-function (wiper) switch and performs the washer, low-speed, high-speed, and
interval wiper functions. The switch is an input device; the module is the actuator
and timer.

The module lives behind the right-hand side of the instrument panel, near the top of
the cowl panel. Knowing this matters for diagnosis: a wiper symptom that only affects
one mode (for example, interval not working while low and high speed are fine) points
at the module or its timing logic rather than at the motor or the switch, which is
why the FSM's pinpoint tests separate symptoms by mode.

This module ties into the truck inventory system `electrical-body`.

## Related Concepts

- [[notes/wpr-interval-first-wipe-can-lag-up-to-12-seconds|The first interval wipe can lag up to 12 seconds, which is normal]]
- [[notes/wpr-wiper-and-washer-switch-are-one-multi-function-switch|The wiper switch and washer switch are a single multi-function switch on the steering column]]
- [[notes/wpr-park-test-confirms-the-motor-stops-in-park|The park test confirms the wiper motor cycles once and stops in the Park position]]

## Source

- [[sources/wpr-wiper-control-module|Wiper Control Module and Interval Wipe Operation (FSM)]]
