---
title: "The fuel pressure regulator references manifold vacuum to hold a constant pressure drop across the injectors"
kind: how-it-works
source: "[[sources/eec-fuel-pressure-regulator-and-pump-control|Fuel Delivery — Injectors, Pressure Regulator, and Pump Control (FSM)]]"
related:
  - "[[notes/eec-injector-fuel-quantity-is-governed-by-pulse-width|Injector fuel quantity is governed only by pulse width because lift and rail pressure are constant]]"
  - "[[notes/eec-fuel-pump-runs-12s-at-key-on-then-needs-an-rpm-signal|The fuel pump runs 1-2 s at key-on, then the PCM keeps it running only with an rpm signal above 120]]"
tags:
  - fuel-pressure-regulator
  - manifold-vacuum
  - fuel-pressure
  - fuel
---

The fuel pressure regulator is a spring-loaded, diaphragm-operated relief valve. One side of the
diaphragm senses fuel pressure; the other connects to intake-manifold vacuum. By referencing
manifold vacuum, the regulator keeps a *constant pressure drop* across the injectors regardless
of manifold pressure, so a given pulse width always delivers the same fuel. Excess fuel bypasses
the regulator and returns to the tank.

This vacuum reference is why maximum fuel pressure is read with the regulator's vacuum hose
removed or at wide-open throttle. System pressure should be 345-415 kPa (50-60 PSI) key-on/
engine-off and 310-415 kPa (45-60 PSI) at idle. The regulator also traps fuel at shutdown to
prevent vapor lock, giving instant restarts and proper initial idle. Together with the injectors,
it defines fuel metering for the `fuel` system. Regulator retaining screws torque to 3-5 Nm
(27-44 in lb).

## Related Concepts

- [[notes/eec-injector-fuel-quantity-is-governed-by-pulse-width|Injector fuel quantity is governed only by pulse width because lift and rail pressure are constant]]
- [[notes/eec-fuel-pump-runs-12s-at-key-on-then-needs-an-rpm-signal|The fuel pump runs 1-2 s at key-on, then the PCM keeps it running only with an rpm signal above 120]]
- [[notes/mnt-fuel-pressure-spec-is-50-60-psi-key-on-engine-off|The 4.9L fuel pressure spec is 50-60 PSI key-on-engine-off and 45-60 PSI at idle]]
- [[notes/eng-fuel-pressure-is-50-60-psi-koeo-and-45-60-running|Fuel pressure is 50-60 PSI key-on/engine-off and 45-60 PSI running at idle]]
- [[notes/eng-energize-the-fuel-pump-at-the-diagnostic-connector-to-test-pressure|Energize the fuel pump at the diagnostic connector to test pressure at the Schrader port]]

## Source

- [[sources/eec-fuel-pressure-regulator-and-pump-control|Fuel Delivery — Injectors, Pressure Regulator, and Pump Control (FSM)]]
