---
title: "The video's 35-45 PSI fuel pressure target is for the Bronco V8s, not the 4.9L FSM spec"
kind: spec
source: "[[sources/yt-diagnose-test-adjust-fuel-pressure-1980-1996-bronc|Diagnose Test & Adjust Fuel Pressure | 1980-1996 Bronco F150 | Rich/Lean | Bronco Restoration]]"
related:
  - "[[notes/eng-fuel-pressure-is-50-60-psi-koeo-and-45-60-running|Fuel pressure is 50-60 PSI key-on/engine-off and 45-60 PSI running at idle]]"
tags:
  - fuel
  - fuel-pressure
  - spec
---

The host states a key-on/engine-off target of about 35-45 PSI and an acceptable running range
of 30-45 PSI for "these engines," working on a 5.0L/5.8L Bronco. Do **not** carry those numbers
over to a stock 1994 F-150 4.9L. The Ford factory manual for the 4.9L specifies a higher
fuel pressure: about 50-60 PSI key-on/engine-off and 45-60 PSI running at idle.

The difference is a real engine-family difference, not an ASR error: the Bronco V8 EFI systems
of this era run a lower rail pressure than the 4.9L truck. When diagnosing the `fuel` system on
a 1994 F-150, judge the reading against the FSM 50-60 / 45-60 PSI figures, and treat the video's
35-45 PSI only as the correct target for the Bronco engines it is filmed on.

The host's own truck reads ~30 PSI, which he calls lean; note that his lean condition is
compounded by a non-stock cause — a 5.0L-to-5.8L engine swap with the ECM still calibrated for
the smaller engine — so his fix (an adjustable regulator bumped to ~38 PSI) is a workaround
specific to that modified setup, not a stock-truck specification.

## Related Concepts

- [[notes/eng-fuel-pressure-is-50-60-psi-koeo-and-45-60-running|Fuel pressure is 50-60 PSI key-on/engine-off and 45-60 PSI running at idle]]
- [[notes/eng-energize-the-fuel-pump-at-the-diagnostic-connector-to-test-pressure|Energize the fuel pump at the diagnostic connector to test pressure at the Schrader port]]

## Source

- [[sources/yt-diagnose-test-adjust-fuel-pressure-1980-1996-bronc|Diagnose Test & Adjust Fuel Pressure | 1980-1996 Bronco F150 | Rich/Lean | Bronco Restoration]]
