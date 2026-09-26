"""Ford CII slipper-pump construction with provisional geometry and belt station."""
import math

import build123d as cad

POSITION = (473.56, 280, 410)
ROTATION = (0, 90, 0)
PULLEY_RADIUS = 5.17 * 25.4 / 2
PULLEY_BORE = 0.6854 * 25.4
SOURCES = ['ford-cii-pump-study', 'dorman-300-029', 'gates-1994-drive', 'ford-accessory-routing']
GAPS = [
    'Ford identifies the CII slipper pump with ten rotor cavities, ten slippers and springs, two dowels, pressure plates, disc spring, valve cover, reservoir, seals and flow-control valve. All internal dimensions and clearances remain illustrative.',
    'Dorman 300-029 provides 5.17 inch pulley OD and steel press-fit construction. Its bore value 0.6854 has no displayed unit; treating this as inches is an explicit assumption. Dorman lists five grooves, conflicting with Ford six-rib seating instructions and Gates belt data. The study uses six illustrative grooves for the Ford belt; exact Dorman replacement compatibility remains unresolved.',
    'Pulley width, dish, hub offset and groove profile are provisional. The pulley press fit is drawn with clearance for study; no production interference or fit tolerance is claimed.',
    'The elliptical two-lobe cam track, slipper contour, spring geometry, shaft support bushing and smooth spline interface are illustrative. This is not a displacement, contact-motion or pressure simulation.',
    'Valve body is one unresolved flow/relief assembly, not an invented relief-valve interior. Valve bore, passages, spool, outlet and return fitting geometry are provisional and do not establish a complete working hydraulic circuit.',
    'Reservoir shape, wall thickness, cap/dipstick, sealing grooves, mount ears, port positions and material colors are construction-study approximations. Ford supports a fiberglass-reinforced nylon reservoir.',
    'Station (473.56,280,410) is an illustrative upper-LH accessory position following the labeled Ford routing and provisional belt plane. Exact engine bracket, hose routing, working belt geometry and installed pump identity remain unresolved.',
]


def cylinder(radius, length, axial):
    return cad.Pos(0, 0, axial) * cad.Cylinder(radius, length)


def ring(outer, inner, length, axial):
    return cylinder(outer, length, axial) - cylinder(inner, length + 2, axial)


def radial_cylinder(radius, length, center, radial_x=-10, axial=-104):
    return cad.Pos(radial_x, center, axial) * cad.Rot(-90, 0, 0) * cad.Cylinder(radius, length)


def torus(radius, wire, axial):
    return cad.Pos(0, 0, axial) * cad.Torus(radius, wire)


def spring(height, radius, wire, turns):
    path = cad.Helix(pitch=height / turns, height=height, radius=radius)
    profile = cad.Plane(path @ 0, z_dir=path % 0) * cad.Circle(wire)
    return cad.sweep(profile, path=path)


def dowel_holes(shape):
    for direction in (-1, 1):
        shape -= cad.Pos(0, 36 * direction, 0) * cylinder(2.15, 80, -85)
    return shape


def housing():
    shape = ring(58, 14.2, 8, -45)
    shape += ring(48, 44, 71, -84.5)
    shape += ring(20, 14.2, 22, -30)
    shape -= cylinder(44.8, 2.2, -118)
    shape -= radial_cylinder(7.6, 24, 46)
    for angle in (45, 165, 285):
        radians = math.radians(angle)
        location = cad.Pos(62 * math.cos(radians), 62 * math.sin(radians), 0)
        shape += location * cylinder(10, 8, -45)
        shape -= location * cylinder(4.8, 10, -45)
    return shape


def reservoir():
    shape = cylinder(56, 78, -89) - cylinder(52, 76, -86)
    neck = cad.Pos(-82, 0, -95) * cad.Rot(0, -90, 0) * cad.Cylinder(18, 60)
    shape += neck
    shape -= cad.Pos(-81, 0, -95) * cad.Rot(0, -90, 0) * cad.Cylinder(15, 66)
    shape -= radial_cylinder(10.2, 30, 56)
    shape += radial_cylinder(6, 28, 64, 20, -98)
    shape -= radial_cylinder(3.5, 36, 63, 20, -98)
    return shape


