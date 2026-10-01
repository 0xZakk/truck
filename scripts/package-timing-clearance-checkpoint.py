"""Package frozen follow-up evidence; no active engine parts are replaced."""
from pathlib import Path
import argparse
import hashlib
import json
import tarfile

ROOT = Path(__file__).resolve().parents[1]
GENERATED = ROOT / "cad/engine/generated"
FOLDERS = (
    "timing-pump-foot-candidate", "timing-pump-foot-faceted-candidate",
    "timing-valvetrain-inclined-candidate", "timing-valvetrain-inclined-neighbors",
    "timing-pan-access-candidate", "timing-pan-oil-boundary",
    "timing-block-combined-candidate",
)
OWN_IMAGES = {"pump-foot-render.png", "block-glb-review.png", "block-glb-render.png",
              "lower-stack-section.png", "adapter-comparison.png", "rocker-cover-conflict.png",
              "review.png", "rim-review.png", "roof-section-review.png"}
LOG_PREFIXES = ("timing-block-combined-", "timing-valvetrain-inclined-")


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    base = json.loads((ROOT / "docs/cad-timing-support-checkpoint.json").read_text())
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
            if path.suffix.lower() not in (".json", ".step", ".glb", ".npz", ".log", ".txt", ".py", ".png"):
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
    report = {"release_tag": "studies-2026-10-01-timing-clearance", "asset": args.output.name,
              "sha256": sha(args.output), "size_bytes": args.output.stat().st_size,
              "files": len(files), "required_base_release": base["release_tag"],
              "required_base_archive_sha256": base["sha256"],
              "manifest_sha256": base["manifest_sha256"],
              "scope": "Frozen analytical/faceted pump feet, inclined linkage/passages and failed peak-cover check, rejected pan wall and capped-void failures, combined block composition/mesh. Candidate evidence only, no installation. Excludes active front-block, rocker crest and dry-side wall revisions. No source originals or owner photos.",
              "file_sha256": hashes}
    (ROOT / "docs/cad-timing-clearance-checkpoint.json").write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps({k: v for k, v in report.items() if k != "file_sha256"}, indent=2))


if __name__ == "__main__":
    main()
