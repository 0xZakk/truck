"""Preserve occurrence identity when repeated geometry is exported to STEP."""
from copy import deepcopy
import build123d as b
from assembly_math import transforms
from valvetrain_dispatch import occurrence_shape


def placed_occurrences(manifest, definitions):
    locations = transforms(manifest)
    result = []
    for occurrence in manifest['occurrences']:
        # Locations alone share the underlying OCCT shape. STEP's naming table
        # can then give every instance the last instance's name. Copy topology
        # before assigning an occurrence name, without changing its geometry.
        shape = deepcopy(occurrence_shape(
            occurrence, definitions[occurrence['definition']], 0))
        shape = shape.moved(locations[occurrence['id']])
        shape.label = occurrence['id']
        result.append(shape)
    return result


def verify_roundtrip(path, expected):
    restored = b.import_step(path)
    actual = list(restored.children)
    names = [shape.label for shape in actual]
    target = {shape.label: shape for shape in expected}
    if len(target) != len(expected) or len(set(names)) != len(names):
        raise AssertionError('Duplicate STEP occurrence labels')
    if set(names) != set(target):
        raise AssertionError('STEP occurrence labels differ from manifest')
    worst = 0.
    for shape in actual:
        original = target[shape.label]
        if len(shape.solids()) != 1 or not shape.is_valid:
            raise AssertionError(f'Invalid STEP occurrence: {shape.label}')
        left, right = shape.bounding_box(), original.bounding_box()
        delta = max(abs(getattr(getattr(left, end), axis) -
                        getattr(getattr(right, end), axis))
                    for end in ('min', 'max') for axis in ('X', 'Y', 'Z'))
        worst = max(worst, delta)
        if delta > .01:
            raise AssertionError(f'STEP occurrence placement/bounds changed: {shape.label}, {delta} mm')
    return {'unique_occurrence_labels': len(names),
            'max_roundtrip_bounds_delta_mm': worst,
            'bounds_tolerance_mm': .01,
            'scope': 'Occurrence identity, solid validity and world bounding boxes; not exact geometric equivalence or manufacturing fit'}
