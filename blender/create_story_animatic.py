"""Build and render a low-detail Juicebuilder motion study in Blender.

Run from the project root:
  blender -b --python blender/create_story_animatic.py

The scene is a timing and staging prototype. Geometry is intentionally simple;
it is not the final photoreal ingredient or liquid work.
"""
import bpy
import math
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BASE = ROOT / "aloe-story-shot-v2.blend"
OUTPUT = ROOT / "juicebuilder-story-animatic.blend"
FRAME_DIR = ROOT / "renders" / "animatic"
FRAME_DIR.mkdir(parents=True, exist_ok=True)

bpy.ops.wm.open_mainfile(filepath=str(BASE))
scene = bpy.context.scene

# Keep the industrial kitchen set and replace the experimental leaf with clear proxies.
for obj in list(scene.objects):
    if obj.name.startswith("Aloe leaf | Hi3D"):
        bpy.data.objects.remove(obj, do_unlink=True)

scene.camera.data.dof.use_dof = False
scene.camera.location = (-3.25, -7.0, 3.45)
target = (0.0, -0.2, 0.65)
from mathutils import Matrix, Vector
direction = Vector(target) - scene.camera.location
scene.camera.rotation_euler = direction.to_track_quat("-Z", "Y").to_euler()
scene.camera.data.lens = 58

# A soft preview key and fill keep the blockout readable without changing the set.
def area_light(name, location, power, size, color):
    data = bpy.data.lights.new(name, "AREA")
    data.energy = power
    data.shape = "DISK"
    data.size = size
    data.color = color
    obj = bpy.data.objects.new(name, data)
    bpy.context.collection.objects.link(obj)
    obj.location = location
    obj.rotation_euler = (Vector((0, 0, 0.5)) - obj.location).to_track_quat("-Z", "Y").to_euler()

area_light("Animatic softbox key", (-2.2, -2.2, 4.1), 220, 3.6, (1.0, 0.78, 0.52))
area_light("Animatic camera fill", (2.8, -3.6, 3.0), 100, 3.0, (0.7, 0.82, 1.0))

def material(name, color, roughness=0.38, metallic=0.0, transmission=0.0, texture_scale=0, pore_scale=0):
    mat = bpy.data.materials.get(name) or bpy.data.materials.new(name)
    mat.diffuse_color = (*color, 1.0)
    mat.use_nodes = True
    shader = mat.node_tree.nodes.get("Principled BSDF")
    shader.inputs["Roughness"].default_value = roughness
    shader.inputs["Metallic"].default_value = metallic
    if "Specular IOR Level" in shader.inputs:
        shader.inputs["Specular IOR Level"].default_value = 0.3 if texture_scale else 0.22
    if "Transmission Weight" in shader.inputs:
        shader.inputs["Transmission Weight"].default_value = transmission
    nodes, links = mat.node_tree.nodes, mat.node_tree.links
    if texture_scale:
        texcoord = nodes.new("ShaderNodeTexCoord")
        noise = nodes.new("ShaderNodeTexNoise")
        noise.inputs["Scale"].default_value = texture_scale
        noise.inputs["Detail"].default_value = 3.0
        noise.inputs["Roughness"].default_value = 0.72
        ramp = nodes.new("ShaderNodeValToRGB")
        dark = tuple(component * 0.72 for component in color) + (1.0,)
        light = tuple(min(component * 1.18 + 0.012, 1.0) for component in color) + (1.0,)
        ramp.color_ramp.elements[0].position = 0.19
        ramp.color_ramp.elements[0].color = dark
        ramp.color_ramp.elements[1].position = 0.82
        ramp.color_ramp.elements[1].color = light
        links.new(texcoord.outputs["Generated"], noise.inputs["Vector"])
        links.new(noise.outputs["Fac"], ramp.inputs["Fac"])
        links.new(ramp.outputs["Color"], shader.inputs["Base Color"])
        if pore_scale:
            pores = nodes.new("ShaderNodeTexVoronoi")
            pores.inputs["Scale"].default_value = pore_scale
            bump = nodes.new("ShaderNodeBump")
            bump.inputs["Strength"].default_value = 0.28
            bump.inputs["Distance"].default_value = 0.018
            links.new(texcoord.outputs["Generated"], pores.inputs["Vector"])
            links.new(pores.outputs["Distance"], bump.inputs["Height"])
            links.new(bump.outputs["Normal"], shader.inputs["Normal"])
    else:
        shader.inputs["Base Color"].default_value = (*color, 1.0)
    return mat

