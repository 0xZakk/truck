---
title: "A fuel pump that runs continuously at key-on instead of cycling off points toward the PCM"
kind: troubleshooting
source: "[[sources/yt-ford-49l-crankno-start-issue-solved-1994-f-250-49l|Ford 4.9l Crank/No Start Issue SOLVED (1994 F-250 4.9l)]]"
related:
  - "[[notes/eec-fuel-pump-runs-12s-at-key-on-then-needs-an-rpm-signal|The fuel pump runs 1-2 s at key-on, then the PCM keeps it running only with an rpm signal above 120]]"
tags:
  - fuel-pump
  - pcm
  - no-start
  - troubleshooting
  - fuel
---

On a healthy EEC-IV 4.9L the `fuel` pump runs only a short prime burst at key-on (about 1-2
seconds) and then the PCM opens the fuel-pump-relay ground until it sees an rpm signal from
cranking. In this video the owner's key clue to a failing PCM was the opposite behavior: at
key-on the pump **never cycled off after priming — it just kept running**. Because the PCM is
what times that prime pulse and gates the relay ground, a pump that won't stop cycling/priming
on its own implicates the control module rather than the pump, relay, or inertia switch.

He pairs this with a second telltale — an intermittent check-engine light — and treats the two
together as the signature of a marginal PCM. The practical takeaway for diagnosis: don't read
"pump runs" as proof the fuel side is fine; whether the pump **stops** when it should is itself
a diagnostic signal. He also speculates that the constantly-running pump cooked his earlier
replacement pump, since a pump left energized continuously runs hot.

## Related Concepts

- [[notes/eec-fuel-pump-runs-12s-at-key-on-then-needs-an-rpm-signal|The fuel pump runs 1-2 s at key-on, then the PCM keeps it running only with an rpm signal above 120]]
- [[notes/rly-pcm-power-relay-supplies-bplus-and-gives-reverse-battery-protection|The PCM power relay supplies B+ to the PCM and protects it against reverse battery polarity]]

## Source

- [[sources/yt-ford-49l-crankno-start-issue-solved-1994-f-250-49l|Ford 4.9l Crank/No Start Issue SOLVED (1994 F-250 4.9l)]]
