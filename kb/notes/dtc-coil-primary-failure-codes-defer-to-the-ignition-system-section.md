---
title: "Coil-primary-failure DTCs are detected by the PCM but defer to the Ignition System section to diagnose"
kind: troubleshooting
source: "[[sources/dtc-ignition-codes|EEC DTCs 211-244 — Ignition and Spark Codes (FSM)]]"
related:
  - "[[notes/dtc-211-and-226-point-to-the-pip-and-idm-crank-signals|DTCs 211 and 226 point at the PIP and IDM crank-timing signals the PCM needs to fire the ignition]]"
  - "[[notes/dtc-codes-may-be-shared-between-modules-so-confirm-the-source|DTC numbers may be shared between modules, so confirm which module a code came from before chasing it]]"
tags:
  - dtc
  - ignition
  - ignition-coil
  - troubleshooting
---

A cluster of 200-series codes — 215, 216, 217, 224, 232, and 238 — all read as "Powertrain
control module detected coil [N] primary circuit failure." The PCM monitors the primary
(low-voltage) side of the ignition coil(s) and sets one of these when it sees the primary
circuit fail. What makes them distinctive in the chart is the routing: instead of sending the
technician to a lettered pinpoint test, each of these entries says "Go to Ignition System /
Testing and Inspection."

That deferral is a useful signal. It tells you the EEC self-test has done its job — it has
told you which coil circuit the PCM thinks is bad — but the actual coil resistance checks,
connector inspection, and primary-circuit wiring tests live in the dedicated Ignition System
chapter rather than in the EEC pinpoint trees. Related codes 218/222 (loss of IDM signal
left/right), 221 (spark timing error), 223 (loss of dual plug inhibit control), and 241 (IDM
pulsewidth transmission error between the ignition module and PCM) defer the same way.

For the 4.9L's `ignition` system, these codes narrow the suspect to a specific coil primary
circuit, then hand off to the coil's own test procedure.

## Related Concepts

- [[notes/dtc-211-and-226-point-to-the-pip-and-idm-crank-signals|DTCs 211 and 226 point at the PIP and IDM crank-timing signals the PCM needs to fire the ignition]]
- [[notes/dtc-codes-may-be-shared-between-modules-so-confirm-the-source|DTC numbers may be shared between modules, so confirm which module a code came from before chasing it]]
- [[notes/dtc-fuel-pump-codes-distinguish-relay-from-secondary-circuit|Fuel pump DTCs distinguish a relay primary-circuit fault from a pump secondary-circuit fault]]

## Source

- [[sources/dtc-ignition-codes|EEC DTCs 211-244 — Ignition and Spark Codes (FSM)]]
