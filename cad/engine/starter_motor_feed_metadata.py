"""Optional integration and teaching metadata for the isolated motor-feed study."""
import starter_motor_feed as feed
import starter_wiring as coil_wiring

FUNCTIONS = {
    'starter-motor-positive-feed': 'Provisional common positive conductor and eyelet join solenoid M to two brush pigtails. Ford PMGR-family service text establishes this connector role; braid geometry and installed routing are assumed.',
    'starter-motor-feed-jacket': 'Separate provisional dielectric jacket surrounds the external motor-feed conductor. It meets a separate frame grommet; material, thickness and electrical durability are unverified.',
    'starter-motor-feed-grommet': 'Flanged provisional insulating grommet locates the motor feed through the bored frame wall. It represents the grommet identified by Ford, without claiming production shape or environmental sealing.',
    'starter-motor-ground-bridge': 'Common provisional metal return bridge connects two ground pigtails to the rear end plate and retaining screws. A metal ground bracket is visible in comparison photographs; this annular profile and two-pad construction are assumed.',
    'starter-solenoid-terminal-2': 'Heavy M terminal joins the pull-winding end and external positive-brush connector. The power-contact bridge supplies M at closure. Armature winding connections and complete electrical performance remain unresolved.',
    'starter-brush-carrier': 'Provisional insulating brush carrier locates four holders and separates their hardware from the common ground bridge. Local relief channels accommodate the new pigtails; production molding remains unverified.',
    'starter-frame': 'Supports the permanent-magnet structure and rear brush region. A provisional bored opening and separate grommet admit the motor-feed conductor without contact to the grounded frame.'
}


def api(base_api):
    define, add, group = base_api
    replacements = feed.parts()

    def define_part(identifier, shape, name, function, system, color='#8498a3', sources=(), gaps=(), *args, **kwargs):
        if identifier in replacements:
            shape = replacements[identifier]
        if identifier.startswith('starter-'):
            gaps = [gap for gap in gaps if gap != coil_wiring.GAPS[2]]
            gaps = list(dict.fromkeys(gaps + feed.GAPS))
            sources = list(dict.fromkeys(list(sources) + feed.SOURCES))
            function = FUNCTIONS.get(identifier, function)
            if identifier in ('starter-brush-1', 'starter-brush-4'):
                function = 'Brush assigned to the positive pair in this provisional clocking. A modeled pigtail joins it to the common M feed; production brush angle and commutator winding topology remain unverified.'
            elif identifier in ('starter-brush-2', 'starter-brush-3'):
                function = 'Brush assigned to the ground pair in this provisional clocking. A modeled pigtail joins it to the common return bridge and rear plate; production brush angle and commutator winding topology remain unverified.'
        return define(identifier, shape, name, function, system, color, sources, gaps, *args, **kwargs)

    return define_part, add, group


def build(base_api):
    define, add, group = base_api
    for index, (identifier, shape) in enumerate(feed.parts().items()):
        if identifier in feed.REPLACED:
            continue
        function = FUNCTIONS.get(identifier, 'Separate provisional flexible braid envelope joins one brush to its feed or return conductor at nonpenetrating attachment faces. Strand construction, brush-wear travel and lead deformation remain unresolved.')
        dielectric = identifier.endswith(('jacket', 'grommet'))
        define(identifier, shape, identifier.replace('-', ' ').capitalize(), function, 'starting', '#44474b' if dielectric else '#b87843', feed.SOURCES, feed.GAPS)
        add(identifier, identifier, 'starter-motor-assembly', explode=(-320, -320, -100 - (index - len(feed.REPLACED)) * 100))
