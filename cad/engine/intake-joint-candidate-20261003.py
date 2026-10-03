"""Isolated estimated joint successor. No canonical writes or installation."""
from pathlib import Path
import json, hashlib
import build123d as b
import upper_intake_clearance_candidate as core
from fuel_mounts import MOUNT_X
ROOT = Path(__file__).resolve().parents[2]
PARAM = Path(__file__).with_name('intake-joint-candidate-20261003-parameters.json')
assert hashlib.sha256(PARAM.read_bytes()).hexdigest() == '4ee45b936aac6200273e8675af2e14f75e843c2cc74b36ad7d9cb7e3d5c5658e'
P = json.loads(PARAM.read_text())
X = [284.48 - 568.96 * u for u in P['port_stations']]
H = {h['feature_id']: (284.48 - 568.96 * h['normalized_uv'][0], -228 - 568.96 * h['normalized_uv'][1]) for h in P['holes']}

def solid(s):
    return b.Compound(children=list(s)) if isinstance(s, b.ShapeList) else s

def bake(s,label):
 folder=ROOT/'cad/engine/generated/intake-joint-candidate-20261003';folder.mkdir(exist_ok=True)
 path=folder/(label+'-baked.step');b.export_step(s,path);return b.import_step(path)

def cyl(r, z0, z1, x, y):
    return b.Pos(x, y, (z0 + z1) / 2) * b.Cylinder(r, z1 - z0)

def outline(z0, z1):
    shape = b.Pos((X[0] + X[-1]) / 2, -228, (z0 + z1) / 2) * b.Box(X[0] - X[-1], 24, z1 - z0)
    for x in X:
        shape += cyl(33, z0, z1, x, -228)
        shape = solid(shape)
    for x, y in H.values():
        nearest = max(X[-1], min(X[0], x))
        a = b.Vector(nearest, -228, 0)
        c = b.Vector(x, y, 0)
        d = c - a
        bridge = b.Pos(*(a + c) / 2) * b.Rot(0, 0, __import__('math').degrees(__import__('math').atan2(d.Y, d.X))) * b.Box(d.length + 2, 22, z1 - z0)
        bridge = b.Pos(0, 0, (z0 + z1) / 2) * bridge
        shape += bridge
        shape = solid(shape)
        shape += cyl(11, z0, z1, x, y)
        shape = solid(shape)
    return shape

def holes(shape, z0, z1, port_r=25):
    for x in X:
        shape -= cyl(port_r, z0, z1, x, -228)
        shape = solid(shape)
    for x, y in H.values():
        shape -= cyl(5.5, z0, z1, x, y)
        shape = solid(shape)
    return shape

def split(points, t):
    levels = [list(map(b.Vector, points))]
    while len(levels[-1]) > 1:
        levels.append([a * (1 - t) + c * t for a, c in zip(levels[-1], levels[-1][1:])])
    return ([v[0] for v in levels], [v[-1] for v in levels[::-1]])

def tube_sections(path, first, last):
    return b.loft([b.Plane(origin=path @ t, z_dir=path % t) * b.Circle(first + (last - first) * t) for t in (0, 0.2, 0.4, 0.6, 0.8, 1)])

