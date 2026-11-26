#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"
bash -n "$ROOT/scripts/install.sh"
bash -n "$ROOT/scripts/uninstall.sh"
if grep -Eq '^\\$|^#[0-9a-fA-F]{6}:' "$ROOT/themes/Hyrule-Pixel/gnome-shell/gnome-shell.css"; then
  echo "Invalid Sass-style token found in GNOME Shell CSS." >&2
  exit 1
fi
python3 - "$ROOT" <<'PY'
import pathlib
import sys
import xml.etree.ElementTree as ET

root = pathlib.Path(sys.argv[1])
icons = root / "icons" / "Hyrule-Icons"
svg_files = sorted(icons.rglob("*.svg"))
for svg in svg_files:
    document = ET.parse(svg)
    if document.getroot().get("shape-rendering") != "crispEdges":
        raise SystemExit(f"Pixel-art rendering hint missing: {svg.relative_to(root)}")

theme_index = (icons / "index.theme").read_text()
for section in ("[128x128/apps]", "[128x128/places]", "[128x128/status]", "[128x128/mimetypes]", "[scalable/apps]", "[scalable/places]", "[scalable/status]", "[scalable/mimetypes]"):
    if section not in theme_index:
        raise SystemExit(f"Missing icon theme directory declaration: {section}")
for directory in ("apps", "places", "status", "mimetypes"):
    if not (icons / "scalable" / directory).is_dir():
        raise SystemExit(f"Missing icon directory: scalable/{directory}")
    if not (icons / "128x128" / directory).is_dir():
        raise SystemExit(f"Missing PNG icon directory: 128x128/{directory}")

png_files = sorted((icons / "128x128").rglob("*.png"))
for png in png_files:
    data = png.read_bytes()
    if data[:8] != b"\\x89PNG\\r\\n\\x1a\\n":
        raise SystemExit(f"Invalid PNG signature: {png.relative_to(root)}")
    if len(data) < 24 or data[12:16] != b"IHDR":
        raise SystemExit(f"Missing PNG header: {png.relative_to(root)}")
    width = int.from_bytes(data[16:20], "big")
    height = int.from_bytes(data[20:24], "big")
    if (width, height) != (128, 128):
        raise SystemExit(f"Expected 128x128 PNG: {png.relative_to(root)} ({width}x{height})")
if len(png_files) < 18:
    raise SystemExit(f"Expected at least 18 PNG icons, found {len(png_files)}")

required = [
    root / "README.md",
    root / "themes/Hyrule-Pixel/gnome-shell/gnome-shell.css",
    root / "themes/Hyrule-Pixel/gtk-3.0/gtk.css",
    root / "themes/Hyrule-Pixel/gtk-4.0/gtk.css",
    root / "icons/Hyrule-Icons/index.theme",
]
missing = [str(path.relative_to(root)) for path in required if not path.is_file()]
if missing:
    raise SystemExit("Missing required files: " + ", ".join(missing))

required_icons = (
    "status/network-wireless.svg",
    "status/network-wired.svg",
    "status/bluetooth-active.svg",
    "status/battery-full.svg",
    "status/user-trash.svg",
    "places/drive-harddisk.svg",
)
missing_icons = [
    f"scalable/{name}" for name in required_icons
    if not (icons / "scalable" / name).is_file()
]
if missing_icons:
    raise SystemExit("Missing system icons: " + ", ".join(missing_icons))
if len(svg_files) < 10:
    raise SystemExit(f"Expected at least 10 SVG icons, found {len(svg_files)}")
print(f"Validated {len(svg_files)} SVG and {len(png_files)} PNG icon(s), pixel-art rendering, system icons, scripts, and theme files.")
PY
