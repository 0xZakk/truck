---
title: "The HO2S reports rich vs. lean by generating a high voltage when exhaust oxygen is low and a low voltage when it is high"
kind: how-it-works
source: "[[sources/sen-oxygen-sensor|Heated Oxygen Sensor (HO2S) — Description, Operation, and Testing (FSM)]]"
related:
  - "[[notes/sen-ho2s-must-reach-600f-and-uses-a-heater|The HO2S only reads accurately above 600°F, which is why it carries an internal heater]]"
  - "[[notes/sen-closed-loop-fuel-control-targets-14-7-1|Closed-loop fuel control on the 4.9L trims injector pulse width toward 14.7:1 using the HO2S feedback]]"
tags:
  - oxygen-sensor
  - ho2s
  - fuel
---

The heated oxygen sensor is a zirconium-dioxide cell that measures the *difference* in oxygen
between two sides: its outside is vented to atmosphere, and its tip is bathed in the exhaust
stream. That oxygen imbalance is what generates the sensor's voltage, so the HO2S does not
read air/fuel ratio directly — it reads how much oxygen survived combustion.

A rich mixture burns up nearly all the oxygen, leaving a big imbalance and a **high** output
voltage. A lean mixture leaves oxygen in the exhaust, shrinking the imbalance and producing a
**low** output. The normal swing is about 0.0 V (lean) to 1.1 V (rich). The PCM watches this
signal switch back and forth and trims fueling to keep the average near stoichiometric.

For the truck's `fuel` system this is the core feedback that makes the EEC-IV system "closed
loop": a lazy or biased HO2S signal will skew fuel trim and show up as a fuel-control fault
during the system-level **H – Fuel Control** pinpoint tests.

## Related Concepts

- [[notes/sen-ho2s-must-reach-600f-and-uses-a-heater|The HO2S only reads accurately above 600°F, which is why it carries an internal heater]]
- [[notes/sen-closed-loop-fuel-control-targets-14-7-1|Closed-loop fuel control on the 4.9L trims injector pulse width toward 14.7:1 using the HO2S feedback]]
- [[notes/eec-ho2s-generates-voltage-from-exhaust-vs-atmosphere-oxygen-difference|The HO2S generates voltage from the oxygen difference between exhaust and atmosphere]]
- [[notes/eec-ho2s-must-exceed-600f-so-it-has-a-built-in-heater|The HO2S needs 600 deg F to work, so a built-in heater shortens warm-up before closed loop]]

## Source

- [[sources/sen-oxygen-sensor|Heated Oxygen Sensor (HO2S) — Description, Operation, and Testing (FSM)]]
