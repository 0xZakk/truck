"""Constrained starter engagement study with provisional slotted clevis and shift groove."""
import math
import build123d as b
import starter_motor as starter
import starter_solenoid as switch

UPPER_ARM = 30.0
LOWER_ARM = 32.0
PIVOT = (0, -32, -16)
MAX_ANGLE = math.degrees(math.asin(starter.TRAVEL / LOWER_ARM))
SLIDE = UPPER_ARM * (1 - math.cos(math.radians(MAX_ANGLE)))
REPLACED = {'starter-drive-lever', 'starter-solenoid-plunger', 'starter-solenoid-clevis-pin',
            'starter-drive-clutch', 'starter-drive-pinion', 'starter-drive-end-housing',
            'starter-housing-seal', 'starter-solenoid-front-seat'}
SOURCES = ['ford-pmgr-starter-exploded', 'ford-pmgr-conventional-circuit']
GAPS = [
    'Factory drawing supports a fork lever and drive assembly, not these arm lengths, groove or slotted-clevis dimensions. All linkage detail and travel are provisional engineering geometry.',
    'A 30mm upper arm and32mm lower arm connect11.25mm solenoid stroke to12mm pinion travel. A transverse slot in the plunger clevis accommodates the upper pin arc; this is not a verified production joint design.',
    'Spherical fork pads engage a3mm-wide annular clutch shift groove. Force, compliance, wear, friction, clutch internals, gear-tooth blocking and real starter sequencing are not simulated.',
    'Housing, front-seat and seal clearances are candidate interface modifications only, not production machining guidance. Default viewer remains static/retracted.'
]
FUNCTIONS = {
    'starter-drive-lever': 'Rigid fork lever pivots about the fixed fulcrum. Its upper pin slides in the translating plunger clevis, while integral spherical lower pads retain axial contact with the clutch shift groove. Dimensions and joint construction are provisional.',
    'starter-solenoid-plunger': 'Translating magnetic plunger with a provisional transverse-slot clevis. The slot accommodates the lever pin arc during the11.25mm prescribed stroke without forcing the plunger off axis.',
    'starter-solenoid-clevis-pin': 'Captured pivot pin follows the upper lever arc and slides transversely within the plunger clevis. End shoulders prevent axial escape in this provisional joint; load and wear are not calculated.',
    'starter-drive-clutch': 'Sliding clutch envelope with a provisional annular shift groove engaged by the fork pads. The sleeve retains its noncircular shaft coupling throughout12mm travel. Overrunning clutch internals and loaded operation remain unresolved.',
    'starter-drive-pinion': 'Ten-tooth pinion translates12mm with the clutch during the prescribed linkage stroke. Its sourced27.7mm outside diameter and provisional manual-flywheel mounting datums are unchanged.',
    'starter-drive-end-housing': 'Housing supports the drive and linkage; explicit candidate passage changes clear the full lever and clutch stroke while retaining a single connected casting and nose support. These are not production machining instructions.',
    'starter-housing-seal': 'Separate seal envelope with a provisional enlarged slot clearing the rotating lever stem. Elastomer deformation, environmental sealing and production dimensions remain unresolved.',
    'starter-solenoid-front-seat': 'Mounting seat with a provisional13mm-radius aperture clearing the lever stem and slotted clevis throughout the prescribed stroke. Its ears still attach to the drive housing.'
}


def pose(fraction):
    if not 0 <= fraction <= 1:
        raise ValueError('Engagement fraction must be within [0, 1]')
    travel = starter.TRAVEL * fraction
    angle = math.degrees(math.asin(travel / LOWER_ARM))
    return {'angle_deg': angle, 'drive_mm': travel, 'plunger_mm': UPPER_ARM / LOWER_ARM * travel,
            'upper_pin_slide_mm': UPPER_ARM * (1 - math.cos(math.radians(angle))),
            'fork_lateral_mm': LOWER_ARM * (1 - math.cos(math.radians(angle)))}


