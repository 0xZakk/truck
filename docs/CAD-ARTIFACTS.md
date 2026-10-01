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
