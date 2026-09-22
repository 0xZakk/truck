---
title: "The truck is assembled from individually modeled physical components"
date: 2026-09-22
---

## Owner's scope

The owner selected the engine first and explicitly requires every physical part
to be modeled and structured into the assembly. This applies recursively to the
whole truck: engine, transmission, ignition, starter, brakes and other systems.
System-level exterior models are context assets, not completion of a system.
The final site must support individual component inspection and explain how
components work together. A partial milestone does not reduce the final scope.

## Component identity

Maintain four connected representations:

1. **Part definitions:** reusable geometry and technical information for a part
   design, with revision, material, parameters, evidence and geometry status.
2. **Physical occurrences:** every installed instance has a stable ID, parent
   assembly and local transform. Six identical pistons share a definition but
   have six independently selectable and animated occurrences. Each ring, pin,
   bearing shell and fastener is separately represented when present.
3. **Mechanical relationships:** mating datums, joint axes, supported motion,
   gear relationships and dependencies. Housing geometry is distinct from its
   contents. A fused crankshaft casting is one part; a crankshaft with bolted-on
   gears, keys or other attachments is an assembly of distinct parts.
4. **Functional relationships:** force/torque, oil, coolant, air/fuel and electric
   paths. Systems are cross-cutting tags/graphs, not exclusive assembly parents;
   the same physical component can participate in several systems without being
   duplicated in the truck.

Clickable identity survives CAD → STEP → GLB → browser export through stable
occurrence IDs and an explicit manifest. Do not rely on mesh ordering or transient
CAD face numbers. Rendering may batch repeated hardware, but picking must map
each rendered instance back to its own occurrence.

## Engine decomposition

This is a research checklist, not a verified or complete engine BOM. Derive exact
variants, quantities and hardware from applicable diagrams and teardown sources.

- Block assembly: casting, individual main caps, bearing shells, applicable
  plugs, seals, dowels and fasteners; model bores and functional interfaces.
- Rotating assembly: crankshaft; each piston, its individual rings and pin;
  each connecting rod, cap, bearing shells and hardware; flywheel interfaces.
- Head and valve train: head casting, each intake/exhaust valve, spring,
  retainer, locks, seal, rocker and supporting hardware, pushrod and lifter.
  Represent seats/guides according to the actual construction; do not invent
  removable parts where the casting provides the feature.
- Timing: camshaft, crank/cam gears and their attachment/retention components,
  cover, gasket, seal and hardware.
- Lubrication: pump housing, internal pumping elements, relief components,
  pickup and screen, oil pan, drain plug and seals; source internal passages.
- Closures and attachments: valve cover, gaskets, manifolds, mounts, brackets,
  sensors and their hardware, connected to neighboring system assemblies.

Small components remain in scope. Unknowns stay visible in the completion
ledger; they cannot be replaced by a label claiming the assembly is complete.

## Geometry and motion workflow

Use the existing build123d/OpenCASCADE basis for parametric mechanical geometry.
Evaluate the maintained earthtojake/text-to-cad tooling as the export, inspection
and kinematics layer. Its current interface differs from the repository's old
cadpy/plugin integration; pin a tested version and verify a representative part
and assembly before migration. No new CAD runtime was installed in this review.

Create reusable factories for sourced hardware and part families. Define mating
dimensions centrally so journals, bearings, housings and bolts fit by construction.
Preserve editable CAD alongside tessellated GLB. Blender remains useful for
body surfaces, materials and visual review, with stable component identities.

Use deterministic kinematics for explanatory motion. A common crank-angle input
drives crank, rods, pistons and valve-train timing through geometric relationships.
Transmission motion will use verified gear ratios, clutch/selector state and
engaged paths. This does not require a general rigid-body physics simulation.
Keep combustion/flow visualization separate from claims of simulated pressure,
temperature or fluid dynamics.

Maintain three separate display operations: operating motion, explanatory
explosion, and service disassembly. An exploded diagram need not be a physically
valid removal sequence. A service sequence must respect obstruction, retention
and prerequisite removal; do not infer that validity from attractive movement.

## Evidence and validation

Source functional geometry first: dimensions, counts, bore centers, interfaces,
clearances, shaft spacing, rotation axes and timing. Refine casting contours from
drawings/photos or scans. Explicitly distinguish published, measured and inferred
parameters, with units and source locators. Store conflicting evidence without
silently repairing suspicious values.

For example, the restored manual's Engine Rebuilding Specifications page has an
apparently inconsistent piston-pin diameter range and two identically labeled
pin-bore entries. These require corroboration before becoming CAD parameters.

An assembly passes a milestone only when:

- Every item in that milestone's sourced BOM has a corresponding occurrence,
  or an explicit unresolved entry. Report quantities and unique designs separately.
- Export/import preserves hierarchy, instance count, labels, scale and axes.
- Each physical part is selectable, isolatable, explainable and locatable within
  the enclosing assembly; hiding a housing reveals its actual modeled contents.
- Dimensional checks cover sourced interfaces. Overlap checks distinguish valid
  fits, threads and seal contacts from impossible penetrations; broad same-assembly
  collision exemptions cannot certify internal geometry.
- Motion satisfies joint relationships throughout the cycle, not just at a
  static pose; explosion reassembles exactly to the authoritative transforms.
- Multi-angle renders and cutaways are compared with references. Missing detail
  and unverified geometry are reported, not counted as accurate by appearance.

The first implementation slice is a single independently modeled piston/rod
assembly with its rings, pin, cap, bearing shells and hardware, connected to a
crank mechanism. This validates the full pipeline and component interaction.
Then instantiate all cylinders and expand to the complete long block, timing,
valve train and attached systems. It is a pipeline proof, not the final engine.

## Reference review

- [Jake Fitzgerald's car assembly](https://x.com/earthtojake/status/2084834223123202321):
  post describes 1,500+ generated parts and points to text-to-cad v0.4 beta.
- [Manufacturing/work-instruction example](https://x.com/augmentedcamel/status/2084297691392098764)
  quotes the assembly-sequence example below.
- [Sam Kelleran's fan assembly](https://x.com/skkelleran/status/2084093614716813585):
  inspected the image showing a component tree and assembled fan; the author
  describes it as designed for sourcing/manufacture, not independently certified here.
- [Assembly-sequence example](https://x.com/augmentedcamel/status/2082835320362394033):
  post describes geometric reasoning for assembly sequences.
- [Maintained text-to-cad repository](https://github.com/earthtojake/text-to-cad)
  and [CAD workflow documentation](https://github.com/earthtojake/text-to-cad/blob/main/skills/cad/SKILL.md).

All four posts were readable in the browser. Embedded videos reported unable to
play; no claim is made to have inspected their motion or verified their geometry.
