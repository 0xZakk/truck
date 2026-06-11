---
title: "Rationality DTCs flag a sensor reading that disagrees with the rest of the engine picture rather than a broken circuit"
kind: concept
source: "[[sources/dtc-air-fuel-sensor-codes|EEC DTCs 112-195 — Air, Fuel, and Sensor Input Codes (FSM)]]"
related:
  - "[[notes/dtc-temperature-sensor-codes-pair-low-and-high-voltage|Temperature sensor DTCs come in low/high pairs that mean shorted (254°F) or open (-40°F)]]"
  - "[[notes/dtc-adaptive-fuel-limit-codes-mean-trims-ran-out-of-room|Adaptive-fuel-limit DTCs mean fuel trim hit its correction ceiling and the oxygen sensor can no longer keep the mixture balanced]]"
tags:
  - dtc
  - throttle-position
  - mass-air-flow
  - engine
  - fuel
---

Beyond the simple "circuit too high / too low" codes, the EEC sets a second class of codes
when a sensor's voltage is electrically valid but **inconsistent with what the other sensors
say**. The FSM phrases these as "higher or lower than expected." DTC 121, for example, is
closed-throttle voltage higher or lower than expected, explicitly described as "throttle
position voltage inconsistent with the mass air flow sensor" — the TP and MAF signals
disagree about how much air is entering. Similarly 124/125 are TP voltage out of expected
range, 159 is MAF out of range, and 184/185 are MAF higher/lower than expected.

These rationality codes are harder to chase than a dead circuit because nothing is open or
shorted — a vacuum leak, a dirty MAF element, a slipped throttle stop, or a misadjusted
sensor can all skew one reading relative to the others. That is why several of them route to
the in-range "G" pinpoint tests (visual MAF inspection, vacuum checks) rather than to a
continuity test. The principle: a circuit code says the wire is broken; a rationality code
says the wire is fine but the number it is carrying does not add up.

This distinction shapes how you read codes from the truck's `engine` and `fuel` systems.

## Related Concepts

- [[notes/dtc-temperature-sensor-codes-pair-low-and-high-voltage|Temperature sensor DTCs come in low/high pairs that mean shorted (254°F) or open (-40°F)]]
- [[notes/dtc-adaptive-fuel-limit-codes-mean-trims-ran-out-of-room|Adaptive-fuel-limit DTCs mean fuel trim hit its correction ceiling and the oxygen sensor can no longer keep the mixture balanced]]
- [[notes/eec-pcm-cross-checks-tps-map-and-pulse-width-for-in-range-failures|The PCM cross-checks TP, MAP, and injector pulse width to catch in-range sensor failures]]

## Source

- [[sources/dtc-air-fuel-sensor-codes|EEC DTCs 112-195 — Air, Fuel, and Sensor Input Codes (FSM)]]
