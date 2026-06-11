---
title: "The HO2S only reads accurately above 600°F, which is why it carries an internal heater"
kind: how-it-works
source: "[[sources/sen-oxygen-sensor|Heated Oxygen Sensor (HO2S) — Description, Operation, and Testing (FSM)]]"
related:
  - "[[notes/sen-ho2s-voltage-tells-pcm-rich-vs-lean|The HO2S reports rich vs. lean by generating a high voltage when exhaust oxygen is low and a low voltage when it is high]]"
tags:
  - oxygen-sensor
  - ho2s
  - fuel
---

The zirconium-dioxide cell in the oxygen sensor is only chemically active once hot — the FSM
specifies it must be above 600°F to operate properly. Until then its output is unreliable and
the PCM cannot trust it, so the engine runs open-loop (on programmed maps) right after a cold
start. To shorten that period, the sensor has a built-in heating element.

That heater is why the 1994 F-150 uses a **4-wire** HO2S rather than a bare 1-wire sensor:
besides the signal wire and signal return (SIG RTN) ground, there are two heater wires — a
12 V supply taken from the Ignition Run circuit and a heater ground. The heater draws power
whenever the key is in Run.

A burned-out heater element delays closed-loop entry and can keep the sensor from staying hot
at idle, hurting `fuel` trim and emissions even though the sensing element itself is fine.

## Related Concepts

- [[notes/sen-ho2s-voltage-tells-pcm-rich-vs-lean|The HO2S reports rich vs. lean by generating a high voltage when exhaust oxygen is low and a low voltage when it is high]]
- [[notes/eec-ho2s-must-exceed-600f-so-it-has-a-built-in-heater|The HO2S needs 600 deg F to work, so a built-in heater shortens warm-up before closed loop]]
- [[notes/eec-ho2s-generates-voltage-from-exhaust-vs-atmosphere-oxygen-difference|The HO2S generates voltage from the oxygen difference between exhaust and atmosphere]]
- [[notes/sen-closed-loop-fuel-control-targets-14-7-1|Closed-loop fuel control on the 4.9L trims injector pulse width toward 14.7:1 using the HO2S feedback]]

## Source

- [[sources/sen-oxygen-sensor|Heated Oxygen Sensor (HO2S) — Description, Operation, and Testing (FSM)]]
