# Headless Blender build: 1994 F-150 chrome front bumper.
# Run:  /Applications/Blender.app/Contents/MacOS/Blender -b -P scripts/blender/front_bumper.py
#
# Conventions for all Blender part scripts in this repo:
#   - 1 Blender unit = 1 inch.
#   - Build with Blender +X = truck forward, +Z = up, +Y = truck LEFT.
#     The glTF exporter (Y-up) then lands the part in viewer part-local axes
#     (+X fwd, +Y up, +Z right) so records place it with scale 1, rotation 0.
#   - Origin = the part's record position (here: bumper center, [106, 20, 0]).
#   - Export one .glb into models/<part-id>.glb.

import bpy
import os

OUT = os.path.join(os.path.dirname(__file__), '..', '..', 'models', 'front-bumper.glb')

bpy.ops.wm.read_factory_settings(use_empty=True)


def material(name, color, metallic, roughness):
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    bsdf = m.node_tree.nodes['Principled BSDF']
    bsdf.inputs['Base Color'].default_value = (*color, 1)
    bsdf.inputs['Metallic'].default_value = metallic
    bsdf.inputs['Roughness'].default_value = roughness
    return m


chrome = material('chrome', (0.92, 0.93, 0.94), 1.0, 0.08)
dark = material('darkSteel', (0.18, 0.19, 0.21), 0.8, 0.5)

# ---- sweep path (top view): straight face bar, ends wrap back toward the truck
path = bpy.data.curves.new('bumperPath', 'CURVE')
path.dimensions = '3D'
path.resolution_u = 24
sp = path.splines.new('BEZIER')
sp.bezier_points.add(3)
# (x fwd, y left, z up) — ends at y ±34 swept back 7"
coords = [(-7, -34, 0), (0, -27, 0), (0, 27, 0), (-7, 34, 0)]
for bp, c in zip(sp.bezier_points, coords):
    bp.co = c
    bp.handle_left_type = bp.handle_right_type = 'AUTO'
path_obj = bpy.data.objects.new('bumperPath', path)
bpy.context.collection.objects.link(path_obj)

# ---- cross-section profile: 10" tall face, slight convex bulge, rolled lips
prof = bpy.data.curves.new('bumperProfile', 'CURVE')
prof.dimensions = '2D'
prof.resolution_u = 12
ps = prof.splines.new('BEZIER')
ps.bezier_points.add(4)
# profile local X = outward (bumper face direction), Y = up
ppts = [(-0.7, -5.0), (0.5, -3.6), (1.1, 0.0), (0.5, 3.6), (-0.7, 5.0)]
for bp, c in zip(ps.bezier_points, ppts):
    bp.co = (*c, 0)
    bp.handle_left_type = bp.handle_right_type = 'AUTO'
prof_obj = bpy.data.objects.new('bumperProfile', prof)
bpy.context.collection.objects.link(prof_obj)

path.bevel_mode = 'OBJECT'
path.bevel_object = prof_obj

# convert swept surface to mesh, give it sheet-metal thickness
bpy.context.view_layer.objects.active = path_obj
path_obj.select_set(True)
bpy.ops.object.convert(target='MESH')
bumper = bpy.context.view_layer.objects.active
bumper.name = 'front-bumper'
solid = bumper.modifiers.new('thk', 'SOLIDIFY')
solid.thickness = 0.14
bpy.ops.object.modifier_apply(modifier='thk')
bumper.data.materials.append(chrome)
bpy.ops.object.shade_smooth_by_angle(angle=0.6)

# ---- mounting brackets (dark steel, behind the bar)
for y in (-20, 20):
    bpy.ops.mesh.primitive_cube_add(location=(-3.4, y, -0.5))
    b = bpy.context.view_layer.objects.active
    b.scale = (2.6, 1.5, 2.2)
    bpy.ops.object.transform_apply(scale=True)
    b.data.materials.append(dark)

# profile curve is no longer needed
bpy.data.objects.remove(prof_obj, do_unlink=True)

os.makedirs(os.path.dirname(os.path.abspath(OUT)), exist_ok=True)
bpy.ops.export_scene.gltf(filepath=os.path.abspath(OUT), export_format='GLB')
print('WROTE', os.path.abspath(OUT))
