# Component contract: expanded seat v3 block

Issue #32/engine #1; root owns integration. Baseline70542fad9de467a5c03ad54a6f54def8550956eb, branch engine/timing-interface-integration. New isolated module/checks/reports/generated directory named v3; all prior geometry/reports/failures frozen. Same original combined block and frozen front adapter, shared v2 API SHA4fa9d104606158710bb221fcfc71ca5dcddb62bf00243338920e92adb8f9839e, pan SHAd7f495ec95b0cc465880c72ae38f6e873f5ee30cdbebecf4a1613a7cbe6e5b3f and gasket SHA8e968afca78cf09e81e678307b24d59a78cbe251210983a4eb5f6981619d6936. World millimeters, original transforms and axes. No canonical edits or source originals.

Root authorized one bounded change from failed v2: apply the same shared `transition_below_seat()` after restoring old socket-region stock. This removes obsolete sloping stock below the new R10 flat−24.5 seat; it does not shrink the guard or change threads. Prior15.059289mm³ gasket collision remains as negative evidence in frozen v2. The complete R10 socket region may now change only inside the declared functional below-seat mask or the separately approved station20 source bore cavity. Sourcefemale beginningZ−24.3, complete bore wall and floor remain protected; material outside both masks unchanged. V2's source bore-minus-female reconstruction, R10 flat pads and explicit10mm upper support are unchanged. No actual neighbor carve.

Required gates inherit v2: valid single solid/exact STEP1e−5mm³; watertight directGLB0.15mm bounds; exact boundedmaterial; rear<=300/deck/feet/20retainedpan/main/cam/retention/wet guards; front>=365 except declared station20 cavity; sourcefemale/floor/bore equivalence; actual pan/gasket/bothmales/cover/core/pumps; full analytic gasket backing and actual translated-face support. Existing strict quadrature convergence1e−7 unchanged. Factory fidelity, strength, whole oil containment, hardware torque/BOM, motion, browser and installed acceptance remain open.

Command: `XDG_CACHE_HOME=/tmp/truck-cache .venv-cad/bin/python scripts/check-timing-front-block-expanded-seat-v3-candidate.py`. Pair and source restoration scripts use matching v3 names. Environment macOS/Python3.13/build123d0.10.0, no dependency changes. Model/effort/usage unavailable. Root owns publication/review. Delivery pending; no release URL.

## Pair and socket delivery checkpoint

Saved STEP SHA `66917915d9244f49cd96c2965315cba4bbb7007b236d36de67ac7c32fe4635b8`. `inventory/engine/timing-front-expanded-seat-v3-pair.json` PASS: block/pan, block/gasket, pan/gasket, male10/block and male20/block each0mm³ overlap; analytic upper and lower backing missing0; actual gasket translated upper/lower support missing0. This proves the scopedX300..365 joint, not the entire oil cavity or inherited rear gasket region.

`inventory/engine/timing-front-socket-v3-source-restoration.json` PASS: intended source void clear; complete bore+floor material matches sourcefutureland; source female retained; old union168.469254mm³ unintended bore stock detected as negative control; repair outside declared cavity/belowseat mask0. `inventory/engine/timing-front-v3-socket-walls.json` independently verifies complete physical annular wallR4.17..6.2 (2.03mm modeled radial thickness) and source1mm floorlocal22.6..23.6 at both10/20, with no missing material in source or candidate. These dimensions are model guards, not strength or factory minimums.

Reproduction supplements:

```sh
XDG_CACHE_HOME=/tmp/truck-cache .venv-cad/bin/python scripts/check-timing-front-expanded-seat-v3-pair.py --pan-sha d7f495ec95b0cc465880c72ae38f6e873f5ee30cdbebecf4a1613a7cbe6e5b3f --gasket-sha 8e968afca78cf09e81e678307b24d59a78cbe251210983a4eb5f6981619d6936
XDG_CACHE_HOME=/tmp/truck-cache .venv-cad/bin/python scripts/check-timing-front-socket-v3-source-restoration.py
XDG_CACHE_HOME=/tmp/truck-cache .venv-cad/bin/python scripts/check-timing-front-v3-socket-walls.py
```

Syntax checks passed. Full native export/neighbor checker remains running at this interim checkpoint; final results follow. Candidate only, source/application/strength/motion/containment/browser/installation remain open. Earlier frozen trials are negative evidence, not superseded factual passes. Parent owns review, issue updates and asset release.

## Export review and aggregate-metric limitation

Actual native/exported block remains one connected valid solid. Direct GLB readback is one watertight component with consistent winding and positive volume. Both `block-glb-review.png` and `pair-glb-review.png` were visually reviewed; the latter is a centroid-based mesh crop, so its open cut boundaries/edge triangles are visualization artifacts, not CAD modifications. Input and render hashes: `inventory/engine/timing-front-v3-visual-review.json`.

