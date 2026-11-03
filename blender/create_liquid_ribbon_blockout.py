"""Create the first Liquid Ribbon animation blockout.

This is an art-direction prototype, not a final photoreal render. It keeps the
approved 18-second timing, the S-shaped ingredient arrangement, the jug handoff
and the diagonal pour in one editable Blender scene.

Run from the project root:
  blender -b --python blender/create_liquid_ribbon_blockout.py
"""
import math
from pathlib import Path

import bpy
from mathutils import Vector

ROOT = Path(__file__).resolve().parent.parent
SCENE_FILE = ROOT / "liquid-ribbon-blockout-v1.blend"
RENDER_DIR = ROOT / "renders" / "liquid-ribbon-blockout"
RENDER_DIR.mkdir(parents=True, exist_ok=True)


def set_input(node, names, value):
    for name in names:
        socket = node.inputs.get(name)
        if socket is not None:
            socket.default_value = value
            return


def material(name, color, roughness=0.35, metallic=0.0, transmission=0.0, alpha=1.0):
    mat = bpy.data.materials.new(name)
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes.get("Principled BSDF")
    set_input(bsdf, ("Base Color",), (*color, 1.0))
    set_input(bsdf, ("Roughness",), roughness)
    set_input(bsdf, ("Metallic",), metallic)
    set_input(bsdf, ("Transmission Weight", "Transmission"), transmission)
    set_input(bsdf, ("Alpha",), alpha)
    if alpha < 1:
        mat.surface_render_method = "DITHERED"
    return mat


def aim_at(obj, point):
    obj.rotation_euler = (Vector(point) - obj.location).to_track_quat("-Z", "Y").to_euler()


def key(obj, frame, location=None, rotation=None, scale=None):
    if location is not None:
        obj.location = location
        obj.keyframe_insert(data_path="location", frame=frame)
    if rotation is not None:
        obj.rotation_euler = rotation
        obj.keyframe_insert(data_path="rotation_euler", frame=frame)
    if scale is not None:
        obj.scale = scale
        obj.keyframe_insert(data_path="scale", frame=frame)


def smooth_animation(obj):
    if not obj.animation_data or not obj.animation_data.action:
        return
    action = obj.animation_data.action
    # Blender 5.2's layered Action API no longer exposes legacy fcurves here;
    # keyed properties already use the desired Bezier default in that mode.
    if not hasattr(action, "fcurves"):
        return
    for fc in action.fcurves:
        for point in fc.keyframe_points:
            point.interpolation = "BEZIER"


def apply_material(obj, mat):
    obj.data.materials.append(mat)
    if hasattr(obj.data, "polygons"):
        for poly in obj.data.polygons:
            poly.use_smooth = True
    return obj


def sphere(name, location, scale, mat, segments=48, rings=24):
    bpy.ops.mesh.primitive_uv_sphere_add(segments=segments, ring_count=rings, location=location)
    obj = bpy.context.object
    obj.name = name
    obj.scale = scale
    apply_material(obj, mat)
    bevel = obj.modifiers.new("Soft fruit edge", "BEVEL")
    bevel.width = 0.012
    bevel.segments = 2
    return obj


def cube(name, location, scale, mat, bevel=0.04, rotation=(0, 0, 0)):
    bpy.ops.mesh.primitive_cube_add(location=location, rotation=rotation)
    obj = bpy.context.object
    obj.name = name
    obj.scale = scale
    apply_material(obj, mat)
    edge = obj.modifiers.new("Soft cut edge", "BEVEL")
    edge.width = bevel
    edge.segments = 4
    obj.modifiers.new("Weighted normals", "WEIGHTED_NORMAL")
    return obj


def cylinder(name, location, radius, depth, mat, vertices=64):
    bpy.ops.mesh.primitive_cylinder_add(vertices=vertices, radius=radius, depth=depth, location=location)
    obj = bpy.context.object
    obj.name = name
    apply_material(obj, mat)
    edge = obj.modifiers.new("Soft edge", "BEVEL")
    edge.width = 0.018
    edge.segments = 3
    return obj


def torus(name, location, major, minor, mat, rotation=(0, 0, 0)):
    bpy.ops.mesh.primitive_torus_add(major_radius=major, minor_radius=minor, major_segments=64, minor_segments=16, location=location, rotation=rotation)
    obj = bpy.context.object
    obj.name = name
    apply_material(obj, mat)
    return obj


