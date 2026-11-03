"""Print the loaded ingredient asset transforms for debugging composition."""
import bpy
from pathlib import Path
from mathutils import Vector
root = Path(__file__).resolve().parent.parent
bpy.ops.wm.open_mainfile(filepath=str(root / "juicebuilder-story-animatic.blend"))
scene = bpy.context.scene
scene.frame_set(112)
for key in ("Dandelion", "Aloe", "Lemon", "Kiwi"):
    print("GROUP", key)
    for obj in scene.objects:
        if key.lower() in obj.name.lower() and obj.type == "EMPTY":
            print(" EMPTY", obj.name, "loc", tuple(round(v,3) for v in obj.location), "scale", tuple(round(v,3) for v in obj.scale), "parent", obj.parent.name if obj.parent else "none")
        if key.lower() in obj.name.lower() and obj.type == "MESH":
            corners = [obj.matrix_world @ Vector(c) for c in obj.bound_box]
            lo = Vector((min(v[i] for v in corners) for i in range(3)))
            hi = Vector((max(v[i] for v in corners) for i in range(3)))
            print(" ", obj.name, "bounds", tuple(round(v,2) for v in lo), tuple(round(v,2) for v in hi), "hide", obj.hide_render)
