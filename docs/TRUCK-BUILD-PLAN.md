# Whole-truck reconstruction

The target is the complete 1994 F-150 XLT SuperCab, 2WD, 4.9L, M5OD-R2: an
assembly of individually explorable physical parts with operation and diagnostic
explanations. The engine is the first branch, not the project boundary.

## Current working surface

`/viewer/` now navigates 15 systems and 3,628 indexed factory reference pages.
`inventory/truck/systems.json` retains their local paths, public URLs and hashes.
The old `inventory/bom.json` contains archived prototype completion flags; these
are not accepted as evidence that components exist in the new reconstruction.
Manual pages can discuss multiple options, even within this vehicle archive.
Explicit automatic transmission, transfer case and ZF branches are excluded from
the transmission entry; remaining references still require applicability review.

Engine atlas: 119 reusable definitions / 551 individual occurrences. A damper
hub, elastomer and inertia ring have been added with sourced overall dimensions.
The internal sections, bore and engine position remain provisional. The catalog
is evidence for a replacement part, not identification of the installed part.

## Work sequence and shared interfaces

1. Engine: reconcile measured replacement dimensions with the provisional block,
   head and valvetrain datums; finish cooling, ignition, accessory drive and hardware.
2. Clutch and M5OD-R2: build the clutch, input/counter/output shafts, bearings,
   gear pairs, synchronizers, shift mechanism and case as independent components.
   Establish crank flange, pilot, input-shaft and bellhousing interfaces first.
3. Driveshaft and rear axle: establish transmission-output, universal-joint and
   pinion interfaces; confirm axle identity/ratio before selecting ring/pinion data.
4. Frame, steering, suspension and brakes: establish common frame stations, hubs,
   wheel axes and mounting interfaces. Confirm wheelbase and bed configuration
   before assembling a supposedly dimensionally accurate chassis.
5. Body, cabin, fuel tanks, cooling pack, exhaust, HVAC and electrical systems:
   connect each to established structural and mechanical interfaces. Route hoses,
   pipes and harnesses as separate parts with sourced terminals and connections.

Every branch uses stable part identities, millimeter CAD, reusable definitions,
individual occurrences, source records, explicit assumptions, and scale/interface
validation. Counts are not completion percentages. A catalog kit is not a full
physical BOM. A teaching section of a sealed part is labeled as such.

## Acquisition currently pending

See `inventory/truck/acquisition.json`. One D21940 EVTM eBook is in the
FordManuals browser cart ($21.95 before applicable tax). No payment submitted.
Exact-year PC/ED listing is $129.98 before shipping/tax, used print. Budget approval
is pending; neither complete manual has been acquired. Continue available work
without waiting for these purchases. Once acquired, retain original bytes and
hashes, inspect model/year coverage, extract and ingest, then link usable sections.

## Validation for this increment

- Engine STEP solids, exported GLB bounds and all static assembly pairs passed.
- Combined damper envelope matches published replacement dimensions.
- Navigation test reaches all 551 occurrences through 658 distinct links.
- Browser verified damper isolation/explosion and local transmission reference search.
- This does not establish casting accuracy, fitted-part identity or truck completion.
