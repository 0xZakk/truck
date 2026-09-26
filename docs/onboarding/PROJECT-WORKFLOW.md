# Project tracking and integration

## Structure and ownership

[Project 2](https://github.com/users/0xZakk/projects/2) is the shared Kanban. Each `[System]` parent issue is an assignable workstream (our “subproject”), not a separate repository or native nested GitHub Project. The [workstream index](../github-workstreams.json) maps the 14 sections to their issues. Filter with labels such as `system:brakes`; use the Team items view for contributor ownership.

Assign a system parent to its lead, and bounded component sub-issues to individual contributors. Use `type:system`, `type:component` and the matching `system:*` label. Link dependencies by issue number and state which datum, evidence or deliverable is needed. A parent is Done only after its complete agreed component scope and system integration are accepted, not because its current child list happens to be closed.

The **system lead** agrees scope and cross-system interfaces. The **contributor** builds and validates the component. The **integration owner** serializes shared assembly changes, reviews the acceptance evidence, runs affected integrated checks and merges. Record names in the issue/PR; an agent acts through its developer's authorized account. Zach need not review PRs. Repository merge permissions still determine who can merge; this document does not grant access.

## Status rules

| Column | Enter when | Leave when |
|---|---|---|
| Backlog | Task exists; scope or dependencies not ready | Contract and prerequisites are sufficiently defined |
| Ready | Owner can reproduce baseline and has evidence/interface inputs and acceptance scope | Assigned contributor starts work |
| In progress | Active research/modeling/verification | Deliverable and handoff are ready for review |
| In review | PR/candidate package is available to integration owner | Accepted and merged, or returned with concrete failures |
| Done | Agreed task scope accepted, merged, documented and reflected in viewer where applicable | Reopen if a regression invalidates acceptance |

For a blocker, keep the issue open and state **Blocked by #… / missing …**, impact and next action. Do not use Done as “agent stopped.” Project status and issue closure can differ; verify both after merging. Existing pilot issues #15–17 remain open because their installed fit is unresolved.

## A component cycle

1. Read current state and issue. Assign the task; record baseline commit, contract, owned files, expected evidence and check commands using the common handoff. Freeze critical interface decisions before detailed geometry.
2. Start from current main in a focused branch. Example (replace number/name):

```sh
git switch main
git pull --ff-only
git switch -c component/123-example-part
```

For concurrent tasks, use a separate clone or `git worktree add -b component/123-example-part ../truck-123 main` from a clean updated checkout. Each worktree needs access to its own generated artifacts/environment. Do not share mutable output folders between workers.

3. Research → prototype silhouette/interfaces → review → detail → export/check → integrate. Keep module changes scoped. Propose neighbor changes in the issue rather than silently moving parts to make a candidate fit.
4. Save commands, full local logs, compact machine-readable reports, actual renders and hashes. Update the issue at meaningful milestones, on scope changes, blockers and handoff. Avoid repeated unchanged progress messages.
5. Commit/push the branch and open a PR using the template. Link the issue with `Refs #123` while acceptance remains open. Use `Closes #123` only when the agreed task can actually be closed. Include changed geometry, evidence limits, check scope, failure cases and artifact links.
6. Integration owner reviews the submitted revision and rubric, coordinates shared builder updates, checks affected neighbors/motion and whole-assembly consistency, and verifies the browser. Local checks and lightweight CI are complementary. After a rebase or neighbor change, rerun invalidated checks.
7. Squash-merge the checked PR; update the issue/board and `docs/CURRENT-STATE.md` for a new integrated checkpoint. Preserve unresolved candidates as candidates. Contributors pull the merged main before the next task. No owner PR approval step is required.

## Shared-file and contract changes

A worker normally owns its component source, evidence/learning and dedicated checks. `full_engine.py`, shared exporters, assembly math, the combined inventory and viewer data loaders require integration-owner coordination. Record contract changes in the handoff/PR: old versus new datum, rationale, affected components and required reruns. Agree cross-system frames before connecting engine/transmission, driveshaft/axle, suspension/frame, harness/control or hose/fluid interfaces.

## Pauses, limits and handoffs

Before a planned stop, push a labeled WIP branch if authorized and record current commit, completed steps, outstanding failures, exact next command, missing local assets and whether any process is still running. Another developer can resume from repository files and the issue; do not depend on access to someone else's Codex chat. Never claim continued autonomous work after the session or process has stopped.

## Efficiency and measurement

Follow [the efficiency workflow](../TOKEN-EFFICIENT-BUILD-WORKFLOW.md). Fresh focused briefs reference relevant files rather than carrying all history. Parallel workers require non-overlapping ownership and a single integration owner; more agents alone do not improve token efficiency.

For experiments, record model/effort, stage scope, outcome, elapsed time and available input/cached/output usage for workers **and** coordinator/rework. Reasoning is already included in output where reported that way. Mark unavailable usage as unavailable. Compare similar accepted deliverables with the same gates; the three-part pilot's candidate-only cost is not a completed-part budget. Do not mix unrelated GitHub administration into a modeling benchmark without labeling it.
