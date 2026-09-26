# Start here: developers and Codex agents

## What we are building

An interactive, mechanically coherent reconstruction of one white 1994 Ford F-150 XLT SuperCab, short bed, 2WD, 4.9L inline-six, M5OD-R2 five-speed. The owner knows of no modifications; that is owner testimony, not proof every component is original. Emissions calibration remains unknown because the identifying label was not found.

The goal is individual physical parts, reusable geometry definitions and separately identifiable installed occurrences, assembled to scale. Users should isolate systems, select a component, see how it works, explore motion/explosion and understand common faults. A convincing exterior shell or generic engine does not satisfy this goal. Engine work is the current focus; the board covers the entire truck.

## Your first session

1. Obtain access to the private [repository](https://github.com/0xZakk/truck) and [project board](https://github.com/users/0xZakk/projects/2) from the owner. Repository and project access may differ. Use your own GitHub account and Codex sign-in; do not copy another person's credentials or local Codex configuration. This project does not require a shared API key or custom plugin.
2. Clone the repository and open the checkout as your Codex project. The conversation history is not a dependency. Read root `AGENTS.md`, [current state](../CURRENT-STATE.md), [workflow](PROJECT-WORKFLOW.md) and [quality standard](QUALITY-STANDARD.md).
3. Preview the committed build before generating anything. Clone from your projects directory (skip the first two commands if already inside your checkout):

```sh
git clone git@github.com:0xZakk/truck.git
cd truck
python3 -m http.server 8081
```

Open http://127.0.0.1:8081/viewer/engine.html . Stop the server with Ctrl-C. Choose another port if occupied. The meshes are committed; no CAD installation is needed for this preview. The viewer uses a pinned external Three.js CDN, so it needs network access. Inspect a part page, system isolation, explosion and motion.

4. In another terminal, run `node scripts/check-engine-navigation.mjs` and `python3 -m compileall -q cad scripts tools`. Node 22 and Python 3.12 are used by lightweight CI. These are onboarding checks, not proof the engine is complete.
5. Claim one bounded sub-issue beneath a system parent. Complete the [task contract](../templates/COMPONENT-HANDOFF.md) before modeling. Confirm needed source files, mounting datums and neighboring geometry actually exist locally. If missing, make evidence/interface discovery the task; do not promise a finished installed part.
6. Make your first delivery small enough for the integration owner to compare with the common quality rubric. Do not start an entire transmission independently before agreeing on its frame and engine/clutch/driveshaft interfaces.

## CAD environment and reference assets

The tested CAD lock is `cad/requirements-engine-lock.txt` (macOS / Python 3.13); it is separate from the root knowledge-base requirements. On a compatible environment:

```sh
python3.13 -m venv .venv-cad
.venv-cad/bin/python -m pip install -r cad/requirements-engine-lock.txt
.venv-cad/bin/python -c "import build123d, trimesh; print('CAD imports OK')"
```

On Windows use the environment's `Scripts/python.exe`. Other platforms may need a compatible environment using `cad/requirements-engine.txt`; record the actual package versions and any changes, and verify exports before using that environment for accepted geometry. Do not silently update project pins. Rendering scripts have additional dependencies identified by each task; the CAD import smoke check does not cover them.

Restore required generated STEP baselines using [CAD artifact instructions](../CAD-ARTIFACTS.md) before running checks that import them. Do not run `first_assembly.py` or a whole-engine refresh just to preview the site: they write generated output. Some historical builders/checkers depend on specific intermediate stages or original-machine paths. Inspect the selected command's inputs and outputs, adapt paths in your isolated branch, and document any portability limitation. A clean-clone full rebuild is not yet guaranteed.

Purchased manuals and owner photographs are intentionally absent from Git. Ask the system lead for authorized access, or use a cited public source. Never reconstruct a missing measurement from a screenshot as if it were measured. The source ledger should identify what was available to the worker and reviewer.

## Starting prompt for your own Codex session

Replace ISSUE_URL before using this prompt:

> Work on ISSUE_URL in this repository. Read AGENTS.md, docs/onboarding/START-HERE.md, docs/CURRENT-STATE.md, the issue, and the shared quality standard. Summarize the task scope, baseline, owned files, interfaces, evidence gaps and acceptance checks in the component handoff before editing. Use a focused branch. Build and verify the bounded deliverable, preserve source facts versus assumptions, and leave a reproducible handoff and PR. Do not promote unresolved candidate geometry or claim Done from export success. Keep the issue updated with consequential progress and blockers. Do not merge unless acting as the authorized integration owner.

Codex supports repository instructions through `AGENTS.md`; see [official instructions documentation](https://learn.chatgpt.com/docs/agent-configuration/agents-md). Personal instructions can differ, so explicitly ask the agent to identify conflicts with this project's process. The previous pilot used GPT-6 Astra medium; record your actual model/effort if available rather than assuming subscriptions offer identical settings. Comparable quality comes from evidence and acceptance checks, not identical prose or model selection.

## Where information lives

| Information | Authoritative location |
|---|---|
| Assignment, ownership, dependencies, board status | GitHub issue / Project 2 |
| Current integrated checkpoint and caveats | `docs/CURRENT-STATE.md` |
| Installed hierarchy, IDs and transforms | `inventory/engine/full-assembly.json` |
| Parametric source / browser meshes | `cad/engine/` / `models/engine/` |
| Evidence, dimensions, learning and validation | Relevant `inventory/engine/` records and `kb/` sources |
| Component acceptance and reproducible handoff | Task handoff linked from issue and PR |
| Historical research and failed approaches | Relevant older docs/candidate records; retrieve on demand |

The [pilot results](../pilot/RESULTS.md) are a useful negative example: three useful candidates, zero accepted installations. They demonstrate how to report gaps honestly, not a quality-approved template to copy blindly.
