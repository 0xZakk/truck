---
title: "The belt mismatch requires accessory datum reconciliation"
date: 2026-09-25
status: candidates-rejected
---

Three new accessory-layout candidates were developed and checked against installed STEP geometry. None is ready to install. A numerical 2,491 mm route can clear the engine but contradict the Ford arrangement; preserving the arrangement exposes the coolant-outlet obstruction. The work narrows the problem to actual accessory stations, pulley reference diameters and the outlet/upper-belt corridor rather than an adjustable belt length.

## Verified diagnostic

The existing seven-pulley construction stations produce a 2,785.401 mm path when outside radii are treated as effective radii, versus the Gates K060980 / 6PK2491 catalog effective length of 2,491 mm. These radius conventions differ: this discrepancy is not a replacement-belt recommendation.

Sampling the provisional tensioner's entire 360° circle at 0.1° increments produces a minimum path of 2,768.158 mm. Removing the tensioner constraint entirely gives the same relaxed-route length, still 277.158 mm above the catalog value. Full rotation and bypassing the tensioner are diagnostic devices, not allowable installed configurations. The existing assumed cord-profile correction adds 19.473 mm; it does not explain away the roughly 294 mm discrepancy.

## Rejected experiments

| Candidate module | Exact checks | Outcome |
|---|---:|---|
| `accessory_layout_candidate.py` | 148 | 44 overlaps. Upper-only relocation matches nominal diagnostic length but intersects intake, outlet and old supports. Original groove conflicts retained. |
| `accessory_layout_constrained.py` | 136 | 14 old-support overlaps; no other reported engine/belt obstruction. Still rejected: nominal-length solution puts tensioner above P/S and A/C above W/P, contradicting the schematic. |
| `accessory_layout_evidence.py` | 180 | 18 overlaps: 17 old-support conflicts plus belt/outlet intersection of 328.460 mm³. Qualitative ordering preserved; loop remains 2,658.324 mm. |

Each has a dedicated `scripts/check-accessory-layout-*.py` checker and `inventory/engine/accessory-layout-*.json` report. Candidate checks freeze the installed manifest and geometry-module bytes; STEP round trips and intersections use the existing 0.01 mm³ overlap threshold. Later candidates normalize the five pulley groove bands using the existing PK comparison adapter locally. Their fixed normalized crank-pulley geometry still requires full installed-neighbor QC before any integration.

The source-ordered candidate's rigid group displacements, in CAD Y/Z mm, are ALT `(0,-80)`, P/S `(-60,+10)`, A/C `(+30,+60)`, Thermactor `(-50,+60)`, tensioner `(+100,-20)`. Crank and water pump stay fixed. These are **numerical hypotheses, not measured factory locations**. Existing supports are deliberately kept in the checks: their conflicts are recorded rather than waived. All mounts, engine feet and affected connections would require redesign and verification.

## Source ordering and owner photographs

Re-viewing the Ford with-A/C schematic establishes P/S above the tensioner, tensioner above ALT, tensioner on the P/S side of the centerline, and A/C below W/P. The engine photographs show the installed accessory hardware but obscure pulley centers and contain perspective distortion. They cannot certify a 115 mm compressor relocation or supply calibrated centers. `reference/engine/accessory-layout-source-review.json` records the reviewed files and hashes. No dimensions were scaled from the schematic.

Conservative mesh-bound station screening and discrete search are reproducible with `scripts/search-accessory-layout-bounds.py` then `scripts/search-accessory-layout-evidence.py`. The search is bounded to ±120 mm at 10 mm spacing and is **not a global optimum proof**; bounding boxes can reject a geometrically viable curved-body position. Exact CAD checks remain necessary.

## Targeted outlet refinement

Keeping the other source-ordered stations fixed and raising ALT from −80 mm toward its original elevation reduces the outlet collision but grows the belt loop again. At original ALT elevation the overlap is still 1.726 mm³ and the diagnostic length is 2,743.421 mm. At +4 mm elevation—just below the provisional tensioner—the overlap is 0.0969 mm³ and length 2,748.096 mm. This still fails the unchanged 0.01 mm³ threshold. `scripts/check-accessory-layout-outlet-refinement.py` saves the exact local sweep; it is not a whole-assembly audit.

## Path to integration

1. Establish engine-to-bracket and bracket-to-accessory stations from a dimensioned drawing or calibrated reference. Prioritize P/S/tensioner registration and the ALT–tensioner span passing the coolant outlet.
2. Verify pulley effective/gauge diameters, belt plane and tensioner working range. The source catalog length alone does not determine a unique layout.
3. Reconstruct shared P/S–A/C and alternator supports around the supported stations, including actual mounting load paths and hose/pipe interfaces. Independently moving P/S relative to A/C precludes simply translating their shared bracket.
4. Repeat exact body checks, belt/outlet clearance and sampled physical tensioner travel, then whole-engine integration checks. Do not install any of the rejected configurations merely because its length matches a catalog number.

Existing reviewed source records are `reference/engine/gates-1994-drive-reviewed.json`, `reference/engine/ford-accessory-routing-reviewed.json`, and `reference/engine/pk-belt-profile-reviewed.json`. No builder, installed geometry, manifest or viewer file was changed by this study.
