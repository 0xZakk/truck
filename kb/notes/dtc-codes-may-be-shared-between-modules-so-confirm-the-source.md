---
title: "DTC numbers may be shared between modules, so confirm which module a code came from before chasing it"
kind: concept
source: "[[sources/dtc-self-test-overview|EEC Diagnostic Trouble Codes — Self-Test Overview and Code Conventions (FSM)]]"
related:
  - "[[notes/dtc-transmission-codes-apply-only-to-the-e4od-automatic|The 600-series and 998 DTCs apply only to the E4OD automatic, not the standard M5OD manual]]"
  - "[[notes/dtc-self-test-runs-in-koeo-and-koer-modes|The EEC self-test runs in two modes — Key On Engine Off and Key On Engine Running — and each finds different faults]]"
tags:
  - dtc
  - diagnosis
  - self-test
---

The FSM's "Related Tests, Information and Procedures" page warns that DTC numbers can be
shared between control modules, so the same number means different things depending on which
module reported it. The manual's example is from a later vehicle — GEM code B1342 means the
GEM module is defective, while ABS code B1342 means an antilock brake control module failure —
but the principle holds across the truck: identify the source module first, then read the code
in that module's chart.

The page adds a second caveat: a given fault may be listed differently depending on the
retrieval method or the brand of scan tool. All codes in this manual are written as the OE
(Ford) scan tool reports them, so a number from a generic tool might not match yet still be
valid. Together these warnings explain why the chart sometimes hands a code off to a specific
component's Testing and Inspection section rather than a generic pinpoint tree — it is making
sure you land in the right module's diagnostics.

For this truck, the practical habit is: confirm whether a code came from the powertrain
(`engine`, `fuel`, `ignition`), transmission, ABS, or body module before opening a chart, so
you do not diagnose the wrong system.

## Related Concepts

- [[notes/dtc-transmission-codes-apply-only-to-the-e4od-automatic|The 600-series and 998 DTCs apply only to the E4OD automatic, not the standard M5OD manual]]
- [[notes/dtc-self-test-runs-in-koeo-and-koer-modes|The EEC self-test runs in two modes — Key On Engine Off and Key On Engine Running — and each finds different faults]]
- [[notes/dtc-111-is-system-pass-not-a-fault|DTC 111 means System Pass — the self-test found no faults]]

## Source

- [[sources/dtc-self-test-overview|EEC Diagnostic Trouble Codes — Self-Test Overview and Code Conventions (FSM)]]
