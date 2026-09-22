---
title: "If the fuel pump doesn't buzz at key-on, check for 12 volts at the pump connector to split pump from wiring"
kind: troubleshooting
source: "[[sources/yt-diagnose-test-adjust-fuel-pressure-1980-1996-bronc|Diagnose Test & Adjust Fuel Pressure | 1980-1996 Bronco F150 | Rich/Lean | Bronco Restoration]]"
related:
  - "[[notes/eng-energize-the-fuel-pump-at-the-diagnostic-connector-to-test-pressure|Energize the fuel pump at the diagnostic connector to test pressure at the Schrader port]]"
tags:
  - fuel
  - electrical-starting
  - fuel-pump
  - troubleshooting
---

To run the pump for a pressure test, ground the fuel-pump lead at the diagnostic connector
with a jumper so the pump runs continuously with the key on. You should hear the pump buzz.
If you do not hear it, the next step distinguishes a dead pump from a supply problem on the
`fuel` and `electrical-starting` systems: check for 12 volts at the fuel-pump electrical
connector.

If 12 volts is present at the connector but the pump won't run, the pump is bad. If there is
no 12 volts, the fault is upstream — inspect the fuel-pump circuit wiring, relays, and fuses
rather than condemning the pump. This keeps you from replacing a good in-tank pump when the
real failure is a relay, fuse, or broken wire.

On a 1994 F-150, the PCM normally runs the pump for about a second at key-on and then needs an
RPM signal to keep it energized, so jumpering at the diagnostic connector is what lets the pump
run long enough for a static pressure test.

## Related Concepts

- [[notes/eng-energize-the-fuel-pump-at-the-diagnostic-connector-to-test-pressure|Energize the fuel pump at the diagnostic connector to test pressure at the Schrader port]]
- [[notes/eec-fuel-pump-runs-12s-at-key-on-then-needs-an-rpm-signal|The fuel pump runs ~1s at key-on then needs an RPM signal]]
- [[notes/rly-fuel-pump-relay-is-grounded-by-the-pcm-not-a-simple-switch|The fuel pump relay is grounded by the PCM, not a simple switch]]

## Source

- [[sources/yt-diagnose-test-adjust-fuel-pressure-1980-1996-bronc|Diagnose Test & Adjust Fuel Pressure | 1980-1996 Bronco F150 | Rich/Lean | Bronco Restoration]]
