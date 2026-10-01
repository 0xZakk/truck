# Accessory layout checkpoint handoff

## Contract

- Issue: engine #32; integration and publication owner: root. Scope is finite reproducibility preservation, not modeling or installation.
- Baseline: `488c9d76ef2eff541cd8586588720cfc01034ab6`, shared `engine/timing-drive-fit` branch. No assembly or occurrence transforms changed.
- Owned files: `scripts/accessory-layout-checkpoint-package.py`, `docs/accessory-layout-checkpoint-draft.json`, this handoff, and the generated archive under `cad/engine/generated/accessory-layout-checkpoint/`.
- Six frozen delivery ledgers define the source allowlist: block-FS10 investigation and source/datum delivery, right-contour delivery, common-layout discovery, constrained-layout delivery, and matched-carriers delivery. Full paths and hashes are in metadata.
- Excluded: active `accessory-psac-carrier*`, original photographs, manuals, catalog captures, and the old source-image comparison composite. No shared files or previous studies modified.
- Units/frames, physical interfaces and source fidelity inherit each study unchanged. New dimensions, placements, learning lessons and installed acceptance are N/A.

## Evidence ledger

| Preserved evidence | Binding | Limit |
|---|---|---|
| Frozen source/datum and layout work | 175 delivery hash claims checked | Prior failures remain failures |
| Authored artifacts through ALT/AP trial 6 | 96 exact archive members | Includes rejected trials, source snapshots, witnesses and authored renders |
| Source/report/handoff allowlist | 91 exact files and sizes | Stored in repository, not duplicated inside artifact archive |
| Legacy inputs missing from predecessor inventories | Nine explicitly named supplemental artifacts | Includes current canonical block STEP; does not replace predecessor archive or mutate canonical |
| External report inputs | 883 exact current hashes: 716 repository inputs, 163 predecessor artifact matches, four excluded originals/composites | Originals are separately authorized dependencies, never bundled |
| Predecessor chain | Eleven release/archive hash links from ignition connections back through neck-core | Uses published metadata and existing neck-core member audit; other archives were not freshly reopened |

## Delivery

- Archive: `cad/engine/generated/accessory-layout-checkpoint/truck-accessory-layout-studies-20261001.tar.gz`.
- Size: 22,027,686 bytes. SHA-256: `dd374011c14bec494f0647c3e84b8ff56ff3fd4e337e0f2fc6ad57bf9ac47d7b`.
- Publication: NOT RUN; root owns release creation and final restore documentation. Waterpump study archive remains a draft dependency until root publishes it.
- Archive stores only explicitly allowlisted generated files. The package script never extracts or publishes. Deterministic tar/gzip metadata makes rebuilding identical input bytes reproducible.
- Environment: Python 3 standard library, macOS; no CAD or renderer execution needed. Model/effort and billing unavailable.

From repository root, rebuild against the existing frozen allowlist with:

```sh
python3 scripts/accessory-layout-checkpoint-package.py
python3 scripts/accessory-layout-checkpoint-package.py --verify-only
```

`--prepare` deliberately derives a new metadata snapshot from the six source deliveries. Do not use it merely to bypass a changed-file failure. Review any new allowlist or input revision first.

Restore prerequisites in reverse order of `prerequisite_chain_in_reverse_restore_order`, following the installed neck-core predecessor instructions in `docs/CAD-ARTIFACTS.md`, then restore the waterpump study archive, then this archive. Review the nine named supplemental inputs before restoring onto an existing checkout: the intended target is a clean reproduction directory. Commit the 91 source/report files with their exact recorded hashes and preserve the repository inputs listed in metadata. The packager verifies predecessor metadata hashes, all locally available external inputs, every source row and every streamed archive member, without overwriting any artifact.

## Validation and review

| Gate | Result | Scope |
|---|---|---|
| Application/coverage | PASS for requested freeze | Source/datum, common/constrained, ALT/AP through trial 6; PS/AC active work excluded |
| Dimensions/coordinates, CAD/export, source comparison | N/A new checks | Existing reports and renders preserved without reclassification |
| Installed interfaces, motion/disassembly | NOT RUN | No new acceptance; inherited conflicts and estimates remain |
| Learning/browser | N/A / NOT RUN | No runtime or learning changes |
| Reproduction | PASS | Exact member names/order/hashes, source sizes/hashes, no duplicate archive members, metadata and dependency hashes |
| Full clean-clone CAD rerun | NOT RUN | Archive fidelity is narrower than full model reproduction |

The eleven release-chain links are validated against their declared archive hashes. The 163 prerequisite artifact mappings identify exact path/hash records; this does not claim fresh byte verification of every predecessor archive. Source originals remain unavailable in a public clone by policy. Authored landmark/geometry plots contain no copied original pixels; the Dorman original and image composite are explicitly excluded.

## Tracking and restart

- No commit, upload or shared manifest edit performed. No modeling resumed.
- Root next action: review metadata/source allowlist, publish archive, commit source files, and resolve waterpump release identity in final restoration instructions. This does not close engine #32 or mark carriers installed.
- Running process: none after verification. Usage unavailable.
