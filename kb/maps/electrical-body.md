---
title: "Body electrical & lighting"
kind: map
system_id: electrical-body
tags:
  - electrical-body
---

Harnesses, fuses, lamps, switches, gauges.

This map is the entry point for the **body electrical & lighting** system of the truck. As notes are added
(via `kb-process`), link the load-bearing ones below.

## Key Notes

- [[notes/acc-door-disarm-switch-grounds-the-controller-when-the-door-is-key-unlocked|A door disarm switch grounds the controller when its door is unlocked with the key, disabling the anti-theft system]]
- [[notes/wpr-wiper-motor-current-draw-under-3-5-amps|A healthy wiper motor draws no more than 3.5 amps at either low or high speed]]  ·  _spec_
- [[notes/ipc-voltmeter-normal-range-is-13-5-to-14-volts|A normal voltmeter reading on the F-150 is 13.5 to 14.0 volts]]  ·  _spec_
- [[notes/wpr-circuit-breaker-needs-two-bench-tests-to-pass|A wiper circuit breaker passes only if it survives the rated-hold test and trips within 20 seconds at double current]]  ·  _procedure_
- [[notes/crz-vacuum-vent-valve-plunger-shows-0-050-inch-or-less|Adjust the cruise vacuum vent valve so 0.050 inch or less of plunger shows with the pedal released]]  ·  _spec_
- [[notes/crz-diagnose-cruise-with-a-visual-check-first|Cruise control diagnosis starts with a visual check, and ABS must be healthy first]]  ·  _procedure_
- [[notes/crz-cruise-has-multiple-independent-deactivation-paths|Cruise control has several independent deactivation paths so braking always disengages it]]
- [[notes/crz-speed-control-holds-throttle-with-an-electronic-servo-and-cable|Cruise control holds speed with an electronic servo that pulls the throttle through an actuator cable]]
- [[notes/crz-speed-reference-comes-from-the-psom-or-vss|Cruise control regulates against the speed signal from the PSOM or VSS]]
- [[notes/wpr-disarm-the-air-bag-before-working-on-the-column-switch|Disarm the air bag before removing the column-mounted wiper/washer switch]]  ·  _procedure_
- [[notes/crz-disarm-the-air-bag-before-working-on-the-cruise-switches|Disarm the air bag before servicing the steering-wheel cruise switches]]  ·  _procedure_
- [[notes/ipc-functional-test-of-the-oil-level-warning-by-draining-two-quarts|Functional-test the oil level warning by draining two quarts and waiting five minutes]]  ·  _procedure_
- [[notes/lgt-headlamp-bulbs-9004-and-9007-look-alike-but-are-not-interchangeable|Headlamp bulbs No. 9004 and No. 9007 look alike but are not interchangeable]]  ·  _spec_
- [[notes/ipc-instrument-panel-fastener-torque-values|Instrument-panel mounting fasteners torque to between 12 and 53 in-lbs depending on location]]  ·  _spec_
- [[notes/ipc-magnetic-gauges-need-tester-021-00055|Magnetic dash gauges are diagnosed with tester tool 021-00055 and per-symptom pinpoint tests]]  ·  _procedure_
- [[notes/crz-clutch-switch-deactivates-cruise-when-pedal-depressed|On manual trucks the clutch switch deactivates cruise the moment the pedal is depressed]]
- [[notes/rly-pcm-retainer-and-connector-torque-specs|PCM retainer screw and connector bolt have specific in-lb torque values]]  ·  _spec_
- [[notes/rly-eec-power-relay-feeds-the-fuel-pump-relay-coil|Power to the fuel pump relay comes from the EEC power relay through the PCM and the inertia switch]]
- [[notes/wpr-wiper-motor-and-linkage-live-under-the-cowl-grille|Reaching the wiper motor, pivots, or linkage means removing the cowl grille first]]  ·  _procedure_
- [[notes/ipc-reprogram-the-psom-conversion-constant-when-tire-size-changes|Reprogram the PSOM conversion constant whenever tire size changes]]  ·  _procedure_
- [[notes/ipc-speedometer-is-electronic-psom-fed-by-the-abs-sensor|The 1994 F-150 speedometer is an electronic PSOM fed by the ABS/differential speed sensor, not a cable]]
- [[notes/ipc-check-engine-message-signals-eec-iv-fmem-mode|The CHECK ENGINE message signals the EEC-IV has entered a backup (FMEM) operating strategy]]
- [[notes/ipc-oil-level-warning-is-separate-from-oil-pressure-warning|The Check Oil low-level warning is a separate system from the oil pressure warning lamp]]
- [[notes/rly-drl-module-runs-high-beams-at-reduced-intensity-with-a-brake-fluid-diode|The DRL module pulses the high beams at reduced intensity and uses a diode so low brake fluid cannot disable it]]
- [[notes/lgt-drl-module-runs-high-beams-dimly-only-with-park-brake-off|The DRL module runs the high beams dimly only with ignition in RUN, park brake off, and headlamps off]]
- [[notes/rly-pcm-power-relay-uses-a-separate-external-diode-not-an-internal-one|The PCM power relay is an SPDT relay with no internal diode and relies on a separate external diode]]  ·  _spec_
- [[notes/rly-pcm-power-relay-supplies-bplus-and-gives-reverse-battery-protection|The PCM power relay supplies B+ to the PCM and protects it against reverse battery polarity]]
- [[notes/rly-pcm-calibration-assembly-is-integral-and-not-replaceable|The PCM's calibration assembly is matched to vehicle weight, axle ratio, and transmission and is not replaceable]]
- [[notes/rly-psom-converts-the-abs-speed-sensor-signal-to-8000-pulses-per-mile|The PSOM converts the ABS differential speed sensor input to a standard 8000 pulses-per-mile signal]]
- [[notes/rly-wot-ac-relay-cuts-the-compressor-at-wide-open-throttle|The WOT A/C relay drops the compressor at wide open throttle to free up power]]
- [[notes/rly-air-bag-monitor-diagnoses-but-does-not-deploy-the-air-bag|The air bag diagnostic monitor only diagnoses the SRS; hard-wired sensors deploy the air bag]]
- [[notes/rly-alarm-module-disables-starting-and-flashes-lamps-at-80-cycles-per-minute|The alarm module disables the starting system and flashes the lamps at 80 cycles per minute when triggered]]
- [[notes/acc-anti-theft-module-monitors-switches-and-flashes-lamps-at-80-cpm|The anti-theft controller module monitors vehicle switches and, when triggered, sounds the horn and flashes the lamps at 80 cycles per minute]]
- [[notes/lgt-brake-light-switch-feeds-pcm-cruise-shift-lock-and-abs|The brake light switch feeds the PCM, cruise control, shift lock and ABS, not just the stop lamps]]
- [[notes/crz-brake-pressure-switch-opens-at-5-to-10-pounds|The brake pressure switch is a redundant deactivator that opens at 5-10 lbs of pedal pressure]]  ·  _spec_
- [[notes/ipc-charge-lamp-grounds-through-regulator-terminal-1|The charge lamp lights because the regulator grounds it through terminal 1 until the S-circuit voltage is reached]]
- [[notes/ipc-chime-module-handles-key-in-ignition-lamps-on-and-belt-reminders|The chime module drives key-in-ignition, lamps-on, and seat-belt reminders from separate inputs]]
- [[notes/lgt-multifunction-switch-removal-and-screw-torque|The column multi-function switch comes off after the shroud and torques to 18-27 inch-lbs]]  ·  _procedure_
- [[notes/lgt-headlamp-assembly-fastener-torque-and-removal|The composite headlamp assembly is freed by backing the horizontal aim screw fully out]]  ·  _procedure_
- [[notes/lgt-courtesy-lamp-pillar-switch-uses-three-rotating-locking-tabs|The courtesy/dome lamp pillar switch retains to the wiring with three tabs you can rotate to when one breaks]]  ·  _procedure_
- [[notes/crz-servo-cable-needs-0-04-inch-of-slack|The cruise actuator cable must be left with 0.04 inch of slack, never pulled tight]]  ·  _procedure_
- [[notes/wpr-interval-first-wipe-can-lag-up-to-12-seconds|The first interval wipe can lag up to 12 seconds, which is normal]]
- [[notes/rly-fuel-pump-relay-is-grounded-by-the-pcm-not-a-simple-switch|The fuel pump relay is grounded by the PCM, so its ground circuit is the real no-start clue]]
- [[notes/ipc-fuel-sender-resistance-spans-22-5-to-145-ohms|The fuel sender resistance spans 22.5 ohms empty to 145 ohms full]]  ·  _spec_
- [[notes/lgt-halogen-headlamp-bulb-must-be-handled-only-by-its-plastic-base|The halogen headlamp bulb is pressurized and must be handled only by its plastic base]]  ·  _procedure_
- [[notes/wpr-multi-function-switch-screws-torque-to-18-27-inch-lbs|The multi-function switch attaching screws torque to 18–27 inch-lbs]]  ·  _spec_
- [[notes/ipc-oil-level-module-has-a-five-minute-reset-delay|The oil level module waits about five minutes after key-off to allow oil drain-back before re-reading]]
- [[notes/ipc-oil-pressure-lamp-is-ground-switched-by-the-engine-unit|The oil pressure warning lamp is ground-switched by an engine-mounted pressure switch]]
- [[notes/wpr-park-test-confirms-the-motor-stops-in-park|The park test confirms the wiper motor cycles once and stops in the Park position]]  ·  _procedure_
- [[notes/ipc-seat-belt-reminder-runs-4-to-8-seconds-at-key-on|The seat belt reminder lamp runs for 4 to 8 seconds at key-on regardless of belt state]]
- [[notes/crz-control-switch-sends-set-coast-accel-resume-to-amplifier|The steering-wheel speed control switch tells the amplifier to set, hold, coast, or accelerate]]
- [[notes/ipc-dash-gauges-share-a-three-coil-magnetic-movement|The temperature, oil pressure, and fuel gauges all use the same three-coil magnetic movement with no voltage regulator]]
- [[notes/lgt-turn-signal-flasher-lives-on-the-front-of-the-fuse-panel|The turn signal flasher is a separate plug-in on the front of the fuse panel]]  ·  _spec_
- [[notes/rly-warning-chime-module-sounds-for-key-in-lights-on-and-unbuckled-belt|The warning chime module sounds for key-in-ignition, lights-on-with-door-open, and unbuckled belt]]
- [[notes/wpr-washer-pump-current-draw-window-is-1-7-to-4-amps|The washer pump must draw between 1.7 and 4 amps while pumping]]  ·  _spec_
- [[notes/wpr-wiper-control-module-drives-all-wiper-modes|The wiper control module, not the switch, drives all wiper and washer modes from switch signals]]
- [[notes/wpr-wiper-and-washer-switch-are-one-multi-function-switch|The wiper switch and washer switch are a single multi-function switch on the steering column]]
- [[notes/wpr-wiper-circuit-breaker-is-rated-8-25-amps|The wiper/washer system is protected by an 8.25-amp circuit breaker in the fuse junction panel]]  ·  _spec_
- [[notes/lgt-turn-signal-hazard-and-dimmer-are-one-multifunction-switch|Turn signal, hazard and high/low dimmer are all one steering-column multi-function switch]]
- [[notes/sen-vehicle-speed-flows-through-the-psom|Vehicle speed reaches the PCM through the PSOM, which converts the axle sensor signal to 8000 pulses per mile]]
- [[notes/lgt-backup-lamp-source-depends-on-the-transmission|What powers the backup lamps depends on which transmission the truck has]]

## Common Issues

- [[notes/lgt-a-failed-brake-light-switch-can-disable-cruise-and-torque-converter-unlock|A failed brake light switch shows up as cruise or torque-converter symptoms, not just dark stop lamps]]  ·  _troubleshooting_
- [[notes/ipc-charge-lamp-jumper-test-from-terminal-1-to-battery-negative|A jumper from regulator terminal 1 to battery negative proves the charge lamp bulb and circuit]]  ·  _troubleshooting_
- [[notes/crz-cruise-pinpoint-tests-are-organized-by-symptom-letter|Cruise control pinpoint tests are organized by lettered symptom from A through K]]  ·  _troubleshooting_
- [[notes/ipc-grounding-the-oil-lamp-wire-isolates-bulb-from-sender|Grounding the oil-lamp sender wire isolates a bad bulb from a bad pressure switch]]  ·  _troubleshooting_
- [[notes/lgt-on-automatics-the-range-switch-shares-backup-lamps-and-starter-relay|On automatics the same range switch lights the backup lamps and closes the starter relay]]  ·  _troubleshooting_
- [[notes/sen-clutch-switch-is-the-manual-start-interlock|On the manual F-150 the clutch pedal switch is the start interlock and feeds the starter relay only when the pedal is down]]  ·  _troubleshooting_
- [[notes/crz-servo-test-is-a-connector-and-wiring-inspection|Testing the cruise servo is mostly a connector-pin and broken-wire inspection]]  ·  _troubleshooting_
- [[notes/rly-air-bag-monitor-flashes-two-digit-codes-and-beeps-if-the-lamp-is-dead|The air bag monitor flashes two-digit trouble codes on the indicator, or beeps five sets of five if the lamp is dead]]  ·  _troubleshooting_
- [[notes/acc-anti-theft-disables-the-starting-system-until-disarmed|The anti-theft system disables the starting system until it is disarmed]]  ·  _troubleshooting_
- [[notes/wpr-wiper-motor-magnets-can-shatter-from-physical-shock|The wiper motor's ceramic magnets can shatter from a physical shock and kill the motor]]  ·  _troubleshooting_

## Sources

- [[sources/acc-anti-theft-alarm-system|Anti-Theft / Alarm System — Alarm Module and Arm/Disarm Switch (FSM)]]
- [[sources/crz-brake-deactivation-switches|Cruise Control Brake Switches — Brake On/Off Switch and Brake Pressure (Deactivator) Switch (FSM)]]
- [[sources/crz-control-switch-and-clutch-switch|Speed Control Switch and Clutch Switch — Description and Operation (FSM)]]
- [[sources/crz-diagnosis-and-vacuum-vent-valve|Cruise Control Diagnosis Overview and Vacuum Vent (Dump) Valve Adjustment (FSM)]]
- [[sources/crz-speed-control-servo-and-cable|Speed Control Servo and Actuator Cable — Description, Testing, Adjustment (FSM)]]
- [[sources/crz-speed-control-system-overview|Cruise Control (Speed Control) System — Description, Operation, Service Precautions (FSM)]]
- [[sources/ipc-charge-lamp-indicator|Charge Lamp / Indicator — Description, Operation and Testing (FSM)]]
- [[sources/ipc-fuel-gauge-and-sender|Fuel Gauge and Fuel Gauge Sender — Description, Operation and Testing (FSM)]]
- [[sources/ipc-magnetic-gauge-movement|Magnetic Gauge Movement / Instrument Cluster — Description, Operation and Specifications (FSM)]]
- [[sources/ipc-malfunction-indicator-lamp|Malfunction Indicator Lamp (Check Engine) — Description and Operation (FSM)]]
- [[sources/ipc-oil-level-warning-indicator|Oil Level Warning Indicator — Description, Operation and Testing (FSM)]]
- [[sources/ipc-oil-pressure-gauge|Oil Pressure Gauge — Description, Operation and Testing (FSM)]]
- [[sources/ipc-oil-pressure-warning-lamp|Oil Pressure Warning Lamp / Indicator — Testing and Inspection (FSM)]]
- [[sources/ipc-seat-belt-and-audible-warning|Seat Belt Reminder and Audible Warning (Chime) Module — Description and Operation (FSM)]]
- [[sources/ipc-speedometer-psom|Speedometer / Programmable Speedometer-Odometer Module (PSOM) — Description and Operation (FSM)]]
- [[sources/ipc-voltmeter-gauge|Voltmeter Gauge — Description and Operation (FSM)]]
- [[sources/lgt-backup-lamp-switch|Backup Lamp Switch / Park-Neutral Position Switch by Transmission (FSM)]]
- [[sources/lgt-brake-light-switch|Brake (Stop) Light Switch — Description and Service (FSM)]]
- [[sources/lgt-daytime-running-lamp|Daytime Running Lamp (DRL) Control Unit — Description and Operation (FSM)]]
- [[sources/lgt-headlamp|Headlamp, Headlamp Bulb, Headlamp Switch and Dimmer Switch (FSM)]]
- [[sources/lgt-interior-lamp-switch|Interior / Courtesy / Dome Lamp Pillar Switch — Service and Repair (FSM)]]
- [[sources/lgt-multifunction-switch|Steering-Column Multi-Function Switch — Turn Signal, Hazard and Dimmer (FSM)]]
- [[sources/rly-air-bag-diagnostic-monitor|Air Bag Control Module (Air Bag Diagnostic Monitor) — Description and Testing (FSM)]]
- [[sources/rly-body-control-modules|Body Control Modules — Warning Chime, Alarm, Keyless Entry, Wiper, PSOM, Starter Relay (FSM)]]
- [[sources/rly-daytime-running-lamp-module|Daytime Running Lamp (DRL) Control Unit — Description and Operation (FSM)]]
- [[sources/rly-fuel-pump-relay|Fuel Pump Relay — Description, Operation and Testing (FSM)]]
- [[sources/rly-pcm-power-main-relay|Main Relay (Computer/Fuel System) / PCM Power Relay — Description and Operation (FSM)]]
- [[sources/rly-powertrain-control-module|Powertrain Control Module (PCM/ECM) — Description, Reset, Service and Specs (FSM)]]
- [[sources/rly-wot-ac-compressor-clutch-relay|Compressor Clutch Relay (WOT A/C Relay) — Description and Operation (FSM)]]
- [[sources/sen-clutch-pedal-position-switch|Clutch Pedal Position Switch (Manual Transmission Start Interlock) — Description and Operation (FSM)]]
- [[sources/sen-vehicle-speed-sensor|Vehicle Speed Sensor / PSOM and Differential Speed Sensor — Description and Operation (FSM)]]
- [[sources/wpr-circuit-breaker|Wiper Circuit Breaker — Rating and Two-Part Test (FSM)]]
- [[sources/wpr-diagnostics-and-precautions|Wiper/Washer Diagnostics, Park Test, and Air Bag Service Precautions (FSM)]]
- [[sources/wpr-multi-function-switch|Wiper/Washer Multi-Function Switch — Service and Testing (FSM)]]
- [[sources/wpr-washer-pump|Windshield Washer Pump — Current Draw Test (FSM)]]
- [[sources/wpr-wiper-arm-and-linkage|Wiper Arm, Pivot, and Linkage — Removal and Installation (FSM)]]
- [[sources/wpr-wiper-control-module|Wiper Control Module and Interval Wipe Operation (FSM)]]
- [[sources/wpr-wiper-motor|Wiper Motor — Testing, Service, and Upgraded Kits (FSM)]]
