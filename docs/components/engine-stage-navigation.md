# Component handoff: candidate engine navigation

## Contract

Root integration owner, issue #32 under Engine #1. Baseline PR104 `8c2d2d9a1400acf784e04581a61e6a6ede38d3ba`. Scope is an isolated navigation adapter for the frozen corrected-engine v2 manifest, not installed CAD or browser acceptance. Owned files: `viewer/engine-stage-navigation.js`, `scripts/check-engine-stage-navigation.mjs`, `inventory/engine/engine-stage-navigation-validation.json` and this handoff. Canonical inventory and atlas remain unchanged.

Preserve all physical IDs, hierarchy and millimeter transforms. Replace the obsolete one-piece front-seal route with an explicit alias to the three-part assembly. Keep candidate links in their candidate context. No new physical dimensions or service specifications are asserted.

## Delivery and reproduction

`buildStageNavigation(manifest)` wraps the existing navigation builder and requires the corrected motion revision. It validates aliases, resolves legacy links and retains `stage=timing` in generated URLs. This query is preparatory: atlas does not yet load the candidate or this helper.

Run `node scripts/check-engine-stage-navigation.mjs`. The report binds the exact manifest, navigation, learning modules and checker. It checks all 1,361 occurrences and 1,561 navigation nodes, reachable ancestry without cycles, deep-link round trips, three legacy seal query forms, 174 resolved lessons and 417 part links. Missing alias targets fail the negative control. The manifest is unchanged after the check.

## Review and acceptance

Navigation and learning-reference checks PASS. Browser selection, isolation, explosion and visual review remain NOT RUN. Motion correctness and CAD interfaces are outside this adapter's scope; the stage's 77 known overlapping pairs are not waived. CAD export/source comparison are N/A for this code-only change. No external files or credentials are needed for the Node check beyond repository data. Runtime/model billing details are unavailable.

Readiness: candidate. Next action is a coordinated atlas runtime/data-loader integration after geometry and motion dependencies are resolved, followed by authorized browser acceptance. No component issue is closed by this helper.
