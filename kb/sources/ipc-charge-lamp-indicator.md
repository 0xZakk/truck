---
title: "Charge Lamp / Indicator — Description, Operation and Testing (FSM)"
source: "manuals/factory-service-manual/1994 Ford F 150 2WD Pickup L6-300 4.9L/Repair and Diagnosis/Instrument Panel, Gauges and Warning Indicators/Charge Lamp/Indicator/Description and Operation/index.html"
type: local
date: 2026-06-11
author: "Ford Factory Service Manual"
tags:
  - charge-lamp
  - warning-indicators
  - charging-system
  - alternator
  - voltage-regulator
processed: true
---

## Summary

The charge (alternator) warning lamp alerts the driver when charging output falls below the
normal range. Its operation is tied directly to the integral voltage regulator. With the
ignition in START or RUN, battery current flows through the warning indicator into the
regulator at terminal "1" and to ground through the regulator's internal indicator switch —
which is what lights the lamp. The regulator's electronic control senses low voltage at
terminal A and closes the field switch, applying battery voltage to the field through
terminal F. With field current and the rotor turning, the stator produces voltage at
terminals B and S. Once a predetermined voltage appears at terminal S, the electronic
control opens the indicator switch, removing the ground and turning the lamp OFF.

The FSM troubleshooting confirms the lamp's two-sided nature. If the lamp does not light with
ignition ON and engine off, check the bulb first; if good, check for an open between the
ignition switch and the regulator terminal. A jumper from regulator connector terminal "1"
to the negative battery post should light the lamp — if not, the bulb, the circuit to the
regulator, or a 500-ohm resistor across the lamp (if equipped) is at fault.

## Key Points

- Lamp is ground-switched by the integral regulator's internal indicator switch (regulator terminal "1").
- In START/RUN, current flows battery -> lamp -> regulator terminal 1 -> ground, lighting the lamp.
- Regulator senses low voltage at terminal A, closes field switch, energizes field via terminal F.
- Predetermined voltage at terminal S opens the indicator switch and turns the lamp OFF.
- No light with key ON, engine off: check bulb, then for an open between ignition switch and regulator.
- Jumper test: terminal "1" to battery negative should light the lamp; a 500-ohm resistor may parallel the lamp.

## Notable Excerpts

> "When the ignition switch is in START or RUN position, battery current flows through the
> alternator warning indicator into regulator at terminal 1 and to ground through the
> indicator switch."

> "A predetermined voltage at terminal S operates the electronic control to open indicator
> switch, which removes ground from alternator warning indicator."

> "connect a jumper wire between 1 terminal of regulator electrical connector and negative
> battery post cable clamp. With ignition turned to ON position, indicator lamp should light."

Source: FSM — Instrument Panel, Gauges and Warning Indicators / Charge Lamp/Indicator / Description and Operation and Testing and Inspection.
