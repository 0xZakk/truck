# V9 accepted candidate: accessible pan joint and staged display separation

Use `cad/engine/oil_pan_joint_v9_candidate.py` in place of theV8candidate import. Existing block/gasket/hardware interfaces are unchanged. The panadapter now reconstructs the source `oil_pan.py` shallow shell at726mm outside/720mm inside length and then applies the joint flanges/neck. It intentionally rebuilds that provisional shell instead of preserving the old trapped end-wall geometry. Rear sump profile, drain frame/boss/seat and depth are retained.

V9 exact static check:684neighbor intersections, five valid single-solid STEP exports/imports,25flange/seat/socket/floor controls, no collisions. The new shallow end-wall dimensions remain assumptions; the exact gasket photo establishes10+10+3+2topology, not stations or which end faces forward. Three-hole-front assignment is still unverified.

Add occurrence `explode_stages=pan_hardware_stages(explode_cad_mm)` to all25screws and25washers, from `cad/engine/explode_stages_candidate.py`. Stages are0→zero,.35→[0,0,-137],.6→[finalX,finalY,-217],1→existingfinaloffset. The first segment extracts axially; the second moves outward in the corridor above the deeper pan walls. These are educational display coordinates, not a disassembly procedure.

The JS helper `viewer/engine-explode-stages-candidate.js` exports `explodeOffset(occurrence, amount)` and mirrors Python `explode_offset`. Call it where the viewer currently multiplies the final CAD explode vector by amount; retain the existing CAD-to-viewer conversion afterward. Occurrences without stages keep legacy linear offsets. Both implementations passed boundary/interpolation and legacy checks.

`check-oil-pan-joint-v9-staged-motion.py` passed706rotating-neighbor checks at25crank phases and773joint pair checks at12explode fractions including both sides of stage breakpoints. It uses uncut screw stock as a conservative superset when that proves zero collision; OCCT otherwise returns spurious overlaps/null results on some translated threaded-screw/washer pairs. This is a mathematical containment proof, not a collision exception. Where stock overlaps, actualpart intersection is still checked. No continuous swept-volume or production-fit claim.

`check-oil-pan-v9-preserved-interfaces.py` verifies unchanged deeper rear sump below the shallow floor, unchanged drain vicinity, three retained shallow-floor material probes, and an open drain. The shallow-floor/end-wall footprint intentionally changes; its old corner volume is not claimed preserved.

Actual assembled/60%staged CAD mesh inspected at `reference/engine/qc/oil-pan-v9-staged.png`. The offline exporter represents the staged60%pose explicitly; it is not a viewer integration test.

After isolated integration use `check-oil-pan-joint-v9-installed.py --baseline-root <unchanged-prepan-baseline-with-V9-accepted-report>`. It checks five definition geometries, all50rigidposes and stage contracts. Root still needs fullengine/belt/viewer verification after combining other candidates.
