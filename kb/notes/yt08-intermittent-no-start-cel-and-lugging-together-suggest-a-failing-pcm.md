---
title: "Intermittent no-start, an occasional check-engine light, and on-road lugging together suggest a failing PCM"
kind: troubleshooting
source: "[[sources/yt-ford-49l-crankno-start-issue-solved-1994-f-250-49l|Ford 4.9l Crank/No Start Issue SOLVED (1994 F-250 4.9l)]]"
related:
  - "[[notes/rly-pcm-power-relay-supplies-bplus-and-gives-reverse-battery-protection|The PCM power relay supplies B+ to the PCM and protects it against reverse battery polarity]]"
tags:
  - pcm
  - no-start
  - intermittent
  - troubleshooting
  - ignition
---

The owner spent a long time replacing individual `fuel` and `ignition` parts before the pattern
itself became the diagnosis. What finally pointed at the PCM was that **every symptom was
intermittent**: random crank/no-starts, a check-engine light that appeared only occasionally,
and hesitation or "lugging" on the highway that came and went. No single sensor failure cleanly
explained all three at once, and the come-and-go nature is the hallmark of a marginal control
module rather than a hard-failed component.

His lesson, stated plainly, is that the PCM "is something I probably should have checked from
the beginning" given that profile — he describes PCM failure as a **common failure point on
these 4.9L OBS trucks**. Treat this as a heuristic, not a guarantee: before condemning an
expensive module, the FSM still expects you to confirm power and grounds to the PCM (the
`electrical-starting` run circuit and the PCM power relay) and to pull and clear codes. But when
multiple unrelated, intermittent driveability faults coincide, the PCM belongs high on the list.

## Related Concepts

- [[notes/rly-pcm-power-relay-supplies-bplus-and-gives-reverse-battery-protection|The PCM power relay supplies B+ to the PCM and protects it against reverse battery polarity]]
- [[notes/eec-fuel-pump-runs-12s-at-key-on-then-needs-an-rpm-signal|The fuel pump runs 1-2 s at key-on, then the PCM keeps it running only with an rpm signal above 120]]

## Source

- [[sources/yt-ford-49l-crankno-start-issue-solved-1994-f-250-49l|Ford 4.9l Crank/No Start Issue SOLVED (1994 F-250 4.9l)]]