def curve(name, points, radius, mat, resolution=18):
    data = bpy.data.curves.new(name, "CURVE")
    data.dimensions = "3D"
    data.resolution_u = resolution
    data.bevel_depth = radius
    data.bevel_resolution = 5
    spline = data.splines.new("BEZIER")
    spline.bezier_points.add(len(points) - 1)
    for point, coords in zip(spline.bezier_points, points):
        point.co = coords
        point.handle_left_type = "AUTO"
        point.handle_right_type = "AUTO"
    obj = bpy.data.objects.new(name, data)
    bpy.context.collection.objects.link(obj)
    data.materials.append(mat)
    return obj


def parent_keep_world(obj, parent):
    world = obj.matrix_world.copy()
    obj.parent = parent
    obj.matrix_world = world


def area_light(name, location, energy, size, color, target):
    data = bpy.data.lights.new(name, "AREA")
    data.energy = energy
    data.shape = "DISK"
    data.size = size
    data.color = color
    obj = bpy.data.objects.new(name, data)
    bpy.context.collection.objects.link(obj)
    obj.location = location
    aim_at(obj, target)
    return obj


def set_visibility_keys(obj, visible_at, end=180):
    key(obj, 1, scale=(0.001, 0.001, 0.001))
    key(obj, visible_at, scale=(1, 1, 1))
    key(obj, end, scale=(1, 1, 1))


# Start from an empty scene so this prototype remains independent of the kiwi work.
bpy.ops.wm.read_factory_settings(use_empty=True)
scene = bpy.context.scene
scene.frame_start = 1
scene.frame_end = 180
scene.render.fps = 24
scene.render.engine = "BLENDER_EEVEE"
scene.render.resolution_x = 560
scene.render.resolution_y = 360
scene.render.resolution_percentage = 100
scene.render.image_settings.file_format = "PNG"
scene.render.film_transparent = False  # inspection background only; production alpha is documented separately
scene.render.image_settings.color_mode = "RGBA"
scene.render.filepath = str(RENDER_DIR / "frame-001.png")
scene.render.engine = "BLENDER_EEVEE"

world = bpy.data.worlds.new("Liquid Ribbon · preview world")
scene.world = world
world.use_nodes = True
world.node_tree.nodes["Background"].inputs["Color"].default_value = (0.012, 0.018, 0.018, 1)
world.node_tree.nodes["Background"].inputs["Strength"].default_value = 0.18

# Materials: deliberately simple blockout materials with readable silhouette.
pineapple_mat = material("Fruit · pineapple", (0.95, 0.53, 0.08), 0.38)
papaya_mat = material("Fruit · papaya", (0.96, 0.36, 0.18), 0.33)
coconut_shell_mat = material("Fruit · coconut shell", (0.19, 0.09, 0.045), 0.62)
coconut_flesh_mat = material("Fruit · coconut flesh", (0.94, 0.90, 0.72), 0.4)
banana_mat = material("Fruit · banana", (0.88, 0.68, 0.14), 0.36)
cherry_mat = material("Fruit · cherry", (0.52, 0.035, 0.045), 0.24)
grape_mat = material("Fruit · grape", (0.20, 0.07, 0.30), 0.28)
lime_mat = material("Fruit · lime", (0.33, 0.72, 0.15), 0.32)
stem_mat = material("Fruit · stems", (0.18, 0.09, 0.035), 0.6)
ribbon_mat = material("Liquid · golden peach ribbon", (0.92, 0.34, 0.08), 0.16, transmission=0.12)
liquid_mat = material("Liquid · golden peach", (0.88, 0.30, 0.075), 0.22, transmission=0.2)
glass_mat = material("Glass · clear studio", (0.72, 0.88, 0.90), 0.12, transmission=0.35)
highlight_mat = material("Glass · rim highlight", (0.55, 0.86, 0.88), 0.16, transmission=0.2)

# Camera: fixed composition with a small final approach.
bpy.ops.object.camera_add(location=(0, -8.6, 2.25))
camera = bpy.context.object
camera.name = "Camera · Liquid Ribbon master"
camera.data.lens = 52
camera.data.sensor_width = 36
aim_at(camera, (0.10, 0, 1.85))
scene.camera = camera
key(camera, 1, location=(0, -12.2, 2.55))
key(camera, 150, location=(0, -12.2, 2.55))
key(camera, 180, location=(0, -11.7, 2.55))
for frame in (1, 150, 180):
    camera.keyframe_insert(data_path="rotation_euler", frame=frame)

