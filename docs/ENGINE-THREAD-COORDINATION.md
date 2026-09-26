# Concurrent engine workspace edits detected

At2026-09-25 21:23UTC this continuation detected another desktop continuation
writing the same rear-mount files and `docs/NEXT-SESSION.md`. This thread is
avoiding further shared geometry/integration edits until ownership is clarified.
The user has been asked asynchronously which session should own integration.
Do not revert or overwrite the other session's work.

## Verified published checkpoint

Manifest90807873b8c58234650e03b08557e524044f800d8fc3de97e212dd644e816cb9:
688definitions /1244occurrences. This thread's build31395, rear/front installed
audits81984, eye/dowel/explosion24701, whole-static54208 and installed renders95471
are all terminal PASS. Static4542 exact checks have zero overlaps above0.1mm3.
Navigation1244/1438 and162 local capture hashes pass. The entire engine remains
unfinished; rear collector/EGR takeoff location and production dimensions remain
unverified.

## Candidate ownership conflict

This thread attempted a rear mount module with stations+40mm forward of both
outer rear ports, using rectangular runner relief. The on-disk module instead
contains stations(-65,315) and(-292,315), three-value station tuples and direct
helper imports. Its SHA256 is
`bf9a84d292d5ad4e95576a4db4cc64a10113f1cfded51aa2fc6e9bdd568a12d3`.
Its origin must not be attributed to this thread's intended candidate.

This thread's checker `scripts/check-rear-manifold-mounts.py` expects a different
module API (`hardware`, `profile`, two-value station tuples). Audit92934 is terminal
FAIL at import/API validation. Reconcile the module/checker as a pair before
using this checker; no candidate clearance pass is claimed here. Diagnostic14356
and preview21699 ran during this conflict, without a reliable frozen source hash
for the diagnostic; they do not validate the intended+40mm candidate.

The manufacturer's head-facing rear photo shows both end holes offset to the
same side of their respective mouths, unlike a symmetrical front mounting pattern.
The Ford1994 numbered sequence image should determine which outer port each
bolt15/16 belongs to and orientation. No pixel-to-millimetre scaling is justified.
Check all rectangular corner probes after adding lugs: circular-only15mm relief
can restore unwanted material in rectangular entry corners.

The existing `/private/tmp/truck-rear-mounts-candidate.log` confirms two rear
passage obstructions:124.490318mm3 atX-31.896 and123.229113mm3 atX-259.48. It ends
in AssertionError. Its line-number text no longer matches the current checker
because that file was edited concurrently. Do not treat this candidate as passed.

The other continuation's checkpoint lists independent belt-layout, valve-motion
and oil-pan-fastener workers. This thread has no live subagents and will not
duplicate those candidates. It has not terminated any other session's jobs.
