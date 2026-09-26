# Alternator carrier candidate integration

This candidate corrects the Ford routing schematic's qualitative vertical order: PS center410, tensioner350, alternator320mm. Alternator Y−325 and belt planeX473.56 remain unchanged. The owner's passenger-side photo supports the front/passenger-side installation but cannot supply calibrated center distances. All coordinates and support contours remain approximate.

## Candidate and integration

Use `cad/engine/alternator_carrier_1994_candidate.py`.

1. Replace only the `alternator-support-bracket`, `alt-bracket-bolt-1`, and `alt-bracket-bolt-2` definitions with `replacements()` shapes. These shapes are already in world coordinates, as were the old support definitions.
2. For each occurrence whose parent is `alternator-assembly`, use `placement_override(occurrence)` to set absolute local position `(473.56,-325,320)`. Retain its existing rotation and its local part definition. This placement override is idempotent; the independent candidate audit still expresses the original922ac5c8-to-candidate movement as a90mm downward displacement.
3. Keep the two `alt-engine-bracket-bolt-*` occurrences and the original block/head receiver bosses. No engine or coolant-outlet geometry adapter is needed.
4. Add the candidate's sources/limits to changed support metadata and replace the old stated alternator station with the new explicitly provisional position. No definition/occurrence count changes are expected.

The current shared PS/AC/tensioner carrier remains untouched. No belt is installed or declared fitted by this change.

## Verification

On isolated manifest `922ac5c8f0708ca58ab598c1c711685d8fbafea2ca640b250913f278ab6fded8`:

- 29 candidate components passed STEP round trips.
- 93 exact candidate/candidate or candidate/full-engine intersection checks found zero overlaps above0.01mm³, with1272 fixed neighbors considered by broad phase.
- Both existing head/block seats have zero gap. Withdrawing the bracket2mm produces a2mm gap at each seat; penetrating0.2mm produces141.843mm³ overlap at each seat. These negative controls demonstrate the checks detect lost contact and interference.
- The assembled and exploded preview was visually reviewed: attachment ribs join the ring and the two existing engine feet; the alternator assembly follows its rebuilt ring, and carrier topology remains separate. The wide lateral span is inherited provisional geometry, not a measured production casting.

Reports: `inventory/engine/alternator-carrier-1994-candidate-validation.json` and `inventory/engine/alternator-carrier-1994-joint-validation.json`.

Preview: `reference/engine/alternator-carrier-1994-preview.png`. The preview contains selected context, not every engine part; all installed neighbors were considered by the intersection checker.

Run the candidate checker and joint checker with `--assembly-root` pointing at a frozen copy. After integration, run the candidate checker with `--installed` to compare the three actual saved support definitions and all26 actual alternator placement matrices against the candidate before the full-neighbor audit. The installed report is written inside the specified assembly root. A candidate-only pass does not certify integration.

## Outstanding belt and pump datums

The unchanged coolant-outlet envelope still constrains the belt route. No unverified pump or outlet dimensions have been changed to make a belt fit. Gates' automotive catalog identifies44009 for1993–96 4.9L F-series, but the new search did not establish a trustworthy hub height. Search snippets with5.62-inch hub height belong to7.5L V8 applications and were excluded. Industrial CSG649 dimensions likewise cannot be transferred. Coordinate further pump/outlet correction with the independent engine-joint work.
