---
title: "Disconnecting the battery erases the PCM adaptive strategy and may need 10+ miles to relearn"
kind: troubleshooting
source: "[[sources/chg-service-precautions|Starting and Charging — Service Precautions (FSM)]]"
related:
  - "[[notes/chg-disarm-the-air-bag-before-battery-work-on-starting-and-charging|Disarm the air bag system before disconnecting the battery for starting/charging work]]"
tags:
  - charging-system
  - pcm
  - troubleshooting
---

After the battery has been disconnected and reconnected on the 1994 F-150, the Powertrain
Control Module loses its **learned adaptive strategy**. The manual warns that **abnormal
drive conditions may be present** while the PCM relearns, and the truck may need to be driven
**10 or more miles** before it behaves normally again.

This matters for diagnosis: a rough idle, hesitation, or odd shifting that shows up right
after charging-system or battery work is often just the PCM relearning, not a new fault.
Give it the relearn miles before chasing a driveability complaint. The manual also reminds
you to record radio presets before pulling the battery, since they are lost too.

> "After the battery has been disconnected and reconnected, abnormal drive conditions may be
> present while the Powertrain Control Module (PCM) relearns its adaptive strategy. The
> vehicle may need to be driven 10 or more miles to relearn the strategy."

This relates to truck inventory systems `electrical-starting` and `electrical-charging`.

## Related Concepts

- [[notes/chg-disarm-the-air-bag-before-battery-work-on-starting-and-charging|Disarm the air bag system before disconnecting the battery for starting/charging work]]
- [[notes/bdy-battery-disconnect-forces-the-pcm-to-relearn-over-ten-miles|Any cab battery disconnect forces the PCM to relearn its adaptive strategy over about ten miles]]
- [[notes/eec-clear-kam-and-drive-10-miles-after-replacing-an-eec-part|After replacing an EEC component, clear Keep Alive Memory and drive ~10 miles to relearn]]
- [[notes/eec-pcm-learns-an-adaptive-strategy-stored-in-kam|The PCM learns an adaptive strategy in Keep Alive Memory to compensate for component wear]]

## Source

- [[sources/chg-service-precautions|Starting and Charging — Service Precautions (FSM)]]
