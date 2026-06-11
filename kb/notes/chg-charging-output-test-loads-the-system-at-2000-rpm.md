---
title: "The charging Output Test loads the system at 2000 RPM and expects at least 1/2 volt above resting"
kind: procedure
source: "[[sources/chg-charging-system-in-vehicle-tests|Charging System — In-Vehicle Tests (FSM)]]"
related:
  - "[[notes/chg-alternator-no-load-test-should-read-12-to-14-volts|The alternator No-Load Test should read about 12-14 volts at 1500 RPM]]"
  - "[[notes/charging-system-works-through-three-circuits|The charging system works through three circuits: A (sense), B+ (output), and S (feedback)]]"
tags:
  - charging-system
  - alternator
  - procedure
  - diagnosis
---

The factory in-vehicle Output Test checks that the alternator can hold voltage while
actually carrying load. With a tachometer connected, turn the A/C blower motor to maximum
and the headlamps to high beam, then raise engine speed to approximately 2000 RPM. The
voltmeter should read a **minimum of 1/2 volt above normal** (resting) voltage. If it does,
the charging system is operating correctly.

This test pairs with the No-Load Test: No-Load proves the alternator can charge an unloaded
battery, while the Output Test proves it can still push current with the heaviest electrical
loads switched on. If the Output reading is out of range, the manual routes you to the Over
Voltage or Under Voltage tests.

> "Increase engine speed to approximately 2000 RPM. Voltmeter should indicate a minimum of
> 1/2 volt above normal. … If voltage is within specifications, the charging system is
> operating correctly."

This relates to truck inventory system `electrical-charging`.

## Related Concepts

- [[notes/chg-alternator-no-load-test-should-read-12-to-14-volts|The alternator No-Load Test should read about 12-14 volts at 1500 RPM]]
- [[notes/charging-system-works-through-three-circuits|The charging system works through three circuits: A (sense), B+ (output), and S (feedback)]]
- [[notes/ipc-voltmeter-normal-range-is-13-5-to-14-volts|A normal voltmeter reading on the F-150 is 13.5 to 14.0 volts]]

## Source

- [[sources/chg-charging-system-in-vehicle-tests|Charging System — In-Vehicle Tests (FSM)]]
