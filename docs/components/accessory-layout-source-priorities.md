# Accessory layout: source priorities after family screening

Research supplement to `accessory-common-layout-discovery.md`, same #32/#34 baseline8c2d2d9a1400acf784e04581a61e6a6ede38d3ba. No geometry/pose changes; original family reports remain frozen. Root reviewed the existing belt solver's tangent, winding and actual CAD-wire checks. This supplement avoids rerunning those builds.

## Pulley identities and dimensions

| Wheel | Current outside envelope | Authority / unresolved detail |
|---|---:|---|
| Crank | 163.068mm OD | Dorman594-152 catalog6.42in overall diameter, 1987–96 Ford4.9 comparison (`inventory/engine/research-2026-09-23.json`, PDF241/printed239). Overall OD is not a measured effective groove diameter |
| PS | 131.318mm OD | Dorman300-0295.17in comparison; F1501990–96 manufacturer summary. Published5-groove metadata conflicts with Ford/Gates6-rib application. Installed pulley identity and effective diameter unresolved |
| AC | 145mm clutch OD | UACCO101220C1990–95F-series4.9 comparison,6grooves. Clutch OD is not necessarily a groove effective diameter; installed compressor unknown |
| Tensioner | 90mm OD | Gates38022 replacement, smooth/backside, width37.5/bore17. Gates1994catalog4.9 table lists38022/38131. Do not substitute the TSB's Econoline-only76mm recommendation |
| WP | 150mm OD | Explicit illustrative diameter. Ford supports separate pulley and backside belt contact; no dimensional evidence establishes150mm |
| ALT | 70mm OD | Explicit illustrative geometry. Installed75/95/130A and2G/3G branch unresolved; no identified pulley specification |
| AP | 140mm OD | Explicit illustrative geometry. Ford vane-pump topology/three-hole hub supported; installed19/22in³ branch and pulley dimension unknown |

No source here authorizes changing any of these to tune belt length. The first productive dimension research targets WP, ALT and AP identification/OD, followed by the PS groove-count contradiction; replacement OD comparisons still require effective-diameter treatment.

## Routing and radius interpretation

Direct review of the applicable Ford drawing agrees with the solver's order ALT→TENS→PS→AC→WP→CS→AP and its smooth-back WP/TENS contact. The signed normal branch yields tangent travel in that directed order. Current sampled wraps are ALT98.692°, TENS95.869°, PS178.506°, AC131.805°, WP207.698°, CS189.034°, AP65.530°; signed grooved-minus-back total is360°. This is a read-only formulation check, not a new acceptance test. Existing root-reviewed tangency/winding/CAD-wire validation remains the actual solver evidence.

The family screen explicitly compares a modeled **cord** route using outside envelopes with a2491mm **effective** catalog length. Existing generic PK comparison offsets are1.75mm for ribbed wheels and0.35mm for back wheels; neither converts an unknown outside diameter into a verified effective diameter. Small offsets cannot explain the entire385.888mm residual, but unknown WP/ALT/AP diameters and working tensioner angle prevent assigning all mismatch to centers. Do not optimize that residual as if it were a calibrated physical objective.

## Coherent candidate constraints and ownership

The source already corroborates current qualitative ordering. The weak numerical assumption is the combination of side spacing, accessory heights and unknown radii. The preferred B family retains the source's common PS-over-AC column and sharedPS/AC/tensioner carrier. Its carrier should be regenerated from fixed engine anchors to matched accessory ears, preserving the Ford load-path topology; existing stock must not be stretched or cut around neighboring solids without this contract.

The opposite ALT/AP side also has a common carrier, supported by `reference/engine/ford-alt-thermactor-shared-carrier-reviewed.json`; moving either is a coordinated two-accessory bracket revision, not a free belt node. The Brazilian seller's conflicting power-steering application label is not accepted as USF150 fitment. Source photographs establish carrier topology only.

A next bounded trial should freeze a small family of declared center/radius assumptions and compare source ordering, carrier load paths, actual engine clearance, seat contact, belt tangency/wrap and residuals separately. Keep crank, pump, timing contours/axes and engine bracket anchor frames fixed. Keep complete AC/PS/ALT/AP branches rigid internally; rebuild external connections by named endpoints. Preserve current manifold/PS fitting endpoints as before/after records and leave missing hoses explicit. Only after a family survives these gates should it become an exported candidate. The existing+25/+50/+75mm diagnostic grid is not such a selected candidate.

## Delivery and validation

Owned new files: this supplement and `inventory/engine/accessory-layout-source-priorities.json`. Research only; no build or new STEP/GLB/browser/learning content. Source/coordinate limits above are part of acceptance, not future optional work. Application coverage partial; dimensions remain mixed replacement/estimate/unknown; CAD/export N/A; actual installation FAIL remains; motion NOT RUN; source review complete within captured material; root review pending. Reports bind source modules/ledgers for reproduction. No running processes. Next step is a root-owned whole-accessory candidate contract with the unresolved radius identities explicitly carried, rather than moving one compressor to clear the timing rail.
