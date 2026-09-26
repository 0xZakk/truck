"""Acceptance gates for the incomplete clutch comparison, not a rigid substitute."""
import manual_clutch_boundary

PREFERRED_BASELINE = '10-inch-R2'
REQUIRED_INTERFACES = {
    'cover_to_pressure_ring': {
        'mechanism': 'Tangential straps transmit torque and lift/locate the pressure plate.',
        'geometry_resolved': False,
        'needed': 'Application-specific strap stations, sections, rivets and pressure-plate lugs.'
    },
    'cover_to_diaphragm': {
        'mechanism': 'Cover-supported fulcrum ring/rivets react the diaphragm spring load.',
        'geometry_resolved': False,
        'needed': 'Application-specific fulcrum type, radius, support and retention.'
    },
    'diaphragm_to_pressure_ring': {
        'mechanism': 'Outer diaphragm load ring applies axial clamp force.',
        'geometry_resolved': False,
        'needed': 'Installed diaphragm section, coning, contact radius, preload and release stroke.'
    },
    'facings_to_carrier': {
        'mechanism': 'Facings transmit friction torque through attachments and cushioning segments.',
        'geometry_resolved': False,
        'needed': 'Facing rivets and cushioning-segment layout; touching annuli alone do not provide these joints.'
    },
    'carrier_to_hub': {
        'mechanism': 'Drive/retainer plates load window springs against a hub flange; friction elements damp relative rotation.',
        'geometry_resolved': False,
        'needed': 'Verified hub flange, spring windows/counts, stops, bushes and friction stack. A solid annular cartridge is not an equivalent mechanism.'
    },
    'hub_to_input_shaft': {
        'mechanism': 'Ten-spline nominal interface transfers torque while allowing axial disc motion.',
        'geometry_resolved': False,
        'needed': 'Spline tooth form/fit, input shaft and pilot-bearing interface.'
    }
}


def acceptance(variant):
    if variant not in manual_clutch_boundary.VARIANTS:
        raise ValueError(f'Unknown clutch branch: {variant}')
    missing = [name for name, interface in REQUIRED_INTERFACES.items() if not interface['geometry_resolved']]
    if variant == '11-inch-2F':
        missing.append('eleven_inch_upgrade_fastener_and_flywheel_interface')
    return {'variant': variant, 'owner_configuration_baseline': variant == PREFERRED_BASELINE,
            'installed_disc_verified': False, 'missing_interfaces': missing,
            'ready_for_installed_assembly': not missing}


def require_complete_load_path(variant):
    report = acceptance(variant)
    if not report['ready_for_installed_assembly']:
        raise ValueError('Incomplete clutch load path: ' + ', '.join(report['missing_interfaces']))
    return report
