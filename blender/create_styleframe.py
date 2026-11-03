"""Build an industrial-kitchen Juicebuilder look-development frame in Blender.

Run with:
  blender -b --python blender/create_styleframe.py

This is a procedural look-development scene, not the final hero animation.
It establishes camera, lighting, materials, composition and the temporary bottle
before the individual ingredient models are refined or replaced by licensed scans.
"""
import bpy
import math
import random
from pathlib import Path
from mathutils import Vector

random.seed(27)

OUT = r"C:\Coding\Applications\Ideas\juicebuilder\renders\aloe-industrial-look-test.png"
BLEND = r"C:\Coding\Applications\Ideas\juicebuilder\juicebuilder-industrial-lookdev.blend"
Path(OUT).parent.mkdir(parents=True, exist_ok=True)

# Reset to an empty scene.
bpy.ops.object.select_all(action="SELECT")
bpy.ops.object.delete(use_global=False)
for datablocks in (bpy.data.meshes, bpy.data.curves, bpy.data.materials, bpy.data.cameras, bpy.data.lights):
    for block in list(datablocks):
        if block.users == 0:
            datablocks.remove(block)

scene = bpy.context.scene
scene.render.engine = "CYCLES"
scene.cycles.samples = 40
scene.cycles.use_denoising = True
scene.render.resolution_x = 1440
scene.render.resolution_y = 1080
scene.render.resolution_percentage = 100
scene.render.image_settings.file_format = "PNG"
scene.render.image_settings.color_mode = "RGBA"
scene.render.filepath = OUT
scene.view_settings.view_transform = "AgX"
scene.view_settings.look = "AgX - Medium High Contrast"
scene.render.image_settings.color_depth = "8"
scene.render.film_transparent = False
scene.world.color = (0.72, 0.77, 0.63)

def principled(name, color, roughness=0.38, metallic=0.0, subsurface=0.0, transmission=0.0):
    mat = bpy.data.materials.new(name)
    mat.diffuse_color = (*color, 1)
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes.get("Principled BSDF")
    bsdf.inputs["Base Color"].default_value = (*color, 1)
    bsdf.inputs["Roughness"].default_value = roughness
    bsdf.inputs["Metallic"].default_value = metallic
    bsdf.inputs["Subsurface Weight"].default_value = subsurface
    bsdf.inputs["Transmission Weight"].default_value = transmission
    return mat

def noisy_skin(name, base, roughness, scale, bump_strength, subsurface=0.0):
    mat = principled(name, base, roughness, subsurface=subsurface)
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    bsdf = nodes.get("Principled BSDF")
    noise = nodes.new("ShaderNodeTexNoise")
    noise.inputs["Scale"].default_value = scale
    noise.inputs["Detail"].default_value = 3.0
    noise.inputs["Roughness"].default_value = 0.72
    bump = nodes.new("ShaderNodeBump")
    bump.inputs["Strength"].default_value = bump_strength
    bump.inputs["Distance"].default_value = 0.035
    links.new(noise.outputs["Fac"], bump.inputs["Height"])
    links.new(bump.outputs["Normal"], bsdf.inputs["Normal"])
    return mat

