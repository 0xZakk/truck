"""Provisional ALT placement consistent with the Ford with-A/C route ordering."""
import build123d as cad
import accessory_brackets as base

POSITION = (473.56, -325, 320)
DISPLACEMENT = (0, 0, -90)
EARS = [(-248, 320), (-402, 320)]
SOURCES = ['ford-accessory-brackets', 'ford-accessory-routing', 'ford-alternator-study']
GAPS = [
    'The Ford with-A/C diagram supports ALT below the tensioner and on the opposite side from PS; all actual coordinates remain provisional.',
    'The owner passenger-side engine photo corroborates side/front placement only; perspective and occlusion do not dimension the station.',
    'The ring, ribs, hole sizes and fasteners are illustrative. Existing dry head and block attachment seats are retained without changing either casting.',
    'The alternator remains a generic integral-regulator study; exact installed amperage and housing identity are unknown.',
    'No belt is installed by this candidate. Correct qualitative ordering does not establish nominal belt fit or resolve the coolant-outlet envelope.'
]

def bracket():
    shape = base.boss(base.ALT_FACE, -325, 320, 88, 70)
    for y,z in EARS:
        shape += base.boss(base.ALT_FACE,y,z,11,5.5)
    shape += base.web(base.ALT_FACE,(-243,320),(-200,310),18)
    shape += base.web(base.ALT_FACE,(-200,310),(-200,220),18)
    for z in (220,310):
        shape += base.engine_foot(-100,z,base.ALT_FACE+5,-200)
    for y,z in EARS:
        shape -= base.axial(5.5,14,(base.ALT_FACE+5,y,z))
    return shape

def replacements():
    result = {'alternator-support-bracket': bracket()}
    for index,(y,z) in enumerate(EARS,1):
        result[f'alt-bracket-bolt-{index}'] = base.bolt(418.76,448.56,y,z,4.9)
    return result

def placement_override(occurrence):
    if occurrence['parent'] == 'alternator-assembly':
        return POSITION
    return None
