"""Build a focused Juicebuilder kiwi look test in the industrial kitchen.

Run from the project root:
  blender -b --python blender/create_kiwi_lookdev.py

The outer skin uses the project's CC0 Poly Haven scan. The cut face uses an
original AI-generated texture with a modeled edge and separate water droplets.
"""
import bpy
import math
import os
import random
from pathlib import Path
from mathutils import Matrix, Vector

ROOT = Path(__file__).resolve().parent.parent
BASE = ROOT / "aloe-story-shot-v2.blend"
SOURCE = ROOT / "assets" / "ingredients" / "food_kiwi_01" / "food_kiwi_01_2k.gltf"
CUT_TEXTURE = ROOT / "assets" / "lookdev" / "kiwi-cut-surface-v1.png"
BRICK_DIR = ROOT / "assets" / "materials" / "brick_wall_001"
SCENE_FILE = ROOT / "kiwi-lookdev-v1.blend"
RENDER_DIR = ROOT / "renders" / "kiwi-lookdev"
RENDER_DIR.mkdir(parents=True, exist_ok=True)

bpy.ops.wm.open_mainfile(filepath=str(BASE))
scene = bpy.context.scene

for obj in list(scene.objects):
    if obj.name.startswith("Aloe leaf | Hi3D"):
        bpy.data.objects.remove(obj, do_unlink=True)

def aim_at(obj, point):
    obj.rotation_euler = (Vector(point) - obj.location).to_track_quat("-Z", "Y").to_euler()

def parent_keep_world(obj, parent):
    world = obj.matrix_world.copy()
    obj.parent = parent
    obj.matrix_world = world

def key(obj, frame, location=None, scale=None, rotation=None):
    if location is not None:
        obj.location = location
        obj.keyframe_insert(data_path="location", frame=frame)
    if scale is not None:
        obj.scale = scale
        obj.keyframe_insert(data_path="scale", frame=frame)
    if rotation is not None:
        obj.rotation_euler = rotation
        obj.keyframe_insert(data_path="rotation_euler", frame=frame)

def principled(name, color, roughness=0.3, metallic=0.0, transmission=0.0):
    mat = bpy.data.materials.new(name)
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes.get("Principled BSDF")
    bsdf.inputs["Base Color"].default_value = (*color, 1)
    bsdf.inputs["Roughness"].default_value = roughness
    bsdf.inputs["Metallic"].default_value = metallic
    bsdf.inputs["Transmission Weight"].default_value = transmission
    return mat

def cylinder(name, location, radius, depth, mat, bevel=0.015):
    bpy.ops.mesh.primitive_cylinder_add(vertices=72, radius=radius, depth=depth, location=location)
    obj = bpy.context.object
    obj.name = name
    obj.data.materials.append(mat)
    for polygon in obj.data.polygons:
        polygon.use_smooth = True
    edge = obj.modifiers.new("Soft machined edge", "BEVEL")
    edge.width = bevel
    edge.segments = 3
    obj.modifiers.new("Weighted normals", "WEIGHTED_NORMAL")
    return obj

def turned_profile(name, center, profile, material, segments=96, wall_thickness=0.008):
    """Revolve a radial cross-section into a pitcher or appliance shell."""
    vertices = []
    for radius, height in profile:
        for index in range(segments):
            angle = 2 * math.pi * index / segments
            vertices.append((center[0] + radius * math.cos(angle),
                             center[1] + radius * math.sin(angle), height))
    faces = []
    for ring in range(len(profile) - 1):
        for index in range(segments):
            following = (index + 1) % segments
            faces.append((ring * segments + index,
                          ring * segments + following,
                          (ring + 1) * segments + following,
                          (ring + 1) * segments + index))
    mesh = bpy.data.meshes.new(name)
    mesh.from_pydata(vertices, [], faces)
    mesh.update()
    obj = bpy.data.objects.new(name, mesh)
    bpy.context.collection.objects.link(obj)
    obj.data.materials.append(material)
    for polygon in mesh.polygons:
        polygon.use_smooth = True
    if wall_thickness:
        solidify = obj.modifiers.new("Wall thickness", "SOLIDIFY")
        solidify.thickness = wall_thickness
    bevel = obj.modifiers.new("Polished edges", "BEVEL")
    bevel.width = 0.008
    bevel.segments = 2
    obj.modifiers.new("Weighted normals", "WEIGHTED_NORMAL")
    return obj

def pitcher_xy(radius, angle, height, center):
    # A rounded-square section reads as a purpose-built blender pitcher.
    exponent = 2 / 4.6
    cosine, sine = math.cos(angle), math.sin(angle)
    x = center[0] + radius * math.copysign(abs(cosine) ** exponent, cosine)
    y = center[1] + radius * math.copysign(abs(sine) ** exponent, sine)
    # Pull just the front rim forward into a small pouring beak.
    front_angle = math.atan2(math.sin(angle + math.pi / 2), math.cos(angle + math.pi / 2))
    if height > 1.43:
        y -= .075 * math.exp(-((front_angle / .28) ** 2))
    return x, y

