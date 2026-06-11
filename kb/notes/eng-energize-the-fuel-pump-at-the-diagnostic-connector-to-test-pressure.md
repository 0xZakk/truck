---
title: "Energize the fuel pump at the diagnostic connector to test pressure at the Schrader port"
kind: procedure
source: "[[sources/eng-fuel-pressure|Fuel Pressure — Test Procedure and Specifications (FSM)]]"
related:
  - "[[notes/eng-fuel-pressure-is-50-60-psi-koeo-and-45-60-running|Fuel pressure is 50-60 PSI key-on/engine-off and 45-60 PSI running at idle]]"
tags:
  - engine
  - fuel-pressure
  - fuel-system
  - procedure
  - intake-exhaust
---

To read fuel pressure on the 4.9L, first observe the fuel-system service precautions and relieve
system pressure before opening anything (the warning exists to avoid fuel spillage, spray, injury,
or fire). With the key off, relieve pressure at the Schrader (test-port) fitting and install a
fuel-pressure tester on it. Then energize the pump by grounding the fuel-pump lead at the
diagnostic connector with a jumper and turning the key on with the engine off; the pump runs and
you verify the reading is within the specified limits.

Running the pump key-on/engine-off checks pump and regulator performance on the
`engine`/`intake-exhaust` inventory systems without the engine running, isolating fuel delivery
from combustion variables. It also lets you watch both the peak pressure and how well it holds
after the pump stops — a quick leak-down check of the check valve, injectors, and regulator. To
find maximum pressure, pull the vacuum hose off the regulator or hold wide-open throttle.

> "Ground the fuel pump lead of the Diagnostic Connector with a jumper. Key On, Engine Off to
> operate the fuel pump. Verify that the observed fuel pressure is within specified limits."

## Related Concepts

- [[notes/eng-fuel-pressure-is-50-60-psi-koeo-and-45-60-running|Fuel pressure is 50-60 PSI key-on/engine-off and 45-60 PSI running at idle]]
- [[notes/mnt-fuel-pressure-spec-is-50-60-psi-key-on-engine-off|The 4.9L fuel pressure spec is 50-60 PSI key-on-engine-off and 45-60 PSI at idle]]
- [[notes/eng-normal-oil-pressure-is-40-60-psi-hot-at-2000-rpm|Normal oil pressure is 40-60 PSI hot at 2000 rpm]]
- [[notes/eec-regulator-references-manifold-vacuum-to-hold-a-constant-injector-pressure-drop|The fuel pressure regulator references manifold vacuum to hold a constant pressure drop across the injectors]]
- [[notes/eec-compression-is-acceptable-if-lowest-cylinder-is-within-25-percent|Compression is acceptable if the lowest cylinder reads within 25% of the highest]]

## Source

- [[sources/eng-fuel-pressure|Fuel Pressure — Test Procedure and Specifications (FSM)]]
- [[sources/mnt-fuel-pressure|Fuel Pressure — Testing and Specifications (FSM)]]
