# Headless Blender build: F-150 wheel + tire.
#   Tire:  P235/75R15 (28.9" OD, 9.25" section) — owner's likely size; brochure
#          lists P215/75R15SL std / P235/75R15XL opt. Confirm from photos.
#   Wheel: 15x6 argent steel, 5 on 5.5" bolt circle (brochure: "5-hole/6\" F-150"),
#          vent slots, dog-dish chrome cap.
# Axis: wheel axis along Blender Y, OUTBOARD face toward -Y (lands on viewer +Z;
# left-side records rotate [0,180,0], same convention as the old builder).
# Run:  /Applications/Blender.app/Contents/MacOS/Blender -b -P scripts/blender/wheel_tire.py

import bpy
import bmesh
import math
import os

OUT = os.path.join(os.path.dirname(__file__), '..', '..', 'models', 'wheel-tire.glb')
TAU = math.tau

bpy.ops.wm.read_factory_settings(use_empty=True)


def material(name, color, metallic, roughness):
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    b = m.node_tree.nodes['Principled BSDF']
    b.inputs['Base Color'].default_value = (*color, 1)
    b.inputs['Metallic'].default_value = metallic
    b.inputs['Roughness'].default_value = roughness
    return m


rubber = material('rubber', (0.032, 0.032, 0.036), 0.0, 0.93)
argent = material('argent', (0.62, 0.63, 0.64), 0.55, 0.42)
chromeM = material('chrome', (0.92, 0.93, 0.94), 1.0, 0.09)
zinc = material('zinc', (0.72, 0.73, 0.74), 0.95, 0.32)


def spin_profile(name, pts, mat, closed=False, thickness=0.0, steps=128):
    """Polyline profile (radius, axial) revolved around Y via Screw modifier."""
    me = bpy.data.meshes.new(name)
    bm = bmesh.new()
    vs = [bm.verts.new((x, y, 0)) for x, y in pts]
    for a, b in zip(vs, vs[1:]):
        bm.edges.new((a, b))
    if closed:
        bm.edges.new((vs[-1], vs[0]))
    bm.to_mesh(me)
    bm.free()
    ob = bpy.data.objects.new(name, me)
    bpy.context.collection.objects.link(ob)
    bpy.context.view_layer.objects.active = ob
    scr = ob.modifiers.new('screw', 'SCREW')
    scr.axis = 'Y'
    scr.angle = TAU
    scr.steps = steps
    scr.use_merge_vertices = True
    bpy.ops.object.modifier_apply(modifier='screw')
    if thickness:
        sol = ob.modifiers.new('thk', 'SOLIDIFY')
        sol.thickness = thickness
        bpy.ops.object.modifier_apply(modifier='thk')
    ob.data.materials.append(mat)
    ob.select_set(True)
    bpy.ops.object.shade_smooth_by_angle(angle=0.55)
    ob.select_set(False)
    return ob


# ---- tire: closed profile, circumferential tread grooves
R, BEAD = 14.45, 7.5
tread = [(R - 0.1, 3.1)]
for c in (2.0, 0.7, -0.7, -2.0):                      # grooves
    tread += [(R, c + 0.55), (R, c + 0.18), (R - 0.45, c + 0.10),
              (R - 0.45, c - 0.10), (R, c - 0.18)]
tread += [(R, -2.55), (R - 0.1, -3.1)]
prof = ([(BEAD, 3.55), (10.0, 4.4), (12.9, 4.62), (13.9, 3.95)] + tread +
        [(13.9, -3.95), (12.9, -4.62), (10.0, -4.4), (BEAD, -3.55)])
spin_profile('tire', prof, rubber, closed=True, steps=160)

# ---- steel wheel: barrel + disc (disc set outboard, ~3.75" backspacing)
barrel = [(7.9, 3.0), (7.45, 2.7), (7.3, 2.2), (6.5, 0.9),
          (6.5, -0.6), (7.3, -1.9), (7.45, -2.4), (7.9, -2.7)]
spin_profile('rim-barrel', barrel, argent, thickness=0.12)

disc = [(1.4, -2.6), (2.9, -2.6), (3.4, -2.3), (4.6, -2.05), (5.5, -1.5), (6.55, -1.1)]
disc_ob = spin_profile('wheel-disc', disc, argent, thickness=0.15)

# vent slots punched through the disc (ovals between the lugs and the rim)
for i in range(4):
    a = math.radians(45 + i * 90)
    bpy.ops.mesh.primitive_cylinder_add(radius=0.85, depth=3,
        location=(math.cos(a) * 5.0, -1.8, math.sin(a) * 5.0),
        rotation=(math.pi / 2, 0, 0))
    cut = bpy.context.view_layer.objects.active
    cut.scale = (1.0, 1.55, 1.0)
    bpy.ops.object.transform_apply(scale=True)
    bo = disc_ob.modifiers.new('cut', 'BOOLEAN')
    bo.operation = 'DIFFERENCE'
    bo.object = cut
    bpy.context.view_layer.objects.active = disc_ob
    bpy.ops.object.modifier_apply(modifier='cut')
    bpy.data.objects.remove(cut, do_unlink=True)

# ---- 5 lug nuts on the 5.5" bolt circle (r = 2.75)
for i in range(5):
    a = i * TAU / 5
    bpy.ops.mesh.primitive_cylinder_add(vertices=6, radius=0.39, depth=0.8,
        location=(math.cos(a) * 2.75, -2.85, math.sin(a) * 2.75),
        rotation=(math.pi / 2, 0, 0))
    bpy.context.view_layer.objects.active.data.materials.append(zinc)

# ---- dog-dish center cap
cap = [(0.01, -3.2), (1.2, -3.12), (1.9, -2.85), (2.2, -2.55)]
spin_profile('center-cap', cap, chromeM, thickness=0.08, steps=96)

os.makedirs(os.path.dirname(os.path.abspath(OUT)), exist_ok=True)
bpy.ops.export_scene.gltf(filepath=os.path.abspath(OUT), export_format='GLB')
print('WROTE', os.path.abspath(OUT))
