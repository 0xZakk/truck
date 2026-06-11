---
title: "The 600-series and 998 DTCs apply only to the E4OD automatic, not the standard M5OD manual"
kind: concept
source: "[[sources/dtc-transmission-codes|EEC DTCs 617-998 — E4OD Transmission Codes (FSM)]]"
related:
  - "[[notes/dtc-temperature-sensor-codes-pair-low-and-high-voltage|Temperature sensor DTCs come in low/high pairs that mean shorted (254°F) or open (-40°F)]]"
  - "[[notes/dtc-codes-may-be-shared-between-modules-so-confirm-the-source|DTC numbers may be shared between modules, so confirm which module a code came from before chasing it]]"
tags:
  - dtc
  - transmission
  - e4od
  - shift-solenoid
  - troubleshooting
---

The 600-series codes (and 998) all belong to the electronically controlled E4OD automatic
transmission, whose shift solenoids, pressure control, torque-converter clutch, and sensors
are driven by the same PCM and read out through the same EEC self-test. On a 4.9L F-150 the
M5OD-R2 five-speed manual is the standard gearbox, so a correctly-equipped manual truck should
never produce these codes — seeing one means either the truck has the E4OD or a code is being
misread from another module.

The codes group cleanly: shift-solenoid circuit faults (566, 621/SS1, 622/SS2, 641/SS3), shift
errors and gear-ratio faults (617-619, 645-648), electronic pressure control and
torque-converter-clutch codes (624/625/649/651 and 627/629/643/652/656), transmission range
sensor codes (634/654/667/668/675), and the fluid-temperature codes 637 (open, -40°F
indicated) and 638 (shorted, 290°F indicated). The fluid-temp pair follows the same
shorted-reads-hot / open-reads-cold thermistor logic as the engine coolant and intake air
sensors.

For this truck's `engine`-managed driveline, these codes are only in scope if the automatic is
fitted; otherwise they are a strong hint that the code came from the wrong module.

## Related Concepts

- [[notes/dtc-temperature-sensor-codes-pair-low-and-high-voltage|Temperature sensor DTCs come in low/high pairs that mean shorted (254°F) or open (-40°F)]]
- [[notes/dtc-codes-may-be-shared-between-modules-so-confirm-the-source|DTC numbers may be shared between modules, so confirm which module a code came from before chasing it]]

## Source

- [[sources/dtc-transmission-codes|EEC DTCs 617-998 — E4OD Transmission Codes (FSM)]]
