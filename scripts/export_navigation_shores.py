"""Regenerate convex navigation shorelines from the illustrated PNG alpha."""
import json
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]


def convex_hull(points):
    points = sorted(set(points))

    def cross(o, a, b):
        return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])

    def half(sequence):
        result = []
        for point in sequence:
            while len(result) >= 2 and cross(result[-2], result[-1], point) <= 0:
                result.pop()
            result.append(point)
        return result

    return half(points)[:-1] + half(reversed(points))[:-1]


shorelines = {}
for path in sorted((ROOT / "assets/source/navigation").glob("*.png")):
    with Image.open(path) as image:
        alpha = image.getchannel("A")
        width, height = image.size
        # Exclude the transparent lighting fringe; keep the solid shore and rocks.
        points = [(x, y) for y in range(0, height, 4) for x in range(0, width, 4)
                  if alpha.getpixel((x, y)) >= 200]
    shorelines[path.stem] = [[round(x / width, 5), round(y / height, 5)]
                            for x, y in convex_hull(points)]

(ROOT / "data/navigation-shores.json").write_text(json.dumps(shorelines, indent=2) + "\n")
print(f"Exported {len(shorelines)} navigation shorelines.")
