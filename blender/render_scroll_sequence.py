"""Render evenly spaced story frames for a scroll-driven image sequence."""
import bpy
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCENE_FILE = ROOT / "juicebuilder-story-animatic.blend"
FRAME_DIR = ROOT / "renders" / "scroll-sequence"
FRAME_DIR.mkdir(parents=True, exist_ok=True)
COUNT = 45

bpy.ops.wm.open_mainfile(filepath=str(SCENE_FILE))
scene = bpy.context.scene
scene.render.resolution_x = 480
scene.render.resolution_y = 600
scene.render.resolution_percentage = 100
scene.cycles.samples = 8
scene.cycles.use_denoising = True
scene.render.image_settings.file_format = "PNG"
scene.render.image_settings.color_mode = "RGB"

start, end = scene.frame_start, scene.frame_end
frames = [round(start + i * (end - start) / (COUNT - 1)) for i in range(COUNT)]
for index, frame in enumerate(frames):
    scene.frame_set(frame)
    scene.render.filepath = str(FRAME_DIR / ("frame-%03d.png" % index))
    bpy.ops.render.render(write_still=True)
    print("Scroll sequence %02d/%02d · timeline frame %d" % (index + 1, COUNT, frame), flush=True)
print("Rendered sequence frames to:", FRAME_DIR)
