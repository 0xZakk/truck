#!/usr/bin/env python3
"""Extract the factory parts catalog ("Parts and Labor") into a structured BOM ledger.

The catalog is the authoritative parts list. Every leaf page = one catalogued part /
part-group with a Ford part number. This produces `inventory/bom.json`: the master
checklist the build loop ticks off, so "do we have every part?" is auditable, not a guess.

Run: python3 scripts/build_bom.py
"""
import os, re, html, json, collections

FSM = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                   "manuals", "factory-service-manual",
                   "1994 Ford F 150 2WD Pickup L6-300 4.9L")
CATALOG = os.path.join(FSM, "Parts%20and%20Labor")
OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                   "inventory", "bom.json")

# coarse default mapping catalog top-group -> viewer system (the loop refines per part)
GROUP_SYSTEM = {
    "Accessories and Optional Equipment": "exterior-trim",
    "Body and Frame": "body-cab",
    "Brakes and Traction Control": "brakes",
    "Cruise Control": "electrical-body",
    "Engine, Cooling and Exhaust": "engine",
    "Heating and Air Conditioning": "hvac",
    "Instrument Panel, Gauges and Warning Indicators": "interior",
    "Lighting and Horns": "electrical-body",
    "Maintenance": "",
    "Powertrain Management": "engine",
    "Relays and Modules": "electrical-body",
    "Restraints and Safety Systems": "interior",
    "Sensors and Switches": "electrical-body",
    "Starting and Charging": "electrical-starting",
    "Steering and Suspension": "suspension",
    "Transmission and Drivetrain": "driveline",
    "Windows and Glass": "glass",
    "Wiper and Washer Systems": "electrical-body",
}

# Ford service part number, e.g. E9TZ11450B / F2TZ11002ARM / F4TZ1522050B
PN_RE = re.compile(r'\b[A-Z]\d[A-Z][A-Z]\d{4,7}[A-Z]{1,3}\b')
PARTS_INFO = "Parts%20Information"


def decode(s):
    return html.unescape(s.replace("%20", " ").replace("%2C", ",").replace("%2F", "/"))


def slug(s):
    s = re.sub(r"[^a-z0-9]+", "-", decode(s).lower()).strip("-")
    return s[:70]


def page_text(path):
    t = open(path, encoding="utf-8", errors="ignore").read()
    t = re.sub(r"<[^>]+>", " ", t)
    return html.unescape(re.sub(r"\s+", " ", t))


def main():
    rows = []
    for dirpath, dirnames, filenames in os.walk(CATALOG):
        # a PART is a node that has a "Parts Information" child page
        if PARTS_INFO not in dirnames:
            continue
        rel = os.path.relpath(dirpath, CATALOG)
        segs = [decode(p) for p in rel.split(os.sep)]
        if len(segs) < 2:
            continue
        group = segs[0]
        name = segs[-1]
        subgroup = " / ".join(segs[1:-1]) if len(segs) > 2 else ""
        # OEM part numbers from the Parts Information table
        pi = os.path.join(dirpath, PARTS_INFO, "index.html")
        pns = []
        if os.path.exists(pi):
            raw = open(pi, encoding="utf-8", errors="ignore").read()
            tbl = re.search(r"parts-table.*?</table>", raw, re.S)
            pns = sorted(set(PN_RE.findall(tbl.group(0)))) if tbl else []
        rows.append({
            "id": slug("-".join(segs[-2:]) if len(segs) > 1 else name),
            "catalog_group": group,
            "subgroup": subgroup,
            "name": name,
            "part_numbers": pns[:6],
            "catalog_path": rel.replace(os.sep, "/"),
            "system": GROUP_SYSTEM.get(group, ""),
            "status": "not-started",     # not-started -> catalogued -> modeled
            "modeled": False,
        })

    # de-dup ids
    seen = collections.Counter()
    for r in rows:
        seen[r["id"]] += 1
        if seen[r["id"]] > 1:
            r["id"] = f'{r["id"]}-{seen[r["id"]]}'
    rows.sort(key=lambda r: (r["catalog_group"], r["subgroup"], r["name"]))

    with open(OUT, "w") as f:
        json.dump({
            "_comment": "Master BOM ledger extracted from the factory Parts catalog. "
                        "The build loop ticks parts off here. status: not-started|catalogued|modeled.",
            "source": "factory-service-manual / Parts and Labor",
            "total": len(rows),
            "parts": rows,
        }, f, indent=1)

    by_group = collections.Counter(r["catalog_group"] for r in rows)
    with_pn = sum(1 for r in rows if r["part_numbers"])
    print(f"BOM ledger written: {OUT}")
    print(f"Total catalogued parts: {len(rows)}  ({with_pn} have a Ford part number in-text)\n")
    print(f"{'catalog group':<48} parts")
    for g, n in sorted(by_group.items(), key=lambda x: -x[1]):
        print(f"  {g:<46} {n:>4}")


if __name__ == "__main__":
    main()
