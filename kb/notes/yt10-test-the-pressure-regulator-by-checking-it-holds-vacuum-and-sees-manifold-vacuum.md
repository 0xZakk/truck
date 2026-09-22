---
title: "Test the fuel pressure regulator by confirming it holds hand vacuum and actually sees manifold vacuum"
kind: troubleshooting
source: "[[sources/yt-diagnose-test-adjust-fuel-pressure-1980-1996-bronc|Diagnose Test & Adjust Fuel Pressure | 1980-1996 Bronco F150 | Rich/Lean | Bronco Restoration]]"
related:
  - "[[notes/eec-regulator-references-manifold-vacuum-to-hold-a-constant-injector-pressure-drop|The fuel pressure regulator references manifold vacuum to hold a constant pressure drop across the injectors]]"
tags:
  - fuel
  - fuel-pressure
  - pressure-regulator
  - troubleshooting
---

Before touching the fuel gauge, the host checks the vacuum side of the pressure regulator
on the `fuel` system. First, pull the vacuum line off the regulator and apply about 10 inches
of vacuum with a hand pump; the regulator must hold it. If the diaphragm leaks vacuum down,
the regulator is bad and gets replaced. Second, connect a vacuum gauge to the regulator's
vacuum supply line from the intake manifold and start the engine — you should see roughly
15 inches of manifold vacuum. If vacuum is low or absent, repair the line.

Both checks matter because the regulator references manifold vacuum to hold a constant pressure
drop across the injectors: as manifold vacuum rises at idle/cruise it lowers fuel pressure, and
as vacuum drops under load it raises pressure. A ruptured diaphragm or a disconnected/leaking
vacuum line therefore corrupts the mixture and can drive a rich or lean condition.

A related high-pressure check: if measured pressure is too high, pull the regulator's vacuum
line and sniff it — a fuel smell means the diaphragm has ruptured and is leaking fuel into the
vacuum side, so the regulator must be replaced.

## Related Concepts

- [[notes/eec-regulator-references-manifold-vacuum-to-hold-a-constant-injector-pressure-drop|The fuel pressure regulator references manifold vacuum to hold a constant pressure drop across the injectors]]
- [[notes/yt10-diagnose-low-fuel-pressure-by-pinching-the-return-then-supply-line|Pinch the return line, then both lines, to sort low fuel pressure between regulator, pump, and injectors]]

## Source

- [[sources/yt-diagnose-test-adjust-fuel-pressure-1980-1996-bronc|Diagnose Test & Adjust Fuel Pressure | 1980-1996 Bronco F150 | Rich/Lean | Bronco Restoration]]
