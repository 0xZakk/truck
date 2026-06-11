---
title: "EEC DTCs 211-244 — Ignition and Spark Codes (FSM)"
source: "manuals/factory-service-manual/1994 Ford F 150 2WD Pickup L6-300 4.9L/Repair%20and%20Diagnosis/A%20L%20L%20%20Diagnostic%20Trouble%20Codes%20%28%20DTC%20%29/Testing%20and%20Inspection/Manufacturer%20Code%20Charts/184-219/index.html"
type: local
date: 2026-06-11
author: "Ford Factory Service Manual"
tags: [dtc, ignition, pip, idm, spark, coil, knock-sensor]
processed: true
---

## Summary

The 200-series ignition DTCs report faults in the distributor ignition system: the Profile
Ignition Pickup (PIP) crankshaft position signal, the Ignition Diagnostic Monitor (IDM)
feedback, the SPOUT/spark output circuit, the Cylinder Identification (CID) signal, and the
ignition coil primary circuits. DTC 211 is a PIP circuit failure (routes to NA1, Erratic
Ignition). DTC 212 means the PCM lost the IDM input or the spark output circuit is grounded
(NA2). DTC 213 is spark output circuit open (PA1), and DTC 219 means spark timing defaulted
to 10 degrees with the spark output circuit open. DTC 214 is a cylinder identification
circuit failure.

A large block of codes (215, 216, 217, 224, 232, 238) report that the PCM detected a coil
primary circuit failure on a specific coil or group of coils; these route directly to the
Ignition System Testing and Inspection section rather than to a pinpoint test. Several
others — 218 (loss of IDM signal, left side), 221 (spark timing error), 222 (loss of IDM
signal, right side), 223 (loss of dual plug inhibit control), and 241 (IDM pulsewidth
transmission error between the ignition control module and PCM) — also defer to the Ignition
System section. DTC 225 means knock was not sensed during the KOER dynamic response test
(routes to DG1), and DTC 226 means the IDM signal was not received at all (NC2). DTC 244 is
a CID circuit fault detected when a cylinder balance test was requested.

## Key Points

- 211 = PIP (crank position) circuit failure → NA1; 226 = IDM signal not received → NC2.
- 212 = lost IDM input or spark output grounded → NA2.
- 213 = spark output circuit open → PA1; 219 = timing defaulted to 10° with spark output open.
- 214 / 244 = Cylinder Identification (CID) circuit fault → DR1.
- 215/216/217/224/232/238 = PCM-detected coil primary circuit failure → Ignition System T&I.
- 225 = knock not sensed during KOER dynamic response test → DG1 (knock sensor check).

## Notable Excerpts

> "DTC 211 — Profile ignition pickup circuit failure."

> "DTC 213 — Spark output circuit open."

> "DTC 219 — Spark timing defaulted to 10 degrees, spark output circuit open."

> "DTC 225 — Knock not sensed during dynamic response test KOER."

Source: manuals/factory-service-manual/1994 Ford F 150 2WD Pickup L6-300 4.9L/Repair%20and%20Diagnosis/A%20L%20L%20%20Diagnostic%20Trouble%20Codes%20%28%20DTC%20%29/Testing%20and%20Inspection/Manufacturer%20Code%20Charts/ (pages 184-219, 221-326)
