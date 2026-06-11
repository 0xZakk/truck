---
title: "Charging system"
kind: map
system_id: electrical-charging
tags:
  - electrical-charging
---

Alternator, regulator, charging wiring.

This map is the entry point for the **charging system** system of the truck. As notes are added
(via `kb-process`), link the load-bearing ones below.

## Key Notes

- [[notes/chg-all-f150-alternators-use-an-internal-regulator-at-15-volts|All F-150 alternators use an internal regulator set near 15 volts]]  ·  _spec_
- [[notes/chg-alternator-brush-and-slip-ring-wear-limits|Alternator brush and slip-ring wear limits depend on the unit's amperage rating]]  ·  _spec_
- [[notes/chg-disarm-the-air-bag-before-battery-work-on-starting-and-charging|Disarm the air bag system before disconnecting the battery for starting/charging work]]  ·  _procedure_
- [[notes/chg-alternator-no-load-test-should-read-12-to-14-volts|The alternator No-Load Test should read about 12-14 volts at 1500 RPM]]  ·  _procedure_
- [[notes/chg-charging-output-test-loads-the-system-at-2000-rpm|The charging Output Test loads the system at 2000 RPM and expects at least 1/2 volt above resting]]  ·  _procedure_
- [[notes/charging-system-works-through-three-circuits|The charging system works through three circuits: A (sense), B+ (output), and S (feedback)]]

## Common Issues

- [[notes/charge-light-staying-on-points-to-regulator-or-stator-circuit|A charge light that stays on points to the regulator or stator circuit, not always a dead alternator]]  ·  _troubleshooting_
- [[notes/chg-disconnecting-the-battery-erases-the-pcm-adaptive-strategy|Disconnecting the battery erases the PCM adaptive strategy and may need 10+ miles to relearn]]  ·  _troubleshooting_

## Sources

- [[sources/alternator-description-and-operation-fsm|Alternator — Description and Operation (FSM)]]
- [[sources/chg-alternator-specifications|Alternator — Specifications (FSM)]]
- [[sources/chg-charging-system-in-vehicle-tests|Charging System — In-Vehicle Tests (FSM)]]
- [[sources/chg-service-precautions|Starting and Charging — Service Precautions (FSM)]]
