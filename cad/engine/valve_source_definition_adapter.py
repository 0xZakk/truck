"""Persistent source-sized definition adapters for fresh or refreshed geometry."""
import valve_source_layout as v
from valve_layout_integration import station_pairs

IDS = {'cylinder-head', 'rocker-arm', 'pushrod', 'lifter-body',
       'lifter-pushrod-cup', 'valve-cover', 'valve-seal',
       'intake-valve', 'exhaust-valve', 'intake-spring', 'exhaust-spring'}


def replacement(identifier, shape, manifest):
    if identifier == 'cylinder-head':
        for pair in station_pairs(manifest):
            shape = v.head_adapter(shape, pair['stations'])
        return shape
    if identifier in ('intake-valve', 'exhaust-valve'):
        kind = identifier.split('-')[0]
        length = shape.bounding_box().size.Z
        if abs(length - v.LENGTHS[kind]) < .0001:
            return shape
        if abs(length - 109) > .0001:
            raise ValueError(f'Unexpected input valve length: {identifier}: {length}')
        return v.valve(shape, kind)
    if identifier == 'lifter-body':
        return v.lifter_body(shape)
    if identifier in ('intake-spring', 'exhaust-spring'):
        return v.spring(identifier.split('-')[0])
    generators = {'rocker-arm': v.rocker, 'pushrod': v.pushrod,
                  'lifter-pushrod-cup': v.lifter_cup, 'valve-cover': v.cover,
                  'valve-seal': v.seal}
    return generators[identifier]() if identifier in generators else shape
