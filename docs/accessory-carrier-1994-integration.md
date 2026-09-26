---
title: "Integrate the 1994 shared accessory carrier topology"
date: 2026-09-25
status: candidate-passed-local-qc-not-installed
---

Ford TSB 94-10-19 Figure 4 supplies the corrected architecture: one carrier supports power steering, A/C and the tensioner; a front-head bolt, side-head bolt and two block-side stud/nut stacks attach it to the engine. The older Figure 3 lower bolts #4 are absent from the 1994 drawing. Every candidate dimension and casting section remains provisional.

## Frozen candidate

`cad/engine/accessory_carrier_1994.py` SHA256: `663c2de33cd56994f1c0ad9a9cfdc7c7257cd6f656fd3094138a24f7a6666951`.

The independent neighbor report matches manifest `90807873b8c58234650e03b08557e524044f800d8fc3de97e212dd644e816cb9`. It passes 192 exact intersections with zero overlaps above 0.01 mm³ and 19 STEP round trips: 17 candidate pieces plus adapted block/head. The joint checker passes washer/carrier and washer/nut seating, three clear blind receivers and solid floor probes, adapter idempotence, and deliberate displacement controls. Report files are `inventory/engine/accessory-carrier-1994-validation.json` and `inventory/engine/accessory-carrier-1994-joint-validation.json`.

Visual inspection of `/private/tmp/truck-carrier94-preview-v5.png` confirms the common carrier, separate side fastening stacks, and tensioner wheel below its pivot. The retained P/S-to-A/C spacing produces a tall, open frame; it is not a reproduced Ford casting contour. The screenshot includes five installed accessory context pieces, hence 22 displayed items. Its exploded view is a preview, not a complete exploded-motion collision certification.

## Integration hooks

Use `cad/engine/accessory_carrier_1994_integration.py` as the adapter reference.

1. Replace definition `ps-ac-support-bracket` with `carrier()`. Keep the existing P/S and A/C component placements and accessory-to-bracket bolts.
2. Remove both occurrences AND now-unused definitions `ps-ac-engine-bracket-bolt-1` and `ps-ac-engine-bracket-bolt-2`.
3. Keep the eight existing tensioner identities. Set every one to position `[473.56,167,350]`, rotation `[0,90,0]`. Keep local wheel/arm geometries, except replace `tensioner-mounting-bolt` with the extended `mount_bolt_local()` geometry exposed by the helper. Do not install the earlier independent `tensioner-engine-bracket` candidate.
4. Apply composable `block_interface(shape)` and `head_interface(shape)` to the current geometry AFTER existing accepted changes. They do not replace the engine definitions with a frozen baseline. Retain the existing front-head seat at Y90/Z300. The prior original P/S front-block boss at Y90/Z220 is no longer an attachment; on a fresh builder pass, suppress that positive-Y boss in the old accessory adapter while retaining its alternator-side boss. Do not blindly subtract it from an already modified block, which could remove original material.
5. Invoke `build_hardware(api)` for eight new items: front-head bolt #1, side-head bolt #2, two block studs, two washers and two nuts. It places them in `carrier-1994-engine-attachments`. Net change is +6 occurrences, without duplicate carrier or tensioner bodies.
6. Register source `ford-tsb-94-10-19-accessory` from `reference/engine/ford-tsb-94-10-19-accessory-reviewed.json`, and use the candidate's source/limitation metadata for replaced carrier and relocated tensioner descriptions. The KB source page is `kb/sources/ford-tsb-94-10-19-identifies-the-1994-accessory-bracket-and-belt.md`.
7. Rerun candidate checks on the integrated variant, installed whole-engine QC, navigation, source hashes, and relevant exploded positions. In particular verify the head adapter composed with newer rear-manifold changes. Prior frozen-manifest reports are not installation certification.

## Explicit remaining limits

The shared-carrier/tensioner relationship is now source-supported, but coordinates are still assumed. The unchanged alternator remains at Z410 while the relocated tensioner wheel is Z350; this does not reproduce the overall schematic's ALT-to-tensioner height ordering. No belt is installed with this correction. Catalog length, pulley effective/pitch radii, working tensioner angle, load analysis and production threads remain unresolved.

The carrier fixes attachment topology and removes the independent tensioner load path. It must not be described as a completed factory FEAD layout or a faithful dimensional casting replica.