MAT = {
    "lemon": material("Animatic · citrus yellow", (0.58, 0.22, 0.002), 0.72, texture_scale=42, pore_scale=175),
    "lime": material("Animatic · lime green", (0.08, 0.3, 0.02), 0.68, texture_scale=44, pore_scale=190),
    "apple": material("Animatic · apple green", (0.16, 0.34, 0.025), 0.62, texture_scale=18, pore_scale=130),
    "aloe": material("Animatic · aloe green", (0.2, 0.48, 0.1), 0.3, texture_scale=28, pore_scale=110),
    "kiwi": material("Animatic · kiwi skin", (0.42, 0.19, 0.065), 0.75, texture_scale=24, pore_scale=230),
    "dandelion": material("Animatic · dandelion yellow", (0.92, 0.48, 0.008), 0.6, texture_scale=8),
    "leaf": material("Animatic · leaf green", (0.15, 0.35, 0.05), 0.45, texture_scale=24, pore_scale=90),
    "okra": material("Animatic · okra green", (0.18, 0.39, 0.045), 0.42, texture_scale=36, pore_scale=120),
    "cut": material("Animatic · fresh cut", (0.68, 0.8, 0.34), 0.55, texture_scale=35, pore_scale=130),
    "pith": material("Animatic · pale citrus pith", (0.82, 0.72, 0.48), 0.58, texture_scale=24, pore_scale=60),
    "lemon_flesh": material("Animatic · lemon flesh", (0.92, 0.66, 0.16), 0.5, texture_scale=22, pore_scale=70),
    "lime_flesh": material("Animatic · lime flesh", (0.7, 0.76, 0.25), 0.5, texture_scale=22, pore_scale=70),
    "apple_flesh": material("Animatic · apple flesh", (0.83, 0.69, 0.42), 0.52, texture_scale=18, pore_scale=55),
    "kiwi_flesh": material("Animatic · kiwi flesh", (0.32, 0.58, 0.1), 0.5, texture_scale=26, pore_scale=75),
    "seed": material("Animatic · fruit seeds", (0.16, 0.075, 0.022), 0.42, texture_scale=16, pore_scale=40),
    "glass": material("Animatic · clear vessel glass", (0.88, 0.94, 0.91), 0.055, 0.0, 0.96),
    "juice": material("Animatic · green juice", (0.12, 0.4, 0.025), 0.24, transmission=0.08, texture_scale=10, pore_scale=80),
    "steel": material("Animatic · blender steel", (0.12, 0.14, 0.13), 0.24, 0.72),
    "cap": material("Animatic · bottle caps", (0.68, 0.75, 0.25), 0.3, 0.1),
}

def smooth(obj):
    if obj.type == "MESH":
        for poly in obj.data.polygons:
            poly.use_smooth = True
    return obj

def parent_keep_world(obj, parent):
    obj.parent = parent
    obj.matrix_parent_inverse = parent.matrix_world.inverted()
    return obj

def clear_children(parent):
    for child in list(parent.children_recursive):
        bpy.data.objects.remove(child, do_unlink=True)

def import_ingredient(asset_id, parent, target_center, target_size, mesh_name_contains=None):
    """Import a licensed glTF, normalize its bounds, and parent it for story animation."""
    path = ROOT / "assets" / "ingredients" / asset_id / (asset_id + "_2k.gltf")
    if not path.exists():
        raise FileNotFoundError("Missing CC0 ingredient model: " + str(path))
    before = set(bpy.data.objects)
    bpy.ops.import_scene.gltf(filepath=str(path))
    imported = [obj for obj in bpy.data.objects if obj not in before and obj.type == "MESH"]
    if mesh_name_contains:
        selected = [obj for obj in imported if mesh_name_contains in obj.name]
        for obj in imported:
            if obj not in selected:
                bpy.data.objects.remove(obj, do_unlink=True)
        imported = selected
    if not imported:
        raise RuntimeError("No mesh objects imported from " + str(path))
    corners = [obj.matrix_world @ Vector(corner) for obj in imported for corner in obj.bound_box]
    minimum = Vector((min(p[i] for p in corners) for i in range(3)))
    maximum = Vector((max(p[i] for p in corners) for i in range(3)))
    center = (minimum + maximum) * 0.5
    dimensions = maximum - minimum
    factor = target_size / max(dimensions)
    anchor = empty("CC0 asset · " + asset_id)
    for obj in imported:
        parent_keep_world(obj, anchor)
    parent_keep_world(anchor, parent)
    anchor.scale = (factor, factor, factor)
    anchor.location = Vector(target_center) - center * factor
    return anchor

def mesh_object(name, verts, faces, mat, parent=None):
    mesh = bpy.data.meshes.new(name + " mesh")
    mesh.from_pydata(verts, [], faces)
    mesh.materials.append(mat)
    mesh.update()
    obj = bpy.data.objects.new(name, mesh)
    bpy.context.collection.objects.link(obj)
    smooth(obj)
    if parent:
        parent_keep_world(obj, parent)
    return obj

