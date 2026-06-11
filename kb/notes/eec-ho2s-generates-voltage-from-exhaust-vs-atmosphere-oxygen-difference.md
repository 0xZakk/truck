---
title: "The HO2S generates voltage from the oxygen difference between exhaust and atmosphere"
kind: how-it-works
source: "[[sources/eec-oxygen-sensor|Heated Oxygen Sensor (HO2S) — EEC-IV Description, Operation, and Specs (FSM)]]"
related:
  - "[[notes/eec-ho2s-must-exceed-600f-so-it-has-a-built-in-heater|The HO2S needs 600 deg F to work, so a built-in heater shortens warm-up before closed loop]]"
  - "[[notes/sen-closed-loop-fuel-control-targets-14-7-1|Closed-loop fuel control on the 4.9L trims injector pulse width toward 14.7:1 using the HO2S feedback]]"
tags:
  - oxygen-sensor
  - ho2s
  - fuel
  - closed-loop
---

The Heated Exhaust Gas Oxygen Sensor is a zirconium-dioxide ceramic thimble with a platinum
electrode. Its outside is vented to atmosphere while its inside is exposed to the exhaust
stream, and the zirconium dioxide is electrically sensitive to the difference in oxygen between
those two sources. That difference is what makes the sensor generate its own voltage.

A rich mixture burns most of the oxygen, leaving little in the exhaust; the large oxygen
difference produces a higher voltage. A lean mixture leaves more oxygen in the exhaust, a
smaller difference, and a lower voltage. Normal output spans 0.0 V (lean) to 1.1 V (rich). The
PCM reads this swing in closed loop to keep the `fuel` system at 14.7:1. After driving 55 mph
for 5 minutes the signal should swing between 0.3 and 0.9 V within 3 seconds.

## Related Concepts

- [[notes/eec-ho2s-must-exceed-600f-so-it-has-a-built-in-heater|The HO2S needs 600 deg F to work, so a built-in heater shortens warm-up before closed loop]]
- [[notes/sen-closed-loop-fuel-control-targets-14-7-1|Closed-loop fuel control on the 4.9L trims injector pulse width toward 14.7:1 using the HO2S feedback]]
- [[notes/sen-ho2s-voltage-tells-pcm-rich-vs-lean|The HO2S reports rich vs. lean by generating a high voltage when exhaust oxygen is low and a low voltage when it is high]]
- [[notes/sen-ho2s-must-reach-600f-and-uses-a-heater|The HO2S only reads accurately above 600°F, which is why it carries an internal heater]]

## Source

- [[sources/eec-oxygen-sensor|Heated Oxygen Sensor (HO2S) — EEC-IV Description, Operation, and Specs (FSM)]]
