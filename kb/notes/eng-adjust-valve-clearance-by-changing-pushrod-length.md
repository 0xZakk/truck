---
title: "Adjust 4.9L valve clearance by changing pushrod length, in firing order"
kind: procedure
source: "[[sources/eng-valve-clearance-and-idle|Valve Clearance & Idle Speed — Adjustment Procedures and Specs (FSM)]]"
related:
  - "[[notes/eng-49l-firing-order-is-1-5-3-6-2-4|The 4.9L firing order is 1-5-3-6-2-4]]"
  - "[[notes/eng-idle-speed-is-pcm-controlled-dont-back-off-the-throttle-stop|Idle speed is PCM-controlled — don't back off the throttle-plate stop screw]]"
tags:
  - engine
  - valve-clearance
  - hydraulic-lifter
  - procedure
  - spec
---

The 4.9L has hydraulic lifters, so its "valve clearance" check is really a measurement of the
collapsed-tappet gap between the rocker arm and the valve-stem tip, measured with the lifter bled
down. Because the rocker bolts are torqued fixed (non-adjustable) — there is no shim or screw to
dial it in — clearance is corrected by swapping pushrods. With a cylinder at TDC on its
compression stroke, torque the rocker bolts to spec, then use a tappet bleed-down tool to fully
bottom the lifter plunger and measure the gap with a feeler gauge. The allowable range is
0.100-0.200 in, with a desirable range of 0.125-0.175 in. If the gap is too small, install a
shorter pushrod; if too large, install a longer one.

Work through the cylinders in firing order 1-5-3-6-2-4, turning the crankshaft one-third turn at a
time (the damper is marked at three 120-degree points to index this) on the `engine` inventory
system. Out-of-range clearance points to lifter or valvetrain wear and can mimic driveability or
noise complaints, so it belongs alongside compression as an `engine` mechanical check.

> "If clearance is less than specifications, install shorter pushrod. If clearance is greater than
> specifications, install longer pushrod. ... in firing order sequence of 1-5-3-6-2-4."

## Related Concepts

- [[notes/eng-49l-firing-order-is-1-5-3-6-2-4|The 4.9L firing order is 1-5-3-6-2-4]]
- [[notes/eng-idle-speed-is-pcm-controlled-dont-back-off-the-throttle-stop|Idle speed is PCM-controlled — don't back off the throttle-plate stop screw]]
- [[notes/spc-valvetrain-overhaul-specs-cover-springs-guides-and-seats|Valve-train overhaul specs set 45° seats, 0.001–0.0027 in stem clearance, and 66–74 lb closed spring pressure]]
- [[notes/spc-camshaft-and-lifter-overhaul-clearances-for-the-49l|Camshaft and lifter overhaul clearances for the 4.9L]]
- [[notes/spc-piston-clearance-is-0010-0018-in-and-compression-ring-end-gap-is-0010-0020-in|Piston clearance is 0.0010–0.0018 in and compression ring end gap is 0.010–0.020 in]]

## Source

- [[sources/eng-valve-clearance-and-idle|Valve Clearance & Idle Speed — Adjustment Procedures and Specs (FSM)]]
- [[sources/eec-tune-up-and-engine-checks|Tune-up and Engine Performance Checks — Timing, Firing Order, Compression, Valve Clearance, Spark Plugs (FSM)]]
