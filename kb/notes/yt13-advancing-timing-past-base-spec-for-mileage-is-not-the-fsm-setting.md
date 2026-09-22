---
title: "Advancing base timing past 10° BTDC for mileage is a hobbyist experiment, not the factory spec"
kind: troubleshooting
source: "[[sources/yt-ignition-timing-demostration-1990-ford-f150|Ignition Timing Demostration 1990 Ford F150]]"
related:
  - "[[notes/mnt-base-timing-is-10-degrees-btdc-firing-order-1-5-3-6-2-4|Base ignition timing is 10° BTDC and the 4.9L firing order is 1-5-3-6-2-4]]"
  - "[[notes/mnt-octane-jumper-removed-retards-timing-three-degrees|Pulling the octane-adjust jumper retards computed timing about three degrees to fight detonation]]"
tags:
  - ignition
  - timing
  - troubleshooting
---

In this video the presenter advances his base timing to roughly 14-15 degrees BTDC, hoping to
improve gas mileage, and observes idle climb from about 650 rpm (his stated factory reference at
10 degrees) to around 700-750 rpm. Treat this as a hobbyist tuning experiment, not a setting to
copy. The factory base timing for the EEC-IV 4.9L on the `ignition` system is 10 degrees BTDC; the
PCM then adds computed advance on top of that once SPOUT is reconnected.

Running more base advance than spec raises the entire computed-advance curve and reduces knock
margin, so it can cause detonation (pinging) under load — especially on lower-octane fuel or in
hot weather. Ford's own tool for the opposite direction is the octane-adjust jumper, which retards
computed timing about three degrees to fight detonation. If you are diagnosing or restoring a
truck, set base timing to the factory 10 degrees BTDC rather than chasing mileage with extra
advance; an over-advanced distributor is a plausible cause of pinging or a slightly elevated idle.

## Related Concepts

- [[notes/mnt-base-timing-is-10-degrees-btdc-firing-order-1-5-3-6-2-4|Base ignition timing is 10° BTDC and the 4.9L firing order is 1-5-3-6-2-4]]
- [[notes/mnt-octane-jumper-removed-retards-timing-three-degrees|Pulling the octane-adjust jumper retards computed timing about three degrees to fight detonation]]
- [[notes/eng-set-base-timing-by-disconnecting-the-spout-connector|Set base timing by disconnecting the SPOUT connector and using the key to start]]

## Source

- [[sources/yt-ignition-timing-demostration-1990-ford-f150|Ignition Timing Demostration 1990 Ford F150]]
