# Upper intake support: evidence and interface study

## Contract

- Component issue [#36](https://github.com/0xZakk/truck/issues/36), engine parent #1. Root owns integration, datum coordination and browser review.
- Baseline commit `fb2a1e756cf5e0d6ed925975312231406fce18ed`; current manifest and detailed exterior stage hashes are in `reference/engine/intake-support-review.json`.
- Scope: establish the real support identity, decomposition and both attachments, then build an isolated candidate if evidence supports it. Frozen intake/cap/exterior files and canonical assets are excluded.
- Owned: this handoff, `reference/engine/intake-support-review.json`; prospective `cad/engine/intake_support_candidate.py`, scoped checker and validation report. No geometry file exists yet.
- Intended detail: formed support, actual mounting holes/bends, separate identifiable fastening hardware, supported mating seats and removal path. Millimeters and existing CAD axes; local frame/parent not assigned until the anchors are identified.
- Available inputs: exact1994 offline intake removal/parts pages and tightening figure; earlier Ford installation and parts drawings; specimen upper manifold photograph; owner engine-bay photograph; immutable detailed-intake stage. Restricted source originals stay outside Git.
- Planned checks once datums exist: single-solid parts/STEP roundtrip/GLB bounds; exact seated contact, fastening stack and engagement; all nearby installed parts plus cap withdrawal and throttle motion; shifted-seat negative control. Existing numerical overlap convention0.1mm³ is not a production tolerance.

## Evidence and decomposition

The exact1994 intake removal procedure lists the support's manifold-end screw/washer separately from the seven upper studs and thermactor bracket. Its only diagram shows lower intake/exhaust head-bolt tightening sequence; it does not locate the upper support. The parts page identifies upperE7TZ9424A and lowerE7TZ9424D without listing this bracket separately.

The actual earlier Ford installation drawing labels support9J444 beside the direct front throttle flange. It shows7/16-14×1.50 and3/8-16×.88 screw/washer callouts in that inset. These are earlier-year comparison evidence; both callouts have not yet been safely assigned to exact1994 attachment endpoints. The parts drawing separately depicts a formed support. It does not justify a generic long diagonal brace.

Proposed physical decomposition is one formed support, the documented manifold-end screw/washer assembly, and opposite-anchor hardware once positively identified. Captive versus loose washer construction remains unknown. This support must not be conflated with the accelerator bracket, seven flange studs, thermactor bracket or engine lifting eye.

An E7TZ-9J444-A catalog lead appears alongside E8TZ-9J444-A and E5TZ-9J444-B variants. It is an identification lead, not verified truck applicability. Search-result captions are not geometry evidence. The owner bay and full specimen views obscure the anchors. A reinspection of the previously captured different-owner1994 twin-port interface close-up resolves the manifold end: a cast pad directly below the throttle flange, with a large visible washer and screw clamping a vertical flat strap. The strap continues down beyond the crop; the other anchor remains unidentified. Its original page is [1994 F1504.9L Rough Idle](https://www.ford-trucks.com/forums/1556834-1994-f150-4-9l-rough-idle.html). This is a useful actual specimen observation, not calibrated geometry.

## Proposed interface plan

1. Trace9J444 in an actual full-engine exploded figure and front/underside specimen view. Root independently checks owner-photo context.
2. Identify the non-manifold anchor and which screw fits each end; document source-visible seat orientation and unknown offsets before choosing millimeters.
3. Inspect the detailed intake's corresponding mounting pad. If a boss/seat is missing, propose an isolated coordinated casting patch; do not drill the nearest convenient solid.
4. Build the formed bracket and explicit hardware against those named seats, preserving cap removal, runner air volume and throttle motion. Dimensions inferred from photographs remain estimates.

## Delivery and validation

Readiness: **research**. No bracket geometry, exports, canonical edits or production fit claim. Ledger binds viewed captures and source observations; original manual pages/photos are not redistributed. Application evidence passes for bracket existence and separate manifold screw. Actual1994 comparison pixels establish the below-throttle manifold pad/strap topology. Exact variant, dimensions, opposite anchor and complete stack remain unresolved. CAD/export, source-versus-candidate render, installed interfaces, motion/removal, learning integration and browser gates are **NOT RUN** because no justified candidate has been built. Reproduction is limited to source identification/hashes at this stage.

Next evidence target: full-engine Ford exploded image at https://www.supermotors.net/getfile/905228/fullsize/1988-ford-f150-4.9l-exploded.jpg . Parent inspected this image: it is only383×565 and adds no anchor detail beyond the existing local overview. This is earlier-year comparison, not an exact1994 dimension drawing. No background build runs. Issue remains open; no background work continues after this checkpoint.

### Wider specimen observation

Root obtained and independently inspected the actual wider2017 forum photograph, now locally available at `cad/engine/generated/intake-support-reference/intake-front-support.jpg`. I inspected its pixels too. It confirms the below-flange cast pad and bolted flat strap, continuing downward beside the visible cover wall. Pipes and the image crop still obscure its lower anchor. The forum author names4.9L; vehicle identity is not independently authenticated. This photograph and any derived composites must be excluded from shared CAD archives. URL and hash are in the ledger.

This introduces an upstream interface question: current flangeX200,Y25 lies over the modeled valve-cover roof. A vertical strap at the pictured manifold pad would encounter that roof. The photo may require a different longitudinal or lateral intake-to-cover relation; perspective does not select a unique correction. Do not use a bent detour or a convenient roof mount to conceal that uncertainty. Root must coordinate the source-supported datum review before a complete bracket can become integration-ready.

### Coordinator checkpoint

Root deferred support geometry because the lower anchor is unsupported. Preserve the two unviewed higher-resolution1996 leads in the ledger for future direct pixel inspection. Next action is source/anchor and intake-to-cover datum resolution, not bracket generation. Work moved to a separate distributor-center-contact task.

Later review: Ford upper-engine exploded figure A10700-E (1996 comparison), callout11, confirms a formed support near the throttle. Its exploded projection still does not resolve the lower anchor. Image hash and nonredistribution policy are in the ledger; no CAD was added.
