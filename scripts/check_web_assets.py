"""Validate real browser/share assets and generated metadata using only stdlib."""
import json
import os
from pathlib import Path
import struct
from urllib.parse import urlsplit
import xml.etree.ElementTree as ET
import zipfile


def image_size(path):
    data = path.read_bytes()
    if data[:8] == b"\x89PNG\r\n\x1a\n":
        return struct.unpack(">II", data[16:24])
    if data[:2] == b"\xff\xd8":
        pos = 2
        while pos + 4 < len(data):
            if data[pos] != 0xFF:
                break
            marker = data[pos + 1]
            if marker in {0xC0, 0xC1, 0xC2}:
                height, width = struct.unpack(">HH", data[pos + 5:pos + 9])
                return width, height
            length = int.from_bytes(data[pos + 2:pos + 4], "big")
            pos += length + 2
    raise ValueError(f"Unsupported or malformed image: {path.name}")


def check_web_assets(public, config, base_url, documents):
    errors = []
    root = Path(__file__).resolve().parents[1]
    home = base_url.rstrip("/") + "/"
    origin = urlsplit(home).netloc
    private = config["extra"]["preview"] or os.environ.get("CF_PAGES_BRANCH", "main") != "main"
    catalog = json.loads((root / "data/social.json").read_text())
    cards = {card["path"]: card for card in catalog}

    def need(condition, message):
        if not condition:
            errors.append(message)

    def dimensions(relative, size):
        try:
            need(image_size(public / relative) == size, f"{relative}: expected {size}")
        except (OSError, ValueError, struct.error) as error:
            errors.append(str(error))

    seen = set()
    for path, doc in documents.items():
        relative = path.relative_to(public).as_posix()
        if doc.redirect:
            continue
        route = "/" if relative == "index.html" else "/" + relative.removesuffix("index.html")
        is_error = relative == "404.html"
        if not is_error:
            seen.add(route)
            need(route in cards, f"{relative}: no sharing card assigned")
            need(doc.canonical == home + route.lstrip("/"), f"{relative}: incorrect canonical path")
            need(doc.metas["og:url"] == [doc.canonical], f"{relative}: Open Graph URL differs from canonical")
        card = cards.get(route, cards["/"])
        image = home + "brand/social/" + card["slug"] + ".jpg"
        expected = {
            "og:site_name": "Astro90", "og:type": "website", "og:locale": "en_US",
            "og:title": doc.title.strip(), "og:description": doc.description,
            "og:image": image, "og:image:type": "image/jpeg",
            "og:image:width": "1200", "og:image:height": "630", "og:image:alt": card["alt"],
            "twitter:card": "summary_large_image", "twitter:title": doc.title.strip(),
            "twitter:description": doc.description, "twitter:image": image, "twitter:image:alt": card["alt"],
            "application-name": "Astro90", "apple-mobile-web-app-title": "Astro90",
            "robots": "noindex, nofollow, noarchive" if private or is_error or route == "/brand/states/" else "index, follow, max-image-preview:large",
        }
        for key, value in expected.items():
            need(doc.metas[key] == [value], f"{relative}: missing, duplicate or incorrect {key}")
        manifest_links = [link for link in doc.links if link.get("rel") == "manifest"]
        need(len(manifest_links) == 1 and manifest_links[0].get("href") == home + "site.webmanifest" and manifest_links[0].get("crossorigin") == "use-credentials", f"{relative}: manifest must use the build origin and credentials")
        for rel in ["icon", "apple-touch-icon", "mask-icon"]:
            need(any(link.get("rel") == rel for link in doc.links), f"{relative}: missing {rel}")
        if is_error:
            need(not doc.jsonld and not doc.canonical, "404 must not identify itself as an indexable website page")
            continue
        need(len(doc.jsonld) == 1, f"{relative}: expected one JSON-LD graph")
        graph = doc.jsonld[0].get("@graph", []) if doc.jsonld else []
        need(all(isinstance(node, dict) for node in graph), f"{relative}: invalid graph nodes")
        nodes = {node.get("@type"): node for node in graph if isinstance(node, dict)}
        need(nodes.get("Organization", {}).get("name") == "Astro90" and nodes.get("WebSite", {}).get("url") == home, f"{relative}: incorrect website/organization schema")
        page_nodes = [node for node in graph if node.get("@type") in {"WebPage", "CollectionPage", "AboutPage", "ContactPage"}]
        need(len(page_nodes) == 1 and page_nodes[0].get("url") == doc.canonical, f"{relative}: incorrect page schema")
        for node in graph:
            need(urlsplit(node.get("@id", "")).netloc == origin, f"{relative}: schema ID uses the wrong origin")
        if route != "/":
            trail = nodes.get("BreadcrumbList", {}).get("itemListElement", [])
            need(len(trail) >= 2 and trail[0].get("item") == home and trail[-1].get("item") == doc.canonical and [item.get("position") for item in trail] == list(range(1, len(trail)+1)), f"{relative}: incorrect breadcrumb hierarchy")
    need(seen == set(cards), "Sharing-card route catalog differs from rendered website routes")
    need(len(cards) == len(catalog), "Duplicate sharing-card route")
    expected_social_files = {card["slug"] + ".jpg" for card in catalog} | {"post-square.jpg", "post-portrait.jpg", "profile-banner.jpg", "repository-cover.jpg"}
    need({path.name for path in (public / "brand/social").glob("*.jpg")} == expected_social_files, "Social artwork directory contains missing or retired exports")
    for card in catalog:
        dimensions("brand/social/" + card["slug"] + ".jpg", (1200, 630))
    for filename, size in [("post-square", (1080,1080)),("post-portrait", (1080,1350)),("profile-banner", (1500,500)),("repository-cover", (1280,640))]:
        dimensions(f"brand/social/{filename}.jpg", size)
    dimensions("apple-touch-icon.png", (180,180))
    for size in [16,32,48,96]:
        dimensions(f"brand/favicon-{size}.png", (size,size))
    for name in ["saffron", "white", "midnight"]:
        dimensions(f"brand/wordmark-{name}.png", (1320,244))

    try:
        manifest = json.loads((public / "site.webmanifest").read_text())
        for key, value in {"id":"/","start_url":"/","scope":"/","name":"Astro90","short_name":"Astro90","display":"standalone","theme_color":"#090E17","background_color":"#090E17"}.items():
            need(manifest.get(key) == value, f"Manifest: incorrect {key}")
        combinations = set()
        for icon in manifest.get("icons", []):
            size = tuple(map(int, icon["sizes"].split("x")))
            combinations.add((icon.get("purpose"), size))
            need(icon.get("type") == "image/png" and icon["src"].startswith("/brand/"), "Manifest: icon format or origin is incorrect")
            dimensions(icon["src"].lstrip("/"), size)
        need(combinations == {(purpose, (size,size)) for purpose in ["any","maskable"] for size in [192,512]}, "Manifest: missing standard/maskable icons")
        for shortcut in manifest.get("shortcuts", []):
            need(shortcut["url"] in cards, "Manifest: shortcut points to an unknown route")
        ico = (public / "favicon.ico").read_bytes()
        need(ico[:6] == b"\x00\x00\x01\x00\x03\x00" and [(ico[6+i*16], ico[7+i*16]) for i in range(3)] == [(16,16),(32,32),(48,48)], "Favicon ICO is missing its three resolutions")
        robots = (public / "robots.txt").read_text()
        need(("Disallow: /" in robots) if private else ("Disallow: /" not in robots and "Sitemap: " + home + "sitemap.xml" in robots), "robots.txt does not match the release state")
        sitemap = ET.parse(public / "sitemap.xml")
        locations = [node.text for node in sitemap.findall(".//{http://www.sitemaps.org/schemas/sitemap/0.9}loc")]
        need(len(locations) == len(set(locations)) and set(locations) == {home + route.lstrip("/") for route in cards if route != "/brand/states/"}, "Sitemap must contain only canonical content routes")
        exports = json.loads((root / "assets/brand/exports.json").read_text())
        with zipfile.ZipFile(public / "brand/astro90-asset-kit.zip") as kit:
            need(kit.testzip() is None, "Asset kit is corrupt")
            need(set(kit.namelist()) == set(exports) | {"site.webmanifest", "README.md"}, "Asset kit has missing or unexpected files")
            for filename in exports + ["site.webmanifest"]:
                need(kit.read(filename) == (public / filename).read_bytes(), f"Asset kit has a stale {filename}")
            need(kit.read("README.md") == (root / "docs/WEB-ASSETS.md").read_bytes(), "Asset kit documentation is stale")
    except (OSError, ValueError, KeyError, ET.ParseError, zipfile.BadZipFile) as error:
        errors.append(f"Web asset validation: {error}")
    return errors
