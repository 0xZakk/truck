---
title: "The ECT and IAT are identical two-lead NTC thermistors on a 5.0 V reference whose voltage drops as temperature rises"
kind: how-it-works
source: "[[sources/eec-temperature-sensors-ect-iat|ECT and IAT Temperature Sensors — Operation, DTCs, and Specs (FSM)]]"
related:
  - "[[notes/eec-ntc-temp-sensors-read-falsely-cold-with-bad-grounds|A bad ground or corroded connection makes the ECT and IAT read falsely cold]]"
tags:
  - ect
  - iat
  - thermistor
  - pcm
  - engine
---

The Engine Coolant Temperature (ECT) and Intake Air Temperature (IAT) sensors are the same
kind of part: two-lead thermistors with a *negative* temperature coefficient (NTC). The PCM
applies a 5.0 V reference to the signal lead with the return on a common sensor ground (SIG
RTN). As the medium — coolant or intake air — warms, sensor resistance falls, so the voltage
drop across the sensor decreases; the PCM reads temperature as a voltage. The FSM even reuses a
single "descriptive schematic" for both sensors, and they share the same self-test value table.

Their normal voltage ranges differ only because they track different media. The ECT runs about
3.50 V at 50 deg F down to 0.35 V at 230 deg F; the IAT runs about 3.50 V at 50 deg F down to
1.02 V at 158 deg F. The PCM combines both with MAP and TP data to set fuel-injection base
pulse width, EGR flow, and ignition timing for the `engine` and `cooling` inventory systems —
IAT also corrects for air density, since cold air is denser and carries more oxygen per unit
volume. To pass self-test, coolant must exceed 50 deg F (KOEO) or 180 deg F (KOER).

Because the two sensors are electrically identical, a useful diagnostic shortcut follows: with
the engine cold and soaked overnight, IAT and ECT should read nearly the same temperature. A
large split between them at cold start points to a bad sensor or a high-resistance circuit on
one of the two.

> "The PCM applies a 5.0 volt reference voltage to the ECT signal lead ... As the temperature of
> the engine coolant increases the resistance of the ECT sensor decreases and correspondingly the
> voltage drop across the ECT sensor is reduced."

## Related Concepts

- [[notes/eec-ntc-temp-sensors-read-falsely-cold-with-bad-grounds|A bad ground or corroded connection makes the ECT and IAT read falsely cold]]
- [[notes/dtc-temperature-sensor-codes-pair-low-and-high-voltage|Temperature sensor DTCs come in low/high pairs that mean shorted (254°F) or open (-40°F)]]
- [[notes/drv-m5od-tot-sensor-is-part-of-solenoid-body|The transmission temperature (TOT) sensor is a thermistor in the solenoid body, replaced only as an assembly]]
- [[notes/sen-eec-iv-sensors-share-vref-and-sig-rtn|Most EEC-IV sensors share a common 5.0 V VREF and SIG RTN ground, so one bad reference skews many readings]]

## Source

- [[sources/eec-temperature-sensors-ect-iat|ECT and IAT Temperature Sensors — Operation, DTCs, and Specs (FSM)]]
- [[sources/eng-coolant-temperature-sensor|Engine Coolant Temperature (ECT) Sensor — Operation, Values & DTCs (FSM)]]
- [[sources/sen-intake-air-temperature-sensor|Intake Air Temperature (IAT) Sensor — Description, Operation, and DTCs (FSM)]]
