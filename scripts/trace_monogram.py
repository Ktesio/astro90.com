"""Optical vector reconstruction of the selected Studio Wordmark 04 a.

The proportions follow its 208 × 184 alpha silhouette. Quadratic curves remove
raster noise before extrusion. This is a drawn vector, not a font substitution.
"""
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]
commands = [
    ('M', [69, 0]), ('L', [141, 0]), ('Q', [208, 0, 208, 67]),
    ('L', [208, 166]), ('Q', [208, 184, 190, 184]), ('L', [161, 184]),
    ('Q', [144, 184, 144, 166]), ('L', [144, 78]), ('Q', [144, 60, 126, 60]),
    ('L', [84, 60]), ('Q', [65, 60, 65, 78]), ('L', [65, 106]),
    ('Q', [65, 125, 84, 125]), ('L', [115, 125]), ('Q', [136, 125, 136, 146]),
    ('L', [136, 167]), ('Q', [136, 184, 118, 184]), ('L', [69, 184]),
    ('Q', [0, 184, 0, 115]), ('L', [0, 70]), ('Q', [0, 0, 69, 0]),
]
points = []
for command, values in commands:
    if command in ('M', 'L'):
        points.append(values)
    else:
        start = points[-1]
        control, end = values[:2], values[2:]
        for step in range(1, 33):
            t = step / 32
            points.append([round((1-t)**2*start[i] + 2*(1-t)*t*control[i] + t*t*end[i], 4) for i in range(2)])
path = ' '.join(command + ' '.join(map(str, values)) for command, values in commands) + ' Z'
data = {'width': 208, 'height': 184, 'contours': [points[:-1]], 'path': path,
        'source': 'Optical vector reconstruction of selected Studio Wordmark 04 a.'}
(ROOT / 'assets/brand').mkdir(parents=True, exist_ok=True)
(ROOT / 'assets/brand/monogram.json').write_text(json.dumps(data, separators=(',', ':')) + '\n')
icon = f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><rect width="64" height="64" rx="14" fill="#F4C84C"/><path d="{path}" transform="translate(10 12.54) scale(.211538)" fill="#0B101A"/></svg>'
(ROOT / 'static/brand/monogram.svg').write_text(icon + '\n')
(ROOT / 'static/brand/favicon.svg').write_text(icon + '\n')
print(f'Selected a: {len(points)-1} smooth vertices')
