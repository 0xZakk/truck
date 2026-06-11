---
title: "A tripped inertia switch is a common crank-no-start cause and must be manually reset"
kind: troubleshooting
source: "[[sources/sen-inertia-fuel-shutoff-switch|Inertia Fuel Shutoff (IFS) Switch — Description and Operation (FSM)]]"
related:
  - "[[notes/sen-inertia-switch-uses-a-magnet-held-ball|The inertia switch cuts fuel-pump power in a crash using a magnet-held ball that breaks loose on impact]]"
tags:
  - inertia-switch
  - fuel-pump
  - fuel
  - troubleshooting
  - no-start
---

When the engine cranks normally but won't start and you can't hear the fuel pump prime, the
inertia fuel shutoff switch is one of the first cheap things to check on this truck. The switch
latches open after any sharp jolt — a hard pothole, a parking tap, even a slammed door or
tailgate can be enough — and once open it kills power to the electric fuel pump until someone
presses its reset button.

Because the switch is in the pump's power feed, a tripped IFS produces exactly the symptoms of a
dead pump: good cranking, spark present, but no fuel pressure and no start. The fix is to find
the reset button (on the F-150 it's in the cab, typically near a kick panel/footwell) and push
it back in.

Two cautions tie back to the `fuel` system: confirm there's no fuel leak before resetting (the
FSM warns not to reset if you see or smell fuel), and if the switch keeps tripping with no
impact, suspect a faulty switch or loose mounting rather than repeatedly resetting it.

## Related Concepts

- [[notes/sen-inertia-switch-uses-a-magnet-held-ball|The inertia switch cuts fuel-pump power in a crash using a magnet-held ball that breaks loose on impact]]
- [[notes/rly-fuel-pump-relay-is-grounded-by-the-pcm-not-a-simple-switch|The fuel pump relay is grounded by the PCM, so its ground circuit is the real no-start clue]]
- [[notes/sen-clutch-switch-is-the-manual-start-interlock|On the manual F-150 the clutch pedal switch is the start interlock and feeds the starter relay only when the pedal is down]]
- [[notes/rly-eec-power-relay-feeds-the-fuel-pump-relay-coil|Power to the fuel pump relay comes from the EEC power relay through the PCM and the inertia switch]]
- [[notes/eec-fuel-pump-runs-12s-at-key-on-then-needs-an-rpm-signal|The fuel pump runs 1-2 s at key-on, then the PCM keeps it running only with an rpm signal above 120]]

## Source

- [[sources/sen-inertia-fuel-shutoff-switch|Inertia Fuel Shutoff (IFS) Switch — Description and Operation (FSM)]]