# Invisible studio lights: the render is still an empty-space composition.
area_light("Key · softbox", (-3.8, -4.2, 6.0), 900, 4.5, (1.0, 0.82, 0.65), (0, 0, 1.6))
area_light("Rim · cool edge", (4.0, 0.8, 4.7), 1100, 3.0, (0.54, 0.8, 1.0), (0.6, 0, 1.6))
area_light("Fill · front", (0, -4.5, 1.2), 450, 3.5, (1.0, 0.66, 0.44), (0, 0, 1.2))

# Glass anchor, lower-left. Its liquid is a separate object so the level can rise.
glass_group = bpy.data.objects.new("Glass · hero rig", None)
bpy.context.collection.objects.link(glass_group)
glass_group.location = (-1.05, 0.0, 0.68)
glass_body = cylinder("Glass · clear tumbler", (0, 0, 0.52), 0.55, 1.05, glass_mat)
glass_body.scale = (1.0, 0.86, 1.0)
glass_body.parent = glass_group
glass_body.hide_render = True  # the blockout uses a readable rim/outline; final glass is a material pass
glass_rim = torus("Glass · rim", (0, 0, 1.04), 0.48, 0.022, highlight_mat)
glass_rim.scale.y = 0.86
glass_rim.parent = glass_group
glass_base = torus("Glass · base rim", (0, 0, 0.03), 0.43, 0.02, highlight_mat)
glass_base.scale.y = 0.86
glass_base.parent = glass_group
glass_left = curve("Glass · left outline", [(-0.49, 0, 0.06), (-0.53, 0, 0.52), (-0.48, 0, 1.04)], 0.018, highlight_mat, resolution=8)
glass_left.parent = glass_group
glass_right = curve("Glass · right outline", [(0.49, 0, 0.06), (0.53, 0, 0.52), (0.48, 0, 1.04)], 0.018, highlight_mat, resolution=8)
glass_right.parent = glass_group
glass_liquid = cylinder("Glass · rising drink", (0, 0, 0.18), 0.46, 0.70, liquid_mat)
glass_liquid.scale.y = 0.86
glass_liquid.parent = glass_group
key(glass_liquid, 1, scale=(1, 1, 0.001))
key(glass_liquid, 112, scale=(1, 1, 0.03))
key(glass_liquid, 142, scale=(1, 1, 0.52))
key(glass_liquid, 158, scale=(1, 1, 0.78))
key(glass_liquid, 180, scale=(1, 1, 0.78))

# Opening ingredient arrangement: a loose S that foreshadows the ribbon.
ingredients = []

pineapple = cube("Ingredient · pineapple wedge", (-2.45, 0.05, 2.80), (0.38, 0.23, 0.62), pineapple_mat, bevel=0.14, rotation=(0.0, 0.08, -0.34))
ingredients.append(pineapple)

papaya = torus("Ingredient · papaya crescent", (-0.65, 0.0, 3.32), 0.45, 0.18, papaya_mat, rotation=(math.radians(78), 0, math.radians(18)))
ingredients.append(papaya)
for idx, x in enumerate((-0.82, -0.66, -0.50)):
    seed = sphere(f"Papaya seed {idx+1}", (x, -0.17, 3.35), (0.045, 0.04, 0.045), cherry_mat, 20, 12)
    ingredients.append(seed)

coconut = sphere("Ingredient · open coconut shell", (1.05, 0.06, 2.95), (0.56, 0.34, 0.52), coconut_shell_mat)
coconut_inner = sphere("Ingredient · coconut flesh", (1.05, -0.22, 3.02), (0.40, 0.10, 0.37), coconut_flesh_mat)
ingredients.extend((coconut, coconut_inner))

banana = curve("Ingredient · peeled banana", [(1.85, 0.02, 2.35), (2.06, 0.0, 2.62), (2.22, 0.0, 2.84), (2.05, 0.0, 3.04)], 0.16, banana_mat)
ingredients.append(banana)

