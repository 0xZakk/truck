# Belt datum follow-up after the 1994 carrier correction

The shared carrier and its actual installed joints passed the independent saved-geometry checker in the isolated assembly (195 intersections, zero overlaps). This validates the implemented joints, not the factory accessory center coordinates or a belt installation.

`scripts/check-carrier-1994-belt-datums.py` reproduces the remaining analytic study. The new carrier's assumed pulley stations give a 2908.071mm outside-radius loop and a 2930.361mm illustrative cord loop. The optimistic full 360° scan of the provisional 75mm tensioner arm still has a minimum outside-radius loop of 2769.406mm. This scan ignores spring travel limits and swept collisions, so it cannot authorize a position even at its minimum.

The study uses the earlier 2491mm replacement catalog figure only as a comparison. Ford TSB94-10-19 identifies E8TZ-8620-T / JK6-984-B for the relevant truck class; it does not give an effective length. Overall pulley diameter, groove-root radius, cord radius and catalog effective gauge must remain distinct.

## Next geometric correction

Resolve the alternator installation jointly with its support and intake/coolant outlet envelopes. The present ALT and PS centers both have Z410, while the corrected carrier puts the tensioner wheel at Z350. Ford's routing schematic places the tensioner below the PS but above the alternator. Therefore the carrier alone is not a completed front accessory layout. Previous attempts lowering the alternator into an approximately schematic order met the present coolant outlet geometry; those attempts remain rejected. Moving a pulley without its support or hiding that interference is not an acceptable fit.

Before another layout optimization, establish the automotive water-pump pulley identity and OD, pump hub-to-crank vertical spacing, and the crank pulley's belt-running datum. E7TZ8509E is a lookup lead only, not a verified specification. Current 150mm pump-pulley OD and 170mm center height are authored assumptions. Dorman594-152's sourced envelope OD does not establish its effective running diameter.

## Research exclusions

[Foley Tech Tip221](https://www.foleyengines.com/tech-tip-221-ford-300-water-pump-identification/) explicitly differentiates industrial pumps from automotive applications. Its industrial flange and shaft dimensions must not be used to close the truck's geometry gap. See the dedicated source page.

[Ford Racing basic engine dimensions](https://www.trackey.ford.com/download/pdfs/EngineDimensions.pdf), page1, lists the 1965–96 300I6 core bore, stroke, bore spacing and deck height, but provides no automotive pump/pulley center datum. It cannot resolve this accessory fit. No engine geometry was changed from this research.
