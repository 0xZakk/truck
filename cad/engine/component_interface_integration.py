"""Install explicitly provisional bracket and generic pump-seal teaching parts.

No source gap is resolved by this adapter. It preserves other geometry and IDs.
"""
from pathlib import Path
import importlib.util
import json
import hashlib
import water_pump_mechanical_seal_candidate as seal

ROOT = Path(__file__).resolve().parents[2]
spec = importlib.util.spec_from_file_location('throttle_bracket_candidate',
    Path(__file__).parent / 'pilot/throttle-bracket/candidate.py')
bracket = importlib.util.module_from_spec(spec)
spec.loader.exec_module(bracket)
STUD_ID = 'throttle-bracket-stud-estimated'
NEW_IDS = set(seal.LABELS) | {'accelerator-cable-bracket', STUD_ID}


def install(define, add, group, definitions, occurrences, assemblies):
    remove = NEW_IDS | {'water-pump-seal'}
    definitions[:] = [d for d in definitions if d['id'] not in remove]
    occurrences[:] = [o for o in occurrences if o['id'] not in remove]
    assemblies[:] = [a for a in assemblies if a['id'] != 'water-pump-mechanical-seal-assembly']
    seal.build((define, add, group))
    # The candidate only uses define/add; the legacy API reserves two helpers.
    bracket.build((define, add, group, None, None))
    define(STUD_ID, bracket.mounting_stud_shape(),
           'Throttle bracket mounting stud · estimated envelope',
           'Longer modeled stud envelope accommodates the bracket and full nut height. '
           'Actual Ford length, threads and anchorage are unverified.',
           'induction', '#879297', bracket.SOURCES, bracket.GAPS)
    changed = set()
    for occurrence in occurrences:
        key = occurrence['id']
        if key in ('throttle-stud-3', 'throttle-stud-4'):
            occurrence['definition'] = STUD_ID
            occurrence['position_cad_mm'][0] = bracket.STACK['stud_center_x_mm']
            occurrence['name'] = 'Bracket mounting stud · estimated envelope'
            occurrence['function'] = 'Supports the bracket/nut stack; actual threads and anchorage unverified.'
            changed.add(key)
        elif key in ('throttle-nut-3', 'throttle-nut-4'):
            occurrence['position_cad_mm'][0] = bracket.STACK['nut_center_x_mm']
            changed.add(key)
    assert len(changed) == 4, f'Missing expected throttle mounting occurrences: {changed}'


def sources():
    path = ROOT / 'reference/engine/water-pump-internal-construction-reviewed.json'
    result = {'water-pump-internal-construction': {
        'title': 'Manufacturer descriptions of generic water-pump seal construction',
        'url': 'https://www.gatestechzone.com/en/news/2022-05-water-pump-installation',
        'path': '/' + str(path.relative_to(ROOT)),
        'sha256': hashlib.sha256(path.read_bytes()).hexdigest()}}
    learning = json.loads((ROOT / 'inventory/engine/pilot/throttle-bracket/learning.json').read_text())
    result.update(learning.get('sources', {}))
    return result
