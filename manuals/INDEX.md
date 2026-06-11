# Manuals Catalog — 1994 Ford F-150 XLT SuperCab (4.9L I6, 5-speed, 2WD)

This folder holds the reference library for the truck. Everything here was sourced
from free/legitimate locations. Copyrighted manuals that cannot be freely downloaded
(Haynes, Chilton) are listed at the bottom with where to buy or borrow them.

## The truck
- **Year/Model:** 1994 Ford F-150 XLT, SuperCab (extended cab)
- **Engine:** 4.9L (300 cu in) inline-six — the legendary, near-bulletproof Ford "300 Six"
- **Transmission:** 5-speed manual (Mazda M5OD-R2 in this application)
- **Drivetrain:** 2WD (rear-wheel drive)
- **Color:** White
- **Generation:** 9th-gen F-Series, the 1992–1996 "OBS" (Old Body Style) trucks

---

## What's here

### 1. `factory-service-manual/` — ⭐ THE primary mechanic-grade resource
**Complete digitized Ford factory service manual for the exact vehicle:**
`1994 Ford F 150 2WD Pickup L6-300 4.9L`.
Source: [Operation CHARM](https://charm.li) (`charm.li`), free offline bundle.

This is ~12,100 HTML pages + ~2,150 diagram images (125 MB). Open
`factory-service-manual/1994 Ford F 150 2WD Pickup L6-300 4.9L/index.html`
in a browser to read it. It is split into **Repair and Diagnosis** and
**Parts and Labor**. Repair-and-Diagnosis sections (page counts):

| Section | Pages | Section | Pages |
|---|---|---|---|
| Powertrain Management | 2614 | Transmission and Drivetrain | 1005 |
| Brakes and Traction Control | 827 | Technical Service Bulletins | 704 |
| Maintenance | 606 | Body and Frame | 573 |
| Sensors and Switches | 433 | Engine, Cooling and Exhaust | 392 |
| Starting and Charging | 384 | Restraints and Safety Systems | 371 |
| Steering and Suspension | 335 | Diagrams (wiring) | 310 |
| Heating and Air Conditioning | 224 | Power and Ground Distribution | 209 |
| Accessories and Optional Equipment | 206 | Instrument Panel / Gauges | 182 |
| Cruise Control | 180 | Lighting and Horns | 175 |
| Specifications | 155 | Relays and Modules | 142 |
| Windows and Glass | 55 | Wiper and Washer Systems | 48 |
| Locations | 16 | All Diagnostic Trouble Codes (DTC) | 15 |

**This single resource covers engine, wiring/electrical (EVTM-equivalent),
diagnostic trouble codes, torque specs, fluid specs, and TSBs** — which is why
there are no separate `engine/` or `wiring/` folders; it would be duplication.

### 2. `owners-manual/` — glovebox owner guide
`1996-Ford-F-Series-Owner-Guide-(same-gen-as-1994).pdf` — official Ford owner
guide, 401 pages. Source: Ford's content server (`fordservicecontent.com`).
Ford only hosts owner guides back to 1996; the 1996 F-Series is the **same
1992–1996 generation** as the '94, so controls, maintenance schedule, fluid
capacities, and dashboard layout match closely. (Minor caveat: 1996 added some
emissions/OBD-II content the '94 lacks — trust the factory service manual over
this guide for anything engine-management-specific.)

### 3. `brochures/` — period sales literature (learning/context)
- `1994-Ford-Trucks-Sales-Brochure.pdf` — full 1994 Ford truck lineup
- `1994-Ford-Pickups-Chassis-Brochure.pdf` — pickups & chassis specs/options

Source: `xr793.com` (Ford literature archive). Good for understanding factory
options, trims, and how the F-150 was positioned — not for repair.

---

## Copyrighted manuals — buy or borrow (not downloaded here)

These are excellent DIY companions but are under copyright, so they aren't
included as files:

- **Haynes Repair Manual #36058** — *Ford Pickups & Bronco 1980–1996*. The classic
  DIY-hobbyist manual; clearer step-by-step photos than the factory manual. Buy
  from Haynes, Amazon, or any parts store (~$30).
- **Chilton Ford Full-Size Trucks 1987–1996** — borrowable for free (14-day
  digital loan, in-browser, DRM-protected) at the Internet Archive:
  https://archive.org/details/chiltonsfordfull0000unse_s7g2

---

## Other useful free references (web, not archived here)
- **Ford Truck Enthusiasts (FTE)** — `ford-trucks.com/forums` — the OBS-truck
  community; deep knowledge on the 300 I6.
- **Bullnose Garage** — enthusiast deep-dives on the Ford 300 inline-six.

---

## Where this is going (project vision)
The end goal is a tool/web app to **diagnose issues** and **learn how each system
works**. The factory service manual above is structured, machine-readable HTML —
ideal raw material for that app:
- DTC lookup → `.../Repair and Diagnosis/A L L Diagnostic Trouble Codes ( DTC )/`
- Component locations → `.../Locations/`
- Wiring diagrams → `.../Diagrams/` and `.../Power and Ground Distribution/`
- Torque/fluid specs → `.../Specifications/`

See the repo-root `README.md` for the build plan.
