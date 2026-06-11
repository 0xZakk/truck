---
title: "EEC Diagnostic Trouble Codes — Self-Test Overview and Code Conventions (FSM)"
source: "manuals/factory-service-manual/1994 Ford F 150 2WD Pickup L6-300 4.9L/Repair%20and%20Diagnosis/A%20L%20L%20%20Diagnostic%20Trouble%20Codes%20%28%20DTC%20%29/Testing%20and%20Inspection/Related%20Tests%2C%20Information%20and%20Procedures/index.html"
type: local
date: 2026-06-11
author: "Ford Factory Service Manual"
tags: [dtc, self-test, koeo, koer, powertrain-management, diagnosis]
processed: true
---

## Summary

The 1994 F-150's powertrain self-diagnostics report faults as three-digit Diagnostic
Trouble Codes (DTCs). Every code chart in this section opens with the same legend: KOEO
means **Key On Engine Off**, KOER means **Key On Engine Running**, and DTCs are to be
diagnosed in the order they are received. The codes are retrieved by running the EEC
self-test and reading the output, then each code routes the technician to a lettered
pinpoint test (for example DA, DH, DC, H, KE, TC) or, for some faults, directly to a
component's own Testing and Inspection section.

A given code can appear under different test conditions, and the chart distinguishes them:
**KOEO Hard Code** (fault present right now, key on, engine off), **KOER Hard Code** (fault
present with the engine running), and **KOEO Memory Code** (fault stored in Keep Alive
Memory from earlier driving but not necessarily present now). The same numeric code may
point to a different pinpoint test depending on which of these conditions produced it,
which is why the chart lists separate routing for each.

The "Related Tests, Information and Procedures" page adds an important caveat: DTC numbers
can be shared between control modules, and the same fault may be reported differently
depending on the retrieval method or scan tool. All codes here are listed as the OE
(Ford) scan tool reports them. Always confirm which module a code came from before chasing
a diagnostic chart.

## Key Points

- KOEO = Key On Engine Off; KOER = Key On Engine Running; diagnose DTCs in the order received.
- Three reporting conditions: KOEO Hard Code, KOER Hard Code, KOEO Memory Code.
- A hard code is present at the time of test; a memory code was stored from a previous fault.
- Each code routes to a lettered pinpoint test or to a component's Testing and Inspection.
- DTC 111 = System Pass (no faults). "No DTCs output / not listed" routes to QA1 (check VREF).
- DTC numbers may be shared across modules and may differ by scan tool; verify the source module.

## Notable Excerpts

> "KOEO refers to Key On Engine Off (KOEO). KOER refers to Key On Engine Running (KOER).
> DTC refers to Diagnostic Trouble Code (DTC). DTCs should be diagnosed in the order they
> are received."

> "On many vehicles, diagnostic trouble codes (DTC's) numbers may be shared between modules.
> Be sure you know which group of codes you have requested and the actual code name/number
> before looking for the related diagnostic chart."

> "DTC 111 — System Pass."

Source: manuals/factory-service-manual/1994 Ford F 150 2WD Pickup L6-300 4.9L/Repair%20and%20Diagnosis/A%20L%20L%20%20Diagnostic%20Trouble%20Codes%20%28%20DTC%20%29/Testing%20and%20Inspection/Related%20Tests%2C%20Information%20and%20Procedures/index.html
