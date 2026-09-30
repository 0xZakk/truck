# Component contract and handoff: coupled timing core

## Contract

- Issue #32 under #1, continued isolated study. Root owns integration; worker owns only NEW `cad/engine/timing_coupled_core_candidate.py`, `scripts/check-timing-coupled-core-candidate.py`, `scripts/render-timing-coupled-core-candidate.py`, this handoff, `inventory/engine/timing-coupled-core-candidate-validation.json` and ignored `cad/engine/generated/timing-coupled-core-candidate/`.
- Integration base: `eb502ce755d12fe896b3ea915f3ada4361e52a9c`, branch `engine/timing-interface-reconciliation` after PR #96. Geometry baseline: accepted isolated thrust-land/core set plus revised backlash gear exports. Earlier modules/reports and canonical/shared files remain frozen. Input hashes and current relevant manifest rows are recorded before checks.
- Actual rotating/translating cam group: `camshaft`, `cam-timing-gear`, `cam-timing-key`, `cam-gear-spacer`. Current manifest parents and retention source confirm these four. No separate gear-retaining bolt is established. Root's earlier bolt wording was not source evidence. Exact-year procedure specifies puller removal and installation with key/spacer; press-fit retention is a possible interpretation, but interference fit is unknown and not modeled.
- Stationary group: four `cam-bearing-*`, `rear-cam-plug`, `cam-thrust-plate`, two `cam-thrust-bolt-*` and two `cam-thrust-washer-*`. Plate fasteners never rotate. Crank gear rotates separately as the tooth-pair partner.
- Motion: axial delta in [-0.1,0] mm; complete keyed cam group angle = -crank_angle/2 + k*delta, k=-tan(25°)/81.2 rad/mm. Rigid rotation about the migrated cam axis YZ=(95.1098209901611,76.08785679212888), not world origin. Gear axial station remains X=385.259375.
- Acceptance: rigid group relative interfaces preserved, exact thrust contacts/endplay and overtravel controls retained. Check moving group against stationary core using rotation-invariant radial/axial support certificates and bounded source slabs; finite endpoint checks supplement them. Inherit only hash-bound proofs whose geometry/relative pose are invariant. Coupled tooth proof remains finite 25-angle/2-endpoint scope; do not extend it to continuous rotation.
- Geometry thresholds: exact core/containment/interference volume 1e-5 mm³; contact area >1 mm²; overtravel overlap >0.1 mm³. Preserve prior export tolerances for any re-exported pair. No threshold relaxation.
- Exclusions: block/cover installation, full cam/crank lobe clearance, valve linkage and distributor/pump phase dependencies. These remain integration requirements; no full-engine dynamic or production-fit claim.

## Evidence and reproduction plan

Read `timing-gear-backlash-candidate.md`, `timing-core-migration-candidate.md`, frozen thrust-land report/checker and `cam_retention.py`. The Ford timing service source is identified and hashed by `reference/engine/timing-gear-backlash-review.json`. Use only the actual four-part modeled cam group; do not invent or relabel a stationary fastener.

Contract was recorded before construction. Final scoped checks now PASS as detailed below. No canonical change or installation proposed. Usage/effort/billing unavailable. Source originals remain ignored. Exact command and completed proof scope will follow.


## Delivery and reproduction

```sh
XDG_CACHE_HOME=/tmp/truck-cache .venv-cad/bin/python scripts/check-timing-coupled-core-candidate.py
PYTHONPATH=.venv-cad/lib/python3.13/site-packages MPLCONFIGDIR=cad/engine/generated/timing-coupled-core-candidate/mpl python3 scripts/render-timing-coupled-core-candidate.py
```

Parametric APIs: `timing_coupled_core_candidate.parts()` imports the frozen set and substitutes the revised pair; `posed(parts, crank_degrees=0, axial_mm=0)` applies one common cam transform to all four moving members and separate crank rotation. It does not edit source objects or canonical data.

All 15 exports use **world CAD coordinates per occurrence**, not drop-in definition-local coordinates. Thirteen unchanged exports are byte-identical copies of the frozen thrust-land/core set. Only the two revised gears are transformed from their frozen local exports to the preserved world axes, exported and checked again. Restore those frozen inputs through the repository CAD artifact policy; no personal files or credentials are needed by the commands.

Environment remains locked Python 3.13/build123d 0.10.0/trimesh 4.7.4; rendering uses local matplotlib. No dependency updates. Actual exported neutral/coupled front and retention-detail views were rendered and directly inspected in `cad/engine/generated/timing-coupled-core-candidate/coupled-core-render.png`. Teal denotes the whole moving cam group; gray plate fasteners remain stationary. The view is a mechanism study, not factory-geometry acceptance.

## Exact proof scope

