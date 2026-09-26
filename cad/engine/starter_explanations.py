"""Role-specific learning metadata and exploded placement, without geometry edits."""
import math
import re

FUNCTIONS = {
    'frame': 'Holds the six permanent-magnet pole pieces around the armature and provides the motor frame. It is distinct from the individual magnets, shunts and retainers.',
    'through-bolt': 'Clamps the rear plate, motor frame and drive-end housing together along the starter axis. Threads, clamp load and production dimensions remain provisional.',
    'brush-plate-screw': 'Fastens the brush-carrier region to the rear end plate. Its head, shank and matching holes show the attachment; thread geometry is not modeled.',
    'brush-end-plate': 'Closes the rear of the motor and locates the rear armature bushing and brush hardware. The separate bushing supports the rotating shaft.',
    'drive-end-housing': 'Locates the reduction and drive components, supports the nose bushing, and provides the two mounting ears. The bellhousing and index plate that would locate those ears are absent.',
    'rear-bushing': 'Supports the rear armature journal while allowing rotation. Clearance is geometric; bearing wear, lubrication and radial load are not simulated.',
    'nose-bushing': 'Supports the forward end of the output shaft in the drive nose. This is separate from the clutch and the pinion that slide on the shaft.',
    'magnet': 'One of six permanent-magnet pole pieces identified in the Ford exploded view. Their field interacts with current in the armature; magnetic polarity and field strength are not simulated.',
    'pole-shunt': 'One of six separate pole shunts identified by Ford. It belongs to the magnetic-field structure, not the brush circuit or the mechanical magnet-retaining clips. Its detailed magnetic effect is not quantified here.',
    'magnet-retainer': 'One of six separate retainers that locate the magnetic pole pieces in the frame. Retaining preload and production clip construction remain unverified.',
    'armature-core': 'Provides the iron armature body and slots for the winding packets. The single solid represents a lamination stack; individual laminations and eddy-current behavior are not modeled.',
    'armature-winding': 'Aggregate copper winding packet carried by the armature. Current in the rotating winding interacts with the permanent field to produce torque. Twelve packets are a modeling subdivision, not a recovered winding diagram.',
    'armature-shaft': 'Carries the rotating armature and its integral sun gear. The sun drives the three planet gears; the rear bushing and forward thrust-ball interface support the shaft.',
    'commutator-insulator': 'Separates the commutator segments from the armature shaft in this geometric study. Electrical insulation thickness, material and voltage capability are not established.',
    'commutator-segment': 'Conductive commutator segment passing beneath the stationary brushes to switch armature current as the rotor turns. Twenty-four displayed segments and their winding connections are not factory-verified.',
    'brush-carrier': 'Locates the four brush holders at the commutator end of the motor. It keeps their radial paths organized; the depicted insulating construction is provisional.',
    'brush': 'Conductive brush that transfers current between stationary wiring and the rotating commutator. A separate spring maintains contact; lead wiring and wear are not simulated.',
    'brush-spring': 'Loads its brush toward the commutator as the brush wears. The coil and its holder reaction seat are distinct, but spring force and installed preload are uncalibrated.',
    'brush-holder': 'Guides one brush radially and supports its spring reaction seat. The open guide allows the brush to advance toward the commutator; manufacturing details remain provisional.',
    'armature-thrust-ball': 'Separate thrust ball identified by Ford between the armature and output-shaft region. It provides a localized axial interface; Hertzian stress and lubrication are not calculated.',
    'gear-retainer': 'Retains the planetary components axially on the armature side. Its profile and clearances are provisional rather than a traced Ford retainer drawing.',
    'stationary-gear': 'Fixed internal ring gear reacting the planet forces into the housing. With the assumed 12-tooth sun and 48-tooth ring fixed, the output carrier rotates at one fifth of sun speed.',
    'planet-gear': 'One of three planet gears meshing with the sun and fixed internal ring. Each spins on a carrier pin while its center orbits the sun. The displayed 18-tooth count is provisional.',
    'output-shaft-assembly': 'Integral carrier, three planet pins and output shaft collect the reduced-speed drive. Six provisional straight splines form a sliding noncircular coupling to the drive-clutch sleeve.',
    'armature-thrust-washer': 'Provides a separate axial spacing and thrust surface in the drive-shaft stack. The washer is not a substitute for the overrunning clutch.',
    'shaft-e-ring': 'Separate open retaining ring locating the shaft stack axially. Groove geometry, snap fit and retention capacity remain unverified.',
    'drive-clutch': 'Overrunning drive-clutch envelope coupled to the sliding shaft splines. In a real starter it transmits starting torque while allowing the engine to overrun the motor; internal rollers, ramps and springs are unresolved here.',
    'drive-pinion': 'Ten-tooth, 27.7 mm outside-diameter pinion constrained by the J&N manual-starter cross-reference. It is retracted in the displayed resting state; the separate engagement study meshes it with the 164-tooth flywheel.',
    'stop-ring': 'Locates the forward travel-stop region on the output shaft. Exact groove dimensions and engagement travel require an applicable production reference.',
    'stop-ring-retainer': 'Retains the drive stop ring as a separate component. The stop stack is distinct from the pinion, clutch and nose bushing.',
    'drive-lever': 'Forked lever couples solenoid-plunger motion to the sliding drive assembly. The resting linkage is decomposed; the current engagement test does not validate its complete articulation.',
    'lever-pivot': 'Provides the fulcrum for the drive lever within the drive-end housing. Pivot fit and bearing pressure are provisional.',
    'housing-seal': 'Separate housing-seal envelope around the lever region identified in the exploded view. Its shape does not establish a production elastomer or environmental sealing rating.',
    'solenoid-shell': 'Encloses the solenoid winding and moving plunger. The solenoid is a drive actuator and high-current switching assembly, not the separate vehicle-mounted starter relay.',
    'solenoid-coil-envelope': 'Aggregate electromagnetic winding envelope around the plunger. Energizing the real winding creates the pull that actuates the lever; pull-in/hold-in circuits and individual turns are not yet reconstructed.',
    'solenoid-plunger': 'Moving magnetic plunger with a provisional clevis connection to the drive lever. The modeled resting geometry is connected; magnetic force and full-stroke articulation remain unverified.',
    'solenoid-clevis-pin': 'Connects the provisional plunger clevis and lever while allowing pivoting. It is a fit-study decomposition rather than a separately identified Ford service part.',
    'solenoid-return-spring': 'Returns the plunger toward the resting position when electromagnetic force is removed. The spring geometry has no calibrated force or release-time claim.',
    'solenoid-terminal': 'One of the two large solenoid-terminal envelopes for the high-current path. Battery/motor assignments, internal contact bridge and external cables are not yet reconstructed.',
    'solenoid-terminal-nut': 'Retains a cable lug on a large solenoid terminal. No cable lug is installed here, and the smooth bore is not a modeled screw thread.',
    'solenoid-screw': 'Fastens the solenoid front mounting ears to the drive-end housing. Matching holes provide a visible attachment without a calibrated clamp-load claim.',
    'solenoid-end-cap': 'Insulating end-cap envelope surrounding the terminal penetrations. It is separate from the metal shell; contact switching and dielectric performance are unresolved.',
    'solenoid-front-seat': 'Locates the plunger opening and supports the solenoid mounting ears. Its shoulder and screws close the mechanical mounting path to the drive housing.'
}

