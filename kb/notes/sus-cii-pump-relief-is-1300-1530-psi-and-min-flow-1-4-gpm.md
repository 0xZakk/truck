---
title: "CII pump relief pressure is 1300-1530 psi with min flow around 1.4 GPM"
kind: spec
source: "[[sources/sus-power-steering-pump|Power Steering Pump (Ford CII) (FSM)]]"
related:
  - "[[notes/sus-power-steering-pressure-test-isolates-pump-gear-or-hose-faults|The power steering pressure/flow test isolates pump, gear, or hose faults]]"
tags:
  - steering
  - power-steering
  - power-steering-pump
  - spec
---

The Ford CII power steering pump comes in several calibrations identified by model code, all
with similar limits. The base HBC-HG reads minimum relief pressure 1300 psi, maximum relief
pressure 1530 psi, and minimum flow 1.4 GPM measured at 740 psi. Other models span the same
envelope: HBC-HN 1350/1530 psi at 1.5 GPM, HBC-JX 1400/1530 at 1.4 GPM, HBC-JY 1450/1530 at
1.5 GPM, and HBC-KK 1400/1530 at 1.4 GPM.

The FSM cautions that minimum flow depends on pump model, engine RPM, and pulley drive ratio,
so engine speed must be set to specification when checking flow capacity. Use these numbers
as the pass/fail reference during the analyzer pressure/flow test of the `steering` system —
relief pressure below the minimum or flow under spec condemns the pump's cam pack or flow-
control valve.

## Related Concepts

- [[notes/sus-power-steering-pressure-test-isolates-pump-gear-or-hose-faults|The power steering pressure/flow test isolates pump, gear, or hose faults]]

## Source

- [[sources/sus-power-steering-pump|Power Steering Pump (Ford CII) (FSM)]]
