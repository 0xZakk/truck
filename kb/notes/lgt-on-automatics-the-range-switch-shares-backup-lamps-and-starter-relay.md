---
title: "On automatics the same range switch lights the backup lamps and closes the starter relay"
kind: troubleshooting
source: "[[sources/lgt-backup-lamp-switch|Backup Lamp Switch / Park-Neutral Position Switch by Transmission (FSM)]]"
related:
  - "[[notes/lgt-backup-lamp-source-depends-on-the-transmission|What powers the backup lamps depends on which transmission the truck has]]"
tags:
  - backup-lamp
  - park-neutral-switch
  - starter
  - troubleshooting
  - lighting
---

On the 1994 F-150's automatic transmissions, the backup lamp circuit and the starter circuit
go through the same component. With the C6 the park/neutral position switch directs current
to the backup lamps in REVERSE and to the starter motor relay in PARK or NEUTRAL; with the
E4OD/4R70W the manual lever position (transmission range) sensor does both.

This shared role is a useful diagnostic clue. If both the reverse lights are dead and the
engine won't crank in Park/Neutral, suspect the range/PNP switch or its adjustment rather
than two unrelated faults. Conversely, a no-crank that is cured by jiggling the shifter, or
reverse lights that come on in the wrong gear, both point to the same switch being out of
adjustment. This is part of the truck's `electrical-body` system.

> "With the transmission in 'PARK' or 'NEUTRAL' the park/neutral position switch directs
> current to close the starter motor relay."

## Related Concepts

- [[notes/lgt-backup-lamp-source-depends-on-the-transmission|What powers the backup lamps depends on which transmission the truck has]]
- [[notes/chg-park-neutral-switch-both-closes-the-relay-and-lights-backup-lamps|On automatics, the park/neutral switch both closes the starter relay and lights the backup lamps]]
- [[notes/chg-clutch-switch-is-an-in-series-interlock-to-the-starter-relay|The starting interlock switch sits in series between the start signal and the starter relay]]
- [[notes/clutch-pedal-position-switch-is-the-start-interlock-on-manual-f150|The clutch pedal position switch is the start interlock on a manual F-150]]

## Source

- [[sources/lgt-backup-lamp-switch|Backup Lamp Switch / Park-Neutral Position Switch by Transmission (FSM)]]