Native and independent saved-STEP whole changed-material accumulation both encountered strict quadrature nonconvergence. Total removed-material and total removed futureland metrics must be marked **NOT VERIFIED**, not precise accepted measurements. Logs `validation.log`, `saved-step-validation.log`, and `delivery-validation.log` preserve failures. `timing-front-v3-material-integration-diagnosis.json` independently decomposes a direct saved-STEP difference into5 added/7 removed solids, each converging at the unchanged criterion; that supplemental run sums16885.545448mm³ added and1716.859882mm³ removed. The contradictory aggregate behavior remains explicit; this independent result does not silently change the failed aggregate gate or relax numerical thresholds. No further healing or repeated precision search is planned.

The final delivery checker records individually verified and unverified fields and retains an aggregate FAIL when a required metric is unverified. It reconstructs the same native source without rewriting exports, rechecks protected regions and native/STEP equivalence, and binds the complete native-neighbor log as provenance for those completed checks. This distinction permits scoped functional review without claiming a full validation pass. Installed source fidelity, whole oil containment (including inherited rear gasket support issue), torque/hardware BOM, motion and browser remain open. Cover neighbor here is frozen attachment-v2; root must compose/recheck the separate2692 seal-cover candidate at integration.

## Frozen delivery — 2026-10-01

Final report `inventory/engine/timing-front-block-expanded-seat-v3-delivery-validation.json`: **aggregate FAIL**, solely because required aggregate changed-material verification is incomplete. `removed_mm3` and `future_land_missing_mm3` are null with explicit strict convergence errors in `unverified_metrics`; neither is zero or an accepted precise total. All other declared gates PASS: valid one-solid native/STEP, zero native-to-STEP difference, watertight GLB bounds0.006842475mm, bounded material, protected interfaces, all actual neighbors, futureland retained outside transition, source socket void and full gasket backing. Added volume converges16885.545448mm³; added/removed material outside declared masks each0. Futureland missing outside authorized transition0. The separate complete pair, sourcefloor and wall reports also PASS.

All current input hashes in the delivery/pair/source/wall/material-diagnostic/visual reports were rechecked and match. Geometry, scripts, reports and renders are now frozen; no processes remain for this work. No canonical component or shared inventory was modified. Root inspected actual renders and owns publication/integration. This is a reviewable bounded candidate with two metric gaps, not full installed acceptance. Asset release URL remains pending root packaging. Browser remains NOT RUN under prior security block; do not bypass.

Final commands:

```sh
XDG_CACHE_HOME=/tmp/truck-cache .venv-cad/bin/python scripts/check-timing-front-block-expanded-seat-v3-delivery.py
XDG_CACHE_HOME=/tmp/truck-cache .venv-cad/bin/python scripts/render-timing-front-block-expanded-seat-v3.py --extract
MPLCONFIGDIR=/tmp/truck-gear-mpl python3 scripts/render-timing-front-block-expanded-seat-v3.py
XDG_CACHE_HOME=/tmp/truck-cache .venv-cad/bin/python scripts/render-timing-front-expanded-seat-v3-pair.py --extract
MPLCONFIGDIR=/tmp/truck-gear-mpl python3 scripts/render-timing-front-expanded-seat-v3-pair.py
```

Delivery checker intentionally exits nonzero for aggregate FAIL after saving its report. Native checker also retains its original strict-volume failure. Do not rerun exporters merely to hide these gaps. Exact next integration action: package this frozen scoped candidate with matching panv2 and separately reviewed seal candidate, retain both metric gaps and inherited rear gasket/containment/browser/hardware issues, then compose only through root. Cover bolt/seat research continues separately.

Frozen SHA-256:

- `inventory/engine/timing-front-block-expanded-seat-v3-delivery-validation.json`: `154635a0a2ada559cf7c8165eda42698415e28a52ff821076a644df94e5e8370`
- `inventory/engine/timing-front-expanded-seat-v3-pair.json`: `ed6b1947ff8b61cf2061f4afac22f3fd1f4dfd88efc1b41ccc77c12456832dc8`
- `inventory/engine/timing-front-socket-v3-source-restoration.json`: `1579d685249f3e1f2cd087cbe46ed6ff957b6092f36704770b76429a6cd73aae`
- `inventory/engine/timing-front-v3-socket-walls.json`: `fe22eef61e98b1a274bb5801eb4932666e90c5dc14204c8f4b611cf8cc00ff79`
- `inventory/engine/timing-front-v3-visual-review.json`: `3776060beff64a602eb48e017282d40c0d21dc2764ab40afbef1aaf92705d40a`
- `cad/engine/generated/timing-front-block-expanded-seat-v3-candidate/block.step`: `66917915d9244f49cd96c2965315cba4bbb7007b236d36de67ac7c32fe4635b8`
- `cad/engine/generated/timing-front-block-expanded-seat-v3-candidate/block.glb`: `68899221bcb4ded05a9fe285aecb770bb23c03a805b9e1032c0000da813d0441`
- `cad/engine/generated/timing-front-block-expanded-seat-v3-candidate/block-glb-review.png`: `0e2d170976d757ceca8ce22fd06e99cb1714264fee031bc4d548975bf2c45ab7`
- `cad/engine/generated/timing-front-block-expanded-seat-v3-candidate/pair-glb-review.png`: `b7500ca76f8a38489e7f7e697de25a809bad279077b0393310f3e59914a48b6a`
