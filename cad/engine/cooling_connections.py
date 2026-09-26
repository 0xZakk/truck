"""Connected heater takeoffs and two-wire ECT study; vehicle hoses unresolved."""
import build123d as b

PUMP_POSITION = (440, 0, 170)
ECT_POSITION = (464, 34, 285)
SUPPLY_ENDPOINT = (488, -57, 335)
RETURN_ENDPOINT = (438, -100, 270)
SOURCES = ['ford-cooling-connections', 'ford-ect-construction', 'ford-cooling-sensor-circuits',
           'gates-1994-drive', 'truck-cooling-hose-photos']
GAPS = [
    'Ford identifies the two-lead ECT at the thermostat housing/heater elbow and specifies 3/8-18 NPTF-SPL dry-seal thread. All sensor dimensions, internal thermistor shape and connector detail are provisional.',
    'A separate single-wire gauge sender C150 on the RH engine side feeds circuit 39 R/W and grounds through its body. It is not the ECT C183. Gauge sender mounting and the head coolant jacket remain unresolved; no false dry pocket is presented as a coolant connection.',
    'Both heater connections use Gates 18767 in the five-speed manual application. Exact hose end assignment, bore, installed cut length and routing are not established here; metal tubes, radii, beads and clearances are illustrative.',
    'Owner photos show paired red-orange heater hoses crossing from the firewall toward the front engine. Only attached engine-side metal takeoffs are modeled; full heater/radiator hoses need located vehicle endpoints.',
    'The thermostat-side elbow opens into the existing secondary outlet passage; the pump return opens into its existing coolant chamber. Pump/block and outlet/head jacket connections remain incomplete.',
    'Ford TSB 94-9-13 describes an E4OD-only radiator bleed tee. That automatic-transmission arrangement is not applied to this manual truck.',
    'Thread helices, tapered sealing fits, hose deformation, clamps, harness connectors and coolant/temperature simulation are absent. Sensor resistor and leads are a construction study, not a rebuild procedure.'
]


def cylinder(radius, length, center, direction=(0, 0, 1)):
    start = tuple(center[index] - direction[index] * length / 2 for index in range(3))
    return b.Solid.make_cylinder(radius, length, b.Plane(origin=start, z_dir=direction))


def supply_path():
    return b.Wire([
        b.Edge.make_line((442, 28, 265), (473, 28, 265)),
        b.Edge.make_three_point_arc((473, 28, 265), (483.6066017, 23.6066017, 265), (488, 13, 265)),
        b.Edge.make_line((488, 13, 265), (488, -37, 265)),
        b.Edge.make_three_point_arc((488, -37, 265), (488, -51.1421356, 270.8578644), (488, -57, 285)),
        b.Edge.make_line((488, -57, 285), SUPPLY_ENDPOINT)
    ])


def return_path():
    return b.Wire([
        b.Edge.make_line((438, -60, 185), (438, -80, 185)),
        b.Edge.make_three_point_arc((438, -80, 185), (438, -94.1421356, 190.8578644), (438, -100, 205)),
        b.Edge.make_line((438, -100, 205), RETURN_ENDPOINT)
    ])


def supply_sweep(radius):
    return b.sweep(b.Plane(origin=(442, 28, 265), z_dir=(1, 0, 0)) * b.Circle(radius), supply_path())


def return_sweep(radius):
    return b.sweep(b.Plane(origin=(438, -60, 185), z_dir=(0, -1, 0)) * b.Circle(radius), return_path())


def supply_elbow():
    shape = supply_sweep(8)
    shape += cylinder(10.8, 23, (453.5, 28, 265), (1, 0, 0))
    shape += cylinder(12, 20, (ECT_POSITION[0], ECT_POSITION[1], 275))
    shape += cylinder(8.5, 2, (488, -57, 331))
    shape -= supply_sweep(6.5)
    shape -= cylinder(8.6, 23, (ECT_POSITION[0], ECT_POSITION[1], 275))
    return shape


def return_elbow():
    shape = return_sweep(8)
    shape += cylinder(8.5, 2, (438, -100, 266))
    return shape - return_sweep(6.5)


def pump_housing_interface(shape):
    passage = cylinder(8.1, 26, (-2, -67, 15), (0, -1, 0))
    return shape - passage


def ect_body():
    shape = cylinder(4.5, 18, (0, 0, -9)) + cylinder(8.5, 12, (0, 0, -6))
    shape += b.extrude(b.RegularPolygon(11.5, 6), amount=5)
    return shape - cylinder(3, 22, (0, 0, -5))