def sphere(name, location, scale, mat, parent=None, subdivisions=2):
    bpy.ops.mesh.primitive_uv_sphere_add(segments=20, ring_count=12, location=location)
    obj = bpy.context.object
    obj.name = name
    obj.scale = scale
    obj.data.materials.append(mat)
    smooth(obj)
    if subdivisions:
        mod = obj.modifiers.new("Proxy smoothness", "SUBSURF")
        mod.levels = subdivisions
        mod.render_levels = subdivisions
    if parent:
        parent_keep_world(obj, parent)
    return obj

def produce(name, location, scale, mat, kind):
    """Higher-resolution, subtly asymmetric produce silhouette."""
    bpy.ops.mesh.primitive_uv_sphere_add(segments=48, ring_count=32, location=location)
    obj = bpy.context.object
    obj.name = name
    for v in obj.data.vertices:
        x, y, z = v.co
        if kind == "citrus":
            radial = 1.0 + 0.035 * math.cos(5 * math.atan2(y, x)) * (1 - abs(z))
            v.co.x *= radial * (1 + 0.07 * abs(z))
            v.co.y *= radial * (1 + 0.07 * abs(z))
            v.co.z *= 0.88
        elif kind == "apple":
            lobes = math.cos(5 * math.atan2(y, x))
            v.co.x *= 1.0 + 0.055 * lobes * max(z, 0) ** 2
            v.co.y *= 1.0 + 0.055 * lobes * max(z, 0) ** 2
            if z > 0.72: v.co.z -= 0.10 * ((z - 0.72) / 0.28) ** 2
            if z < -0.75: v.co.z += 0.07 * ((-z - 0.75) / 0.25) ** 2
        elif kind == "kiwi":
            v.co.x *= 1.0 + 0.035 * math.sin(4 * math.atan2(y, x))
            v.co.z *= 0.90
        v.co.x *= scale[0]; v.co.y *= scale[1]; v.co.z *= scale[2]
    obj.data.materials.append(mat)
    smooth(obj)
    return obj

def cylinder(name, location, radius, depth, mat, parent=None, vertices=20, radius_top=None):
    if radius_top is None:
        bpy.ops.mesh.primitive_cylinder_add(vertices=vertices, radius=radius, depth=depth, location=location)
    else:
        bpy.ops.mesh.primitive_cone_add(vertices=vertices, radius1=radius, radius2=radius_top, depth=depth, location=location)
    obj = bpy.context.object
    obj.name = name
    obj.data.materials.append(mat)
    smooth(obj)
    bevel = obj.modifiers.new("Soft proxy edge", "BEVEL")
    bevel.width = 0.035
    bevel.segments = 2
    obj.modifiers.new("Proxy normals", "WEIGHTED_NORMAL")
    if parent:
        parent_keep_world(obj, parent)
    return obj

def empty(name, parent=None):
    obj = bpy.data.objects.new(name, None)
    bpy.context.collection.objects.link(obj)
    if parent:
        parent_keep_world(obj, parent)
    return obj

def key(obj, frame, *, location=None, scale=None, rotation=None):
    if location is not None:
        obj.location = location
        obj.keyframe_insert(data_path="location", frame=frame)
    if scale is not None:
        obj.scale = scale
        obj.keyframe_insert(data_path="scale", frame=frame)
    if rotation is not None:
        obj.rotation_euler = rotation
        obj.keyframe_insert(data_path="rotation_euler", frame=frame)

def leaf_mesh(name, length, width, mat, parent, z=0):
    verts = []
    faces = []
    steps = 28
    for i in range(steps + 1):
        t = i / steps
        y = (t - 0.5) * length
        w = width * (math.sin(math.pi * t) ** 0.7) * (0.76 + 0.24 * t)
        ridge = 0.11 * math.sin(math.pi * t)
        verts.extend([(-w, y, z), (0, y, z + ridge), (w, y, z)])
        if i < steps:
            base = i * 3
            nxt = base + 3
            faces.extend([(base, base + 1, nxt + 1, nxt), (base + 1, base + 2, nxt + 2, nxt + 1)])
    obj = mesh_object(name, verts, faces, mat, parent)
    if "Aloe leaf proxy" in name:
        solid = obj.modifiers.new("Fleshy aloe thickness", "SOLIDIFY")
        solid.thickness = 0.065
        smooth_mod = obj.modifiers.new("Aloe surface smoothness", "SUBSURF")
        smooth_mod.levels = 1
        smooth_mod.render_levels = 1
    return obj

