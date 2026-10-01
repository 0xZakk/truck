"""Validate isolated EVTM lessons; never modify canonical or private-stage inputs."""
import copy
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LEARNING = 'inventory/engine/engine-control-electrical-learning-candidate.json'
SOURCES = 'inventory/engine/engine-control-electrical-learning-sources.json'
MAP = 'reference/engine/engine-control-electrical-map.json'
REVIEW = 'inventory/engine/engine-control-electrical-map-root-review.json'
MANIFESTS = ['inventory/engine/full-assembly.json', 'inventory/engine/corrected-engine-stage-v3.json']
REPORT = 'inventory/engine/engine-control-electrical-learning-validation.json'
BIND = {**{f'fuel-injector-{n}': f'injector-{n}' for n in range(1, 7)},
        'iac-valve-body': 'iac', 'egr-vacuum-regulator': 'evr',
        'egr-position-sensor': 'evp', 'throttle-sensor': 'tps',
        'engine-coolant-temperature-assembly': 'ect'}

def load(path):
    return json.loads((ROOT / path).read_text())

def sha(path):
    return hashlib.sha256((ROOT / path).read_bytes()).hexdigest()

def validate(lessons, sources, source_map, manifests):
    assert set(lessons) == set(BIND), 'Wrong learning target coverage'
    expected = {row['id']: row for row in source_map['components']}
    links = 0
    for manifest in manifests:
        ids = {row['id'] for key in ('assemblies', 'occurrences') for row in manifest[key]}
        for target, lesson in lessons.items():
            assert target in ids, f'Absent target {target}'
            assert lesson['electrical_contract'] == expected[BIND[target]], f'Electrical contract mismatch {target}'
            for field in ('summary', 'limits', 'steps', 'sources', 'troubleshooting'):
                assert lesson[field], f'Missing content {target}/{field}'
            assert 'cavity' in lesson['limits'] and 'calibration' in lesson['limits']
            for item in lesson['steps'] + lesson['troubleshooting']:
                assert item['title'] and item['text']
                if 'part' in item:
                    assert item['part'] in ids, f'Broken part link {item["part"]}'
                    links += 1
            for key in lesson['sources']:
                assert key in sources, f'Missing source {key}'
    # Independent critical electrical invariants, beyond object equality to the map.
    for n in range(1, 7):
        lesson = lessons[f'fuel-injector-{n}']
        driver = next(x for x in lesson['electrical_contract']['contacts'] if x['role'] == 'group driver')
        circuit, pin, group = ('555', 58, '1, 3 and 5') if n % 2 else ('556', 59, '2, 4 and 6')
        assert (driver['circuit'], driver['pcm_c185_cavity']) == (circuit, pin), 'Wrong injector group'
        prose = ' '.join(x['text'] for x in lesson['steps'])
        assert f'C185/{pin}' in prose and group in prose, 'Wrong narrative injector group'
        assert 'not injection timing' in prose
    for target in ('throttle-sensor', 'egr-position-sensor', 'engine-coolant-temperature-assembly'):
        ret = next(x for x in lessons[target]['electrical_contract']['contacts'] if x['role'] == 'sensor signal return')
        assert (ret['circuit'], ret['pcm_c185_cavity']) == ('359', 46), 'Wrong sensor ground'
    o2 = expected['heated-oxygen-sensor']['contacts']
    assert next(x for x in o2 if x['role'] == 'oxygen sensor ground')['pcm_c185_cavity'] == 49
    assert next(x for x in o2 if x['role'] == 'heater chassis ground')['path_from_component'][-1] == 'G101'
    prose = ' '.join(x['text'] for x in lessons['engine-coolant-temperature-assembly']['steps'])
    for phrase in ('89 O oxygen ground to PCM49', '57 BK heater/chassis ground viaG101', 'None is a replacement for359'):
        assert phrase in prose, 'Wrong oxygen/heater ground explanation'
    for source in sources.values():
        assert source['sha256'] == source_map['source']['sha256']
        assert sha(source['path']) == source['sha256'], 'Source PDF changed'
        assert source['url'] == '/' + source['path'] + '#page=' + str(source['pdf_page_1_based'])
        assert any(p['pdf_page_1_based'] == source['pdf_page_1_based'] and p['printed'] == source['printed_page'] for p in source_map['source']['pages']), 'Wrong source page'
    return links

def main():
    lessons, sources, source_map = load(LEARNING), load(SOURCES), load(MAP)
    review = load(REVIEW)
    assert review['inputs'][MAP] == sha(MAP), 'Stale independent source review'
    manifests = [load(p) for p in MANIFESTS]
    links = validate(lessons, sources, source_map, manifests)
    controls = {}
    def rejected(name, mutate):
        bad = copy.deepcopy(lessons)
        mutate(bad)
        try:
            validate(bad, sources, source_map, manifests)
        except AssertionError as exc:
            controls[name] = dict(rejected=True, reason=str(exc))
        else:
            raise AssertionError(f'Insensitive negative control: {name}')
    rejected('odd_injector_sent_to_even_driver', lambda d: d['fuel-injector-1']['electrical_contract']['contacts'][1].update(circuit='556', pcm_c185_cavity=59))
    rejected('sensor_return_replaced_by_chassis_ground', lambda d: d['throttle-sensor']['electrical_contract']['contacts'][1].update(circuit='57', pcm_c185_cavity=None))
    rejected('oxygen_ground_narrative_replaced_by_sensor_return', lambda d: d['engine-coolant-temperature-assembly']['steps'][2].update(text=d['engine-coolant-temperature-assembly']['steps'][2]['text'].replace('89 O oxygen ground to PCM49', '359 GY/R sensor return to PCM46')))
    rejected('phantom_map_part_link', lambda d: d['throttle-sensor']['steps'][1].update(part='map-sensor-nonexistent'))
    rejected('wrong_narrative_injector_group', lambda d: d['fuel-injector-1']['steps'][1].update(text=d['fuel-injector-1']['steps'][1]['text'].replace('C185/58', 'C185/59')))
    files = [LEARNING, SOURCES, MAP, REVIEW, *MANIFESTS, 'scripts/check-engine-control-electrical-learning.py']
    report = dict(status='PASS isolated learning content and reference guards',lesson_count=len(lessons),part_links_checked_across_two_manifests=links,negative_controls=controls,bindings={p: sha(p) for p in files},missing_physical_targets=['MAP C1011', 'IAT C164', 'HO2S C1025'],limits=['Candidate not loaded; no replacement of existing lessons yet', 'Private purchased-page URLs require authorized local PDF; public availability NOT RUN', 'No browser, live electrical diagnostic, installed harness or calibration validation'])
    (ROOT / REPORT).write_text(json.dumps(report, indent=2) + '\n')
    print(report['status'], len(lessons), 'lessons;', len(controls), 'controls rejected')

if __name__ == '__main__':
    main()
