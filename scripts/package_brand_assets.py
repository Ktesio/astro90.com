"""Package the committed digital assets without any image-tool dependencies."""
import json
from pathlib import Path
import zipfile

ROOT = Path(__file__).resolve().parents[1]
exports = json.loads((ROOT / "assets/brand/exports.json").read_text())
files = {name: ROOT / "static" / name for name in exports}
files["site.webmanifest"] = ROOT / "static/site.webmanifest"
files["README.md"] = ROOT / "docs/WEB-ASSETS.md"
destination = ROOT / "static/brand/astro90-asset-kit.zip"
with zipfile.ZipFile(destination, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
    for name, source in sorted(files.items()):
        info = zipfile.ZipInfo(name, date_time=(1980, 1, 1, 0, 0, 0))
        info.compress_type = zipfile.ZIP_DEFLATED
        info.external_attr = 0o644 << 16
        archive.writestr(info, source.read_bytes())
print(f"Packaged {len(files)} files; {destination.stat().st_size:,} bytes.")