def pitcher_shell(name, center, profile, material, segments=96):
    verts = []
    for radius, height in profile:
        for index in range(segments):
            angle = math.tau * index / segments
            x, y = pitcher_xy(radius, angle, height, center)
            verts.append((x, y, height))
    faces = []
    for ring in range(len(profile) - 1):
        for index in range(segments):
            nxt = (index + 1) % segments
            faces.append((ring * segments + index, ring * segments + nxt,
                          (ring + 1) * segments + nxt, (ring + 1) * segments + index))
    mesh = bpy.data.meshes.new(name)
    mesh.from_pydata(verts, [], faces)
    mesh.update()
    obj = bpy.data.objects.new(name, mesh)
    bpy.context.collection.objects.link(obj)
    obj.data.materials.append(material)
    for polygon in mesh.polygons:
        polygon.use_smooth = True
    bevel = obj.modifiers.new("Polished glass edges", "BEVEL")
    bevel.width = .006
    bevel.segments = 2
    obj.modifiers.new("Weighted glass normals", "WEIGHTED_NORMAL")
    return obj

def tube(name, points, radius, material):
    curve = bpy.data.curves.new(name, "CURVE")
    curve.dimensions = "3D"
    curve.resolution_u = 24
    curve.bevel_depth = radius
    curve.bevel_resolution = 5
    spline = curve.splines.new("BEZIER")
    spline.bezier_points.add(len(points) - 1)
    for point, coords in zip(spline.bezier_points, points):
        point.co = coords
        point.handle_left_type = "AUTO"
        point.handle_right_type = "AUTO"
    obj = bpy.data.objects.new(name, curve)
    bpy.context.collection.objects.link(obj)
    obj.data.materials.append(material)
    return obj

def vortex_juice(name, location, radius, height, material, segments=96):
    """Closed juice volume with an uneven, shallow vortex surface."""
    rings = [(radius, 0.0), (radius, height), (.78 * radius, height - .010),
             (.53 * radius, height - .022), (.27 * radius, height - .035)]
    vertices = []
    for ring_index, (ring_radius, ring_height) in enumerate(rings):
        for index in range(segments):
            angle = math.tau * index / segments
            ripple = 0 if ring_index == 0 else .012 * math.sin(5 * angle + ring_index * .7)
            vertices.append((ring_radius * math.cos(angle),
                             ring_radius * math.sin(angle), ring_height + ripple))
    vertices.append((0, 0, height - .042))
    faces = []
    for ring in range(len(rings) - 1):
        for index in range(segments):
            following = (index + 1) % segments
            faces.append((ring * segments + index, ring * segments + following,
                          (ring + 1) * segments + following, (ring + 1) * segments + index))
    center_index = len(vertices) - 1
    for index in range(segments):
        faces.append(((len(rings) - 1) * segments + index,
                      (len(rings) - 1) * segments + (index + 1) % segments,
                      center_index))
    faces.append(tuple(reversed(range(segments))))
    mesh = bpy.data.meshes.new(name)
    mesh.from_pydata(vertices, [], faces)
    mesh.update()
    obj = bpy.data.objects.new(name, mesh)
    bpy.context.collection.objects.link(obj)
    obj.location = location
    mesh.materials.append(material)
    for polygon in mesh.polygons:
        polygon.use_smooth = True
    return obj

def area_light(name, location, power, size, color, target):
    data = bpy.data.lights.new(name, "AREA")
    data.energy = power
    data.shape = "DISK"
    data.size = size
    data.color = color
    obj = bpy.data.objects.new(name, data)
    bpy.context.collection.objects.link(obj)
    obj.location = location
    aim_at(obj, target)
    return obj

# Replace the evenly patterned blockout wall with a photographed CC0 PBR set.
wall = bpy.data.objects.get("Brick wall")
if wall is None:
    raise RuntimeError("The industrial kitchen base is missing its brick wall")
brick_mat = principled("Kitchen · Poly Haven scanned industrial brick", (.5, .5, .5), .85)
brick_nodes, brick_links = brick_mat.node_tree.nodes, brick_mat.node_tree.links
brick_bsdf = brick_nodes.get("Principled BSDF")
coordinates = brick_nodes.new("ShaderNodeTexCoord")
separate = brick_nodes.new("ShaderNodeSeparateXYZ")
brick_links.new(coordinates.outputs["Generated"], separate.inputs["Vector"])
u = brick_nodes.new("ShaderNodeMath")
u.operation = "MULTIPLY"
u.inputs[1].default_value = 7.4
brick_links.new(separate.outputs["X"], u.inputs[0])
v = brick_nodes.new("ShaderNodeMath")
v.operation = "MULTIPLY"
v.inputs[1].default_value = 3.2
brick_links.new(separate.outputs["Z"], v.inputs[0])
combine = brick_nodes.new("ShaderNodeCombineXYZ")
brick_links.new(u.outputs[0], combine.inputs["X"])
brick_links.new(v.outputs[0], combine.inputs["Y"])

def brick_image(kind, color_space="sRGB"):
    node = brick_nodes.new("ShaderNodeTexImage")
    node.image = bpy.data.images.load(str(BRICK_DIR / f"brick_wall_001_{kind}_2k.jpg"), check_existing=True)
    node.image.colorspace_settings.name = color_space
    node.extension = "REPEAT"
    brick_links.new(combine.outputs["Vector"], node.inputs["Vector"])
    return node

