# Common alternator / Thermactor carrier candidate

This is an explicitly approximate one-piece carrier study informed by photographs of Ford casting F4TE-10239-AC. The two accessory stations, four engine seats, mounting ears and all fasteners remain fixed. Its continuous spine connects open accessory cradles. Casting contours, rib sections and the correspondence between photograph holes and model seats remain assumptions; this is not an exact OEM casting replica or a belt-fit correction.

## Integration

1. Copy `cad/engine/alt_thermactor_common_carrier_candidate.py` and retain its frozen dependencies: `accessory_brackets.py`, `alternator_carrier_1994_candidate.py`, and `water_pump_thermactor_foot_candidate.py`. Register source `ford-alt-thermactor-shared-carrier` from `reference/engine/ford-alt-thermactor-shared-carrier-reviewed.json`.
2. Remove definitions and occurrences `alternator-support-bracket` and `thermactor-support-bracket` from the assembled inventory; do not duplicate them behind the new casting.
3. Define `alternator-thermactor-common-carrier` using `carrier()` from the new module. Geometry is already in world CAD coordinates. Add one occurrence with the same identifier, identity placement and rotation, under the accessory-drive hierarchy. Preserve existing engine-interface adapters and all accessory/engine fastener occurrences.
4. Definition and occurrence counts each decrease by one. No head/block/pump adapter, accessory position, pulley datum or hardware change belongs to this integration.
5. Run the full neighbor/contact/roundtrip checker against saved installed geometry:

   `.venv-cad/bin/python scripts/check-alt-thermactor-common-carrier.py --assembly-root <root> --installed`

   The checker compares actual saved geometry/pose to the candidate and uses that saved shape for clearance and contact checks. Run the separate continuity control:

   `.venv-cad/bin/python scripts/check-common-carrier-load-path.py`

The provisional Thermactor mounting ears are on `thermactor-front-plate`, not its cylindrical housing. The initial checker selected the wrong contact target and reported its real17.889mm separation; that diagnostic is retained as `alt-thermactor-common-carrier-initial-checker-error.json`. Correcting the target does not alter geometry or tolerance.

## Review limits

The source photographs show one ribbed casting and its stamp. Their perspective does not establish orientation, scale, centers, hole axes or exact accessory-ear assignment. The bracket's approximate constructed contours should remain clearly distinguished from measured parts. In particular, retaining existing station assumptions does not resolve the current belt/outlet interference or nominal belt-length residual.

Preview: `reference/engine/alt-thermactor-common-carrier-preview.png`. Full-engine baseline: frozen manifest c2ea58608b4f6e24a72c0d7b3c862202230fde7cce9dc5292774cb7635359fb1.
