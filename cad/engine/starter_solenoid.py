"""Provisional PMGR magnetic-switch decomposition, not a production solenoid drawing."""
import build123d as b
import starter_motor as starter

FRAME = b.Pos(0, -65, 0)
STROKE = 11.25
SOURCES = ['ford-pmgr-starter-exploded', 'ford-starter-solenoid-test', 'ford-pmgr-conventional-circuit']
GAPS = [
    'Ford test identifies S, M and frame continuity. Ford patent Figure 1 supports conventional pull/hold and normally-open power-contact topology, not this 1994 part geometry or production adoption of the patent invention.',
    'All added dimensions, radial winding allocation, contact position and 11.25mm stroke are provisional packaging assumptions. Coils are aggregate winding envelopes, not individual turns.',
    'Circuit graph is an explicit logical connection specification. Coil lead wires, motor brush connections, vehicle battery cable and control harness remain unmodeled open boundaries; no assembled electrical continuity or current rating is claimed.',
    'This isolated magnetic-switch stroke does not animate or validate the existing lever/clevis, return linkage, fork or pinion engagement. Default installed pose remains open and retracted.',
    'Contact pressure, bounce, arcing, insulation, spring force, magnetic force and loaded starter performance are not simulated.'
]
REPLACED = {'starter-solenoid-coil-envelope', 'starter-solenoid-end-cap',
            'starter-solenoid-return-spring', 'starter-solenoid-terminal-1',
            'starter-solenoid-terminal-2'}
FUNCTIONS = {
    'pull-winding': 'Aggregate pull-in winding between S and M in the declared circuit. It assists initial plunger attraction and is shunted when M reaches battery potential; physical lead wires remain an open boundary.',
    'hold-winding': 'Separate aggregate holding winding between S and frame in the declared circuit. It maintains attraction after contact closure; no force or resistance is calculated.',
    'winding-bobbin': 'Provisional insulating former and divider separating the two winding envelopes from the plunger and shell.',
    'fixed-pole': 'Provisional stationary magnetic pole around the insulated contact pushrod guide. It bounds the spring chamber; magnetic flux is not solved.',
    'contact-rod': 'Provisional rod translating with the plunger to carry the insulated moving contact. Its connection to the existing plunger is a geometric study.',
    'bridge-insulator': 'Insulating sleeve and axial shoulders isolate the moving power-contact bridge from its steel rod.',
    'contact-bridge': 'Normally open copper bridge connecting the B and M contact faces at the candidate stroke endpoint. This is a physical contact study, not a current-carrying certification.',
    's-terminal': 'Distinct small S control terminal identified by the factory continuity test. Terminal shape and clocking are provisional; the external control harness and internal coil leads are absent.',
    's-terminal-insulator': 'Insulating sleeve through the contact-cap wall for the distinct S terminal. Material and dielectric performance are unresolved.'
}


def circuit(closed=False):
    edges = [('S', 'M', 'pull-winding'), ('S', 'FRAME', 'hold-winding')]
    if closed:
        edges.append(('B', 'M', 'contact-bridge'))
    return {'nodes': ['B', 'M', 'S', 'FRAME'], 'edges': edges,
            'open_boundaries': ['battery cable at B', 'control harness at S',
                                'motor brush feed at M', 'coil end leads'],
            'physical_wiring_complete': False}


def parts(fraction=0):
    if not 0 <= fraction <= 1:
        raise ValueError('Solenoid stroke fraction must be within [0, 1]')
    cylinder, ring = starter.cylinder, starter.ring
    travel = STROKE * fraction
    move = b.Pos(0, 0, -travel)
    result = {}
    result['starter-solenoid-pull-winding'] = ring(14, 9.2, -84, -35)
    result['starter-solenoid-hold-winding'] = ring(19.2, 14.5, -84, -35)
    bobbin = ring(9.15, 8.7, -85, -34) + ring(14.45, 14.05, -85, -34)
    bobbin += ring(19.5, 8.7, -85, -84.05) + ring(19.5, 8.7, -34.95, -34)
    result['starter-solenoid-winding-bobbin'] = bobbin
    result['starter-solenoid-fixed-pole'] = ring(19.5, 2.3, -88, -86)
    result['starter-solenoid-return-spring'] = starter.spring(5, .25, -86, 13.5 - travel, 4)
    rod = cylinder(2, -101, -72) + cylinder(3, -101, -100.5) + cylinder(3, -97.5, -97)
    result['starter-solenoid-contact-rod'] = move * rod
    collar = ring(3.15, 2.05, -100, -98)
    collar += ring(4, 2.05, -100.5, -100) + ring(4, 2.05, -98, -97.5)
    result['starter-solenoid-bridge-insulator'] = move * collar
    bridge = b.Pos(0, 0, -99) * b.Box(28, 8, 2) - cylinder(3.2, -102, -96)
    result['starter-solenoid-contact-bridge'] = move * bridge
    cap = cylinder(20, -117, -108) - cylinder(18, -114, -107)
    for index, station in enumerate((-10, 10), 1):
        cap -= b.Pos(station, 0, 0) * cylinder(3.1, -118, -113)
        post = cylinder(3, -123, -113) + cylinder(4, -113, -111.25)
        result[f'starter-solenoid-terminal-{index}'] = b.Pos(station, 0, 0) * post
    cap -= b.Pos(0, -12, 0) * cylinder(2.6, -118, -107)
    result['starter-solenoid-end-cap'] = cap
    result['starter-solenoid-s-terminal'] = b.Pos(0, -12, 0) * cylinder(1.5, -124, -110)
    result['starter-solenoid-s-terminal-insulator'] = b.Pos(0, -12, 0) * ring(2.5, 1.55, -119, -110)
    return {identifier: FRAME * shape for identifier, shape in result.items()}


def api(base_api):
    define, add, group = base_api
    replacements = parts()

    def define_part(identifier, shape, name, function, system, color, sources, gaps, *args, **kwargs):
        if identifier == 'starter-solenoid-coil-envelope':
            return None
        if identifier in REPLACED:
            shape = replacements[identifier]
            sources = list(dict.fromkeys(sources + SOURCES))
            gaps = gaps + GAPS
            if identifier.startswith('starter-solenoid-terminal-'):
                name = 'Starter solenoid ' + ('B battery terminal' if identifier.endswith('-1') else 'M motor terminal')
                function = 'Heavy power terminal with an internal fixed contact face. B/M assignment is the candidate convention; clocking and internal geometry are provisional.'
        return define(identifier, shape, name, function, system, color, sources, gaps, *args, **kwargs)

    def add_part(identifier, definition, parent, *args, **kwargs):
        if definition == 'starter-solenoid-coil-envelope':
            return None
        return add(identifier, definition, parent, *args, **kwargs)

    return define_part, add_part, group


def build(api):
    define, add, group = api
    for index, (identifier, shape) in enumerate(parts().items()):
        if identifier in REPLACED:
            continue
        role = identifier.removeprefix('starter-solenoid-')
        insulating = role in ('winding-bobbin', 'bridge-insulator', 's-terminal-insulator')
        color = '#43464b' if insulating else '#b87843' if role in ('pull-winding', 'hold-winding', 'contact-bridge', 's-terminal') else '#a2abb2'
        define(identifier, shape, identifier.replace('-', ' ').capitalize(), FUNCTIONS[role], 'starting', color, SOURCES, GAPS)
        add(identifier, identifier, 'starter-solenoid-assembly', explode=(0, -220 - index * 12, -40 - index * 18))
