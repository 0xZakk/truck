"""Photo-supported front exhaust form with provisional dimensional transitions."""
import build123d as cad
import manifold_lifting_eye as lifting_eye

PORTS = (309.48, 195.688, 81.896)
PORT_Z = 277.5
HEAD_ORIGIN_Z = 255.5
SOURCES = ['dorman-674185-profile-specification', 'dorman-674185-head-facing-photo',
           'dorman-674185-opposite-photo', 'dorman-674185-application']
GAPS = [
    'Dorman674-185 manufacturer photos/specifications establish rectangular entries and a blended collector for its1994F1504.9L front application, not the installed truck casting identity.',
    'Entry28x28mm with3mm corners, outer pad36x36mm with6mm corners, runner radii15/18mm and collector radii18/24mm are dimensional study assumptions.',
    'The three port stations, rectangular-to-round transitions, collector centerline and outlet station retain provisional engine datums. Wall thickness, thermal stress, flow and casting manufacturability are unverified.',
    'Existing provisional lifting-eye lugs are retained. Other manifold clamping stations, production flange outline and downstream pipe joint remain incomplete.',
    'Rear manifold and intake port shape are not inferred from the front replacement photograph.'
]


def section(horizontal, depth, width=28, radius=3):
    plane = cad.Plane(origin=(horizontal, depth, PORT_Z), x_dir=(1, 0, 0), z_dir=(0, -1, 0))
    return plane * cad.RectangleRounded(width, width, radius)


def runner_path(horizontal):
    return cad.Bezier((horizontal, -138, PORT_Z), (horizontal, -188, PORT_Z),
                      (horizontal, -180, 258), (horizontal, -180, 235))


def transition(horizontal, outside=False, shrink=0):
    path = runner_path(horizontal)
    radius = (18 if outside else 15) - shrink
    width = (36 if outside else 28) - 2 * shrink
    corner = (6 if outside else 3) - shrink
    end = cad.Plane(origin=path @ .27, x_dir=(1, 0, 0), z_dir=path % .27) * cad.Circle(radius)
    return cad.loft([section(horizontal, -132, width, corner),
                     section(horizontal, -141, width, corner), end], ruled=True)


def runner_void(horizontal, shrink=0):
    path = runner_path(0)
    tail = path.trim(.27, 1)
    wire = cad.Wire([tail, cad.Line(path @ 1, (0, -180, 225))])
    sweep = cad.sweep(cad.Plane(origin=tail @ 0, x_dir=(1, 0, 0), z_dir=tail % 0)
                      * cad.Circle(15 - shrink), path=wire)
    return cad.Pos(horizontal, 0, 0) * transition(0, shrink=shrink).fuse(sweep)


def head_void(horizontal, shrink=0):
    end = cad.Plane(origin=(horizontal, -115, PORT_Z), x_dir=(1, 0, 0), z_dir=(0, -1, 0)) * cad.Circle(15 - shrink)
    return cad.loft([section(horizontal, -134, 28 - 2 * shrink, 3 - shrink),
                     section(horizontal, -127, 28 - 2 * shrink, 3 - shrink), end], ruled=True)


def capsule(radius):
    length = PORTS[0] - PORTS[-1]
    result = cad.Pos(PORTS[1], -180, 230) * cad.Rot(0, 90, 0) * cad.Cylinder(radius, length)
    for horizontal in (PORTS[0], PORTS[-1]):
        result += cad.Pos(horizontal, -180, 230) * cad.Sphere(radius)
    return result


def front_casting():
    shape = capsule(24)
    for horizontal in PORTS:
        path = runner_path(0).trim(.27, 1)
        sweep = cad.sweep(cad.Plane(origin=path @ 0, x_dir=(1, 0, 0), z_dir=path % 0) * cad.Circle(18), path=path)
        outer = transition(0, outside=True).fuse(sweep)
        outer &= cad.Pos(0, -183, PORT_Z) * cad.Box(80, 100, 100)
        shape += cad.Pos(horizontal, 0, 0) * outer
    shape += cad.Pos(PORTS[1], -180, 175) * cad.Cylinder(27, 70)
    shape = lifting_eye.front_interface(shape)
    cavity = capsule(18)
    cavity += cad.Pos(PORTS[1], -180, 175) * cad.Cylinder(20, 86)
    for horizontal in PORTS:
        cavity += runner_void(horizontal)
    return shape - cavity


def head_interface(shape):
    world = cad.Pos(0, 0, HEAD_ORIGIN_Z) * shape
    for horizontal in PORTS:
        world += cad.extrude(section(horizontal, -115, 36, 6), amount=18)
        world -= head_void(horizontal)
    return cad.Pos(0, 0, -HEAD_ORIGIN_Z) * world


def front_interface(previous_shape):
    """Replace the old casting completely; apply later front-casting edits afterward."""
    return front_casting()


ADAPTERS = {'cylinder-head': head_interface, 'exhaust-front': front_interface}
