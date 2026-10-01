# Component contract: coordinated front block adapter candidate

Issue #32 under engine #1; root integration owner; historical creation branch `engine/timing-clearance-revisions`, creation baseline `4e480f8`. NEW isolated candidate; all research and prior geometry frozen. Input is root combined block `cad/engine/generated/timing-block-combined-candidate/block.step`, SHA-256 `72773d2ce6793180ff828d3d8ddf089daea3d85b738962084d335ca4a17c1a36`.

Root authorized a bounded estimated adapter trial after the source/owner research. Declared sequence: close only five retired source blind bores within their original physical boss height; remove the three functional source masks (main dry region aheadX373; source upper clamp band X365..373; source rising front pan underside fromX335); unite the frozen `timing-cover-attachment-v2/future-block-land.step`. This is a source-boundary construction, not subtraction of neighboring parts. Remaining obsolete boss stock is harmless only if material/sealing checks pass; its old mounting role is retired. Stations10/20move to future block land,21/22/23to cover;20retainedstations keep exact interfaces.

Estimated dimensions/registration are inherited unchanged. No production-strength claim. Added material is limited to five original bore fills and futureland; removed material to the three named masks. DeckZ244..254, facetedfeet,20activepaninterfaces, pumpwet/mountinterfaces, main/cambearing support and cam-retention backing/socket guards must remain exactlyunchanged. Actual cover/pan/main-gasket/pan-gasket/sealant/crank-and-cam core/pump neighbors checked. Single valid topology, exact STEPreadback1e-5mm³, completewatertightdirectGLB and0.15mm bounds required. No threshold relaxation. Tighter quadrature may be used while preserving original1e-7 convergence criterion; failures remain failures. BrowserNOTRUN; candidate-only, rootonlycanonical.

Owned module/check/render/report/generated directory and this handoff. Restore inputs through CAD-ARTIFACTS.md and referenced handoffs. No personal input path. Record actual outcomes before review; no automatic promotion.

## Delivery checkpoint — 2026-10-01

During the work root merged PR100; active review branch is now `engine/timing-interface-integration`, HEAD70542fad9de467a5c03ad54a6f54def8550956eb. The exact combined STEP input is still the predeclared72773d2c… hash. No canonical file was changed. Readiness: **candidate, FAIL overall; frozen pending coordinated pan-interface work**.

API `timing_front_block_adapter_candidate.build()` returns `(block, witnesses)`. Module source, masks and originalfillparameters are repository files. Native block and direct GLB export are under `cad/engine/generated/timing-front-block-adapter-candidate/`; report `inventory/engine/timing-front-block-adapter-validation.json`. Actual shaded GLB was inspected in `block-glb-review.png`. New artifacts await root publication; no release URL yet. Restore required inputs using CAD-ARTIFACTS.md and the component handoffs.

```sh
XDG_CACHE_HOME=/tmp/truck-cache .venv-cad/bin/python scripts/check-timing-front-block-adapter-candidate.py > cad/engine/generated/timing-front-block-adapter-candidate/validation.log 2>&1
XDG_CACHE_HOME=/tmp/truck-cache .venv-cad/bin/python scripts/diagnose-timing-front-block-physical-guards.py
XDG_CACHE_HOME=/tmp/truck-cache .venv-cad/bin/python scripts/diagnose-timing-front-block-material-bounds.py
XDG_CACHE_HOME=/tmp/truck-cache .venv-cad/bin/python scripts/diagnose-timing-front-block-pan-contact.py
XDG_CACHE_HOME=/tmp/truck-cache .venv-cad/bin/python scripts/check-timing-front-block-dry-neck-pair.py
XDG_CACHE_HOME=/tmp/truck-cache .venv-cad/bin/python scripts/render-timing-front-block-adapter.py --extract
MPLCONFIGDIR=/tmp/truck-gear-mpl python3 scripts/render-timing-front-block-adapter.py
```

macOS/Python3.13/build123d0.10.0; system Python NumPy/Matplotlib render. Syntax checked. No dependency changes. Model/effort/usage unavailable.

