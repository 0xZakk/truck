---
title: "DTCs 411 and 412 mean the PCM could not control idle RPM during the KOER self-test"
kind: troubleshooting
source: "[[sources/dtc-idle-speed-input-codes|EEC DTCs 411-539 — Idle Speed, Vehicle Speed, and Switch Input Codes (FSM)]]"
related:
  - "[[notes/dtc-self-test-runs-in-koeo-and-koer-modes|The EEC self-test runs in two modes — Key On Engine Off and Key On Engine Running — and each finds different faults]]"
  - "[[notes/dtc-switch-input-codes-fail-when-the-truck-is-not-staged-for-self-test|Switch-input DTCs often just mean the truck was not staged correctly — in gear, A/C on, or brake not pressed]]"
tags:
  - dtc
  - idle-air-control
  - koer
  - troubleshooting
  - engine
---

During the KOER self-test the PCM commands the Idle Air Control (IAC) valve to drive idle
speed up and down to prove it can govern RPM. DTC 411 means it "cannot control RPM during the
KOER self-test low RPM check," and 412 means it "cannot control RPM during the high RPM
check." In other words, the PCM moved the IAC but the engine speed did not follow as expected.

These codes implicate the whole idle-air path, not just the valve: a stuck or carboned-up IAC,
a vacuum leak (which lets unmetered air bypass the valve so the PCM loses authority), a
throttle plate that does not seat, or a base idle set wrong. The adaptive companion codes 415
(IAC at maximum lower adaptive limit) and 416 (IAC at upper adaptive learning limit) say the
PCM has been steadily compensating in one direction until it ran out of adjustment — a slow
drift rather than an acute failure. 411/412 route to the KE pinpoint tests.

For the truck's `engine` idle behavior — hunting, stalling, or a too-high idle — these are the
codes to read first.

## Related Concepts

- [[notes/dtc-self-test-runs-in-koeo-and-koer-modes|The EEC self-test runs in two modes — Key On Engine Off and Key On Engine Running — and each finds different faults]]
- [[notes/dtc-switch-input-codes-fail-when-the-truck-is-not-staged-for-self-test|Switch-input DTCs often just mean the truck was not staged correctly — in gear, A/C on, or brake not pressed]]
- [[notes/eec-iac-is-part-of-adaptive-strategy-and-surges-at-its-limits|The IAC is part of adaptive strategy and surges when it reaches its learning limits]]
- [[notes/eec-iac-meters-air-around-the-throttle-plate-via-pcm-duty-cycle|The IAC valve sets idle by metering air around the throttle plate via a PCM-controlled duty cycle]]
- [[notes/eng-idle-speed-is-pcm-controlled-dont-back-off-the-throttle-stop|Idle speed is PCM-controlled — don't back off the throttle-plate stop screw]]

## Source

- [[sources/dtc-idle-speed-input-codes|EEC DTCs 411-539 — Idle Speed, Vehicle Speed, and Switch Input Codes (FSM)]]
