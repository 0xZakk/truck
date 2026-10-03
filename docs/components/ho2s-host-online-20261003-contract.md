# HO2S front-pipe host — conditional source contract

## Contract and ownership

Issue #82 under engine #1; exhaust parent #9 is an interface dependency. Worker `airbox_screw_finish`; root owns integration and shared files. Research checkpoint baseline `0e9d513794e7bab3dfcab45c7da06a669bb44878`. No assembly manifest is a geometry input and no installed transform is accepted. Own only `ho2s-host-online-20261003*` docs/reference/KB files. No CAD, shared builder, inventory, viewer, Git or issue changes. Preserve the preceding 107-member sensor specimen archive unchanged.

Task: identify a source-supported candidate front/Y-pipe host and freeze its application, two manifold joints and HO2S topology before any model. Read the relevant sensor coverage, installed rear collector/neck contract and applicable Ford service pages. Missing emissions/3D interface evidence remains a gap; no owner request is required to preserve this conditional research.

## Outcome and application bridge

**Walker 45166 is an identified conditional replacement comparison, not yet an accepted host for this truck.** Walker's exact 1994 F-150 4.9 catalog row requires non-California emissions. It does not display transmission, drivetrain or wheelbase restrictions; its `vcdb_attributes` object is empty. That is the scope of the reviewed record, not proof that all 4.9 transmission/body combinations share one front pipe. The owner's M5OD-R2 and 2WD configuration are known project context, but a transmission-specific Ford drawing and emissions identity are not closed here.

The manufacturer's public interchange endpoint returns a Ford-brand E8TZ5F250C Y-pipe → 45166 mapping. It also returns a separately typed generic-OEM converter → 15142 mapping for that number. Preserve both types rather than turning this into a unique production identity claim. The explicit specific-fit field, `universal_part=0` and year/model application conflict with generic marketing text calling the product universal; use the structured application provisionally and retain the conflict.

Historical Walker diagram 13143 (PDF 937 / printed 935) shows the 1987–1995 F-150 4.9 system under a 2 and 4WD heading and lists 116/133/138/155-inch wheelbase variants. Its front-pipe/converter drawing is grouped as assembly 15739; the following intermediate pipes vary by wheelbase. This distinguishes a front assembly from downstream length adjustment. It does **not** transfer 15739's all-emissions footnote to current 45166's non-California restriction. Historical 138-inch versus current 139-inch intermediate-pipe labels remain a catalog difference, not an owner's wheelbase measurement.

## Evidence ledger and dimensions

