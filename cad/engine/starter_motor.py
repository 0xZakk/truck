"""Manual-transmission PMGR starter study, with explicit unresolved mounting datums."""
import math
import build123d as b

PINION_TEETH = 10
PINION_OD = 27.7
RING_TEETH = 164
MODULE = 362 / 166
CENTER_DISTANCE = (RING_TEETH + PINION_TEETH) * MODULE / 2 + .8
AXIS_HEIGHT = -35.0
AXIS_SIDE = -math.sqrt(CENTER_DISTANCE ** 2 - AXIS_HEIGHT ** 2)
POSITION = (-388.475, AXIS_SIDE, AXIS_HEIGHT)
ROTATION = (0, -90, 0)
FRAME = b.Pos(*POSITION) * b.Rot(*ROTATION)
TRAVEL = 12.0
PINION_PHASE = ((RING_TEETH + PINION_TEETH) * math.degrees(math.atan2(-AXIS_SIDE, -AXIS_HEIGHT)) - 180) / PINION_TEETH % 36
SOURCES = ['ford-pmgr-starter-exploded', 'ford-manual-starter-parts', 'jn-410-14033-starter', 'tuffstuff-ford-starter-boundaries']
GAPS = [
    'Factory PMGR architecture/counts and manual F2TZ11002ARM identity are supported; J&N replacement cross-reference supplies ten pinion teeth,27.7mm OD and11mm mounting-hole diameter. Remaining dimensions are provisional.',
    'Starter center distance, clocking, axial station,12mm travel and housing envelope are fit-study assumptions. No bellhousing, index-plate bore or mounting bolt support is reconstructed or claimed.',
    'The9.525mm ring-face setback is a manual164-tooth Ford V8 comparison, not a verified4.9L mounting datum. Existing flywheel tooth module/pressure angle are also assumptions; sampled mesh is not production certification.',
    'Internal12/18/48 tooth reducer counts,5:1 ratio, winding/commutator subdivision and clearances are assumptions. Electromagnetics, current, insulation performance, overrunning-clutch internals and solenoid contact switching are not simulated.',
    'Six straight drive splines form a sliding noncircular coupling in this study. Production spline count, tooth form, helix and fit are not established by the exploded drawing.',
    'Default state is disengaged and stationary. The engagement study translates the clutch/pinion only; lever/plunger articulation and electrical connections need subsequent validation.'
]


def cylinder(radius, lower, upper):
    return b.Pos(0, 0, (lower + upper) / 2) * b.Cylinder(radius, upper - lower)


def ring(outer, inner, lower, upper):
    return cylinder(outer, lower, upper) - cylinder(inner, lower - 1, upper + 1)


def sector(outer, inner, lower, upper, start, sweep):
    points = [(radius * math.cos(math.radians(angle)), radius * math.sin(math.radians(angle)))
              for radius, angles in [(outer, [start + sweep * index / 32 for index in range(33)]),
                                     (inner, [start + sweep * index / 32 for index in reversed(range(33))])]
              for angle in angles]
    return b.Pos(0, 0, lower) * b.extrude(b.Polygon(*points, align=None), amount=upper - lower)


def gear(teeth, module, lower, upper, bore=0, outside=None, internal=False, rim=0, phase=0):
    pitch = teeth * module / 2
    base = pitch * math.cos(math.radians(20))
    root = pitch - module * (1 if internal else 1.25)
    tip = outside / 2 if outside else pitch + module * (1.25 if internal else 1)
    half = math.pi / (2 * teeth) + (.06 if internal else -.06) / pitch
    if outside and not internal:
        shift = (tip - pitch - module) / module
        root += shift * module
        half += 2 * shift * math.tan(math.radians(20)) / teeth

    def involute(radius):
        parameter = math.sqrt(max(0, (radius / base) ** 2 - 1))
        return parameter - math.atan(parameter)

    points = []
    for index in range(teeth):
        angle = index * math.tau / teeth
        points.append((root * math.cos(angle - math.pi / teeth), root * math.sin(angle - math.pi / teeth)))
        radii = [root + (tip - root) * step / 12 for step in range(13)]
        for radius in radii:
            edge = angle - half + involute(radius) - involute(pitch)
            points.append((radius * math.cos(edge), radius * math.sin(edge)))
        for radius in reversed(radii):
            edge = angle + half - involute(radius) + involute(pitch)
            points.append((radius * math.cos(edge), radius * math.sin(edge)))
    profile = b.Polygon(*points, align=None)
    if internal:
        profile = b.Circle(rim) - profile
    elif bore:
        profile -= b.Circle(bore)
    return b.Pos(0, 0, lower) * b.Rot(0, 0, phase) * b.extrude(profile, amount=upper - lower)


