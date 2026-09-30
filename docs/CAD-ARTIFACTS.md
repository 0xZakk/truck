# Restore the engine CAD checkpoint

Browser meshes, modeling source and validation reports are committed to Git. Generated STEP files live in private GitHub release archives because the combined assembly exceeds normal GitHub file limits. Browser exploration needs only the committed GLBs.

## Prepared rear-exhaust and timing-study checkpoint

The September30 exhaust/timing archive is prepared for PR #95; publication is pending. It preserves **741 definitions / 1,349 occurrences**, the installed rear collector and separate timing studies. Browser acceptance remains NOT RUN; the engine is unfinished.

After publication, restore using:

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
