# Front crank seal — source and envelope study

## Contract before geometry

Root owns `reference/engine/front-crank-seal-envelope-review.json`, this handoff, a new `front_crank_seal_envelope_candidate.py` and dedicated checker/report/render. Issue #32; baseline `3079300f629f5a2db6c1150fa87092578c9e2cad`, branch `engine/timing-coupled-fit`. Canonical manifest remains 91950c89. No shared builder or existing candidate changes.

Scope: use the exact-year seal identity and manufacturer replacement dimensions to quantify incompatibility of the current annulus and future timing-cover seat. This is an envelope/interface diagnostic, not a finished seal. Do not infer crankshaft bore diameter from the contacted seal surface, assign a production lip position or move the damper to hide a gap.

## Evidence

The exact-year parts entry gives E6DZ6700A. National's manufacturer-authored cross-reference links it to 2692. National's current specification table gives a 1.875-inch shaft surface, 2.561-inch housing bore, 2.565-inch case OD and 0.528-inch width. Timken's public table independently agrees and gives a 3.16-inch flange OD. Inch values convert exactly at25.4 mm/in; catalog metric values are rounded. Source paths, hashes, URLs and actual page review are in the ledger.

The National type76 diagram shows a stepped/flanged case, elastomer and spring section, but it does not dimension those internals. Timken also identifies its internal drawing features as representative. No vendor CAD drawing has been downloaded or incorporated.

## Planned checks and limits

Compare replacement envelope against the current 54/42×8 mm annulus and estimated cover seat; quantify radial bore mismatch and axial registration alternatives without adopting either. Keep observed current hub gap separate from source evidence. An eventual coordinated change must address cover boss/flange support, damper sealing track, seal deformation and case seating while preserving gear, gasket and mounting interfaces.

No new model is installed, no browser gate has run, and no issue is Done. The bounded envelope diagnostic is complete; physical seal construction remains open. Originals are ignored and excluded from release packages. Usage/model-effort metrics unavailable.

## Diagnostic delivery

`front_crank_seal_envelope_candidate.probes(front)` constructs annular envelopes, a housing-bore probe and a zero-thickness flange face. These are clearly named diagnostic geometry, not reusable physical part definitions. No seal internal geometry or flange thickness is inferred.

Commands from the repository root:

```sh
XDG_CACHE_HOME=/tmp/truck-cache .venv-cad/bin/python scripts/check-front-crank-seal-envelope.py
XDG_CACHE_HOME=/tmp/truck-cache MPLCONFIGDIR=/tmp/truck-gear-mpl PYTHONPATH=.venv-cad/lib/python3.13/site-packages python3 scripts/render-front-crank-seal-envelope.py
```

The locked CAD environment supplies build123d; the render command also uses the existing system matplotlib. The first attempt using only the CAD environment lacked matplotlib and failed before rendering; no dependency was installed. Cache directories contain no required evidence.

Both hypothetical axial registrations show substantial existing cover material inside the required housing probe (11,220.842 and12,360.781 mm³). The unchanged smaller bore control is clear. Required bore radius increases5.5247 mm from the current27 mm; free-case nominal diametral interference is0.1016 mm. These are envelope comparisons, not a real seal collision or tolerance calculation. Neither position is adopted.

Root inspected the actual cover section with the source-sized probes in `cad/engine/generated/front-crank-seal-envelope/section-review.png`. Exported STEP probe hashes and all evidence inputs are recorded in `inventory/engine/front-crank-seal-envelope-validation.json`. The result supports a coordinated cover/hub/seal correction; it does not establish lip position, compression, spring dimensions or production seating.

Quality gates: source identity/cross-reference and dimensions PASS for a replacement comparison; envelope checks PASS; physical CAD, installed fit, motion and browser NOT RUN; learning N/A for this diagnostic. No part was marked Done.

Report SHA-256: `0798390cbb171d169369494581e810af8005b4e14d2a5d17375348f620ab135a`.
