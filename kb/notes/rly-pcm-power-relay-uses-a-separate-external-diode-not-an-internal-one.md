---
title: "The PCM power relay is an SPDT relay with no internal diode and relies on a separate external diode"
kind: spec
source: "[[sources/rly-pcm-power-main-relay|Main Relay (Computer/Fuel System) / PCM Power Relay — Description and Operation (FSM)]]"
related:
  - "[[notes/rly-pcm-power-relay-supplies-bplus-and-gives-reverse-battery-protection|The PCM power relay supplies B+ to the PCM and protects it against reverse battery polarity]]"
tags:
  - pcm-power-relay
  - main-relay
  - diode
  - relays-and-modules
---

The PCM power relay is constructed as a single-pole double-throw (SPDT) type. Unlike many relays
that carry their own coil-suppression diode, this relay does not have an internal diode — it is
used together with a separate, stand-alone diode.

This construction detail is practically important: if you replace the relay, the suppression diode
is an external part that must remain in the circuit, and a swapped-in relay that does contain an
internal diode is not an exact equivalent. When chasing intermittent control-module faults in the
`electrical-body` distribution, the separate diode is its own failure point worth verifying.

## Related Concepts

- [[notes/rly-pcm-power-relay-supplies-bplus-and-gives-reverse-battery-protection|The PCM power relay supplies B+ to the PCM and protects it against reverse battery polarity]]

## Source

- [[sources/rly-pcm-power-main-relay|Main Relay (Computer/Fuel System) / PCM Power Relay — Description and Operation (FSM)]]