def cap():
    shape = cad.Pos(-115, 0, -95) * cad.Rot(0, 90, 0) * cad.Cylinder(20, 6)
    shape += cad.Pos(-121, 0, -95) * cad.Box(8, 8, 32)
    shape += cad.Pos(-88.5, 0, -95) * cad.Box(47, 2, 3)
    return shape


def pressure_plate(front):
    center, width, bore = (-59.5, 7, 8.8) if front else (-91, 6, 11.2)
    shape = ring(43, bore, width, center)
    for direction in (-1, 1):
        slot = cad.Pos(28 * direction, 0, center - width) * cad.extrude(cad.SlotOverall(16, 5, rotation=90), amount=width * 2)
        shape -= slot
    if front:
        shape -= torus(40.8, 1.2, -56.5) + torus(12, 1.2, -56.5)
    return dowel_holes(shape)


def cam():
    chamber = cad.Pos(0, 0, -89) * cad.extrude(cad.Ellipse(30, 26), amount=27)
    return dowel_holes(cylinder(42.5, 25, -75.5) - chamber)


def rotor():
    shape = ring(23, 8.8, 24.6, -75.5)
    for index in range(10):
        shape -= cad.Rot(0, 0, index * 36) * cad.Pos(24.5, 0, -75.5) * cad.Box(19, 5.8, 26)
    return shape


def slipper(index):
    angle = math.radians(index * 36)
    radius = 1 / math.sqrt((math.cos(angle) / 30) ** 2 + (math.sin(angle) / 26) ** 2)
    blank = cad.Rot(0, 0, index * 36) * cad.Pos(radius - 3.5, 0, -75.5) * cad.Box(7, 5.3, 24.4)
    chamber = cad.Pos(0, 0, -88) * cad.extrude(cad.Ellipse(29.85, 25.85), amount=25)
    shape = blank.intersect(chamber)
    groove = cad.Rot(0, 0, index * 36) * cad.Pos(radius - 0.5, 0, -75.5) * cad.Box(1, 1, 25)
    return shape - groove


def slipper_spring(index):
    angle = math.radians(index * 36)
    radius = 1 / math.sqrt((math.cos(angle) / 30) ** 2 + (math.sin(angle) / 26) ** 2)
    coil = spring(radius - 22.8, 1.3, 0.35, 3)
    return cad.Rot(0, 0, index * 36) * cad.Pos(15.4, 0, -75.5) * cad.Rot(0, 90, 0) * coil


def valve_cover():
    shape = cylinder(43, 22, -105)
    shape -= radial_cylinder(7.5, 68, 18)
    shape -= cylinder(9.2, 4, -95)
    shape -= torus(42.6, 1.3, -113.5)
    return dowel_holes(shape)


def outlet():
    shape = radial_cylinder(7.4, 26, 47)
    shape += cad.Pos(-10, 60, -104) * cad.Rot(-90, 0, 0) * cad.extrude(cad.RegularPolygon(12, 6), amount=8)
    return shape - radial_cylinder(3.5, 36, 51)


def pulley():
    shape = ring(PULLEY_RADIUS, PULLEY_RADIUS - 4, 27, 0)
    shape += ring(PULLEY_RADIUS - 2, PULLEY_BORE / 2, 3, -4)
    shape += ring(17, PULLEY_BORE / 2, 24, 0)
    for index in range(6):
        axial = (index - 2.5) * 3.6
        profile = cad.Plane.XZ * cad.Polygon((PULLEY_RADIUS - 1.6, axial), (PULLEY_RADIUS + 1, axial - 1), (PULLEY_RADIUS + 1, axial + 1), align=None)
        shape -= cad.revolve(profile, axis=cad.Axis.Z)
    return shape


