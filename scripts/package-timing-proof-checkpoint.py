"""Package frozen follow-up evidence; no active engine parts are replaced."""
from pathlib import Path
import argparse
import hashlib
import json
import tarfile

ROOT = Path(__file__).resolve().parents[1]
GENERATED = ROOT / "cad/engine/generated"
FOLDERS = (
    "timing-block-fixed-stock-candidate", "timing-block-boolean-topology-candidate",
    "timing-block-rear-seat-csg-candidate", "timing-block-rear-seat-repair-candidate",
    "timing-block-rear-seat-topology-candidate", "timing-cover-attachment-candidate",
    "timing-coupled-core-candidate", "timing-rotating-clearance-candidate",
    "front-crank-seal-envelope", "timing-proof-checkpoint",
)
OWN_IMAGES = {"block-render.png", "side-cover-sections.png", "journal-support-sections.png",
              "attachment-review.png", "coupled-core-render.png", "section-review.png"}
LOG_PREFIXES = ("timing-block-fixed-stock-", "timing-block-rear-seat-",
                "timing-block-boolean-topology-", "timing-carrier-machining-",
                "front-crank-seal-envelope-")


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    base = json.loads((ROOT / "docs/cad-timing-studies-checkpoint.json").read_text())
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
    report = {"release_tag": "studies-2026-09-30-timing-proof", "asset": args.output.name,
              "sha256": sha(args.output), "size_bytes": args.output.stat().st_size,
              "files": len(files), "required_base_release": base["release_tag"],
              "required_base_archive_sha256": base["sha256"],
              "manifest_sha256": base["manifest_sha256"],
              "scope": "Frozen fixed-stock failures and topology-only repair, rejected attachment, coupled-core and rotating clearance, seal-envelope diagnostic. No installation. Excludes active support machining, fastener revision and valvetrain work; no original manuals, PDFs or photos.",
              "file_sha256": hashes}
    (ROOT / "docs/cad-timing-proof-checkpoint.json").write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps({k: v for k, v in report.items() if k != "file_sha256"}, indent=2))


if __name__ == "__main__":
    main()
