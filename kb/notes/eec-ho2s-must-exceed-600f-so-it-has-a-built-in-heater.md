---
title: "The HO2S needs 600 deg F to work, so a built-in heater shortens warm-up before closed loop"
kind: spec
source: "[[sources/eec-oxygen-sensor|Heated Oxygen Sensor (HO2S) — EEC-IV Description, Operation, and Specs (FSM)]]"
related:
  - "[[notes/eec-ho2s-generates-voltage-from-exhaust-vs-atmosphere-oxygen-difference|The HO2S generates voltage from the oxygen difference between exhaust and atmosphere]]"
tags:
  - oxygen-sensor
  - ho2s
  - heater
  - fuel
---

The HO2S must be above 600 deg F to produce a valid signal, so a heating element is built into
the sensor to minimize warm-up time and let the PCM enter closed loop sooner. The HO2S uses a
4-wire connection: the sensor output (HO2S), sensor ground (SIG RTN), a 12 V heater supply from
the Ignition Run circuit, and a separate heater ground.

The heater element has measurable resistance specs useful for diagnosis: 2.0-5.0 ohms at room
temperature and 5.0-30.0 ohms hot-to-warm. An open heater circuit slows the sensor reaching
operating temperature, delaying closed-loop `fuel` control and degrading cold-running economy
and emissions even if the sensing element itself is fine.

## Related Concepts

- [[notes/eec-ho2s-generates-voltage-from-exhaust-vs-atmosphere-oxygen-difference|The HO2S generates voltage from the oxygen difference between exhaust and atmosphere]]
- [[notes/sen-ho2s-must-reach-600f-and-uses-a-heater|The HO2S only reads accurately above 600°F, which is why it carries an internal heater]]
- [[notes/sen-ho2s-voltage-tells-pcm-rich-vs-lean|The HO2S reports rich vs. lean by generating a high voltage when exhaust oxygen is low and a low voltage when it is high]]
- [[notes/sen-closed-loop-fuel-control-targets-14-7-1|Closed-loop fuel control on the 4.9L trims injector pulse width toward 14.7:1 using the HO2S feedback]]

## Source

- [[sources/eec-oxygen-sensor|Heated Oxygen Sensor (HO2S) — EEC-IV Description, Operation, and Specs (FSM)]]