def components():
    disc_profile = cad.Plane.XZ * cad.Polygon((15, -55.5), (37, -53), (37, -51.8), (15, -54.3), align=None)
    retaining_ring = ring(44.7, 40.5, 2, -118) - cad.Pos(44, 0, -118) * cad.Box(10, 8, 4)
    shaft_clip = ring(10.8, 8.7, 1.2, -90) - cad.Pos(10, 0, -90) * cad.Box(5, 3, 3)
    valve = radial_cylinder(7.1, 4, 14) + radial_cylinder(5, 11, 21.5) + radial_cylinder(7.1, 4, 29)
    valve_spring = cad.Pos(-10, -9, -104) * cad.Rot(-90, 0, 0) * spring(18, 5, 0.6, 5)
    shapes = {
        'ps-pump-housing': housing(),
        'ps-pump-reservoir': reservoir(),
        'ps-pump-cap-dipstick': cap(),
        'ps-pump-shaft': cylinder(8.6, 108, -40) - cylinder(3.2, 14, 8),
        'ps-pump-shaft-bushing': ring(14, 8.8, 16, -33),
        'ps-pump-shaft-seal': ring(14, 8.8, 4, -21),
        'ps-pump-shaft-seal-retainer': ring(15, 8.8, 1, -18.5),
        'ps-pump-disc-spring': cad.revolve(disc_profile, axis=cad.Axis.Z),
        'ps-pump-lower-plate': pressure_plate(True),
        'ps-pump-lower-outer-seal': torus(40.8, 1.1, -56.5),
        'ps-pump-lower-inner-seal': torus(12, 1.1, -56.5),
        'ps-pump-cam': cam(),
        'ps-pump-rotor': rotor(),
        'ps-pump-rotor-clip': shaft_clip,
        'ps-pump-upper-plate': pressure_plate(False),
        'ps-pump-valve-cover': valve_cover(),
        'ps-pump-valve-cover-seal': torus(42.6, 1.1, -113.5),
        'ps-pump-cover-retaining-ring': retaining_ring,
        'ps-pump-reservoir-seal': ring(56, 52, 1, -49.5),
        'ps-pump-flow-valve': valve,
        'ps-pump-flow-spring': valve_spring,
        'ps-pump-outlet-fitting': outlet(),
        'ps-pump-outlet-seal': radial_cylinder(10, 2, 54) - radial_cylinder(7.5, 4, 54),
        'ps-pump-pulley': pulley(),
    }
    for index, direction in enumerate((-1, 1), 1):
        shapes[f'ps-pump-dowel-{index}'] = cad.Pos(0, direction * 36, 0) * cylinder(2, 57, -84)
    for index in range(10):
        shapes[f'ps-pump-slipper-{index + 1}'] = slipper(index)
        shapes[f'ps-pump-slipper-spring-{index + 1}'] = slipper_spring(index)
    return shapes


def parts():
    mount = cad.Pos(*POSITION) * cad.Rot(*ROTATION)
    return {identifier: mount * shape for identifier, shape in components().items()}


