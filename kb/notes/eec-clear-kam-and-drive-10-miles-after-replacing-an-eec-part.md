---
title: "After replacing an EEC component, clear Keep Alive Memory and drive ~10 miles to relearn"
kind: procedure
source: "[[sources/eec-engine-control-module|Engine Control Module (PCM / EEC-IV) — Description, Operation, and Reset (FSM)]]"
related:
  - "[[notes/eec-pcm-learns-an-adaptive-strategy-stored-in-kam|The PCM learns an adaptive strategy in Keep Alive Memory to compensate for component wear]]"
  - "[[notes/eec-iac-is-part-of-adaptive-strategy-and-surges-at-its-limits|The IAC is part of adaptive strategy and surges when it reaches its learning limits]]"
tags:
  - keep-alive-memory
  - kam-reset
  - adaptive-strategy
  - eec-iv
---

When an Electronic Engine Control component is replaced, the values the PCM learned for the old
part are now wrong for the new one, so the FSM procedure is to clear Keep Alive Memory (KAM)
and let the PCM relearn. To clear KAM, disconnect the battery negative terminal for five minutes
or more — preferably 15 minutes. This erases the stored adaptive corrections.

After the repair and KAM reset, drive the vehicle at least ten miles so the PCM can relearn the
optimum fuel-delivery and idle values. During that relearn drive the truck may exhibit
driveability symptoms (rough or wandering idle, minor hesitation); these should clear once KAM
has relearned. The same caution appears in the TPS and IAC service procedures after any battery
disconnect.

This procedure applies across the `engine`, `fuel`, and `ignition` inventory systems whenever an
EEC part is changed.

## Related Concepts

- [[notes/eec-pcm-learns-an-adaptive-strategy-stored-in-kam|The PCM learns an adaptive strategy in Keep Alive Memory to compensate for component wear]]
- [[notes/eec-iac-is-part-of-adaptive-strategy-and-surges-at-its-limits|The IAC is part of adaptive strategy and surges when it reaches its learning limits]]
- [[notes/chg-disconnecting-the-battery-erases-the-pcm-adaptive-strategy|Disconnecting the battery erases the PCM adaptive strategy and may need 10+ miles to relearn]]
- [[notes/rly-pcm-calibration-assembly-is-integral-and-not-replaceable|The PCM's calibration assembly is matched to vehicle weight, axle ratio, and transmission and is not replaceable]]
- [[notes/bdy-battery-disconnect-forces-the-pcm-to-relearn-over-ten-miles|Any cab battery disconnect forces the PCM to relearn its adaptive strategy over about ten miles]]

## Source

- [[sources/eec-engine-control-module|Engine Control Module (PCM / EEC-IV) — Description, Operation, and Reset (FSM)]]
