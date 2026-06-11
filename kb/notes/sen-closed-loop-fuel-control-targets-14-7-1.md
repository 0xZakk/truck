---
title: "Closed-loop fuel control on the 4.9L trims injector pulse width toward 14.7:1 using the HO2S feedback"
kind: how-it-works
source: "[[sources/sen-oxygen-sensor|Heated Oxygen Sensor (HO2S) — Description, Operation, and Testing (FSM)]]"
related:
  - "[[notes/sen-ho2s-voltage-tells-pcm-rich-vs-lean|The HO2S reports rich vs. lean by generating a high voltage when exhaust oxygen is low and a low voltage when it is high]]"
  - "[[notes/sen-ect-resistance-falls-as-coolant-warms|The ECT is a negative-coefficient thermistor whose voltage drops as the engine warms, and a bad ground reads falsely cold]]"
tags:
  - fuel
  - closed-loop
  - eec-iv
  - ho2s
---

"Closed loop" describes the operating mode where the PCM stops relying purely on its internal
maps and starts correcting fuel delivery from a live measurement. On the 1994 F-150 that
measurement is the HO2S voltage: the PCM watches it swing rich/lean and continuously adjusts
the base injector pulse width to hold the average air/fuel ratio at 14.7:1, the stoichiometric
point where the catalytic converter works best.

The base pulse width the loop corrects is itself computed from other inputs — engine load
(MAP), engine and intake air temperature (ECT/IAT), throttle position (TP), and rpm — so the
oxygen sensor is the *trim* on top of a calculated starting point, not the whole calculation.
The system can only close the loop once the HO2S is hot enough to be trusted.

This note ties the `fuel` system together: nearly every other powertrain sensor feeds the base
fuel calculation, and the HO2S is the feedback that closes the loop around it.

## Related Concepts

- [[notes/sen-ho2s-voltage-tells-pcm-rich-vs-lean|The HO2S reports rich vs. lean by generating a high voltage when exhaust oxygen is low and a low voltage when it is high]]
- [[notes/sen-ect-resistance-falls-as-coolant-warms|The ECT is a negative-coefficient thermistor whose voltage drops as the engine warms, and a bad ground reads falsely cold]]
- [[notes/eec-ho2s-must-exceed-600f-so-it-has-a-built-in-heater|The HO2S needs 600 deg F to work, so a built-in heater shortens warm-up before closed loop]]
- [[notes/sen-ho2s-must-reach-600f-and-uses-a-heater|The HO2S only reads accurately above 600°F, which is why it carries an internal heater]]
- [[notes/eec-injector-fuel-quantity-is-governed-by-pulse-width|Injector fuel quantity is governed only by pulse width because lift and rail pressure are constant]]
- [[notes/eec-ho2s-generates-voltage-from-exhaust-vs-atmosphere-oxygen-difference|The HO2S generates voltage from the oxygen difference between exhaust and atmosphere]]

## Source

- [[sources/sen-oxygen-sensor|Heated Oxygen Sensor (HO2S) — Description, Operation, and Testing (FSM)]]
