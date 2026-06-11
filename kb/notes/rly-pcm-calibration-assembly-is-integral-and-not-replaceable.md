---
title: "The PCM's calibration assembly is matched to vehicle weight, axle ratio, and transmission and is not replaceable"
kind: how-it-works
source: "[[sources/rly-powertrain-control-module|Powertrain Control Module (PCM/ECM) — Description, Reset, Service and Specs (FSM)]]"
related:
  - "[[notes/eec-pcm-learns-an-adaptive-strategy-stored-in-kam|The PCM learns an adaptive strategy in Keep Alive Memory to compensate for component wear]]"
  - "[[notes/rly-pcm-retainer-and-connector-torque-specs|PCM retainer screw and connector bolt have specific in-lb torque values]]"
tags:
  - pcm
  - calibration
  - relays-and-modules
---

The PCM compares live sensor inputs against calibration information stored in its memory. That
calibration assembly contains the programming that fine-tunes the PCM's engine commands to the
specific vehicle's weight, axle ratio, and transmission application. Critically, the calibration
assembly is an integral part of the PCM and is not separately replaceable.

The practical consequence is that a replacement PCM must be the correct part for this exact
truck's weight class, axle ratio, and gearbox — you cannot recalibrate a generic module by
swapping a chip. This is distinct from the PCM's learned adaptive strategy, which lives in Keep
Alive Memory and can be cleared and relearned. Both behaviors anchor the `electrical-body` control
network.

## Related Concepts

- [[notes/eec-pcm-learns-an-adaptive-strategy-stored-in-kam|The PCM learns an adaptive strategy in Keep Alive Memory to compensate for component wear]]
- [[notes/rly-pcm-retainer-and-connector-torque-specs|PCM retainer screw and connector bolt have specific in-lb torque values]]
- [[notes/eec-clear-kam-and-drive-10-miles-after-replacing-an-eec-part|After replacing an EEC component, clear Keep Alive Memory and drive ~10 miles to relearn]]

## Source

- [[sources/rly-powertrain-control-module|Powertrain Control Module (PCM/ECM) — Description, Reset, Service and Specs (FSM)]]
