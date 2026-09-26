# Engine reference research — September 23, 2026

For the 1994 F-150 XLT SuperCab, 2WD, 4.9L inline-six, M5OD-R2.

This round found useful dimensional data, exact Ford publication identifiers and
manufacturer-confirmed replacement part numbers. These can improve the engine
without requiring a full dimensional survey first. They do not yet supply a
complete production drawing set or identify every part installed in this truck.

## Saved results

- [17-source acquisition ledger](../inventory/engine/research-2026-09-23.json): URLs, original-file hashes, review findings, applicability and limitations.
- [10 specification groups](../inventory/engine/replacement-specs-2026-09-23.json): part numbers, values, units and one-based PDF page locators.
- [27 Melling application entries](../inventory/engine/melling-1994-49-applications.json): browser-reviewed manufacturer results with exact vehicle filters and catalog notes.
- Seventeen corresponding `kb/sources/` pages, deliberately `processed: false` pending atomic-note extraction.
- Public PDFs/HTML in `reference/engine/research-2026-09-23/`; normalized text in `kb/.raw/`. These originals remain local and gitignored, matching the existing reference-library pattern. Findings, links, hashes and structured data are versionable.

No geometry changed in this research pass. No paid manuals were purchased.

## Ford publications to add

| Publication | Identified reference | What it adds | Access established |
|---|---|---|---|
| 1994 Bronco/F-Series EVTM | Ford FPS-12128-94; Forel D21940; ISBN 9781603714525 | Wiring, grounds, connector views, component locations and vacuum circuits | [Licensed publisher sample](https://www.forelpublishing.com/demo/Demo21940.pdf), 35 pages, saved; [publisher listing](https://www.forelpublishing.com/clickbank/index.html) offered complete product at $21.95 on research date |
| 1994 Powertrain Control/Emissions Diagnosis | FPS1210694A | EEC-IV truck supplement, Quick Test, pinpoint tests, intermittent-fault diagnosis and emissions systems | [Retailer listing](https://www.auto-repair-manuals.com/Ford-Mercury-Lincoln-1994-Car-Truck-Powertrain-Control-Emission-Diagnosis-Factory-Service-Manual.html) captured; approximately 4,500 pages, $129.98 as listed; complete contents not obtained |
| 1994 truck service manual, two volumes | FPS-12107-94-1 / -2; ISBN 9781791419578 | Mechanical procedures, specifications and system service | [Reprint listing](https://www.tmbbooks.com/en/term_FordUSArep08.html) identifies Detroit Iron 2023 edition, 3,952 pages; acquisition metadata only |
| 1980–89 Ford Master Parts Catalog | FPS8472-A text / FPS8472-B illustrations | Exploded views and part-number interpretation | [251-page publisher sample](https://www.forelpublishing.com/demo/Demo20083.pdf) saved; earlier applications only |

The EVTM sample's contents page identifies 4.9L controls at cell 23, ignition 21,
starting 20, vacuum 140, connector faces 150 and locations 151–152. These are
**full-book section references**, not a claim that the sample contains every
section. Publisher and affiliate listings disagree about total page count
(140 versus 379); verify the actual product scope before acquisition.

The Master Parts Catalog's March 1994 final-issue date does **not** extend its
1980–89 application coverage to this truck. It is comparison material.

The existing CHARM archive remains valuable, including substantial powertrain
and wiring content. The old manuals index overclaimed completeness and
EVTM equivalence; that wording is corrected. A complete exact-year PC/ED PDF
was not confirmed in this round. Buying or borrowing the exact EVTM and PC/ED
would add more value than collecting generic EEC-IV explanations alone.

## Specifications that can improve the model

| Part | Finding | Evidence and modeling limit |
|---|---|---|
| Water pump | Gates **44009** for 1993–96 F-Series 4.9L; Ford **F6TZ8501KB** cross-reference | [Gates catalog](https://cms.gates.com/~/media/Files/Gates/Industrial/Fluid%20Power/Catalogs/Water%20Pump%20Catalog%20Full%20Version.pdf), PDF 55 / printed 35 and PDF 199 / printed 179. Earlier 44007 is a different application. Mounting and hub datums still needed. |
| Damper | Dorman **594-152**, diameter **6.42 in**, width **2.8 in** | [Manufacturer catalog on distributor mirror](https://images.carid.com/dorman/pdf/2006-oes-catalog.pdf), PDF 241 / printed 239. Useful envelope and photo; not bore, keyway or axial-offset geometry. |
| Pushrod | Melling **MPR-306**, **10.140 in** long × **.312 in** diameter, drilled, H&H ends | [Manufacturer table](https://specsearch.melling.com/PDF/Push_Rod_2024-03-18_09-23-05.pdf), PDF 1. Standard-size application confirmed in live lookup. Use illustrated length convention. |
| Camshaft | **SYB-38**: .247-in cam lift, .395-in valve lift, 192° duration at .050, 270° advertised, rocker ratio 1.6 | [Manufacturer table](https://specsearch.melling.com/PDF/Camshaft2024-03-18_09-48-28.pdf), PDF 13. Constrains animation; cannot reconstruct complete lobe curves from these values. |
| Valve heads | **V1504** exhaust 1.559 in; **V1505** intake 1.783 in | [Manufacturer identification chart](https://specsearch.melling.com/PDF/Stock%20Valve%20ID%20Chart%2001192024.pdf), PDF 1 and 4. Application listing contains an anomalous diesel-style exception; reconcile before promotion. |
| Expansion plugs | **MPE-107R** kit decomposes into five MPS-126, one MPC-147, one MPS-59A, two MPP-554 | [Melling guide](https://melling.com/wp-content/uploads/2025/05/2026-plug-catalog.pdf), PDF 10 / printed 8; dimensional tables PDF 3, 7–9. MPS-126 OD is 1.640–1.642 in, height .365 in. Locations and wall sections remain unresolved. |

Melling's [manufacturer application lookup](https://melling.mypartfinder.com/)
confirmed the standard pump M-74, pickup 74-S2, shaft IS-74, lifter JB-900,
rocker MR-710, bolt MRM-1741, bridge MRM-1776, intake spring VS-2215 and exhaust
spring VS-2216. These are excellent next search keys for detailed product
images and dimensions. The saved application table includes all 27 results.
It is not an engine BOM: the catalog also includes a priming tool, repair liners,
kits and mutually exclusive replacement options.

## Discrepancies retained for later review

- The Melling valve application note refers to an injection-pump gear tower and engine codes inappropriate-looking for this gasoline application. This occurs on the manufacturer lookup too; it is not merely a dealer transcription error.
- Dorman's old catalog cross-reference uses F7TZ6312-A; its [current product page](https://www.dormanproducts.com/p-20122-594-152.aspx) gives E7TZ6312-A. Do not silently merge them.
- The plug guide prints 2.070 in and 52.48 mm for MPS-59-A OD; these do not convert exactly. Preserve the printed values and resolve before precise modeling.
- The downloaded Melling spring-kit specification sheet does not contain VS-2215/VS-2216. Its performance spring dimensions must not be assigned to these stock springs.
- A publicly indexed older Melling timing-gear PDF returned 404. The live catalog verifies several gear-set alternatives, but not their detailed tooth geometry or which is installed.
- Search results for a “Ford 300” automobile, Ford Modular engine guides, miniature-engine drawings and neighboring OBD-II years must not be treated as exact 4.9L EEC-IV evidence.

## Recommended next work

1. Apply the pushrod and damper dimensions in a controlled CAD revision, then check the affected assembly datums. A correct part length can reveal that existing head, rocker or lifter placement is provisional.
2. Reconcile the expansion-plug inventory and locations with the Ford block illustrations; model the named plug types individually.
3. Use the confirmed Melling identifiers to seek pump, rocker, spring and gear detail. Obtain the exact EVTM for wiring/location structure and PC/ED for diagnostic decision paths when full copies are available.
4. Continue looking for block/head/manifold dimensions and scaled matching-part photographs. Catalog envelopes and service diagrams are progress, but do not verify casting contours, hidden galleries or all mounting coordinates.

## Reproduce and inspect

```sh
python3 scripts/fetch-engine-research-round.py
pdftotext -layout reference/engine/research-2026-09-23/melling-pushrod-specifications.pdf /tmp/pushrod.txt
python3 tools/ingest.py /tmp/pushrod.txt --type local --title melling-pushrod-specifications
```

The fetcher restores public static files and checks saved SHA-256 values. Changed
remote bytes require review rather than silent replacement. The dynamic Melling
lookup is preserved as a reviewed transcription; reapply its saved filters for a
fresh check. PDF extraction used Poppler followed by the existing local-text
ingester because the system interpreter lacked `pypdf`. Relevant tables were
checked in rendered page images; automatic HTML extraction is incomplete for
some listings, so the original HTML and browser review matter.
