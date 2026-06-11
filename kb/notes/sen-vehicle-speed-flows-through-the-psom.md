---
title: "Vehicle speed reaches the PCM through the PSOM, which converts the axle sensor signal to 8000 pulses per mile"
kind: how-it-works
source: "[[sources/sen-vehicle-speed-sensor|Vehicle Speed Sensor / PSOM and Differential Speed Sensor — Description and Operation (FSM)]]"
related:
  - "[[notes/sen-pcm-reads-throttle-mode-and-rate-from-tps|The PCM derives idle, cruise, WOT, and acceleration-pump action from TP angle and its rate of change]]"
tags:
  - vehicle-speed-sensor
  - psom
  - electrical-body
---

The 1994 F-150 doesn't send the raw speed sensor straight to the PCM. A Differential Speed
Sensor (DSS) at the rear axle generates the original signal, and the Programmable
Speedometer/Odometer Module (PSOM) — the electronic module behind the speedometer — reads it,
then re-emits a clean, standardized **8000 pulses-per-mile** signal. That conditioned signal is
what the PCM, the speed-control servo amplifier, and the instrument cluster all consume.

This architecture matters for the `electrical-body` system because the PSOM is a single point
of failure for several functions at once. A PSOM fault can simultaneously kill the speedometer,
disable cruise control, and throw off the PCM's speed-based decisions (shift scheduling and, on
automatics, torque-converter-clutch lockup), setting DTC 29/452.

It also explains a diagnostic ordering: if the speedometer is dead but the truck drives fine,
suspect the DSS-to-PSOM stage; if speed-dependent powertrain behavior is wrong, look at the
PSOM-to-PCM output. Pinpoint tests live in the system-level DS routine.

## Related Concepts

- [[notes/sen-pcm-reads-throttle-mode-and-rate-from-tps|The PCM derives idle, cruise, WOT, and acceleration-pump action from TP angle and its rate of change]]
- [[notes/ipc-speedometer-is-electronic-psom-fed-by-the-abs-sensor|The 1994 F-150 speedometer is an electronic PSOM fed by the ABS/differential speed sensor, not a cable]]
- [[notes/crz-speed-reference-comes-from-the-psom-or-vss|Cruise control regulates against the speed signal from the PSOM or VSS]]
- [[notes/ipc-reprogram-the-psom-conversion-constant-when-tire-size-changes|Reprogram the PSOM conversion constant whenever tire size changes]]
- [[notes/eec-tps-is-a-potentiometer-reading-06v-closed-to-45v-wot|The TP sensor is a potentiometer reading about 0.6 V closed to 4.5 V at wide-open throttle]]

## Source

- [[sources/sen-vehicle-speed-sensor|Vehicle Speed Sensor / PSOM and Differential Speed Sensor — Description and Operation (FSM)]]
