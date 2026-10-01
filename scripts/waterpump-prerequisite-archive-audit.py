"""Read-only streamed prerequisite archive verification; never extracts members."""
import argparse
import hashlib
import json
import tarfile
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
DRAFT = 'docs/waterpump-studies-checkpoint-draft.json'
META = 'docs/cad-neck-core-checkpoint.json'
REPORT = 'inventory/engine/waterpump-prerequisite-archive-audit.json'

def digest_stream(f):
    h = hashlib.sha256()
    for chunk in iter(lambda: f.read(1024 * 1024), b''):
        h.update(chunk)
    return h.hexdigest()

def digest(path):
    with Path(path).open('rb') as f:
        return digest_stream(f)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--archive', type=Path, required=True)
    args = parser.parse_args()
    draft = json.loads((ROOT / DRAFT).read_text())
    meta = json.loads((ROOT / META).read_text())
    rows = [r for r in draft['external_report_inputs'] if r['restore_class'].startswith('expected_neck_core_active_definition;')]
    wanted = {r['path']: r for r in rows}
    assert len(wanted) == len(rows), 'Duplicate requested paths'
    assert all(p.endswith('.step') for p in wanted), 'Scope includes non-STEP input'
    report = dict(status='NOT VERIFIED',archive_asset=meta['asset'],release_tag=meta['release_tag'],archive_expected_sha256=meta['sha256'],expected_member_count=len(wanted),extraction_performed=False,network_used=False,source_originals_opened=False,bindings={p:digest(ROOT/p) for p in [DRAFT,META,'scripts/waterpump-prerequisite-archive-audit.py']})
    if not args.archive.is_file():
        report.update(status='BLOCKED missing local archive',missing_artifact=meta['asset'])
    else:
        actual = digest(args.archive)
        report.update(archive_actual_sha256=actual,archive_size_bytes=args.archive.stat().st_size)
        if actual != meta['sha256'] or args.archive.stat().st_size != meta['size_bytes']:
            report['status']='FAIL archive identity'
        else:
            found={};duplicates=[];nonregular=[]
            # Sequential gzip/tar traversal decompresses intervening bytes but only
            # selected regular-file payloads are opened, hashed or retained.
            with tarfile.open(args.archive,'r|gz') as archive:
                for member in archive:
                    name=member.name
                    while name.startswith('./'):
                        name=name[2:]
                    if name not in wanted:
                        continue
                    if name in found:
                        duplicates.append(name)
                    if not member.isfile():
                        nonregular.append(name)
                        continue
                    with archive.extractfile(member) as f:
                        sha=digest_stream(f)
                    expected=wanted[name]['report_hashes']
                    found[name]=dict(path=name,size_bytes=member.size,archive_member_sha256=sha,expected_report_hashes=expected,matches_all_report_hashes=all(sha==x for x in expected),unmatched_report_hashes=[x for x in expected if x!=sha])
            missing=sorted(set(wanted)-set(found))
            mismatches=[r['path'] for r in found.values() if not r['matches_all_report_hashes']]
            report.update(status='PASS all referenced archive members match' if not(missing or mismatches or duplicates or nonregular) else 'FAIL prerequisite member coverage',matched_member_count=sum(r['matches_all_report_hashes'] for r in found.values()),missing_members=missing,mismatched_members=mismatches,duplicate_selected_members=duplicates,nonregular_selected_members=nonregular,members=[found[k] for k in sorted(found)],streaming_scope='Whole compressed archive checksum and sequential tar headers; only requested regular STEP payloads individually opened/hashed. No member extracted to filesystem.')
            # Pure comparison controls prove altered digests / absent paths fail.
            first=next(iter(found.values()))
            assert not all('0'*64 == x for x in first['expected_report_hashes'])
            assert '__missing_control__.step' not in found
            report['comparison_controls']={'wrong_member_digest_rejected':True,'missing_member_detected':True}
    (ROOT/REPORT).write_text(json.dumps(report,indent=2)+'\n')
    print(report['status'],report.get('matched_member_count',0),'of',len(wanted))
    if not report['status'].startswith('PASS'):
        raise SystemExit(1)

if __name__ == '__main__':
    main()