def spring(radius, wire, lower, length, turns):
    path = b.Helix(length / turns, length, radius)
    return b.Pos(0, 0, lower + wire) * b.sweep(b.Plane(origin=path @ 0, z_dir=path % 0) * b.Circle(wire), path=path)


def pinion(engaged=False, degrees=0):
    return b.Pos(0, 0, TRAVEL if engaged else 0) * b.Rot(0, 0, degrees + PINION_PHASE) * gear(PINION_TEETH, MODULE, -4, 6, 6.5, PINION_OD)


def drive_splines(lower, upper, clearance=0):
    shape = cylinder(5 + clearance, lower, upper)
    for index in range(6):
        shape += b.Rot(0, 0, index * 60) * b.Pos(5.6, 0, (lower + upper) / 2) * b.Box(1.6 + 2 * clearance, 1.5 + 2 * clearance, upper - lower)
    return shape


def parts(engaged=False):
    result = {}
    frame = ring(42, 38, -143, -52)
    rear = ring(42, 8, -151, -143)
    housing = ring(42, 29.5, -52, -10) + ring(52.4, 22, -10, 0)
    for station in (-66, 66):
        housing += b.Pos(station / 2, 0, -5) * b.Box(abs(station), 15, 10)
        housing += b.Pos(station, 0, -5) * b.Cylinder(12, 10)
        housing -= b.Pos(station, 0, 0) * cylinder(5.5, -12, 2)
    for station in (-12, 12):
        housing += b.Pos(station, -18, 17) * b.Box(7, 8, 36)
    housing += ring(23, 8, 33, 39)
    housing -= cylinder(22, -11, 1)
    housing -= b.Pos(0, -33, -15) * b.Box(10, 50, 20)
    housing -= b.Pos(0, -11, -15) * b.Box(44, 30, 20)
    for station in (-15, 15):
        housing += b.Pos(station, -45, 0) * cylinder(6, -38, -30)
        housing -= b.Pos(station, -45, 0) * cylinder(2.7, -40, -25)
        housing -= b.Pos(station, -45, 0) * cylinder(6.1, -30, -25)
    housing -= b.Pos(0, -65, 0) * cylinder(22.1, -110, -30)
    housing -= cylinder(18.2, -19, 9)
    pivot_bore = b.Pos(0, -32, -16) * b.Rot(0, 90, 0) * cylinder(2.1, -8, 8)
    housing -= pivot_bore
    for index, angle in enumerate((60, 240), 1):
        lateral = (35 * math.cos(math.radians(angle)), 35 * math.sin(math.radians(angle)))
        cutter = b.Pos(*lateral, 0) * cylinder(2.2, -154, -8)
        frame -= cutter
        rear -= cutter
        housing -= cutter
        result[f'starter-through-bolt-{index}'] = b.Pos(*lateral, 0) * (cylinder(2, -151, -12) + cylinder(4, -155, -151))
    result['starter-frame'] = frame
    for index, angle in enumerate((45, 225), 1):
        screw_frame = b.Rot(0, 0, angle) * b.Pos(30, 0, 0)
        rear -= screw_frame * cylinder(1.6, -149, -142)
        result[f'starter-brush-plate-screw-{index}'] = screw_frame * (cylinder(1.5, -148, -141) + cylinder(3, -141, -138))
    result['starter-brush-end-plate'] = rear
    result['starter-drive-end-housing'] = housing
    result['starter-rear-bushing'] = ring(8, 6.05, -152, -143)
    result['starter-nose-bushing'] = ring(8, 5.05, 33, 39)
    for index in range(6):
        angle = index * 60
        result[f'starter-magnet-{index + 1}'] = sector(36, 31, -120, -62, angle + 6, 48)
        result[f'starter-pole-shunt-{index + 1}'] = sector(37, 36, -120, -62, angle + 6, 48)
        result[f'starter-magnet-retainer-{index + 1}'] = sector(37.8, 30.8, -120, -62, angle + 54.5, 1.5)
    core = ring(27, 6, -120, -62)
    for index in range(12):
        rotation = b.Rot(0, 0, index * 30)
        core -= rotation * b.Pos(24.5, 0, -91) * b.Box(9, 5, 60)
        packet = b.Pos(24, 0, -91) * (b.Box(6, 4, 68) - b.Box(3, 6, 58))
        result[f'starter-armature-winding-{index + 1}'] = rotation * packet
    result['starter-armature-core'] = core
    result['starter-armature-shaft'] = cylinder(6, -150, -46) + gear(12, 1, -46, -34, 2.05)
    result['starter-commutator-insulator'] = ring(17, 6, -141, -125)
    for index in range(24):
        result[f'starter-commutator-segment-{index + 1}'] = sector(18, 17, -141, -125, index * 15 + .25, 14.5)
    brush_carrier = ring(37.5, 18.5, -143, -141)
    for angle in (60, 240):
        brush_carrier -= b.Pos(35 * math.cos(math.radians(angle)), 35 * math.sin(math.radians(angle)), 0) * cylinder(2.2, -145, -140)
    for angle in (45, 225):
        brush_carrier -= b.Rot(0, 0, angle) * b.Pos(30, 0, 0) * cylinder(1.6, -145, -140)
    result['starter-brush-carrier'] = brush_carrier
    for index in range(4):
        rotation = b.Rot(0, 0, index * 90)
        result[f'starter-brush-{index + 1}'] = rotation * b.Pos(24, 0, -134) * b.Box(12, 7, 12)
        result[f'starter-brush-spring-{index + 1}'] = rotation * b.Pos(30, 0, -134) * b.Rot(0, 90, 0) * spring(2.5, .35, 0, 6, 4)
        cage = b.Pos(25, 0, -134) * (b.Box(16, 10, 14) - b.Box(18, 7.2, 12.2))
        cage -= cylinder(18.55, -145, -120)
        for side in (-4.5, 4.5):
            cage += b.Pos(35, side, -134) * b.Box(4, 1, 3)
        cage += b.Pos(37.35, 0, -134) * b.Box(1.3, 10, 8)
        cage &= cylinder(38, -150, -120)
        result[f'starter-brush-holder-{index + 1}'] = rotation * cage
    result['starter-armature-thrust-ball'] = b.Pos(0, 0, -44) * b.Sphere(2)
    result['starter-gear-retainer'] = ring(28, 6.1, -49, -47)
    result['starter-stationary-gear'] = gear(48, 1, -46, -34, internal=True, rim=29, phase=3.75)
    carrier = ring(24, 5, -33, -30)
    for index in range(3):
        angle = index * 120
        frame = b.Rot(0, 0, angle) * b.Pos(15, 0, 0)
        result[f'starter-planet-gear-{index + 1}'] = frame * gear(18, 1, -46, -34, 3.05, phase=10)
        carrier += frame * cylinder(3, -46, -32)
    result['starter-output-shaft-assembly'] = carrier + cylinder(5, -33, 39) + cylinder(2, -42, -32) + drive_splines(-25, 10)
    result['starter-armature-thrust-washer'] = ring(10, 5.05, -29, -28)
    result['starter-shaft-e-ring'] = ring(8, 5.05, -27, -26) - b.Pos(8, 0, -26.5) * b.Box(12, 5, 3)
    travel = TRAVEL if engaged else 0
    result['starter-drive-clutch'] = b.Pos(0, 0, travel) * (cylinder(18, -18, -4) - drive_splines(-19, -3, .05))
    result['starter-drive-pinion'] = pinion(engaged)
    result['starter-stop-ring'] = ring(6, 5.05, 24, 25)
    result['starter-stop-ring-retainer'] = ring(8, 5.05, 25, 27)
    lever = b.Pos(0, -43.5, -16) * b.Box(5, 43, 5)
    lever += b.Pos(0, -22, -16) * b.Box(43, 5, 5)
    for station in (-20, 20):
        lever += b.Pos(station, -10, -12) * b.Box(3, 28, 12)
    clevis_bore = b.Pos(0, -62, -16) * b.Rot(0, 90, 0) * cylinder(1.55, -7, 7)
    result['starter-drive-lever'] = lever - pivot_bore - clevis_bore
    result['starter-solenoid-clevis-pin'] = b.Pos(0, -62, -16) * b.Rot(0, 90, 0) * cylinder(1.5, -6, 6)
    result['starter-lever-pivot'] = b.Pos(0, -32, -16) * b.Rot(0, 90, 0) * cylinder(2, -7, 7)
    result['starter-housing-seal'] = b.Pos(0, -34, -15) * (b.Box(10, 16, 20) - b.Box(6, 18, 8)) - pivot_bore
    solenoid_frame = b.Pos(0, -65, 0)
    result['starter-solenoid-shell'] = solenoid_frame * ring(22, 20, -108, -30)
    result['starter-solenoid-coil-envelope'] = solenoid_frame * ring(19.5, 9, -98, -34)
    plunger = solenoid_frame * cylinder(8.5, -72, -22)
    for side in (-4.5, 4.5):
        plunger += b.Pos(side, -65, -17) * b.Box(3, 10, 10)
    result['starter-solenoid-plunger'] = plunger - clevis_bore
    cap = cylinder(20, -113, -108)
    front_seat = ring(22, 8.7, -30, -27)
    result['starter-solenoid-return-spring'] = solenoid_frame * spring(5, .5, -108, 35, 8)
    for index, station in enumerate((-10, 10), 1):
        cap -= b.Pos(station, 0, 0) * cylinder(3.1, -114, -107)
        result[f'starter-solenoid-terminal-{index}'] = solenoid_frame * b.Pos(station, 0, 0) * cylinder(3, -123, -111)
        result[f'starter-solenoid-terminal-nut-{index}'] = solenoid_frame * b.Pos(station, 0, -120) * b.extrude(b.RegularPolygon(5.5, 6) - b.Circle(3), amount=3)
    for index, station in enumerate((-15, 15), 1):
        front_seat += b.Pos(station, 20, 0) * cylinder(6, -30, -26)
        front_seat -= b.Pos(station, 20, 0) * cylinder(2.7, -32, -24)
        result[f'starter-solenoid-screw-{index}'] = b.Pos(station, -45, 0) * (cylinder(2.5, -38, -26) + cylinder(4.5, -26, -23))
    result['starter-solenoid-end-cap'] = solenoid_frame * cap
    result['starter-solenoid-front-seat'] = solenoid_frame * front_seat
    return result


