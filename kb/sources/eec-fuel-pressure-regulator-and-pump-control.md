---
title: "Fuel Delivery — Injectors, Pressure Regulator, and Pump Control (FSM)"
source: "manuals/factory-service-manual/1994 Ford F 150 2WD Pickup L6-300 4.9L/Repair%20and%20Diagnosis/Powertrain%20Management/Fuel%20Delivery%20and%20Air%20Induction/Fuel%20Pressure%20Regulator/Description%20and%20Operation/index.html"
type: local
date: 2026-06-11
author: "Ford Factory Service Manual"
tags:
  - fuel-injector
  - fuel-pressure-regulator
  - fuel-pump-relay
  - inertia-switch
  - fuel-pressure
  - fuel
processed: true
---

## Summary

The fuel injectors are electro-mechanical solenoids that meter and atomize fuel. Each has a
spring-loaded needle or ball valve; a current pulse from the PCM unseats it and fuel flows
through the orifice, atomized by the pintle contour. Because the injector always opens the same
distance and the regulator holds rail pressure constant, the fuel delivered depends only on how
long the nozzle is held open — the injector pulse width in milliseconds. Injector resistance is
11-18 ohms.

The fuel pressure regulator is a spring-loaded, diaphragm-operated relief valve that controls
pressure to the injectors. One side of the diaphragm senses fuel pressure; the other connects to
intake-manifold vacuum, so balancing against manifold vacuum keeps a constant pressure drop
across the injectors regardless of load. Fuel in excess of engine demand bypasses the regulator
and returns to the tank. The regulator also traps fuel at shutdown to prevent vapor formation,
giving instant restarts and proper initial idle.

Fuel pump operation is governed by the PCM through the fuel pump relay, gated by the EEC power
relay and the Inertia Fuel Shutoff (IFS) switch. At key-on the pump runs ~1-2 seconds; if the
PCM gets no ignition signal within about one second, a PCM timer opens the relay ground and
stops the pump. The PCM closes the ground at START and during running, but opens it (killing the
pump) if engine speed drops below 120 rpm. Measured system pressure is 50-60 PSI key-on/engine-off
and 45-60 PSI at idle; maximum pressure is read with the regulator vacuum hose removed or at WOT.

## Key Points

- Injector: solenoid + spring-loaded needle/ball; PCM current pulse unseats the valve; atomization from pintle contour.
- Constant injector lift and rail pressure mean fuel quantity is governed by pulse width (ms); injector resistance 11-18 ohms.
- Regulator: spring/diaphragm relief valve referenced to manifold vacuum, constant injector pressure drop.
- Excess fuel returns to tank; regulator traps fuel at shutdown for restarts and initial idle.
- Pump runs ~1-2 s at key-on; PCM stops it if no ignition signal within ~1 s.
- PCM opens the fuel pump relay ground if engine speed falls below 120 rpm.
- Pump control path: EEC power relay -> fuel pump relay -> IFS switch -> pump.
- Pressure: 345-415 kPa (50-60 PSI) KOEO; 310-415 kPa (45-60 PSI) at idle.
- Max pressure obtained with regulator vacuum hose off or at WOT.
- Regulator retaining screws: 3-5 Nm (27-44 in lb).

## Notable Excerpts

> "Balancing one side of the diaphragm with manifold vacuum maintains a constant fuel pressure drop across the injectors. Fuel in excess of that used by the engine is bypassed through the regulator and returns to the fuel tank."

> "The PCM monitors engine speed and opens the fuel pump relay ground circuit if the engine speed drops below 120 rpm."

> "The amount of fuel delivered by the injector depends on the amount of time that the nozzle is open. This is the injector pulse width."

Relates to truck inventory system `fuel`.

Source: manuals/factory-service-manual/1994 Ford F 150 2WD Pickup L6-300 4.9L/Repair%20and%20Diagnosis/Powertrain%20Management/Fuel%20Delivery%20and%20Air%20Induction/Fuel%20Pressure%20Regulator/Description%20and%20Operation/index.html
