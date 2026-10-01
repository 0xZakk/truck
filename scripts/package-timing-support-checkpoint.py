"""Package frozen follow-up evidence; no active engine parts are replaced."""
from pathlib import Path
import argparse
import hashlib
import json
import tarfile

ROOT = Path(__file__).resolve().parents[1]
GENERATED = ROOT / "cad/engine/generated"
FOLDERS = (
    "pan-fastener-thread-candidate", "timing-block-support-machining-candidate",
    "timing-cover-attachment-v2", "timing-valvetrain-contract",
    "timing-valvetrain-adapter-candidate", "timing-support-checkpoint",
)
OWN_IMAGES = {"thread-review.png", "block-render.png", "journal-support-sections.png",
              "pump-pan-conflict.png", "attachment-review.png", "adapter-comparison.png"}
LOG_PREFIXES = ("timing-block-support-machining-", "timing-valvetrain-adapter-candidate-")


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    base = json.loads((ROOT / "docs/cad-timing-proof-checkpoint.json").read_text())
    manifest = ROOT / "inventory/engine/full-assembly.json"
    assert sha(manifest) == base["manifest_sha256"]
    files = []
    for name in FOLDERS:
        folder = GENERATED / name
        assert folder.is_dir(), folder
        for path in folder.rglob("*"):
            if not path.is_file() or path.is_symlink():
                continue
            if any(p in path.parts for p in ("__pycache__", "mpl", ".cache")):
                continue
            if "source-comparison" in path.name or "reference" in path.name:
                continue
            if path.suffix.lower() == ".png" and path.name not in OWN_IMAGES:
                continue
            if path.suffix.lower() not in (".json", ".step", ".glb", ".npz", ".log", ".py", ".png"):
                continue
            files.append(path)
    files.extend(p for p in GENERATED.glob("*.log") if p.name.startswith(LOG_PREFIXES))
    files = sorted(set(files))
    hashes = {str(p.relative_to(ROOT)): sha(p) for p in files}
    with tarfile.open(args.output, "w:gz") as archive:
        for path in files:
            archive.add(path, arcname=str(path.relative_to(ROOT)), recursive=False)
    assert all(sha(ROOT / p) == h for p, h in hashes.items())
    assert sha(manifest) == base["manifest_sha256"]
    report = {"release_tag": "studies-2026-09-30-timing-support", "asset": args.output.name,
              "sha256": sha(args.output), "size_bytes": args.output.stat().st_size,
              "files": len(files), "required_base_release": base["release_tag"],
              "required_base_archive_sha256": base["sha256"],
              "manifest_sha256": base["manifest_sha256"],
              "scope": "Frozen pan male and rejected cover attachment v2, block support/machining and pump collision witnesses, valve-linkage contract and rejected pedestal-only adapter. No installation. Excludes active pump-foot, pan dry-side revision and inclined-linkage work. No source originals or photos.",
              "file_sha256": hashes}
    (ROOT / "docs/cad-timing-support-checkpoint.json").write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps({k: v for k, v in report.items() if k != "file_sha256"}, indent=2))


if __name__ == "__main__":
    main()