NUMBERED = {'through-bolt', 'brush-plate-screw', 'magnet', 'pole-shunt', 'magnet-retainer',
            'armature-winding', 'commutator-segment', 'brush', 'brush-spring', 'brush-holder',
            'planet-gear', 'solenoid-terminal', 'solenoid-terminal-nut', 'solenoid-screw'}
NONMETALLIC = {'magnet', 'brush', 'brush-holder', 'brush-carrier', 'commutator-insulator', 'housing-seal', 'solenoid-end-cap'}


def role(identifier):
    key = identifier.removeprefix('starter-')
    numbered = re.sub(r'-\d+$', '', key)
    if numbered in NUMBERED:
        key = numbered
    if key not in FUNCTIONS:
        raise ValueError('Missing starter explanation: ' + identifier)
    return key


def color_for(identifier):
    key = role(identifier)
    if key in ('armature-winding', 'commutator-segment', 'solenoid-coil-envelope', 'solenoid-terminal'):
        return '#ae7441'
    if key in NONMETALLIC:
        return '#343d42' if key != 'commutator-insulator' else '#9b7555'
    if key in ('rear-bushing', 'nose-bushing'):
        return '#b3a16e'
    return '#98a3ac'


def is_nonmetallic(identifier):
    return role(identifier) in NONMETALLIC