for idx, (x, z) in enumerate(((0.25, 2.18), (0.54, 2.05), (0.48, 2.33))):
    cherry = sphere(f"Ingredient · cherry {idx+1}", (x, 0.02, z), (0.15, 0.15, 0.15), cherry_mat)
    stem = curve(f"Cherry stem {idx+1}", [(x, 0.02, z + 0.12), (x + 0.05, 0.01, z + 0.30)], 0.018, stem_mat, resolution=10)
    ingredients.extend((cherry, stem))

for idx, (x, z) in enumerate(((1.02, 1.95), (1.25, 2.10), (1.35, 1.87), (1.12, 2.30), (1.47, 2.22))):
    grape = sphere(f"Ingredient · grape {idx+1}", (x, 0.0, z), (0.13, 0.13, 0.13), grape_mat)
    ingredients.append(grape)

lime = sphere("Ingredient · lime half", (2.15, 0.02, 1.58), (0.42, 0.16, 0.42), lime_mat)
ingredients.append(lime)

for obj in ingredients:
    key(obj, 1, scale=(1, 1, 1))
    key(obj, 72, scale=(1, 1, 1))
    key(obj, 104, scale=(0.03, 0.03, 0.03))
    key(obj, 150, scale=(0.001, 0.001, 0.001))
    key(obj, 180, scale=(0.001, 0.001, 0.001))
    smooth_animation(obj)

# Fruit-specific strands emerge from the S arrangement into the shared ribbon.
strand_specs = [
    ("Strand · pineapple", [(-2.3, 0.03, 2.8), (-1.75, -0.02, 2.45), (-1.15, 0.0, 2.28), (-0.45, 0.0, 2.15)], 0.10, pineapple_mat),
    ("Strand · papaya", [(-0.65, 0.02, 3.2), (-0.40, 0.0, 2.70), (-0.08, 0.0, 2.34), (0.42, 0.0, 2.12)], 0.095, papaya_mat),
    ("Strand · coconut", [(1.02, 0.02, 2.98), (0.80, 0.0, 2.65), (0.58, 0.0, 2.34), (0.42, 0.0, 2.12)], 0.085, coconut_flesh_mat),
    ("Strand · banana", [(2.0, 0.0, 2.70), (1.55, 0.0, 2.45), (1.0, 0.0, 2.22), (0.42, 0.0, 2.12)], 0.08, banana_mat),
    ("Strand · cherry", [(0.40, 0.0, 2.22), (0.56, 0.0, 2.12), (0.68, 0.0, 2.03), (0.74, 0.0, 1.96)], 0.055, cherry_mat),
    ("Strand · grape", [(1.18, 0.0, 2.10), (0.98, 0.0, 2.02), (0.80, 0.0, 1.94), (0.74, 0.0, 1.96)], 0.05, grape_mat),
    ("Strand · lime", [(2.12, 0.0, 1.64), (1.70, 0.0, 1.74), (1.25, 0.0, 1.86), (0.74, 0.0, 1.96)], 0.06, lime_mat),
]
for name, points, radius, mat in strand_specs:
    obj = curve(name, points, radius, mat)
    key(obj, 1, scale=(0.001, 0.001, 0.001))
    key(obj, 42, scale=(0.001, 0.001, 0.001))
    key(obj, 78, scale=(1, 1, 1))
    key(obj, 112, scale=(1, 1, 1))
    key(obj, 150, scale=(0.001, 0.001, 0.001))
    key(obj, 180, scale=(0.001, 0.001, 0.001))
    smooth_animation(obj)

# One broad signature ribbon and its handoff into the jug.
main_ribbon = curve("Ribbon · signature curl", [(-0.48, 0.0, 2.12), (0.00, 0.0, 2.30), (0.75, 0.0, 2.46), (1.35, 0.0, 2.28), (1.60, 0.0, 1.92), (1.35, 0.0, 1.65)], 0.18, ribbon_mat)
key(main_ribbon, 1, scale=(0.001, 0.001, 0.001))
key(main_ribbon, 70, scale=(0.001, 0.001, 0.001))
key(main_ribbon, 86, scale=(1, 1, 1))
key(main_ribbon, 112, scale=(1, 1, 1))
key(main_ribbon, 180, scale=(0.001, 0.001, 0.001))