cream = noisy_skin("Honed charcoal island stone", (0.19, 0.18, 0.16), 0.28, 5.0, 0.08)
brick_mat = principled("Handmade red brick", (0.34, 0.105, 0.048), 0.86)
cabinet_mat = principled("Charcoal painted cabinetry", (0.055, 0.065, 0.067), 0.29, metallic=0.08)
steel_mat = principled("Blackened steel framing", (0.025, 0.031, 0.034), 0.25, metallic=0.72)
brass_mat = principled("Warm brushed brass hardware", (0.42, 0.26, 0.10), 0.27, metallic=0.78)
leaf_mat = noisy_skin("Aloe skin | waxy, mottled green", (0.095, 0.22, 0.065), 0.25, 13.0, 0.17, 0.08)
leaf_edge_mat = principled("Aloe serrations", (0.34, 0.48, 0.12), 0.3, subsurface=0.03)
gel_mat = principled("Fresh aloe gel", (0.48, 0.73, 0.30), 0.19, subsurface=0.23, transmission=0.24)
lemon_mat = noisy_skin("Lemon peel", (0.93, 0.56, 0.055), 0.35, 34.0, 0.25, 0.05)
lime_mat = noisy_skin("Lime peel", (0.29, 0.49, 0.07), 0.32, 36.0, 0.22, 0.05)
pith_mat = principled("Citrus pith", (0.89, 0.79, 0.55), 0.66, subsurface=0.06)
pulp_mat = principled("Citrus pulp", (1.0, 0.65, 0.16), 0.3, subsurface=0.2, transmission=0.07)
juice_mat = principled("Apple aloe juice", (0.28, 0.49, 0.13), 0.16, transmission=0.8)
glass_mat = principled("Clear bottle glass", (0.85, 0.92, 0.82), 0.08, transmission=0.98)
label_mat = principled("Unbranded paper label", (0.91, 0.88, 0.77), 0.7)
water_mat = principled("Water droplets", (0.86, 0.96, 1.0), 0.055, transmission=0.96)

def smooth(obj):
    if obj.type == "MESH":
        for poly in obj.data.polygons:
            poly.use_smooth = True
    return obj

def uv_sphere(name, location, scale, material, segments=48, rings=32):
    bpy.ops.mesh.primitive_uv_sphere_add(segments=segments, ring_count=rings, location=location)
    obj = bpy.context.object
    obj.name = name
    obj.scale = scale
    obj.data.materials.append(material)
    return smooth(obj)

def cylinder_between(name, a, b, radius, material, vertices=20):
    delta = Vector(b) - Vector(a)
    mid = (Vector(a) + Vector(b)) / 2
    bpy.ops.mesh.primitive_cylinder_add(vertices=vertices, radius=radius, depth=delta.length, location=mid)
    obj = bpy.context.object
    obj.name = name
    obj.rotation_mode = "QUATERNION"
    obj.rotation_quaternion = delta.to_track_quat("Z", "Y")
    obj.data.materials.append(material)
    return smooth(obj)

# Industrial kitchen island, exposed brick, charcoal cabinetry and steel framing.
bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0, -0.15))
table = bpy.context.object
table.name = "Charcoal stone kitchen island"
table.dimensions = (7.2, 3.8, 0.28)
bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
table.data.materials.append(cream)

brick = bpy.data.materials.new("Warm handmade brick with pale mortar")
brick.use_nodes = True
brick_nodes = brick.node_tree.nodes
brick_links = brick.node_tree.links
brick_bsdf = brick_nodes.get("Principled BSDF")
brick_tex = brick_nodes.new("ShaderNodeTexBrick")
brick_tex.inputs["Color1"].default_value = (.37, .12, .055, 1)
brick_tex.inputs["Color2"].default_value = (.20, .065, .035, 1)
brick_tex.inputs["Mortar"].default_value = (.30, .27, .22, 1)
brick_tex.inputs["Scale"].default_value = 3.2
brick_tex.inputs["Mortar Size"].default_value = .025
brick_tex.inputs["Mortar Smooth"].default_value = .015
brick_bump = brick_nodes.new("ShaderNodeBump")
brick_bump.inputs["Strength"].default_value = .22
brick_bump.inputs["Distance"].default_value = .055
brick_links.new(brick_tex.outputs["Color"], brick_bsdf.inputs["Base Color"])
brick_links.new(brick_tex.outputs["Fac"], brick_bump.inputs["Height"])
brick_links.new(brick_bump.outputs["Normal"], brick_bsdf.inputs["Normal"])

# Vertical brick wall behind the preparation island.
bpy.ops.mesh.primitive_plane_add(size=1, location=(0, 2.4, 2.0), rotation=(math.radians(90), 0, 0))
wall = bpy.context.object
wall.name = "Exposed brick kitchen wall"
wall.dimensions = (10.5, 4.5, 1)
bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
wall.data.materials.append(brick)