def parts():
    paths = []
    lower = outline(350, 360)
    flange = b.Pos(0, -140.5, 300.5) * b.Box(688, 10, 10)
    for old, new in zip(core.PORTS, X):
        pts = [(old - 25, -140.5, 277.5), (old - 25, -183, 277.5), (old, -228, 315), (old, -228, 355)]
        a, c = split(pts, 0.65)
        c[-2] = b.Vector(new, -228, c[-2].Z)
        c[-1] = b.Vector(new, -228, 355)
        p0, p1 = (b.Bezier(*a), b.Bezier(*c))
        paths.append((p0, p1))
        flange += b.Pos(old - 25, -140.5, 277.5) * b.Rot(90, 0, 0) * b.Cylinder(25, 10)
        flange = solid(flange)
        lower += b.sweep(b.Plane(origin=p0 @ 0, z_dir=p0 % 0) * b.Circle(21), path=p0)
        lower = solid(lower)
        lower += tube_sections(p1, 21, 32)
        lower = solid(lower)
    lower += flange
    lower = solid(lower)
    for (p0, p1), old, new in zip(paths, core.PORTS, X):
        bore = b.Wire([b.Line((old - 25, -125, 277.5), p0 @ 0), p0])
        lower -= b.sweep(b.Plane(origin=bore @ 0, z_dir=bore % 0) * b.Circle(15), path=bore)
        lower = solid(lower)
        lower -= tube_sections(p1, 15, 25)
        lower = solid(lower)
        lower -= cyl(25, 354, 370, new, -228)
        lower = solid(lower)
    for x, y in H.values():
        lower -= cyl(5.5, 345, 370, x, y)
        lower = solid(lower)
    for old in core.PORTS:
        lower += cyl(10, 286, 314, old - 25, -163)
        lower = solid(lower)
        lower -= cyl(7.6, 278, 318, old - 25, -163)
        lower = solid(lower)
    for x in MOUNT_X:
        lower += b.Pos(x, -157.5, 300.5) * b.Box(14, 42, 10)
        lower = solid(lower)
        lower += cyl(8, 299, 364, x, -178)
        lower = solid(lower)
        lower -= cyl(3.2, 339, 365, x, -178)
        lower = solid(lower)
    import manifold_lifting_eye, intake_locating_dowel, rear_manifold_mounts_desktop_candidate
    for adapter in (manifold_lifting_eye, intake_locating_dowel, rear_manifold_mounts_desktop_candidate):
        lower = adapter.lower_interface(lower)
    joint = holes(outline(360, 361.5), 359, 363, 25.5)
    upper = bake(outline(361.5, 371.5),'upper-flange')
    ups = []
    for old, new in zip(core.PORTS, X):
        terminal = -150 + (old + core.PORTS[0]) / (2 * core.PORTS[0]) * 300
        path = b.Bezier((new, -228, 366.5), (new, -228, 490), (terminal, -145, 490), (terminal, -20, 490))
        ups.append(path)
        upper += bake(b.sweep(b.Plane(origin=path@0,z_dir=path%0)*b.Circle(32),path=path),'upper-runner-'+str(len(ups)))
        upper = solid(upper)
    upper += b.Pos(0, 25, 490) * core.rounded_box(400, 145, 90, 25)
    upper = solid(upper)
    upper -= b.Pos(0, 25, 490) * core.rounded_box(392, 137, 82, 21)
    upper = solid(upper)
    for new, path in zip(X, ups):
        bore=b.Wire([b.Line((new,-228,354),path@0),path])
        upper -= b.sweep(b.Plane(origin=bore@0,z_dir=bore%0)*b.Circle(25),path=bore)
        upper = solid(upper)
    for x, y in H.values():
        upper -= cyl(5.5, 354, 380, x, y)
        upper = solid(upper)
    upper += b.Pos(200, 25, 490) * b.Box(8, 124, 68)
    upper = solid(upper)
    for y in (-24, 74):
        for z in (464, 516):
            upper -= b.Pos(195, y, z) * core.cx(4.2, 22)
            upper = solid(upper)
    for y in (-2, 52):
        upper -= b.Pos(200, y, 490) * core.cx(20, 22)
        upper = solid(upper)
    from egr import intake_interface
    from regulator_vacuum import intake_interface as vacuum
    upper = b.Pos(*core.EGR_DELTA) * intake_interface(b.Pos(*(-v for v in core.EGR_DELTA)) * upper)
    upper = vacuum(upper)
    return ({'efi-lower-intake': solid(lower), 'efi-upper-intake': solid(upper), 'efi-upper-intake-gasket': solid(joint)}, paths, ups)
