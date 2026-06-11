---
title: "Oil Level Warning Indicator — Description, Operation and Testing (FSM)"
source: "manuals/factory-service-manual/1994 Ford F 150 2WD Pickup L6-300 4.9L/Repair and Diagnosis/Instrument Panel, Gauges and Warning Indicators/Oil Level Warning Indicator/Description and Operation/index.html"
type: local
date: 2026-06-11
author: "Ford Factory Service Manual"
tags:
  - oil-level-warning-indicator
  - warning-indicators
  - lubrication
  - troubleshooting
processed: true
---

## Summary

The Check Oil (low oil level) warning system is distinct from the oil pressure lamp. It
consists of a float-type sensor on the side of the oil pan, an electronic control module,
and an instrument-panel warning lamp. The lamp lights in START as a bulb prove-out. When the
key is in RUN or START, the control module reads whether the sensor is grounded (oil low) or
ungrounded (oil not low). If level is adequate, the lamp goes out in RUN; if the oil is
roughly 1.5 quarts or more low, the relay turns the lamp ON and it stays on until the
ignition is turned OFF.

A key behavior to understand is the reset delay: after the ignition is turned OFF, the
module will not reset for about five minutes, allowing oil to drain back before another
reading. If the engine is restarted within that window, the last reading is displayed. The
FSM's functional test exploits this — drain two quarts, wait ~5 minutes, restart, and the
lamp should come on and stay on.

## Key Points

- Components: pan-mounted float sensor + electronic control module + IP warning lamp.
- Bulb prove-out occurs in START.
- Module reads sensor grounded (low) vs. ungrounded (not low) in RUN/START.
- Trips at approximately 1.5 quarts or more low; stays on until ignition OFF.
- ~5-minute reset delay after key-OFF for oil drain-back; restart within window shows last reading.
- Functional test: drain 2 quarts, wait ~5 min, restart; lamp should illuminate and stay on. If not, check fuse, low-oil relay, sensor, and lamp.

## Notable Excerpts

> "If oil level is approximately 1.5 quarts or more low, the relay turns the warning lamp ON.
> The lamp will remain ON until ignition is turned OFF."

> "After ignition is turned OFF, module will not reset for approximately five minutes. This
> delay allows time for oil drain back before another reading is allowed to occur."

> "Drain two quarts of oil from engine. Wait approximately five minutes, then restart engine.
> Warning lamp should come on and stay on. If warning lamp does not come on check fuse, low
> oil level relay, low oil level sensor and lamp."

Source: FSM — Instrument Panel, Gauges and Warning Indicators / Oil Level Warning Indicator / Description and Operation and Testing and Inspection.
