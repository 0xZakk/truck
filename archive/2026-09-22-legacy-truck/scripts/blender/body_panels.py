# Headless Blender build: crowned body panels — hood + cab roof.
# The flat extrusions read as boxes; real OBS panels carry a subtle crown
# (~1" center rise) that catches the studio light.
#   hood.glb     — 38x68, center crown, slopes to the nose, front edge rolls down.
#                  Record origin (80, 47, 0); local top surface ~z 0.
#   cab-roof.glb — 83x76.3 crowned panel. Record origin (3.5, 67.2, 0).
# Axes: Blender +X fwd, +Z up, +Y left. 1 BU = 1".
# Run:  /Applications/Blender.app/Contents/MacOS/Blender -b -P scripts/blender/body_panels.py

import bpy
import math
import os

MODELS = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'models'))


def clear():
    bpy.ops.wm.read_factory_settings(use_empty=True)


def paint():
    m = bpy.data.materials.new('paint')
    m.use_nodes = True
    b = m.node_tree.nodes['Principled BSDF']
    b.inputs['Base Color'].default_value = (0.93, 0.94, 0.95, 1)
    b.inputs['Metallic'].default_value = 0.0
    b.inputs['Roughness'].default_value = 0.3
    if 'Coat Weight' in b.inputs:           # Blender 4+/5 clearcoat naming
        b.inputs['Coat Weight'].default_value = 1.0
        b.inputs['Coat Roughness'].default_value = 0.12
    return m


def crowned_panel(name, length, width, zfunc, thickness=1.1, subx=26, suby=16):
    bpy.ops.mesh.primitive_grid_add(x_subdivisions=subx, y_subdivisions=suby, size=1)
    ob = bpy.context.view_layer.objects.active
    ob.name = name
    ob.scale = (length, width, 1)        # grid size=1 spans ±0.5, unlike cubes (±1)
    bpy.ops.object.transform_apply(scale=True)
    for v in ob.data.vertices:
        v.co.z = zfunc(v.co.x, v.co.y)
    sol = ob.modifiers.new('thk', 'SOLIDIFY')
    sol.thickness = thickness
    sol.offset = -1.0                       # surface is the TOP face
    bpy.ops.object.modifier_apply(modifier='thk')
    bv = ob.modifiers.new('bv', 'BEVEL')
    bv.width = 0.15
    bv.segments = 2
    bv.angle_limit = math.radians(50)
    bpy.ops.object.modifier_apply(modifier='bv')
    ob.data.materials.append(paint())
    ob.select_set(True)
    bpy.ops.object.shade_smooth_by_angle(angle=0.7)
    ob.select_set(False)
    return ob


# ---- hood: crown + front slope + nose roll-down
clear()
def hood_z(x, y):
    crown = 1.1 * (1 - (y / 34) ** 2)
    base = -0.05 * (x + 19)                 # gentle slope toward the nose
    if x > 15:                              # nose rolls down over the last 4"
        t = (x - 15) / 4
        base -= 1.6 * t * t
    return base + crown * (1 - 0.25 * max(0, (x - 10) / 9))
crowned_panel('hood', 38, 68, hood_z)
bpy.ops.export_scene.gltf(filepath=os.path.join(MODELS, 'hood.glb'), export_format='GLB')
print('WROTE hood.glb')

# ---- cab roof: doubly-crowned panel
clear()
def roof_z(x, y):
    return 1.2 * (1 - (y / 38.15) ** 2) * (1 - 0.35 * (x / 41.5) ** 2)
crowned_panel('cab-roof', 83, 76.3, roof_z)
bpy.ops.export_scene.gltf(filepath=os.path.join(MODELS, 'cab-roof.glb'), export_format='GLB')
print('WROTE cab-roof.glb')
