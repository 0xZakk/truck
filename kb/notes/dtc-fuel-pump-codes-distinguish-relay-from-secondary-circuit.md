---
title: "Fuel pump DTCs distinguish a relay primary-circuit fault from a pump secondary-circuit fault"
kind: troubleshooting
source: "[[sources/dtc-actuator-pcm-codes|EEC DTCs 542-593 — Fuel Pump, Output Actuator, and VCRM Codes (FSM)]]"
related:
  - "[[notes/dtc-vcrm-codes-report-over-current-and-open-faults-on-high-load-outputs|VCRM DTCs report over-current and open-circuit faults on the high-current loads the relay module manages]]"
  - "[[notes/eng-fuel-pressure-is-50-60-psi-koeo-and-45-60-running|Fuel pressure is 50-60 PSI key-on/engine-off and 45-60 PSI running at idle]]"
tags:
  - dtc
  - fuel-pump
  - fuel-pump-relay
  - fuel
  - troubleshooting
---

The fuel-delivery DTCs separate the control side of the pump circuit from the load side. DTC
556 is a **fuel pump relay primary circuit failure** — a fault in the low-current side the PCM
uses to switch the relay coil (routes to J1). DTCs 542 and 543 are **fuel pump secondary
circuit failures** — faults in the higher-current side that actually feeds the pump (J10/J20),
and 557 is a low-speed fuel pump primary circuit failure (X70).

This primary-vs-secondary split is the same logic used for the ignition coils, and it tells
you where to put the meter: a primary code means look at the PCM's drive wire and the relay
coil; a secondary code means look at the relay output, the inertia switch, the harness to the
tank, and the pump itself. DTC 554 (fuel pressure regulator control circuit failure) rounds
out the fuel actuator codes. Because these are circuit codes, they confirm a wiring or relay
fault rather than a worn pump — but a real no-start should still be cross-checked against
actual fuel pressure.

For the truck's `fuel` system, these codes localize a cranks-but-won't-start to a specific
segment of the pump power path.

## Related Concepts

- [[notes/dtc-vcrm-codes-report-over-current-and-open-faults-on-high-load-outputs|VCRM DTCs report over-current and open-circuit faults on the high-current loads the relay module manages]]
- [[notes/eng-fuel-pressure-is-50-60-psi-koeo-and-45-60-running|Fuel pressure is 50-60 PSI key-on/engine-off and 45-60 PSI running at idle]]
- [[notes/rly-fuel-pump-relay-is-grounded-by-the-pcm-not-a-simple-switch|The fuel pump relay is grounded by the PCM, so its ground circuit is the real no-start clue]]
- [[notes/rly-eec-power-relay-feeds-the-fuel-pump-relay-coil|Power to the fuel pump relay comes from the EEC power relay through the PCM and the inertia switch]]
- [[notes/dtc-coil-primary-failure-codes-defer-to-the-ignition-system-section|Coil-primary-failure DTCs are detected by the PCM but defer to the Ignition System section to diagnose]]
- [[notes/eec-fuel-pump-runs-12s-at-key-on-then-needs-an-rpm-signal|The fuel pump runs 1-2 s at key-on, then the PCM keeps it running only with an rpm signal above 120]]
- [[notes/rly-pcm-power-relay-supplies-bplus-and-gives-reverse-battery-protection|The PCM power relay supplies B+ to the PCM and protects it against reverse battery polarity]]

## Source

- [[sources/dtc-actuator-pcm-codes|EEC DTCs 542-593 — Fuel Pump, Output Actuator, and VCRM Codes (FSM)]]
