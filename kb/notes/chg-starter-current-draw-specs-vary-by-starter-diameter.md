---
title: "Starter current-draw specs vary by starter diameter"
kind: spec
source: "[[sources/chg-starter-motor-specifications|Starter Motor — Specifications (FSM)]]"
related:
  - "[[notes/chg-starter-no-load-test-finds-shorts-and-rubbing-armature|The starter No-Load test finds shorted windings and a rubbing armature by reading current draw]]"
  - "[[notes/chg-starter-load-test-feeds-the-relay-s-terminal-from-a-remote-switch|The starter Load Test cranks the engine by feeding the relay S terminal from a remote switch]]"
tags:
  - starter
  - starting-system
  - spec
---

The pass/fail numbers for the starter No-Load and Load tests depend on which starter is
fitted, so identify the diameter first. The **4-1/2 in** starter draws **150–180 A** under
normal load and **80 A no-load @ 12 V**, with a cranking speed of **150–290 RPM**. One **4 in**
variant draws **150–200 A** loaded and **60–85 A no-load**, cranking at **180–250 RPM**.
A second **4 in** variant draws **130–220 A** loaded and **60–80 A no-load**, cranks at
**140–220 RPM**, and has a minimum stall torque of **11 ft-lbs @ 5 V**.

Brush limits are similar across units: brush length new is **0.50 in** (or **0.66 in** on the
high-torque 4 in variant) with a **0.25 in** wear limit, and brush-spring tension is **40 oz**
(or **64 oz** on that variant). Reading current that is above the loaded spec or no-load
spec points to a dragging or shorted starter; reading low cranking speed with normal current
points instead at the battery or cables.

> "Starter Diameter 4 1/2 Inch — Ampere Draw Normal Load 150-180 — No-Load Ampere @ 12 Volts
> 80 … Engine Cranking Speed 150-290 RPM"

This relates to truck inventory system `electrical-starting`.

## Related Concepts

- [[notes/chg-starter-no-load-test-finds-shorts-and-rubbing-armature|The starter No-Load test finds shorted windings and a rubbing armature by reading current draw]]
- [[notes/chg-starter-load-test-feeds-the-relay-s-terminal-from-a-remote-switch|The starter Load Test cranks the engine by feeding the relay S terminal from a remote switch]]

## Source

- [[sources/chg-starter-motor-specifications|Starter Motor — Specifications (FSM)]]
