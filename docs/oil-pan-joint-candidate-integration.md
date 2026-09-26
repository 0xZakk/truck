# Oil-pan joint candidate — NOT released until QC and visual review pass

`cad/engine/oil_pan_fasteners.py`'s original 13/12-station layout is **rejected** by the newly acquired exact-part photograph. Reuse only its source-dimensioned screw and explicitly assumed washer shape functions. Do not integrate its `build`, `pan_api`, or `block_interface`.

The replacement candidate is `cad/engine/oil_pan_joint_candidate.py`: 10+10+3+2 hole topology, one continuous molded gasket, matched curved end lands, and 25 screw/washer pairs. The three-hole bridge is provisionally assigned to +X; this is not a verified photo orientation or OEM pattern.

## Proposed integration, after acceptance

- Apply `block_interface` to the block before export.
- Apply `pan_interface` to the oil-pan definition at **both** pan build sites, preserving its local `(0,-12,-96)` assembly translation.
- Suppress `pan-side-gasket-1` and `pan-side-gasket-2` definitions **and their occurrences** from both existing pan builder calls. They are replaced by the new continuous gasket, whose definition is already in the global CAD frame and is added at `(0,0,0)`.
- Call the new `build((define,add,group))` once after the initial pan group is created. It adds three definitions and 51 occurrences (the gasket plus 50 hardware pieces), replacing two old gasket definitions/occurrences.
- Register `felpro-os34601r-topology` to `reference/engine/felpro-os34601r-topology-reviewed.json`, its exact product-page URL, and file SHA. The review includes the image SHA and explicit application/geometry limitations.
- Merge `inventory/engine/oil-pan-joint-learning.json`. Retire the rejected study's unused learning file from any proposed integration.
- Run the candidate checker against the frozen pre-integration build, then independently compare installed STEP definitions to candidate geometry and run the complete static/navigation/source audit plus assembled/exploded visual inspection.

## Scope

Front/rear radii, flat pads, head/washer construction, station coordinates, end orientation, dry block extensions, gasket thickness and compression are provisional. The central rail offset seen in the photograph is not reconstructed. Physical production fits and the timing-cover/block/pan three-way joint remain unresolved. Hardware represents the observed overall layout but is not a recovered dimensioned Ford assembly.
