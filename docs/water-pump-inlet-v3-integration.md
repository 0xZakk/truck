# Pump radiator-inlet V3 candidate

Uninstalled candidate only. The frozen mounting candidate is unchanged. Source identity and assumptions are recorded in `reference/engine/water-pump-inlet-v3-topology-reviewed.json`, supplementing existing source ID `water-pump-mounting-topology`. No independent inlet part is added: it is part of the one-piece housing.

## Integration

1. Copy the files listed by `inventory/engine/water-pump-inlet-v3-review.json` and the two validation reports.
2. After `water_pump_joint_candidate.housing_interface(old_housing)` has reconstructed the mounted pump, apply `water_pump_inlet_v3_candidate.housing_interface(result)` exactly once. Do not run the old-housing reconstruction again on already reconstructed geometry.
3. Keep the accepted mounting candidate's group positions, gasket, four hardware instances, impeller, shaft, fan, pulley and heater return unchanged. This adapter changes only the housing solid; counts remain unchanged.
4. Add this module's GAPS to the housing metadata. Replace obsolete claims that the radiator-inlet casting is absent with a statement that its exterior and connectivity are provisional. Keep the fifth-opening, deeper-jacket and internal-component limits. Merge the new learning JSON as appropriate.
5. Run the original installed pump checker before adding the inlet (its expected housing intentionally has no inlet). After adding the inlet, use `scripts/check-water-pump-inlet-v3-installed.py --baseline-root /private/tmp/truck-desktop-pan-v9-baseline-6b11c0f8 --candidate-report PATH_TO_ACCEPTED_INLET_REPORT`. That checker compares the installed housing to the audited reconstruction and checks ten unchanged rigid poses. It is syntax checked, not yet run against an installed build.
6. Rerun full-engine contact checks against the latest integrated engine, plus normal mesh/metadata/browser verification. This candidate's acceptance is on the frozen 6b11c0f8 baseline, not a claim about later independent changes.

## Accepted checks

- Baseline manifest `6b11c0f874bb53638b0e7fd0f477f6b7d5fca4df928bcbc918b37c98cb01d94f`.
- Full candidate audit: 56 valid single solids, 162 exact neighbor tests, no overlaps; start/end input and STEP hashes unchanged.
- Rear flange and dry nose material unchanged; open connected probe from neck to the wet chamber; retained full annular neck-wall sample; positive casting-to-housing material connection.
- No new cut through seal, bearing or slinger. Conservative full impeller rotation envelope has zero housing overlap.
- Exported housing is a valid single solid; adaptive symmetric STEP difference is zero.
- Actual assembled and inlet-axis CAD section rendered and inspected: `reference/engine/qc/water-pump-inlet-v3.png`.
- Sibling belt study reports no inlet conflict and 7.0411mm clearance to its unaccepted illustrative route. That route still conflicts with outlet pieces and is not a production belt-fit claim.

## Limits and rejected attempts

The exact Gates44009 photos show a lateral cast arm, round hose neck and retaining bead. They do not supply millimeter dimensions, mounting angle, internal volute, or impeller-eye feed. The modeled arm runs from local(-20,19,25) to(-10,60,25), then to mouth(-10,145,25). Bore radius20mm, outer24mm and bead25.5mm are assumptions, not replacement specifications.

V1 intersected the timing cover. V2 at localX10/Z−12 intersected the pulley. These are rejected, even where isolated flow checks passed. V3 relocates the whole arm above the timing cover and behind the pulley, preserving all previously proven pump interfaces. No collision exemption or per-hole notch is used. The spatial fit proves consistency with the current model, not factory accuracy.

No radiator, vehicle hose, clamp, flow simulation or hydraulic capacity is included. The pump's simplified internal bearing and seal construction remains unfinished.
