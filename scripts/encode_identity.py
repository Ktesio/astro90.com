"""Encode the Cycles frame sequence as a single-play, transparent WebP.

Requires Pillow. Render assets/blender/build_identity.py -- --render first.
"""
from pathlib import Path
import shutil
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / '.local/identity-frames'
frames = []
for number in range(1, 97):
    with Image.open(SOURCE / f'frame_{number:04}.png') as image:
        frame = image.convert('RGBA')
        assert frame.size == (960, 960), f'Wrong frame size: {number}'
        bounds = frame.getchannel('A').getbbox()
        if bounds:
            assert min(bounds[0], bounds[1], 960-bounds[2], 960-bounds[3]) >= 40, f'Clipped frame: {number}'
        frames.append(frame)
output = ROOT / 'static/media/monogram-build.webp'
delivery = [frame.resize((720, 720), Image.Resampling.LANCZOS) for frame in frames]
delivery[0].save(output, save_all=True, append_images=delivery[1:], duration=[33, 33, 34] * 32,
                 loop=1, quality=80, method=4)
frames[-1].save(ROOT / 'static/media/monogram.webp', quality=92, method=6)
shutil.copy2(SOURCE / 'frame_0096.png', ROOT / 'assets/renders/monogram.png')
with Image.open(output) as animation:
    assert animation.info['loop'] == 1, 'The construction must play once'
    assert animation.n_frames > 40, 'The construction frames are missing'
    duration = 0
    for number in range(animation.n_frames):
        animation.seek(number)
        animation.load()
        duration += animation.info['duration']
    assert duration == 3200, f'Unexpected timing: {duration}'
    print(f'{animation.n_frames} encoded frames, {duration} ms, one play, {output.stat().st_size / 1024 / 1024:.2f} MiB')
