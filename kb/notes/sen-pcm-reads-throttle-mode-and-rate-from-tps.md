---
title: "The PCM derives idle, cruise, WOT, and acceleration-pump action from TP angle and its rate of change"
kind: how-it-works
source: "[[sources/sen-throttle-position-sensor|Throttle Position (TP) Sensor — Description, Operation, and DTCs (FSM)]]"
related:
  - "[[notes/sen-tps-is-a-voltage-divider-06-to-45-volts|The TP sensor is a potentiometer that outputs about 0.6 V at closed throttle and 4.5 V at wide open throttle]]"
  - "[[notes/sen-map-converts-manifold-vacuum-to-a-frequency|The MAP sensor reports engine load as a frequency that falls as manifold vacuum rises]]"
tags:
  - throttle-position-sensor
  - tps
  - fuel
---

The TP signal is more than "how far is the pedal" — the PCM turns it into discrete operating
modes. A closed-throttle reading means idle or deceleration; a mid-range reading means cruise
or moderate acceleration; a near-VREF reading means wide open throttle, which triggers
dechoke-on-crank (clears a flooded engine) and A/C compressor cutout for full power.

The PCM also differentiates the signal over time. A fast rise in throttle angle is read as an
acceleration-pump-type demand, enriching fuel transiently the way a carburetor's accelerator
pump would. The same throttle-rate data feeds the transmission shift schedule.

For the `fuel` system, this is why a TP sensor that reads correctly at the endpoints but is
dead or glitchy in the middle causes driveability complaints — hesitation, surging, or wrong
shift timing — even when no hard DTC sets. The in-range codes 124/125 exist precisely to catch
a TP signal that looks plausible but disagrees with airflow and injector pulse width.

## Related Concepts

- [[notes/sen-tps-is-a-voltage-divider-06-to-45-volts|The TP sensor is a potentiometer that outputs about 0.6 V at closed throttle and 4.5 V at wide open throttle]]
- [[notes/sen-map-converts-manifold-vacuum-to-a-frequency|The MAP sensor reports engine load as a frequency that falls as manifold vacuum rises]]
- [[notes/eec-tps-is-a-potentiometer-reading-06v-closed-to-45v-wot|The TP sensor is a potentiometer reading about 0.6 V closed to 4.5 V at wide-open throttle]]
- [[notes/eec-pcm-cross-checks-tps-map-and-pulse-width-for-in-range-failures|The PCM cross-checks TP, MAP, and injector pulse width to catch in-range sensor failures]]
- [[notes/eec-map-sensor-outputs-a-frequency-and-doubles-as-a-baro-sensor|The MAP sensor outputs a frequency proportional to load and doubles as a barometric sensor]]

## Source

- [[sources/sen-throttle-position-sensor|Throttle Position (TP) Sensor — Description, Operation, and DTCs (FSM)]]
