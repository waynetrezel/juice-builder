"""Inspect downloaded Poly Haven glTF object bounds before animatic integration."""
import bpy
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
aloe_file = ROOT / "assets" / "aloe" / "aloe-leaf-web.glb"
if aloe_file.exists():
    bpy.ops.object.select_all(action="SELECT")
    bpy.ops.object.delete(use_global=False)
    bpy.ops.import_scene.gltf(filepath=str(aloe_file))
    print("ASSET aloe-leaf-web.glb")
    for obj in bpy.context.scene.objects:
        if obj.type == "MESH":
            print("  MESH", obj.name, "dim", tuple(round(v, 4) for v in obj.dimensions), "scale", tuple(round(v, 3) for v in obj.scale))
for folder in sorted((ROOT / "assets" / "ingredients").iterdir()):
    files = list(folder.glob("*.gltf"))
    if not files:
        continue
    bpy.ops.object.select_all(action="SELECT")
    bpy.ops.object.delete(use_global=False)
    bpy.ops.import_scene.gltf(filepath=str(files[0]))
    print("ASSET", folder.name)
    for obj in bpy.context.scene.objects:
        if obj.type == "MESH":
            print("  MESH", obj.name, "dim", tuple(round(v, 4) for v in obj.dimensions), "scale", tuple(round(v, 3) for v in obj.scale))
