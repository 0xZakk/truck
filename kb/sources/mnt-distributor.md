---
title: "Distributor and Distributor Ignition (DI) System (FSM)"
source: "manuals/factory-service-manual/1994 Ford F 150 2WD Pickup L6-300 4.9L/Repair%20and%20Diagnosis/Maintenance/Tune-up%20and%20Engine%20Performance%20Checks/Distributor/Description%20and%20Operation/index.html"
type: local
date: 2026-06-11
author: "Ford Factory Service Manual"
tags:
  - engine
  - ignition
  - distributor
  - eec-iv
processed: true
---

## Summary

The 4.9L uses a gear-driven, die-cast distributor with a Hall Effect stator assembly to trigger
the ignition coil. Critically, this system has no centrifugal or vacuum advance — all spark
advance is computed electronically. The distributor's Hall Effect switch generates the Profile
Ignition Pickup (PIP) signal sent to the Powertrain Control Module (PCM). The PCM returns a Spark
Output (SPOUT) signal to the ignition module, which switches the coil primary on and off. Each
primary interruption induces a secondary high-voltage pulse (up to ~40,000 volts) that the
distributor routes to fire the plugs in firing order.

There are two Distributor Ignition (DI) variants: Push Start (gray ICM) and Computer Controlled
Dwell (black ICM). The push-start mode allows a manual-transmission truck to be push started —
relevant to this M5OD-R2 truck. Ford cautions never to push start an automatic-transmission
vehicle. This grounds `engine` ignition diagnosis: because advance is PCM-controlled, a no-spark
or timing fault should be traced through PIP/SPOUT and the ICM, not mechanical advance parts.

## Key Points

- Gear-driven die-cast distributor with a Hall Effect stator; no centrifugal or vacuum advance.
- Hall Effect switch produces the PIP signal to the PCM.
- PCM returns SPOUT to the ignition module, which switches the coil primary on/off.
- Secondary high voltage can reach ~40,000 volts.
- Two DI types: Push Start (gray ICM) and Computer Controlled Dwell (black ICM).
- Manual-transmission trucks can be push started; never push start an automatic.

## Notable Excerpts

> "A Hall Effect stator assembly is used to trigger the ignition coil. This system does not use either centrifugal or vacuum advance mechanisms."

> "The PCM uses the PIP input to produce a Spark Output (SPOUT) signal that is sent to the ignition module to switch 'ON' and 'OFF' current in the primary voltage."

> "Push start systems feature a push start mode that will allow manual transmission equipped vehicle to be push started... CAUTION: Do not attempt to push start an automatic transmission equipped vehicle."

Source: manuals/factory-service-manual/1994 Ford F 150 2WD Pickup L6-300 4.9L/Repair%20and%20Diagnosis/Maintenance/Tune-up%20and%20Engine%20Performance%20Checks/Distributor/Description%20and%20Operation/index.html
