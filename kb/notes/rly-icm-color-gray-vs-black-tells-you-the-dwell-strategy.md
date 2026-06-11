---
title: "A gray ICM controls its own dwell while a black ICM lets the SPOUT signal set dwell"
kind: how-it-works
source: "[[sources/rly-ignition-control-module|Ignition Control Module (ICM) — Description, Operation and Service (FSM)]]"
related:
  - "[[notes/rly-spout-falling-edge-only-controls-coil-on-time-on-the-ccd-system|On the CCD (black ICM) system the SPOUT falling edge controls when the coil turns on]]"
  - "[[notes/mnt-manual-trucks-with-gray-icm-can-be-push-started|Manual-transmission trucks with a gray push-start ICM can be push started]]"
tags:
  - ignition-control-module
  - dwell
  - spout
  - ignition
---

The Ignition Control Module comes in two internal arrangements distinguished by case color. The
gray ICM is the push-start type: it internally determines when to turn the coil ON based on engine
rpm, giving it increased dwell (coil ON time) during cranking. The black ICM is the
computer-controlled-dwell (CCD) type: it does not decide coil ON time itself and instead lets the
PCM's SPOUT signal control dwell entirely.

This color-coded distinction is a fast field identifier for which ignition strategy a truck runs
before chasing spark problems. On both modules the coil fires on the SPOUT rising edge; the
difference is whether the module or the PCM owns the coil charge time. The ICM is the switching
element of the `electrical-starting` spark path, taking the PCM's timing command and driving the
coil.

## Related Concepts

- [[notes/rly-spout-falling-edge-only-controls-coil-on-time-on-the-ccd-system|On the CCD (black ICM) system the SPOUT falling edge controls when the coil turns on]]
- [[notes/mnt-manual-trucks-with-gray-icm-can-be-push-started|Manual-transmission trucks with a gray push-start ICM can be push started]]
- [[notes/eng-distributor-uses-hall-effect-pip-no-mechanical-advance|The distributor uses a Hall-effect PIP signal and has no mechanical advance]]

## Source

- [[sources/rly-ignition-control-module|Ignition Control Module (ICM) — Description, Operation and Service (FSM)]]
