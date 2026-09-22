"""Evidence-tagged piston/rod study. All dimensions mm; +Z cylinder, +X pin axis.

Run .venv-cad/bin/python cad/engine/first_assembly.py from any directory.
Generates individual STEP/GLB parts, an assembled STEP, and occurrence manifest.
This is a provisional reconstruction; see inventory/engine/dimensions.json.
"""
from pathlib import Path
import json
import math
import build123d as b
import numpy as np
import trimesh

ROOT = Path(__file__).resolve().parents[2]
EVIDENCE = json.loads((ROOT / 'inventory/engine/dimensions.json').read_text())
P = {p['id']: p['value'] for p in EVIDENCE['claims']}
OUT = ROOT / 'models/engine'
STEP = ROOT / 'cad/engine/generated'


def cx(radius, length):
    return b.Rot(0, 90, 0) * b.Cylinder(radius, length)


def annulus(ro, ri, height):
    return b.Cylinder(ro, height) - b.Cylinder(ri, height + 2)


def split_ring(ro, ri, h, gap):
    return annulus(ro, ri, h) - b.Pos(0, ro, 0) * b.Box(gap, 2 * (ro-ri)+4, h+2)


def make_parts():
    bore = P['bore']
    pr = P['piston_diameter'] / 2
    ch, low = P['compression_height'], P['skirt_below_pin']
    total = ch + low
    piston = b.Pos(0, 0, (ch-low)/2) * b.Cylinder(pr, total)
    # Open underside, continuous skirt, and a crown with a separate D-shaped dish.
    cavity_top = ch - P['dish_depth'] - P['crown_wall']
    piston -= b.Pos(0, 0, (cavity_top-low-2)/2) * b.Cylinder(pr-P['skirt_wall'], cavity_top+low+2)
    for x in [-35, 35]:
        piston += b.Pos(x, 0, 0) * cx(P['pin_diameter']/2+5, 27)
    # Boss pads remain inside the piston envelope, including at the skirt sides.
    piston &= b.Pos(0,0,(ch-low)/2)*b.Cylinder(pr,total)
    piston -= cx(P['pin_diameter']/2+0.03, bore+4)
    dish = b.Cylinder(P['dish_radius'], P['dish_depth']+1)
    dish &= b.Pos(0, -15, 0) * b.Box(100, 70, 30)
    piston -= b.Pos(0, 0, ch-(P['dish_depth']-1)/2) * dish
    for station, width in [('top_ring_z', P['compression_ring_width']),
                           ('second_ring_z', P['compression_ring_width']),
                           ('oil_ring_z', P['oil_ring_pack_width'])]:
        cutter = annulus(pr+2, bore/2-P['ring_radial_depth']-0.5,
                         width+P['ring_groove_clearance'])
        piston -= b.Pos(0, 0, P[station]) * cutter

    journal = sum(P['rod_journal_diameter_range'])/2
    bearing_inner = journal/2 + P['rod_bearing_clearance']/2
    bearing_outer = bearing_inner + P['bearing_thickness']
    w, L = P['rod_width'], P['rod_length']
    ring = cx(P['rod_outer_radius'], w)
    # Forging silhouette is provisional; center distance remains an assumption.
    web = b.extrude(b.Plane.YZ * b.Polygon((-17, 4), (-8, L-8), (8, L-8), (17, 4), align=None), amount=w/2, both=True)
    rod_full = ring + web + b.Pos(0, 0, L)*cx(P['pin_diameter']/2+6, w)
    for y in [-P['bolt_spacing_half'], P['bolt_spacing_half']]:
        rod_full += b.Pos(0, y, 0)*b.Box(w, 14, 44)
    rod_full -= cx(bearing_outer, w+4)
    rod_full -= b.Pos(0, 0, L)*cx(P['pin_diameter']/2+0.01, w+4)
    for y in [-P['bolt_spacing_half'], P['bolt_spacing_half']]:
        rod_full -= b.Pos(0, y, 0)*b.Cylinder(P['bolt_diameter']/2+0.2, 80)
        rod_full -= b.Pos(0, y, 122)*b.Box(w+4, 14.1, 200)
        rod_full -= b.Pos(0, y, -122)*b.Box(w+4, 14.1, 200)
    rod = rod_full & b.Pos(0, 0, 150)*b.Box(200, 200, 300)
    cap = rod_full & b.Pos(0, 0, -100)*b.Box(200, 200, 200)
    shell = cx(bearing_outer, w-0.4) - cx(bearing_inner, w+2)
    upper = shell & b.Pos(0, 0, 50.02)*b.Box(200, 200, 100)
    lower = shell & b.Pos(0, 0, -50.02)*b.Box(200, 200, 100)
    bolt = b.Pos(0, 0, -4)*b.Cylinder(P['bolt_diameter']/2, 54)
    bolt += b.Pos(0, 0, 22)*b.extrude(b.RegularPolygon(7, 6), amount=5)
    nut = b.extrude(b.RegularPolygon(7, 6), amount=6)
    nut -= b.Pos(0, 0, 3)*b.Cylinder(P['bolt_diameter']/2, 10)
    pin = cx(P['pin_diameter']/2, P['pin_length']) - cx(P['pin_diameter']/2-P['pin_wall'], P['pin_length']+2)
    cr = bore/2
    compression = split_ring(cr, cr-P['ring_radial_depth'], P['compression_ring_width'], P['ring_end_gap'])
    rail = split_ring(cr, cr-P['ring_radial_depth'], P['oil_rail_width'], P['ring_end_gap'])
    expander = split_ring(cr-0.7, cr-P['ring_radial_depth'], P['oil_ring_pack_width']-2*P['oil_rail_width']-0.1, 1)
    # A pedagogical crank throw, intentionally distinguished from a real crankshaft.
    R = P['stroke']/2
    cheek = b.Pos(-24, 0, R/2)*b.Box(12, 36, R+30)
    throw = cheek + b.Pos(-34, 0, 0)*cx(24, 28) + b.Pos(0, 0, R)*cx(journal/2, 60)
    return {'piston': piston, 'pin': pin, 'compression-ring': compression,
            'oil-rail': rail, 'oil-expander': expander, 'rod': rod, 'rod-cap': cap,
            'upper-bearing': upper, 'lower-bearing': lower, 'rod-bolt': bolt,
            'rod-nut': nut, 'crank-throw-demo': throw}


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    STEP.mkdir(parents=True, exist_ok=True)
    parts = make_parts()
    colors = {'piston': '#c4cbd3', 'pin': '#a1b4c4', 'compression-ring': '#586b78',
              'oil-rail': '#bcaa76', 'oil-expander': '#917449', 'rod': '#8c9ba5',
              'rod-cap': '#71848e', 'upper-bearing': '#c9ad7a', 'lower-bearing': '#c9ad7a',
              'rod-bolt': '#526671', 'rod-nut': '#526671', 'crank-throw-demo': '#407c83'}
    definitions = []
    for key, shape in parts.items():
        shape.label = key
        if not shape.is_valid or shape.volume <= 0 or len(shape.solids()) != 1:
            raise ValueError(f'Invalid or disconnected physical definition: {key}')
        b.export_step(shape, STEP/f'{key}.step', unit=b.Unit.MM)
        vertices, faces = shape.tessellate(0.08, 0.15)
        # Explicit CAD Z-up -> glTF Y-up; mm -> standard glTF metres.
        xyz = np.array([[v.X, v.Z, -v.Y] for v in vertices]) / 1000
        mesh = trimesh.Trimesh(vertices=xyz, faces=faces, process=False)
        mesh.visual = trimesh.visual.TextureVisuals(material=trimesh.visual.material.PBRMaterial(
            baseColorFactor=trimesh.visual.color.hex_to_rgba(colors[key]), metallicFactor=0.65, roughnessFactor=0.32))
        scene = trimesh.Scene()
        scene.add_geometry(mesh, node_name=key, geom_name=key)
        (OUT/f'{key}.glb').write_bytes(scene.export(file_type='glb'))
        definitions.append({'id': key, 'glb': f'/models/engine/{key}.glb',
                            'step': f'/cad/engine/generated/{key}.step', 'color': colors[key],
                            'volume_mm3': shape.volume, 'solid_count': len(shape.solids()),
                            'geometry_status': 'schematic' if key == 'crank-throw-demo' else 'provisional',
                            'triangle_count': len(faces)})

    occurrences = []
    def add(id, definition, group, name, explanation, pos=(0, 0, 0), explode=(0, 0, 0)):
        occurrences.append({'id': id, 'definition': definition, 'parent': group,
                            'name': name, 'function': explanation, 'position_cad_mm': list(pos),
                            'explode_cad_mm': list(explode)})
    add('piston-1', 'piston', 'piston-group', 'Piston', 'Receives combustion force at the crown and transfers it through the wrist pin. D-shaped dish, underside and ring grooves are modeled; skirt profile and pin offset remain provisional.', explode=(0, 0, 65))
    for id, name, z, ex in [('top-ring-1', 'Top compression ring', P['top_ring_z'], 110), ('second-ring-1', 'Second compression ring', P['second_ring_z'], 90)]:
        add(id, 'compression-ring', 'piston-group', name, 'Seals combustion gases and transfers heat toward the bore. Individual split ring; exact section profile is not yet reconstructed.', (0, 0, z), (0, 0, ex))
    for i, sign in enumerate([1, -1]):
        add(f'oil-rail-{i+1}', 'oil-rail', 'piston-group', f'Oil-control rail {i+1}', 'One of two thin rails in the provisional three-piece oil-control pack.', (0, 0, P['oil_ring_z']+sign*(P['oil_ring_pack_width']-P['oil_rail_width'])/2), (0, 0, 65+sign*10))
    add('oil-expander-1', 'oil-expander', 'piston-group', 'Oil-ring expander', 'Loads the oil rails outward. A split band represents this component; actual corrugations and oil-drain windows remain unmodeled.', (0, 0, P['oil_ring_z']), (0, 0, 65))
    add('wrist-pin-1', 'pin', 'piston-group', 'Wrist pin', 'Connects piston and rod at their small-end joint. Retainer configuration and offset need confirmation.', explode=(100, 0, 0))
    add('connecting-rod-1', 'rod', 'rod-group', 'Connecting rod', 'Transfers force between wrist pin and crank journal. Its angle is solved from the mechanism; center distance and forging profile are provisional.', explode=(0, 0, 0))
    add('rod-cap-1', 'rod-cap', 'rod-group', 'Rod cap', 'Closes the big end around the crank journal and lower bearing shell.', explode=(0, 0, -80))
    add('rod-bearing-upper-1', 'upper-bearing', 'rod-group', 'Upper bearing shell', 'Supports the loaded side of the crank-journal interface. Separate from the rod forging.', explode=(65, 0, 20))
    add('rod-bearing-lower-1', 'lower-bearing', 'rod-group', 'Lower bearing shell', 'Fits inside the removable cap. Oil film is an explanation, not a fluid simulation.', explode=(65, 0, -40))
    for i, y in enumerate([-P['bolt_spacing_half'], P['bolt_spacing_half']]):
        add(f'rod-bolt-{i+1}', 'rod-bolt', 'rod-group', f'Rod bolt {i+1}', 'Clamps the cap to the rod. Smooth-shank placeholder; thread, grade and dimensions remain unverified.', (0, y, 0), (0, y, 65))
        add(f'rod-nut-{i+1}', 'rod-nut', 'rod-group', f'Rod nut {i+1}', 'Retains its cap bolt. Threads and locking details are not yet modeled.', (0, y, -28), (0, y, -100))
    add('crank-throw-context', 'crank-throw-demo', 'crank-group', 'Crank throw · schematic', 'Demonstrates the sourced stroke and journal diameter. This is a mechanism fixture, not a replica of the six-cylinder crankshaft.', explode=(-70, 0, 0))
    R, L = P['stroke']/2, P['rod_length']
    children = []
    for o in occurrences:
        x, y, z = o['position_cad_mm']
        z += {'piston-group': R+L, 'rod-group': R, 'crank-group': 0}[o['parent']]
        s = parts[o['definition']].moved(b.Location((x, y, z)))
        s.label = o['id']
        children.append(s)
    assembly = b.Compound(children=children)
    b.export_step(assembly, STEP/'first-assembly.step', unit=b.Unit.MM)
    manifest = {'schema_version': 1, 'title': 'Ford 4.9L · piston and rod study',
                'status': 'Provisional component study — not a complete or verified OEM engine',
                'coordinate_system': {'source': 'mm, +Z cylinder, +X pin axis', 'gltf': 'metres, Y-up', 'display_scale': 1000},
                'evidence': '/inventory/engine/dimensions.json', 'definitions': definitions,
                'assemblies': [{'id': 'study', 'parent': None}, {'id': 'piston-group', 'parent': 'study'}, {'id': 'rod-group', 'parent': 'study'}, {'id': 'crank-group', 'parent': 'study'}],
                'occurrences': occurrences, 'mechanism': {'stroke_mm': P['stroke'], 'rod_length_mm': L, 'pin_offset_mm': 0, 'model': 'idealized zero-offset slider crank', 'rod_length_verified': False},
                'omissions': ['Unconfirmed pin retainers', 'Exact pin offset', 'Exact rod forging and cap geometry', 'Fastener threads and specifications', 'Oil expander corrugations', 'Piston taper and ovality', 'Full crankshaft', 'Cylinder/block/head and remaining engine']}
    (ROOT/'inventory/engine/first-assembly.json').write_text(json.dumps(manifest, indent=2)+'\n')
    print(f'Exported {len(definitions)} valid single-solid definitions, {len(occurrences)} occurrences and assembled STEP')


if __name__ == '__main__':
    main()
