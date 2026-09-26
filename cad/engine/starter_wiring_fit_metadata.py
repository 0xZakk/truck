"""Integration adapter for the separately validated nonpenetrating wiring geometry."""
import starter_wiring as accepted
import starter_wiring_fit as fitted

GAPS = [
    'The four coil-end conductors terminate at nonpenetrating face interfaces. Separate S routes and insulating sleeves meet separate patches of the same S terminal; no interpenetrating conductor or sleeve union is required.',
    'Zero-distance CAD interfaces and directional contact-area witnesses establish geometric attachment only. Production solder, crimp or weld construction, contact resistance, preload, ampacity and dielectric strength remain unresolved.'
]


def api(base_api):
    define, add, group = base_api
    replacements = fitted.parts()

    def define_part(identifier, shape, name, function, system, color='#8498a3', sources=(), gaps=(), *args, **kwargs):
        if identifier in replacements:
            shape = replacements[identifier]
            gaps = list(dict.fromkeys(list(gaps) + accepted.GAPS + GAPS))
            if identifier.startswith('starter-solenoid-lead-insulation-'):
                function = 'Separate provisional dielectric sleeve around one coil-end conductor. The two S sleeves remain physically separated; the S sleeve ends meet the existing terminal insulator without overlapping material.'
            elif identifier.startswith('starter-solenoid-lead-'):
                function = 'Provisional coil-end conductor with nonpenetrating winding and terminal/frame attachment faces. The two S conductors contact separate patches of the same terminal; aggregate winding interiors remain unresolved.'
        return define(identifier, shape, name, function, system, color, sources, gaps, *args, **kwargs)

    return define_part, add, group
