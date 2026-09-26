# Illustrative mechanical face-seal candidate

This is a generic construction study, not an identified Gates44009 internal bill of materials. Manufacturer descriptions justify a rotating face, a spring-loaded stationary face, and secondary supports. Neither the actual six-piece count nor any dimension/material is established for this truck. Keep these limits visible in the component names and learning text.

## Integration

- Add source ID `water-pump-internal-construction` pointing to `reference/engine/water-pump-internal-construction-reviewed.json`. It records Gates applicability separately from generic GMB and Schaeffler construction.
- Remove the old `water-pump-seal` envelope definition/occurrence from the pump builder's collected output. Invoke `water_pump_mechanical_seal_candidate.build((define, add, group))` after the pump parent group exists. Six definitions and six occurrences replace one: net+5 each.
- New group: `water-pump-mechanical-seal-assembly`, child of existing `water-pump-assembly`. All shapes retain original pump-local coordinates, with group pose unchanged at(440,−32,170). Housing, shaft, impeller, mounting and drive components are untouched.
- Merge `inventory/engine/water-pump-mechanical-seal-learning.json`. Keep the unverified bearing cartridge and its unresolved internal arrangement. Do not label these parts exact or use them as a service/rebuild list.
- Remove stale text saying no seal internals are represented, while retaining the caveat that exact production construction remains unknown.
- Run `scripts/check-water-pump-mechanical-seal-installed.py --candidate-report PATH_TO_ACCEPTED_REPORT` after export. It is syntax checked but not run against a published build. Run full-engine and browser checks on the integrated version.

## Geometry and acceptance

The carrier meets the existing housing throat at radius24mm over localX18..21, correcting the earlier0.2mm radial float without changing the housing. The rotating collar meets the shaft at radius8mm. All other dimensions are assumptions inside the inherited10mm axial seal space.

The checker uses the frozen accepted pump snapshot at `cad/engine/candidates/pump-joint-desktop/accepted`, with unchanged-neighbor STEP files from frozen6b11c0f8. It tests six single solids, pairwise/engine neighbors, all intended contacts, the common annular face area, and separate connected wet/dry voids. The void test uses ideal closed face contact; it is not a simulated coolant film or pressure seal. STEP roundtrips use adaptive volume comparison. Sampled pump-study explosions check internal display separation, not full-engine disassembly or a removal procedure.

## Bearing research decision

Schaeffler TPI131 shows integral shaft raceways, common outer ring, rolling-element rows, cages and end seals. It includes several row arrangements and standard sizes. Gates'2011 catalog identifies a unitized bearing/shaft but does not select those internals for44009. No exact bearing part number, row arrangement, or ball/roller count is inferred. The existing cartridge remains unresolved. Future manufacturer data or a measured teardown can replace that uncertainty; a generic illustration must stay separate from verified truck configuration.
