---
title: "Switch-input DTCs often just mean the truck was not staged correctly — in gear, A/C on, or brake not pressed"
kind: troubleshooting
source: "[[sources/dtc-idle-speed-input-codes|EEC DTCs 411-539 — Idle Speed, Vehicle Speed, and Switch Input Codes (FSM)]]"
related:
  - "[[notes/dtc-411-and-412-mean-the-pcm-cannot-control-idle-rpm|DTCs 411 and 412 mean the PCM could not control idle RPM during the KOER self-test]]"
  - "[[notes/dtc-hard-codes-vs-memory-codes-mean-present-vs-stored|A hard code is a fault present during the test, while a memory code was stored from earlier driving]]"
tags:
  - dtc
  - park-neutral
  - brake-switch
  - power-steering
  - troubleshooting
---

Several self-test codes are not component failures at all but operator-staging errors. The
EEC expects the truck set up a particular way before it runs: transmission in Park or Neutral,
A/C and defrost off, brake pedal released until prompted. If those conditions are wrong, the
test reports it as a code. DTC 522 means "vehicle not in PARK or NEUTRAL during KOEO, or
Park/Neutral switch circuit open"; 525 means "vehicle in gear or A/C on during self-test";
527 means "Park/Neutral switch circuit open or A/C on"; and 539 means "A/C or defrost ON
during self-test." DTC 536 is the brake on/off switch not actuated during the KOER test —
the test asks you to tap the brake and 536 sets if it never sees it.

The practical lesson is to re-run the self-test with the truck staged correctly before
condemning a switch. Only if the code persists with everything in the right state does it
become a real circuit fault. The same logic applies to the power-steering pressure switch
codes 519 (circuit open at KOEO) and 521 (did not change states during KOER, meaning you may
not have turned the wheel when prompted), and to clutch-pedal code 528.

These straddle the truck's `engine` and chassis inputs; mis-staging is the most common reason
they appear.

## Related Concepts

- [[notes/dtc-411-and-412-mean-the-pcm-cannot-control-idle-rpm|DTCs 411 and 412 mean the PCM could not control idle RPM during the KOER self-test]]
- [[notes/dtc-hard-codes-vs-memory-codes-mean-present-vs-stored|A hard code is a fault present during the test, while a memory code was stored from earlier driving]]
- [[notes/dtc-self-test-runs-in-koeo-and-koer-modes|The EEC self-test runs in two modes — Key On Engine Off and Key On Engine Running — and each finds different faults]]

## Source

- [[sources/dtc-idle-speed-input-codes|EEC DTCs 411-539 — Idle Speed, Vehicle Speed, and Switch Input Codes (FSM)]]
