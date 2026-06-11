---
title: "The IAC valve sets idle by metering air around the throttle plate via a PCM-controlled duty cycle"
kind: how-it-works
source: "[[sources/eec-idle-air-control-valve|Idle Air Control (IAC) Valve — Operation, DTCs, Service, and Specs (FSM)]]"
related:
  - "[[notes/eec-iac-is-part-of-adaptive-strategy-and-surges-at-its-limits|The IAC is part of adaptive strategy and surges when it reaches its learning limits]]"
  - "[[notes/unplugging-iac-while-idling-tests-the-idle-air-circuit|Unplugging the IAC while idling tests whether the idle-air circuit is involved]]"
tags:
  - iac
  - idle-air-control
  - duty-cycle
  - idle-speed
  - fuel
---

The Idle Air Control (IAC) solenoid is how the PCM controls idle speed without touching the
throttle plates. It receives a constant 12 V on circuit VPWR, and the PCM controls the ground
side, varying the duty cycle of that ground to set how long the solenoid is energized. The
solenoid is linked to a reverse-seated pintle valve that opens a bypass channel around the
throttle plates, so a higher duty cycle admits more bypass air and raises idle.

Beyond holding base idle, the IAC works as a deceleration dashpot (cushioning throttle
closing) and raises idle to absorb added loads like the A/C compressor or electrical demand.
Solenoid resistance should be 6.0-13.0 ohms, solenoid-to-case over 10,000 ohms, and the PCM
drive signal 3.0-11.5 V at 3000 rpm. This is the heart of idle behavior on the `fuel`/`engine`
systems.

## Related Concepts

- [[notes/eec-iac-is-part-of-adaptive-strategy-and-surges-at-its-limits|The IAC is part of adaptive strategy and surges when it reaches its learning limits]]
- [[notes/unplugging-iac-while-idling-tests-the-idle-air-circuit|Unplugging the IAC while idling tests whether the idle-air circuit is involved]]
- [[notes/dtc-411-and-412-mean-the-pcm-cannot-control-idle-rpm|DTCs 411 and 412 mean the PCM could not control idle RPM during the KOER self-test]]
- [[notes/eng-idle-speed-is-pcm-controlled-dont-back-off-the-throttle-stop|Idle speed is PCM-controlled — don't back off the throttle-plate stop screw]]
- [[notes/hvc-pcm-trims-idle-air-when-the-ac-clutch-engages|The PCM raises idle air when the A/C clutch engages to keep idle speed from sagging]]

## Source

- [[sources/eec-idle-air-control-valve|Idle Air Control (IAC) Valve — Operation, DTCs, Service, and Specs (FSM)]]