def lever_location(fraction):
    return b.Pos(*PIVOT) * b.Rot(pose(fraction)['angle_deg'], 0, 0) * b.Pos(0, 32, 16)


def pin_axis(radius, center, lower, upper):
    return b.Pos(*center) * b.Rot(0, 90, 0) * starter.cylinder(radius, lower, upper)


def lever():
    shape = b.Pos(0, -43.5, -16) * b.Box(5, 44, 5)
    shape += b.Pos(0, -23.25, -16) * b.Box(49, 2.5, 3)
    for side in (-1, 1):
        shape += b.Pos(side * 23, -13, -16) * b.Box(3, 28, 3)
        shape += pin_axis(1, (0, 0, -16), min(side * 18.5, side * 23), max(side * 18.5, side * 23))
        shape += b.Pos(side * 18.5, 0, -16) * b.Sphere(1.5)
    return shape - pin_axis(2.1, PIVOT, -8, 8) - pin_axis(1.55, (0, -62, -16), -8, 8)


def plunger():
    shape = switch.FRAME * starter.cylinder(8.5, -72, -22)
    for station in (-4.5, 4.5):
        shape += b.Pos(station, -62, -17) * b.Box(3, 10, 10)
    slot = pin_axis(1.55, (0, -62, -16), -8, 8)
    slot += pin_axis(1.55, (0, -62 + SLIDE, -16), -8, 8)
    slot += b.Pos(0, -62 + SLIDE / 2, -16) * b.Box(16, SLIDE, 3.1)
    return shape - slot


def clutch():
    shape = starter.cylinder(18, -18, -4) + starter.cylinder(21, -20, -12)
    shape -= starter.ring(22, 16.5, -17.5, -14.5)
    return shape - starter.drive_splines(-21, -3, .05)


def interfaces(baseline):
    housing = baseline['starter-drive-end-housing']
    housing -= b.Pos(0, -12.5, -11.25) * b.Box(51, 34, 19.5)
    housing -= starter.cylinder(25, -21, -1.5)
    housing -= starter.cylinder(21.2, -21, 1)
    seal = baseline['starter-housing-seal'] - b.Pos(0, -34, -16) * b.Box(6, 18, 16)
    seat = baseline['starter-solenoid-front-seat'] - switch.FRAME * starter.cylinder(13, -31, -26)
    return {'starter-drive-end-housing': housing, 'starter-housing-seal': seal,
            'starter-solenoid-front-seat': seat}


def parts(fraction=0, baseline=None):
    if baseline is None:
        baseline = starter.parts()
    coordinates = pose(fraction)
    rotated = lever_location(fraction)
    pin = pin_axis(1.5, (0, -62, -16), -6, 6)
    pin += pin_axis(2.2, (0, -62, -16), -7, -6) + pin_axis(2.2, (0, -62, -16), 6, 7)
    result = interfaces(baseline)
    result.update({'starter-drive-lever': rotated * lever(),
                   'starter-solenoid-plunger': b.Pos(0, 0, -coordinates['plunger_mm']) * plunger(),
                   'starter-solenoid-clevis-pin': rotated * pin,
                   'starter-drive-clutch': b.Pos(0, 0, coordinates['drive_mm']) * clutch(),
                   'starter-drive-pinion': b.Pos(0, 0, coordinates['drive_mm']) * starter.pinion()})
    return result


def api(base_api):
    define, add, group = base_api
    replacements = parts()

    def define_part(identifier, shape, name, function, system, color, sources, gaps, *args, **kwargs):
        gaps = [gap for gap in gaps if gap != starter.GAPS[-1]]
        if identifier in REPLACED:
            shape = replacements[identifier]
            function = FUNCTIONS[identifier]
            sources = list(dict.fromkeys(sources + SOURCES))
            gaps = gaps + GAPS
        return define(identifier, shape, name, function, system, color, sources, gaps, *args, **kwargs)

    return define_part, add, group
