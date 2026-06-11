---
title: "Interior"
kind: map
system_id: interior
tags:
  - interior
---

Seats, dash, trim panels, carpet, console.

This map is the entry point for the **interior** system of the truck. As notes are added
(via `kb-process`), link the load-bearing ones below.

## Key Notes

- [[notes/acc-door-disarm-switch-grounds-the-controller-when-the-door-is-key-unlocked|A door disarm switch grounds the controller when its door is unlocked with the key, disabling the anti-theft system]]
- [[notes/ipc-voltmeter-normal-range-is-13-5-to-14-volts|A normal voltmeter reading on the F-150 is 13.5 to 14.0 volts]]  ·  _spec_
- [[notes/rst-seat-belt-anchor-bolts-torque-to-22-30-ft-lb|All seat belt and anchor bolts torque to 30-40 Nm (22-30 ft lbs)]]  ·  _spec_
- [[notes/rst-two-sensors-must-close-together-to-deploy-the-air-bag|At least two sensors — one primary plus the safing sensor — must close together to deploy the air bag]]
- [[notes/rst-use-the-2-ohm-air-bag-simulator-not-a-zero-ohm-jumper|Diagnose the SRS with a 2-ohm air bag simulator, never a zero-ohm jumper]]  ·  _procedure_
- [[notes/rst-tethered-child-seats-belong-in-a-rear-position|Ford places tethered child safety seats in a rear position, front only as a last resort]]
- [[notes/ipc-instrument-panel-fastener-torque-values|Instrument-panel mounting fasteners torque to between 12 and 53 in-lbs depending on location]]  ·  _spec_
- [[notes/ipc-magnetic-gauges-need-tester-021-00055|Magnetic dash gauges are diagnosed with tester tool 021-00055 and per-symptom pinpoint tests]]  ·  _procedure_
- [[notes/ipc-reprogram-the-psom-conversion-constant-when-tire-size-changes|Reprogram the PSOM conversion constant whenever tire size changes]]  ·  _procedure_
- [[notes/rst-srs-fastener-torque-values|SRS fastener torque values for the air bag module, sliding contact, and crash sensors]]  ·  _spec_
- [[notes/rst-test-retractor-lock-with-a-5-mph-max-brake-stop|Test a belt retractor's lock with a 5 mph maximum-brake stop, then retry at 15 mph]]  ·  _procedure_
- [[notes/ipc-speedometer-is-electronic-psom-fed-by-the-abs-sensor|The 1994 F-150 speedometer is an electronic PSOM fed by the ABS/differential speed sensor, not a cable]]
- [[notes/ipc-check-engine-message-signals-eec-iv-fmem-mode|The CHECK ENGINE message signals the EEC-IV has entered a backup (FMEM) operating strategy]]
- [[notes/rst-backup-power-supply-depletes-one-minute-after-disconnect|The SRS backup power supply depletes about one minute after the positive cable is disconnected]]
- [[notes/rst-srs-supplements-belts-and-runs-from-battery-in-any-key-position|The air bag SRS supplements the belts and runs straight from the battery in any key position]]
- [[notes/rst-air-bag-deploys-in-four-steps-in-a-fraction-of-a-second|The air bag deploys in four steps in a fraction of a second]]
- [[notes/rly-air-bag-monitor-diagnoses-but-does-not-deploy-the-air-bag|The air bag diagnostic monitor only diagnoses the SRS; hard-wired sensors deploy the air bag]]
- [[notes/rst-sliding-contact-relays-srs-signals-through-the-rotating-wheel|The air bag sliding contact (clockspring) relays SRS signals through the rotating steering wheel]]
- [[notes/ipc-charge-lamp-grounds-through-regulator-terminal-1|The charge lamp lights because the regulator grounds it through terminal 1 until the S-circuit voltage is reached]]
- [[notes/rst-continuous-loop-retractor-locks-at-5-mph|The continuous-loop belt retractor lets webbing move freely but locks at impacts of 5 mph or more]]
- [[notes/rst-thermal-fuse-disables-deployment-and-must-not-be-jumpered|The diagnostic monitor's thermal fuse disables deployment and must never be jumpered]]
- [[notes/rst-driver-air-bag-fills-to-2-3-cu-ft-in-about-40-ms|The driver air bag is a 28-inch neoprene-coated nylon bag that fills to 2.3 cu ft in about 40 milliseconds]]  ·  _spec_
- [[notes/rst-air-bag-module-is-serviced-only-as-a-complete-assembly|The driver air bag module is serviced only as a complete assembly]]
- [[notes/acc-factory-radio-pulls-with-din-tool-after-depressing-one-inch|The factory radio is released with DIN removal tool T87P-19061-A pushed in about one inch, not by unscrewing]]  ·  _procedure_
- [[notes/ipc-fuel-sender-resistance-spans-22-5-to-145-ohms|The fuel sender resistance spans 22.5 ohms empty to 145 ohms full]]  ·  _spec_
- [[notes/ipc-seat-belt-reminder-runs-4-to-8-seconds-at-key-on|The seat belt reminder lamp runs for 4 to 8 seconds at key-on regardless of belt state]]
- [[notes/ipc-dash-gauges-share-a-three-coil-magnetic-movement|The temperature, oil pressure, and fuel gauges all use the same three-coil magnetic movement with no voltage regulator]]
- [[notes/rly-warning-chime-module-sounds-for-key-in-lights-on-and-unbuckled-belt|The warning chime module sounds for key-in-ignition, lights-on-with-door-open, and unbuckled belt]]

## Common Issues

- [[notes/rst-five-sets-of-five-beeps-means-a-dead-indicator-not-code-55|Five sets of five beeps means a dead air bag indicator with a fault present, not code 55]]  ·  _troubleshooting_
- [[notes/rst-replace-belts-after-any-collision-including-unused-ones|Inspect and replace belt assemblies after any collision, including belts not in use]]  ·  _troubleshooting_
- [[notes/rst-undamaged-srs-sensors-reset-and-can-be-reused|Undamaged SRS sensors reset automatically after a crash and can be reused]]  ·  _troubleshooting_

## Sources

- [[sources/acc-anti-theft-alarm-system|Anti-Theft / Alarm System — Alarm Module and Arm/Disarm Switch (FSM)]]
- [[sources/acc-radio-stereo-removal|Radio / Stereo — Removal and Installation (FSM)]]
- [[sources/ipc-charge-lamp-indicator|Charge Lamp / Indicator — Description, Operation and Testing (FSM)]]
- [[sources/ipc-fuel-gauge-and-sender|Fuel Gauge and Fuel Gauge Sender — Description, Operation and Testing (FSM)]]
- [[sources/ipc-magnetic-gauge-movement|Magnetic Gauge Movement / Instrument Cluster — Description, Operation and Specifications (FSM)]]
- [[sources/ipc-malfunction-indicator-lamp|Malfunction Indicator Lamp (Check Engine) — Description and Operation (FSM)]]
- [[sources/ipc-oil-pressure-gauge|Oil Pressure Gauge — Description, Operation and Testing (FSM)]]
- [[sources/ipc-seat-belt-and-audible-warning|Seat Belt Reminder and Audible Warning (Chime) Module — Description and Operation (FSM)]]
- [[sources/ipc-speedometer-psom|Speedometer / Programmable Speedometer-Odometer Module (PSOM) — Description and Operation (FSM)]]
- [[sources/ipc-voltmeter-gauge|Voltmeter Gauge — Description and Operation (FSM)]]
- [[sources/rly-air-bag-diagnostic-monitor|Air Bag Control Module (Air Bag Diagnostic Monitor) — Description and Testing (FSM)]]
- [[sources/rly-body-control-modules|Body Control Modules — Warning Chime, Alarm, Keyless Entry, Wiper, PSOM, Starter Relay (FSM)]]
- [[sources/rst-air-bag-diagnostic-monitor|Air Bag Diagnostic Monitor and Trouble Codes — Description, Operation, and Diagnostics (FSM)]]
- [[sources/rst-air-bag-impact-and-safing-sensors|Air Bag Impact (Crash) Sensors and Safing Sensor — Description, Operation, Specs (FSM)]]
- [[sources/rst-driver-air-bag-module-and-sliding-contact|Driver Air Bag Module, Inflator, and Air Bag Sliding Contact (Clockspring) — Description, Operation, Specs (FSM)]]
- [[sources/rst-seat-belt-system|Seat Belt System — Description, Operation, Testing, and Specs (FSM)]]
- [[sources/rst-supplemental-air-bag-restraint-system|Supplemental Air Bag Restraint System (SRS) — Description and Operation (FSM)]]
