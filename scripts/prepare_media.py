"""Create delivery WebPs from the committed original artwork. Requires Pillow.

This is format/size optimization only; design sources stay intact.
The normal Zola build uses the committed WebPs and does not need Python.
"""
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
MEDIA = ROOT / "static" / "media"

sources = sorted((ROOT / "assets/source/products").iterdir()) + sorted((ROOT / "assets/renders").iterdir())
for source in sources:
    if source.suffix.lower() not in {".png", ".jpg"}:
        continue
    with Image.open(source) as original:
        image = original.convert("RGBA" if "A" in original.getbands() else "RGB")
        image.save(MEDIA / (source.stem + ".webp"), "WEBP", quality=88, method=6)
    print(f"{source.name} → {source.stem}.webp")
