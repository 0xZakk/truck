#!/usr/bin/env python3
"""Reproduce the evidence-limited zero-offset piston TDC comparison; no CAD writes."""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PREFIX = 'core-piston-reconciliation-20261003'
OUT = ROOT / 'reference/engine'

def digest(path):
    return hashlib.sha256((ROOT / path).read_bytes()).hexdigest()

inputs = ['inventory/engine/dimensions.json', 'inventory/engine/first-assembly.json',
          'cad/engine/first_assembly.py', 'cad/engine/full_engine.py',
          'reference/engine/ford-nominal-core-20261003-audit.json',
          'kb/sources/silvolite-efi-ford-300-piston-dimensions-40-40.md',
          'kb/sources/pump-deck-height-20261003-ford-nominal.md']
claims = {x['id']: x for x in json.loads((ROOT / inputs[0]).read_text())['claims']}
sources = [
    {'id': 'uem-2020', 'url': 'https://www.uempistons.com/themes/UEM/images/Silv-O-Lite%2012.20.20.pdf',
     'sha256': 'e4cae4c7b6aefacf612ac24318686da51e4a803d4ca3ca2a126ed4468baab114',
     'pdf_page': 40, 'printed_page': 38, 'actual_raster_review': True,
     'rows': ['1186', '1186H'], 'application': 'Ford L6-300, 4.9L; 1987–96; VIN Y; EFI truck',
     'compression_height_in': 1.776, 'pin_diameter_in': .9752, 'pin_offset': 'specified offset, amount and direction absent',
     'dish': 'D-shaped recess .310 inch deep', 'bore_in': 4.0,
     'limitation': 'Replacement piston reference; not proof of owner-installed or original-equipment piston.'},
    {'id': 'uem-supplement', 'url': 'https://uempistons.com/sites/default/files/Supplement_Catalog.pdf',
     'sha256': 'f38a45d485e87b164d70534fd763c854c7e4af545b6c5ccf3641b101e0fddef4',
     'pdf_page': 13, 'printed_page': 11, 'actual_raster_review': True,
     'row': '1186H', 'application': 'L6, 4.9L, 1987–1996, Ford Inline 6-Cylinder, bore 4.000 inch',
     'limitation': 'Confirms application only. No compression-height column. Page footer date 12/1/23.'},
    {'id': 'ford-nominal', 'url': 'https://www.trackey.ford.com/download/pdfs/EngineDimensions.pdf',
     'sha256': '0e81983110834897b86bbb06023f5f1df4381ab9e9174c35a18a425f4430049c',
     'pdf_page': 1, 'row': '300 I-6, 1965–96', 'compression_height_in': 1.757,
     'rod_length_mean_in': 6.210, 'stroke_in': 3.980, 'deck_height_in': 10.000,
     'limitation': 'Broad family nominal table; supplies no production tolerance or exact 1994 VIN Y piston identification.'}
]
local_catalog = ROOT / 'reference/engine/silvolite-2020.pdf'
if local_catalog.exists():
    assert hashlib.sha256(local_catalog.read_bytes()).hexdigest() == sources[0]['sha256']
ch, rod, stroke = [claims[k]['value'] for k in ['compression_height', 'rod_length', 'stroke']]
assert abs(ch - 1.776 * 25.4) < 1e-8
assert abs(stroke - 3.980 * 25.4) < 1e-8
rows = []
for label, r, h in [('Current replacement reference', rod, ch),
                     ('Replacement + Ford mean rod', 6.210*25.4, ch),
                     ('Ford nominal stack', 6.210*25.4, 1.757*25.4),
                     ('Ford piston + current rod', rod, 1.757*25.4)]:
    top = stroke/2 + r + h
    rows.append({'case': label, 'deck_mm': 254.0, 'stroke_mm': stroke, 'rod_mm': r,
                 'compression_height_mm': round(h, 8), 'tdc_crown_z_mm': round(top, 8),
                 'below_deck_mm': round(254-top, 8)})
report = {'scope': 'Research only; no CAD or installed geometry changes',
          'requested_baseline': '5c5a11d', 'observed_start_head': '0d318ea9a78bbc2b23041193c3090e7fd54343fd',
          'branch': 'engine/component-fit-followup-20261003',
          'input_sha256': {p: digest(p) for p in inputs}, 'sources': sources,
          'recommendation': 'Retain 45.1104 mm compression height as the exact-application UEM 1186/1186H replacement reference. Do not relabel it as factory or owner-measured. Ford family nominal 44.6278 mm remains a distinct comparison.',
          'formula': 'below_deck = 254 - stroke/2 - rod_length - compression_height',
          'assumptions': ['Crank axis z=0, positive z toward deck.', 'Idealized zero pin offset, aligned cylinder and crank axes.', 'Rigid nominal dimensions; no tolerances supplied or inferred.'],
          'cases': rows, 'compression_height_difference_mm': round(ch-1.757*25.4, 8),
          'current_rod_minus_ford_mean_mm': round(rod-6.210*25.4, 8),
          'limitations': ['Actual offset pin amount/direction unknown.', 'Rod identity and owner piston identity unverified.',
                         'Below-deck arithmetic is not piston-to-head clearance or measured deck clearance.',
                         'Dish volume, chamber volume, gasket compressed thickness, thermal expansion and compression ratio are not validated here.',
                         'No causal explanation for the broad Ford versus UEM dimension difference is asserted.']}
(OUT / f'{PREFIX}-report.json').write_text(json.dumps(report, indent=2)+'\n')
# Authored comparison graphic, not manufacturer pixels or a CAD fidelity render.
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(10, 4.7))
values = [r['below_deck_mm'] for r in rows]
ax.barh([r['case'] for r in rows], values, color=['#286f93','#60a3bc','#c18a46','#b3a07d'])
for i, v in enumerate(values):
    ax.text(v+.025, i, f'{v:.4f} mm', va='center')
ax.invert_yaxis(); ax.set_xlim(0,1.35)
ax.set_xlabel('Calculated crown below nominal deck at TDC (mm)')
ax.set_title('Piston height evidence: four distinct nominal combinations', loc='left', pad=15)
ax.spines[['top','right']].set_visible(False)
fig.text(.02,.02,'Idealized zero-offset stack; not measured clearance. Deck 254 mm; stroke 101.092 mm. No inferred tolerances.',fontsize=9)
fig.tight_layout(rect=[0,.05,1,1])
fig.savefig(OUT / f'{PREFIX}-comparison.png', dpi=160)
print(json.dumps({'report': str(OUT/f'{PREFIX}-report.json'), 'cases': rows}, indent=2))
