# Valve-layout candidate

Unpublished cylinder1 intake/exhaust candidate. Installed files are untouched.

- `provenance.json`: static local audit, baseline hashes and assumed datums.
- `interface-validation.json`: positive seat/material and support-contact probes.
- `motion-validation.json`: latest18-pose sweep; inspect status and hashes.
- `occurrence-layout.json`: placements for the exported candidate definitions.
- `history-*` / `rejected-*`: historical checks, not current approval.

The preserved baseline is in `../valve-station/baseline/`. Do not replace the live
head/cam from these baseline-derived STEP files: apply the composable functions in
`cad/engine/valve_layout_candidate.py` to the current solids and rerun integration
checks. Full instructions and limits: `docs/VALVETRAIN-CANDIDATE.md`.

Valve, head, cam and rocker manufacturing geometry remains unverified. Only two
of twelve valve stations have been checked here. The candidate does not finish the
engine or authorize a whole-engine motion claim.
