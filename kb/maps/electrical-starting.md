---
title: "Starting system"
kind: map
system_id: electrical-starting
tags:
  - electrical-starting
---

Battery, cables, relay, solenoid, starter, interlocks.

This map is the entry point for the **starting system** system of the truck. As notes are added
(via `kb-process`), link the load-bearing ones below.

## Key Notes

- [[notes/rly-icm-color-gray-vs-black-tells-you-the-dwell-strategy|A gray ICM controls its own dwell while a black ICM lets the SPOUT signal set dwell]]
- [[notes/chg-disarm-the-air-bag-before-battery-work-on-starting-and-charging|Disarm the air bag system and wait one minute before any battery, steering column, or wheel work]]  ·  _procedure_
- [[notes/chg-park-neutral-switch-both-closes-the-relay-and-lights-backup-lamps|On automatics, the park/neutral switch both closes the starter relay and lights the backup lamps]]
- [[notes/rly-spout-falling-edge-only-controls-coil-on-time-on-the-ccd-system|On the CCD (black ICM) system the SPOUT falling edge controls when the coil turns on]]
- [[notes/rly-eec-power-relay-feeds-the-fuel-pump-relay-coil|Power to the fuel pump relay comes from the EEC power relay through the PCM and the inertia switch]]
- [[notes/chg-starter-current-draw-specs-vary-by-starter-diameter|Starter current-draw specs vary by starter diameter]]  ·  _spec_
- [[notes/f150-uses-permanent-magnet-gear-reduction-starter|The 1994 F-150 uses a permanent-magnet gear-reduction starter]]
- [[notes/rly-icm-mounts-on-a-heatsink-with-dielectric-grease-and-two-torque-specs|The ICM mounts to a heatsink with dielectric grease and has two distinct screw torque specs]]  ·  _procedure_
- [[notes/rly-pcm-power-relay-supplies-bplus-and-gives-reverse-battery-protection|The PCM power relay supplies B+ to the PCM and protects it against reverse battery polarity]]
- [[notes/rly-alarm-module-disables-starting-and-flashes-lamps-at-80-cycles-per-minute|The alarm module disables the starting system and flashes the lamps at 80 cycles per minute when triggered]]
- [[notes/clutch-pedal-position-switch-is-the-start-interlock-on-manual-f150|The clutch pedal position switch is the start interlock on a manual F-150]]
- [[notes/rly-fuel-pump-relay-is-grounded-by-the-pcm-not-a-simple-switch|The fuel pump relay is grounded by the PCM, so its ground circuit is the real no-start clue]]
- [[notes/chg-starter-load-test-feeds-the-relay-s-terminal-from-a-remote-switch|The starter Load Test cranks the engine by feeding the relay S terminal from a remote switch]]  ·  _procedure_
- [[notes/chg-starter-no-load-test-finds-shorts-and-rubbing-armature|The starter No-Load test finds shorted windings and a rubbing armature by reading current draw]]  ·  _procedure_
- [[notes/chg-starter-solenoid-test-checks-continuity-s-to-m-and-s-to-ground|The starter solenoid test checks continuity from S to M and from S to ground]]  ·  _procedure_
- [[notes/chg-clutch-switch-is-an-in-series-interlock-to-the-starter-relay|The starting interlock switch sits in series between the start signal and the starter relay]]

## Common Issues

- [[notes/chg-disconnecting-the-battery-erases-the-pcm-adaptive-strategy|Disconnecting the battery erases the PCM adaptive strategy and may need 10+ miles to relearn]]  ·  _troubleshooting_

## Sources

- [[sources/chg-service-precautions|Starting and Charging — Service Precautions (FSM)]]
- [[sources/chg-starter-motor-bench-tests|Starter Motor — Bench and Load Tests (FSM)]]
- [[sources/chg-starter-motor-specifications|Starter Motor — Specifications (FSM)]]
- [[sources/chg-starting-interlock-switches|Starting Interlock Switches (Clutch / Neutral Safety) — Description and Operation (FSM)]]
- [[sources/rly-body-control-modules|Body Control Modules — Warning Chime, Alarm, Keyless Entry, Wiper, PSOM, Starter Relay (FSM)]]
- [[sources/rly-fuel-pump-relay|Fuel Pump Relay — Description, Operation and Testing (FSM)]]
- [[sources/rly-ignition-control-module|Ignition Control Module (ICM) — Description, Operation and Service (FSM)]]
- [[sources/rly-pcm-power-main-relay|Main Relay (Computer/Fuel System) / PCM Power Relay — Description and Operation (FSM)]]
- [[sources/starter-motor-description-and-operation-fsm|Starter Motor — Description and Operation (FSM)]]