def okra_pod(name, parent, center=(0, 0, 0.55), length=1.2, radius=0.2, material_ref=None):
    """Ribbed, gently curved okra pod with a tapered tip and five ridges."""
    verts, faces = [], []
    rings, segments = 36, 40
    for i in range(rings + 1):
        t = i / rings
        x = (t - 0.5) * length
        taper = 1.0 - 0.94 * (t ** 5)
        r = (0.13 + 0.07 * math.sin(math.pi * t)) * taper
        cy = 0.035 * math.sin(math.pi * t)
        cz = 0.024 * math.sin(math.pi * t * 1.2)
        for j in range(segments):
            angle = math.tau * j / segments
            rib = 1.0 + 0.075 * math.cos(8 * angle)
            irregular = 1.0 + 0.012 * math.sin(angle * 3 + t * 8)
            rr = r * rib * irregular
            verts.append((x, cy + rr * math.cos(angle), cz + rr * math.sin(angle)))
            if i < rings:
                a = i * segments + j
                b = i * segments + (j + 1) % segments
                c = (i + 1) * segments + (j + 1) % segments
                d = (i + 1) * segments + j
                faces.append((a, b, c, d))
    pod = mesh_object(name, verts, faces, material_ref or MAT["okra"], parent)
    pod.location = center
    # A small woody stem and star-shaped green calyx anchor the pod.
    stem = cylinder(name + " stem", (-length * 0.54, 0, 0), 0.045, 0.18, MAT["leaf"], parent, 10, 0.035)
    stem.rotation_euler[1] = math.pi / 2
    stem.location = (center[0] - length * 0.52, center[1], center[2])
    for i in range(5):
        angle = math.tau * i / 5
        sepal = sphere(name + " calyx point %d" % i,
                       (center[0] - length * 0.42, center[1] + math.cos(angle) * radius * 0.62, center[2] + math.sin(angle) * radius * 0.62),
                       (0.10, 0.035, 0.035), MAT["leaf"], parent, 0)
        sepal.rotation_euler[0] = angle
    return pod

def okra_slice(name, center, parent):
    """Five-lobed cross section with pale flesh and visible seed beads."""
    verts, faces = [(0, 0, 0)], []
    segments, r = 40, 0.135
    for i in range(segments):
        a = math.tau * i / segments
        rr = r * (1.0 + 0.16 * math.cos(8 * a))
        verts.append((0, math.cos(a) * rr, math.sin(a) * rr))
    for i in range(segments):
        faces.append((0, i + 1, (i + 1) % segments + 1))
    outer = mesh_object(name + " ribbed rind", verts, faces, MAT["okra"], parent)
    outer.location = center
    inside_verts = [(0, 0, 0)] + [(0, math.cos(math.tau*i/segments)*r*0.72, math.sin(math.tau*i/segments)*r*0.72) for i in range(segments)]
    inside = mesh_object(name + " cut flesh", inside_verts, faces, MAT["cut"], parent)
    inside.location = (center[0] + 0.004, center[1], center[2])
    for i in range(5):
        a = math.tau * i / 5
        seed = sphere(name + " seed %d" % i,
                      (center[0] + 0.009, center[1] + math.cos(a)*r*0.39, center[2] + math.sin(a)*r*0.39),
                      (0.009, 0.018, 0.018), MAT["cap"], parent, 0)
    return outer

def fruit_chunk(name, location, scale, skin, flesh, parent, kind=None):
    """Ellipsoid fruit segment with a modeled peel, pith and fresh cut surface."""
    cut_x = 0.48
    around, axial = 32, 14
    verts, faces, material_ids = [(-scale[0], 0, 0)], [], []
    rings = []
    for step in range(1, axial + 1):
        x = -0.97 + (cut_x + 0.97) * (step - 1) / (axial - 1)
        radius = math.sqrt(max(0.0, 1.0 - x * x))
        ring = []
        for side in range(around):
            angle = math.tau * side / around
            ring.append(len(verts))
            verts.append((x * scale[0], math.cos(angle) * radius * scale[1],
                          math.sin(angle) * radius * scale[2]))
        rings.append(ring)
    for side in range(around):
        faces.append((0, rings[0][(side + 1) % around], rings[0][side]))
        material_ids.append(0)
    for first, second in zip(rings, rings[1:]):
        for side in range(around):
            nxt = (side + 1) % around
            faces.append((first[side], first[nxt], second[nxt], second[side]))
            material_ids.append(0)

    # Concentric cut face: juicy centre, pale pith, then the colored peel rim.
    center = len(verts)
    verts.append((cut_x * scale[0] + 0.001, 0, 0))
    radius = math.sqrt(1.0 - cut_x * cut_x)
    cap_rings = []
    for fraction in (0.76, 0.9, 1.0):
        ring = []
        for side in range(around):
            angle = math.tau * side / around
            ring.append(len(verts))
            verts.append((cut_x * scale[0] + 0.001,
                          math.cos(angle) * radius * scale[1] * fraction,
                          math.sin(angle) * radius * scale[2] * fraction))
        cap_rings.append(ring)
    for side in range(around):
        faces.append((center, cap_rings[0][side], cap_rings[0][(side + 1) % around]))
        material_ids.append(2)
    for ring_index, mat_index in ((0, 1), (1, 0)):
        first, second = cap_rings[ring_index], cap_rings[ring_index + 1]
        for side in range(around):
            nxt = (side + 1) % around
            faces.append((first[side], second[side], second[nxt], first[nxt]))
            material_ids.append(mat_index)

    piece = mesh_object(name, verts, faces, skin, parent)
    piece.location = location
    piece.data.materials.append(MAT["pith"])
    piece.data.materials.append(flesh)
    for polygon, material_index in zip(piece.data.polygons, material_ids):
        polygon.material_index = material_index
    if kind in ("kiwi", "apple"):
        count = 10 if kind == "kiwi" else 2
        for seed_index in range(count):
            if kind == "kiwi":
                angle = math.tau * seed_index / count + 0.12 * math.sin(seed_index * 2.1)
                radial = 0.42 + 0.08 * math.sin(seed_index * 3.7)
            else:
                angle = 0.55 + seed_index * math.pi
                radial = 0.18
            y = math.cos(angle) * radius * scale[1] * radial
            z = math.sin(angle) * radius * scale[2] * radial
            sphere(name + " · seed %02d" % seed_index,
                   (location[0] + cut_x * scale[0] + 0.006, location[1] + y, location[2] + z),
                   (0.004, 0.008 if kind == "kiwi" else 0.01, 0.004), MAT["seed"], parent, 0)
    return piece

