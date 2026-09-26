# Three-part efficiency pilot — 2026-09-26

Three workers received fresh focused briefs, used the same model capability, owned disjoint files and each delivered one component candidate. All three completed their bounded worker assignments. **Zero are accepted installed parts**: unchanged quality gates found unresolved interfaces and production evidence. The requested three-finished-part benchmark is therefore not yet achieved.

| Worker | Calls | Input tokens (includes cached) | Output tokens | Standard-rate equivalent |
|---|---:|---:|---:|---:|
| pilot_throttle_bracket | 31 | 2,157,665 | 9,268 | $3.29 |
| pilot_dipstick | 26 | 1,727,817 | 10,674 | $2.83 |
| pilot_oil_cap | 38 | 3,125,821 | 12,687 | $4.58 |

Total: **7,011,303 input + 32,629 output tokens**, 95 calls, **$10.70 worker-only**. Reasoning tokens are included in output. Rates are the same recorded pricing snapshot as the prior estimate; this is a counterfactual API equivalent, not a Codex charge.

Average input per call: **73,803**, versus the earlier project's **130,526**, a **43.5% reduction**. This is a descriptive context-size comparison, not proof of equal-quality cost savings. The prior workload contained harder integrated assemblies and long-running coordination. Root experiment review and GitHub administration occurred concurrently and cannot be cleanly assigned to these workers; they are excluded, so this is a lower bound on experiment cost, not an end-to-end budget.

## Quality outcome

- Oil cap: source-supported screw retention and replacement dimensions; frozen cover has no female thread. Static rocker gap 1.3754 mm does not prove moving clearance.
- Throttle bracket: source-supported topology; dimensions inferred. Existing nuts conflict; a proposed shift leaves engagement unresolved.
- Dipstick: approximate specimen length and engineering marking; calibration not invented. Trial installation intersects the block by 163.67 mm³ and is rejected.

The integration owner inspected all three CAD renders and handoffs. Keep these as candidate studies; do not change the installed engine or close their component issues. The current engine manifest stays 821f7d3b. The experiment shows that focused workers can produce useful evidence and expose constraints at modest worker cost; it does **not** establish the previously hypothesized 40–60% end-to-end savings or justify lowering the whole-truck budget yet.

## Next experiment change

Give each worker a verified interface contract before dispatch, or explicitly make interface discovery the deliverable. Choose a part whose upstream datums and evidence are sufficient to finish. Preserve focused contexts and automated checks. Measure planning, worker work, integration and rework in a dedicated run separate from repository administration so total cost can be compared fairly.

## Coordinator accounting

At 2026-09-26T14:59:34.772Z, the coordinator had used 7,772,728 input and 16,260 output tokens since this request: **$9.64** standard-rate equivalent. This combines pilot planning/review with repository consolidation, GitHub issues/board setup and archiving. Adding all of it to the workers gives **$20.34** through that snapshot, but overstates pilot-specific cost. The snapshot excludes subsequent final administration. A clean end-to-end pilot allocation is unavailable; worker-only cost must not be presented as the full cost.
