---
title: "The PCM learns an adaptive strategy in Keep Alive Memory to compensate for component wear"
kind: how-it-works
source: "[[sources/eec-engine-control-module|Engine Control Module (PCM / EEC-IV) — Description, Operation, and Reset (FSM)]]"
related:
  - "[[notes/eec-clear-kam-and-drive-10-miles-after-replacing-an-eec-part|After replacing an EEC component, clear Keep Alive Memory and drive ~10 miles to relearn]]"
  - "[[notes/eec-iac-is-part-of-adaptive-strategy-and-surges-at-its-limits|The IAC is part of adaptive strategy and surges when it reaches its learning limits]]"
tags:
  - pcm
  - eec-iv
  - adaptive-strategy
  - keep-alive-memory
---

Beyond its fixed base calibration, the 1994 F-150's EEC-IV PCM continuously calculates and
learns an adaptive strategy that compensates for the normal wear and aging of components. It
shifts fuel-delivery calculations and idle-speed values over time so the truck keeps running
correctly as injectors, the IAC, and sensors drift from new. These learned corrections live in
Keep Alive Memory (KAM), which is retained as long as battery power is present.

The practical consequence is that the PCM's behavior is partly a record of the specific parts
currently installed. When you swap a part, the old learned values no longer match the new
hardware, which is why the FSM ties part replacement to a KAM reset. The base calibration
assembly itself is integral to the PCM and is not separately replaceable.

This is foundational to the `engine`, `fuel`, and `ignition` inventory systems, since adaptive
strategy touches fuel pulse width, idle air, and timing.

## Related Concepts

- [[notes/eec-clear-kam-and-drive-10-miles-after-replacing-an-eec-part|After replacing an EEC component, clear Keep Alive Memory and drive ~10 miles to relearn]]
- [[notes/eec-iac-is-part-of-adaptive-strategy-and-surges-at-its-limits|The IAC is part of adaptive strategy and surges when it reaches its learning limits]]
- [[notes/rly-pcm-calibration-assembly-is-integral-and-not-replaceable|The PCM's calibration assembly is matched to vehicle weight, axle ratio, and transmission and is not replaceable]]
- [[notes/chg-disconnecting-the-battery-erases-the-pcm-adaptive-strategy|Disconnecting the battery erases the PCM adaptive strategy and may need 10+ miles to relearn]]

## Source

- [[sources/eec-engine-control-module|Engine Control Module (PCM / EEC-IV) — Description, Operation, and Reset (FSM)]]
