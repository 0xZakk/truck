---
title: "1994 Ford F-150 Knowledge Base"
---

A knowledge base for a **1994 Ford F-150 XLT SuperCab** (2WD, 4.9L / 300 cu in inline-six,
M5OD-R2 5-speed). It collects sources — the factory service manual, the owner's guide,
brochures, forum threads, and videos — and distills them into atomic, cross-linked notes
on how each system works and how to diagnose and fix it. It feeds the truck project's
larger goal: an interactive "every system → every part" model with how-it-works and
common-issues walkthroughs.

## Maps

One entry point per system (seeded from `inventory/systems.json`):

- [[maps/engine|Engine (4.9L I6)]]
- [[maps/fuel|Fuel system]]
- [[maps/ignition|Ignition system]]
- [[maps/cooling|Cooling]]
- [[maps/intake-exhaust|Intake & exhaust]]
- [[maps/driveline|Transmission & driveline]]
- [[maps/rear-axle|Rear axle & differential]]
- [[maps/suspension|Suspension]]
- [[maps/steering|Steering]]
- [[maps/brakes|Brakes]]
- [[maps/wheels-tires|Wheels & tires]]
- [[maps/electrical-starting|Starting system]]
- [[maps/electrical-charging|Charging system]]
- [[maps/electrical-body|Body electrical & lighting]]
- [[maps/hvac|Heating & A/C]]
- [[maps/frame-chassis|Frame & chassis]]
- [[maps/body-cab|Cab & body]]
- [[maps/body-bed|Bed & box]]
- [[maps/exterior-trim|Exterior trim & hardware]]
- [[maps/interior|Interior]]
- [[maps/glass|Glass]]

## How this KB is built

- **sources/** — one page per ingested item (manual sections, owner's guide, forum threads, videos)
- **notes/** — atomic notes, one idea each, cross-linked; each tagged with a `kind`
  (`how-it-works`, `troubleshooting`, `procedure`, `spec`, `concept`)
- **maps/** — the curated system overviews above

Built and maintained with the kb-toolkit skills: `kb-add-source`, `kb-process`, `kb-explore`.
Notes reference truck `inventory/` system and part ids where useful, so the viewer/app can
join the KB to the 3D model.
