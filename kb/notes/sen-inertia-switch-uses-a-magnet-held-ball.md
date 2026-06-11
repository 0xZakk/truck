---
title: "The inertia switch cuts fuel-pump power in a crash using a magnet-held ball that breaks loose on impact"
kind: how-it-works
source: "[[sources/sen-inertia-fuel-shutoff-switch|Inertia Fuel Shutoff (IFS) Switch — Description and Operation (FSM)]]"
related:
  - "[[notes/sen-tripped-inertia-switch-causes-crank-no-start|A tripped inertia switch is a common crank-no-start cause and must be manually reset]]"
tags:
  - inertia-switch
  - fuel
  - safety
---

The inertia fuel shutoff switch is a purely mechanical safety device, no electronics involved.
Inside, a steel ball is held in a detent by a permanent magnet. Under normal driving the magnet
holds the ball put, and the switch's electrical contacts — wired in series with the electric
fuel pump's power feed — stay closed.

In a collision the deceleration force overcomes the magnet's hold. The ball breaks loose, rolls
up a conical ramp, and strikes a target plate that opens the contacts. That cuts power to the
fuel pump, and the engine starves and quits within a few seconds. The purpose is to stop
pumping fuel toward a possibly ruptured line after a crash.

For the `fuel` system, the key behavioral detail is that this is a latching open: once tripped,
the contacts stay open until the button is manually pushed to re-seat the ball. The truck stays
fuel-dead until reset — by design, so a crash doesn't keep feeding a leak.

## Related Concepts

- [[notes/sen-tripped-inertia-switch-causes-crank-no-start|A tripped inertia switch is a common crank-no-start cause and must be manually reset]]
- [[notes/eec-fuel-pump-runs-12s-at-key-on-then-needs-an-rpm-signal|The fuel pump runs 1-2 s at key-on, then the PCM keeps it running only with an rpm signal above 120]]
- [[notes/rly-fuel-pump-relay-is-grounded-by-the-pcm-not-a-simple-switch|The fuel pump relay is grounded by the PCM, so its ground circuit is the real no-start clue]]
- [[notes/rly-eec-power-relay-feeds-the-fuel-pump-relay-coil|Power to the fuel pump relay comes from the EEC power relay through the PCM and the inertia switch]]

## Source

- [[sources/sen-inertia-fuel-shutoff-switch|Inertia Fuel Shutoff (IFS) Switch — Description and Operation (FSM)]]
