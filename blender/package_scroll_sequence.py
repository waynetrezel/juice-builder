"""Compress rendered scroll frames for the local website and make a contact sheet."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent.parent
SOURCE = ROOT / "renders" / "scroll-sequence"
WEB = ROOT / "story-site" / "assets" / "sequence"
WEB.mkdir(parents=True, exist_ok=True)
count = 45
thumb_w, thumb_h, cols = 144, 180, 9
gap, top = 10, 38
rows = (count + cols - 1) // cols
sheet = Image.new("RGB", (cols * thumb_w + (cols + 1) * gap, top + rows * thumb_h + (rows + 1) * gap), "#171a16")
draw = ImageDraw.Draw(sheet)
font = ImageFont.truetype("C:/Windows/Fonts/arial.ttf", 15) if Path("C:/Windows/Fonts/arial.ttf").exists() else ImageFont.load_default()
draw.text((gap, 10), "JUICEBUILDER / 45-FRAME SCROLL STUDY", font=font, fill="#eef0e6")
for index in range(count):
    image = Image.open(SOURCE / ("frame-%03d.png" % index)).convert("RGB")
    image.save(WEB / ("frame-%03d.webp" % index), "WEBP", quality=82, method=6)
    image.thumbnail((thumb_w, thumb_h), Image.Resampling.LANCZOS)
    x = gap + (index % cols) * (thumb_w + gap)
    y = top + gap + (index // cols) * (thumb_h + gap)
    sheet.paste(image, (x, y))
sheet.save(ROOT / "renders" / "juicebuilder-scroll-sequence-contact.png", optimize=True)
total = sum(path.stat().st_size for path in WEB.glob("*.webp"))
print("Compressed 45 frames to", WEB, "(%0.2f MB)" % (total / (1024 * 1024)))
print("Contact sheet:", ROOT / "renders" / "juicebuilder-scroll-sequence-contact.png")
