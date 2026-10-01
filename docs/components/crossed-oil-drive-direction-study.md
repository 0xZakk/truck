# Crossed cam/distributor/oil-pump direction study

## Contract before checks

Issues #32/#34, baseline `dafb8175e4e7b328d2a16bdc47914307f044b0c8`, branch `engine/timing-motion-integration`. Root requested a bounded actual-geometry dependency review after accepting the separate pan stage; all pan-stage files remain frozen. Own only this handoff, dedicated checker/report and generated witnesses. No shared transforms, canonical geometry, whole-gear mirror or event-time reversal.

Inputs: rotation-convention research, corrected pose candidate, actual frozen shifted camshaft and canonical distributor/shaft/pump definitions, original declared `oil_drive_layout` tooth construction and actual manifest ratios. Determine signed compatibility from the tooth construction and world axes rather than assigning an unsupported factory hand label. Inspect actual rest/limited-tooth-period fits and the connected hex shaft datums. If current geometry is incompatible, report the exact hand/phase/axis dependency; only a separately justified and reviewed bounded gear-surface revision may follow.

All source drive tooth count16, pitch radius18mm,45° lead,12mm face, phase and20° shaft tilt remain estimates. Melling intermediate length/hex section retain their source class. Positive event time and source-supported distributor direction stay unchanged. Existing local drive ratios do not themselves prove tooth meshing or pump flow direction.

## Frozen discovery result

The two existing tooth generators both use signed lead k=−1/18rad/mm (−38.197186° over12mm), not a source-verified factory hand. Let a=(1,0,0), d=(0,sin20°,cos20°), n=d×a. Pitch contact vectors are18n and−18n. Actual lead tangents are tcam=a−d and tdist=d−a. Their common transverse normal is proportional to a+d; zero relative normal velocity requires **ωdistributor=ωcam**. Legacy−q/2/−q/2 is compatible with that sign relation; proposed+q/2/−q/2 is not. Radial pressure components do not change this signed result because pitch velocities are perpendicular to n.

Actual frozen STEP evidence confirms the dependency: at rest distance0.1690987mm and zero overlap; at(+5.625°, +5.625°) zero overlap/distance0.1701941mm; at(+5.625°, −5.625°) **114.10496282mm³ overlap**. Both(+11.25°, +11.25°) and(+11.25°, −11.25°) clear because the16-tooth periodicity aliases that endpoint. Rest/endpoints alone therefore miss the defect. These samples do not certify the legacy gear design.

The corrected cam axis requires the connected distributor/pump branch translation(0,5.10982099,4.08785679)mm to retain the declared36mm crossed-axis spacing. Leaving the branch unshifted gives32.59646829mm spacing and−5.58899057mm distributor axial registration error. This is a previously declared common-datum dependency, not a new centerline adjustment to hide tooth interference.

After common translation, actual distributor/intermediate/pump-shaft axes are coaxial within7.2e−15mm. Both actual hex interfaces have0.04mm surface clearance and zero rest overlap. Their existing same-axis−0.5 rates preserve their relative pose for arbitrary event angle; pump outer−0.4 retains the modeled4:5 rotor relation. This does not prove hydraulic pumping direction or tooth contact pressure. No downstream ratio reversal is justified by correcting the cam sign.

Discovery report: `inventory/engine/crossed-oil-drive-direction-review.json`. Actual bad-pose STEP components and overlap are in `generated/crossed-oil-drive-direction/`; render `direction-defect-review.png` is bound by the dedicated render report. Source/captured rotation viewing assumptions remain in the root research. No factory tooth-count/hand/phase claim, no CAD repair yet.

Commands: `.venv-cad/bin/python scripts/check-crossed-oil-drive-direction.py`, `.venv-cad/bin/python scripts/export-crossed-oil-drive-witness.py`, `python3 scripts/render-crossed-oil-drive-direction.py`. Existing macOS CAD Python3.13/build123d0.10/trimesh/numpy and system matplotlib; no installation, model/usage unavailable. Input/output hashes and actual sampled poses are retained. Root owns shared transforms. Discovery source comparison is code/actual geometry plus existing direction research, not a new factory gear drawing. Browser/user-facing learning NOT RUN; geometric direction compatibility FAIL; attachment datum checks PASS bounded. Whole motion/pressure/production acceptance remains open.
