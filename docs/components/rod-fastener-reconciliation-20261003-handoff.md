# Rod-fastener replacement evidence handoff

## Contract and outcome

Research follow-up for engine #21/#22; root integration owner. Baseline `1ba1593ba3509c1378a4e6fa08e44070f558e866`, branch `engine/functional-fit-20261003`. Scope and ownership: `rod-fastener-reconciliation-20261003*` files only; no shared CAD, inventory, Git, KB or browser edits. Part/occurrence IDs, millimeter units, rod journal/pin/bearing datums, rod length and corrected motion remain unchanged. Existing five-group architecture contract is `docs/components/rod-fastener-architecture-contract.md`.

**Public manufacturer evidence now supports a 3/8-24 replacement thread and 9/16-inch replacement nut hex for a Ford 4.9L truck application covering 1994. It does not yet support a complete paired bolt/rod-seat reconstruction or resolution of the six inherited motion conflicts.** No geometry changed and no conflict is newly claimed passed.

## Evidence ledger

| Claim | Evidence and exact location | Applicability / limitation |
|---|---|---|
| Dorman bolt 635-027 and nut 635-002 | Dorman-authored [AutoGrade catalog](https://images.carid.com/dorman/info/pdf/dorman-auto-grade-catalog.pdf), PDF page 578 / printed 352, right column Ford Truck L6 4.9L (300 CID), row 1994–65 | Manufacturer replacement application explicitly covers 1994. It supplies no VIN-specific qualifier or owner-installed identity. Adjacent 1996–95 row has a dash for bolt but the same nut. |
| Nut 635-002: Type 2, 3/8-24 thread, 9/16-inch hex; Ford C9AZ-6212-B OE cross | Same catalog PDF page 576 / printed 350, Connecting Rod Nuts table | Published replacement nominal values; height, chamfer dimensions and bearing footprint absent. Actual type-2 illustration is hexagonal and chamfered; no dimensions can be inferred from its perspective sketch. |
| Current manufacturer nut description agrees | [Dorman 635-002 product page](https://www.dormanproducts.com/p-3711-635-002.aspx), reviewed 2026-10-03 | Primary corroboration of thread and hex. Broad year range alone is not the exact application proof; that comes from the older application table. Current OE cross section omits Ford. |
| E3TZ-6200-E rod, C9AZ-6212-B nut 3/8-24, C4OZ-6214-B bolt | Ford Power Products April 1993 [CSG649/CSG649P catalog](https://generator-info.com/Engine%20Manuals/Ford/194-203%20Ford%20CSG649%20CSG649P%20300CID%20Parts%20manual%20%28Apr1993%29.pdf), PDF and printed page 7, refs 4–6 | Previously indexed lead is now actually visually verified. Industrial analogy, not proof of the individual bolt inside the 1994 service rod E3TZ6200ERM. |
| ARP 152-6002 style M applies to 4.9L inline six; 152-6001 style G separately covers 240–300 | [2026 ARP page 49](https://arpcatalog.com/49/) | Family replacement application; style letters edition-bound. Earlier actual 2019 style-M photo review already exists in `reference/engine/online-rod-research.json`; do not repeat older claim that no photo was obtained. |
| Generic ARP dimensioned table cannot fill this gap | [2026 ARP page 43](https://arpcatalog.com/43/) | SAE aftermarket rod-bolt table gives seven dimensional columns, but neither applicable kit is listed. No identified individual-bolt cross-reference permits transfer. |

Dorman PDF SHA256: `2a6a6e148e4ab98553ad700b9e680cb243c3b3668e635506323071dda1124f5f`. Ford 1993 PDF SHA256: `e9ff1a3aeb3d5e580c599c88d07ee8b0f6ea187bd2290e0a2d4d359b740ba1b6`. Actual Dorman pages 576/578 and Ford page 7 were rendered and inspected; raw PDFs/manufacturer pixels are excluded from delivery. The ledger includes retrieval failures rather than treating challenge pages as source content.

## Numerical interface proposal for root review

Adopt these only as scoped replacement-reference constraints in a future paired fastener/rod-seat candidate:

| Parameter | Supported nominal / conversion | Existing estimate | Consequence |
|---|---:|---:|---|
| Mating thread size | 3/8-24; nominal diameter 9.525 mm, pitch 1.058333 mm | Smooth 8 mm shank; no thread | Nominal thread size increases 1.525 mm. It is **not** a press-shoulder diameter or a drill size. |
| Nut across flats | 9/16 inch = 14.2875 mm | 12.124356 mm from regular hex circumradius 7 mm | Replacement hex is 2.163144 mm wider across flats. No shrinking is supported. |
| Regular-hex construction radius | Derived 8.248892 mm | 7 mm | Construction aid only; actual corner/chamfer envelope still unknown. |

Do not build a nominal 9.525-mm cylinder into an assumed bore and call it press-fit. The shoulder, fit allowance, engagement length, radius relief and rod seating surface still need dimensions. Do not alter the existing 6-mm nut height, 5-mm head height, seat Z22, bolt centers Y±34.5 or 14×44-mm bosses based on this evidence. A wider replacement nut also requires its own tool-access/contact review; it does not repair the bolt-head witness.

The inherited witness is on the estimated head near local Z26.592894 at local 55°, crank radius 98.179965 mm versus the estimated R98 cavity. New thread and nut evidence neither establishes the head envelope nor validates the block cavity. Preserve the frozen diagnostic and original failure controls.

## What remains unresolved

| Existing required capture group | New progress | Still required before a coherent correction |
|---|---|---|
| Head plan and orthogonal elevations | Known qualitative ARP style M comparison retained | Applicable head outline, clocking and height |
| Bolt head and rod seat together | ARP press-fit/chamfer architecture retained | Under-head radius, seat Z, bearing footprint |
| Press/grip/thread/nut stack | Replacement thread and nut hex now supported | Press diameter/length, grip/thread lengths, cap hole, nut height/plane |
| Rod shoulders and bolt centers | Ford industrial component-number linkage verified | Datum-linked centers, boss contours and edge distances |
| Block section near witness | No new dimensional evidence | Actual crankcase contour tied to crank axis/cylinder station |

Specific false substitutions excluded: Dorman 635-025 / Ford C9AZ-6214-B is not Dorman 635-027 / Ford C4OZ-6214-B. The dimensioned 635-025 row on page 576 cannot be assigned to 635-027. Generic retailer engine-filter pages include 16-bolt/8-rod listings despite a six-cylinder title, so their E6TZ/E8AZ entries do not prove an exact six-cylinder bolt identity. Historical Ford C4OZ length found in an index was not raster-verified and is not adopted. No applicable public STEP or full 152-6002/635-027 dimensioned drawing emerged from this focused search; that is not proof none exists.

## Delivery and reproduction

Readiness: partial research evidence, not integration-ready geometry. Commit/PR/release: root-managed; no CAD exports or asset release needed. Parametric CAD API: N/A. Authored entry point:

```sh
python3 scripts/engine/rod-fastener-reconciliation-20261003.py
python3 -m py_compile scripts/engine/rod-fastener-reconciliation-20261003.py
```

Python 3.13.12, macOS, standard library only. Output `reference/engine/rod-fastener-reconciliation-20261003-report.json` records eight current input hashes, source hashes/locations, calculations, exclusions and exact next actions. Source retrieval/raster review needs public downloads plus `pdftoppm`; normalized PDF extraction used available bundled pypdf. No temporary file is needed to rerun the arithmetic. Purchased/manual source pixels remain excluded. Model/effort and usage unavailable.

## Validation and review

| Gate | Status / method |
|---|---|
| Application/coverage | PASS for Dorman replacement application; exact original bolt identity remains UNKNOWN |
| Dimensions/coordinates | PARTIAL: two nominal dimensions plus thread pitch; remaining coupled dimensions UNKNOWN |
| Source/visual comparison | PASS for three newly reviewed table pages; no source-scaled CAD silhouette claim |
| CAD/export | N/A research-only |
| Installed interfaces and motion | Existing FAIL unresolved; no new sweep run or implied pass |
| Motion/disassembly/tool access | NOT RUN for proposed replacement dimensions; no candidate geometry |
| Learning/diagnostics | PASS: source scope and numeric consequences documented |
| Browser integration | N/A research-only |
| Reproduction/review | Worker script and syntax PASS; independent root source review pending |

## Tracking and exact next actions

Root can retain these scoped thread/hex claims and link this handoff from the existing unresolved architecture audit. Next evidence target is the archived Dorman 635-027 engineering/dimensional sheet or ARP 152-6002 drawing identifying individual bolt and nut numbers, with press shoulder and paired seat dimensions. A Ford exact-year individual bolt listing would strengthen OEM identity separately. Do not request owner measurements as the only route, substitute a generic cap screw, or perform a clearance-only block cut. No process remains running; root owns issue status and any future geometry contract.
