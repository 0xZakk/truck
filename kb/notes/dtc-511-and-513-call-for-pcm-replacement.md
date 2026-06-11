---
title: "DTCs 511 and 513 are internal PCM failures that the chart resolves by replacing the PCM"
kind: troubleshooting
source: "[[sources/dtc-idle-speed-input-codes|EEC DTCs 411-539 — Idle Speed, Vehicle Speed, and Switch Input Codes (FSM)]]"
related:
  - "[[notes/dtc-hard-codes-vs-memory-codes-mean-present-vs-stored|A hard code is a fault present during the test, while a memory code was stored from earlier driving]]"
  - "[[notes/dtc-111-is-system-pass-not-a-fault|DTC 111 means System Pass — the self-test found no faults]]"
tags:
  - dtc
  - powertrain-control-module
  - keep-alive-memory
  - troubleshooting
---

Most DTCs route to a pinpoint test, but a few point at the computer itself. DTC 511 is a PCM
Read Only Memory test failure during the KOEO self-test, and 513 is a PCM internal voltage
failure during the KOEO self-test. For both, the chart's resolution under every condition —
KOEO Hard, KOER Hard, and KOEO Memory — is simply "Replace Powertrain Control Module." There
is no wiring to chase: the processor has failed its own internal check.

DTC 512 is the softer relative: a Keep Alive Memory (KAM) test failure. KAM is the battery-
backed RAM that stores adaptive fuel trims and learned values, and a 512 routes to pinpoint
test QB1 rather than to outright replacement, because a KAM fault can be caused by lost
keep-alive power (a blown fuse or corroded battery connection) rather than a dead module.
The distinction is worth respecting: 511/513 condemn the PCM, but 512 first asks whether the
module is simply losing its memory power.

These bear on the truck's `engine`, `fuel`, and `ignition` systems at once, since the PCM
governs all three.

## Related Concepts

- [[notes/dtc-hard-codes-vs-memory-codes-mean-present-vs-stored|A hard code is a fault present during the test, while a memory code was stored from earlier driving]]
- [[notes/dtc-111-is-system-pass-not-a-fault|DTC 111 means System Pass — the self-test found no faults]]
- [[notes/dtc-self-test-runs-in-koeo-and-koer-modes|The EEC self-test runs in two modes — Key On Engine Off and Key On Engine Running — and each finds different faults]]

## Source

- [[sources/dtc-idle-speed-input-codes|EEC DTCs 411-539 — Idle Speed, Vehicle Speed, and Switch Input Codes (FSM)]]