def build(api):
    define, add, group = api
    group('starter-assembly', 'Manual PMGR starter · provisional mounting study', 'engine', position=POSITION, rotation=ROTATION)
    for subgroup, name in [('motor', 'Permanent magnet motor'), ('reducer', 'Planetary reduction'),
                           ('drive', 'Retracted drive and lever'), ('solenoid', 'Solenoid and terminals')]:
        group('starter-' + subgroup + '-assembly', name, 'starter-assembly')
    for identifier, shape in parts().items():
        subgroup = 'solenoid' if 'solenoid' in identifier else 'reducer' if any(word in identifier for word in ('gear', 'carrier', 'output', 'thrust', 'e-ring')) and 'brush' not in identifier else 'drive' if any(word in identifier for word in ('drive', 'nose', 'stop', 'lever', 'housing-seal')) else 'motor'
        color = '#ae7441' if 'winding' in identifier or 'commutator-segment' in identifier else '#3d4146' if any(word in identifier for word in ('magnet', 'brush-', 'insulator', 'seal', 'end-cap')) else '#98a3ac'
        function = 'Separate component in the factory PMGR architecture. Dimensions and installed datums remain a provisional fit study; electrical and loaded mechanical performance are not simulated.'
        if identifier == 'starter-drive-clutch':
            function = 'Overrunning drive clutch envelope, separate from the ten-tooth pinion. Internal rollers, ramps, springs and locking behavior are unresolved, not represented by arbitrary valve-like parts.'
        define(identifier, shape, identifier.replace('-', ' ').capitalize(), function, 'starting', color, SOURCES, GAPS)
        add(identifier, identifier, 'starter-' + subgroup + '-assembly', explode=(0, -100, 0))
