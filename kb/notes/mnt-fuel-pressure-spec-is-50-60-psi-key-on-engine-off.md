---
title: "The 4.9L fuel pressure spec is 50-60 PSI key-on-engine-off and 45-60 PSI at idle"
kind: spec
source: "[[sources/mnt-fuel-pressure|Fuel Pressure — Testing and Specifications (FSM)]]"
related:
  - "[[notes/mnt-grounding-the-fuel-pump-lead-runs-the-pump-key-on-engine-off|Grounding the diagnostic-connector fuel-pump lead runs the pump with the key on and engine off]]"
  - "[[notes/mnt-fuel-filter-is-a-high-pressure-canister-protecting-injector-orifices|The fuel filter is a high-pressure paper-element canister protecting the injector orifices]]"
tags:
  - engine
  - fuel-system
  - spec
---

For the 4.9L EFI `engine`, fuel rail pressure should read 345-415 kPa (50-60 PSI) with the key
on and engine off, and 310-415 kPa (45-60 PSI) at idle. The idle figure is lower because manifold
vacuum acting on the fuel pressure regulator pulls rail pressure down under load-off conditions.

Maximum fuel pressure is obtained with the vacuum hose removed from the regulator, or at wide-open
throttle where manifold vacuum approaches zero. This gives a useful diagnostic lever: if pressure
does not rise when the regulator vacuum hose is pulled, the regulator is suspect; if pressure is
low across the board, look upstream at the pump, filter, or a line restriction.

## Related Concepts

- [[notes/mnt-grounding-the-fuel-pump-lead-runs-the-pump-key-on-engine-off|Grounding the diagnostic-connector fuel-pump lead runs the pump with the key on and engine off]]
- [[notes/mnt-fuel-filter-is-a-high-pressure-canister-protecting-injector-orifices|The fuel filter is a high-pressure paper-element canister protecting the injector orifices]]
- [[notes/eng-fuel-pressure-is-50-60-psi-koeo-and-45-60-running|Fuel pressure is 50-60 PSI key-on/engine-off and 45-60 PSI running at idle]]
- [[notes/eng-energize-the-fuel-pump-at-the-diagnostic-connector-to-test-pressure|Energize the fuel pump at the diagnostic connector to test pressure at the Schrader port]]
- [[notes/eec-regulator-references-manifold-vacuum-to-hold-a-constant-injector-pressure-drop|The fuel pressure regulator references manifold vacuum to hold a constant pressure drop across the injectors]]

## Source

- [[sources/mnt-fuel-pressure|Fuel Pressure — Testing and Specifications (FSM)]]
