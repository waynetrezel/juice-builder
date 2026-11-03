"""Package the rendered kiwi still and motion frames for the local review page."""
from pathlib import Path
from PIL import Image, ImageDraw
import shutil
import subprocess

ROOT = Path(__file__).resolve().parent.parent
RENDERS = ROOT / "renders" / "kiwi-lookdev"
FRAMES = RENDERS / "motion-frames"
WEB = ROOT / "story-site" / "assets" / "kiwi"
WEB.mkdir(parents=True, exist_ok=True)

still = Image.open(RENDERS / "kiwi-lookdev-hero-v1.png").convert("RGB")
still.save(WEB / "kiwi-hero-v6.webp", "WEBP", quality=86, method=6)

frame_paths = sorted(FRAMES.glob("frame-*.png"))
if len(frame_paths) != 72:
    raise RuntimeError("Expected 72 kiwi motion frames, found %d" % len(frame_paths))

ffmpeg = shutil.which("ffmpeg")
if ffmpeg is None:
    raise RuntimeError("ffmpeg is needed to package the kiwi motion preview")
subprocess.run([
    ffmpeg, "-hide_banner", "-loglevel", "error", "-y", "-framerate", "12",
    "-i", str(FRAMES / "frame-%03d.png"), "-c:v", "libx264", "-crf", "23",
    "-pix_fmt", "yuv420p", "-movflags", "+faststart",
    str(WEB / "kiwi-motion-v6.mp4"),
], check=True)

preview_indices = (0, 12, 24, 36, 48, 60, 71)
thumb_w, thumb_h, gap = 320, 220, 12
sheet = Image.new("RGB", (thumb_w * 4 + gap * 5, thumb_h * 2 + gap * 3), "#171a16")
draw = ImageDraw.Draw(sheet)
for slot, index in enumerate(preview_indices):
    thumb = Image.open(FRAMES / ("frame-%03d.png" % index)).convert("RGB")
    thumb.thumbnail((thumb_w, thumb_h), Image.Resampling.LANCZOS)
    x = gap + (slot % 4) * (thumb_w + gap)
    y = gap + (slot // 4) * (thumb_h + gap)
    sheet.paste(thumb, (x, y))
    draw.text((x + 8, y + 8), "%02d / 72" % (index + 1), fill="#f2f2ea")
sheet.save(RENDERS / "kiwi-motion-contact.png", optimize=True)

print("Kiwi still:", WEB / "kiwi-hero-v6.webp")
print("Kiwi motion:", WEB / "kiwi-motion-v6.mp4")
print("Motion contact:", RENDERS / "kiwi-motion-contact.png")
