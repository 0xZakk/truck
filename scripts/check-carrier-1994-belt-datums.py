#!/usr/bin/env python3
"""Bounded analytic study of the accepted carrier; never edits installed CAD."""
import hashlib
import json
import math
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'cad/engine'))
import accessory_belt as belt
import accessory_carrier_1994 as carrier

nodes = [dict(n) for n in belt.PULLEYS]
nodes[1]['center'] = carrier.TENSIONER_POSITION[1:]

def measure(ns):
    outside = belt.solve(ns, cord_path=False)
    cord = belt.solve(ns)
    return {'outside_radius_loop_mm': outside['length'],
            'assumed_cord_loop_mm': cord['length'],
            'wrap_degrees': {a['pulley']: a['wrap_degrees'] for a in cord['arcs']},
            'signed_winding_degrees': sum(-a['side'] * a['wrap_degrees'] for a in cord['arcs'])}

base = measure(nodes)
assert abs(base['signed_winding_degrees'] + 360) < 1e-6
sensitivities = []
for i, n in enumerate(nodes):
    shifted = [dict(x) for x in nodes]
    shifted[i]['radius'] += 1
    sensitivities.append({'id': n['id'], 'radius_delta_mm': 1,
                          'loop_delta_mm': measure(shifted)['outside_radius_loop_mm'] - base['outside_radius_loop_mm']})

# Full unconstrained arm rotation is a deliberately optimistic diagnostic bound.
# It is NOT the spring's known operating range and does not check swept collisions.
samples = []
for step in range(3600):
    a = step * math.tau / 3600
    ns = [dict(n) for n in nodes]
    ns[1]['center'] = (167 + 75 * math.cos(a), 425 + 75 * math.sin(a))
    try:
        report = measure(ns)
    except AssertionError:
        continue
    if abs(report['signed_winding_degrees'] + 360) < 1e-6:
        samples.append({'angle_degrees': step / 10, 'center': ns[1]['center'], **report})
best = min(samples, key=lambda x: x['outside_radius_loop_mm'])
result = {
    'status': 'diagnostic-only; no belt or layout accepted',
    'carrier_source_sha256': hashlib.sha256(Path(carrier.__file__).read_bytes()).hexdigest(),
    'baseline': base, 'pulley_nodes': nodes,
    'radius_sensitivities': sensitivities,
    'unconstrained_75mm_arm_scan': {'sample_count': len(samples), 'best': best},
    'catalog_comparison_mm': belt.NOMINAL_EFFECTIVE_LENGTH,
    'catalog_comparison_is_not_a_matching_gauge_datum': True,
    'limits': [
        'All station coordinates, arm length and most pulley radii remain provisional.',
        'Dorman damper envelope OD is not an established belt effective diameter.',
        'TSB94-10-19 identifies E8TZ-8620-T / JK6-984-B for this truck class; it does not supply an effective length.',
        'The 2491mm comparison belongs to the previous replacement specification and is not silently assigned to every OE belt.',
        'Current PS and ALT centers share Z410; TENS Z350 lies below both. The reviewed schematic places TENS below PS but above ALT.',
        'Industrial CSG649 pump data cannot establish the automotive pump hub datum.',
        'No mesh collision, spring load, traction, effective gauge or production dimensional validation is implied.'
    ]
}
out = ROOT / 'inventory/engine/carrier-1994-belt-datum-study.json'
out.write_text(json.dumps(result, indent=2) + '\n')
print(json.dumps({'report': str(out), 'baseline': base,
                  'arm_scan_best_outside_loop_mm': best['outside_radius_loop_mm']}, indent=2))