brick_color = brick_image("diffuse")
brick_grade = brick_nodes.new("ShaderNodeHueSaturation")
brick_grade.inputs["Saturation"].default_value = .85
brick_grade.inputs["Value"].default_value = .44
brick_links.new(brick_color.outputs["Color"], brick_grade.inputs["Color"])
brick_links.new(brick_grade.outputs["Color"], brick_bsdf.inputs["Base Color"])
brick_rough = brick_image("rough", "Non-Color")
brick_links.new(brick_rough.outputs["Color"], brick_bsdf.inputs["Roughness"])
brick_normal = brick_image("nor_gl", "Non-Color")
normal_map = brick_nodes.new("ShaderNodeNormalMap")
normal_map.inputs["Strength"].default_value = .7
brick_links.new(brick_normal.outputs["Color"], normal_map.inputs["Color"])
brick_links.new(normal_map.outputs["Normal"], brick_bsdf.inputs["Normal"])
wall.data.materials[0] = brick_mat

# Import the CC0 scan and put its mesh centre at the origin so both versions
# share the same original texture and normal detail.
before = set(bpy.data.objects)
bpy.ops.import_scene.gltf(filepath=str(SOURCE))
imported = [obj for obj in bpy.data.objects if obj not in before and obj.type == "MESH"]
if len(imported) != 1:
    raise RuntimeError("Expected one Poly Haven kiwi mesh, found %d" % len(imported))
whole = imported[0]
whole.name = "Kiwi · Poly Haven whole scan"
bounds = [Vector(corner) for corner in whole.bound_box]
low = Vector((min(v[i] for v in bounds) for i in range(3)))
high = Vector((max(v[i] for v in bounds) for i in range(3)))
whole.data.transform(Matrix.Translation(-((low + high) * 0.5)))
bpy.context.view_layer.update()
factor = 0.82 / whole.dimensions.z
whole.scale = (factor, factor, factor)
whole.rotation_euler = (math.radians(69), 0, math.radians(-14))
whole.location = (-0.82, 0.13, 0.91)
peel_mat = whole.data.materials[0]
if peel_mat and peel_mat.use_nodes:
    peel_nodes, peel_links = peel_mat.node_tree.nodes, peel_mat.node_tree.links
    peel_shader = next((node for node in peel_nodes if node.type == "BSDF_PRINCIPLED"), None)
    if peel_shader:
        peel_shader.inputs["Roughness"].default_value = 0.79
        color_link = next((link for link in peel_links if link.to_node == peel_shader and link.to_socket.name == "Base Color"), None)
        if color_link:
            source_node, source_socket = color_link.from_node, color_link.from_socket
            peel_links.remove(color_link)
            grade = peel_nodes.new("ShaderNodeHueSaturation")
            grade.label = "Deepen photographed kiwi skin"
            grade.inputs["Saturation"].default_value = 1.05
            grade.inputs["Value"].default_value = 0.58
            peel_links.new(source_socket, grade.inputs["Color"])
            peel_links.new(grade.outputs["Color"], peel_shader.inputs["Base Color"])

# A clean half shell uses a dedicated 3D skin shader and sparse short fibres.
# Reusing the whole scan's photographic UV atlas on new geometry stretched it
# into obvious bands; the original scanned whole fruit remains intact.
skin = principled("Kiwi half · mottled skin", (.24, .13, .06), .86)
skin_nodes, skin_links = skin.node_tree.nodes, skin.node_tree.links
skin_bsdf = skin_nodes.get("Principled BSDF")
skin_noise = skin_nodes.new("ShaderNodeTexNoise")
skin_noise.inputs["Scale"].default_value = 12
skin_noise.inputs["Detail"].default_value = 5
skin_noise.inputs["Roughness"].default_value = .72
skin_ramp = skin_nodes.new("ShaderNodeValToRGB")
skin_ramp.color_ramp.elements[0].position = .23
skin_ramp.color_ramp.elements[0].color = (.075, .038, .018, 1)
skin_ramp.color_ramp.elements[1].position = .75
skin_ramp.color_ramp.elements[1].color = (.24, .13, .058, 1)
skin_links.new(skin_noise.outputs["Fac"], skin_ramp.inputs["Fac"])
skin_links.new(skin_ramp.outputs["Color"], skin_bsdf.inputs["Base Color"])
skin_micro = skin_nodes.new("ShaderNodeTexNoise")
skin_micro.inputs["Scale"].default_value = 94
skin_micro.inputs["Detail"].default_value = 3
skin_bump = skin_nodes.new("ShaderNodeBump")
skin_bump.inputs["Strength"].default_value = .26
skin_bump.inputs["Distance"].default_value = .012
skin_links.new(skin_micro.outputs["Fac"], skin_bump.inputs["Height"])
skin_links.new(skin_bump.outputs["Normal"], skin_bsdf.inputs["Normal"])
around, axial = 72, 20
shell_verts, shell_faces = [], []
for step in range(axial):
    t = step / axial
    y = 0.41 * t
    radial = math.sqrt(max(0.0, 1.0 - t * t))
    for side in range(around + 1):
        angle = math.tau * side / around
        shell_verts.append((math.cos(angle) * 0.318 * radial, y,
                            math.sin(angle) * 0.315 * radial))
for step in range(axial - 1):
    for side in range(around):
        a = step * (around + 1) + side
        b = a + around + 1
        shell_faces.append((a, b, b + 1, a + 1))
tip = len(shell_verts)
shell_verts.append((0, 0.41, 0))
last_ring = (axial - 1) * (around + 1)
for side in range(around):
    shell_faces.append((last_ring + side, tip, last_ring + side + 1))
