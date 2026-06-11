---
title: "EGR DTCs split into two families depending on whether the truck uses a pressure (PFE) or position (EVP) feedback sensor"
kind: troubleshooting
source: "[[sources/dtc-emissions-egr-codes|EEC DTCs 311-341, 558-572 — EGR and Emissions Codes (FSM)]]"
related:
  - "[[notes/dtc-secondary-air-injection-codes-come-from-the-koer-self-test|Secondary air injection DTCs are produced by the KOER self-test as the PCM commands and watches the thermactor system]]"
  - "[[notes/dtc-rationality-codes-flag-readings-that-disagree-with-other-sensors|Rationality DTCs flag a sensor reading that disagrees with the rest of the engine picture rather than a broken circuit]]"
tags:
  - dtc
  - egr
  - evp
  - emissions
  - troubleshooting
---

The EGR system on these EEC engines is monitored by one of two feedback sensors, and the DTC
chart is explicit that the codes are not interchangeable. Vehicles using an EGR valve
**pressure** sensor (the PFE/DPFE style, which infers flow from exhaust backpressure) throw
DTCs 326, 335, and 336 — and the chart notes each of these "does not apply to vehicles
equipped with EGR Valve Position (EVP) sensors." Vehicles using an EGR valve **position**
(EVP) sensor, which reads the valve's mechanical position directly, throw 327 (circuit below
minimum voltage), 337 (above maximum voltage), and the closed-voltage codes 328 (low) and 334
(high).

Knowing which sensor your truck has is therefore the first step before chasing an EGR code,
because looking up the wrong family wastes the diagnosis. DTC 332 (insufficient EGR flow
detected) is common to both and points at flow rather than the sensor. The EGR actuator side
adds 558 (vacuum regulator circuit), 571 (EGRA solenoid), and 572 (EGRV solenoid) — all
KOEO output-state circuit checks.

For the truck's `engine` emissions hardware, identifying the PFE-vs-EVP variant up front keeps
you on the right diagnostic chart.

## Related Concepts

- [[notes/dtc-secondary-air-injection-codes-come-from-the-koer-self-test|Secondary air injection DTCs are produced by the KOER self-test as the PCM commands and watches the thermactor system]]
- [[notes/dtc-rationality-codes-flag-readings-that-disagree-with-other-sensors|Rationality DTCs flag a sensor reading that disagrees with the rest of the engine picture rather than a broken circuit]]
- [[notes/dtc-self-test-runs-in-koeo-and-koer-modes|The EEC self-test runs in two modes — Key On Engine Off and Key On Engine Running — and each finds different faults]]

## Source

- [[sources/dtc-emissions-egr-codes|EEC DTCs 311-341, 558-572 — EGR and Emissions Codes (FSM)]]
