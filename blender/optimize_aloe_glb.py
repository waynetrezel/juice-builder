"""Create a compact web copy of the original Hi3D aloe GLB.

Run from the project root with Blender 5.2:
  blender -b --python blender/optimize_aloe_glb.py

The source download is preserved. This creates a 175k-triangle GLB with 2K
textures and Draco mesh compression for the website.
"""
import bpy
import json
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SOURCE = ROOT / "assets" / "aloe" / "Hi3D_Untitled_allparts_20261026_014833.glb"
OUTPUT = ROOT / "assets" / "aloe" / "aloe-leaf-web.glb"

# Start with a clean scene so Blender's default cube is not exported.
bpy.ops.object.select_all(action="SELECT")
bpy.ops.object.delete(use_global=False)
bpy.ops.import_scene.gltf(filepath=str(SOURCE))
meshes = [obj for obj in bpy.context.scene.objects if obj.type == "MESH"]

for obj in meshes:
    if len(obj.data.polygons) > 250_000:
        modifier = obj.modifiers.new(name="Web detail reduction", type="DECIMATE")
        modifier.ratio = 0.035
        bpy.context.view_layer.objects.active = obj
        bpy.ops.object.modifier_apply(modifier=modifier.name)

for image in bpy.data.images:
    if image.size[0] > 2048 or image.size[1] > 2048:
        image.scale(2048, 2048)

bpy.ops.object.select_all(action="DESELECT")
for obj in meshes:
    obj.select_set(True)
if meshes:
    bpy.context.view_layer.objects.active = meshes[0]

properties = bpy.ops.export_scene.gltf.get_rna_type().properties.keys()
options = {
    "filepath": str(OUTPUT),
    "export_format": "GLB",
    "use_selection": True,
    "export_apply": True,
}
if "export_draco_mesh_compression_enable" in properties:
    options["export_draco_mesh_compression_enable"] = True
    if "export_draco_mesh_compression_level" in properties:
        options["export_draco_mesh_compression_level"] = 6

bpy.ops.export_scene.gltf(**options)
for obj in meshes:
    obj.data.calc_loop_triangles()
print(
    "Optimized aloe GLB: "
    + json.dumps(
        {
            "output": str(OUTPUT),
            "bytes": os.path.getsize(OUTPUT),
            "meshes": [
                {
                    "name": obj.name,
                    "vertices": len(obj.data.vertices),
                    "triangles": len(obj.data.loop_triangles),
                }
                for obj in meshes
            ],
            "texture_sizes": [list(image.size) for image in bpy.data.images if image.size[0] and image.size[1]],
            "draco": options.get("export_draco_mesh_compression_enable", False),
        },
        separators=(",", ":"),
    )
)
