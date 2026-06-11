---
title: "Install the TP sensor by rotating it clockwise only, or idle speed runs high"
kind: procedure
source: "[[sources/eec-throttle-position-sensor|Throttle Position Sensor (TP) — Operation, DTCs, Service, and Specs (FSM)]]"
related:
  - "[[notes/eec-tps-is-a-potentiometer-reading-06v-closed-to-45v-wot|The TP sensor is a potentiometer reading about 0.6 V closed to 4.5 V at wide-open throttle]]"
tags:
  - tps
  - throttle-position-sensor
  - procedure
  - idle-speed
  - fuel
---

The TP sensor mounts to the throttle body with two screws and engages the throttle shaft through
rotary tangs. The FSM caution is specific: slide the rotary tangs over the throttle shaft blade,
then rotate the sensor CLOCKWISE ONLY into the installed position. Installing it any other way
can leave the wiper offset and result in excessive idle speed.

Position the sensor so the connector points opposite the IAC solenoid (it will end up pointing
toward the throttle body inlet), rotate clockwise to align the scribe marks made during removal,
then torque the two screws to 2-3 Nm (18-27 in lb). Because the battery is disconnected for this
job, expect the PCM to need a ~10-mile adaptive relearn afterward. Getting this right keeps the
`fuel` and idle systems reading a correct closed-throttle baseline.

## Related Concepts

- [[notes/eec-tps-is-a-potentiometer-reading-06v-closed-to-45v-wot|The TP sensor is a potentiometer reading about 0.6 V closed to 4.5 V at wide-open throttle]]
- [[notes/sen-tps-is-a-voltage-divider-06-to-45-volts|The TP sensor is a potentiometer that outputs about 0.6 V at closed throttle and 4.5 V at wide open throttle]]
- [[notes/eec-pcm-cross-checks-tps-map-and-pulse-width-for-in-range-failures|The PCM cross-checks TP, MAP, and injector pulse width to catch in-range sensor failures]]

## Source

- [[sources/eec-throttle-position-sensor|Throttle Position Sensor (TP) — Operation, DTCs, Service, and Specs (FSM)]]
