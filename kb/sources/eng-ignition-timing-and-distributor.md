---
title: "Distributor & Ignition Timing — Hall-Effect Operation and Timing Procedure (FSM)"
source: "manuals/factory-service-manual/1994 Ford F 150 2WD Pickup L6-300 4.9L/Repair%20and%20Diagnosis/Engine%2C%20Cooling%20and%20Exhaust/Engine/Tune-up%20and%20Engine%20Performance%20Checks/Distributor/Description%20and%20Operation/index.html"
type: local
date: 2026-06-11
author: "Ford Factory Service Manual"
tags:
  - engine
  - distributor
  - ignition-timing
  - spout
  - pip
processed: true
---

## Summary

The 4.9L distributor is a gear-driven die-cast unit that uses a Hall-effect stator to
trigger the coil; it has no centrifugal or vacuum advance. The Hall-effect switch generates
the Profile Ignition Pickup (PIP) signal to the PCM, which returns a Spark Output (SPOUT)
signal to the ignition module to switch primary current on and off, producing secondary
voltage up to 40,000 V. On the closed-bowl distributor the ignition module is remotely
mounted. Two DI systems exist: push-start (gray ICM, allows a manual-transmission truck to
be push started) and computer-controlled dwell (black ICM, PCM controls coil charge time).

Setting initial timing relies on isolating the SPOUT signal: with the transmission in
neutral and A/C/heater off, connect an inductive timing light, disconnect the in-line SPOUT
connector (or pull the shorting bar), then set base timing to 10 degrees BTDC at idle.
The FSM warns to start the engine with the ignition key only — using a remote starter or
disconnecting the start wire forces the ignition module into start-mode timing that won't
self-correct. After setting, reconnect SPOUT and verify the timing advances past the base
setting.

This source backs the `engine` inventory system.

## Key Points

- Distributor is gear-driven with a Hall-effect stator; no centrifugal or vacuum advance.
- PIP signal from the Hall switch goes to the PCM; PCM returns SPOUT to the ignition module.
- ICM color identifies the system: gray = push-start, black = computer-controlled dwell.
- Do NOT push-start an automatic-transmission vehicle (this truck is manual).
- Base timing: 10 degrees BTDC at idle.
- Timing procedure: neutral, A/C/heater off, inductive timing light, disconnect in-line
  SPOUT connector (or pull shorting bar), set base, reconnect, verify advance.
- Start with the ignition key only — a remote starter locks in start-mode timing.

## Notable Excerpts

> "A Hall Effect stator assembly is used to trigger the ignition coil. This system does not
> use either centrifugal or vacuum advance mechanisms."

> "Disconnect the single wire in-line Spark Output (SPOUT) connector or remove the shorting
> bar from the double wire SPOUT connector. ... check or adjust initial timing to specification."

> "To set timing correctly, a remote starter should not be used. Use the ignition key only to
> start the vehicle."

Source: manuals/factory-service-manual/1994 Ford F 150 2WD Pickup L6-300 4.9L/Repair%20and%20Diagnosis/Engine%2C%20Cooling%20and%20Exhaust/Engine/Tune-up%20and%20Engine%20Performance%20Checks/ (Distributor Description and Operation, Ignition Timing Adjustments and Specifications)
