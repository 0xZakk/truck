"""Isolated two-feed/two-ground Ford PMGR comparison wiring, with assumed clocking."""
import math
import build123d as b
import starter_motor as starter
import starter_solenoid as switch
import starter_wiring as routes

SOURCES = ['ford-pmgr-starter-exploded', 'ford-pmgr-brush-connector-comparison', 'jn-pmgr-brush-holder-comparison', 'wagner-pmgr-brush-holder-cross-reference']
GAPS = [
    'Ford family service text identifies the positive brush connector at M and its frame grommet. J&N photographs and Wagner cross-references support a two-feed/two-ground PMGR comparison; this is not a recovered1994F150 brush wiring drawing.',
    'Brushes1and4 are assigned feed and2and3 ground only for this provisional90degree CAD layout. Actual production brush angle, polarity clocking, lead gauge, braid length, joining process and eyelet orientation remain unverified.',
    'Conductors and sleeves are aggregate geometry, not strands or current/thermal/insulation calculations. Flexible braid deformation and brush-wear travel are not modeled.',
    'Commutator-to-armature winding connections, individual winding topology, battery cable and control harness remain open. Complete starter electrical continuity is not claimed.'
]
REPLACED = {'starter-frame', 'starter-brush-carrier'} | {'starter-brush-holder-' + str(index) for index in range(1, 5)}
FEED_PATH = [(10, -59, -120.5), (16, -48, -126), (22, -22, -136)]
PIGTAILS = {
    'positive-1': [(22, -22, -136), (30, -10, -134), (27, -3.1, -134)],
    'positive-4': [(22, -22, -136), (10, -30, -134), (3.1, -27, -134)],
    'ground-2': [(25, 30 / math.sqrt(2), -141.5), (27, 24, -138), (10, 30, -136), (3.1, 27, -134)],
    'ground-3': [(-25, -30 / math.sqrt(2), -141.5), (-27, -24, -138), (-30, -10, -136), (-27, -3.1, -134)]
}


def parts():
    baseline = starter.parts()
    baseline.update(switch.parts())
    result = {identifier: baseline[identifier] for identifier in REPLACED}
    eyelet = b.Pos(10, -65, 0) * starter.ring(6, 3, -121, -120)
    feed = routes.route(FEED_PATH, 1.3) + eyelet
    result['starter-motor-positive-feed'] = feed
    jacket = routes.route(FEED_PATH, 1.9) - routes.route(FEED_PATH, 1.35)
    jacket -= eyelet
    jacket -= baseline['starter-solenoid-terminal-nut-2']
    jacket -= b.Pos(*FEED_PATH[-1]) * b.Sphere(4)
    result['starter-motor-feed-jacket'] = jacket
    zone = starter.ring(43.5, 36.5, -143, -122)
    grommet = routes.route(FEED_PATH, 2.5).intersect(zone)
    flanges = routes.route(FEED_PATH, 3.2).intersect(zone) - baseline['starter-frame']
    grommet = (grommet + flanges) - routes.route(FEED_PATH, 2)
    result['starter-motor-feed-grommet'] = grommet
    result['starter-frame'] -= routes.route(FEED_PATH, 2.55)
    ground_bridge = starter.ring(31.2, 28.8, -143, -142)
    result['starter-brush-carrier'] -= starter.ring(31.3, 28.7, -144, -141.9)
    for angle in (45, 225):
        location = b.Rot(0, 0, angle) * b.Pos(30, 0, 0)
        ground_bridge += location * starter.ring(4, 1.5, -143, -141)
        result['starter-brush-carrier'] -= location * starter.cylinder(4.1, -144, -140)
    for angle in (45, 225):
        ground_bridge -= b.Rot(0, 0, angle) * b.Pos(30, 0, 0) * starter.cylinder(1.5, -144, -137)
    result['starter-motor-ground-bridge'] = ground_bridge
    for role, points in PIGTAILS.items():
        brush = 'starter-brush-' + role[-1]
        terminal = 'starter-motor-positive-feed' if role.startswith('positive') else 'starter-motor-ground-bridge'
        pigtail = routes.route(points, .65) - baseline[brush] - result[terminal]
        result['starter-brush-pigtail-' + role] = pigtail
        result['starter-brush-holder-' + role[-1]] -= routes.route(points, .95)
        result['starter-brush-carrier'] -= routes.route(points, .95)
    return result
