"""Build a labeled contact sheet from the rendered animatic chapter frames."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent.parent
FRAME_DIR = ROOT / "renders" / "animatic"
OUTPUT = ROOT / "renders" / "juicebuilder-animatic-contact-sheet-v2.png"
WEB_ASSETS = ROOT / "story-site" / "assets" / "animatic"
WEB_ASSETS.mkdir(parents=True, exist_ok=True)
chapters = [
    ("00-kitchen.png", "THE KITCHEN"), ("01-lemon.png", "01 / LEMON"),
    ("02-lime.png", "02 / LIME"), ("03-apple.png", "03 / APPLE"),
    ("04-aloe-vera.png", "04 / ALOE VERA"), ("05-kiwi.png", "05 / KIWI"),
    ("06-dandelion.png", "06 / DANDELION"), ("07-okra.png", "07 / OKRA"),
    ("08-whirl.png", "THE WHIRL"), ("09-blend.png", "THE BLEND"),
    ("10-pour.png", "THE POUR"),
]

columns = 3
cell_w, cell_h = 260, 370
gap = 18
top = 82
rows = (len(chapters) + columns - 1) // columns
canvas = Image.new("RGB", (columns * cell_w + (columns + 1) * gap, top + rows * cell_h + (rows + 1) * gap), "#171a16")
draw = ImageDraw.Draw(canvas)
font_path = Path("C:/Windows/Fonts/arial.ttf")
title_font = ImageFont.truetype(str(font_path), 22) if font_path.exists() else ImageFont.load_default()
label_font = ImageFont.truetype(str(font_path), 14) if font_path.exists() else ImageFont.load_default()
draw.text((gap, 22), "JUICEBUILDER / STORY ANIMATIC", font=title_font, fill="#eef0e6")
draw.text((canvas.width - 220, 29), "LOW-DETAIL BLOCKOUT", font=label_font, fill="#d5e267")

for index, (filename, label) in enumerate(chapters):
    source = Image.open(FRAME_DIR / filename).convert("RGB")
    source.thumbnail((cell_w, cell_h - 26), Image.Resampling.LANCZOS)
    web_name = Path(filename).stem + ".webp"
    Image.open(FRAME_DIR / filename).convert("RGB").save(WEB_ASSETS / web_name, "WEBP", quality=82, method=6)
    col, row = index % columns, index // columns
    x, y = gap + col * (cell_w + gap), top + gap + row * (cell_h + gap)
    canvas.paste(source, (x, y))
    draw.rectangle((x, y + cell_h - 25, x + cell_w, y + cell_h), fill="#23271f")
    draw.text((x + 8, y + cell_h - 21), label, font=label_font, fill="#eef0e6")

canvas.save(OUTPUT, optimize=True)
print("Saved contact sheet:", OUTPUT)
print("Saved optimized website animatic frames:", WEB_ASSETS)