def lathe_vessel(name, center, profile, mat, parent, segments=64):
    """Revolve a radial-height shell profile into a smooth closed vessel mesh."""
    verts, faces = [], []
    for radius, z in profile:
        for i in range(segments):
            a = math.tau * i / segments
            verts.append((radius * math.cos(a), radius * math.sin(a), z))
    for ring in range(len(profile) - 1):
        for i in range(segments):
            a = ring * segments + i
            b = ring * segments + (i + 1) % segments
            c = (ring + 1) * segments + (i + 1) % segments
            d = (ring + 1) * segments + i
            faces.append((a, b, c, d))
    obj = mesh_object(name, verts, faces, mat, parent)
    obj.location = center
    bevel = obj.modifiers.new("Glass edge glints", "BEVEL")
    bevel.width = 0.012
    bevel.segments = 3
    obj.modifiers.new("Weighted glass normals", "WEIGHTED_NORMAL")
    return obj

def pourable_liquid(name, parent, radius, bottom, top, mat):
    # Rounded meniscus-like lip with a subtly domed top.
    profile = [(0.001, bottom), (radius * 0.94, bottom), (radius, bottom + 0.025),
               (radius, top - 0.025), (radius * 0.97, top), (radius * 0.68, top + 0.006),
               (0.001, top - 0.018), (0.001, bottom)]
    return lathe_vessel(name, (0, 0, 0), profile, mat, parent, 48)

def make_group(name):
    root = empty(name)
    whole = empty(name + " · whole", root)
    pieces = empty(name + " · chopped", root)
    return root, whole, pieces

def make_citrus(name, mat, center, chopped_mat):
    root, whole, pieces = make_group(name)
    asset_id = "lemon" if "Lemon" in name else "food_lime_01"
    import_ingredient(asset_id, whole, center, 0.95)
    for i, pos in enumerate(((-0.2, -0.08, 0.0), (0.14, 0.02, 0.05), (0.0, 0.1, -0.08), (0.22, -0.12, -0.04))):
        kind = "lemon" if "Lemon" in name else "lime"
        fruit_chunk(name + " chopped piece %d" % i, pos, (0.23, 0.19, 0.18), mat, chopped_mat, pieces, kind)
    return root, whole, pieces

ingredients = []
# Each item is deliberately a distinct group so the layout is easy to replace with real assets.
root, whole, pieces = make_citrus("01 · Lemon", MAT["lemon"], (0, 0, 0.45), MAT["lemon_flesh"])
ingredients.append((root, whole, pieces, "lemon"))
root, whole, pieces = make_citrus("02 · Lime", MAT["lime"], (0, 0, 0.45), MAT["lime_flesh"])
ingredients.append((root, whole, pieces, "lime"))

root, whole, pieces = make_group("03 · Apple")
import_ingredient("food_apple_01", whole, (0, 0, 0.47), 0.95)
for i, pos in enumerate(((-0.16, -0.05, 0), (0.14, 0.05, 0.03), (0, 0.13, -0.08), (0.22, -0.11, -0.02))):
    fruit_chunk("Apple chopped piece %d" % i, pos, (0.22, 0.2, 0.18), MAT["apple"], MAT["apple_flesh"], pieces, "apple")
ingredients.append((root, whole, pieces, "apple"))