| Gate | Result |
|---|---|
| Application/coverage | Estimated coordinated study only; factory contour/routing/strength NOT RUN. |
| Dimensions/coordinates | PASS declared source geometry and input hash;5retired versus20activepanstations explicit. |
| CAD/export | PASS: valid single solid and STEP, zero roundtrip difference; direct GLB watertight, bounds error0.006842475mm. |
| Material bounds | Original overlapping-compound-mask check FAIL145.301876mm³; independent sequential and fused SAME-source-operand subtraction both give exactlyzero outside material. Original failure preserved, supplemental geometric diagnosis supports bounded additions without expandedmask/tolerance. Removed-outside-source-regions zero. |
| Protected regions | Deck244..254, facetedfeet,20activepaninterfaces, main/cam/retention and physical pump/accessory interfaces unchanged. Three broad guard additions retained as FAIL; see supplemental diagnosis. |
| Actual interfaces | Cover, main gasket, pan gasket, terminalsealant, refinedcrankgear, cam core/bearings/retention, waterpump and shifted oilpump/bolts have zero overlap. Refinedcrankgear minimum gap5.259375mm. **PAN FAIL** for both frozen alternatives below. |
| Source/visual | Actual shaded exported GLB inspected; research CAD sections retained. Factory source comparison NOT RUN. |
| Motion/disassembly | NOT RUN beyond static neighbors. |
| Learning/diagnostics | N/A: isolated candidate; installed learning unchanged. |
| Browser | NOT RUN; prior root security block, no bypass. |
| Reproduction/review | Source/report/input/output hashes and diagnostic witnesses preserved; root review/publication pending. |

Native added material73910.194130mm³ and removed39864.416083mm³. Original compound allow-mask difference falsely leaves a valid145.301876mm³ fragment at oldbore20; sequential subtraction of land then the samefivefills and a separatelyfused union both remove it exactly. This is documented in `timing-front-block-material-bounds-diagnosis.json`, not hidden by adjusting tolerance.

Broad accessory guard changes0.031523535mm³; actual radius12boss and radius5.2socket are unchanged, and the added region lies0.474372mm from the boss. Broad radius85pump-frontguard adds1242.821018mm³. Radius61pump-wallguard adds0.269854671mm³ atX363..364/Y7.801..9.326/Z123.774..125.132,1.790414mm outside the radius59fluid opening. Actual pump gasket's2mm rear support, gasket/housing and fluid passages are unchanged. These physical findings do not erase broad failures or imply source/strength acceptance. See `timing-front-block-physical-guard-diagnosis.json`.

Frozen attachmentv2 pan still overlaps5.164992827mm³ atX338.75..340.294118/Y−127.439024..−126.25 (conservativeZbounds−32..0). Its witness/report are `pan-overlap-0.step` and `timing-front-block-pan-contact-diagnosis.json`. The separate dry-neck pan SHA`b519c1e37e6cacec5ed2326d92264c61ce7dd7f9f1a40eec7a57afeca1eb0caf` overlaps1252.768512940mm³ atX335..343.582821/Y100..126.591294 (conservativeZbounds−32..0). Witness `dry-neck-overlap-0.step` and report `timing-front-block-dry-neck-pair.json` preserve that failure. Neither was subtracted from the block.

## Coordination and next action

Root and pan worker are defining a common analytic transition-seat contract before either failed geometry is revised. The source right seat runs X335/Y111.5/width11/Z−32 toX359/Y179.1/width29.4/Z−24.5 toX365/Y196/width34/Z−24.5. A steep normal-offset wall can extend inboard beyond that supporting seat. Do not blanket-trim block material to clear an unsupported upper pan wall. Preserve both failed pan pairs and this candidate; a subsequent revision must establish contact/seat/oil-boundary continuity as well as zero overlap. Full sealing, attachment, motion, browser and installed acceptance remain open. No processes remain from this candidate build or diagnostics.

Final checkpoint SHA-256:

- `inventory/engine/timing-front-block-adapter-validation.json`: `1d7696731ee3b528e7d67f2772af0410f020e2b2e5bfe1719135e4bb1e1b3b29`
- `inventory/engine/timing-front-block-material-bounds-diagnosis.json`: `0924602148755b748d1def1f9e8add95168519b95d97c8fa57118e5ded43b4e4`
- `inventory/engine/timing-front-block-physical-guard-diagnosis.json`: `32e154e7390d966d7aeb9e8c95c250c7c195420cab2ab137d95c9c222f8eec00`
- `inventory/engine/timing-front-block-dry-neck-pair.json`: `85c5c314865cd3ac23b0e4148cc5855422cdd9c4e66c2d07a42c2c65a0abaa73`
- `cad/engine/generated/timing-front-block-adapter-candidate/block.step`: `661dcdfce65f64ff19aeaeb01c8b4ac46f67379eb37d4f29e80aa4dfad594502`
- `cad/engine/generated/timing-front-block-adapter-candidate/block.glb`: `5c5b04730e06092fade31faf47fc713fa43213656de93172ac1ec5c0be8e0ef4`
- `cad/engine/generated/timing-front-block-adapter-candidate/block-glb-review.png`: `a2544c5a2c5dbe660060f6d2d495f55cafdccae55400ad134a0f7539b6eacf3d`
