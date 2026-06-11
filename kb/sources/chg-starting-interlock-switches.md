---
title: "Starting Interlock Switches (Clutch / Neutral Safety) — Description and Operation (FSM)"
source: manuals/factory-service-manual/1994 Ford F 150 2WD Pickup L6-300 4.9L/Repair%20and%20Diagnosis/Starting%20and%20Charging/Starting%20System/Clutch%20Switch/Description%20and%20Operation/index.html
type: local
date: 2026-06-11
author: "Ford Factory Service Manual"
tags:
  - starting-system
  - clutch-switch
  - neutral-safety-switch
  - how-it-works
  - electrical
processed: true
---

## Summary

The 1994 F-150's starting circuit includes an interlock switch that decides whether the
ignition switch's start signal is allowed to reach the starter relay. The factory service
manual documents two interlock types depending on the truck: the **clutch pedal position
switch** on manual transmissions, and the **manual lever position sensor / park-neutral
position switch** on automatics. The interlock's job is to keep the engine from starting
unless the truck is in a safe state.

On the manual (M5OD) truck, pressing the clutch pedal closes the clutch switch and passes
voltage through to the starter relay — so the engine will not crank with the clutch
engaged. On automatics, the park/neutral switch (C6) or manual lever position sensor
(4R70W/E4OD) closes only in PARK or NEUTRAL to energize the relay, and also routes current
to the backup lamps in REVERSE.

## Key Points

- **Clutch switch (manual):** purpose is to prevent engine startup with the clutch engaged.
  Depressing the clutch pedal closes the clutch pedal position switch, directing voltage and
  current to the **starter relay**.
- **Park/Neutral switch (C6 automatic):** in PARK or NEUTRAL it directs current to close the
  starter motor relay; in REVERSE it directs current to illuminate the backup lamps.
- **Manual lever position sensor (4R70W/E4OD automatic):** same logic — closes the starter
  relay in PARK/NEUTRAL, lights the backup lamps in REVERSE.
- All three are series elements between the ignition switch's start signal and the starter
  relay, so a failed interlock causes a no-crank.

## Notable Excerpts

> "Prevents engine startup with clutch engaged. … Depressing the clutch pedal closes the
> clutch pedal position switch, directing voltage and current to the starter relay."

> "With the transmission in 'PARK' or 'NEUTRAL' the park/neutral position switch directs
> current to close the starter motor relay."

Relates to truck inventory system `electrical-starting`.

Source: manuals/factory-service-manual/1994 Ford F 150 2WD Pickup L6-300 4.9L/Repair%20and%20Diagnosis/Starting%20and%20Charging/Starting%20System/ (Clutch Switch and Neutral Safety Switch, Description and Operation)
