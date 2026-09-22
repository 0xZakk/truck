---
title: "Generic parts-store scanners may report no codes on an EEC-IV truck, so read the codes off the flashing check-engine lamp"
kind: how-it-works
source: "[[sources/yt-fix-egr-valve-issues-on-your-f150-1986-1995-diy-tr|Fix EGR Valve Issues on Your F150 (1986-1995) | DIY Troubleshooting Guide for Code 332]]"
related:
  - "[[notes/dtc-111-is-system-pass-not-a-fault|DTC 111 means System Pass — the self-test found no faults]]"
tags:
  - dtc
  - eec-iv
  - diagnosis
  - how-it-works
---

The 1994 F-150's EEC-IV system pre-dates the OBD-II standard, so the generic code readers used
at many auto-parts stores may not communicate with it. In the video the store's scanner returned
"no codes" and claimed the check-engine light shouldn't be on, even though the lamp was clearly
lit. The correct method on these trucks is the on-board self-test, which flashes the two-digit
trouble codes on the check-engine lamp; reading those flashes is how the presenter recovered the
real code (332).

The takeaway for diagnosing the `engine` management system is not to trust a parts-store "no
codes" result on an EEC-IV truck — use the flash-code self-test (or an EEC-IV-capable tool) to
pull stored codes. The procedure for triggering and counting the flashes is covered separately;
this note's point is simply that the older system needs its own read method, and a generic OBD-II
reader giving "no codes" does not mean the truck is fault-free.

## Related Concepts

- [[notes/dtc-111-is-system-pass-not-a-fault|DTC 111 means System Pass — the self-test found no faults]]

## Source

- [[sources/yt-fix-egr-valve-issues-on-your-f150-1986-1995-diy-tr|Fix EGR Valve Issues on Your F150 (1986-1995) | DIY Troubleshooting Guide for Code 332]]