def box(name, location, dimensions, material, bevel=0.0):
    bpy.ops.mesh.primitive_cube_add(size=1, location=location)
    obj = bpy.context.object
    obj.name = name
    obj.dimensions = dimensions
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    obj.data.materials.append(material)
    if bevel:
        modifier = obj.modifiers.new("Soft manufactured edges", "BEVEL")
        modifier.width = bevel
        modifier.segments = 3
        obj.modifiers.new("Weighted corner normals", "WEIGHTED_NORMAL")
    return obj

# Cabinet fronts and slim metal handles establish the industrial kitchen set.
for x in (-2.45, -1.15, 0.15, 1.45, 2.65):
    box("Charcoal island cabinet", (x, -1.57, -0.70), (1.20, .72, .82), cabinet_mat, .045)
    box("Brushed metal drawer pull", (x, -1.955, -0.43), (.42, .035, .045), brass_mat, .018)
box("Back counter cabinet run", (0.0, 2.0, .40), (6.7, .52, .90), cabinet_mat, .04)
box("Back worktop", (0.0, 1.68, .88), (7.1, 1.1, .12), cream, .025)

# Black steel rails and glazing echo the window framing in the user's reference.
for x in (-3.65, -2.05, -.45, 1.15, 2.75, 3.65):
    box("Steel window mullion", (x, 2.30, 2.70), (.055, .065, 3.0), steel_mat)
for z in (1.22, 2.70, 4.15):
    box("Steel window crossbar", (0.0, 2.30, z), (7.3, .065, .055), steel_mat)

# Pendant shades are visible over the set; light itself is focused downward.
for x in (-1.75, .15, 2.0):
    cylinder_between("Pendant suspension", (x, .88, 3.86), (x, .88, 3.42), .018, steel_mat, 12)
    bpy.ops.mesh.primitive_cone_add(vertices=40, radius1=.34, radius2=.10, depth=.25, location=(x, .88, 3.32))
    shade = bpy.context.object
    shade.name = "Black industrial pendant shade"
    shade.data.materials.append(steel_mat)

# Aloe leaf is the hero: a custom lofted, gently cupped blade with a sliced end.
length = 3.45
sections = 96
around = 28
verts, faces = [], []
for i in range(sections + 1):
    t = i / sections
    x = -length * 0.5 + length * t
    taper = max(0.025, math.sin(math.pi * (0.05 + 0.9 * t)) ** 0.72)
    width = 0.045 + 0.48 * taper
    thickness = 0.035 + 0.14 * taper
    center_z = 0.12 + 0.27 * math.sin(math.pi * t) + 0.10 * t
    for j in range(around):
        angle = math.tau * j / around
        y = width * math.cos(angle)
        z = center_z + thickness * math.sin(angle) - 0.09 * (y / max(width, 0.001)) ** 2
        verts.append((x, y, z))
for i in range(sections):
    for j in range(around):
        a = i * around + j
        b = i * around + (j + 1) % around
        c = (i + 1) * around + (j + 1) % around
        d = (i + 1) * around + j
        faces.append((a, b, c, d))
faces.append(tuple(range(around - 1, -1, -1)))
mesh = bpy.data.meshes.new("Aloe leaf sculpted loft")
mesh.from_pydata(verts, [], faces)
mesh.materials.append(leaf_mat)
leaf = bpy.data.objects.new("Hero aloe vera leaf", mesh)
bpy.context.collection.objects.link(leaf)
smooth(leaf)
leaf.rotation_euler[2] = math.radians(18)
leaf.location = (-0.15, -0.2, 0.0)
bpy.context.view_layer.update()

# Cut end: an ivory-green rind ring and translucent gel centre.
cut_x = -length * 0.5
cut_y = leaf.location.y
cut_z = 0.12 + 0.10 * 0.0 + 0.005
ring_verts = [(cut_x, 0.0, 0.0)]
for radius_y, radius_z in ((0.19, 0.09), (0.12, 0.064)):
    for j in range(40):
        a = math.tau * j / 40
        ring_verts.append((cut_x, radius_y * math.cos(a), cut_z + radius_z * math.sin(a)))