root, whole, pieces = make_group("04 · Aloe vera")
aloe_asset = ROOT / "assets" / "aloe" / "aloe-leaf-web.glb"
if aloe_asset.exists():
    before = set(bpy.data.objects)
    bpy.ops.import_scene.gltf(filepath=str(aloe_asset))
    aloe_meshes = [obj for obj in bpy.data.objects if obj not in before and obj.type == "MESH"]
    for obj in aloe_meshes:
        parent_keep_world(obj, whole)
    all_corners = [obj.matrix_world @ Vector(corner) for obj in aloe_meshes for corner in obj.bound_box]
    low = Vector((min(p[i] for p in all_corners) for i in range(3)))
    high = Vector((max(p[i] for p in all_corners) for i in range(3)))
    aloe_center = (low + high) * 0.5
    factor = 1.42 / max(high - low)
    aloe_anchor = empty("Hi3D aloe leaf · single leaf, no roots")
    for obj in aloe_meshes:
        parent_keep_world(obj, aloe_anchor)
    parent_keep_world(aloe_anchor, whole)
    aloe_anchor.scale = (factor, factor, factor)
    aloe_anchor.location = Vector((0, 0, 0.55)) - aloe_center * factor
else:
    leaf_mesh("Aloe leaf proxy", 1.4, 0.46, MAT["aloe"], whole, 0.06)
