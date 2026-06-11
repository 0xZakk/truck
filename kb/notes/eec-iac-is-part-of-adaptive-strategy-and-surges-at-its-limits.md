---
title: "The IAC is part of adaptive strategy and surges when it reaches its learning limits"
kind: troubleshooting
source: "[[sources/eec-idle-air-control-valve|Idle Air Control (IAC) Valve — Operation, DTCs, Service, and Specs (FSM)]]"
related:
  - "[[notes/eec-iac-meters-air-around-the-throttle-plate-via-pcm-duty-cycle|The IAC valve sets idle by metering air around the throttle plate via a PCM-controlled duty cycle]]"
  - "[[notes/eec-pcm-learns-an-adaptive-strategy-stored-in-kam|The PCM learns an adaptive strategy in Keep Alive Memory to compensate for component wear]]"
tags:
  - iac
  - idle-air-control
  - troubleshooting
  - adaptive-strategy
  - rough-idle
---

The IAC plays an integral role in adaptive strategy: the PCM continuously adjusts the IAC
calibration to correct for wear and aging. The FSM logs DTC 415 when adaptive learning hits its
minimum limit (valve reducing airflow as far as possible) and DTC 416 at the maximum limit
(admitting as much air as possible); DTC 412 means rpm could not be held within band during the
KOER self-test.

A characteristic symptom appears when the IAC reaches the limits of its operation: it can no
longer compensate for the required idle change, so the engine surges, hunting between the upper
and lower limits of the IAC system. Because the IAC is adaptive, the FSM recommends clearing
Keep Alive Memory whenever the valve is cleaned or replaced, and warns of temporary idle
concerns until new values are learned. The serviceable Hitachi (no vent/filter) type can be
cleaned of sludge; the vent/filter type cannot. This is a common `fuel`/`engine` rough-idle path.

## Related Concepts

- [[notes/eec-iac-meters-air-around-the-throttle-plate-via-pcm-duty-cycle|The IAC valve sets idle by metering air around the throttle plate via a PCM-controlled duty cycle]]
- [[notes/eec-pcm-learns-an-adaptive-strategy-stored-in-kam|The PCM learns an adaptive strategy in Keep Alive Memory to compensate for component wear]]
- [[notes/dtc-411-and-412-mean-the-pcm-cannot-control-idle-rpm|DTCs 411 and 412 mean the PCM could not control idle RPM during the KOER self-test]]

## Source

- [[sources/eec-idle-air-control-valve|Idle Air Control (IAC) Valve — Operation, DTCs, Service, and Specs (FSM)]]
