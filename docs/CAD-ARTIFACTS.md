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
