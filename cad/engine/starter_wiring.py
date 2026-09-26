"""Provisional coil-end attachment study; routing is not a Ford production drawing."""
import build123d as b
import starter_motor as starter
import starter_solenoid as switch

REPLACED = {'starter-solenoid-winding-bobbin', 'starter-solenoid-fixed-pole'}
SOURCES = switch.SOURCES
GAPS = [
    'Circuit endpoints follow the Ford conventional PM starter diagram and applicable S/M/frame continuity description. Every route, lead diameter, sleeve and feedthrough is a packaging assumption.',
    'Aggregate winding envelopes represent insulated windings; they are not solid copper electrical nodes. Four modeled ends specify attachment interfaces, not winding turns or an electrical resistance simulation.',
    'Motor brush feed at M, brush pigtails, armature winding connections, battery cable and control harness remain open boundaries. Complete starter electrical continuity is not claimed.',
    'The shell attachment is a provisional ground interface. Joint processes, dielectric strength, current capacity, thermal behavior and production wire routing are unresolved.'
]
ROUTES = {
    'pull-s': [(-11.5, -2, -82), (-11.5, -2, -91), (-11.5, -10, -94), (0, -12, -109.8)],
    'pull-m': [(11.5, 2, -82), (11.5, 2, -91), (15, 7, -94), (15, 7, -112.8), (10, 0, -112.8)],
    'hold-s': [(-16, 2, -82), (-16, 2, -91), (-15, -8, -95), (0, -12, -109.8)],
    'hold-frame': [(16, -2, -82), (16, -2, -91), (20, -7, -94)]
}
CONTACTS = {
    'pull-s': ['starter-solenoid-pull-winding', 'starter-solenoid-s-terminal'],
    'pull-m': ['starter-solenoid-pull-winding', 'starter-solenoid-terminal-2'],
    'hold-s': ['starter-solenoid-hold-winding', 'starter-solenoid-s-terminal'],
    'hold-frame': ['starter-solenoid-hold-winding', 'starter-solenoid-shell']
}
FUNCTIONS = {
    'pull-winding': 'Aggregate insulated pull winding between S and M. Two provisional coil-end conductors attach it to those terminals; individual winding turns and resistance remain unresolved. Closing the B/M bridge shunts this winding in the declared circuit.',
    'hold-winding': 'Aggregate insulated hold winding between S and frame. Two provisional coil-end conductors attach it to S and the shell; magnetic force, winding turns and resistance remain unresolved.',
    'winding-bobbin': 'Provisional insulating former and divider with four bored lead passages. Separate sleeves clear the passage walls; dimensions and production lead routing are unverified.',
    'fixed-pole': 'Provisional stationary magnetic pole with four insulated lead feedthroughs around the contact pushrod guide. Magnetic flux and production pole construction are not solved.',
    's-terminal': 'Small S control terminal joined to both provisional coil-start conductors. Its external control harness remains absent; terminal clocking and joint construction are assumed.',
    'shell': 'Encloses the solenoid and provides the provisional hold-winding ground attachment. The attachment is a packaging study rather than a verified Ford joint construction.',
    'terminal-2': 'Heavy M terminal joins the provisional pull-winding end and the moving power-contact bridge at closure. The motor brush feed at this terminal remains absent.'
}


def route(points, radius):
    result = None
    for start, end in zip(points, points[1:]):
        direction = b.Vector(end) - b.Vector(start)
        segment = b.Solid.make_cylinder(radius, direction.length, b.Plane(origin=start, z_dir=direction))
        result = segment if result is None else result + segment
    for point in points:
        result += b.Pos(*point) * b.Sphere(radius)
    return result


def parts():
    baseline = starter.parts()
    baseline.update(switch.parts())
    result = {identifier: baseline[identifier] for identifier in REPLACED}
    for role, points in ROUTES.items():
        core = switch.FRAME * route(points, .4)
        clearance = switch.FRAME * route(points, .75)
        sleeve = switch.FRAME * (route(points, .65) - route(points, .45))
        for target in CONTACTS[role]:
            sleeve -= baseline[target]
        for identifier in REPLACED:
            result[identifier] -= clearance
        result['starter-solenoid-lead-' + role] = core
        result['starter-solenoid-lead-insulation-' + role] = sleeve
    shared = result['starter-solenoid-lead-pull-s'] + result['starter-solenoid-lead-hold-s']
    for role in ('pull-s', 'hold-s'):
        result['starter-solenoid-lead-insulation-' + role] -= shared
    return result


def circuit(closed=False):
    result = switch.circuit(closed)
    result['open_boundaries'] = [item for item in result['open_boundaries'] if item != 'coil end leads']
    result['modeled_coil_interfaces'] = dict(CONTACTS)
    result['physical_wiring_complete'] = False
    result['scope'] = 'Four provisional coil-end attachments; aggregate insulated windings, motor feed and armature wiring are not a solved electrical network.'
    return result


def api(base_api):
    define, add, group = base_api
    replacements = parts()

    def define_part(identifier, shape, name, function, system, color='#8498a3', sources=(), gaps=(), *args, **kwargs):
        if identifier in REPLACED:
            shape = replacements[identifier]
        if identifier.startswith('starter-solenoid-'):
            function = FUNCTIONS.get(identifier.removeprefix('starter-solenoid-'), function)
            gaps = [gap for gap in gaps if gap != switch.GAPS[2]]
            gaps = list(dict.fromkeys(gaps + GAPS))
            sources = list(dict.fromkeys(list(sources) + SOURCES))
        return define(identifier, shape, name, function, system, color, sources, gaps, *args, **kwargs)

    return define_part, add, group


def build(api):
    define, add, group = api
    for index, (identifier, shape) in enumerate(parts().items()):
        if identifier in REPLACED:
            continue
        insulated = 'insulation' in identifier
        function = 'Provisional insulating sleeve around a modeled coil-end route.' if insulated else 'Provisional coil-end conductor attachment; aggregate windings retain their declared internal circuit.'
        define(identifier, shape, identifier.replace('-', ' ').capitalize(), function, 'starting', '#44474b' if insulated else '#b87843', SOURCES, GAPS)
        add(identifier, identifier, 'starter-solenoid-assembly', explode=(0, -260 - index * 12, -100 - index * 12))
