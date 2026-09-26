# Seal readiness on accepted inlet revision

The existing six-part illustrative seal module is unchanged and passed against inlet manifest `2032a3dae31b2ae012752e79ba814e616c5406fb0a940336383358a91f8dc421`. Its geometry hash remains `63bf8b89e98d88112a6976afc768a3906eee8cbdd4ebb70f9a43d9362fcbbb9e`.

A complete immutable snapshot of698 definitions was copied to `/private/tmp/truck-seal-inlet-baseline-2032a3da`. The source manifest and every STEP hash were checked before/after; the housing byte-matches the accepted inlet snapshot. This audit does not read the changing live builder.

## Results

- Six valid single solids;30 static neighbor/pair checks;52 sampled pump-study explosion checks; zero collisions.
- All intended material contacts retained, with637.7433mm² annular sealing-face contact. All six STEP comparisons passed.
- Idealized wet/dry voids remain separate. Negative controls confirm that removing the bellows or opening a0.1mm face gap connects them, so the separation test detects both failure modes.
- The unchanged composable `build((define,add,group))` API was exercised in a private temporary manifest, replacing one envelope with six parts. The preparation manifest has703 definitions and1310 occurrences.
- The installed comparison checker passed against that private harness's six audited STEP exports, rigid poses and explosion offsets. This is preparation, not proof of an installed/published engine change.

Use `docs/water-pump-mechanical-seal-integration.md` for integration, source registration and learning. The installed comparison accepts the new readiness report via `--candidate-report`. Run it again on the real integrated export, then run current full-engine/browser checks. No shared builder or live manifest was changed by this followup.

The source and applicability limits are unchanged: generic manufacturer seal architecture, not verified Gates44009 internals. Bearing row arrangement remains unidentified.

Frozen file hashes and report paths: `inventory/engine/water-pump-seal-inlet-readiness-review.json`.