Primary endpoints are publicly linked through [Walker Find My Part](https://www.walkerexhaust.com/find-my-part.html). Exact product, application, interchange and photograph URLs/hashes are in `reference/engine/ho2s-host-online-20261003-evidence.json`; no original photo, catalog PDF or raw source response is redistributed. The Ford service page/image is a separate local access dependency, bound by hash.

| Property | Supported value | Classification / limit |
|---|---|---|
| Replacement identity | Walker 45166; qualified 1994 F-150 4.9 | Primary manufacturer application, conditional emissions |
| Pipe material/finish | Aluminized steel; compression bends | Manufacturer product attribute, not Ford production material proof |
| Inlets / outlet | Two / one | Manufacturer product attributes and actual photograph |
| Inlet connection | Loose two-bolt flange retaining spherical flare | Primary joint topology; no sphere/bolt dimensions |
| Outlet connection | Plain pipe connection | Primary topology; insertion/clamp length unknown |
| Outlet outside diameter | 2.500 in = 63.5 mm | Primary replacement dimension; no tolerance |
| Pipe wall | 0.060 in = 1.524 mm | Primary replacement attribute; forming thinning not specified |
| Catalog Length | 46.875 in = 1190.625 mm | Primary value, **endpoints undefined**; not accepted centerline length or bounding-box span |
| Nominal constant-wall outlet ID | 60.452 mm | Arithmetic OD−2×wall only; not measured formed bore |
| Two inlet diameters / sphere radii | Unknown | Retail 2-inch inlet lead not promoted to primary evidence |
| Flange holes / thickness / clocking | Unknown | Actual two-hole outline visible; no calibrated dimensions |
| Bend centerline and spatial inlet relationship | Unknown | One oblique product photograph; no accepted reconstruction scale/depth |
| HO2S boss position | Common trunk, near bend downstream of convergence | Visual topology plus exact-year Ford pipe-host evidence; no metric axis |
| Bung thread / seat / projection | Unknown | Sensor's prior M18×1.5 visual estimate is not receiving-thread evidence |
| Vehicle pipe/harness/support pose | Unknown | No installation, heat clearance or route accepted |

## Concrete host topology and model boundary

The source supports this separate-region graph for a future **conditional** host candidate:

1. Two hollow inlet necks with formed spherical flare surfaces, one to each exhaust manifold.
2. Two separate loose retaining flanges, each with two holes. Pipe seats and retaining plates must not be collapsed into one flat sealing surface.
3. Short and long inlet paths converging into a common hollow trunk; formed bends continue to the single plain outlet.
4. A distinct boss/seat opening on the common trunk near the bend, upstream of the long outlet run. The photo shows a protruding threaded-looking plug/boss; the Ford service illustration establishes the applicable sensor-in-pipe function. Exact plug versus bare-bung surface and hidden rear face are unresolved.
5. Separate future retention/sealing hardware and any heat shields/supports, only when identified. The manufacturer says mounting hardware is not included; do not invent a verified fastener set from that statement.

`ho2s-host-online-20261003-landmarks.json` records approximate feature regions in the actual 2000×2000 photo. These are **uncalibrated 2D view references** with a declared ±20-pixel manual-pick allowance, not millimeter centers or statistical confidence limits. The two photographed inlet mouths are A/B until their front/rear manifold mapping is independently established. A single oblique view cannot uniquely determine their relative axes/depth or the bung normal.

A usable parameter schema is therefore explicit: outlet OD=63.5, wall=1.524, inlet_count=2, outlet_count=1, joint_type=spherical_flare/loose_two_bolt_flange; catalog_length=1190.625 with datum=null. Inlet diameters, flange metric geometry, curve control points/bend radii, branch axes, bung frame/thread and local-to-engine transform remain null. Numeric hidden-depth estimates must be named in a **new pre-CAD revision approved by root**; silently converting the current photograph or catalog Length into a complete 3D pipe is not authorized by this source contract.

The bounded next model can be a separately framed replacement study with explicitly estimated bend/depth variables. It cannot be an installed host until both modeled manifold receiver joints are reconciled. Source facts already define the functional region breakdown, transverse stock and required passage checks; the specific remaining evidence lead is a second identified 45166 view or manufacturer dimensioned inlet/centerline/bung drawing. No further broad catalog search is needed before root reviews this boundary.

## Existing engine interfaces and acceptance tests

Named future neighbors: `exhaust-front`, `exhaust-rear`, the future front pipe, HO2S exterior specimen, future converter/inlet connection, heat shields/supports and harness mate. Applicable Ford service text disconnects one inlet-pipe assembly from both manifolds; its HO2S procedure and actual image 150757959 locate the sensor in the exhaust pipe. A generic sentence elsewhere saying manifold does not authorize drilling either modeled manifold.

The existing rear-neck contract preserves its outlet/flange/seat frame and estimated axis (X−145.688,Y−180 in its CAD frame). This is protected **model state**, not a Ford pipe measurement. Front and rear receiver seat geometry must both be inspected before adopting the spherical-flare joint; no flange movement or pipe bending by eye to hide mismatch. No sensor pose, installed lead route, tube contact or world coordinate is selected here.

Before accepting future CAD: declare every estimated parameter; preserve separate flare/flange interfaces; valid intended solids and STEP roundtrips; watertight GLBs with existing unit/axis/bounds gates; prove both inlet passages join the common outlet and open bung without blocked-core controls passing; verify spherical seat contact and fastener clearance against both actual host models; reject shifted-axis/blocked-passage controls. Check probe intrusion and gas access, hot-neighbor/tool envelopes and lead slack only after host/harness frames exist. Collision success alone cannot supply the missing application or spherical-seat dimensions.

## Delivery, reproduction and quality gates

Readiness: **research / conditional host contract**. No CAD API, STEP/GLB, installed browser view, model/render comparison or release archive is applicable to this research-only delivery. The prior sensor specimen remains separate and frozen. Source→atomic-note pipeline used the committed authored observations; three source pages and three notes are linked. Root owns semantic index updates.

| Gate | Result | Evidence and limit |
|---|---|---|
| Application/coverage | PASS conditional research | Primary exact-year 4.9 row, emissions qualification, typed Ford interchange; not accepted installed identity |
| Dimensions/coordinates | PASS recorded facts; metric placement NOT RUN | Three manufacturer dimensions/conversions; datum ambiguity and unknown frames explicit |
| CAD/export | N/A | No geometry authored |
| Source/visual | PASS source observation | Actual Walker photo, historical PDF page and Ford service image inspected; no model comparison |
| Installed interfaces | NOT RUN | Both receiver joints, bung gauge, host/route and emissions remain open |
| Motion/disassembly | NOT RUN | No tool/latch/pipe movement model |
| Learning/diagnostics | PASS scoped topology | Two manifold flows converge before sensor region; spherical seat versus retainer distinction |
| Browser | NOT RUN | No assets installed |
| Reproduction/review | PASS worker authored hashes; root review pending | Frozen delivery ledger, exact source URLs/hashes, no original redistribution |

Metric conversion and shape reasoning are reproducible from the committed evidence/landmark records without temporary files. Pixel re-review requires fetching the hash-identified public photo/PDF or obtaining the authorized local manual page. Public catalog response schemas/endpoints can change; recorded hashes distinguish later versions. No credentials, site scripts or temporary source files are build dependencies.

## Tracking and preserved review feedback

Root is reviewing the preceding 27-region sensor candidate. Its 107-member archive SHA256 remains `9a4a62c92886a32351da0fcaec3a7e72e94b9722c9ff8aaf1b8e47f785361257`. Root requested two caption fixes for the **next** render revision: sensor “Front oblique / protective cap”; connector “Axial connector mouth”. They are recorded here without altering frozen renders or hashes.

No running process at handoff. Model/effort/usage measurements unavailable. #82 and exhaust host integration stay open. Next action: root reviews this conditional host scope and chooses either an explicitly estimated isolated layout revision or the bounded second-view/dimensioned-drawing lead. No owner confirmation, broad CAD restart or shared integration write is required for preservation.