def ect_insulator():
    shape = cylinder(8.3, 18, (0, 0, 14))
    shape -= cylinder(4.5, 16, (0, 0, 12))
    for horizontal in (-1.5, 1.5):
        shape -= cylinder(.85, 5, (horizontal, 0, 21.5))
    return shape


def ect_terminal():
    return cylinder(.4, 34, (0, 0, 4)) + cylinder(.8, 9, (0, 0, 16.5))


def components():
    return {
        'heater-supply-ect-elbow': supply_elbow(),
        'heater-pump-return-elbow': return_elbow(),
        'engine-coolant-temperature-body': ect_body(),
        'engine-coolant-temperature-insulator': ect_insulator(),
        'engine-coolant-temperature-thermistor': cylinder(2.5, 3, (0, 0, -14.5)),
        'engine-coolant-temperature-terminal': ect_terminal()
    }


def placements():
    return [
        ('heater-supply-ect-elbow', 'heater-supply-ect-elbow', (0, 0, 0)),
        ('heater-pump-return-elbow', 'heater-pump-return-elbow', (0, 0, 0)),
        ('engine-coolant-temperature-body', 'engine-coolant-temperature-body', ECT_POSITION),
        ('engine-coolant-temperature-insulator', 'engine-coolant-temperature-insulator', ECT_POSITION),
        ('engine-coolant-temperature-thermistor', 'engine-coolant-temperature-thermistor', ECT_POSITION),
        ('engine-coolant-temperature-terminal-1', 'engine-coolant-temperature-terminal', (ECT_POSITION[0] - 1.5, ECT_POSITION[1], ECT_POSITION[2])),
        ('engine-coolant-temperature-terminal-2', 'engine-coolant-temperature-terminal', (ECT_POSITION[0] + 1.5, ECT_POSITION[1], ECT_POSITION[2]))
    ]


def parts():
    shapes = components()
    return {identifier: b.Pos(*position) * shapes[definition] for identifier, definition, position in placements()}


def flow_probes():
    return {
        'heater-supply-bore': supply_sweep(.7),
        'heater-return-bore': return_sweep(.7),
        'pump-chamber-to-return': cylinder(.7, 14, (438, -59, 185), (0, -1, 0)),
        'outlet-secondary-to-supply': cylinder(.7, 14, (441, 28, 265), (1, 0, 0))
    }


DESCRIPTIONS = {
    'heater-supply-ect-elbow': ('Heater supply and ECT elbow', 'Connects the thermostat-side coolant passage to the engine-side heater supply endpoint and exposes the ECT probe to coolant. Bend shape and all dimensions are provisional.', '#8e9894'),
    'heater-pump-return-elbow': ('Heater return tube at water pump', 'Returns heater coolant through an opened passage into the existing pump chamber. The open upper end is a vehicle-interface endpoint, not an installed hose.', '#939c96'),
    'engine-coolant-temperature-body': ('ECT sensor metal body', 'Conducts coolant temperature to an internal NTC thermistor. Ford specifies a two-lead ECT with 3/8-18 NPTF-SPL dry-seal thread; the modeled thread envelope and probe dimensions are illustrative.', '#b69559'),
    'engine-coolant-temperature-insulator': ('ECT sensor connector insulator', 'Separates the two terminals from the metal sensor body. Connector shape, keying and sealing details remain provisional.', '#405446'),
    'engine-coolant-temperature-thermistor': ('ECT sensing thermistor · envelope', 'Decreases resistance as coolant temperature rises, changing the PCM input. Shape, encapsulation and thermal interface are illustrative.', '#635950'),
    'engine-coolant-temperature-terminal': ('ECT terminal and internal lead', 'One of two independent conductors: ECT signal and sensor return. This sensor does not use its body as the circuit return; exact connector geometry is unresolved.', '#b6a170')
}


def build(api):
    define, add, group = api
    group('cooling-connections', 'Heater connections and ECT · interface study', 'cooling')
    group('engine-coolant-temperature-assembly', 'PCM coolant temperature sensor · two-lead ECT', 'cooling-connections')
    for identifier, shape in components().items():
        name, description, color = DESCRIPTIONS[identifier]
        define(identifier, shape, name, description, 'cooling', color, SOURCES, GAPS)
    for index, (identifier, definition, position) in enumerate(placements()):
        parent = 'engine-coolant-temperature-assembly' if identifier.startswith('engine-coolant-temperature') else 'cooling-connections'
        add(identifier, definition, parent, position, (130, -80 if index < 2 else 0, 80 + 35 * index))
