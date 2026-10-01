# Water-pump prerequisite archive audit

Root-assigned reproducibility audit under engine #32/#47. Own only this handoff, `scripts/waterpump-prerequisite-archive-audit.py` and `inventory/engine/waterpump-prerequisite-archive-audit.json`. No checkpoint metadata, source originals, manifests or existing geometry changed.

**PASS: all691 referenced canonical STEP members are present and match every expected report hash.** The locally available `truck-active-cad-20260930-neck-core.tar.gz` was located in `/private/tmp`. Its461,888,908-byte size and SHA-256 `27599d6d0c60276009e494a4d2412fc56cb3c71a326529de37ca68faf71b812f` match `docs/cad-neck-core-checkpoint.json` and the prerequisite documented in `docs/CAD-ARTIFACTS.md`.

The checker reads the expected-neck-core classification from the exact bound `docs/waterpump-studies-checkpoint-draft.json`. It hashes the compressed archive, then traverses tar headers sequentially and opens only the691 referenced regular STEP member payloads. Gzip traversal necessarily decompresses intervening bytes; no unselected payload is individually opened, retained or exported. No archive member is extracted to disk. Source originals were not opened, and no network download occurred.

Results:691 matches, zero missing members, zero digest mismatches, zero selected duplicate members and zero selected nonregular members. Each report row records member path, byte count, observed digest and all expected report digests. Pure comparison controls reject a wrong digest and detect an absent member. No CAD import, geometry acceptance or whole clean-clone rebuild is claimed; this closes only the stated691-member prerequisite provenance gap. Other prerequisite classes and source-access dependencies retain their existing limitations.

Reproduce from repository root:

```sh
python3 scripts/waterpump-prerequisite-archive-audit.py --archive /path/to/truck-active-cad-20260930-neck-core.tar.gz
```

The path is a parameter, not a requirement to use the original worker's temporary directory. Obtain the named private release artifact through the existing authorized process in CAD-ARTIFACTS if unavailable locally; this script never downloads it. A missing local archive is reported explicitly before member checks. The script writes only its dedicated JSON report and binds both metadata files plus its own source. Root can append this audit to new checkpoint metadata without altering frozen expectations. Re-run if draft expectations or archive identity changes.

Review scope: source hash/membership PASS, no extraction/mutation, network N/A. CAD, installation, browser and full restore workflow NOT RUN. No running process; Python3 standard library, usage unavailable.
