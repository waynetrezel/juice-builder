"""Build the first Juicebuilder aloe story shot using the generated Hi3D asset.

Run from the project root with Blender 5.2:
  blender -b --python blender/create_aloe_story_shot.py
"""
import bpy
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BASE = ROOT / "aloe-asset-pilot-v2.blend"
MODEL = ROOT / "assets" / "aloe" / "aloe-leaf-web.glb"
BLEND = ROOT / "aloe-story-shot-v2.blend"
RENDER = ROOT / "renders" / "aloe-story-shot-v2.png"

bpy.ops.wm.open_mainfile(filepath=str(BASE))
scene = bpy.context.scene

# Remove the earlier procedural aloe while retaining the kitchen, camera and lights.
for obj in list(scene.objects):
    if obj.type == "MESH" and obj.name.lower().startswith("aloe"):
        bpy.data.objects.remove(obj, do_unlink=True)

bpy.ops.import_scene.gltf(filepath=str(MODEL))
hero = next(obj for obj in scene.objects if obj.type == "MESH" and obj.name.startswith("geometry_"))
hero.name = "Aloe leaf | Hi3D web-ready"
hero.rotation_euler[2] = math.radians(90)
hero.scale = (3.55, 3.55, 3.55)
hero.location = (0.0, 0.0, 0.28)
bpy.context.view_layer.update()

# Richen the model's very bright scan texture without painting over its detail.
mat = bpy.data.materials.get("pbr_material")
if mat and mat.use_nodes:
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    bsdf = next((n for n in nodes if n.type == "BSDF_PRINCIPLED"), None)
    base_link = next((l for l in links if bsdf and l.to_node == bsdf and l.to_socket.name == "Base Color"), None)
    if base_link:
        source_node, source_socket = base_link.from_node, base_link.from_socket
        links.remove(base_link)
        hsv = nodes.new("ShaderNodeHueSaturation")
        hsv.name = "Food commercial color grade"
        hsv.label = "Tasteful green color grade"
        hsv.inputs["Hue"].default_value = 0.5
        hsv.inputs["Saturation"].default_value = 1.15
        hsv.inputs["Value"].default_value = 0.68
        links.new(source_socket, hsv.inputs["Color"])
        links.new(hsv.outputs["Color"], bsdf.inputs["Base Color"])

# Add a quiet row of charcoal cabinetry beneath the exposed brick backdrop.
black = bpy.data.materials.get("Blackened steel")
metal = bpy.data.materials.get("Warm pendant interior")
def box(name, location, dimensions, material, bevel=0.02):
    bpy.ops.mesh.primitive_cube_add(size=1, location=location)
    obj = bpy.context.object
    obj.name = name
    obj.dimensions = dimensions
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    obj.data.materials.append(material)
    if bevel:
        modifier = obj.modifiers.new("Soft manufactured edge", "BEVEL")
        modifier.width = bevel
        modifier.segments = 3
        obj.modifiers.new("Weighted corner normals", "WEIGHTED_NORMAL")
    return obj

box("Charcoal wall cabinet run", (0, 1.83, 0.38), (6.3, 0.78, 0.82), black, 0.035)
for i, x in enumerate((-2.35, -0.8, 0.8, 2.35)):
    door = box("Cabinet front %02d" % i, (x, 1.415, 0.39), (1.43, 0.055, 0.76), black, 0.018)
    handle = box("Brushed brass cabinet pull %02d" % i, (x + 0.47, 1.365, 0.39), (0.035, 0.035, 0.19), metal, 0.014)

# Make the background softer and warmer while keeping focused overhead pools.
brick = bpy.data.materials.get("Warm red brick")
if brick and brick.use_nodes:
    brick_tex = next((n for n in brick.node_tree.nodes if n.type == "TEX_BRICK"), None)
    if brick_tex:
        brick_tex.inputs["Color1"].default_value = (0.16, 0.047, 0.025, 1)
        brick_tex.inputs["Color2"].default_value = (0.09, 0.025, 0.016, 1)

for light in [o for o in scene.objects if o.type == "LIGHT"]:
    if light.name.startswith("Warm kitchen downlight"):
        light.data.energy *= 0.68
    elif light.name == "Soft cool camera fill":
        light.data.energy *= 0.58

scene.camera.data.dof.focus_object = hero
scene.camera.data.dof.aperture_fstop = 2.8
scene.render.engine = "CYCLES"
scene.cycles.samples = 64
scene.cycles.use_denoising = True
scene.render.resolution_x = 1500
scene.render.resolution_y = 1050
scene.render.resolution_percentage = 100
scene.render.image_settings.file_format = "PNG"
scene.render.image_settings.color_mode = "RGBA"
scene.render.filepath = str(RENDER)
scene.view_settings.view_transform = "AgX"
scene.view_settings.look = "AgX - Medium High Contrast"
scene.view_settings.exposure = -0.15

bpy.ops.object.select_all(action="DESELECT")
hero.select_set(True)
bpy.context.view_layer.objects.active = hero
bpy.ops.wm.save_as_mainfile(filepath=str(BLEND))
bpy.ops.render.render(write_still=True)
print("Saved Blender scene:", BLEND)
print("Rendered aloe story frame:", RENDER)
