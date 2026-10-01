# Accessory v4 checkpoint handoff

## Contract

Finite preservation under engine #1 / accessory and timing #34/#32. Root publishes; this worker does not commit, install or publish. Baseline `1ba91c4ba3cafddb770270527908c6df28fc0ec5` (PR111 merge). Owned files: `scripts/accessory-stage-v4-checkpoint-package.py`, `docs/accessory-stage-v4-checkpoint-draft.json`, this handoff and generated archive. Frozen studies and shared files are unchanged.

Scope: frozen PS/AC trial1 and rejected trial0, coordinated private v4, composition/navigation/interface/solid/render evidence, actual wrong-AC-pose control, conflict reconciliation, and the previously omitted whole-engine exterior audit. Exclude all original source photos/manuals/catalogs and interrupted/aborted v4 loading attempts. Final reports may retain historical mentions of those attempts; they are not acceptance evidence or archive members.

## Delivery

Archive: `cad/engine/generated/accessory-stage-v4-checkpoint/truck-accessory-stage-v4-20261001.tar.gz`.

- 46 project-authored artifact members; 17,986,617 bytes.
- SHA-256: `9671be99527ad49387a09877b824f858277e551deae81e2659a0adc6ebadb943`.
- 55 separately verified repository source/report/handoff files in the source allowlist.
- Publication: NOT RUN. This is an unpublished candidate checkpoint.

Metadata schema is explicit: `artifact_files` and `source_report_handoff_files` are arrays of `{path, sha256, size_bytes}`. Only `artifact_files` enter the archive. `packaging_script` binds this new packager separately. `external_inputs` records `{path, sha256, classification, matching_metadata}`. `prerequisite_metadata` binds exact predecessor metadata/audit files. `inherited_manifest_web_reference_claims` resolves the 23 existing web-root source references separately; all match, without bundling originals or claiming a new source review. Root should commit the 55 source rows plus the three new packaging files; there is no need to include unrelated electrical merge work or live CURRENT-STATE in this frozen allowlist.

The source allowlist contains the exact v4 manifest; the two carrier assets remain candidate files. Their stable IDs, units, frames and estimated/source boundaries are preserved in the constituent contracts. The authored images are PS/AC trial1 context, matched v3/v4 context, and the whole-engine exterior review. None contains original photo pixels.

## Dependencies and reproduction

Required published base: `studies-2026-10-01-accessory-layout`, release ID 401248087, archive SHA `dd374011c14bec494f0647c3e84b8ff56ff3fd4e337e0f2fc6ad57bf9ac47d7b`. It follows published waterpump and the existing ordered chain through neck-core. Publication notes in `docs/CAD-ARTIFACTS.md` supersede historical NOT RUN fields in draft-named predecessor snapshots.

873 external generated inputs match exact predecessor artifact inventories or the independently verified neck-core member audit. Another 869 repository inputs and 140 separately authorized source-original dependencies have matching local hashes. No external artifact prerequisite remains unresolved. Predecessor archives were not freshly reopened in this task; this is exact metadata/member-audit matching, not a new all-archive extraction.

From repository root:

```sh
python3 scripts/accessory-stage-v4-checkpoint-package.py
python3 scripts/accessory-stage-v4-checkpoint-package.py --verify-only
```

Use Python 3 standard library; no CAD environment needed. The package is deterministic: sorted explicit names, fixed tar/gzip metadata, stream verification of every member without extraction. Rebuilding checks all artifact/source/dependency hashes before packaging. `--prepare` deliberately derives a new frozen allowlist and must not be used to hide changed input failures. Model/effort/usage unavailable.

## Validation and limitations

Exact names, ordering, member hashes, source sizes/hashes, prerequisite bindings and package script hash: PASS. Rebuild and independent `--verify-only`: PASS. Reproduction is preservation-scoped; clean-clone CAD/browser reruns are NOT RUN.

The preserved q0 solid audit has 971 exact comparisons with zero reported overlap, including 266 changed interfaces and 705 unchanged internal relations. Its actual wrong-AC-pose control detects 17,596.474199 mm³. Reconciliation clears 22 prior known conflicts and retains four unchanged pump/cover/gasket pairs. Interface evidence reuses 20 support seats, 15 clamp annuli, 20 holes and two floor/tip rows by exact asset/frame identity; it does not claim fresh contact Booleans.

Seven PS/AC pulley-blocked tool approaches, three conditional ALT/AP new-pump tool conflicts, inherited rod-bolt/block motion failures, source/retention/strength uncertainties, missing belt and plumbing/wiring interfaces, and browser restrictions remain. Archive success does not promote estimated carrier silhouettes or mark parts installed/Done.

## Tracking and restart

Root next action: review source allowlist, publish this exact archive and add release restoration instructions. No package upload or shared edits performed here. No process remains running. The assigned finite work is complete; further modeling requires new evidence or an explicit new task.
