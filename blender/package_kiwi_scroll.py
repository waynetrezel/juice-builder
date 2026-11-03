"""Compress the rendered kiwi pilot into frames for reversible scroll playback."""
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
SOURCE = ROOT / "renders" / "kiwi-lookdev" / "motion-frames"
DESTINATION = ROOT / "story-site" / "assets" / "kiwi" / "scroll"
DESTINATION.mkdir(parents=True, exist_ok=True)

frames = sorted(SOURCE.glob("frame-*.png"))
if len(frames) != 72:
    raise RuntimeError(f"Expected 72 rendered kiwi frames, found {len(frames)}")

total = 0
for index, source in enumerate(frames):
    destination = DESTINATION / f"frame-{index:03d}.webp"
    with Image.open(source) as image:
        image.convert("RGB").save(destination, "WEBP", quality=58, method=6)
    total += destination.stat().st_size

print(f"Wrote {len(frames)} scroll frames to {DESTINATION}")
print(f"Total compressed size: {total / 1024 / 1024:.2f} MiB")
