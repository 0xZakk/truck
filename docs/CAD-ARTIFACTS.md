# Restore the engine CAD checkpoint

Browser meshes, modeling source and validation reports are committed to Git. Generated STEP files live in private GitHub release archives because the combined assembly exceeds normal GitHub file limits. Browser exploration needs only the committed GLBs.

## Current neck and timing-core checkpoint

The September 30 neck/core package is published at [this private release](https://github.com/0xZakk/truck/releases/tag/checkpoint-2026-09-30-neck-core). It preserves **741 definitions / 1,349 occurrences**, the further installed rear-neck blend, isolated timing-core/thrust-land studies and the failed old-gear backlash diagnostic. The engine remains unfinished and browser acceptance is NOT RUN.

```sh
gh release download checkpoint-2026-09-30-neck-core --repo 0xZakk/truck --pattern truck-active-cad-20260930-neck-core.tar.gz --dir /tmp
shasum -a 256 /tmp/truck-active-cad-20260930-neck-core.tar.gz
```

Compare with `docs/cad-neck-core-checkpoint.json`, preserve newer local generated work, then extract from the repository root using `tar -xzf /tmp/truck-active-cad-20260930-neck-core.tar.gz`. Package reproduction: `python3 scripts/package-neck-core-checkpoint.py --previous <exhaust-timing-archive> --output <new-archive>`.

All prior archive fixtures are retained with current active STEP definitions and the rebuilt combined assembly. The ongoing shifted-block, coordinated pan-joint and reduced-backlash revisions are excluded. Purchased manuals, owner photographs and third-party reference images/composites remain excluded; acquire authorized evidence separately.

## Supplemental timing-fit studies

The separate [timing-fit study archive](https://github.com/0xZakk/truck/releases/tag/studies-2026-09-30-timing-fit) overlays the neck/core base above. It contains the exact block baseline, rejected first axis migration, reviewed estimated cover/pan joint and revised backlash pair. These are isolated candidates, not installed engine changes. Restore the neck/core archive first, then download this smaller supplement:

```sh
gh release download studies-2026-09-30-timing-fit --repo 0xZakk/truck --pattern truck-timing-studies-20260930.tar.gz --dir /tmp
shasum -a 256 /tmp/truck-timing-studies-20260930.tar.gz
```

Compare with `docs/cad-timing-studies-checkpoint.json`, preserve newer local work, then extract from the repository root using `tar -xzf /tmp/truck-timing-studies-20260930.tar.gz`. The metadata records every file hash and required base archive. Reproduce with `python3 scripts/package-timing-studies-checkpoint.py --output <archive>` after restoring the required fixtures. Active fixed-stock, attachment and coupled-core revisions are excluded, as are third-party images, manuals and owner photographs. Failed checks are retained as evidence, not acceptance.

## Supplemental timing proof and failure evidence

The [timing-proof supplement](https://github.com/0xZakk/truck/releases/tag/studies-2026-09-30-timing-proof) requires the neck/core base and timing-fit supplement above, in that order. It preserves fixed-stock block failures and the reviewed topology-only repair, rejected cover attachments, rigid timing-core and continuous rotating-clearance proofs, and the source-sized seal-envelope diagnostic. It replaces no installed engine parts.

```sh
gh release download studies-2026-09-30-timing-proof --repo 0xZakk/truck --pattern truck-timing-proof-20260930.tar.gz --dir /tmp
shasum -a 256 /tmp/truck-timing-proof-20260930.tar.gz
```

Verify against `docs/cad-timing-proof-checkpoint.json`, preserve newer local work, then extract from the repository root with `tar -xzf /tmp/truck-timing-proof-20260930.tar.gz`. Reproduce using `python3 scripts/package-timing-proof-checkpoint.py --output <archive>`. Active support-machining, fastener and valvetrain revisions are excluded. Manufacturer PDFs, original source imagery, purchased manuals and owner photos remain separate reference dependencies and are excluded from all archives.

## Previous rear-exhaust and timing-study checkpoint

The [September30 exhaust/timing archive](https://github.com/0xZakk/truck/releases/tag/checkpoint-2026-09-30-exhaust-timing) is published for PR #95. It preserves **741 definitions / 1,349 occurrences**, the installed rear collector and separate timing studies. Browser acceptance remains NOT RUN; the engine is unfinished.

Restore using:

```sh
gh release download checkpoint-2026-09-30-exhaust-timing --repo 0xZakk/truck --pattern truck-active-cad-20260930-exhaust-timing.tar.gz --dir /tmp
shasum -a 256 /tmp/truck-active-cad-20260930-exhaust-timing.tar.gz
```

Compare with `docs/cad-exhaust-timing-checkpoint.json`, preserve newer local work, then extract from the repository root:

```sh
tar -xzf /tmp/truck-active-cad-20260930-exhaust-timing.tar.gz
```

The archive contains active STEP geometry and the rebuilt combined assembly; prior fixtures; the rear-collector candidate, stages and promotion evidence; separate gear/refinement studies; cover/gasket studies including rejected pan registration; numeric cam-axis feasibility and the newer registration study. Ongoing timing-core and coordinated pan-joint candidates are excluded. Reference originals/composites, purchased manuals and owner photographs are excluded. Source evidence requiring restricted originals remains a separate authorized-access dependency.

Reproduce the package with `scripts/package-exhaust-timing-checkpoint.py --previous <runner-evr-stops-archive> --output <new-archive>`. The script verifies the prior archive and current input stability. It is not a factory-fidelity certificate.

## Previous runner, EVR and throttle-stop checkpoint

The [September30 checkpoint](https://github.com/0xZakk/truck/releases/tag/checkpoint-2026-09-30-runner-evr-stops) contains **741 definitions / 1,349 occurrences**. Geometry remains provisional and browser acceptance for this batch is NOT RUN. It preserves source-compared runner surfaces, illustrative EVR/stop mechanisms and a separate air-cleaner candidate.

```sh
gh release download checkpoint-2026-09-30-runner-evr-stops --repo 0xZakk/truck --pattern truck-active-cad-20260930-runner-evr-stops.tar.gz --dir /tmp
shasum -a 256 /tmp/truck-active-cad-20260930-runner-evr-stops.tar.gz
```

Compare with `docs/cad-runner-evr-stops-checkpoint.json`, preserve newer local work, then extract from the repository root:

```sh
tar -xzf /tmp/truck-active-cad-20260930-runner-evr-stops.tar.gz
```

The archive includes active STEP definitions and the combined assembly; older fixtures; runner, EVR and stop candidates/stages; discrete spring STEP poses; scoped proofs/logs; and the isolated air-cleaner candidate. All five browser spring GLBs and pose metadata are also committed under `models/engine/evr-motion/`. It excludes reference originals/composites, purchased manuals, owner photographs and ongoing exhaust/timing studies. Restricted source access remains an explicit reproduction dependency.

The package can be reproduced with `scripts/package-runner-evr-stops-checkpoint.py --previous <previous-cable-distributor-archive> --output <new-archive>`. It verifies the prior archive, current combined-export hash, active counts and input stability; it does not certify factory fidelity. Restore the previous archive first if a required historical fixture is missing.

## Previous cable and distributor checkpoint

The [cable/distributor release](https://github.com/0xZakk/truck/releases/tag/checkpoint-2026-09-26-cable-distributor) records **733 definitions / 1,341 occurrences**. It adds a source-compared rotor leaf and an explicitly illustrative seven-part engine-end cable mechanism. Production geometry remains provisional and the engine is unfinished.

```sh
gh release download checkpoint-2026-09-26-cable-distributor --repo 0xZakk/truck --pattern truck-active-cad-20260926-cable-distributor.tar.gz --dir /tmp
shasum -a 256 /tmp/truck-active-cad-20260926-cable-distributor.tar.gz
```

Compare with `docs/cad-cable-distributor-checkpoint.json`, preserve newer local work, then extract from the repository root:

```sh
tar -xzf /tmp/truck-active-cad-20260926-cable-distributor.tar.gz
```

This includes active STEP geometry, the combined assembly, prior fixtures and reviewed rotor/cable candidates and integration stages. It excludes ongoing runner/EVR work, symlink promotion mirrors, third-party reference photos/composites, purchased manuals and owner photographs. The committed cable motion table is separate from this CAD archive. Historical reports retain their original input hashes and scopes.

## Previous intake exterior and IAC detail checkpoint

The [intake/IAC detail release](https://github.com/0xZakk/truck/releases/tag/checkpoint-2026-09-26-iac-detail) records **725 definitions / 1,333 occurrences**. It adds source-compared intake exterior detail, an explicitly illustrative captured IAC closure, and separately selectable terminals and insulating carrier. Production geometry remains provisional.

```sh
gh release download checkpoint-2026-09-26-iac-detail --repo 0xZakk/truck --pattern truck-active-cad-20260926-iac-detail.tar.gz --dir /tmp
shasum -a 256 /tmp/truck-active-cad-20260926-iac-detail.tar.gz
```

Compare with `docs/cad-iac-detail-checkpoint.json`, preserve newer local work, then extract from the repository root:

```sh
tar -xzf /tmp/truck-active-cad-20260926-iac-detail.tar.gz
```

This includes active STEP geometry, the combined assembly, prior fixtures and the new exterior/closure/electrical candidates, stages and ordered adapter replay. It excludes ongoing cable/distributor/PCV work, third-party reference photos, purchased manuals and owner photographs. These studies do not make the engine complete.

## Previous intake and attachment checkpoint

The [intake/attachment release](https://github.com/0xZakk/truck/releases/tag/checkpoint-2026-09-26-intake-attachments) records **722 definitions / 1,330 occurrences**. It includes the compact intake, coordinated cap/EGR interfaces, IAC mounting and internal return study, and illustrative plate retention. The engine remains unfinished and dimensions remain provisional.

```sh
gh release download checkpoint-2026-09-26-intake-attachments --repo 0xZakk/truck --pattern truck-active-cad-20260926-intake-attachments.tar.gz --dir /tmp
shasum -a 256 /tmp/truck-active-cad-20260926-intake-attachments.tar.gz
```

Compare against `docs/cad-intake-attachments-checkpoint.json`. Preserve newer local work before extracting from the repository root:

```sh
tar -xzf /tmp/truck-active-cad-20260926-intake-attachments.tar.gz
```

This archive includes prior frozen fixtures plus the new candidate/staging outputs and intake frame-contract solids. It excludes the in-progress intake exterior, IAC closure and accelerator-cable studies, purchased manuals and owner photographs. Restricted reference captures must be obtained separately with appropriate access.

## Timing support supplement (uninstalled)

The timing-support supplement preserves frozen journal-support/machining checks, pump/pan collision witnesses, the revised pan male fastener, rejected cover attachment v2, valve-linkage contract and rejected pedestal-only adapter. It does not replace canonical parts. Active pump-foot, pan-wall and inclined-linkage revisions are excluded.

Restore the neck-core base, timing-fit and timing-proof supplements first. Then download `truck-timing-support-20260930.tar.gz` from release `studies-2026-09-30-timing-support`, verify SHA-256 **498a3840c818dc75362da722284996a56557068a6ac636cc05e70bd9a13ceb91**, and extract at the repository root after preserving newer local work. The 19,381,804-byte archive contains 98 files; `docs/cad-timing-support-checkpoint.json` lists individual hashes and the required predecessor. Only project-authored renders are included; source originals and owner photographs are excluded.

## Timing clearance supplement (uninstalled)

The [timing-clearance supplement](https://github.com/0xZakk/truck/releases/tag/studies-2026-10-01-timing-clearance) preserves analytical and faceted pump feet, inclined linkage/passages, the detected peak rocker/cover conflict, rejected pan/access and capped-void checks, and the composed block. These are candidates and failed-test evidence, not installed or factory-approved parts. Active corrective revisions are excluded.

Restore the neck-core base and timing-fit, timing-proof and timing-support supplements first. Download `truck-timing-clearance-20261001.tar.gz`; verify SHA-256 **fc1aee5ae6a6a65a21a0b35ec972c837070226780c248738aad5e69753b7b74d** before extracting at the repository root, preserving newer generated files. The archive has 92 files / 23,282,544 bytes. `docs/cad-timing-clearance-checkpoint.json` records all file hashes and the predecessor archive. Source originals, purchased manuals and owner photographs are excluded.

## Timing interface supplement (uninstalled)

The [timing-interfaces supplement](https://github.com/0xZakk/truck/releases/tag/studies-2026-10-01-timing-interfaces) preserves front-block region research, both failed pan pairs, the dry-neck local checks, and the crest/neighbor/spring correction. It does not replace the installed engine. Active shared pan-seat and2692 seal work are excluded.

Restore all predecessors through timing-clearance first. Download `truck-timing-interfaces-20261001.tar.gz`, verify SHA-256 **a86d3c16b218840655f395b2c65cbe2cdd8a598581756b2f5bb49d10897d9b18**, then extract at the repository root after preserving newer work. This archive contains81files/17,519,969bytes. Individual hashes and predecessor binding are in `docs/cad-timing-interfaces-checkpoint.json`. Only project-authored images are included; no purchased manuals, reference originals or owner photos.

## Previous linkage and dipstick checkpoint

The [linkage/dipstick release](https://github.com/0xZakk/truck/releases/tag/checkpoint-2026-09-26-linkage-dipstick) records **718 definitions /1,322 occurrences**, still provisional and unfinished. Download with an account that can access the repository:

```sh
gh release download checkpoint-2026-09-26-linkage-dipstick --repo 0xZakk/truck --pattern truck-active-cad-20260926-linkage-dipstick.tar.gz --dir /tmp
shasum -a 256 /tmp/truck-active-cad-20260926-linkage-dipstick.tar.gz
```

Compare the checksum with `docs/cad-linkage-dipstick-checkpoint.json`. Preserve any newer local generated work, then extract from the repository root:

```sh
tar -xzf /tmp/truck-active-cad-20260926-linkage-dipstick.tar.gz
```

The archive includes every active part STEP and the combined STEP, plus frozen linkage/spring/dipstick candidate evidence needed by their scoped checks. Isolated EGR-route candidate exports are included but are **not installed** in this checkpoint. Purchased manuals and owner photographs are excluded.

Part hashes and combined-export identity are in `inventory/engine/combined-step-export.json`. The export uses independent topology for each occurrence, preserving unique names on reimport; its bounds check is not proof of exact shape equivalence or manufacturing fit. Source applicability, inferred dimensions and outstanding work remain in the component reports and `docs/CURRENT-STATE.md`.

## Historical archives

The [original checkpoint](https://github.com/0xZakk/truck/releases/tag/checkpoint-2026-09-26), recorded by `docs/cad-checkpoint.json`, contains older candidate baselines. A later audit recovered17missing and32stale STEP definitions; see `inventory/engine/cad-baseline-restoration.json`. Never trust manifest identity while using arbitrary local STEP files.

The [interface checkpoint](https://github.com/0xZakk/truck/releases/tag/checkpoint-2026-09-26-interfaces), recorded by `docs/cad-interface-checkpoint.json`, covers705definitions/1,310occurrences before the linkage/dipstick work and combined naming correction. If a historical study needs old extra assets, extract its archive first, then overlay the current archive. Do not overwrite newer work without preserving it.

## Regenerate a combined assembly

After reviewed part/manifest changes, rebuild the combined STEP without rebuilding all part geometry:

```sh
XDG_CACHE_HOME=/tmp/truck-cache .venv-cad/bin/python scripts/export-engine-assembly-step.py
```

Installers default to dry-run/staging and preserve unrelated inventory: `install-engine-component-interfaces.py`, `install-throttle-linkage.py` (linkage/shield/spring stages), `install-dipstick.py`, `install-intake-cap-coordination.py`, `install-iac-attachment.py`, and `install-throttle-plate-fasteners.py` under `scripts/`. Read their candidate/input guards before applying; a saved report is evidence for its recorded inputs, not a fresh validation of a changed engine. Use a new branch/worktree for further changes and retain explicit provisional labels.

## Pan-seat and front-seal candidate supplement

The [pan/seal supplement](https://github.com/0xZakk/truck/releases/tag/studies-2026-10-01-pan-seal) preserves the expanded-seat trials, corrected block v3 pair, bounded rear gasket contact study, separate 2692 seal parts and their localized integration-stage assets. It does not replace the installed engine. The block's aggregate report retains FAIL for two unverified volume metrics; its functional, locality and export results are reported separately. Active whole-perimeter and operating-direction studies are excluded.

Restore predecessors through timing-interfaces, then download and verify this supplement:

```sh
gh release download studies-2026-10-01-pan-seal --repo 0xZakk/truck --pattern truck-pan-seal-20261001.tar.gz --dir /tmp
shasum -a 256 /tmp/truck-pan-seal-20261001.tar.gz
```

Expected SHA-256: **5b46ae082c6ea9fe23d67b44b26578e1473fe2d2a13ac92cbae8953904b52fe8**. The archive contains 123 files / 33,127,925 bytes. Individual hashes and predecessor binding are in `docs/cad-pan-seal-checkpoint.json`. Preserve newer local work before extracting at the repository root. Only project-authored renders are included; no purchased manuals, reference originals or owner photographs.

## Motion/contact candidate supplement

The [motion/contact supplement](https://github.com/0xZakk/truck/releases/tag/studies-2026-10-01-motion-contact) contains the corrected crank throw-phase candidate, bounded lower/upper pan contact evidence and guarded pan/fastener integration assets. It is not an installed engine update. Active corrected cam, crossed-drive and main-cover-seat work is excluded.

Restore predecessors through pan-seal first. Download `truck-motion-contact-20261001.tar.gz`, verify SHA-256 **2be3c16b8274c0b06c30eb0aa78c2e3ead383d80eb009fc46ae82368c6468f93**, then extract from the repository root after preserving newer work. The archive has 89 files / 6,756,376 bytes. `docs/cad-motion-contact-checkpoint.json` records every file hash and predecessor binding. Only project-authored renders are included; source originals and owner photographs remain excluded.

## Cam/cover candidate supplement

The cam/cover supplement (`studies-2026-10-01-cam-cover`) preserves corrected cam and crossed-drive geometry/endplay, rejected cover-fastener trials, and the coordinated pan21 candidate. No canonical replacement or installed acceptance. Restore predecessors through motion-contact first.

Download `truck-cam-cover-20261001.tar.gz` from the private repository release, verify SHA-256 **f67121592b2de92346eecb1d750cd49bc2bbfc3cb35bbc14a95dfd8c2b075b3f**, then extract at the repository root after preserving newer work. The archive has 62 files / 22,441,296 bytes. `docs/cad-cam-cover-checkpoint.json` records all hashes. Publication and server-side digest/size verified after PR104 merged. Original references/photos are excluded.

## Composed-engine study checkpoint (published)

`docs/cad-composed-engine-checkpoint.json` records the exact 181-file allowlist, archive hash and dependency on the cam/cover checkpoint. The locally packaged archive is `truck-composed-engine-20261001.tar.gz`, 60,749,763 bytes, SHA-256 `11596222af342b6bdfc461bdbe9b52f39a358a30966879eeac6e30fa208b33d0`. Restore the cam/cover chain first. This candidate archive preserves the composed cam, combined moving snapshot, core/front/sealing assets, pickup study and failed changed-neighbor witnesses. It excludes ongoing repair work and reference originals. Published after PR105 merged; server archive digest/size verified. Download from [the private release](https://github.com/0xZakk/truck/releases/tag/studies-2026-10-01-composed-engine). The supplemental project-authored `guard-review.png` is a separate release asset (160,724 bytes, SHA-256 `9b564f76a18b09d093cd0e45b6683444155644c228afd7706cd38c346a54766e`); restore it to `cad/engine/generated/timing-seven-block-guard-study/guard-review.png`. This render was excluded from the archive image allowlist, so archive bytes/hash remain unchanged.

## Ignition-connections checkpoint (published)

`docs/cad-ignition-connections-checkpoint.json` binds64 files /17,370,033 bytes in `truck-ignition-connections-20261001.tar.gz`, SHA-256 `25bae3deb1d29d8395c9f17b2cf035f959b0c6b7b51d166de32766fb7919d920`. It requires the composed-engine predecessor. Contains28 STEP/GLB pairs, the actual ignition mesh review and seven v2 gasket intersection witnesses. Candidate-only:26 known v3 static conflicts and other gates remain. [Private release](https://github.com/0xZakk/truck/releases/tag/studies-2026-10-01-ignition-connections) published after PR106 merged; server digest/size verified.

## Block closures and oil-pump topology (published)

`docs/cad-block-closures-checkpoint.json` binds13 files /361,986bytes in `truck-block-closures-20261001.tar.gz`, SHA-256 `9def0caead5bf2cb64711df05cbfccf47ac909fe78a8cae8dc998c7d9eddb96a`. It preserves two catalog-envelope cups and three separate illustrative pump topology assets with project-authored review images. Restore the installed neck-core checkpoint for inherited pump inputs; no later timing studies are needed for these isolated assets. Source catalogs/manual access remains separate. No installed acceptance; no reference originals or owner photographs.

Published after [PR107](https://github.com/0xZakk/truck/pull/107) merged at `6b1608257e8c2eaa12512ac0c256d882854f3996`; server digest and size verified. Download from [the private release](https://github.com/0xZakk/truck/releases/tag/studies-2026-10-01-block-closures).

## Water-pump studies (published)

The64-file supplement `truck-waterpump-studies-20261001.tar.gz` is19,508,529bytes, SHA-256 `b13f2bf787e405454b3ab14017e5cb7aa07bb14d15c1ba6eb4c273c08cbe29fc`. Exact frozen allowlist and prerequisite chain are in `docs/waterpump-studies-checkpoint-draft.json`; restore through ignition-connections first. It preserves rear-flange, inlet-orientation/offset and heater-route candidates, including failed trials and project-authored renders. Originals are excluded.

The later independent `inventory/engine/waterpump-prerequisite-archive-audit.json` resolves the draft's unverified691-member provenance gap: all691 expected canonical STEP members match the checksum-verified neck-core archive. No extraction or full rebuild was performed. Remaining source access, whole-engine, browser and production-fidelity limits remain. This archive does not install any pump candidate.

Published after [PR109](https://github.com/0xZakk/truck/pull/109) merged; uploaded digest/size verified. Download from [the private release](https://github.com/0xZakk/truck/releases/tag/studies-2026-10-01-waterpump). The draft-named inventory remains the frozen packaging snapshot; this publication note supersedes its NOT RUN field.


## Accessory layout checkpoint — publication pending

The locally verified archive `truck-accessory-layout-studies-20261001.tar.gz` contains96 project-authored artifacts (22,027,686bytes; SHA256 `dd374011c14bec494f0647c3e84b8ff56ff3fd4e337e0f2fc6ad57bf9ac47d7b`). Its exact member/source allowlists and prerequisite chain are in `docs/accessory-layout-checkpoint-draft.json`; reproduction instructions are in `docs/components/accessory-layout-checkpoint-handoff.md`. Publication has not yet been verified; do not assume a release asset exists.

The handoff's historical waterpump-draft statement is superseded by published `studies-2026-10-01-waterpump` (PR109). Restore that supplement and the listed predecessor chain before this package. This preserves constrained-layout hypotheses, ALT/AP trial6 and rejected studies; it does not install or accept them. PS/AC candidate files are excluded.

Publication verified after PR111 merged (`1ba91c4ba3cafddb770270527908c6df28fc0ec5`): [accessory-layout release](https://github.com/0xZakk/truck/releases/tag/studies-2026-10-01-accessory-layout), release ID401248087. Server asset digest and size matched the values above before publication. This supersedes publication-pending statements in the frozen metadata/handoff.


## Coordinated accessory v4 — publication pending

`docs/accessory-stage-v4-checkpoint-draft.json` binds46 authored artifacts and55 source/report files. Archive `truck-accessory-stage-v4-20261001.tar.gz`:17,986,617bytes; SHA256 `9671be99527ad49387a09877b824f858277e551deae81e2659a0adc6ebadb943`. Restore published accessory-layout and its predecessor chain first. Follow `docs/components/accessory-stage-v4-checkpoint-handoff.md`; this is a noninstalled candidate, with retained static/motion/service/source limitations. Original source images and manuals are excluded. Publication remains pending until a later verified note.

Publication verified after PR112 merged (`95f987449203c9ebaa88266149829324d29125c8`): [coordinated accessory v4](https://github.com/0xZakk/truck/releases/tag/studies-2026-10-01-accessory-v4), release ID401260946. Server digest/size match the values above. This supersedes publication-pending fields in frozen snapshots.


## Online-source candidate checkpoint — publication pending

`docs/online-research-candidates-checkpoint.json` binds40 authored artifacts and31 source/report files. Archive `truck-online-research-candidates-20261001.tar.gz`:5,061,563bytes; SHA256 `f76ed06430c399d467c45d4a4ee4b64c2e16bbe9e23817e91bea34e40e8a4707`. Restore coordinated accessory v4 and its predecessor chain first. Follow `docs/components/online-research-candidates-checkpoint.md`. Six ingest/OCR logs are excluded optional capture metadata, not repository prerequisites. Source images, PDFs and the manufacturer-image landmark overlay are not redistributed.

This preserves conditional heater-route candidates and an estimated local paired-duct specimen, including failed constructions/checks. Later radial-registration analysis in the repository qualifies the heater physical scale; its source overlay is local review only. No candidate is installed or production-accurate. Publication remains pending until a verified note below.

Publication verified after [PR115](https://github.com/0xZakk/truck/pull/115) merged (`2916df6880e5fd68a41b52e80ce2ea67873fc6a0`; CI18s/17sPASS): [online research candidate release](https://github.com/0xZakk/truck/releases/tag/studies-2026-10-01-online-research), release ID401293444. The server-reported SHA256 and byte count match the archive above. This supersedes publication-pending fields in frozen metadata/handoffs. Code and reports restore from PR115 or later; the packaging baseline is a provenance snapshot, not the final source revision.


## ACT replacement specimen — publication pending

`docs/act-online-20261002-package.json` records17 authored artifacts in `truck-act-online-20261002.tar.gz` (574,114bytes; SHA256 `63082663c14d3f4da96083c1f344165dad91b150c1af450d6da8c955e110a773`). Exact source/report inputs and two tracked identity prerequisites are listed separately. No generated predecessor is required. Follow `docs/components/act-online-20261002-package.md`; preservation verification streams members without extraction.

This preserves a six-region replacement-comparison specimen and rejected thread construction. It is not an installed component, complete electrical circuit or verified factory geometry. Source photographs/HTML/PDF are excluded. Publication must be verified separately.

Published after [PR117](https://github.com/0xZakk/truck/pull/117) merged at `1934fc9393b912aa8e8de09a47ea31fe4624252a` (CI21s/26sPASS). [ACT specimen release](https://github.com/0xZakk/truck/releases/tag/studies-2026-10-02-act-specimen), ID401897025, has matching server-reported SHA256 and byte count. This supersedes publication-pending fields in the frozen package metadata.


## October2 duct and pump-height candidates — publication pending

The refined duct supplement `truck-airbox-refined-20261002.tar.gz` contains31 authored files,30,445,366bytes, SHA256 `c05c425cd8c434be3bfca96c5e7a3b8fca1f4ad1cb64bb2a91e8a75d974403b4`. Restore the online-research candidate predecessor for inherited clamp assets. Exact source/dependency/member lists are in `docs/airbox-refined-20261002-package.json`. Local shape/passages/contact checks pass; numeric contours and host fit remain estimates.

The failed coordinated pump-height supplement `truck-pump-height-20261002.tar.gz` contains584 authored files,16,788,862bytes, SHA256 `a1ddb616c29bbaacd1671235832a1d079b841923fb2f6f16448f718770ab4a41`. Restore the predecessor chain enumerated in `reference/engine/pump-height-20261002-package.json`;810 external dependencies are bound to nine metadata records. All failed trials, final selected assets and actual renders are retained. This candidate FAILS integration, rear-stock preservation and aggregate mesh checks; no installation.

Both archives were independently streamed by root and matched exact member hashes. Source originals are excluded. Package handoffs describe reproduction. Publication remains pending until a verified note.

Both supplements were published after [PR118](https://github.com/0xZakk/truck/pull/118) merged at `4f1fe9da2ec177e1ff61668df66ca422e37b0b7c` (CI16s/17sPASS). [Source-candidate release](https://github.com/0xZakk/truck/releases/tag/studies-2026-10-02-source-candidates), ID401907524, has matching server-reported hashes and byte counts for both archives. This supersedes publication-pending fields in frozen metadata.


## Host research illustration — publication pending

`reference/engine/host-research-20261003-package.json` binds three authored ACT registration illustration/log outputs in `truck-host-research-20261003.tar.gz` (103,132bytes; SHA256 `dcb1631f446b177c7d3741145695bbcf5f91ab8d632a8e97230b8ff9ea1e2830`). The numerical study establishes single-view ambiguity, not an installed pose. Repository scripts/contracts/reports and the separately hash-bound installed host STEP/manual are required for full numerical replay; archive integrity verification is independent of those originals. Manufacturer/manual pixels are excluded.

Published after [PR119](https://github.com/0xZakk/truck/pull/119) merged at `16fffb7eefb7ce6e66c0922ad30b789c5f93d964` (CI17s/17sPASS): [host research release](https://github.com/0xZakk/truck/releases/tag/studies-2026-10-03-host-research), ID402592725. Server SHA256/size match the frozen three-member archive.


## Airbox body screw — publication pending

`reference/engine/airbox-screw-online-20261002-delivery.json` binds56 authored/source members in `airbox-screw-online-20261002-authored.tar.gz` (4,161,139bytes; SHA256 `4c664c8146cb743cbd4e0313b51a8b03bc44f7009ec5eb72e9dae73eeb6c8c69`). Root streamed and verified every member and inspected the actual render/catalog. Preserve newer repository dependency files before extraction; exact source/build prerequisites are listed in the ledger. Original photographs/PDFs are excluded.

This is a catalog-sized isolated replacement screw with explicit estimated head/thread/point details and preserved failed constructions. It is not installed: four body coordinates, pilot/clip and sheet stack remain unresolved. See `docs/components/airbox-screw-online-20261002-handoff.md` for build, local geometry checks and limits.

Published after [PR120](https://github.com/0xZakk/truck/pull/120) merged at `1d4e43d3a90a5769396deca5da2dbce0e1e64834` (CI23s/23sPASS): [airbox screw release](https://github.com/0xZakk/truck/releases/tag/studies-2026-10-03-airbox-screw), ID402597976. Server digest and byte count match the frozen56-member archive.


## Functional-region pump candidate — publication pending

`reference/engine/pump-functional-20261003-package.json` records a204-member authored supplement,53,260,199bytes, SHA256 `65e8271ec74edacafb6adbe4c6e4da8afd1f9b7cc525abde5e11b7b6192b2046`. Root independently verified all69 authored files,135 generated assets and839 guarded inputs, then streamed the archive without extraction. Source originals are excluded.

Restore the pump-height and accessory-v4 predecessor chains above first. Download `pump-functional-20261003-authored.tar.gz` once published, verify its hash, and extract at the repository root after preserving newer work. The archive includes authored source snapshots as well as assets; do not overwrite newer code blindly. Follow `docs/components/pump-functional-20261003-delivery.md`. The ledger's guarded inputs define exact baseline dependencies; independent source access is still required for photo review.

This is a failed installation candidate:52 valid STEP solids,51 passing meshes and one spring topology failure, with five actual-v4 clashes. Functional interface checks do not establish source accuracy, motion, service access or browser acceptance. Publication pending; no installed change.
