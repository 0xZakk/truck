# Component contract and handoff: renewed online oil-pump interface evidence

## Contract

- Engine #32; pump worker, root integration owner. Baseline `dbe1e3c435c137fe2d30f6420db28476127c0f55`.
- Research only. Own this handoff, `reference/engine/online-oilpump-research.json`, and `kb/{sources,notes}/online-oilpump-*`. No canonical/model/map changes or source-original distribution.
- Target exact-year C5AZ6600A, comparison M74, separate mount/discharge and pickup interfaces. Existing Ford evidence remains authoritative for application; replacement artwork is qualitative evidence.
- No new units, frame, transforms or exploded poses assigned. Installed engine manifest unchanged. Preserve drive axis, pan, crank/cam, gallery and pickup interfaces pending a coordinated future contract.
- Required inputs: public catalog and existing Ford source notes; no purchase, account or owner photograph needed for this finding.

## Evidence ledger

| Finding | Evidence class | Source | Limit |
|---|---|---|---|
| Identified replacement with two flange patterns | Replacement catalog, directly viewed | RONYU-hosted PDF page 21 / printed 033 / RY-FO132 | Page branding LIZHONG; not asserted Ford manufacturing provenance |
| Different aperture counts on two outlines | Direct visual observation | Same row's gasket drawings | No labeled aperture function or metric scale |
| Source flange architecture differs from old feet/inserted tube | Corroborating comparison | Existing Ford industrial and CSG649 notes linked in new KB notes | Block gallery entry remains unresolved |

Exact URL, PDF hash, search results and exclusions are in the JSON. The useful advance over the earlier discharge audit is actual inspection of identified pump/gasket pixels, not another search-index description. The earlier audit's unknown dimensions remain unknown.

## Proposed next geometry contract

Directly improve the existing topology study by representing **two independent flange templates** and their gasket-pattern correspondence, instead of fitting a gasket around old feet. Preserve the elongated pattern's two interior apertures as distinct topological features. Their hydraulic/drive/dowel identities remain unresolved; test assignments against the Ford source rather than choosing by appearance.

This supports a schematic comparison revision with explicit unscaled patterns and ownership. It does not support production gasket thickness, guessed bolt spacing, a hidden discharge drilling, or installation against current block feet. A later coordinated neck/block candidate must prove both gasket backing and pump-to-block passage correspondence. Wrong mirror, swapped aperture identities, single-hole substitution, blocked discharge and unsupported gasket are required fault cases. No CAD was built in this research scope.

## Delivery and reproduction

- Research-ready: one source page, two atomic notes, JSON and this handoff. No STEP/GLB/release/PR from this worker.
- Python 3 plus existing CAD virtual environment (`pypdf 6.19.0`), Poppler. System Python lacked pypdf; the existing CAD environment worked. Model/usage unavailable.
- Initial web-tool PDF fetch timed out and sandbox download lacked DNS. Authorized read-only network retrieval succeeded. JEGS images and rebuild-thread evidence were not viewable and are not claimed inspected.
- Originals and page renders remain local review material only. Recreate them from the public URL; another developer need not have this session's temporary files:

```sh
curl -L --fail 'https://www.ronyu-china.com/templets/default/pdf/oil-pump-catalogue.pdf' -o /tmp/online-oilpump-ronyu.pdf
sha256sum /tmp/online-oilpump-ronyu.pdf
.venv-cad/bin/python tools/ingest.py /tmp/online-oilpump-ronyu.pdf --type pdf --pages 21 --title online-oilpump-ronyu-identified-flanges
pdftoppm -f 21 -singlefile -scale-to 2400 -png /tmp/online-oilpump-ronyu.pdf /tmp/online-oilpump-ronyu-page21
pdftoppm -f 21 -singlefile -r 350 -x 0 -y 1250 -W 2200 -H 1150 -png /tmp/online-oilpump-ronyu.pdf /tmp/online-oilpump-ronyu-detail
pdftoppm -f 21 -singlefile -r 350 -x 2200 -y 1480 -W 540 -H 510 -png /tmp/online-oilpump-ronyu.pdf /tmp/online-oilpump-ronyu-gaskets
```

Expected PDF SHA-256 `37c83f4d149b5b9811017c7881c23900c080b73e8a71b0102f10c46da3da8574`, 6,641,767 bytes. Recheck if the publisher changes it. Raw text generated under ignored `kb/.raw/`; original PDF/artwork not added to Git.

## Validation and review

| Gate | Status | Evidence / limit |
|---|---|---|
| Application | PASS comparison only | Explicit catalog identity bridge; no exact Ford casting claim |
| Dimensions/coordinates | UNKNOWN | No metric drawing found |
| Source visual | PASS scoped | Row and gasket detail directly viewed |
| CAD/export | N/A | Research only |
| Installed interfaces/flow | NOT RUN | No geometry changes; existing defect retained |
| Motion/disassembly | NOT RUN | No geometry changes |
| Learning | PASS structural | Atomic notes, prefixed links; semantic shared run owned by root |
| Browser integration | NOT RUN | No viewer edit |
| Reproduction | PASS scoped | Public URL/hash/page/commands, no redistributed originals |

Root review pending. This is a concrete source/coverage advance, not installed acceptance. Engine issue stays open. Next bounded work is source-correspondence review of both templates against the Ford exploded/installed views, then an explicitly qualified topology-study correction. No process remains running.
