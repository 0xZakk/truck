# Water-pump mounting reconstruction: source packet and isolated gasket study

This is **not an installed pump joint**. Do not mark the engine coolant mounting interface complete from this study.

## Acquired evidence

`reference/engine/water-pump-mounting-topology-reviewed.json` records identities, URLs, photo observations, limits, and image hashes. It links the existing manufacturer catalog application evidence for Gates44009 and Fel-Pro13816. Four exact product photos are saved alongside it. The local Ford1994 water-pump parts page identifies F6TZ8501KB; its service instructions describe pump attachment but do not dimension the flange.

The Fel-Pro13816 gasket has four small peripheral holes and a larger fifth opening, plus its central opening. Gates44009 front/back/side views corroborate that topology, show an impeller protruding behind the casting flange, a large lateral radiator neck, and a smaller formed heater-return tube.

The newly saved ATK DFF8 automotive1987–96 block-front photo (`atk-dff8-block-front.jpg`, Titan Engines product listing) shows the pump flange machined directly into the block front, beside the cam gear and above the crank. The front cylinder outer wall is visible through the pump opening. The larger fifth opening is near the upper mounting hole. The product gasket photo needs approximately180° in-plane rotation to match that front view; exact orientation/coordinates are not measured.

## Existing mismatch and reconstruction constraints

The present pump is centered at `(440,0,170)`, with its gasket rear surface atX420 and block front atX373. The47mm airgap is an inherited datum error; it should not be disguised with an invented block extension or coolant tunnel. A plausible reconstruction must put the rear flange on the block face, expose a real impeller opening bounded by the cylinder wall, and account for the larger fifth opening without declaring its function prematurely.

The pump axis may also be offset laterally from the crank, opposite the cam, as seen in the perspective block photo. Exact offset needs better dimensional evidence. The existing Y0 is unverified.

Changing pump position alone would shift the drive hub, pulley, fan clutch, and heater return. The belt work currently keeps belt planeX473.56 as an assumption. A coherent reconstruction could revise pump casting/shaft axial proportions while preserving that plane, but should not tune arbitrary dimensions merely to clear the belt. The block-side water jacket and fastener socket depths must remain explicitly unresolved until reconstructed from stronger evidence. IndustrialCSG649 pump dimensions are excluded because the industrial pump/flange is not interchangeable.

Preserve inventory identities for the existing eight pump components and seven heater/ECT components; replacing the present annular gasket does **not** add another gasket occurrence. Existing bearing/seal internals and vane profiles remain simplified even after flange work.

## Isolated deliverable

`cad/engine/water_pump_gasket_topology_candidate.py` is an uninstalled photo-frame approximation using the inherited59mm inner radius as a provisional scale. It has four small mounting apertures and the separate larger opening. All dimensions, local silhouette arcs and installed orientation remain provisional. It intentionally has no builder hook or extra fasteners.

Run `.venv-cad/bin/python scripts/check-water-pump-gasket-topology-candidate.py`. It verifies one valid solid, a valid STEP roundtrip, five open peripheral probes, and two planar faces each with seven wires (one outer boundary, center opening and five peripheral openings). The actual mesh was rendered and visually inspected; it reproduces aperture topology but is a more circular and less smoothly blended silhouette than the product photo.

This is useful geometry for the eventual joint reconstruction, not accepted production geometry or proof of engine fit.
