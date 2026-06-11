---
title: "Alternator — Description and Operation (FSM)"
source: manuals/factory-service-manual/1994 Ford F 150 2WD Pickup L6-300 4.9L/Repair%20and%20Diagnosis/Starting%20and%20Charging/Charging%20System/Alternator/Description%20and%20Operation/index.html
type: local
date: 2026-06-11
author: "Ford Factory Service Manual"
tags:
  - alternator
  - charging-system
  - voltage-regulator
  - electrical
  - how-it-works
processed: true
---

## Summary

The factory service manual's description of how the 1994 F-150 charging system works. With
voltage applied, the regulator activates and feeds current from the **A (sensing) circuit**
to the alternator field coil. The alternator produces AC, which an internal rectifier
converts to DC and supplies to the truck through the **B+ terminal**. A **stator (S)
circuit** feeds a voltage signal (typically half battery voltage) back to the regulator,
which uses it to turn the charge indicator lamp off.

This three-circuit picture (A sense / B+ output / S feedback) is the mental model for every
charging-system diagnosis on this truck.

## Key Points

- Field current flows when the regulator is energized via the A (sensing) circuit.
- The alternator generates AC; an internal rectifier converts it to DC out the B+ terminal.
- The stator (S) circuit feeds ~half battery voltage back to the regulator to control the
  warning lamp — so a charge lamp that stays on is a regulator/stator-circuit signal, not
  necessarily a dead alternator.

## Notable Excerpts

> "The alternator generates an AC output, which is converted to a DC output by a rectifier
> assembly internal to alternator; this DC output is then supplied to the vehicle through the
> B+ terminal."

## Captured Content

Full extracted text in `kb/.raw/alternator-description-and-operation-fsm.txt`.

Relates to truck inventory system `electrical-charging`.
