---
title: "Idle speed is PCM-controlled — don't back off the throttle-plate stop screw"
kind: troubleshooting
source: "[[sources/eng-valve-clearance-and-idle|Valve Clearance & Idle Speed — Adjustment Procedures and Specs (FSM)]]"
related:
  - "[[notes/eng-adjust-valve-clearance-by-changing-pushrod-length|Adjust 4.9L valve clearance by changing pushrod length, in firing order]]"
tags:
  - engine
  - idle-speed
  - throttle-body
  - troubleshooting
---

On the 4.9L there is no conventional idle-adjustment screw to chase. Curb and fast idle are
controlled by the PCM acting through the Idle Air Control-Bypass Air (IAC-BPA) valve, which is not
adjustable. The throttle body uses a "sludge-tolerant" design with an orifice in the throttle plate
to meter idle air, marked by a yellow/black decal. That decal warns the throttle-plate stop screw
must never be backed off counterclockwise — doing so won't lower engine speed and may make the
plate stick in the bore — and the bore must not be cleaned, as cleaning ruins a sensitive coating.

So a rough or wrong idle is almost always a symptom of something else, and the FSM lists what to
fix first on the `engine` inventory system: contamination in the idle-control device, a too-rich or
too-lean fuel condition, sticking/binding throttle, an engine not at operating temperature,
incorrect ignition timing, a clogged PCV, or vacuum leaks. Actually setting base idle then requires
a scan tool and the engine-running Self-Test.

> "The curb and fast idle speeds are controlled by the Powertrain Control Module (PCM) and the Idle
> Air Control-Bypass Air (IAC-BPA) valve. The IAC-BPA valve is not adjustable. ... the throttle plate
> stop screw must not be adjusted counterclockwise (backed off)."

## Related Concepts

- [[notes/eng-adjust-valve-clearance-by-changing-pushrod-length|Adjust 4.9L valve clearance by changing pushrod length, in firing order]]
- [[notes/eec-iac-meters-air-around-the-throttle-plate-via-pcm-duty-cycle|The IAC valve sets idle by metering air around the throttle plate via a PCM-controlled duty cycle]]
- [[notes/unplugging-iac-while-idling-tests-the-idle-air-circuit|Unplugging the IAC while idling tests whether the idle-air circuit is involved]]
- [[notes/dtc-411-and-412-mean-the-pcm-cannot-control-idle-rpm|DTCs 411 and 412 mean the PCM could not control idle RPM during the KOER self-test]]

## Source

- [[sources/eng-valve-clearance-and-idle|Valve Clearance & Idle Speed — Adjustment Procedures and Specs (FSM)]]
