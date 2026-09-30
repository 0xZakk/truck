#!/usr/bin/env python3
"""Actual cover section with dimensioned, explicitly hypothetical seal probes."""
from pathlib import Path
import json
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "cad/engine"))
import build123d as b
import front_crank_seal_envelope_candidate as c
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

report = json.loads((ROOT / "inventory/engine/front-crank-seal-envelope-validation.json").read_text())
cover = b.import_step(ROOT / "cad/engine/generated/timing-cover-front-joint-candidate/cover.step")
section = b.section(cover, section_by=b.Plane.XY)
fig, axes = plt.subplots(1, 2, figsize=(13, 6))
for ax, row in zip(axes, report["alignments"]):
    for edge in section.edges():
        points = np.array([tuple(edge.position_at(t)) for t in np.linspace(0, 1, 65)])
        ax.plot(points[:, 0], points[:, 1], color="#25394b", linewidth=1.4)
    rear, front = row["case_axial_interval_mm"]
    for sign in [-1, 1]:
        lo = c.SHAFT_DIAMETER / 2 if sign > 0 else -c.CASE_DIAMETER / 2
        ax.add_patch(Rectangle((rear, lo), c.WIDTH, (c.CASE_DIAMETER-c.SHAFT_DIAMETER)/2,
                               facecolor="#e89f41", alpha=.4, edgecolor="#996000"))
        ax.plot([front, front], [sign*c.HOUSING_BORE/2, sign*c.FLANGE_DIAMETER/2], color="#ad3b26", linewidth=2)
        ax.plot([400, 425], [sign*c.SHAFT_DIAMETER/2]*2, color="#24755e", linestyle=":")
    ax.set_xlim(394, 424)
    ax.set_ylim(-45, 45)
    ax.set_aspect("equal")
    ax.grid(alpha=.2)
    ax.set_xlabel("Engine X (mm)")
    ax.set_ylabel("Section Y (mm)")
    ax.set_title(row["hypothesis"].replace("-", " ") + "\nNOT adopted", fontsize=10)
fig.suptitle("Source-sized front seal envelope versus actual estimated cover section", fontsize=14)
fig.text(.5, .04, "Blue: actual cover section. Amber: envelope, not solid seal material. Red: zero-thickness flange probe.\n"
         "Lip position, case thickness and damper track remain unknown. Both positions require a larger cover bore.",
         ha="center", fontsize=10)
fig.tight_layout(rect=[0, .10, 1, .93])
fig.savefig(ROOT / "cad/engine/generated/front-crank-seal-envelope/section-review.png", dpi=150)
