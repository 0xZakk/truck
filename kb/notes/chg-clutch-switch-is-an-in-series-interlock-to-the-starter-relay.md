---
title: "The starting interlock switch sits in series between the start signal and the starter relay"
kind: how-it-works
source: "[[sources/chg-starting-interlock-switches|Starting Interlock Switches (Clutch / Neutral Safety) — Description and Operation (FSM)]]"
related:
  - "[[notes/chg-park-neutral-switch-both-closes-the-relay-and-lights-backup-lamps|On automatics, the park/neutral switch both closes the starter relay and lights the backup lamps]]"
  - "[[notes/chg-starter-load-test-feeds-the-relay-s-terminal-from-a-remote-switch|The starter Load Test cranks the engine by feeding the relay S terminal from a remote switch]]"
tags:
  - starting-system
  - clutch-switch
  - neutral-safety-switch
  - how-it-works
---

Whatever the transmission, the starting interlock switch is wired **in series** between the
ignition switch's start signal and the **starter relay**. On the manual F-150 it is the
clutch pedal position switch; on automatics it is the park/neutral switch or manual lever
position sensor. The switch must close before voltage reaches the relay coil, so the relay
cannot pull in — and the starter cannot crank — unless the truck is in a safe state.

This series relationship is why an interlock fault presents as a **no-crank**: the switch
itself, its adjustment, or its wiring breaks the path to the relay. It is also why the
factory starter Load Test deliberately bypasses the relay "S" terminal with a remote switch
— doing so takes the interlock out of the loop so a weak switch cannot be mistaken for a
weak starter.

> "Depressing the clutch pedal closes the clutch pedal position switch, directing voltage
> and current to the starter relay."

This relates to truck inventory system `electrical-starting`.

## Related Concepts

- [[notes/chg-park-neutral-switch-both-closes-the-relay-and-lights-backup-lamps|On automatics, the park/neutral switch both closes the starter relay and lights the backup lamps]]
- [[notes/chg-starter-load-test-feeds-the-relay-s-terminal-from-a-remote-switch|The starter Load Test cranks the engine by feeding the relay S terminal from a remote switch]]
- [[notes/sen-clutch-switch-is-the-manual-start-interlock|On the manual F-150 the clutch pedal switch is the start interlock and feeds the starter relay only when the pedal is down]]
- [[notes/clutch-pedal-position-switch-is-the-start-interlock-on-manual-f150|The clutch pedal position switch is the start interlock on a manual F-150]]
- [[notes/lgt-on-automatics-the-range-switch-shares-backup-lamps-and-starter-relay|On automatics the same range switch lights the backup lamps and closes the starter relay]]
- [[notes/f150-uses-permanent-magnet-gear-reduction-starter|The 1994 F-150 uses a permanent-magnet gear-reduction starter]]

## Source

- [[sources/chg-starting-interlock-switches|Starting Interlock Switches (Clutch / Neutral Safety) — Description and Operation (FSM)]]