for i in range(4):
    leaf_mesh("Aloe chopped piece %d" % i, 0.32, 0.13, MAT["aloe"], pieces, 0.06)
    pieces.children[-1].location.x = (i % 2) * 0.18 - 0.1
    pieces.children[-1].location.y = (i // 2) * 0.2 - 0.1
ingredients.append((root, whole, pieces, "aloe"))

root, whole, pieces = make_group("05 · Kiwi")
import_ingredient("food_kiwi_01", whole, (0, 0, 0.43), 0.85)
for i, pos in enumerate(((-0.15, -0.1, 0), (0.12, 0.12, 0.02), (0.0, -0.18, 0.06), (0.2, -0.03, -0.08))):
    fruit_chunk("Kiwi chopped piece %d" % i, pos, (0.21, 0.19, 0.18), MAT["kiwi"], MAT["kiwi_flesh"], pieces, "kiwi")
ingredients.append((root, whole, pieces, "kiwi"))

root, whole, pieces = make_group("06 · Dandelion")
import_ingredient("dandelion_01", whole, (0, 0, 0.58), 1.12, "dandelion_01_a_LOD0")
for i in range(4):
    leaf_mesh("Dandelion chopped leaf %d" % i, 0.24, 0.09, MAT["leaf"], pieces, 0.08)
ingredients.append((root, whole, pieces, "dandelion"))

root, whole, pieces = make_group("07 · Okra")
okra_pod("Okra · ribbed pod", whole)
for i, pos in enumerate(((-0.18, -0.05, 0.0), (0.15, 0.04, 0.04), (0, 0.16, -0.06), (0.22, -0.12, -0.02))):
    okra_slice("Okra cross-section %d" % i, pos, pieces)
ingredients.append((root, whole, pieces, "okra"))

# One ingredient takes the hero position, then breaks into simple chunks and joins the spiral.
for index, (root, whole, pieces, label) in enumerate(ingredients):
    enter = 16 + index * 18
    hero = enter + 6
    swirl = enter + 12
    angle = (index / len(ingredients)) * math.tau
    hero_location = (-0.25, -0.55, 0.0)
    orbit_location = (math.cos(angle) * 0.62, -0.85 + math.sin(angle) * 0.28, 0.38 + index * 0.13)
    root.scale = (0, 0, 0)
    key(root, enter - 1, scale=(0, 0, 0), location=(-2.6, -0.4, 0.65))
    hero_scale = 1.05 if label in ("aloe", "dandelion") else 1.45
    key(root, enter, scale=(0.4, 0.4, 0.4), location=(-2.6, -0.4, 0.65))
    key(root, hero, scale=(hero_scale, hero_scale, hero_scale), location=hero_location, rotation=(0, 0, angle))
    phase = angle + (swirl - 118) * 0.23
    start_radius = 0.86
    spiral_location = (math.cos(phase) * start_radius, -0.82 + math.sin(phase) * 0.5,
                       0.55 + index * 0.07 + math.sin(phase) * 0.28)
    key(root, swirl, scale=(0.82, 0.82, 0.82), location=spiral_location, rotation=(0.2, 0.2, phase))
    for orbit_frame in range(max(swirl + 4, 140), 171, 4):
        t = max(0.0, min(1.0, (orbit_frame - 140) / 31))
        orbit_phase = angle + (orbit_frame - 118) * 0.23
        radius = 0.86 - t * 0.48
        center_x = t * 1.05
        center_y = -0.82 + t * 0.5
        orbit_location = (center_x + math.cos(orbit_phase) * radius,
                          center_y + math.sin(orbit_phase) * 0.5,
                          0.55 + index * 0.07 + t * 0.35 + math.sin(orbit_phase) * 0.28)
        orbit_scale = 0.82 - t * 0.14
        key(root, orbit_frame, scale=(orbit_scale, orbit_scale, orbit_scale),
            location=orbit_location, rotation=(0.2 + t * 0.4, 0.2, orbit_phase))
    key(root, 174, scale=(0, 0, 0), location=(1.15, -0.15, 1.65))
    key(whole, enter - 1, scale=(1, 1, 1))
    key(whole, swirl - 1, scale=(1, 1, 1))
    key(whole, swirl, scale=(0, 0, 0))
    key(pieces, enter - 1, scale=(0, 0, 0))
    key(pieces, swirl - 1, scale=(0, 0, 0))
    key(pieces, swirl, scale=(1, 1, 1))
    key(pieces, 174, scale=(1, 1, 1))

# A glass pitcher, removable lid and motor base enter after the final ingredient.
blender_root = empty("Blender appliance · proxy")
pitcher = empty("Blender pitcher assembly", blender_root)
pitcher.location = (1.48, -0.1, 0.34)
jar_profile = [(0.001, 0.02), (0.37, 0.02), (0.405, 0.06), (0.405, 0.76),
               (0.39, 1.02), (0.42, 1.08), (0.42, 1.12), (0.385, 1.12),
               (0.37, 1.06), (0.365, 0.09), (0.001, 0.07), (0.001, 0.02)]
jar = lathe_vessel("Blender glass pitcher · thick rim", (0, 0, 0), jar_profile, MAT["glass"], pitcher)
jar_base = cylinder("Blender motor base", (1.48, -0.1, 0.17), 0.47, 0.29, MAT["steel"], blender_root, 48)
base_ring = cylinder("Blender base · lower trim", (1.48, -0.1, 0.055), 0.47, 0.045, MAT["cap"], blender_root, 48)
jar_lid = cylinder("Blender lid", (1.48, -0.1, 1.50), 0.405, 0.09, MAT["steel"], pitcher, 48)
lid_insert = cylinder("Blender lid · center plug", (1.48, -0.1, 1.56), 0.115, 0.035, MAT["cap"], pitcher, 32)
liquid = pourable_liquid("Fresh green juice in pitcher", pitcher, 0.34, 0.08, 0.72, MAT["juice"])
liquid.location = (1.48, -0.1, 0.34)
# A rounded handle follows the pitcher's right side and rotates with the pour.
handle_data = bpy.data.curves.new("Blender pitcher handle curve", "CURVE")
handle_data.dimensions = "3D"
handle_data.bevel_depth = 0.038
handle_data.bevel_resolution = 4
spline = handle_data.splines.new("BEZIER")
spline.bezier_points.add(3)
for point, co in zip(spline.bezier_points, ((0.38, 0, 0.88), (0.69, 0, 0.79), (0.7, 0, 0.32), (0.38, 0, 0.23))):
    point.co = co
    point.handle_left_type = "AUTO"
    point.handle_right_type = "AUTO"
handle = bpy.data.objects.new("Blender handle · dark polymer", handle_data)
bpy.context.collection.objects.link(handle)
handle.data.materials.append(MAT["steel"])
handle.parent = pitcher
handle.matrix_parent_inverse = Matrix.Identity(4)
handle.location = (0, 0, 0)
# One restrained control dial helps sell the appliance silhouette.
dial = cylinder("Blender control dial", (1.48, -0.575, 0.20), 0.085, 0.035, MAT["cap"], blender_root, 32)
dial.rotation_euler[0] = math.radians(90)
key(blender_root, 1, scale=(0, 0, 0))
key(blender_root, 156, scale=(0, 0, 0), location=(0, 0, 0))
key(blender_root, 168, scale=(1, 1, 1), location=(0, 0, 0))
key(liquid, 174, scale=(1, 0, 1))
key(liquid, 189, scale=(1, 0, 1))
key(liquid, 195, scale=(1, 1, 1))
key(pitcher, 205, rotation=(0, 0, 0))
key(pitcher, 218, rotation=(0, -0.68, 0))
key(pitcher, 246, rotation=(0, -0.68, 0))
key(pitcher, 254, rotation=(0, 0, 0))
key(liquid, 219, scale=(1, 1, 1))
key(liquid, 246, scale=(1, 1, 0.56))

# Clear, deliberately unbranded takeaway bottles with shoulders and threaded necks.
bottle_root = empty("Bottle lineup · clear glass concept")
for index, x in enumerate((-0.75, 0.05, 0.85)):
    bottle_profile = [(0.001, 0.04), (0.235, 0.04), (0.27, 0.075), (0.27, 0.67),
                      (0.25, 0.76), (0.14, 0.88), (0.115, 0.90), (0.115, 1.08),
                      (0.13, 1.10), (0.13, 1.13), (0.105, 1.13), (0.10, 0.92),
                      (0.22, 0.76), (0.225, 0.10), (0.001, 0.075), (0.001, 0.04)]
    body = lathe_vessel("Unbranded bottle %d · clear body" % index, (x, -0.65, 0.05), bottle_profile, MAT["glass"], bottle_root)
    cap = cylinder("Unbranded bottle %d cap" % index, (x, -0.65, 1.23), 0.137, 0.13, MAT["cap"], bottle_root, 40)
    fill = pourable_liquid("Green juice fill %d" % index, bottle_root, 0.212, 0.09, 0.63, MAT["juice"])
    fill.location.x = x
    fill.location.y = -0.65
    fill.location.z = 0.05
    if index == 1:
        key(cap, 218, location=(x, -0.65, 1.23), scale=(1, 1, 1))
        key(cap, 224, location=(x + 0.34, -0.65, 0.12), scale=(1, 1, 1))
        key(cap, 264, location=(x + 0.34, -0.65, 0.12), scale=(1, 1, 1))
key(bottle_root, 1, scale=(0, 0, 0))
key(bottle_root, 196, scale=(0, 0, 0))
key(bottle_root, 211, scale=(1, 1, 1))
key(bottle_root, 264, scale=(1, 1, 1))

# A curved green stream bridges the tilted pitcher and uncapped hero bottle.
stream_data = bpy.data.curves.new("Pour stream curve", "CURVE")
stream_data.dimensions = "3D"
stream_data.bevel_depth = 0.055
stream_data.bevel_resolution = 5
stream_spline = stream_data.splines.new("BEZIER")
stream_spline.bezier_points.add(3)
for point, co in zip(stream_spline.bezier_points, ((0.78, -0.1, 1.28), (0.62, -0.27, 1.48), (0.28, -0.48, 1.4), (0.05, -0.65, 1.18))):
    point.co = co
    point.handle_left_type = "AUTO"
    point.handle_right_type = "AUTO"
stream = bpy.data.objects.new("Pour stream · curved juice", stream_data)
bpy.context.collection.objects.link(stream)
stream.data.materials.append(MAT["juice"])
key(stream, 1, scale=(0, 0, 0))
key(stream, 207, scale=(0, 0, 0))
key(stream, 219, scale=(1, 1, 1))
key(stream, 246, scale=(1, 1, 1))
key(stream, 254, scale=(0, 0, 0))

# Keyframes use Blender's default smooth Bezier interpolation for a reversible scrub.
scene.frame_start = 1
scene.frame_end = 264
scene.render.fps = 24
scene.render.engine = "CYCLES"
scene.cycles.samples = 12
scene.cycles.use_denoising = True
scene.render.resolution_x = 720
scene.render.resolution_y = 900
scene.render.resolution_percentage = 100
scene.render.image_settings.file_format = "PNG"
scene.render.image_settings.color_mode = "RGB"
scene.render.filepath = str(FRAME_DIR / "frame-")
scene.render.film_transparent = False
scene.view_settings.view_transform = "AgX"
scene.view_settings.look = "AgX - Medium High Contrast"
scene.view_settings.exposure = 0.25
scene.render.image_settings.compression = 20
scene.use_preview_range = False
scene.frame_set(22)

chapter_frames = [
    (1, "00 · Kitchen"), (22, "01 · Lemon"), (40, "02 · Lime"), (58, "03 · Apple"),
    (76, "04 · Aloe vera"), (94, "05 · Kiwi"), (112, "06 · Dandelion"),
    (130, "07 · Okra"), (157, "08 · Whirl"), (195, "09 · Blend"), (230, "10 · Pour"),
]
for frame, label in chapter_frames:
    marker = scene.timeline_markers.new(label, frame=frame)
    marker.camera = scene.camera

# Select the primary actor on open so the timeline is easy to inspect.
bpy.ops.object.select_all(action="DESELECT")
ingredients[0][0].select_set(True)
bpy.context.view_layer.objects.active = ingredients[0][0]
bpy.ops.file.pack_all()
bpy.ops.wm.save_as_mainfile(filepath=str(OUTPUT))

# Render one low-resolution keyframe per scroll chapter for a storyboard contact sheet.
for frame, label in chapter_frames:
    only = os.environ.get("JUICEBUILDER_RENDER_ONLY")
    slug = label.lower().replace(" · ", "-").replace(" ", "-")
    if only and slug not in {part.strip() for part in only.split(",")}:
        continue
    scene.frame_set(frame)
    scene.render.filepath = str(FRAME_DIR / (slug + ".png"))
    bpy.ops.render.render(write_still=True)

print("Saved Juicebuilder animatic scene:", OUTPUT)
print("Rendered 11 proxy story frames to:", FRAME_DIR)
print("Timeline: 264 frames at 24 fps; ingredient entries begin at frames 16 through 124; whirl 156–174; blend 174–211; pour 211–264.")
