---
title: "Most EEC-IV sensors share a common 5.0 V VREF and SIG RTN ground, so one bad reference skews many readings"
kind: troubleshooting
source: "[[sources/sen-throttle-position-sensor|Throttle Position (TP) Sensor — Description, Operation, and DTCs (FSM)]]"
related:
  - "[[notes/eec-tps-is-a-potentiometer-reading-06v-closed-to-45v-wot|The TP sensor is a potentiometer reading about 0.6 V closed to 4.5 V at wide-open throttle]]"
  - "[[notes/eec-ntc-temp-sensors-read-falsely-cold-with-bad-grounds|A bad ground or added resistance makes the NTC ECT and IAT read falsely cold, driving a needless rich condition]]"
  - "[[notes/eec-map-sensor-outputs-a-frequency-and-doubles-as-a-baro-sensor|The MAP sensor outputs a frequency proportional to load and doubles as a barometric sensor]]"
tags:
  - eec-iv
  - vref
  - sig-rtn
  - fuel
  - troubleshooting
---

Reading the FSM sensor pages together reveals a shared architecture: the TP sensor, ECT, IAT,
and MAP all run on the same two PCM-supplied references — a 5.0 volt reference (VREF) and a
common signal return (SIG RTN) ground. The PCM puts VREF out, the sensor modifies it (a
potentiometer wiper, a thermistor's resistance, or a frequency circuit), and the modified value
returns on the signal lead referenced to SIG RTN.

The diagnostic payoff: because these references are shared, a single fault on VREF or SIG RTN
misreports *several* sensors at once. A SIG RTN with extra resistance (corroded ground) adds to
every thermistor's reading and biases the potentiometers; a dragged-down or shorted VREF shifts
the TP and MAP outputs together. So when ECT, IAT, and TP all read implausibly at the same time,
suspect the common reference circuit before condemning three sensors.

For the `fuel` system this is the difference between chasing one ghost three times and fixing one
bad ground or VREF wire. The ECT page's warning about high-resistance grounds reading "lower
than actual" is one symptom of this shared-circuit reality.

## Related Concepts

- [[notes/eec-tps-is-a-potentiometer-reading-06v-closed-to-45v-wot|The TP sensor is a potentiometer reading about 0.6 V closed to 4.5 V at wide-open throttle]]
- [[notes/eec-ntc-temp-sensors-read-falsely-cold-with-bad-grounds|A bad ground or added resistance makes the NTC ECT and IAT read falsely cold, driving a needless rich condition]]
- [[notes/eec-map-sensor-outputs-a-frequency-and-doubles-as-a-baro-sensor|The MAP sensor outputs a frequency proportional to load and doubles as a barometric sensor]]
- [[notes/eec-ect-and-iat-are-ntc-thermistors-on-a-5v-reference|The ECT and IAT are identical two-lead NTC thermistors on a 5.0 V reference whose voltage drops as temperature rises]]
- [[notes/eec-pcm-cross-checks-tps-map-and-pulse-width-for-in-range-failures|The PCM cross-checks TP, MAP, and injector pulse width to catch in-range sensor failures]]

## Source

- [[sources/sen-throttle-position-sensor|Throttle Position (TP) Sensor — Description, Operation, and DTCs (FSM)]]
