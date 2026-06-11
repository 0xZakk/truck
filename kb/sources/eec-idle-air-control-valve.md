---
title: "Idle Air Control (IAC) Valve — Operation, DTCs, Service, and Specs (FSM)"
source: "manuals/factory-service-manual/1994 Ford F 150 2WD Pickup L6-300 4.9L/Repair%20and%20Diagnosis/Powertrain%20Management/Computers%20and%20Control%20Systems/Idle%20Speed%2FThrottle%20Actuator%20-%20Electronic/Description%20and%20Operation/index.html"
type: local
date: 2026-06-11
author: "Ford Factory Service Manual"
tags:
  - iac
  - idle-air-control
  - idle-speed
  - eec-iv
  - adaptive-strategy
processed: true
---

## Summary

The Idle Air Control (IAC) solenoid lets the PCM control idle speed by metering intake air
around the throttle plates. It is a duty-cycle-driven solenoid linked to a reverse-seated
pintle valve. The solenoid receives 12 V from circuit VPWR; the PCM controls its ground side,
varying the duty cycle to set how much air bypasses the throttle. Besides setting idle, it
acts as a deceleration dashpot and compensates for added loads (A/C, electrical).

The IAC is integral to adaptive strategy: the PCM adjusts its calibration to correct for wear
and aging, so whenever the IAC is cleaned or replaced the FSM recommends clearing Keep Alive
Memory and expecting idle concerns until new values are learned. Two construction styles exist;
the Hitachi type without a vent/filter is serviceable and can be cleaned of sludge, while the
vent/filter type is not serviceable.

A classic failure signature is idle surging when the IAC reaches its operating limits and can
no longer compensate, hunting between upper and lower limits.

## Key Points

- Duty-cycle solenoid + pintle valve; meters air around the throttle plates to set idle.
- 12 V on VPWR; PCM controls the ground duty cycle.
- Also serves as deceleration dashpot and load (A/C/electrical) compensation.
- Part of adaptive strategy; clear KAM after cleaning/replacing, expect temporary idle concerns.
- Hitachi (no vent/filter) is serviceable/cleanable; vent/filter type is not.
- DTCs: 412 rpm could not be controlled in KOER; 415 adaptive learning at minimum limit; 416 at maximum limit.
- Idle surging is common when the IAC reaches its operating limits.
- Specs: solenoid resistance 6.0-13.0 ohms; solenoid-to-case >10,000 ohms; IAC signal 3.0-11.5 V at 3000 rpm. Retaining screws 8-11 Nm (71-97 in lb).

## Notable Excerpts

> "Idle speed surging commonly results when the IAC solenoid reaches the limits of its operation. The IAC solenoid cannot compensate for the required change in idle speed which results in the engine surging between the upper and lower limits of the IAC system."

> "Whenever an IAC component is replaced or cleaned it is recommended that the Keep Alive Memory (KAM) be cleared."

Relates to truck inventory systems `fuel` and `engine`.

Source: manuals/factory-service-manual/1994 Ford F 150 2WD Pickup L6-300 4.9L/Repair%20and%20Diagnosis/Powertrain%20Management/Computers%20and%20Control%20Systems/Idle%20Speed%2FThrottle%20Actuator%20-%20Electronic/Description%20and%20Operation/index.html