ring_verts.append((cut_x, 0.0, cut_z))
ring_faces = []
for j in range(40):
    ring_faces.append((1 + j, 1 + (j + 1) % 40, 41 + (j + 1) % 40, 41 + j))
    ring_faces.append((81, 41 + j, 41 + (j + 1) % 40))
ring_mesh = bpy.data.meshes.new("Fresh cut aloe cross-section")
ring_mesh.from_pydata(ring_verts, [], ring_faces)
ring_mesh.materials.append(leaf_edge_mat)
ring_mesh.materials.append(gel_mat)
for index, poly in enumerate(ring_mesh.polygons):
    poly.material_index = 1 if index % 2 else 0
cap = bpy.data.objects.new("Aloe cut face with clear gel", ring_mesh)
bpy.context.collection.objects.link(cap)
cap.location = leaf.location
cap.rotation_euler[2] = leaf.rotation_euler[2]

# Fine, regularly spaced aloe leaf teeth along both edges.
for side in (-1, 1):
    for i in range(4, 91, 4):
        t = i / 96
        x = -length * 0.5 + length * t
        w = 0.045 + 0.48 * max(0.025, math.sin(math.pi * (0.05 + 0.9 * t)) ** 0.72)
        z = 0.12 + 0.27 * math.sin(math.pi * t) + 0.10 * t
        bpy.ops.mesh.primitive_cone_add(vertices=9, radius1=0.035, radius2=0.0, depth=0.11, location=(x, side * w, z))
        tooth = bpy.context.object
        tooth.name = "Aloe leaf fine serration"
        tooth.rotation_euler[0] = math.radians(-side * 70)
        tooth.data.materials.append(leaf_edge_mat)
        smooth(tooth)
        tooth.location = leaf.matrix_world @ Vector((x, side * w, z))

# Tiny dew beads catch the large softbox highlights.
for _ in range(56):
    t = random.uniform(0.12, 0.91)
    x = -length * 0.5 + length * t
    w = 0.045 + 0.48 * max(0.025, math.sin(math.pi * (0.05 + 0.9 * t)) ** 0.72)
    y = random.uniform(-w * 0.68, w * 0.68)
    z = 0.12 + 0.27 * math.sin(math.pi * t) + 0.10 * t + 0.035 + random.random() * 0.07
    drop_position = leaf.matrix_world @ Vector((x, y, z))
    uv_sphere("Aloe dew", drop_position, (0.018, 0.014, 0.026), water_mat, 16, 12)

# A supporting lime and lemon half, kept softly out of the hero focal plane.
def citrus_half(name, center, radius, peel, rotation=(0, 0, 0)):
    body = uv_sphere(name + " rind", center, (radius, radius, radius * 0.38), peel, 48, 32)
    body.rotation_euler = rotation
    face_z = center[2] + radius * 0.38
    bpy.ops.mesh.primitive_cylinder_add(vertices=64, radius=radius * 0.88, depth=0.025, location=(center[0], center[1], face_z))
    cut = bpy.context.object
    cut.name = name + " pith cut face"
    cut.data.materials.append(pith_mat)
    for poly in cut.data.polygons:
        poly.use_smooth = True
    bpy.ops.mesh.primitive_cylinder_add(vertices=64, radius=radius * 0.73, depth=0.012, location=(center[0], center[1], face_z + 0.017))
    pulp = bpy.context.object
    pulp.name = name + " juicy flesh"
    pulp.data.materials.append(pulp_mat)
    return body

citrus_half("Lemon", (-1.9, 0.65, 0.22), 0.52, lemon_mat, (0.12, 0.1, -0.25))
citrus_half("Lime", (-1.15, 1.15, 0.20), 0.42, lime_mat, (0.05, -0.12, 0.3))

