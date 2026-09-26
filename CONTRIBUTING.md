# Contributing

## Ownership and branches

Pick a component sub-issue under a truck-system parent issue and assign it. Agree on the coordinate frame, units (millimeters), mounting datums, adjacent-part ownership and evidence limits before modeling. Create a focused branch such as `component/123-water-pump`; use a separate worktree when working in parallel. Never have two workers edit the shared assembly builder concurrently.

Keep `main` as the integrated checkpoint. Commit a coherent component, push the branch and open a pull request linked to its issue. The integration agent reviews evidence, diffs and validation, resolves conflicts, runs relevant checks and squash-merges after checks pass. The project owner is not required to review PRs. Do not merge failing geometry or relabel an unresolved candidate as accepted merely to close a task.

## Definition of done

- Record exact vehicle/part applicability and links or captured source hashes; distinguish measured dimensions from inferred geometry.
- Supply reproducible parametric CAD, STEP and GLB outputs, part identity, assembly transform and learning/diagnostic content.
- Compare actual rendered geometry against reference images, including silhouette and interfaces.
- Check scale, solids, contacts, neighboring clearances, staged explosion and relevant motion/fluid continuity. Store input hashes, checker version, results and limitations.
- Verify individual-part navigation and installed assembly behavior in the browser.
- Report changed files, commands, source facts, assumptions and remaining blockers. Whole-assembly checks run at integration checkpoints; reuse previous results only while all relevant hashes remain valid.

## Repository checks

Run `node scripts/check-engine-navigation.mjs`. CAD work uses the environment and build instructions in `cad/engine/README.md`; run the changed component's checker and affected interface/motion checks before integration. Lightweight CI checks navigation and Python syntax; it does not substitute for CAD or visual review.

## Data and artifacts

Do not commit credentials, purchased reference originals or personal owner photos. Preserve their local source paths and reproducible evidence metadata as appropriate. Large generated STEP files belong in the private release checkpoint, with checksums and restoration instructions. Candidate files are clearly labeled and remain separate from accepted installed geometry.

Follow `AGENTS.md` for knowledge-base notes. Use focused worker briefs described in `docs/TOKEN-EFFICIENT-BUILD-WORKFLOW.md`; one integration owner handles shared files.
