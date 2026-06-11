---
title: "The PCM power relay supplies B+ to the PCM and protects it against reverse battery polarity"
kind: how-it-works
source: "[[sources/rly-pcm-power-main-relay|Main Relay (Computer/Fuel System) / PCM Power Relay — Description and Operation (FSM)]]"
related:
  - "[[notes/rly-pcm-power-relay-uses-a-separate-external-diode-not-an-internal-one|The PCM power relay is an SPDT relay with no internal diode and relies on a separate external diode]]"
  - "[[notes/rly-eec-power-relay-feeds-the-fuel-pump-relay-coil|Power to the fuel pump relay comes from the EEC power relay through the PCM and the inertia switch]]"
tags:
  - pcm-power-relay
  - main-relay
  - reverse-polarity-protection
  - pcm
---

The Main Relay (Computer/Fuel System), called the PCM power relay in the FSM, is what actually
delivers battery voltage (B+) to the Powertrain Control Module. It is energized in RUN or START
through the ignition switch; when energized, B+ flows through the relay to power the PCM and its
outputs, and at key OFF the relay de-energizes and removes B+ from the PCM.

Beyond simply powering the computer, the relay provides reverse battery protection for the PCM and
its related actuator assemblies — guarding the expensive control module if the battery is ever
connected backwards. Because it gates power to the whole control system, a failed PCM power relay
mimics a dead computer, which is why the FSM points its pinpoint test to "B - Vehicle Battery" at
the system level. This relay is a central node in the `electrical-body` distribution and the
`electrical-starting` run circuit.

## Related Concepts

- [[notes/rly-pcm-power-relay-uses-a-separate-external-diode-not-an-internal-one|The PCM power relay is an SPDT relay with no internal diode and relies on a separate external diode]]
- [[notes/rly-eec-power-relay-feeds-the-fuel-pump-relay-coil|Power to the fuel pump relay comes from the EEC power relay through the PCM and the inertia switch]]
- [[notes/rly-fuel-pump-relay-is-grounded-by-the-pcm-not-a-simple-switch|The fuel pump relay is grounded by the PCM, so its ground circuit is the real no-start clue]]

## Source

- [[sources/rly-pcm-power-main-relay|Main Relay (Computer/Fuel System) / PCM Power Relay — Description and Operation (FSM)]]
