---
title: "The CHECK ENGINE message signals the EEC-IV has entered a backup (FMEM) operating strategy"
kind: how-it-works
source: "[[sources/ipc-malfunction-indicator-lamp|Malfunction Indicator Lamp (Check Engine) — Description and Operation (FSM)]]"
related:
  - "[[notes/ipc-charge-lamp-grounds-through-regulator-terminal-1|The charge lamp lights because the regulator grounds it through terminal 1 until the S-circuit voltage is reached]]"
tags:
  - malfunction-indicator-lamp
  - check-engine
  - eec-iv
  - warning-indicators
---

The Malfunction Indicator Lamp (MIL) / "CHECK ENGINE" warning on the 1994 F-150 is driven by
the EEC-IV system and means something specific: the Powertrain Control Module (PCM) has
switched to an alternate operating strategy called Failure Modes Effect Management (FMEM).
FMEM is the engine computer running on substitute values because an input has failed, so a
lit MIL is the truck telling you it is limping on backup logic. The PCM sends the message to
the message center through the Data Link Connector (DLC), and the MIL doubles as the device
that flashes service codes during self-test.

The alerting behavior is distinctive: on entering FMEM the "CHECK ENGINE" message appears
with a one-second tone every five seconds, and that tone is suppressed after one minute. The
message also displays during Hardware Limited Operating Strategy (HLOS), an even more
degraded fallback, and a "CHECK DLC" message may accompany it. So MIL diagnosis belongs with
the EEC-IV/powertrain system, even though the lamp itself lives in the `interior` cluster and
`electrical-body` wiring.

## Related Concepts

- [[notes/ipc-charge-lamp-grounds-through-regulator-terminal-1|The charge lamp lights because the regulator grounds it through terminal 1 until the S-circuit voltage is reached]]
- [[notes/ipc-oil-pressure-lamp-is-ground-switched-by-the-engine-unit|The oil pressure warning lamp is ground-switched by an engine-mounted pressure switch]]

## Source

- [[sources/ipc-malfunction-indicator-lamp|Malfunction Indicator Lamp (Check Engine) — Description and Operation (FSM)]]
