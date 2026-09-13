"""Check a built static site without a browser or external dependencies."""
from collections import Counter
from html.parser import HTMLParser
from pathlib import Path
import re
import sys
import tomllib
from urllib.parse import unquote, urljoin, urlsplit

ROOT = Path(__file__).resolve().parents[1]
PUBLIC = ROOT / "public"
CONFIG = tomllib.loads((ROOT / "zola.toml").read_text())
ORIGIN = urlsplit(CONFIG["base_url"])
INTERNAL_HOSTS = {ORIGIN.hostname, "127.0.0.1", "localhost"}
ERRORS = []
EXPECTED = {
    "index.html", "404.html", "games/index.html", "games/lighthouse/index.html",
    "games/inkube/index.html", "apps/index.html", "apps/heronis/index.html",
    "apps/yanando/index.html", "open-source/index.html", "open-source/ktesio/index.html",
    "studio/index.html", "brand/index.html",
}


class Document(HTMLParser):
    def __init__(self, path):
        super().__init__()
        self.path = path
        self.ids = []
        self.refs = []
        self.h1 = 0
        self.main = 0
        self.in_title = False
        self.title = ""
        self.description = ""
        self.canonical = ""
        self.feed(path.read_text())

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if attrs.get("id"):
            self.ids.append(attrs["id"])
        if tag == "h1":
            self.h1 += 1
        if tag == "main":
            self.main += 1
        if tag == "title":
            self.in_title = True
        if tag == "meta" and attrs.get("name") == "description":
            self.description = attrs.get("content", "")
        if tag == "link" and attrs.get("rel") == "canonical":
            self.canonical = attrs.get("href", "")
        if tag == "img" and "alt" not in attrs:
            ERRORS.append(f"{self.path}: image has no alt attribute")
        for attr in ("href", "src", "data-gallery-src", "data-brand-film"):
            if attr in attrs:
                value = attrs[attr]
                if not value or value == "#":
                    ERRORS.append(f"{self.path}: empty {attr} on {tag}")
                else:
                    self.refs.append(value)
        for candidate in attrs.get("srcset", "").split(","):
            if candidate.strip():
                self.refs.append(candidate.split()[0])

    def handle_endtag(self, tag):
        if tag == "title":
            self.in_title = False

    def handle_data(self, value):
        if self.in_title:
            self.title += value


def resolve_reference(value, source):
    relative = source.relative_to(PUBLIC).as_posix()
    parsed = urlsplit(urljoin(f"{CONFIG['base_url']}/{relative}", value))
    if parsed.scheme in {"data", "mailto", "tel"}:
        return None, ""
    if parsed.scheme not in {"http", "https"}:
        ERRORS.append(f"{relative}: unsupported URL {value}")
        return None, ""
    if parsed.hostname not in INTERNAL_HOSTS:
        return None, ""
    target = PUBLIC / unquote(parsed.path).lstrip("/")
    if target.is_dir():
        target /= "index.html"
    if not target.is_file():
        ERRORS.append(f"{relative}: missing destination {value}")
        return None, ""
    return target, unquote(parsed.fragment)


documents = {p: Document(p) for p in sorted(PUBLIC.rglob("*.html"))}
generated = {p.relative_to(PUBLIC).as_posix() for p in documents}
for missing in EXPECTED - generated:
    ERRORS.append(f"Missing page: {missing}; run zola build first")

titles = Counter()
references = 0
for path, doc in documents.items():
    relative = path.relative_to(PUBLIC)
    if doc.h1 != 1 or doc.main != 1:
        ERRORS.append(f"{relative}: expected one h1 and one main, got {doc.h1}/{doc.main}")
    if not doc.title.strip() or not doc.description.strip():
        ERRORS.append(f"{relative}: missing title or description")
    titles[doc.title.strip()] += 1
    if relative.as_posix() != "404.html" and not doc.canonical:
        ERRORS.append(f"{relative}: missing canonical URL")
    for duplicate, count in Counter(doc.ids).items():
        if count > 1:
            ERRORS.append(f"{relative}: duplicate id {duplicate}")
    for value in doc.refs:
        references += 1
        target, fragment = resolve_reference(value, path)
        if target in documents and fragment and fragment not in documents[target].ids:
            ERRORS.append(f"{relative}: missing anchor in {value}")

for title, count in titles.items():
    if count > 1:
        ERRORS.append(f"Duplicate page title: {title}")

for stylesheet in PUBLIC.rglob("*.css"):
    for value in re.findall(r'url\([\s\'\"]*([^\)\'\"]+)', stylesheet.read_text()):
        references += 1
        resolve_reference(value.strip(), stylesheet)

# Protect the finite entrance from an accidental looping or truncated export.
# RIFF fields: https://developers.google.com/speed/webp/docs/riff_container
animation = PUBLIC / "media/monogram-build.webp"
if animation.is_file():
    data = animation.read_bytes()
    offset, frames, duration, loops = 12, 0, 0, None
    valid = data[:4] == b"RIFF" and data[8:12] == b"WEBP"
    valid = valid and int.from_bytes(data[4:8], "little") + 8 == len(data)
    while valid and offset + 8 <= len(data):
        kind = data[offset:offset + 4]
        length = int.from_bytes(data[offset + 4:offset + 8], "little")
        payload = data[offset + 8:offset + 8 + length]
        if len(payload) != length:
            valid = False
            break
        if kind == b"ANIM" and length == 6:
            loops = int.from_bytes(payload[4:6], "little")
        elif kind == b"ANMF" and length >= 16:
            frames += 1
            duration += int.from_bytes(payload[12:15], "little")
        offset += 8 + length + length % 2
    if not valid or offset != len(data) or frames <= 40 or duration != 3200 or loops != 1:
        ERRORS.append(f"Brand animation: expected a complete 3200 ms single-play WebP; got {frames} frames, {duration} ms, {loops} plays")

if ERRORS:
    print("Static site check failed:")
    print("\n".join(f"- {error}" for error in ERRORS))
    sys.exit(1)
print(f"PASS: {len(documents)} pages; {references} references; routes, assets, anchors, metadata, and document structure.")
