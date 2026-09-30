# Local timing-gear evidence captures

These are third-party research inputs, not project-authored CAD. Captures and renders are ignored and excluded from shared CAD releases; retain the parent JSON ledger and its hashes. No credentials are required. From repository root:

```sh
curl -L --fail 'https://www.pbm-erson.com/documents/d/prod/pbmcatalog02-03-2025' -o reference/engine/timing-gear-evidence/pbm-catalog-2025.pdf
curl -L --fail 'https://images.carid.com/melling/info/pdf/melling-engine-parts-catalog.pdf' -o reference/engine/timing-gear-evidence/melling-engine-parts-catalog.pdf
curl -L --fail 'https://catalog.elginind.com/partno-search/?partno=C-2766S' -o reference/engine/timing-gear-evidence/elgin-c2766s.html
curl -L --fail 'https://catalog.elginind.com/media/41/C-2766S-FRO.jpg' -o reference/engine/timing-gear-evidence/elgin-c2766s-front.jpg
pdftoppm -f 204 -singlefile -scale-to 1800 -png reference/engine/timing-gear-evidence/pbm-catalog-2025.pdf reference/engine/timing-gear-evidence/pbm-page-204
pdftoppm -f 111 -singlefile -scale-to 1800 -png reference/engine/timing-gear-evidence/melling-engine-parts-catalog.pdf reference/engine/timing-gear-evidence/melling-page-111
pdftoppm -f 13 -singlefile -scale-to 1800 -png reference/engine/ford-industrial-parts.pdf reference/engine/timing-gear-evidence/industrial-page-13
python3 scripts/check-timing-gear-evidence.py
```

Restore the pre-existing Ford industrial PDF from its URL in `reference/engine/timing-gear-evidence-review.json` if absent. Verify every capture against that ledger before attributing historical results. A dynamically changed supplier page requires fresh review rather than silently updating its checksum. Poppler generated the reviewed page renders. The PBM physical PDF page204 is printed205; Melling PDF111 is printed116; industrial PDF13 is printed10.
