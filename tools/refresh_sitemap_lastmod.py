"""Keep sitemap lastmod values aligned with canonical route files."""

from __future__ import annotations

import subprocess
from datetime import date
from pathlib import Path
from urllib.parse import urlsplit
from xml.etree import ElementTree as ET


ROOT = Path(__file__).resolve().parents[1]
ORIGIN = "https://nasuta.ru"
NS = "http://www.sitemaps.org/schemas/sitemap/0.9"
ET.register_namespace("", NS)


def route_file(url: str) -> Path | None:
    parts = urlsplit(url)
    if f"{parts.scheme}://{parts.netloc}" != ORIGIN:
        return None
    route = parts.path.strip("/")
    return ROOT / route / "index.html" if route else ROOT / "index.html"


def latest_change(path: Path, changed: set[Path]) -> str:
    if path in changed:
        return date.today().isoformat()
    result = subprocess.run(
        ["git", "log", "-1", "--format=%as", "--", str(path.relative_to(ROOT))],
        cwd=ROOT,
        capture_output=True,
        check=True,
        text=True,
    )
    return result.stdout.strip() or date.today().isoformat()


def main() -> None:
    changed = {
        (ROOT / path).resolve()
        for path in subprocess.run(
            ["git", "diff", "--name-only", "HEAD"], cwd=ROOT, capture_output=True, check=True, text=True
        ).stdout.splitlines()
    }
    tree = ET.parse(ROOT / "sitemap.xml")
    root = tree.getroot()
    updated = 0
    for entry in root.findall(f"{{{NS}}}url"):
        loc = entry.findtext(f"{{{NS}}}loc")
        if not loc:
            continue
        page = route_file(loc)
        if not page or not page.exists():
            continue
        desired = latest_change(page.resolve(), changed)
        lastmod = entry.find(f"{{{NS}}}lastmod")
        if lastmod is None:
            lastmod = ET.SubElement(entry, f"{{{NS}}}lastmod")
        if not lastmod.text or lastmod.text < desired:
            lastmod.text = desired
            updated += 1
    tree.write(ROOT / "sitemap.xml", encoding="utf-8", xml_declaration=True)
    print(f"Updated {updated} sitemap lastmod values")


if __name__ == "__main__":
    main()
