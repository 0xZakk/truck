# ACT specimen preservation handoff

Issue82; worker pump, root integration/publication owner. Own this handoff, `scripts/act-online-20261002-package.py`, `docs/act-online-20261002-package.json` and generated archive only. CAD delivery remains frozen. Baseline recorded by packaging metadata. No canonical/host/pose edits, commit or upload.

Root reviewed corrected actual GLB against manufacturer side/end photographs and accepted **preservation of the replacement-comparison candidate**. This does not accept installed fit, thread gauge/truncations, original factory dimensions or a complete electrical circuit. Guard/key rounding and projection limits, hidden leads/potting/chip omissions remain explicit. Existing candidate handoff is unchanged.

The archive contains only exact ledger-listed project-authored generated STEP/GLB/render and rejected construction inputs. Source/report/handoff files remain in a separate exact repository allowlist; restore those alongside the archive. No generated predecessor archive is needed for standalone build. Two prior identity reports are checked as tracked repository evidence. Manufacturer images/HTML/PDF have URLs/hashes in the evidence ledger, are excluded from the archive, and are not required for preservation verification; reacquire them for photo review. Their local review paths are provenance only.

```sh
python3 scripts/act-online-20261002-package.py --prepare
python3 scripts/act-online-20261002-package.py
python3 scripts/act-online-20261002-package.py --verify-only
```

The script verifies frozen delivery hashes, creates sorted fixed-metadata gzip/tar, and streams every member without extraction. The second build checks determinism by comparing archive hashes. Only Python standard library is required. Exact size/hash/count are recorded in the JSON. CAD checks are inherited, not rerun. Root owns publication; active pump/duct work is excluded. No process remains after completion. Usage accounting unavailable.
