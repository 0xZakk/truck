---
title: "An EGR code 332 can be caused by a vacuum leak in the EGR control plumbing, not a failed EGR valve"
kind: troubleshooting
source: "[[sources/yt-fix-egr-valve-issues-on-your-f150-1986-1995-diy-tr|Fix EGR Valve Issues on Your F150 (1986-1995) | DIY Troubleshooting Guide for Code 332]]"
related:
  - "[[notes/dtc-egr-codes-split-by-pressure-sensor-vs-position-sensor|EGR DTCs split into two families depending on whether the truck uses a pressure (PFE) or position (EVP) feedback sensor]]"
tags:
  - egr
  - dtc
  - code-332
  - vacuum
  - troubleshooting
---

EGR code 332 indicates insufficient EGR flow — the EEC commanded the valve to open but the
feedback sensor never saw it move. On this 1994 F-150 the EGR valve is opened by engine vacuum
routed through a control solenoid, so a broken or leaking vacuum line in that plumbing will
prevent the valve from opening and set 332 even though the valve and solenoid themselves are
fine. In the video the actual fault was a cracked vacuum hose hidden under a heat shield,
upstream of the solenoid, and the fix was a cheap plastic splice union rather than any new
emissions part.

The practical lesson for the `engine` emissions hardware is to chase the vacuum supply before
condemning the EGR valve or solenoid. Confirm whether vacuum is even reaching the valve, then
work backward toward the source; a no-vacuum reading at the valve does not by itself prove the
valve is bad. Pay attention to hoses tucked behind heat shields and other hard-to-see spots,
because that is exactly where an older rubber/plastic vacuum line tends to crack.

Note the FSM treats 332 as an insufficient-flow code common to both the pressure-sensor (PFE)
and position-sensor (EVP) EGR variants, so 332 points at flow rather than at a specific sensor
circuit — consistent with the video's vacuum-leak finding.

## Related Concepts

- [[notes/dtc-egr-codes-split-by-pressure-sensor-vs-position-sensor|EGR DTCs split into two families depending on whether the truck uses a pressure (PFE) or position (EVP) feedback sensor]]

## Source

- [[sources/yt-fix-egr-valve-issues-on-your-f150-1986-1995-diy-tr|Fix EGR Valve Issues on Your F150 (1986-1995) | DIY Troubleshooting Guide for Code 332]]
