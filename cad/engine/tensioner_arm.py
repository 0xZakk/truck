"""38131 architecture study; cartridge internals and installed datums unresolved."""
import build123d as cad

POSITION = (473.56, 0, 435)
ROTATION = (0, 90, 90)
PIVOT_OFFSET = -75
SOURCES = ['gates-1994-drive', 'gates-38131-instructions', 'ford-accessory-routing']
GAPS = [
    'Gates 38131 instructions establish an enclosed preloaded spring, moving arm, mounting bolt, locating pin and optional locating-pin bushing. They do not establish internal spring geometry.',
    'The sealed spring/pivot cartridge is an unresolved envelope: spring, damping element, seals, stops and internal retainers are not separately reconstructed.',
    '75 mm arm length, 64 mm cartridge diameter, axial stack, arm contour, fastener dimensions and pivot sleeve are illustrative construction assumptions, not measured Gates or Ford geometry.',
    'Pulley station (473.56,0,435), pivot station (433.56,-75,435) and arm angle are provisional; top-center placement follows labeled Ford routing while the axial datum matches the illustrative pump/damper belt plane. These are not measured installation coordinates. Engine mounting bracket, load path and operating travel remain unresolved.',
    'The removable bushing depicts the large-hole bracket option. Gates specifies 1/2 inch and 5/16 inch bracket holes, not the modeled pin/bushing clearances or installed bracket choice.',
    'Smooth fastener shanks omit threads, grades and tightening specifications. Collision-free geometry does not verify production fit or spring behavior.'
]


def cylinder(radius, width, axial, horizontal=0, vertical=0):
    return cad.Pos(horizontal, vertical, axial) * cad.Cylinder(radius, width)


def components():
    cartridge = cylinder(32, 40, -53, PIVOT_OFFSET) - cylinder(8, 42, -53, PIVOT_OFFSET)
    cartridge += cylinder(3.8, 12, -77, PIVOT_OFFSET, 20)
    arm = cylinder(30, 12, -27, PIVOT_OFFSET)
    arm += cad.Pos(PIVOT_OFFSET / 2, 0, -27) * cad.Box(75, 22, 12)
    arm += cylinder(16, 12, -27)
    arm -= cylinder(8, 14, -27, PIVOT_OFFSET)
    arm += cylinder(14, 12.5, -14.75)
    arm += cylinder(8.4, 17, 0)
    arm -= cylinder(5.7, 45, -9)
    sleeve = cylinder(7.9, 52, -47, PIVOT_OFFSET) - cylinder(6, 54, -47, PIVOT_OFFSET)
    mount_bolt = cylinder(5.5, 60, -49, PIVOT_OFFSET)
    mount_bolt += cad.Pos(PIVOT_OFFSET, 0, -21) * cad.extrude(cad.RegularPolygon(12, 6), amount=6)
    pulley_bolt = cylinder(5.5, 35, -8.5)
    pulley_bolt += cad.Pos(0, 0, 8.5) * cad.extrude(cad.RegularPolygon(10, 6), amount=6)
    bushing = cylinder(6.2, 10, -78, PIVOT_OFFSET, 20) - cylinder(3.9, 12, -78, PIVOT_OFFSET, 20)
    return {
        'tensioner-spring-cartridge': cartridge,
        'tensioner-moving-arm': arm,
        'tensioner-pivot-sleeve': sleeve,
        'tensioner-mounting-bolt': mount_bolt,
        'tensioner-pulley-bolt': pulley_bolt,
        'tensioner-locating-bushing': bushing,
    }


def parts():
    mount = cad.Pos(*POSITION) * cad.Rot(*ROTATION)
    return {identifier: mount * shape for identifier, shape in components().items()}


def build(api):
    define, add, group = api
    group('tensioner-support-assembly', 'Tensioner support · construction study', 'accessory-drive')
    descriptions = {
        'tensioner-spring-cartridge': ('Tensioner spring/pivot cartridge · unresolved interior', 'Houses the enclosed preloaded spring that biases the arm. This envelope intentionally leaves spring turns, anchors, damping and stops unresolved; the rear locating pin registers the housing.', '#797d80'),
        'tensioner-moving-arm': ('Tensioner moving arm', 'Carries the pulley bearing on an offset journal and transfers belt load to the spring pivot. Its simplified contour, journal and working angle are provisional.', '#a1a7aa'),
        'tensioner-pivot-sleeve': ('Tensioner pivot sleeve · illustrative', 'Illustrates separation of arm rotation from the central mounting fastener. The actual bearing or bushing arrangement has not been sourced.', '#aa9477'),
        'tensioner-mounting-bolt': ('Tensioner central mounting bolt · illustrative', 'Represents the central attachment described by Gates. The supporting engine bracket, thread and clamping stack still require evidence.', '#929ba1'),
        'tensioner-pulley-bolt': ('Tensioner pulley retaining bolt · illustrative', 'Illustrates retention on the arm journal. Fastener dimensions, thread and contact with the unresolved bearing cartridge are assumptions; separate bearing races are not reconstructed.', '#929ba1'),
        'tensioner-locating-bushing': ('Tensioner locating-pin bushing · optional', 'Adapts the rear locating pin to the larger bracket-hole variant described in the Gates 38131 instructions. The installed bracket option is unknown.', '#b3a078'),
    }
    for index, (identifier, shape) in enumerate(components().items()):
        name, function, color = descriptions[identifier]
        define(identifier, shape, name, function, 'accessory-drive', color, SOURCES, GAPS)
        add(identifier, identifier, 'tensioner-support-assembly', POSITION, (180 + index * 38, 0, 35), ROTATION)
