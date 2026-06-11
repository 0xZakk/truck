---
title: "Grounding the diagnostic-connector fuel-pump lead runs the pump with the key on and engine off"
kind: procedure
source: "[[sources/mnt-fuel-pressure|Fuel Pressure — Testing and Specifications (FSM)]]"
related:
  - "[[notes/mnt-fuel-pressure-spec-is-50-60-psi-key-on-engine-off|The 4.9L fuel pressure spec is 50-60 PSI key-on-engine-off and 45-60 PSI at idle]]"
tags:
  - engine
  - fuel-system
  - procedure
---

To test fuel pressure on the `engine` without starting it, the FSM has you energize the pump
directly. With the key off, relieve system pressure at the Schrader fitting (per the fuel service
precautions), then install the fuel pressure tester. Ground the fuel-pump lead at the diagnostic
connector with a jumper and turn the key on with the engine off; this runs the pump so you can
read static rail pressure.

Running the pump key-on-engine-off isolates the delivery side from combustion and lets you watch
both the peak pressure and how well it holds after the pump stops (a quick leak-down check of the
check valve, injectors, and regulator). Always observe the fuel service precautions when relieving
pressure to avoid spray and fire.

## Related Concepts

- [[notes/mnt-fuel-pressure-spec-is-50-60-psi-key-on-engine-off|The 4.9L fuel pressure spec is 50-60 PSI key-on-engine-off and 45-60 PSI at idle]]
- [[notes/eng-energize-the-fuel-pump-at-the-diagnostic-connector-to-test-pressure|Energize the fuel pump at the diagnostic connector to test pressure at the Schrader port]]
- [[notes/eng-fuel-pressure-is-50-60-psi-koeo-and-45-60-running|Fuel pressure is 50-60 PSI key-on/engine-off and 45-60 PSI running at idle]]

## Source

- [[sources/mnt-fuel-pressure|Fuel Pressure — Testing and Specifications (FSM)]]