# Jug rig and reservoir, introduced before it tilts so the handoff is readable.
jug_rig = bpy.data.objects.new("Jug · pour rig", None)
bpy.context.collection.objects.link(jug_rig)
jug_rig.location = (1.82, 0.1, 2.90)
jug_body = sphere("Jug · clear body", (0, 0, 0), (0.72, 0.45, 0.88), glass_mat)
jug_body.parent = jug_rig
jug_neck = cylinder("Jug · neck", (0, -0.02, 0.78), 0.28, 0.42, glass_mat)
jug_neck.parent = jug_rig
jug_lip = torus("Jug · lip", (0, -0.02, 1.01), 0.28, 0.025, highlight_mat)
jug_lip.parent = jug_rig
jug_handle = torus("Jug · handle", (0.58, 0.03, 0.25), 0.37, 0.055, highlight_mat, rotation=(math.radians(90), 0, 0))
jug_handle.parent = jug_rig
jug_reservoir = sphere("Jug · liquid reservoir", (0, 0.0, 0.03), (0.60, 0.36, 0.42), liquid_mat)
jug_reservoir.parent = jug_rig
key(jug_rig, 1, scale=(0.001, 0.001, 0.001), rotation=(0, 0, 0))
key(jug_rig, 84, scale=(0.001, 0.001, 0.001), rotation=(0, 0, 0))
key(jug_rig, 98, scale=(1, 1, 1), rotation=(0, 0, 0))
key(jug_rig, 112, scale=(1, 1, 1), rotation=(0, math.radians(-8), 0))
key(jug_rig, 145, scale=(1, 1, 1), rotation=(0, math.radians(-24), 0))
key(jug_rig, 163, scale=(0.001, 0.001, 0.001), rotation=(0, math.radians(-24), 0))
key(jug_rig, 180, scale=(0.001, 0.001, 0.001), rotation=(0, math.radians(-24), 0))
smooth_animation(jug_rig)

handoff = curve("Ribbon · into jug", [(1.32, 0.0, 2.10), (1.55, 0.0, 2.48), (1.72, 0.04, 2.86), (1.82, 0.08, 3.33)], 0.14, ribbon_mat)
key(handoff, 1, scale=(0.001, 0.001, 0.001))
key(handoff, 88, scale=(0.001, 0.001, 0.001))
key(handoff, 104, scale=(1, 1, 1))
key(handoff, 120, scale=(1, 1, 1))
key(handoff, 150, scale=(0.001, 0.001, 0.001))
smooth_animation(handoff)

# Diagonal pour stream and a quiet lime garnish for the hero.
pour = curve("Liquid · continuous pour", [(1.80, 0.06, 3.08), (1.52, -0.02, 2.42), (0.92, -0.03, 1.72), (-0.98, -0.02, 1.28)], 0.12, liquid_mat)
key(pour, 1, scale=(0.001, 0.001, 0.001))
key(pour, 112, scale=(0.001, 0.001, 0.001))
key(pour, 122, scale=(1, 1, 1))
key(pour, 148, scale=(1, 1, 1))
key(pour, 158, scale=(0.46, 0.46, 0.46))
key(pour, 170, scale=(0.001, 0.001, 0.001))
key(pour, 180, scale=(0.001, 0.001, 0.001))
smooth_animation(pour)

garnish = torus("Hero · lime wheel", (-1.05, -0.06, 1.18), 0.16, 0.035, lime_mat, rotation=(math.radians(90), 0, 0))
key(garnish, 1, scale=(0.001, 0.001, 0.001))
key(garnish, 148, scale=(0.001, 0.001, 0.001))
key(garnish, 160, scale=(1, 1, 1))
key(garnish, 180, scale=(1, 1, 1))

# Helpful scene metadata for the next pass.
scene["prototype"] = "liquid-ribbon"
scene["status"] = "18-second blockout; not final media"
scene["timing"] = "24fps / 180 frames"
scene["transparency_note"] = "Preview uses a dark world; production alpha requires a separate test"
scene["approved_ingredients"] = "coconut, pineapple, cherries, papaya, banana, grapes, lime"

# Render a compact set of readable checkpoint frames for review.
for frame in (1, 88, 124, 180):
    scene.frame_set(frame)
    scene.render.filepath = str(RENDER_DIR / f"frame-{frame:03d}.png")
    bpy.ops.render.render(write_still=True)

scene.frame_set(1)
bpy.ops.wm.save_as_mainfile(filepath=str(SCENE_FILE))
print(f"Saved Liquid Ribbon blockout: {SCENE_FILE}")
print(f"Checkpoint renders: {RENDER_DIR}")
