---
title: "DTC 111 means System Pass — the self-test found no faults"
kind: concept
source: "[[sources/dtc-self-test-overview|EEC Diagnostic Trouble Codes — Self-Test Overview and Code Conventions (FSM)]]"
related:
  - "[[notes/dtc-self-test-runs-in-koeo-and-koer-modes|The EEC self-test runs in two modes — Key On Engine Off and Key On Engine Running — and each finds different faults]]"
  - "[[notes/dtc-hard-codes-vs-memory-codes-mean-present-vs-stored|A hard code is a fault present during the test, while a memory code was stored from earlier driving]]"
tags:
  - dtc
  - self-test
  - engine
---

Unlike most diagnostic codes, DTC 111 is good news: it is listed in the FSM simply as
"System Pass." When the EEC self-test runs cleanly and finds nothing wrong, it outputs code
111 rather than going silent, so the technician can tell the difference between "the test
ran and everything checked out" and "the test never produced output."

That distinction is the reason the chart treats a missing or unlisted code separately. If
the self-test produces **no DTCs at all** — not even 111 — the chart routes to pinpoint test
QA1, which checks VREF (the reference voltage) at the self-test connector. A dead self-test
usually means the PCM is not being powered or referenced correctly, which is a different
problem from any single sensor fault. So three outcomes are meaningful: 111 (pass), a fault
code (diagnose it), or no output (go to QA1).

When working the truck's `engine`, `fuel`, or `ignition` systems, reading 111 as a "code"
and chasing it would waste time — it is the all-clear.

## Related Concepts

- [[notes/dtc-self-test-runs-in-koeo-and-koer-modes|The EEC self-test runs in two modes — Key On Engine Off and Key On Engine Running — and each finds different faults]]
- [[notes/dtc-hard-codes-vs-memory-codes-mean-present-vs-stored|A hard code is a fault present during the test, while a memory code was stored from earlier driving]]
- [[notes/dtc-codes-may-be-shared-between-modules-so-confirm-the-source|DTC numbers may be shared between modules, so confirm which module a code came from before chasing it]]

## Source

- [[sources/dtc-self-test-overview|EEC Diagnostic Trouble Codes — Self-Test Overview and Code Conventions (FSM)]]
