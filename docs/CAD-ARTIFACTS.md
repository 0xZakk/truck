# CAD checkpoint restoration

The source, assembly inventory, validation reports and browser meshes are committed to Git. Generated STEP files and candidate baselines are bundled in the private [2026-09-26 checkpoint release](https://github.com/0xZakk/truck/releases/tag/checkpoint-2026-09-26). They exceed normal GitHub file limits and should not be repeatedly duplicated in Git history.

Download once using an account with repository access:

```sh
gh release download checkpoint-2026-09-26 --repo 0xZakk/truck --pattern truck-cad-checkpoint-20260926.tar.gz --dir /tmp
shasum -a 256 /tmp/truck-cad-checkpoint-20260926.tar.gz
```

Compare the checksum with `docs/cad-checkpoint.json`, then extract from the repository root:

```sh
tar -xzf /tmp/truck-cad-checkpoint-20260926.tar.gz
```

The archive restores `cad/` generated files and candidate inputs for the integrated manifest recorded in that JSON. Extraction replaces generated files at those paths; preserve any newer local CAD outputs first. Purchased manuals and owner photographs are excluded. Browser exploration needs only the committed GLBs. Historical scripts may still reference their original temporary workspace paths; adapt those paths before reproducing an old audit and do not treat a saved report as a fresh check.

## Current engine interface checkpoint

The original archive above is historical. A promotion audit found that the local active STEP set did not fully match the promoted manifest/GLB: 17 files were missing and 32 existing files were stale. See `inventory/engine/cad-baseline-restoration.json`. Do not trust a matching manifest hash alone while using arbitrary local STEP files.

For the current 705-definition / 1,310-occurrence checkpoint, restore the [active CAD archive](https://github.com/0xZakk/truck/releases/tag/checkpoint-2026-09-26-interfaces):

```sh
gh release download checkpoint-2026-09-26-interfaces --repo 0xZakk/truck --pattern truck-active-cad-20260926-interfaces.tar.gz --dir /tmp
shasum -a 256 /tmp/truck-active-cad-20260926-interfaces.tar.gz
# Compare against docs/cad-interface-checkpoint.json before extracting.
tar -xzf /tmp/truck-active-cad-20260926-interfaces.tar.gz
```

This archive contains every active part STEP and the regenerated combined STEP. If a historical candidate study needs the old archive's extra assets, extract the old archive **first**, then overlay this one. Preserve newer local generated work before extracting either archive. Per-part hashes are recorded in `inventory/engine/combined-step-export.json`; the active archive contains no purchased manuals or owner photos.

To regenerate the combined STEP after a reviewed manifest change without rebuilding all component geometry:

```sh
XDG_CACHE_HOME=/tmp/truck-cache .venv-cad/bin/python scripts/export-engine-assembly-step.py
```

The bounded interface installer is `scripts/install-engine-component-interfaces.py --apply`; it uses the shared exporter and preserves unrelated inventory. Its new spring bounds use continuous CAD support distances because the CAD kernel's conservative box overstates a clipped helix's axial length. This does not relax the 0.5 mm mesh comparison tolerance or establish factory dimensions.
