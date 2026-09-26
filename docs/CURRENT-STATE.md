# Current integrated checkpoint — 2026-09-26

Repository root is authoritative. The preview on http://127.0.0.1:8081/viewer/engine.html now serves this checkout, not the old temporary integration directory.

Manifest SHA-256: `f725260d8f1497a1b6f2aed9d41d01155bf2a82e7391d24ce866f352bb50cd5b`. **705 definitions / 1,310 occurrences. Engine unfinished.** New provisional content: six independently explorable mechanical-seal pieces replace the water-pump seal envelope; a cable bracket and two longer estimated stud envelopes are installed with seated nuts. Actual factory seal construction, bracket dimensions, threads and cable/return linkage remain unresolved.

Verification: all 4,944 broad-phase-selected static pairs pass the 0.1 mm³ overlap convention. Bracket installed audit passes 19 exact nearby pairs, contact/nominal coverage, mesh bounds and displaced-nut controls. Pump audit passes 30 comparisons, 52 sampled explosion checks, six STEP roundtrips, flow/contact tests and fault controls. Browser and navigation pass (1,310 parts / 1,508 links). Reports are in `inventory/engine/`; these checks do not certify Ford geometry or operating performance.

Oil-cap candidate remains uninstalled because the cover lacks mating retention geometry and actual neck/thread dimensions. Its restored-baseline rocker sweep passes 181 phases across twelve rockers, minimum sampled gap 1.3754 mm. The lightweight motion-scope verifier preserves this result across unrelated changes and rejects a shifted rocker. Dipstick candidate remains rejected pending its guide-tube route.

A restoration audit found 17 missing and 32 stale local STEP definitions behind the correct viewer meshes. All were restored after matching authoritative metadata and GLB bytes; see `inventory/engine/cad-baseline-restoration.json`. Use the current archive in `docs/CAD-ARTIFACTS.md`, and validate part hashes—not merely manifest identity. The clipped seal spring required continuous CAD support bounds; tolerances were not loosened.

GitHub: Engine #1, components #15/#16/#47 remain open. Their acceptance gaps are documented; #16/#47 checklists were refreshed through gh. Project status writes remain blocked by missing Projects scope; the requested device authorization expired without completion. `scripts/set-engine-project-status.py` is ready (dry-run default, exact issue matching, guarded updates, post-write verification); run `gh auth refresh -s project` when the account owner is available. Do not report a successful board write until verified.

Next active evidence tasks: throttle linkage/return spring, oil-fill neck construction, and oil dipstick tube/block entry. Their component handoffs and source ledgers are separate from this integration checkpoint. Complete the focused branch/checked PR merge, then use these inputs for the next component cycle. Preserve source uncertainty; no package is Done from existence of a mesh.
