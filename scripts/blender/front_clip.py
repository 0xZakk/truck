# Headless Blender build: 1992-96 F-150 front clip.
#   front-panel.glb — argent header/grille panel: one molding with boolean openings
#                     for both headlamps, both parking lamps, and the grille; bar
#                     insert + Ford oval. Record origin (104, 36.5, 0).
#   headlamp.glb    — flush composite lamp (symmetric; same glb both sides).
#   corner-lamp.glb — amber parking/turn lamp below the headlamp.
# Axes: Blender +X fwd, +Z up, +Y left (glTF Y-up export -> viewer axes). 1 BU = 1".
# Run:  /Applications/Blender.app/Contents/MacOS/Blender -b -P scripts/blender/front_clip.py

import bpy
import math
import os

MODELS = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'models'))


def clear():
    bpy.ops.wm.read_factory_settings(use_empty=True)


def material(name, color, metallic, roughness):
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    b = m.node_tree.nodes['Principled BSDF']
    b.inputs['Base Color'].default_value = (*color, 1)
    b.inputs['Metallic'].default_value = metallic
    b.inputs['Roughness'].default_value = roughness
    return m


def cube(name, size, loc, mat=None):
    bpy.ops.mesh.primitive_cube_add(location=loc)
    ob = bpy.context.view_layer.objects.active
    ob.name = name
    ob.scale = (size[0] / 2, size[1] / 2, size[2] / 2)
    bpy.ops.object.transform_apply(scale=True)
    if mat:
        ob.data.materials.append(mat)
    return ob


def carve(target, cutter):
    bo = target.modifiers.new('cut', 'BOOLEAN')
    bo.operation = 'DIFFERENCE'
    bo.object = cutter
    bpy.context.view_layer.objects.active = target
    bpy.ops.object.modifier_apply(modifier='cut')
    bpy.data.objects.remove(cutter, do_unlink=True)


def bevel(ob, width=0.12):
    bv = ob.modifiers.new('bv', 'BEVEL')
    bv.width = width
    bv.segments = 2
    bv.angle_limit = math.radians(40)
    bpy.context.view_layer.objects.active = ob
    bpy.ops.object.modifier_apply(modifier='bv')


def export(name):
    bpy.ops.export_scene.gltf(filepath=os.path.join(MODELS, name), export_format='GLB')
    print('WROTE', name)


# ============================ FRONT PANEL ============================
clear()
argent = material('argent', (0.66, 0.67, 0.68), 0.55, 0.4)
dark = material('darkPl', (0.06, 0.065, 0.07), 0.1, 0.75)
chrome = material('chrome', (0.92, 0.93, 0.94), 1.0, 0.09)
blue = material('fordBlue', (0.03, 0.12, 0.42), 0.4, 0.3)

panel = cube('front-panel', (1.2, 62, 14), (0, 0, 0), argent)
# openings (panel local: z up around world 36.5, y across, x fwd)
carve(panel, cube('cutHL_L', (3, 12.5, 5.0), (0, 23.25, 3.0)))      # headlamp L (world z -23.25... mirrored by symmetry)
carve(panel, cube('cutHL_R', (3, 12.5, 5.0), (0, -23.25, 3.0)))     # headlamp R
carve(panel, cube('cutGrille', (3, 31, 10), (0, 0, 0.5)))           # grille opening
carve(panel, cube('cutPk_L', (3, 9, 3.5), (0, 23, -4.75)))          # parking lamp L
carve(panel, cube('cutPk_R', (3, 9, 3.5), (0, -23, -4.75)))         # parking lamp R
bevel(panel)

# grille insert: dark recess + argent bars
cube('recess', (0.5, 31, 10), (-0.8, 0, 0.5), dark)
for z in (-2.4, 0.5, 3.4):
    b = cube('barH', (0.8, 30.6, 0.9), (-0.1, 0, z), argent)
    bevel(b, 0.08)
for y in (-10.3, -5.15, 5.15, 10.3):
    b = cube('barV', (0.7, 0.7, 9.6), (-0.2, y, 0.5), argent)
    bevel(b, 0.08)

# Ford oval on the center bar intersection
bpy.ops.mesh.primitive_uv_sphere_add(segments=28, ring_count=16, location=(0.45, 0, 0.5))
oval = bpy.context.view_layer.objects.active
oval.scale = (0.35, 2.55, 1.0)
bpy.ops.object.transform_apply(scale=True)
oval.data.materials.append(blue)
bpy.ops.object.shade_smooth()
bpy.ops.mesh.primitive_torus_add(major_radius=1.0, minor_radius=0.16, location=(0.55, 0, 0.5),
                                 rotation=(0, math.radians(90), 0))
ring = bpy.context.view_layer.objects.active
ring.scale = (1, 2.55, 1.0)
bpy.ops.object.transform_apply(scale=True)
ring.data.materials.append(chrome)
bpy.ops.object.shade_smooth()
export('front-panel.glb')

# ============================ HEADLAMP ============================
clear()
chrome = material('chrome', (0.92, 0.93, 0.94), 1.0, 0.09)
lensM = material('lamp', (0.88, 0.9, 0.93), 0.9, 0.12)
darkH = material('housing', (0.1, 0.1, 0.11), 0.2, 0.6)

cube('housing', (2.4, 11.9, 4.4), (-0.7, 0, 0), darkH)
bz = cube('bezel', (0.5, 12.1, 4.6), (0.35, 0, 0), chrome)
carve(bz, cube('bzCut', (1.0, 11.1, 3.6), (0.35, 0, 0)))
bevel(bz, 0.08)
lens = cube('lens', (0.6, 11.2, 3.7), (0.3, 0, 0), lensM)
# vertical fresnel flutes
for i in range(11):
    y = -5.0 + i * 1.0
    cube('flute', (0.12, 0.18, 3.5), (0.62, y, 0), lensM)
bevel(lens, 0.06)
export('headlamp.glb')

# ============================ CORNER / PARKING LAMP ============================
clear()
amber = material('amber', (0.95, 0.45, 0.04), 0.3, 0.18)
darkH = material('housing', (0.1, 0.1, 0.11), 0.2, 0.6)
cube('housing', (1.8, 8.4, 3.0), (-0.5, 0, 0), darkH)
al = cube('lens', (0.7, 8.6, 3.2), (0.35, 0, 0), amber)
bevel(al, 0.1)
for i in range(7):
    y = -3.4 + i * 1.13
    cube('rib', (0.1, 0.16, 3.0), (0.72, y, 0), amber)
export('corner-lamp.glb')
