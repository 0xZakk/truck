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
  - start-interlock
  - no-crank
  - how-it-works
---

Whatever the transmission, the starting interlock switch is wired **in series** between the
ignition switch's start signal and the **starter relay**. On the manual F-150 — which has the
**M5OD-R2 5-speed** — that switch is the **clutch pedal position switch** rather than a
neutral safety switch; on automatics it is the park/neutral switch or manual lever position
sensor. The switch must close before voltage reaches the relay coil, so the relay cannot pull
in — and the starter cannot crank — unless the truck is in a safe state. Pressing the clutch
pedal closes the switch and lets voltage reach the relay; with the pedal up the circuit is
open and the relay never pulls in.

> "Depressing the clutch pedal closes the clutch pedal position switch, directing voltage
> and current to the starter relay."

This series relationship is why an interlock fault presents as a **no-crank**: the switch
itself, its adjustment, or its wiring breaks the path to the relay. The clutch switch is a
prime suspect in no-crank complaints — especially the telltale pattern where the truck only
cranks if you "stand on" the clutch, or won't crank at all after the switch drifts out of
adjustment, wears, or unplugs. The battery, relay, and starter can all test fine while a
10-cent switch blocks the trigger signal. A quick check is to verify **continuity through the
switch with the pedal fully depressed and an open with it released**; no continuity when
pressed points at the switch or its adjustment. This is the manual-transmission analog of
diagnosing an automatic's neutral safety switch.

It is also why the factory starter Load Test deliberately bypasses the relay "S" terminal
with a remote switch — doing so takes the interlock out of the loop so a weak switch cannot
be mistaken for a weak starter.

This relates to truck inventory systems `electrical-starting` and `electrical-body`.

## Related Concepts

- [[notes/chg-park-neutral-switch-both-closes-the-relay-and-lights-backup-lamps|On automatics, the park/neutral switch both closes the starter relay and lights the backup lamps]]
- [[notes/chg-starter-load-test-feeds-the-relay-s-terminal-from-a-remote-switch|The starter Load Test cranks the engine by feeding the relay S terminal from a remote switch]]
- [[notes/clutch-pedal-position-switch-is-the-start-interlock-on-manual-f150|The clutch pedal position switch is the start interlock on a manual F-150]]
- [[notes/crz-clutch-switch-deactivates-cruise-when-pedal-depressed|On manual trucks the clutch switch deactivates cruise the moment the pedal is depressed]]
- [[notes/f150-uses-permanent-magnet-gear-reduction-starter|The 1994 F-150 uses a permanent-magnet gear-reduction starter]]
- [[notes/sen-tripped-inertia-switch-causes-crank-no-start|A tripped inertia switch is a common crank-no-start cause and must be manually reset]]

## Source

- [[sources/chg-starting-interlock-switches|Starting Interlock Switches (Clutch / Neutral Safety) — Description and Operation (FSM)]]
- [[sources/sen-clutch-pedal-position-switch|Clutch Pedal Position Switch (Manual Transmission Start Interlock) — Description and Operation (FSM)]]
