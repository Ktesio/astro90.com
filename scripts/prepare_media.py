"""Create delivery WebPs from the committed original artwork. Requires Pillow.

This is format/size optimization only; design sources stay intact.
The normal Zola build uses the committed WebPs and does not need Python.
"""
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
MEDIA = ROOT / "static" / "media"

sources = sorted((ROOT / "assets/source/products").iterdir()) + [ROOT / "assets/renders/monogram.png"]
for source in sources:
    if source.suffix.lower() not in {".png", ".jpg"}:
        continue
    with Image.open(source) as original:
        image = original.convert("RGBA" if "A" in original.getbands() else "RGB")
        image.save(MEDIA / (source.stem + ".webp"), "WEBP", quality=88, method=6)
    print(f"{source.name} → {source.stem}.webp")

# Preserve the painting's composition; object-fit supplies responsive crops.
with Image.open(ROOT / "assets/source/studio/night-coast.png") as original:
    for width in (1643, 960):
        delivery = original.convert("RGB")
        delivery.thumbnail((width, width), Image.Resampling.LANCZOS)
        path = MEDIA / f"night-coast-{width}.webp"
        delivery.save(path, "WEBP", quality=88, method=6)
        print(f"night-coast.png → {path.name}")