def descriptions():
    labels = {
        'housing': ('Pump housing and front plate', 'Encloses the CII cartridge and supports the shaft. Three mounting ears follow the exploded-view architecture; dimensions and engine bracket remain unresolved.', '#899197'),
        'reservoir': ('Reinforced-nylon reservoir and return nipple', 'Stores steering fluid around the pump housing. Owner photographs show a yellowed translucent reservoir and dark cap; hollow body, filler neck and return passage have provisional contour and thickness.', '#c7b574'),
        'cap-dipstick': ('Reservoir cap and dipstick', 'Closes the filler neck and permits checking fluid level. Bayonet detail and level markings remain unresolved.', '#4b5155'),
        'shaft': ('Pump rotor shaft', 'Transfers press-on pulley torque to the rotor. Production splines, stepped diameters and fit are not reconstructed.', '#9ca7af'),
        'shaft-bushing': ('Shaft support bushing · illustrative', 'Represents plain shaft support in the front housing. Bearing construction and dimensions require further evidence.', '#a39166'),
        'shaft-seal': ('Pump shaft seal', 'Separates the fluid cavity from the rotating drive shaft. The lip profile and material stack are unresolved.', '#3d4145'),
        'shaft-seal-retainer': ('Shaft seal retainer', 'Represents the seal retainer shown in the Ford exploded drawing. Exact section and retention fit are provisional.', '#8f979e'),
        'disc-spring': ('Pressure-plate disc spring', 'Preloads the pressure-plate stack. Ford specifies its dished orientation; modeled deflection and spring rate are illustrative.', '#8e979f'),
        'lower-plate': ('Lower pressure plate', 'Closes the pulley-side pumping chambers and carries inner and outer seals. Kidney-port outlines and fluid paths are provisional.', '#8f969b'),
        'lower-outer-seal': ('Lower pressure-plate outer seal', 'Separates pressure regions at the lower plate. O-ring section and compression are illustrative.', '#353d43'),
        'lower-inner-seal': ('Lower pressure-plate inner seal', 'Seals around the central shaft region of the pressure plate. Cross-section is provisional.', '#353d43'),
        'cam': ('CII slipper-pump cam ring', 'A noncircular inner track varies chamber volume as the rotor turns. The study uses an illustrative ellipse, not a recovered Ford cam profile.', '#7c868f'),
        'rotor': ('CII ten-pocket rotor', 'Carries ten spring-loaded slippers, as specified by the Ford assembly procedure. Pocket contour and shaft interface remain provisional.', '#a2abb2'),
        'rotor-clip': ('Rotor shaft retaining clip', 'Locates the rotor on its shaft. The C-clip and shaft groove fit are illustrative.', '#929ba2'),
        'upper-plate': ('Upper pressure plate', 'Closes the reservoir-side pumping chambers. Actual port timing and passages are unresolved.', '#969ea4'),
        'valve-cover': ('Pump valve cover', 'Closes the pressure cartridge and houses the flow-control bore. Internal drilled passages and the separate plastic baffle remain unfinished.', '#8f989f'),
        'valve-cover-seal': ('Valve-cover O-ring', 'Seals the cover inside the housing. Groove and compression are provisional.', '#353d43'),
        'cover-retaining-ring': ('Valve-cover retaining ring', 'Captures the compressed valve-cover stack in the housing groove. End position, section and tolerances are provisional.', '#909aa2'),
        'reservoir-seal': ('Reservoir interface seal · illustrative section', 'Separates the nylon reservoir from the front-plate joint. The simple annulus represents a seal region, not the production O-ring section.', '#353d43'),
        'flow-valve': ('Flow/relief valve assembly · unresolved interior', 'Controls pump delivery in conjunction with its spring and outlet. This spool-shaped assembly leaves relief internals and calibration unresolved.', '#a0a9af'),
        'flow-spring': ('Flow-control valve spring', 'Biases the flow valve. Coil shape is illustrative; preload and hydraulic calibration are not simulated.', '#9ca7af'),
        'outlet-fitting': ('Pressure outlet fitting', 'Retains the flow valve and connects the pressure hose. Ford describes a swiveling quick-connect hose joint; thread and quick-connect details remain unresolved.', '#a6aeb3'),
        'outlet-seal': ('Pressure outlet seal · illustrative', 'Seals the fitting at the reservoir wall. Exact seal count, profile and compression remain unresolved.', '#353d43'),
        'pulley': ('Power steering pulley · Ford belt study', 'Press-fit steel pulley using Dorman comparison OD and an inferred bore unit. Six illustrative grooves follow Ford belt seating instructions; Dorman five-groove metadata remains a recorded conflict.', '#30383f'),
    }
    result = {'ps-pump-' + identifier: values for identifier, values in labels.items()}
    for index in (1, 2):
        result[f'ps-pump-dowel-{index}'] = (f'Pump cartridge dowel {index}', 'Locates the pressure plates, cam and cover. Ford specifies two dowels; diameter and length are provisional.', '#a5afb5')
    for index in range(1, 11):
        result[f'ps-pump-slipper-{index}'] = (f'Pump slipper {index}', 'Slides in a rotor pocket against the cam track. Ten slippers are sourced; contour, track clearance and groove profile are illustrative.', '#a4afb8')
        result[f'ps-pump-slipper-spring-{index}'] = (f'Pump slipper spring {index}', 'Pushes its slipper toward the cam at low speed. Ford specifies one spring per pocket; coil dimensions and loading are illustrative.', '#999fa5')
    return result


def build(api):
    define, add, group = api
    group('power-steering-pump-assembly', 'Power steering pump · CII construction study', 'accessory-drive')
    labels = descriptions()
    for index, (identifier, shape) in enumerate(components().items()):
        name, function, color = labels[identifier]
        define(identifier, shape, name, function, 'accessory-drive', color, SOURCES, GAPS)
        center = shape.bounding_box().center()
        explode = (220 + 2 * (center.Z + 130), 140 + center.Y * 2, 70 - center.X * 2)
        add(identifier, identifier, 'power-steering-pump-assembly', POSITION, explode, ROTATION)