def explosion_for(identifier, center):
    key = role(identifier)

    def radial(distance, axial=0):
        radius = math.hypot(center.X, center.Y)
        return (distance * center.X / radius, distance * center.Y / radius, axial) if radius else (0, distance, axial)

    if key.startswith('solenoid'):
        axial = {'solenoid-shell': -70, 'solenoid-coil-envelope': -25, 'solenoid-plunger': 90,
                 'solenoid-front-seat': 140, 'solenoid-end-cap': -180, 'solenoid-return-spring': 20,
                 'solenoid-terminal': -220, 'solenoid-terminal-nut': -250, 'solenoid-clevis-pin': 110,
                 'solenoid-screw': 170}[key]
        return (center.X * 2, -180, axial)
    radial_roles = {'magnet': (100, 0), 'pole-shunt': (135, 0), 'magnet-retainer': (165, 0),
                    'armature-winding': (65, -90), 'commutator-segment': (50, -180),
                    'brush': (80, -220), 'brush-spring': (120, -220), 'brush-holder': (150, -220),
                    'planet-gear': (65, 90)}
    if key in radial_roles:
        return radial(*radial_roles[key])
    axial = {'frame': -250, 'through-bolt': -380, 'brush-plate-screw': -340, 'brush-end-plate': -310,
             'drive-end-housing': 270, 'rear-bushing': -280, 'nose-bushing': 300,
             'armature-core': -90, 'armature-shaft': -40, 'commutator-insulator': -180,
             'brush-carrier': -220, 'armature-thrust-ball': 20, 'gear-retainer': 60,
             'stationary-gear': 90, 'output-shaft-assembly': 140, 'armature-thrust-washer': 155,
             'shaft-e-ring': 170, 'drive-clutch': 180, 'drive-pinion': 240,
             'stop-ring': 280, 'stop-ring-retainer': 295, 'drive-lever': 210,
             'lever-pivot': 230, 'housing-seal': 230}[key]
    return (0, -90 if key in ('drive-lever', 'lever-pivot', 'housing-seal') else 0, axial)


def api(base):
    define, add, group = base
    centers = {}

    def define_part(identifier, shape, name, function, system, color='#8498a3', sources=(), gaps=(), claims=()):
        centers[identifier] = shape.center()
        define(identifier, shape, name, FUNCTIONS[role(identifier)], system, color_for(identifier), sources, gaps, claims)

    def add_part(identifier, definition, parent, pos=(0, 0, 0), explode=(0, 0, 0), rotation=(0, 0, 0), name=None):
        add(identifier, definition, parent, pos, explosion_for(definition, centers[definition]), rotation, name=name)

    return define_part, add_part, group


def solenoid_api(base):
    define, add, group = base
    offsets = {
        'pull-winding': (0, -320, -120),
        'hold-winding': (0, -320, -220),
        'winding-bobbin': (0, -320, -330),
        'fixed-pole': (0, -320, -390),
        'contact-rod': (80, -350, -430),
        'bridge-insulator': (150, -350, -480),
        'contact-bridge': (0, -350, -520),
        's-terminal': (80, -350, -590),
        's-terminal-insulator': (150, -350, -590),
    }

    def add_part(identifier, definition, parent, pos=(0, 0, 0), explode=(0, 0, 0), rotation=(0, 0, 0), name=None):
        offset = offsets[definition.removeprefix('starter-solenoid-')]
        add(identifier, definition, parent, pos, offset, rotation, name=name)

    return define, add_part, group


def wiring_api(base):
    define, add, group = base
    roles = ['pull-s', 'pull-m', 'hold-s', 'hold-frame']

    def add_part(identifier, definition, parent, pos=(0, 0, 0), explode=(0, 0, 0), rotation=(0, 0, 0), name=None):
        insulated = 'lead-insulation-' in definition
        prefix = 'starter-solenoid-lead-insulation-' if insulated else 'starter-solenoid-lead-'
        index = roles.index(definition.removeprefix(prefix)) * 2 + int(insulated)
        add(identifier, definition, parent, pos, (320, -320, -100 - index * 65), rotation, name=name)

    return define, add_part, group
