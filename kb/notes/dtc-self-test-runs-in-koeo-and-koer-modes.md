---
title: "The EEC self-test runs in two modes — Key On Engine Off and Key On Engine Running — and each finds different faults"
kind: how-it-works
source: "[[sources/dtc-self-test-overview|EEC Diagnostic Trouble Codes — Self-Test Overview and Code Conventions (FSM)]]"
related:
  - "[[notes/dtc-hard-codes-vs-memory-codes-mean-present-vs-stored|A hard code is a fault present during the test, while a memory code was stored from earlier driving]]"
  - "[[notes/dtc-111-is-system-pass-not-a-fault|DTC 111 means System Pass — the self-test found no faults]]"
tags:
  - dtc
  - self-test
  - koeo
  - koer
  - engine
---

The 1994 F-150's EEC powertrain self-test is run in two distinct modes, and the FSM code
charts label every code by the mode that produced it. **KOEO** is Key On Engine Off: the
ignition is on but the engine is not running, so the PCM can check static circuit
continuity and sensor voltages and exercise its output drivers without combustion
interfering. **KOER** is Key On Engine Running: with the engine actually turning, the PCM
can verify dynamic behavior — that the oxygen sensors switch, that EGR flows, that knock is
sensed, and that it can command RPM up and down.

Because the two modes test different things, the same component can throw different codes
depending on the mode. A throttle-position circuit short shows up in KOEO; a "knock not
sensed" fault (DTC 225) can only appear during a KOER dynamic response test because it needs
a running engine to provoke knock. The chart's standing instruction is that DTCs should be
diagnosed in the order they are received, so the technician works the list top to bottom
rather than chasing whichever code seems most alarming.

This framework underlies diagnosis across the truck's `engine`, `fuel`, and `ignition`
systems, since all three report through the same EEC self-test.

## Related Concepts

- [[notes/dtc-hard-codes-vs-memory-codes-mean-present-vs-stored|A hard code is a fault present during the test, while a memory code was stored from earlier driving]]
- [[notes/dtc-111-is-system-pass-not-a-fault|DTC 111 means System Pass — the self-test found no faults]]
- [[notes/dtc-225-confirms-the-knock-sensor-during-the-koer-dynamic-test|DTC 225 means knock was not sensed during the KOER dynamic response test, a knock-sensor check]]
- [[notes/sen-koer-self-test-provokes-knock-to-check-the-ks|The KOER self-test deliberately advances timing to provoke knock and confirm the knock sensor responds]]
- [[notes/dtc-egr-codes-split-by-pressure-sensor-vs-position-sensor|EGR DTCs split into two families depending on whether the truck uses a pressure (PFE) or position (EVP) feedback sensor]]
- [[notes/dtc-switch-input-codes-fail-when-the-truck-is-not-staged-for-self-test|Switch-input DTCs often just mean the truck was not staged correctly — in gear, A/C on, or brake not pressed]]

## Source

- [[sources/dtc-self-test-overview|EEC Diagnostic Trouble Codes — Self-Test Overview and Code Conventions (FSM)]]
