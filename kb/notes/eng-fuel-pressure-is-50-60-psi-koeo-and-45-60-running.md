---
title: "Fuel pressure is 50-60 PSI key-on/engine-off and 45-60 PSI running at idle"
kind: spec
source: "[[sources/eng-fuel-pressure|Fuel Pressure — Test Procedure and Specifications (FSM)]]"
related:
  - "[[notes/eng-energize-the-fuel-pump-at-the-diagnostic-connector-to-test-pressure|Energize the fuel pump at the diagnostic connector to test pressure at the Schrader port]]"
tags:
  - engine
  - fuel-pressure
  - intake-exhaust
  - specifications
---

Fuel pressure on the injected 4.9L is 50-60 PSI (345-415 kPa) with the key on and engine off, and
45-60 PSI (310-415 kPa) with the engine running at idle. The running pressure is lower because the
fuel pressure regulator references intake-manifold vacuum, and the high vacuum at idle pulls the
regulated pressure down. Maximum pressure is reached with the regulator's vacuum hose removed or
at wide-open throttle.

These are the reference values for the `engine` and `intake-exhaust` inventory systems when
diagnosing hard starting, stumble, or lean/rich complaints. Low KOEO pressure points at the pump,
filter, or a leaking regulator; pressure that doesn't rise when the vacuum line is pulled points at
a stuck or failed regulator.

> "Key On Engine Off 345-415 kPa (50-60 PSI) Key On Engine Running (Idle Speed) 310-415 kPa
> (45-60 PSI)."

## Related Concepts

- [[notes/eng-energize-the-fuel-pump-at-the-diagnostic-connector-to-test-pressure|Energize the fuel pump at the diagnostic connector to test pressure at the Schrader port]]
- [[notes/mnt-fuel-pressure-spec-is-50-60-psi-key-on-engine-off|The 4.9L fuel pressure spec is 50-60 PSI key-on-engine-off and 45-60 PSI at idle]]
- [[notes/eec-regulator-references-manifold-vacuum-to-hold-a-constant-injector-pressure-drop|The fuel pressure regulator references manifold vacuum to hold a constant pressure drop across the injectors]]
- [[notes/eng-normal-oil-pressure-is-40-60-psi-hot-at-2000-rpm|Normal oil pressure is 40-60 PSI hot at 2000 rpm]]

## Source

- [[sources/eng-fuel-pressure|Fuel Pressure — Test Procedure and Specifications (FSM)]]
