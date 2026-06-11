---
title: "A hard code is a fault present during the test, while a memory code was stored from earlier driving"
kind: troubleshooting
source: "[[sources/dtc-self-test-overview|EEC Diagnostic Trouble Codes — Self-Test Overview and Code Conventions (FSM)]]"
related:
  - "[[notes/dtc-self-test-runs-in-koeo-and-koer-modes|The EEC self-test runs in two modes — Key On Engine Off and Key On Engine Running — and each finds different faults]]"
  - "[[notes/dtc-111-is-system-pass-not-a-fault|DTC 111 means System Pass — the self-test found no faults]]"
tags:
  - dtc
  - self-test
  - troubleshooting
  - engine
---

Every entry in the FSM code charts splits its diagnostic routing by whether the code is a
**Hard Code** or a **Memory Code**, and the distinction matters when you decide how to chase
it. A hard code (KOEO Hard Code or KOER Hard Code) means the fault is present right now, at
the moment of test — the circuit is shorted, open, or out of range as you read it. A KOEO
Memory Code means the fault was stored in Keep Alive Memory from earlier operation but is not
necessarily occurring during the test.

This drives the pinpoint test the chart sends you to. For DTC 112 (IAT below minimum
voltage), a KOEO Hard Code routes to DA20, but the same code as a Memory Code routes to DA90
— a different procedure aimed at catching an intermittent. Hard codes point you at a fault
you can measure on the bench; memory codes point you at wiggle tests, simulated road shock,
and intermittent-fault hunting because the problem has already come and gone. Mistaking one
for the other sends you down the wrong diagnostic branch.

This applies whenever you pull codes from the `engine`, `fuel`, or `ignition` systems through
the EEC self-test.

## Related Concepts

- [[notes/dtc-self-test-runs-in-koeo-and-koer-modes|The EEC self-test runs in two modes — Key On Engine Off and Key On Engine Running — and each finds different faults]]
- [[notes/dtc-111-is-system-pass-not-a-fault|DTC 111 means System Pass — the self-test found no faults]]
- [[notes/dtc-511-and-513-call-for-pcm-replacement|DTCs 511 and 513 are internal PCM failures that the chart resolves by replacing the PCM]]

## Source

- [[sources/dtc-self-test-overview|EEC Diagnostic Trouble Codes — Self-Test Overview and Code Conventions (FSM)]]