shell_mesh = bpy.data.meshes.new("Kiwi half shell mesh")
shell_mesh.from_pydata(shell_verts, [], shell_faces)
shell_mesh.materials.append(skin)
shell_mesh.update()
shell_uv = shell_mesh.uv_layers.new(name="Peel UV")
for polygon in shell_mesh.polygons:
    polygon.use_smooth = True
    for loop_index in polygon.loop_indices:
        vertex_index = shell_mesh.loops[loop_index].vertex_index
        shell_uv.data[loop_index].uv = (vertex_index % (around + 1) / around,
                                       vertex_index // (around + 1) / axial)
half = bpy.data.objects.new("Kiwi · detailed skin on clean half", shell_mesh)
bpy.context.collection.objects.link(half)
half.location = (0.45, 0.23, 0.91)

fibre_mat = principled("Kiwi half · fine brown fibres", (.28, .16, .076), .9)
fibre_curve = bpy.data.curves.new("Kiwi half fibres", "CURVE")
fibre_curve.dimensions = "3D"
fibre_curve.bevel_depth = .00035
fibre_curve.bevel_resolution = 1
random.seed(71)
for _ in range(1100):
    t = .08 + random.random() * .86
    angle = random.random() * math.tau
    radial = math.sqrt(1 - t * t)
    x = .318 * radial * math.cos(angle)
    y = .41 * t
    z = .315 * radial * math.sin(angle)
    normal = Vector((x / (.318 * .318), y / (.41 * .41), z / (.315 * .315))).normalized()
    tangent = Vector((random.uniform(-.4, .4), random.uniform(-.25, .25), random.uniform(-.4, .4)))
    length = .004 + random.random() * .006
    tip_point = Vector((x, y, z)) + (normal + tangent).normalized() * length
    spline = fibre_curve.splines.new("POLY")
    spline.points.add(1)
    spline.points[0].co = (x, y, z, 1)
    spline.points[1].co = (tip_point.x, tip_point.y, tip_point.z, 1)
fibres = bpy.data.objects.new("Kiwi · fine skin fibres", fibre_curve)
bpy.context.collection.objects.link(fibres)
fibres.location = half.location
fibres.data.materials.append(fibre_mat)

cut_image = bpy.data.images.load(str(CUT_TEXTURE), check_existing=True)
cut_image.name = "Original kiwi cut surface · AI generated"
cut_image.alpha_mode = "STRAIGHT"
cut_mat = principled("Kiwi · wet cut face", (0.5, 0.8, 0.2), roughness=0.24)
nodes, links = cut_mat.node_tree.nodes, cut_mat.node_tree.links
bsdf = nodes.get("Principled BSDF")
tex = nodes.new("ShaderNodeTexImage")
tex.image = cut_image
tex.interpolation = "Linear"
links.new(tex.outputs["Color"], bsdf.inputs["Base Color"])
links.new(tex.outputs["Alpha"], bsdf.inputs["Alpha"])
if "Coat Weight" in bsdf.inputs:
    bsdf.inputs["Coat Weight"].default_value = 0.18
    bsdf.inputs["Coat Roughness"].default_value = 0.12
if "Subsurface Weight" in bsdf.inputs:
    bsdf.inputs["Subsurface Weight"].default_value = 0.045
gray = nodes.new("ShaderNodeRGBToBW")
bump = nodes.new("ShaderNodeBump")
bump.inputs["Strength"].default_value = 0.08
bump.inputs["Distance"].default_value = 0.007
links.new(tex.outputs["Color"], gray.inputs["Color"])
links.new(gray.outputs["Val"], bump.inputs["Height"])
links.new(bump.outputs["Normal"], bsdf.inputs["Normal"])
cut_mat.surface_render_method = "BLENDED"

# A UV mapped disk preserves the generated radial fibre and seed detail.
segments = 96
radius_x, radius_z = 0.318, 0.315
verts = [(0, 0, 0)]
for i in range(segments):
    angle = math.tau * i / segments
    verts.append((math.cos(angle) * radius_x, 0, math.sin(angle) * radius_z))
faces = [(0, i + 1, (i + 1) % segments + 1) for i in range(segments)]
mesh = bpy.data.meshes.new("Kiwi cut cap mesh")
mesh.from_pydata(verts, [], faces)
mesh.materials.append(cut_mat)
mesh.update()
uv = mesh.uv_layers.new(name="Radial image UV")
for polygon in mesh.polygons:
    for loop_index in polygon.loop_indices:
        vertex = mesh.vertices[mesh.loops[loop_index].vertex_index].co
        uv.data[loop_index].uv = (0.5 + vertex.x / (2 * radius_x), 0.5 + vertex.z / (2 * radius_z))
cap = bpy.data.objects.new("Kiwi · photographed cut face", mesh)
bpy.context.collection.objects.link(cap)
cap.location = (0.45, 0.222, 0.91)
cut_rind = principled("Kiwi · soft brown cut rind", (0.28, 0.14, 0.055), 0.76)
bpy.ops.mesh.primitive_torus_add(major_segments=96, minor_segments=16,
                                 location=(0.45, 0.221, 0.91), rotation=(math.pi / 2, 0, 0),
                                 major_radius=0.311, minor_radius=0.009)
rind_ring = bpy.context.object
rind_ring.name = "Kiwi · modeled cut rind edge"
rind_ring.data.materials.append(cut_rind)
for polygon in rind_ring.data.polygons:
    polygon.use_smooth = True

water = principled("Fresh juice droplets", (0.9, 1.0, 0.94), 0.035, transmission=1.0)
water.node_tree.nodes.get("Principled BSDF").inputs["IOR"].default_value = 1.333
random.seed(41)
droplets = []
for index in range(30):
    angle = random.random() * math.tau
    radius = 0.06 + random.random() * 0.22
    x = 0.45 + math.cos(angle) * radius
    z = 0.91 + math.sin(angle) * radius
    size = 0.003 + random.random() * 0.007
    bpy.ops.mesh.primitive_uv_sphere_add(segments=12, ring_count=8, location=(x, 0.214, z))
    drop = bpy.context.object
    drop.name = "Kiwi juice bead %02d" % index
    drop.scale = (size, size * 0.45, size)
    drop.data.materials.append(water)
    droplets.append(drop)

half_rig = bpy.data.objects.new("Kiwi half · animation control", None)
bpy.context.collection.objects.link(half_rig)
half_rig.location = (0.45, 0.23, 0.91)
bpy.context.view_layer.update()
for obj in [half, fibres, cap, rind_ring, *droplets]:
    parent_keep_world(obj, half_rig)

# The pitcher is an open, thick glass shell. Its juice rises only after the
# kiwi enters; this is a story cue, not a fluid simulation.
steel = principled("Look test · brushed stainless", (0.26, 0.30, 0.29), 0.26, metallic=0.82)
dark_steel = principled("Look test · charcoal housing", (0.045, 0.055, 0.055), 0.33, metallic=0.48)
rubber = principled("Look test · rubber details", (0.017, 0.025, 0.023), 0.67)
glass = principled("Look test · thick pitcher glass", (0.97, 0.99, 0.98), 0.015, transmission=1.0)
glass.node_tree.nodes.get("Principled BSDF").inputs["IOR"].default_value = 1.45
juice = principled("Look test · kiwi juice with fine pulp", (0.16, 0.43, 0.055), 0.27, transmission=0.06)
juice_shader = juice.node_tree.nodes.get("Principled BSDF")
juice_shader.inputs["Subsurface Weight"].default_value = .08
texture = juice.node_tree.nodes.new("ShaderNodeTexNoise")
texture.inputs["Scale"].default_value = 31
texture.inputs["Detail"].default_value = 3
texture.inputs["Roughness"].default_value = .65
bump = juice.node_tree.nodes.new("ShaderNodeBump")
bump.inputs["Strength"].default_value = .075
bump.inputs["Distance"].default_value = .009
juice.node_tree.links.new(texture.outputs["Fac"], bump.inputs["Height"])
juice.node_tree.links.new(bump.outputs["Normal"], juice_shader.inputs["Normal"])
foam = principled("Look test · pale foam", (0.42, 0.65, 0.20), 0.42)
blender_center = (1.63, 1.17)
cx, cy = blender_center
motor = turned_profile("Blender motor · tapered housing", blender_center,
    [(0.0, 0.07), (0.36, 0.07), (0.43, 0.12), (0.42, 0.30),
     (0.36, 0.39), (0.0, 0.39)], dark_steel)
motor_trim = cylinder("Blender motor · stainless shoulder", (cx, cy, 0.39), 0.36, 0.055, steel, 0.014)
foot = cylinder("Blender motor · rubber foot", (cx, cy, 0.065), 0.35, 0.045, rubber, 0.012)
coupling = cylinder("Blender motor · dark coupling", (cx, cy, 0.445), 0.18, 0.07, rubber, 0.008)
jar = pitcher_shell("Blender pitcher · faceted open glass", blender_center,
    [(0.0, 0.44), (0.29, 0.44), (0.33, 0.48), (0.35, 0.69),
     (0.375, 1.16), (0.395, 1.48), (0.355, 1.48), (0.337, 1.16),
     (0.31, 0.69), (0.27, 0.50), (0.0, 0.49)], glass)
rim = tube("Blender pitcher · rolled lip",
    [(*pitcher_xy(.395, i * math.tau / 96, 1.48, blender_center), 1.48)
     for i in range(97)], .012, glass)
handle = tube("Blender pitcher · glass handle",
    [(cx + .37, cy + .06, 1.32), (cx + .54, cy + .06, 1.36),
     (cx + .67, cy + .06, 1.20), (cx + .66, cy + .06, .82),
     (cx + .48, cy + .06, .69), (cx + .35, cy + .06, .77)], .060, glass)
jar_collar = cylinder("Blender pitcher · steel locking collar", (cx, cy, .465), .34, .055, steel, .008)
blade_hub = cylinder("Blender blade · central spindle", (cx, cy, .55), .067, .14, steel, .008)
blade_rotor = bpy.data.objects.new("Blender blades · animated rotor", None)
bpy.context.collection.objects.link(blade_rotor)
blade_rotor.location = (cx, cy, .55)
blades = []
for index in range(4):
    angle = index * math.tau / 4
    blade = bpy.data.objects.new("Blender blade · %d" % (index + 1),
                                bpy.data.meshes.new("Curved steel blade"))
    bpy.context.collection.objects.link(blade)
    direction = Vector((math.cos(angle), math.sin(angle), 0))
    normal = Vector((-math.sin(angle), math.cos(angle), 0))
    verts = []
    for reach, sideways, height in ((.045, -.035, .58), (.29, -.018, .63),
                                    (.31, .045, .67), (.045, .045, .59)):
        pos = Vector((cx, cy, 0)) + direction * reach + normal * sideways
        verts.append((pos.x, pos.y, height))
    blade.data.from_pydata(verts, [], [(0, 1, 2, 3)])
    blade.data.materials.append(steel)
    blade.modifiers.new("Blade metal thickness", "SOLIDIFY").thickness = .013
    blades.append(blade)
bpy.context.view_layer.update()
for obj in [blade_hub, *blades]:
    parent_keep_world(obj, blade_rotor)
dial = cylinder("Blender motor · front dial", (cx, cy - .425, .235), .105, .045, steel, .01)
dial.rotation_euler.x = math.pi / 2
dial_center = cylinder("Blender motor · dial centre", (cx, cy - .453, .235), .065, .012, rubber, .005)
dial_center.rotation_euler.x = math.pi / 2
control_marks = []
for index in range(9):
    angle = math.radians(-130 + index * 32.5)
    x = cx + .148 * math.sin(angle)
    z = .235 + .148 * math.cos(angle)
    bpy.ops.mesh.primitive_cube_add(size=1, location=(x, cy - .433, z))
    mark = bpy.context.object
    mark.name = "Blender control · engraved speed mark %02d" % index
    mark.dimensions = (.008, .003, .019)
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    mark.rotation_euler.y = -angle
    mark.data.materials.append(steel)
    control_marks.append(mark)
for index, x in enumerate((cx - .245, cx + .245)):
    button = cylinder("Blender control · switch %d" % (index + 1),
                      (x, cy - .425, .235), .032, .020, rubber, .004)
    button.rotation_euler.x = math.pi / 2
    control_marks.append(button)
liquid = vortex_juice("Blender juice · vortex volume", (cx, cy, .49), .305, .51, juice)
liquid.scale.z = .001
bpy.ops.mesh.primitive_torus_add(major_segments=80, minor_segments=12,
    location=(cx, cy, 1.0), major_radius=.291, minor_radius=.013)
foam_surface = bpy.context.object
foam_surface.name = "Blender juice · foam edge"
foam_surface.data.materials.append(foam)
foam_surface.scale = (.001, .001, .001)
# A detached lid on the countertop leaves a clear opening for the ingredient.
lid = cylinder("Blender lid · resting on counter", (cx + .91, cy - .12, .065), .38, .075, rubber, .012)
lid_cap = cylinder("Blender lid · centre cap", (cx + .91, cy - .12, .13), .13, .07, steel, .012)
blender_rig = bpy.data.objects.new("Background blender · composition control", None)
bpy.context.collection.objects.link(blender_rig)
blender_rig.location = (blender_center[0], blender_center[1], 0.2)
bpy.context.view_layer.update()
for obj in (motor, motor_trim, foot, coupling, jar, rim, handle, jar_collar,
            blade_rotor, dial, dial_center, *control_marks, liquid, foam_surface, lid, lid_cap):
    parent_keep_world(obj, blender_rig)
blender_rig.location = (1.9, 1.42, 0.2)
blender_rig.scale = (0.76, 0.76, 0.76)
# The modeled vortex grows over almost a second. Hide it entirely while the
# ingredient is presented, so no premature green line appears in the glass.
juice_local = liquid.location.copy()
foam_local = foam_surface.location.copy()
key(liquid, 1, scale=(1, 1, .001), location=juice_local)
key(liquid, 95, scale=(1, 1, .001), location=juice_local)
key(liquid, 116, scale=(1, 1, 1), location=juice_local)
key(foam_surface, 95, scale=(.001, .001, .001),
    location=(foam_local.x, foam_local.y, foam_local.z - .51 + .51 * .001))
key(foam_surface, 116, scale=(1, 1, 1), location=foam_local)
liquid.hide_render = True
liquid.keyframe_insert(data_path="hide_render", frame=95)
liquid.hide_render = False
liquid.keyframe_insert(data_path="hide_render", frame=96)
foam_surface.hide_render = True
foam_surface.keyframe_insert(data_path="hide_render", frame=95)
foam_surface.hide_render = False
foam_surface.keyframe_insert(data_path="hide_render", frame=96)
key(blade_rotor, 88, rotation=(0, 0, 0))
key(blade_rotor, 116, rotation=(0, 0, 20 * math.pi))
key(blade_rotor, 120, rotation=(0, 0, 22 * math.pi))

area_light("Kiwi overhead softbox", (-0.75, -0.7, 3.7), 650, 2.4, (1.0, 0.82, 0.62), (0, 0.2, 0.9))
area_light("Kiwi cool edge strip", (1.9, -0.55, 3.1), 380, 1.5, (0.72, 0.86, 1.0), (0.45, 0.2, 0.9))

scene.camera.location = (0.0, -5.45, 2.22)
aim_at(scene.camera, (0.15, 0.42, 0.93))
scene.camera.data.lens = 62
focus = bpy.data.objects.new("Camera focus · kiwi cut", None)
bpy.context.collection.objects.link(focus)
focus.location = (0.45, 0.222, 0.91)
scene.camera.data.dof.use_dof = True
scene.camera.data.dof.focus_object = focus
scene.camera.data.dof.aperture_fstop = 1.05
scene.camera.keyframe_insert(data_path="location", frame=55)
scene.camera.keyframe_insert(data_path="rotation_euler", frame=55)
focus.keyframe_insert(data_path="location", frame=55)
scene.camera.location = (1.13, -4.65, 2.02)
aim_at(scene.camera, (1.90, 1.32, 1.06))
scene.camera.keyframe_insert(data_path="location", frame=84)
scene.camera.keyframe_insert(data_path="rotation_euler", frame=84)
focus.location = (1.90, 1.39, 1.04)
focus.keyframe_insert(data_path="location", frame=84)
scene.camera.location = (1.30, -4.11, 1.92)
aim_at(scene.camera, (1.90, 1.40, 1.03))
scene.camera.keyframe_insert(data_path="location", frame=120)
scene.camera.keyframe_insert(data_path="rotation_euler", frame=120)
focus.keyframe_insert(data_path="location", frame=120)
scene.camera.location = (1.22, -3.55, 1.58)
aim_at(scene.camera, (1.08, .91, .58))
scene.camera.keyframe_insert(data_path="location", frame=148)
scene.camera.keyframe_insert(data_path="rotation_euler", frame=148)
focus.location = (1.08, .91, .58)
focus.keyframe_insert(data_path="location", frame=148)
scene.camera.location = (1.18, -3.15, 1.42)
aim_at(scene.camera, (1.08, .91, .58))
scene.camera.keyframe_insert(data_path="location", frame=180)
scene.camera.keyframe_insert(data_path="rotation_euler", frame=180)
focus.keyframe_insert(data_path="location", frame=180)

# A short reversible editorial move: whole kiwi arrives, the cut half is
# revealed, then the half rises and moves toward the blender.
key(whole, 1, location=(-2.1, 0.13, 0.91), rotation=(math.radians(69), 0, math.radians(-20)))
key(whole, 24, location=(-0.82, 0.13, 0.91), rotation=(math.radians(69), 0, math.radians(-14)))
key(whole, 55, location=(-0.82, 0.13, 0.91))
key(whole, 90, location=(-1.75, 0.2, 0.97), scale=(factor * 0.75,) * 3)
key(half_rig, 1, scale=(0, 0, 0))
key(half_rig, 25, scale=(0, 0, 0), location=(0.45, 0.23, 0.91))
key(half_rig, 39, scale=(1, 1, 1), location=(0.45, 0.23, 0.91))
key(half_rig, 55, scale=(1, 1, 1), location=(0.45, 0.23, 0.91))
key(half_rig, 76, scale=(0.78, 0.78, 0.78), location=(1.30, 0.90, 1.42), rotation=(0.12, 0.18, 0.38))
key(half_rig, 86, scale=(0.52, 0.52, 0.52), location=(1.90, 1.37, 1.48), rotation=(0.22, 0.42, 1.2))
key(half_rig, 92, scale=(0, 0, 0), location=(1.91, 1.40, 1.01), rotation=(.45, .85, 2.3))
key(half_rig, 100, scale=(0, 0, 0), location=(1.91, 1.40, .65), rotation=(.55, 1.05, 3.0))

# A small burst of independently keyed pieces makes the kiwi's transition
# legible before the juice rises. These are modeled pulp fragments, not a
# baked fluid or rigid-body simulation.
chunk_flesh = principled("Kiwi pieces · fresh pulp", (.13, .34, .039), .31)
chunk_nodes, chunk_links = chunk_flesh.node_tree.nodes, chunk_flesh.node_tree.links
chunk_bsdf = chunk_nodes.get("Principled BSDF")
chunk_bsdf.inputs["Subsurface Weight"].default_value = .09
chunk_bsdf.inputs["Coat Weight"].default_value = .12
chunk_noise = chunk_nodes.new("ShaderNodeTexNoise")
chunk_noise.inputs["Scale"].default_value = 6
chunk_noise.inputs["Detail"].default_value = 3
chunk_ramp = chunk_nodes.new("ShaderNodeValToRGB")
chunk_ramp.color_ramp.elements[0].color = (.065, .20, .018, 1)
chunk_ramp.color_ramp.elements[1].color = (.21, .43, .07, 1)
chunk_links.new(chunk_noise.outputs["Fac"], chunk_ramp.inputs["Fac"])
chunk_links.new(chunk_ramp.outputs["Color"], chunk_bsdf.inputs["Base Color"])
chunk_micro = chunk_nodes.new("ShaderNodeTexNoise")
chunk_micro.inputs["Scale"].default_value = 42
chunk_bump = chunk_nodes.new("ShaderNodeBump")
chunk_bump.inputs["Strength"].default_value = .08
chunk_bump.inputs["Distance"].default_value = .008
chunk_links.new(chunk_micro.outputs["Fac"], chunk_bump.inputs["Height"])
chunk_links.new(chunk_bump.outputs["Normal"], chunk_bsdf.inputs["Normal"])
chunk_skin = principled("Kiwi pieces · skin flecks", (.20, .105, .045), .82)
random.seed(94)
for index in range(18):
    bpy.ops.mesh.primitive_cube_add(size=2)
    piece = bpy.context.object
    piece.name = "Kiwi chopped piece %02d" % (index + 1)
    for vertex in piece.data.vertices:
        vertex.co.x += random.uniform(-.13, .13)
        vertex.co.y += random.uniform(-.13, .13)
        vertex.co.z += random.uniform(-.13, .13)
    piece.data.materials.append(chunk_flesh)
    piece.data.materials.append(chunk_skin)
    for polygon in piece.data.polygons:
        polygon.use_smooth = True
        if random.random() < .18:
            polygon.material_index = 1
    edge = piece.modifiers.new("Soft juicy cut edge", "BEVEL")
    edge.width = .18
    edge.segments = 3
    piece.modifiers.new("Weighted cut normals", "WEIGHTED_NORMAL")
    size = .023 + random.random() * .026
    angle = index * 2.39996
    delay = index % 7
    first = 87 + delay
    start_radius = .03 + random.random() * .09
    start = (1.90 + start_radius * math.cos(angle),
             1.39 + start_radius * math.sin(angle),
             1.37 + random.uniform(-.05, .08))
    orbit_radius = .13 + random.random() * .08
    orbit = (1.90 + orbit_radius * math.cos(angle + 1.4),
             1.42 + orbit_radius * math.sin(angle + 1.4),
             1.25 - .018 * delay)
    inside_radius = .065 + random.random() * .08
    inside = (1.90 + inside_radius * math.cos(angle + 3.1),
              1.42 + inside_radius * math.sin(angle + 3.1),
              .95 - random.random() * .12)
    settled = (1.90 + .07 * math.cos(angle + 5),
               1.42 + .07 * math.sin(angle + 5), .67)
    key(piece, first - 1, location=start, scale=(0, 0, 0))
    key(piece, first + 2, location=orbit,
        scale=(size, size * .65, size * .78),
        rotation=(random.random() * 2, random.random() * 2, angle))
    key(piece, 104 + delay // 2, location=inside,
        scale=(size * .76, size * .50, size * .62),
        rotation=(random.random() * 5, random.random() * 5, angle + 5.2))
    key(piece, 114, location=settled, scale=(0, 0, 0),
        rotation=(random.random() * 7, random.random() * 7, angle + 8.4))

# Temporary unbranded bottles close the editorial beat. Their fill and pour
# stream are keyed geometry placeholders for a later fluid-cache pass.
bottle_glass = principled("Bottle · clear recycled glass", (.94, .98, .94), .045, transmission=1.0)
bottle_glass.node_tree.nodes.get("Principled BSDF").inputs["IOR"].default_value = 1.46
bottle_juice = principled("Bottle · fresh kiwi juice", (.12, .33, .035), .24, transmission=.08)
bottle_cap_mat = principled("Bottle · brushed cap", (.35, .38, .34), .24, metallic=.62)
bottle_rig = bpy.data.objects.new("Finished bottles · composition control", None)
bpy.context.collection.objects.link(bottle_rig)
bottle_centres = ((.65, .86), (1.22, .92))
bottle_fill_objects = []
for index, (bx, by) in enumerate(bottle_centres):
    bottle = turned_profile("Finished bottle %02d · clear body" % (index + 1), (bx, by),
        [(0.0, .04), (.16, .04), (.19, .09), (.20, .15), (.20, .61),
         (.18, .70), (.12, .76), (.09, .78), (0.0, .78)], bottle_glass, segments=64,
        wall_thickness=.006)
    fill = cylinder("Finished bottle %02d · juice fill" % (index + 1),
        (bx, by, .35), .165, .52, bottle_juice, .008)
    fill.scale.z = .001
    neck = cylinder("Finished bottle %02d · neck" % (index + 1), (bx, by, .84), .075, .14, bottle_glass, .006)
    cap = cylinder("Finished bottle %02d · cap" % (index + 1), (bx, by, .95), .084, .065, bottle_cap_mat, .008)
    for obj in (bottle, fill, neck, cap):
        parent_keep_world(obj, bottle_rig)
    bottle_fill_objects.append(fill)

stream = tube("Pour stream · kiwi juice",
    [(1.83, 1.42, 1.18), (1.73, 1.18, 1.00), (1.42, 1.02, .84),
     (1.20, .93, .82)], .018, bottle_juice)
stream.scale = (.001, .001, .001)
for fill in bottle_fill_objects:
    key(fill, 1, scale=(1, 1, .001))
    key(fill, 138, scale=(1, 1, .001))
    key(fill, 168, scale=(1, 1, 1))
key(stream, 1, scale=(.001, .001, .001))
key(stream, 138, scale=(.001, .001, .001))
key(stream, 148, scale=(1, 1, 1))
key(stream, 168, scale=(1, 1, 1))

scene.frame_start = 1
scene.frame_end = 180
scene.render.fps = 24
scene.render.engine = "CYCLES"
scene.cycles.samples = 72
scene.cycles.use_denoising = True
scene.render.resolution_x = 1600
scene.render.resolution_y = 1100
scene.render.resolution_percentage = 100
scene.render.image_settings.file_format = "PNG"
scene.render.image_settings.color_mode = "RGB"
scene.render.filepath = str(RENDER_DIR / "kiwi-lookdev-hero-v1.png")
scene.view_settings.view_transform = "AgX"
scene.view_settings.look = "AgX - Medium High Contrast"
scene.view_settings.exposure = -0.08
scene.frame_set(48)

bpy.ops.object.select_all(action="DESELECT")
half.select_set(True)
bpy.context.view_layer.objects.active = half
bpy.ops.file.pack_all()
bpy.ops.wm.save_as_mainfile(filepath=str(SCENE_FILE))
if os.environ.get("JUICEBUILDER_KIWI_DRAFT") == "1":
    scene.cycles.samples = 24
    scene.render.resolution_percentage = 60
    scene.render.filepath = str(RENDER_DIR / "kiwi-lookdev-draft.png")
bpy.ops.render.render(write_still=True)
print("Saved kiwi look test:", SCENE_FILE)
print("Rendered hero:", scene.render.filepath)
print("Modeled kiwi half shell vertices:", len(half.data.vertices))
