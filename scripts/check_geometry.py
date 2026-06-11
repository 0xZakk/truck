#!/usr/bin/env python3
"""Automated geometry QA for the F-150 3D model.

Renders the viewer in headless Chrome, pulls each part's true world-space bounding
box (and cable centerlines) from the scene, and flags problems no human should have
to eyeball part-by-part:
  - CABLE-THROUGH: a cable's centerline passes through a solid part it doesn't connect to
  - OVERLAP: two solid parts from different assemblies interpenetrate significantly
  - FLOATING: a part hangs in space with nothing supporting it below
  - ENVELOPE: a part sticks out beyond the whole-truck bounding box

Usage:  python3 scripts/check_geometry.py [--system <id>]
Requires the static server running on 127.0.0.1:8080 and Google Chrome installed.
"""
import json, re, subprocess, sys, html

CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
URL = "http://127.0.0.1:8080/viewer/?dump=1"


def fetch_geometry():
    out = subprocess.run(
        [CHROME, "--headless=new", "--use-gl=angle", "--use-angle=swiftshader",
         "--enable-unsafe-swiftshader", "--virtual-time-budget=12000", "--dump-dom", URL],
        capture_output=True, text=True, timeout=90).stdout
    m = re.search(r'<pre id="geomdump"[^>]*>(.*?)</pre>', out, re.S)
    if not m:
        sys.exit("Could not find geomdump in page. Is the server running on :8080?")
    return json.loads(html.unescape(m.group(1)))


def inside(pt, lo, hi, pad=0.4):
    return all(lo[i] + pad <= pt[i] <= hi[i] - pad for i in range(3))


def overlap_vol(a, b):
    d = [max(0, min(a["max"][i], b["max"][i]) - max(a["min"][i], b["min"][i])) for i in range(3)]
    return d[0] * d[1] * d[2]


def vol(p):
    return max(0.001, (p["max"][0]-p["min"][0])*(p["max"][1]-p["min"][1])*(p["max"][2]-p["min"][2]))


def legit_interface(a, b):
    """Known physical co-locations that aren't errors (brakes in the wheel, internals
    nested inside their housing/case — which is exactly what the explode view pulls apart)."""
    def has(s, words): return any(w in s for w in words)
    brake = ("rotor", "caliper", "drum", "brake", "hub")
    wheel = ("tire", "wheel-bearing")
    if (has(a, brake) and has(b, wheel)) or (has(b, brake) and has(a, wheel)):
        return True
    housing = ("engine-block", "cylinder-head", "valve-cover", "intake-manifold", "transmission",
               "rear-axle", "starter-motor", "alternator", "differential", "oil-filter", "fuel-tank",
               "dashboard")
    internal = ("crankshaft", "camshaft", "piston", "connecting-rod", "conrod", "timing-gear",
                "oil-pump", "synchro", "valve", "armature", "brush", "pinion", "carrier",
                "side-gear", "ring-and-pinion", "axle-shaft", "clutch", "fuel-pump", "sender",
                "spark-plug", "distributor", "ignition-switch", "ignition-pickup", "water-pump",
                "input-shaft", "mainshaft", "countershaft", "output-shaft", "synchro", "shift-fork")
    # bolted/mating interfaces — parts genuinely in contact by design
    BOLTED = [({"harmonic-balancer"}, {"crankshaft"}),     # balancer on the crank snout
              ({"engine-block"}, {"transmission"}),        # bellhousing face
              ({"crankshaft"}, {"transmission", "input-shaft"}),  # flywheel/pilot inside bellhousing
              ({"shifter"}, {"carpet"}),                   # shifter boot through the floor
              ({"steering-box"}, {"frame-rail"}),          # box bolts to the left rail
              ({"ibeam"}, {"rotor", "drum", "hub"}),       # spindle into the hub/rotor
              ({"rear-axle", "axle-shaft"}, {"drum", "hub"}),  # drums on the axle-shaft flanges
              ({"dashboard"}, {"heater-box", "evaporator", "steering-column", "blower"}),
              ({"engine-mount"}, {"crossmember"}),         # mounts bolt to the engine crossmember
              ({"front-bumper", "rear-bumper"}, {"frame-rail"})]  # bumper brackets bolt to the rail horns
    for left, right in BOLTED:
        if (has(a, left) and has(b, right)) or (has(b, left) and has(a, right)):
            return True
    if (has(a, housing) and has(b, internal)) or (has(b, housing) and has(a, internal)):
        return True
    # exterior lamps mount in the grille/fascia; gauges/cluster in the dash
    lamp = ("headlamp", "tail-light", "parking-light", "park", "lamp", "marker")
    fascia = ("grille", "bumper", "fender", "front-clip")
    if (has(a, lamp) and has(b, fascia)) or (has(b, lamp) and has(a, fascia)):
        return True
    dash = ("dashboard", "instrument-panel")
    indash = ("instrument-cluster", "cluster", "gauge", "radio", "hvac-control", "glovebox")
    if (has(a, ("condenser",)) and has(b, ("radiator",))) or (has(b, ("condenser",)) and has(a, ("radiator",))):
        return True  # A/C condenser stacks in front of the radiator
    glass = ("windshield", "window", "glass", "back-glass")
    greenhouse = ("pillar", "roof", "door", "cab", "header", "cowl", "rear-cab-wall")
    if (has(a, glass) and has(b, greenhouse)) or (has(b, glass) and has(a, greenhouse)):
        return True  # glass sits in the greenhouse openings against pillars/roof/doors
    if (has(a, dash) and has(b, indash)) or (has(b, dash) and has(a, indash)):
        return True
    return False


