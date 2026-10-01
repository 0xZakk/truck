# Component handoff: front crankgear actual-owner diagnosis

## Contract

Research-only follow-up requested by root after the frozen front-clearance research. Issue #32 under engine #1; baseline8547c589d3c086bad91baf879219612bcd9a162f, branch engine/timing-support-joints. New diagnostic files only; no cut or candidate is built. Root owns integration/publication. All prior pump-foot and clearance-research files remain frozen.

Compare actual cover/socket STEP, block and refined crank gear, distinguish actual material from radius10 guard overlap, and classify relocated versus20unchanged pan stations with `timing_cover_attachment_v2.RELOCATIONS`. Probe the existing estimated thread wall and blind floor without changing either. Millimeters, existing world frames, no new dimensions or transforms. Inputs are frozen candidate outputs under repository-relative generated folders; restore via `docs/CAD-ARTIFACTS.md` and their component handoffs. No temporary input dependency.

## Evidence and findings

Everything here is geometric evidence about estimated candidates, not factory measurements or strength acceptance. Source ownership is explicit: future-block-land owns relocated stations10/20; cover owns21/22/23. Canonical positions of those five are retired in this proposed joint. The other20stations stay active in the block. OldX371/Y0 boss23 proximity is historical, not an active production clearance requirement after relocation toX390/Y0.

Actual complete gear/cover overlap is zero, minimum separation0.220022610 mm. The cover-owned physical center socket has the same minimum gear distance. The radius4.18..6.2 annular thread-wall guard atZ−59.2..−44.7 is fully present and1.554251443 mm from the gear. The radius3.95 central floor atZ−44.4..−43.4 is fully present for its entire estimated1mm thickness, with0.242672971 mm gear separation. These thin-wall/floor dimensions are inherited comparison assumptions, not production specifications.

Actual block/cover overlap already totals24865.084929435 mm³. In the radius10 center-socket region alone, overlap93.760709821 mm³ extends X380..381/Y±4.358899/Z−59.4..−43.4. The proposed block removal intersects4.324736524 mm³ of that shared outer boss material, and does **not** intersect the protected thread annulus or central floor. Thus this particular guard overlap does not mean a block-only cut would damage cover retention. It also does not resolve the other89.435973296 mm³ of local overlap or the much larger overall incompatibility.

The analytic cylinder intersects31.434384627 mm³ of the protected cover floor if applied to the cover itself. Its authority must therefore remain block-only; never generalize the cutter to all neighboring parts. Main gasket, pan gasket and terminal sealant have zero intersection with proposed block removal or the envelope. These are static surface/material checks, not oil leak/pressure/strength tests.

## Delivery and reproduction

- API: read-only `scripts/diagnose-timing-front-crank-owner.py`; no model API or geometry candidate.
- Report: `inventory/engine/timing-front-crank-owner-diagnosis.json` includes all25station ownership classifications, input hashes, actual distances/volumes and protected wall/floor presence.
- Witness STEPs: `cad/engine/generated/timing-front-crank-owner-diagnosis/` contains actual center socket, local shared material, proposed removal shared with cover, wall and floor guards. These are diagnostic excerpts, not manufactured separate parts.
- macOS, Python3.13/build123d0.10.0; model/effort/usage unavailable. No environment changes.
- Run `XDG_CACHE_HOME=/tmp/truck-cache .venv-cad/bin/python scripts/diagnose-timing-front-crank-owner.py > cad/engine/generated/timing-front-crank-owner-diagnosis.log 2>&1` and `python3 -m py_compile scripts/diagnose-timing-front-crank-owner.py`.
- No release/PR yet; root handles publication and shared tracking.

| Gate | Result |
|---|---|
| Application/coverage | Geometric research scope complete; factory application/contour unknown. |
| Dimensions/coordinates | PASS inherited world frames and explicit old/new owner classification. |
| CAD/export | Actual input cover valid; diagnostic witnesses only, no candidate export claim. |
| Source/visual | Prior exact CAD section retained; no new physical-source comparison. |
| Interfaces | Actual wall/floor and gear clearance probes PASS; overall block/cover compatibility FAIL from existing overlap. |
| Motion/disassembly | NOT RUN; static research. |
| Learning/diagnostics | N/A, installed content unchanged. |
| Browser | NOT RUN; no installed candidate and earlier root security block. |
| Reproduction/review | Input hashes and local syntax checked; root review pending. |

## Next action

Root can consider a tightly scoped block-only analytic clearance study while keeping residual block/cover overlap explicit, or first define a coherent front-web ownership/retirement contract. No neighbor-shaped subtraction, no change to the cover's thread wall/floor, and no implicit deletion of20active mount supports. A future complete joint needs declared block/cover material partition, oil boundary and sealing-seat continuity, not merely a gear-clearance pass. No processes remain; no background work claimed.

Final report SHA-256: `82a776b454c669ec98d8287b7fe7b5ac75060cb2551555e70ae0eae60989b003`; all input and witness hashes verified.
