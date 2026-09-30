#!/usr/bin/env python3
"""Quantify the current seal-envelope mismatch without adopting new placement."""

from pathlib import Path
import hashlib
import json
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "cad/engine"))
import build123d as b
import front_crank_seal_envelope_candidate as c
from cad_metrics import solid_volume

OUT = ROOT / "cad/engine/generated/front-crank-seal-envelope"
OUT.mkdir(parents=True, exist_ok=True)


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def volume(shape):
    if shape is None or getattr(shape, "wrapped", True) is None:
        return 0.0
    return sum(abs(solid_volume(s, "adaptive")) for s in shape.solids())


ledger = ROOT / "reference/engine/front-crank-seal-envelope-review.json"
source = json.loads(ledger.read_text())
cover_path = ROOT / "cad/engine/generated/timing-cover-front-joint-candidate/cover.step"
watched = [Path(__file__), Path(c.__file__), ledger, cover_path]
for item in source["sources"]:
    if "path" in item:
        path = ROOT / item["path"]
        assert sha(path) == item["sha256"]
        watched.append(path)
inputs = {str(p.relative_to(ROOT)): sha(p) for p in watched}
cover = b.import_step(cover_path)
assert cover.is_valid
dimensions = {"shaft_diameter": c.SHAFT_DIAMETER, "housing_bore": c.HOUSING_BORE,
              "case_diameter": c.CASE_DIAMETER, "width": c.WIDTH,
              "flange_diameter": c.FLANGE_DIAMETER}
assert abs(c.CASE_DIAMETER - c.HOUSING_BORE - 0.1016) < 1e-9
rows = []
for name, front in [("front-aligned-with-estimated-cover", 415.0),
                    ("centered-on-old-seal-datum", 414 + c.WIDTH / 2)]:
    probes = c.probes(front)
    envelope = probes["seal-annular-envelope"]
    assert envelope.is_valid and len(envelope.solids()) == 1
    bb = envelope.bounding_box()
    assert abs(bb.size.X - c.WIDTH) < 1e-6
    assert abs(bb.size.Y - c.CASE_DIAMETER) < 1e-6
    # This measures required housing revision, not seal material collision.
    bore_obstruction = volume(cover.intersect(probes["housing-bore-probe"]))
    assert bore_obstruction > 1
    old_clearance_probe = c.cylinder(26.9, 410.1, 414.9)
    old_clearance = volume(cover.intersect(old_clearance_probe))
    assert old_clearance < 1e-5
    saved = {}
    for label, shape in probes.items():
        path = OUT / f"{name}-{label}.step"
        b.export_step(shape, path)
        saved[path.name] = sha(path)
    rows.append({"hypothesis": name, "adopted": False,
                 "case_axial_interval_mm": [front - c.WIDTH, front],
                 "housing_probe_material_obstruction_mm3": bore_obstruction,
                 "old_bore_control_overlap_mm3": old_clearance,
                 "exports": saved})
assert all(sha(ROOT / p) == h for p, h in inputs.items())
report = {"status": "PASS envelope diagnostic; current seat incompatible; no installation",
          "input_sha256": inputs, "replacement_dimensions_mm": dimensions,
          "current_annulus_dimensions_mm": {"outside": 54, "inside": 42, "width": 8},
          "radial_bore_increase_mm": (c.HOUSING_BORE - 54) / 2,
          "nominal_diametral_case_fit_mm": c.CASE_DIAMETER - c.HOUSING_BORE,
          "alignments": rows,
          "limits": ["Probes are envelopes, not physical seal internals",
                     "Neither axial hypothesis is source-established or adopted",
                     "Catalog nominal fit is not a tolerance or deformation model",
                     "Lip, spring, case thickness and damper track remain unresolved",
                     "Flange face has no assumed thickness; no flange support claim",
                     "No canonical changes, installed clearance or browser acceptance"]}
(ROOT / "inventory/engine/front-crank-seal-envelope-validation.json").write_text(json.dumps(report, indent=2) + "\n")
print(json.dumps({k: v for k, v in report.items() if k != "input_sha256"}, indent=2))