- **Six internal pairs:** all members receive the same rigid transform, so their relative geometry and local contacts/clearances are invariant. Existing static pair proof is reused only with its report/asset hashes. Revised gear material changes are outside R77.2, while the other three cam members are contained inside that radius; the preserved gear interior is exact.
- **Forty moving/stationary pairs:** every cam angle and every axial delta in [-0.1,0] is covered using complete source intervals and rotation-invariant supports. No finite-angle sampling is presented as a full-rotation proof.
- The four bearing interfaces use a verified R25.62225 cylinder containing every shaft source point capable of entering each bearing slab. The plate interface uses the R15.875 nose and the shoulder's axial stop plane. Pure axial separation handles distant parts.
- The gear/fastener certificates use an axisymmetric superset: inner material through R26, outer material beyond R47, and the forward web. Its axial extent is expanded for the full travel. Exact subtraction proves the actual gear is contained; exact intersections show the superset clears the stationary bolts and washers for every rotation.
- The spacer uses its R19.05 support with independent exact containment. A first trial used the square bounding box's R26.94077 circumradius, which was too loose to certify the plate bore. That failed **bound**, not an actual collision, is retained in `rejected-box-radius-bound.log` and its checker. No shape or threshold was altered.
- The other three cam members also have conservative radial separation from the rotating crank gear, with minimum lower bound 42.38467 mm. This does not cover the crankshaft itself or cam-lobe/crankshaft clearance.
- The tooth pair inherits only the exact new gear study: 25 phases across a tooth period, both axial endpoints, and the documented construction-level axial interpolation argument. The fixed-phase axial failure remains recorded there. No continuous tooth-rotation/load proof is inferred.

## Stops, controls and exports

At crank phases 0° and 180°, the gear land contacts the stationary plate at delta=-0.1 mm over **784.0708405 mm²**; the shaft shoulder contacts it at delta=0 over **724.4301821 mm²**. Exact endpoint overlap is zero. Independent full-annulus containment checks show complete material on both opposing faces, making those stop areas invariant under all cam rotations: gear annulus R20.65–26; shoulder contact annulus R20.6375–25.62225.

Overtravel remains sensitive at both phases: delta=-0.11 gives **7.8407084 mm³** gear/plate overlap; delta=+0.11 gives **79.6873200 mm³** shaft/plate overlap. Moving the plate +0.05 mm produces **39.2035420 mm³** overlap at the nominal rear stop. Actual posed centers match the common rigid transform within 1e-7 mm; deliberately leaving the key stationary is detected, including a 0.10036 mm mismatch at the small compensated endpoint. Plate/bolt/washer objects remain unchanged in pose construction.

Both new world-frame gear exports are valid single solids and watertight, with zero duplicate/degenerate mesh faces. Maximum gear bounds error is **0.0128991 mm**, maximum STEP roundtrip volume error below **0.000001 mm³**. Unchanged asset byte identity preserves only the old scoped export proof; it does not certify new installed interfaces.

| Gate | State / scope |
|---|---|
| Application/BOM | PARTIAL; actual modeled membership verified; separate retaining bolt and fit remain unestablished |
| Frames and rigid interfaces | PASS four members together, six invariant internal pairs; no gear slip on key |
| CAD/export | PASS 15 world-frame occurrence exports, 13 byte-identical inherited assets |
| Stationary core motion | PASS all-angle/full-axial supports for 40 pairs |
| Thrust stops | PASS exact endpoint contact plus all-angle annular support; plate and overtravel controls detect faults |
| Gear engagement | Inherited bounded PASS from exact revised pair; continuous rotation/load remains unproven |
| Visual | PASS actual posed meshes inspected; no new source/factory identity claim |
| Block/cover/crankshaft/lobe fit | NOT RUN / excluded; block worker owns outstanding fit |
| Valve/distributor/pump coupling | NOT RUN; required before integrated coupled motion |
| Browser/learning | NOT RUN / N/A uninstalled developer study |

No process remains running. #32 remains open. Root integration review is next; no installation or Done claim. Do not attach only the cam gear to the coupled motion while leaving the keyed shaft/key/spacer behind. Do not rotate the thrust-plate fasteners. Fit/preload, lobe-to-linkage timing, distributor/pump drive phase and full engine clearance remain separate integration dependencies.

## Evidence hashes

Final report `inventory/engine/timing-coupled-core-candidate-validation.json`: `f1b575540747e7475d7a71da84a39f1c58bdd7b35b01b870266eca82434763d4`. All bound inputs and relevant manifest rows were stable through completion.

| New world-frame artifact | SHA-256 |
|---|---|
| `cam-timing-gear.step` | `b64832c685697b36b008951820a39d5f7d4a3590396b18565539b7845dcc0bf6` |
| `cam-timing-gear.glb` | `a01da6b7144043186f2aa55173cf09277aaed7805fb017bef2b98efbbafce61d` |
| `crank-timing-gear.step` | `2f1cab37c7e4867ad8ab055c933bd71e979d75a2135a329c7f7510c821a49866` |
| `crank-timing-gear.glb` | `e03a2b62f917461c0254def74a5698f1485a65384c9f6cccbb214168fc2e627a` |

Actual render SHA-256: `06c8e545b384d6127893ea405c21436cc057fbf3710ad8e04e644614595ce2bd`. Historical initial-pass and rejected-bound evidence remain isolated; no old/shared/canonical source or report was modified.