# Temporary concept bottle, no logo or final brand system.
def lathe(name, x, y, profile, material, segments=64):
    verts, faces = [], []
    for radius, z in profile:
        for j in range(segments):
            a = math.tau * j / segments
            verts.append((x + radius * math.cos(a), y + radius * math.sin(a), z))
    for i in range(len(profile) - 1):
        for j in range(segments):
            a = i * segments + j
            b = i * segments + (j + 1) % segments
            c = (i + 1) * segments + (j + 1) % segments
            d = (i + 1) * segments + j
            faces.append((a, b, c, d))
    mesh = bpy.data.meshes.new(name + " turned surface")
    mesh.from_pydata(verts, [], faces)
    mesh.materials.append(material)
    obj = bpy.data.objects.new(name, mesh)
    bpy.context.collection.objects.link(obj)
    smooth(obj)
    return obj

bx, by = 1.85, 0.6
bottle_profile = [(0.0, .1), (.31, .1), (.38, .16), (.4, .25), (.4, 1.08), (.37, 1.22), (.27, 1.33), (.17, 1.39), (.16, 1.62), (.18, 1.66), (.18, 1.71), (.13, 1.73), (.13, 1.77)]
lathe("Unbranded clear glass bottle", bx, by, bottle_profile, glass_mat)
lathe("Green juice in bottle", bx, by, [(0,.11),(.29,.11),(.34,.17),(.34,.82),(.32,.9),(0,.9)], juice_mat)
lathe("Temporary blank paper label", bx, by, [(.402,.48),(.405,.49),(.405,.82),(.402,.83)], label_mat)
uv_sphere("Glass bottle cap", (bx, by, 1.78), (.14, .14, .07), cream, 32, 16)

# Focused warm downlights over the island with gentle neutral fill.
def area_light(name, location, energy, size, color, target):
    data = bpy.data.lights.new(name, "AREA")
    data.energy = energy
    data.shape = "DISK"
    data.size = size
    data.color = color
    obj = bpy.data.objects.new(name, data)
    bpy.context.collection.objects.link(obj)
    obj.location = location
    obj.rotation_euler = (Vector(target) - obj.location).to_track_quat("-Z", "Y").to_euler()
    return obj

area_light("Pendant downlight left", (-1.75, .88, 3.18), 520, 1.15, (1.0, .69, .40), (-.5, 0, .3))
area_light("Pendant downlight centre", (.15, .88, 3.18), 620, 1.05, (1.0, .78, .52), (0, 0, .3))
area_light("Pendant downlight right", (2.0, .88, 3.18), 560, 1.10, (1.0, .72, .44), (.8, .2, .4))
area_light("Soft front fill", (0.0, -4.0, 3.4), 170, 4.0, (.74, .82, 1.0), (0, 0, .5))

# Dim warm kitchen ambience; product visibility comes from the overhead fixtures.
world = bpy.data.worlds.new("Industrial kitchen ambience") if not bpy.data.worlds else bpy.data.worlds[0]
scene.world = world
world.use_nodes = True
world.node_tree.nodes["Background"].inputs["Color"].default_value = (.13, .095, .065, 1)
world.node_tree.nodes["Background"].inputs["Strength"].default_value = .22

camera_data = bpy.data.cameras.new("Aloe beauty camera")
camera = bpy.data.objects.new("Aloe beauty camera", camera_data)
bpy.context.collection.objects.link(camera)
camera.location = (1.8, -8.5, 4.7)
target = Vector((0.05, 0.1, 0.7))
camera.rotation_euler = (target - camera.location).to_track_quat("-Z", "Y").to_euler()
camera_data.lens = 52
camera_data.dof.use_dof = True
camera_data.dof.focus_object = leaf
camera_data.dof.aperture_fstop = 5.6
scene.camera = camera

# A landscape product crop that keeps the kitchen visible behind the aloe.
scene.render.resolution_x = 1440
scene.render.resolution_y = 1080
scene.render.resolution_percentage = 100
scene.camera.data.lens = 43
scene.render.filepath = OUT

# Save the editable project, then render the proof frame.
bpy.ops.wm.save_as_mainfile(filepath=BLEND)
bpy.ops.render.render(write_still=True)
print("Rendered Juicebuilder aloe look test to", OUT)
