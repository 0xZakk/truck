# Component contract and handoff: accelerator-cable-bracket

## Contract

- Issue: [#16](https://github.com/0xZakk/truck/issues/16), confirmed by integration owner. Parent: engine system.
- Contributor: bracket interface worker; integration owner: coordinating agent.
- Baseline: d410ca6666d764b02b392e07e05befd1c4309e9c. Manifest hash recorded by checker.
- Scope: explicit estimated educational mounting stack, candidate bracket and two replacement stud envelopes. No factory dimensional certification, real thread/load verification or cables/linkage.
- Owned: cad/engine/pilot/throttle-bracket/, scripts/pilot/throttle-bracket/, inventory/engine/pilot/throttle-bracket/, this handoff. Shared assembly edits belong exclusively to integration owner.
- Coordinates: world CAD millimeters, X stud axis; bracket occurrence identity transform in throttle-assembly. Mount centers Y74,Z464/516, casting face X378.5; inherited estimates.
- Interface proposal: retain inward stud end X356, extend outward end386→390 (34 mm length, center373). Nut centers381.5→383.5 to clamp2 mm sheet. Full6 mm nominal engagement plus3.5 mm protrusion. Source-backed engineering rationale, expressly NOT a sourced Ford stud length.
- Inputs: local cad/engine/generated throttle housing/gasket/intake/IAC/TPS/shaft/plate/stud/nut STEP; restore through docs/CAD-ARTIFACTS.md.
- Checks: exact overlap <=0.1 mm³; contact area>1 mm²; axial engagement>=6 mm; protrusion>=2.5 mm (two assumed1.25 mm pitches; pitch unknown for actual truck). Negative controls old30 mm stud and nut shifted1 mm off seat. No claimed thread strength.

## Evidence ledger

| Feature | Value | Class | Source / applicability |
|---|---|---|---|
| Bracket shares throttle-body retention, four studs/nuts | assembly order | verified application | [1994 4.9L factory procedure](https://charm.li/Ford/1994/F%20150%202WD%20Pickup%20L6-300%204.9L/Repair%20and%20Diagnosis/Powertrain%20Management/Fuel%20Delivery%20and%20Air%20Induction/Throttle%20Body/Service%20and%20Repair/), installation steps2–5, accessed2026-09-26 |
| Full nut engagement and protrusion rationale | avoid incomplete end threads | engineering guidance, not Ford specification | [Bolt Science short bolting](https://www.boltscience.com/pages/shortbolting.htm), accessed2026-09-26 |
| Formed bracket topology | tapered web, fork ears, cable holes | inferred | prior pilot salvage photo listing375325588661; no dimensions/exact variant |
| Stud34 mm, diameter8 mm; pitch1.25 mm allowance; bracket2 mm; nut6 mm | all mm | inferred educational stack | deliberately chosen envelope with preserved inward endpoint; actual thread, grade, installed depth unknown |

## Delivery

- Branch: engine/finish-component-interfaces; worker did not commit or change shared assembly.
- Readiness: candidate for explicitly limited educational installation; factory fastener/interface identity remains open.
- Bracket shape unchanged; concrete geometric improvement is two longer proposed stud envelopes with unchanged inward ends and correctly seated nuts.
- API: `candidate.shape(p=None)`, `candidate.build(api)` with five-function assembly API; `candidate.mounting_stud_shape()` returns centered local34 mm X-axis smooth cylinder.
- Integration proposal: call bracket `build(api)` after throttle group exists. Preserve `throttle-stud-3`/`throttle-stud-4` occurrence IDs but reference a separate estimated bracket-stud definition, using `mounting_stud_shape()` and position `(373,74,z)`. Preserve nuts3/4 IDs, change position to `(383.5,74,z)`; z464/516 respectively. Other stud/nut occurrences unchanged. Register learning source IDs. Record estimated status in installed learning fields. Root owner owns all these shared changes.
- STEP/GLB: `cad/engine/pilot/throttle-bracket/accelerator-cable-bracket.{step,glb}` and `bracket-mount-stud-estimated.{step,glb}`. STEP regenerated locally, excluded by artifact policy; no new release dependency needed.
- Evidence/learning, report, log and two renders: `inventory/engine/pilot/throttle-bracket/`. Actual rendered CAD tessellation in `preview.npz`; individual/world bounds match reloaded GLB.
- Environment: macOS, Python3.13.12, build123d0.10.0, trimesh4.7.4. Rendering via system Python with matplotlib3.10.9 and numpy. `.venv-cad` lacks matplotlib; use separate renderer as below. Model/effort and token usage unavailable to worker.
- Reproduction from repository root after restoring checkpoint assets:

```sh
XDG_CACHE_HOME=/tmp/truck-bracket-cache .venv-cad/bin/python scripts/pilot/throttle-bracket/build_check.py > inventory/engine/pilot/throttle-bracket/build-check.log 2>&1
XDG_CACHE_HOME=/tmp/truck-bracket-cache MPLCONFIGDIR=/tmp/truck-bracket-mpl python3 scripts/pilot/throttle-bracket/render.py
python3 -m compileall -q cad/engine/pilot/throttle-bracket scripts/pilot/throttle-bracket
```

Cache locations contain no required inputs. Prior checker dependence on personal `/private/tmp/truck-desktop-integration-20260925` is removed. Required neighbor assets fail loudly if missing. Source/current manifest and STEP hashes are in validation.json; shared integration changes invalidate the whole-manifest hash and require rerun.

## Validation and review

| Gate | Result | Evidence / limits |
|---|---|---|
| Application/coverage | PASS limited educational scope | 1994 procedure supports retention arrangement, not exact bracket variant or dimensions |
| Dimensions/coordinates | PASS estimated envelope | baseline datums retained; every new size explicitly inferred |
| CAD/export | PASS | valid one-solid bracket, watertight mesh, STEP volume roundtrip error2.45e-9 mm³, GLB bounds error0 mm; validation.json |
| Source/visual comparison | PASS topology only | actual CAD context and standalone views visually inspected; tapered web, holes and fork ears preserved from prior pilot. Planar bends remain more angular than salvage photograph; no new photo dimension claims |
| Installed interfaces | PASS nominal envelope / NOT RUN actual threaded retention | each nut contact36.64296 mm², nominal axial coverage6 mm, protrusion3.5 mm, bore radial clearance0.2 mm. Added stud segment has zero exact overlap with checked housing/gasket/IAC/TPS/intake. Smooth cylinders do not establish flank contact, thread engagement, material strength or intake anchorage |
| Motion/disassembly | PASS sampled plates / NOT RUN complete mechanism | 0/45/90° twin plate samples and shaft clear bracket; cables, spring, shield, linkage sweep and staged physical disassembly absent |
| Learning/diagnostics | PASS limited scope | learning.json preserves functional explanation and explicit retention limits |
| Browser integration | NOT RUN | integration owner must install, inspect deep link, selection, isolation, explosion/reset, motion and errors |
| Reproduction/review | PASS local reproduction / pending independent review | validation.json input/output hashes, commands above; integration owner review required |

- Sensitivity: original30 mm stud rejected at5.5 mm coverage and−0.5 mm protrusion; nut shifted1 mm away rejected for zero face contact despite sufficient axial coverage. Check asserts both failures.
- Source versus render comparison: inherited silhouette remains photo-informed; fresh assembled context shows both stud ends projecting beyond seated nuts. No thread helix is drawn or represented as validated.
- Verdict: useful candidate for educational integration with explicit limits; not factory-verified or production fastener advice. Issue#16 remains open until agreed installation/browser scope accepted and unresolved manufacturing limitations recorded.
- Next action: integration owner reviews proposal, applies coordinated stud definition/nut transforms, then runs affected integrated checks/browser review. No worker process remains running after handoff.

## Integration-owner checkpoint

Provisionally installed on manifest `f725260d8f1497a1b6f2aed9d41d01155bf2a82e7391d24ce866f352bb50cd5b`. Current installed checks and whole-static audit pass (4,944 exact pairs, zero overlaps above 0.1 mm³). Browser selection, individual explanations, assembled view, explosion/reset and applicable throttle motion were inspected; see `inventory/engine/component-interface-browser-review.json`. CAD source renders were compared with the cited reference topology. Production dimensions, identities and the other explicit gaps above remain unresolved; issue stays open. This accepts the educational addition for integration, not the complete component ticket or a factory-exact replica.
