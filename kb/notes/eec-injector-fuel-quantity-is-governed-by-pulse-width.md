---
title: "Injector fuel quantity is governed only by pulse width because lift and rail pressure are constant"
kind: how-it-works
source: "[[sources/eec-fuel-pressure-regulator-and-pump-control|Fuel Delivery — Injectors, Pressure Regulator, and Pump Control (FSM)]]"
related:
  - "[[notes/eec-regulator-references-manifold-vacuum-to-hold-a-constant-injector-pressure-drop|The fuel pressure regulator references manifold vacuum to hold a constant pressure drop across the injectors]]"
  - "[[notes/sen-closed-loop-fuel-control-targets-14-7-1|Closed-loop fuel control on the 4.9L trims injector pulse width toward 14.7:1 using the HO2S feedback]]"
tags:
  - fuel-injector
  - pulse-width
  - efi
  - fuel
---

Each fuel injector is a solenoid with a spring-loaded needle or ball valve; a current pulse from
the PCM unseats it and fuel flows through the orifice, atomized by the pintle contour. Crucially,
the injector always opens the same distance, and the fuel pressure regulator holds rail pressure
constant. With both lift and pressure fixed, the only variable left is *time* — the injector
pulse width in milliseconds.

That is why all PCM fuel control reduces to varying pulse width: closed-loop trim from the HO2S,
enrichment from throttle-rate, cold-start enrichment, and adaptive corrections all express
themselves as longer or shorter injector on-time. Injector resistance should measure 11-18 ohms;
a shorted or open injector skews the delivered quantity for that cylinder. This is the actuator
end of the `fuel` system.

## Related Concepts

- [[notes/eec-regulator-references-manifold-vacuum-to-hold-a-constant-injector-pressure-drop|The fuel pressure regulator references manifold vacuum to hold a constant pressure drop across the injectors]]
- [[notes/sen-closed-loop-fuel-control-targets-14-7-1|Closed-loop fuel control on the 4.9L trims injector pulse width toward 14.7:1 using the HO2S feedback]]

## Source

- [[sources/eec-fuel-pressure-regulator-and-pump-control|Fuel Delivery — Injectors, Pressure Regulator, and Pump Control (FSM)]]
