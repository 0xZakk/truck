# Component handoff: online research candidate preservation

## Contract

Engine #32; pump worker packages, root reviews/publishes. Scope is preservation only: frozen online-heater-route and online-airbox-duct-specimen deliveries. No modeling, canonical, inventory, source-photo or map changes. Own `scripts/online-research-candidates-package.py`, `docs/online-research-candidates-checkpoint.json`, this handoff and the generated checkpoint archive. Baseline and exact source hashes are recorded by the packaging script at preparation.

Heater is a conditional axial route hypothesis with unregistered radial projection. Airbox is an uninstalled local specimen with estimated dimensions and unknown vehicle pose. Packaging does not expand either acceptance scope. Original photographs, PDFs, raw captures and ingest output are excluded; authored sources, rejected construction code and diagnostic reports stay in the repository allowlist.

## Delivery

The metadata binds the source/report/handoff files and contains the exact generated artifact allowlist. The archive contains only the listed project-authored generated artifacts; source files are restored from the repository revision and the bound allowlist. Published prerequisites are neck-core and its ordered supplements through waterpump studies, accessory-layout, and coordinated accessory v4. Exact input hashes are matched to predecessor metadata. Published release URLs and publication supersessions are in `docs/CAD-ARTIFACTS.md`.

Prior archive hashes:

- Waterpump studies: `b13f2bf787e405454b3ab14017e5cb7aa07bb14d15c1ba6eb4c273c08cbe29fc`.
- Accessory layout: `dd374011c14bec494f0647c3e84b8ff56ff3fd4e337e0f2fc6ad57bf9ac47d7b`.
- Accessory v4: `9671be99527ad49387a09877b824f858277e551deae81e2659a0adc6ebadb943`.

From repository root:

```sh
python3 scripts/online-research-candidates-package.py --prepare
python3 scripts/online-research-candidates-package.py --verify-only
```

Preparation verifies input hashes and constructs a deterministic gzip/tar with sorted paths and fixed metadata. Verification streams every member, checks exact names and SHA-256, and performs no extraction. Rebuild from the frozen metadata without `--prepare` to demonstrate archive determinism. Python standard library only; no CAD runtime is needed to package or view the STEP/GLB with an appropriate viewer. Usage/model accounting unavailable.

## Validation and limits

Preservation acceptance requires matching delivery hashes, exact archive membership, two equal rebuild hashes, and source-image exclusions. CAD validity/contact/flow/clearance results are inherited from frozen reports, not rerun. Application, metric fidelity, installed interfaces, motion, disassembly and browser installation remain limited as stated in each component handoff. Prior archives are matched through metadata, not freshly reopened or rebuilt. Excluded originals can be reacquired from public source ledgers when needed for source review; they are unnecessary for reading the exported specimen solids.

No upload, commit or release publication is performed here. Root owns final review and publication. Active heater radial-registration work is excluded. Final archive result is in the JSON; no running background work is implied by this handoff.

## Frozen result

Archive: `cad/engine/generated/online-research-candidates-checkpoint/truck-online-research-candidates-20261001.tar.gz`; 40 members, 5,061,563 bytes; SHA-256 `f76ed06430c399d467c45d4a4ee4b64c2e16bbe9e23817e91bea34e40e8a4707`.

Two builds produced identical bytes; streamed member verification PASS. The metadata binds31 source/report/handoff files,746 generated prerequisite hashes matched against8 predecessor metadata files,5 tracked repository inputs,10 excluded source originals and6 excluded capture-metadata logs. Historical airbox CAD/checker Python files and logs are retained inside the generated archive for the recorded recovery procedure. Both rendered images were reviewed as project-authored mesh/CAD views with no source pixels. Packaging syntax check PASS. No original source files, active radial study, shared-state documents, canonical changes, upload or commit included.

Capture metadata is not a restore prerequisite. The five ingest logs and OCR log are excluded from the archive and repository source allowlist; verification checks their hashes only when present. Remaining repository input paths are required to exist in the Git index (tracked or staged).
