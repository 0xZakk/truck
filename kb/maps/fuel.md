---
title: "Fuel system"
kind: map
system_id: fuel
tags:
  - fuel
---

Tank, pump, lines, injection, EVAP.

This map is the entry point for the **fuel system** system of the truck. As notes are added
(via `kb-process`), link the load-bearing ones below.

## Key Notes

- [[notes/sen-narrow-1-shutter-gives-cylinder-identification|A narrower number-1 shutter creates a signature PIP pulse that tells the PCM which cylinder is which]]
- [[notes/eec-clear-kam-and-drive-10-miles-after-replacing-an-eec-part|After replacing an EEC component, clear Keep Alive Memory and drive ~10 miles to relearn]]  ·  _procedure_
- [[notes/sen-closed-loop-fuel-control-targets-14-7-1|Closed-loop fuel control on the 4.9L trims injector pulse width toward 14.7:1 using the HO2S feedback]]
- [[notes/eec-compression-is-acceptable-if-lowest-cylinder-is-within-25-percent|Compression is acceptable if the lowest cylinder reads within 25% of the highest]]  ·  _procedure_
- [[notes/dtc-111-is-system-pass-not-a-fault|DTC 111 means System Pass — the self-test found no faults]]
- [[notes/dtc-codes-may-be-shared-between-modules-so-confirm-the-source|DTC numbers may be shared between modules, so confirm which module a code came from before chasing it]]
- [[notes/eec-injector-fuel-quantity-is-governed-by-pulse-width|Injector fuel quantity is governed only by pulse width because lift and rail pressure are constant]]
- [[notes/eec-install-the-tps-clockwise-only-or-idle-runs-high|Install the TP sensor by rotating it clockwise only, or idle speed runs high]]  ·  _procedure_
- [[notes/dtc-rationality-codes-flag-readings-that-disagree-with-other-sensors|Rationality DTCs flag a sensor reading that disagrees with the rest of the engine picture rather than a broken circuit]]
- [[notes/1994-f150-49l-is-the-efi-300-variant|The 1994 F-150's 4.9L is the EFI 300 variant]]
- [[notes/dtc-self-test-runs-in-koeo-and-koer-modes|The EEC self-test runs in two modes — Key On Engine Off and Key On Engine Running — and each finds different faults]]
- [[notes/eec-ho2s-generates-voltage-from-exhaust-vs-atmosphere-oxygen-difference|The HO2S generates voltage from the oxygen difference between exhaust and atmosphere]]
- [[notes/eec-ho2s-must-exceed-600f-so-it-has-a-built-in-heater|The HO2S needs 600 deg F to work, so a built-in heater shortens warm-up before closed loop]]  ·  _spec_
- [[notes/sen-ho2s-must-reach-600f-and-uses-a-heater|The HO2S only reads accurately above 600°F, which is why it carries an internal heater]]
- [[notes/sen-ho2s-voltage-tells-pcm-rich-vs-lean|The HO2S reports rich vs. lean by generating a high voltage when exhaust oxygen is low and a low voltage when it is high]]
- [[notes/eec-iac-meters-air-around-the-throttle-plate-via-pcm-duty-cycle|The IAC valve sets idle by metering air around the throttle plate via a PCM-controlled duty cycle]]
- [[notes/sen-map-doubles-as-a-barometric-pressure-sensor|The MAP sensor doubles as a barometric pressure sensor to correct fueling for altitude]]
- [[notes/eec-map-sensor-outputs-a-frequency-and-doubles-as-a-baro-sensor|The MAP sensor outputs a frequency proportional to load and doubles as a barometric sensor]]
- [[notes/sen-pcm-reads-throttle-mode-and-rate-from-tps|The PCM derives idle, cruise, WOT, and acceleration-pump action from TP angle and its rate of change]]
- [[notes/eec-pcm-learns-an-adaptive-strategy-stored-in-kam|The PCM learns an adaptive strategy in Keep Alive Memory to compensate for component wear]]
- [[notes/sen-pip-is-a-hall-switch-driven-by-a-6-vane-shutter|The PIP signal is a 0–12 V square wave a distributor Hall switch makes as a camshaft-driven 6-vane shutter passes through it]]
- [[notes/eec-tps-is-a-potentiometer-reading-06v-closed-to-45v-wot|The TP sensor is a potentiometer reading about 0.6 V closed to 4.5 V at wide-open throttle]]
- [[notes/eec-regulator-references-manifold-vacuum-to-hold-a-constant-injector-pressure-drop|The fuel pressure regulator references manifold vacuum to hold a constant pressure drop across the injectors]]
- [[notes/eec-fuel-pump-runs-12s-at-key-on-then-needs-an-rpm-signal|The fuel pump runs 1-2 s at key-on, then the PCM keeps it running only with an rpm signal above 120]]
- [[notes/sen-inertia-switch-uses-a-magnet-held-ball|The inertia switch cuts fuel-pump power in a crash using a magnet-held ball that breaks loose on impact]]
- [[notes/unplugging-iac-while-idling-tests-the-idle-air-circuit|Unplugging the IAC while idling tests whether the idle-air circuit is involved]]  ·  _procedure_

## Common Issues

- [[notes/eec-ntc-temp-sensors-read-falsely-cold-with-bad-grounds|A bad ground or added resistance makes the NTC ECT and IAT read falsely cold, driving a needless rich condition]]  ·  _troubleshooting_
- [[notes/failed-throttle-body-gasket-causes-rough-idle-vacuum-leak|A failed throttle-body-to-manifold gasket is a known vacuum-leak cause of rough idle on the 4.9L]]  ·  _troubleshooting_
- [[notes/dtc-hard-codes-vs-memory-codes-mean-present-vs-stored|A hard code is a fault present during the test, while a memory code was stored from earlier driving]]  ·  _troubleshooting_
- [[notes/sen-tripped-inertia-switch-causes-crank-no-start|A tripped inertia switch is a common crank-no-start cause and must be manually reset]]  ·  _troubleshooting_
- [[notes/dtc-adaptive-fuel-limit-codes-mean-trims-ran-out-of-room|Adaptive-fuel-limit DTCs mean fuel trim hit its correction ceiling and the oxygen sensor can no longer keep the mixture balanced]]  ·  _troubleshooting_
- [[notes/dtc-511-and-513-call-for-pcm-replacement|DTCs 511 and 513 are internal PCM failures that the chart resolves by replacing the PCM]]  ·  _troubleshooting_
- [[notes/dtc-fuel-pump-codes-distinguish-relay-from-secondary-circuit|Fuel pump DTCs distinguish a relay primary-circuit fault from a pump secondary-circuit fault]]  ·  _troubleshooting_
- [[notes/sen-eec-iv-sensors-share-vref-and-sig-rtn|Most EEC-IV sensors share a common 5.0 V VREF and SIG RTN ground, so one bad reference skews many readings]]  ·  _troubleshooting_
- [[notes/eec-iac-is-part-of-adaptive-strategy-and-surges-at-its-limits|The IAC is part of adaptive strategy and surges when it reaches its learning limits]]  ·  _troubleshooting_
- [[notes/eec-pcm-cross-checks-tps-map-and-pulse-width-for-in-range-failures|The PCM cross-checks TP, MAP, and injector pulse width to catch in-range sensor failures]]  ·  _troubleshooting_
- [[notes/dtc-vcrm-codes-report-over-current-and-open-faults-on-high-load-outputs|VCRM DTCs report over-current and open-circuit faults on the high-current loads the relay module manages]]  ·  _troubleshooting_

## Sources

- [[sources/dtc-actuator-pcm-codes|EEC DTCs 542-593 — Fuel Pump, Output Actuator, and VCRM Codes (FSM)]]
- [[sources/dtc-air-fuel-sensor-codes|EEC DTCs 112-195 — Air, Fuel, and Sensor Input Codes (FSM)]]
- [[sources/dtc-idle-speed-input-codes|EEC DTCs 411-539 — Idle Speed, Vehicle Speed, and Switch Input Codes (FSM)]]
- [[sources/dtc-self-test-overview|EEC Diagnostic Trouble Codes — Self-Test Overview and Code Conventions (FSM)]]
- [[sources/eec-engine-control-module|Engine Control Module (PCM / EEC-IV) — Description, Operation, and Reset (FSM)]]
- [[sources/eec-fuel-pressure-regulator-and-pump-control|Fuel Delivery — Injectors, Pressure Regulator, and Pump Control (FSM)]]
- [[sources/eec-idle-air-control-valve|Idle Air Control (IAC) Valve — Operation, DTCs, Service, and Specs (FSM)]]
- [[sources/eec-map-sensor|Manifold Absolute Pressure (MAP) Sensor — Operation, DTCs, and Range (FSM)]]
- [[sources/eec-oxygen-sensor|Heated Oxygen Sensor (HO2S) — EEC-IV Description, Operation, and Specs (FSM)]]
- [[sources/eec-temperature-sensors-ect-iat|ECT and IAT Temperature Sensors — Operation, DTCs, and Specs (FSM)]]
- [[sources/eec-throttle-position-sensor|Throttle Position Sensor (TP) — Operation, DTCs, Service, and Specs (FSM)]]
- [[sources/eec-tune-up-and-engine-checks|Tune-up and Engine Performance Checks — Timing, Firing Order, Compression, Valve Clearance, Spark Plugs (FSM)]]
- [[sources/ford-300-inline-six-bulletproof-engine|Ford 300 Inline Six — What You Need to Know About Ford's Bulletproof Engine (4.9L)]]
- [[sources/rough-idle-94-f-150-49l-ford-truck-enthusiasts-forums|Rough idle — '94 F-150 4.9L (Ford Truck Enthusiasts)]]
- [[sources/sen-distributor-hall-effect-pip-cmp-sensor|Distributor Hall-Effect Sensor — PIP, Camshaft Position, and Cylinder Identification (FSM)]]
- [[sources/sen-inertia-fuel-shutoff-switch|Inertia Fuel Shutoff (IFS) Switch — Description and Operation (FSM)]]
- [[sources/sen-manifold-absolute-pressure-sensor|Manifold Absolute Pressure (MAP) Sensor — Description, Operation, and DTCs (FSM)]]
- [[sources/sen-oxygen-sensor|Heated Oxygen Sensor (HO2S) — Description, Operation, and Testing (FSM)]]
- [[sources/sen-throttle-position-sensor|Throttle Position (TP) Sensor — Description, Operation, and DTCs (FSM)]]
