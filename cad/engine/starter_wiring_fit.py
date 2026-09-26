"""Corrected separate S leads and zero-penetration coil attachment interfaces."""
import build123d as b
import starter_motor as starter
import starter_solenoid as switch
import starter_wiring as accepted

REPLACED = accepted.REPLACED
CONTACTS = accepted.CONTACTS
ROUTES = {role: list(points) for role, points in accepted.ROUTES.items()}
ROUTES['pull-s'][-1] = (.8, -12.65, -109.8)
ROUTES['hold-s'][-1] = (-.8, -11.35, -109.8)


def parts():
    baseline = starter.parts()
    baseline.update(switch.parts())
    result = {identifier: baseline[identifier] for identifier in REPLACED}
    for role, points in ROUTES.items():
        core = switch.FRAME * accepted.route(points, .4)
        clearance = switch.FRAME * accepted.route(points, .75)
        sleeve = switch.FRAME * (accepted.route(points, .65) - accepted.route(points, .45))
        for target in CONTACTS[role]:
            core -= baseline[target]
            sleeve -= baseline[target]
        if role in ('pull-s', 'hold-s'):
            sleeve -= baseline['starter-solenoid-s-terminal-insulator']
        for identifier in REPLACED:
            result[identifier] -= clearance
        result['starter-solenoid-lead-' + role] = core
        result['starter-solenoid-lead-insulation-' + role] = sleeve
    return result
