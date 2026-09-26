# Interactive 1994 Ford F-150 reconstruction

Component-level CAD, an interactive engine explorer, and a source-linked knowledge base for a white 1994 F-150 XLT SuperCab, short bed, 2WD, 4.9L inline-six and M5OD-R2 manual transmission.

This is an educational reconstruction in progress. Geometry carries evidence and uncertainty; export success and collision checks do not establish factory accuracy. The truck's emissions calibration remains unconfirmed.

## Explore

Run `python3 -m http.server 8081` from this directory, then open http://127.0.0.1:8081/viewer/engine.html . The committed viewer and engine meshes work without a CAD installation.

## Collaborate

**New developer or Codex agent? Start with [the onboarding guide](docs/onboarding/START-HERE.md).** It covers setup, the shared quality rubric, task contracts, tracking and handoff.

- [Truck Kanban](https://github.com/users/0xZakk/projects/2): Backlog → Ready → In progress → In review → Done.
- [Complete current engine parts backlog](docs/engine-parts/README.md), including known missing scope and acceptance status.
- [Assignable system workstreams](docs/github-workstreams.json): each parent issue owns a major truck section; component issues belong beneath it.
- [Contribution and merging workflow](CONTRIBUTING.md).
- [Efficient modeling workflow](docs/TOKEN-EFFICIENT-BUILD-WORKFLOW.md).
- [CAD pipeline](cad/engine/README.md), [engine completion](docs/ENGINE-COMPLETION.md), and [knowledge base](kb/).

`In review` means engineering/agent validation; the owner does not need to review pull requests. Assign the system issue to its lead and individual component issues to contributors.

## Repository layout

`cad/engine/` contains parametric source; `models/engine/` contains browser meshes; `inventory/engine/` contains assembly, evidence and validation records; `viewer/` contains the interactive site; `kb/` contains source-linked explanations. `pilot/` folders hold the bounded efficiency experiment and are not automatically accepted into the installed model.

Purchased manuals and owner photographs remain local. Large generated CAD checkpoints are stored as private release assets; see [artifact restoration](docs/CAD-ARTIFACTS.md).
