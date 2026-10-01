# Accessory pose serialization contract

Root integration owner; engine #1 / coordinated timing #32. Baseline PR110; input frozen privatev3 and constrained-layout step-check. Own this handoff, scripts/check-accessory-pose-serialization.py and inventory/engine/accessory-pose-serialization.json. No canonical or frozen manifest edits.

Scope is coordinate serialization only: move six named accessory assembly roots by the frozen inferred group deltas, counter-transform fixed engine bolts inherited under a moving parent, and move separately parented accessory fasteners. Preserve all internal frames/motion metadata and part identities. Check every occurrence world transform against independent world-translation expectations at varied crank, cam-endplay, throttle and compressor states. This proves frame consistency, not solid clearance or factory placement.

Declared tolerance1e-8 in homogeneous matrix elements (millimeter translation, dimensionless rotation). Negative controls must expose missing engine-bolt counter-transform and double-moving compressor parts. Carriers remain replacement obligations; no complete stage produced. Body hoses, belt, source silhouette, physical interface/motion, CAD/export and browser acceptance remain outside this pose-only check. Candidate geometry checks must be rebound after both support assets freeze.

## Delivery

PASS8,166 occurrence-frame comparisons over six explicit crank/endplay/throttle/compressor states. The proposal changes six assembly positions and eleven separately parented/fixed occurrence positions (17 guarded edits total). Both missing fixed-engine-bolt counter-transform and double-translated compressor faults fail as intended. Actual final edits/input hashes/states are in inventory/engine/accessory-pose-serialization.json. Run `.venv-cad/bin/python scripts/check-accessory-pose-serialization.py`; Python3.13/build123d0.10 environment. No manifest/geometry written.

The input position hypotheses remain inferred. This serializes their declared world translations without shifting fixed engine anchors or breaking compressor motion axes; it does not select those poses as factory geometry. Root may compose a new private stage only after binding both frozen carrier assets and running affected combined geometry checks.
