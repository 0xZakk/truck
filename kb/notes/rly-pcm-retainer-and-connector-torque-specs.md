---
title: "PCM retainer screw and connector bolt have specific in-lb torque values"
kind: spec
source: "[[sources/rly-powertrain-control-module|Powertrain Control Module (PCM/ECM) — Description, Reset, Service and Specs (FSM)]]"
related:
  - "[[notes/rly-pcm-calibration-assembly-is-integral-and-not-replaceable|The PCM's calibration assembly is matched to vehicle weight, axle ratio, and transmission and is not replaceable]]"
  - "[[notes/eec-clear-kam-and-drive-10-miles-after-replacing-an-eec-part|After replacing an EEC component, clear Keep Alive Memory and drive ~10 miles to relearn]]"
tags:
  - pcm
  - torque
  - spec
  - relays-and-modules
---

When servicing the Powertrain Control Module, the FSM gives small, precise fastener torques. The
PCM retainer screw is tightened to 2.7-3.7 N-m (24-32 in-lb) — listed as 3-4 N-m in the removal
procedure — and the electrical connector retainer bolt is tightened to 3.7 N-m (32 in-lb).

These are in-pound-range values; over-torquing the connector bolt risks cracking the module or
its connector. The connector retainer bolt also ensures the multi-pin connector is fully seated,
which prevents the intermittent control faults that plague this `electrical-body` module when its
connector is loose.

## Related Concepts

- [[notes/rly-pcm-calibration-assembly-is-integral-and-not-replaceable|The PCM's calibration assembly is matched to vehicle weight, axle ratio, and transmission and is not replaceable]]
- [[notes/eec-clear-kam-and-drive-10-miles-after-replacing-an-eec-part|After replacing an EEC component, clear Keep Alive Memory and drive ~10 miles to relearn]]

## Source

- [[sources/rly-powertrain-control-module|Powertrain Control Module (PCM/ECM) — Description, Reset, Service and Specs (FSM)]]
