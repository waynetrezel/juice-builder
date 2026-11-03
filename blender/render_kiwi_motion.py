"""Render the saved kiwi look test as a compact motion review sequence."""
import bpy
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCENE_FILE = ROOT / "kiwi-lookdev-v1.blend"
FRAME_DIR = ROOT / "renders" / "kiwi-lookdev" / "motion-frames"
FRAME_DIR.mkdir(parents=True, exist_ok=True)

bpy.ops.wm.open_mainfile(filepath=str(SCENE_FILE))
scene = bpy.context.scene
scene.render.resolution_x = 640
scene.render.resolution_y = 440
scene.render.resolution_percentage = 100
scene.cycles.samples = 10
scene.cycles.use_denoising = True
scene.render.image_settings.file_format = "PNG"
scene.render.image_settings.color_mode = "RGB"

count = 72
single = bpy.app.driver_namespace.get("JUICEBUILDER_SINGLE_FRAME")
if single is None:
    import os
    single = os.environ.get("JUICEBUILDER_SINGLE_FRAME")
indices = [int(single)] if single is not None else range(count)
for index in indices:
    timeline_frame = round(scene.frame_start + index * (scene.frame_end - scene.frame_start) / (count - 1))
    scene.frame_set(timeline_frame)
    scene.render.filepath = str(FRAME_DIR / ("frame-%03d.png" % index))
    bpy.ops.render.render(write_still=True)
    print("Kiwi motion %02d/%02d · timeline frame %d" % (index + 1, count, timeline_frame), flush=True)
print("Rendered motion frames:", FRAME_DIR)
