# Component contract and handoff: waterpump-port-registration-audit

## Contract

Issue32/47; root integration owner, pump_foot_resume worker. Baseline8c2d2d9a1400acf784e04581a61e6a6ede38d3ba. Read-only source correspondence and existing tool-obstruction ownership, separate from frozen rear-flange FAIL. Own new registration/localization scripts, reports and this handoff. No source originals redistributed or geometry modified by this audit.

## Source comparison and handedness

Gates44009 front/rear/side product images were re-viewed along with Fel-Pro13816 gasket and applicable automotive block-front source. The product's large lateral neck, formed smaller heater tube and four accessible mounting lugs are visible. The images do **not** show or justify drilling long tool tunnels through the coolant chamber.

The distinct larger fifth aperture and its adjacent smaller mounting hole remove the fourfold ambiguity of the other holes. All five rear-image centers were manually marked in original pixels and matched to the existing provisional aperture pattern. A separate front-view mapping uses the corresponding four lugs; front and rear require opposite image handedness. The audit explicitly tests both parities, every permutation of the four smaller holes while fixing the larger aperture, and wrong fifth-aperture identity. Original images stay unmodified. Pixel coordinates and uncertainties are reproducible in `scripts/research-waterpump-neck-registration.py` and its report.

|Registration/control|RMS residual in inherited model-mm|
|---|---:|
|Correct rear handedness/5identities|1.990423|
|Wrong rear handedness|64.803375|
|Best wrong smaller-hole permutation|35.851817|
|Best wrong larger-fifth identity|16.942534|
|Correct front handedness/4identities|0.584234|
|Wrong front handedness|66.232778|
|Best wrong front correspondence|11.134267|

The correct rear/front neck outward directions are−132.520°/−128.509° in the existing pumpYZ frame; the current analytic neck points along+Y,0°. Rear pixel perturbation±4px at mounts and±8px at neck endpoints,1000seeded samples, stays in−147.144°..−119.627°. This is only landmark sensitivity: projective/axial parallax and specimen differences remain unbounded. Similarity scaling uses the **existing estimated** mounting pattern and does not create sourced millimeter dimensions.

The source also places the smaller heater root in an approximate116°..131° radial sector, versus the current modeled root near161.6°. The front and rear root pixels do not lie in the flange plane, so this angle has additional parallax uncertainty. It is evidence against treating the old heater direction as fixed factory data, not authorization to move a connected tube silently.

## Existing obstruction ownership

`inventory/engine/waterpump-port-access-research.json` intersects actual canonical tool/housing witnesses with declared source-module port stock:

- Station2's7604.417156mm³ obstruction is entirely in the large inlet construction.
- Station3's504.587271mm³ obstruction is entirely in the heater boss construction.
- Stations1/4 have no pump-self obstruction for this tool envelope.

Thus the evidence points to guessed port orientation rather than missing drilled access passages in the main chamber. These results do not prove that every production socket fits; the toolR10.5 is a declared envelope.

## Proposed analytical reconstruction boundary

Retain all4 mounting axes, rear bore/flange contract, shaft/impeller/bearing/hub datums and separate physical ownership. First reconstruct the large inlet analytically at a declared source-angle estimate around−130°, and compare the old source replay against the actual housing before replacing anything. Source-derived orientation and retained estimated dimensions must be separate parameters. The current+25mm transverse offset is also provisional; front/rear neck-line fits require explicit review before selecting a replacement. Do not rotate the entire pump or move its four-hole gasket.

Actual checks must include coolant passage continuity into chamber, real walls, rear gasket/bolt seats, both old and new port regions, cover/main screw access, pulley/fan/alternator/Thermactor brackets, existing heater connection and available hose endpoints. The source supports a cast arm with a beaded neck; it does not dimension its internal curve or certify hydraulic performance. A narrower tube made merely to pass collision checks is not supported.

The heater port needs its own coordinated casting/tube contract if later revised; an inlet-only study must retain station3's inherited accessFAIL. No blind neighbor or tool-envelope subtraction is proposed.

## Delivery and reproduction

Reports: `inventory/engine/waterpump-neck-registration-research.json`, `waterpump-port-access-research.json`, `waterpump-neck-registration-render.json`. Diagnostic actual tool-intersectionSTEPs and new registration figure reside in `cad/engine/generated/waterpump-port-access-research/`. Figure uses plotted landmark data rather than redistributed source images.

```sh
python3 scripts/research-waterpump-neck-registration.py
.venv-cad/bin/python scripts/localize-waterpump-port-access.py
MPLCONFIGDIR=/tmp/truck-gear-mpl python3 scripts/render-waterpump-neck-registration.py
```

Quality: source application/topology PASS with replacement limits; dimension fidelity unknown; handedness/control tests PASS; current accessFAIL preserved; geometry/export/motion/browser N/A for this read-only audit. Root review pending. No canonical/private stage changes. Full rear candidate remains frozen under its own FAIL report. Usage unavailable.
