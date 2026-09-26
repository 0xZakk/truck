# Geometry evidence required to finish the engine

The existing model is a component-level educational reconstruction. It is not yet
an accurate digital replica of the installed engine. More component occurrences
do not resolve a missing datum or establish a complete bill of materials.

## What the current evidence establishes

The restored 1994 manual provides component identities, operation descriptions,
exploded/section illustrations, service limits and some replacement specifications.
The engine index and the separate engine-mounted-system index retain source paths,
URLs, content hashes and image references. Replacement-piston catalogs establish
specific replacement dimensions, not the complete original engine shape.

The fuel injector and IAC section illustrations support internal decomposition.
The TPS description supports a moving wiper and curved resistor. These do not
supply manufacturing profiles, connector details, spring rates or mounting datums.
The manual shows two IAC variants; their serviceability differs.

## Specific unresolved foundations

- Bore pitch is currently 113.792 mm and deck height 254 mm by assumption.
- The block/head surfaces and port stations are provisional; a collision-free
  interface with another provisional part does not verify either one.
- Distributor, oil-pump and cam-drive datums must agree before their connecting
  shaft and gears can be represented as an accurate assembled drive.
- Water-pump, damper, brackets and pulley datums must agree before the belt drive
  can be represented as an accurate assembled system.
- An exploded service diagram often groups welded, molded or nonserviceable
  internals. It does not establish the requested every-physical-part inventory.

## Reference search findings, 2026-09-22

Searches for Ford 300/4.9 CAD, STEP and dimensioned engine drawings did not produce
a verified production model for this truck. A frequently surfaced drawing set is
[George Britnell's miniature engine](https://www.homemodelenginemachinist.com/threads/ford-300-inline-six-drawings.23281/):
its author specifies a 0.750-inch bore, 0.875-inch stroke and splash lubrication.
It is a different model-engine design and must not be scaled into production CAD.
The publicly indexed Ford Performance dimensions sheets mainly concern other
engine families; a similar displacement or Ford name does not establish applicability.
A partial candidate is an [EFI plenum-flange CAD listing](https://www.etsy.com/listing/1243727070/ford-300-efi-plenum-flange-cad-model).
Its existence was found in search, but the product page could not be retrieved;
its dimensional basis, applicability and license have not been verified, and no
file was purchased or used. It is not a complete engine CAD reference.
These searches are not proof that no useful drawing or scan exists elsewhere.

## Useful ways to close the gaps

A trustworthy dimensioned drawing or scan of matching parts can establish casting
shape and mounting datums. A dimensional survey of matching loose components can
supply missing interfaces. Exterior photographs with scale references can improve
recognizable contours and routing, but cannot establish hidden galleries, chambers
or the internals of sealed assemblies. Installed casting/part markings can narrow
variants without treating a later replacement catalog number as the installed part.

No teardown is required to use this viewer. Until stronger evidence is obtained,
the remaining work can expand the educational reconstruction, but cannot honestly
be signed off as the complete accurate engine requested.

## Follow-up research, 2026-09-23

The [new research round](ENGINE-RESEARCH-2026-09-23.md) found usable manufacturer
replacement dimensions for pushrods, damper, camshaft motion constraints and core
plugs. Melling vehicle lookup also confirmed part-number leads. These findings
reduce specific component gaps; the unresolved casting and assembled-datum gaps
above remain. See `inventory/engine/replacement-specs-2026-09-23.json` before
changing CAD. This research does not claim that every remaining dimension must
be obtained by measuring the truck.