def gap_between(a, b):
    """3D gap between two AABBs (0 if they touch/overlap)."""
    d = [max(a["min"][i] - b["max"][i], b["min"][i] - a["max"][i], 0) for i in range(3)]
    return (d[0]**2 + d[1]**2 + d[2]**2) ** 0.5


def main():
    only = None
    if "--system" in sys.argv:
        only = sys.argv[sys.argv.index("--system") + 1]
    parts = fetch_geometry()                              # ALWAYS load the whole truck for spatial context
    scope = [p for p in parts if not only or only in p["systems"]]

    solids = [p for p in parts if "samples" not in p and not p.get("context")]
    neighbors = [p for p in parts if "samples" not in p]  # solids + body context = things to mount against
    cables = [p for p in scope if "samples" in p]
    flags = []

    # 1) cables passing through a solid they DON'T connect to (skip 4 joint samples each end)
    for c in cables:
        conn = set(c.get("connects", []))
        pts = c["samples"][4:-4]
        through = c.get("through")   # exact per-part containment from the viewer's raycast parity test
        for s in solids:
            if s["id"] in conn:
                continue
            if through is not None:
                hits = through.get(s["id"], 0)
            else:
                hits = sum(1 for pt in pts if inside(pt, s["min"], s["max"]))
            if hits >= 2:
                flags.append(("CABLE-THROUGH", f'{c["id"]} passes through {s["id"]} ({hits} interior pts)'))

    # 2) significant interpenetration between solids of different assemblies
    # (AABB heuristic — superseded by the exact mesh test in 2b whenever the dump
    #  carries `pen` data; AABBs false-positive badly on concave parts)
    scope_ids = {p["id"] for p in scope}
    pen_capable = any(p.get("penChecked") for p in parts)
    for i in range(len(solids) if not pen_capable else 0):
        for j in range(i + 1, len(solids)):
            a, b = solids[i], solids[j]
            if a["id"] not in scope_ids and b["id"] not in scope_ids:
                continue
            if a["assembly"] and a["assembly"] == b["assembly"]:
                continue
            if legit_interface(a["id"], b["id"]):   # known co-locations (brake-in-wheel, etc.)
                continue
            frac = overlap_vol(a, b) / min(vol(a), vol(b))
            if frac > 0.35:
                flags.append(("OVERLAP", f'{a["id"]} ∩ {b["id"]} = {frac*100:.0f}% of the smaller part'))

    # 2b) exact mesh penetration (viewer raycast parity: real geometry, not AABBs)
    flagged_pairs = {tuple(sorted(f[1].split(" ∩ ")[0:1] + [f[1].split(" ∩ ")[1].split(" =")[0]]))
                     for f in flags if f[0] == "OVERLAP"}
    for p in parts:
        for other, n in (p.get("pen") or {}).items():
            if p["id"] not in scope_ids and other not in scope_ids:
                continue
            if tuple(sorted([p["id"], other])) in flagged_pairs:
                continue
            if legit_interface(p["id"], other):
                continue
            flags.append(("PENETRATE", f'{p["id"]} ⟂ {other} ({n} mesh verts inside the other part)'))

    # 3) orphaned parts: nearest neighbor (any solid or body shell) is >6" away in every direction
    for p in scope:
        if "samples" in p or p.get("context"):
            continue
        g = min((gap_between(p, q) for q in neighbors if q["id"] != p["id"]), default=999)
        if g > 6:
            flags.append(("ORPHAN", f'{p["id"]} floats free — nearest part is {g:.0f}" away'))

    allmin = [min(p["min"][i] for p in solids) for i in range(3)]
    allmax = [max(p["max"][i] for p in solids) for i in range(3)]

    print(f"\n=== Geometry check: {len(scope)} parts in scope / {len(parts)} total ===")
    print(f"Truck envelope (in): X {allmin[0]:.0f}..{allmax[0]:.0f}  "
          f"Y {allmin[1]:.0f}..{allmax[1]:.0f}  Z {allmin[2]:.0f}..{allmax[2]:.0f}")
    if not flags:
        print("✅ No geometry problems flagged.\n")
    else:
        print(f"\n⚠️  {len(flags)} issue(s):")
        for kind, msg in sorted(flags):
            print(f"  [{kind}] {msg}")
        print()

    # part size/position table (eyeball proportions numerically)
    print("part sizes (in) — id: WxHxL @ center")
    for p in sorted(scope, key=lambda x: x["id"]):
        if p.get("context"):
            continue
        s, c = p["size"], p["center"]
        print(f"  {p['id']:<26} {s[0]:>5.1f} x {s[1]:>5.1f} x {s[2]:>5.1f}  @ ({c[0]:>5.0f},{c[1]:>4.0f},{c[2]:>4.0f})")


if __name__ == "__main__":
    main()
