# Restore the engine CAD checkpoint

Browser meshes, modeling source and validation reports are committed to Git. Generated STEP files live in private GitHub release archives because the combined assembly exceeds normal GitHub file limits. Browser exploration needs only the committed GLBs.

## Current intake and attachment checkpoint

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
