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
import ast
import pathlib
import sys
import xml.etree.ElementTree as ET

root = pathlib.Path(sys.argv[1])
ast.parse((root / "scripts/draw-icons.py").read_text())
ast.parse((root / "scripts/draw-theme-textures.py").read_text())
icons = root / "icons" / "Hyrule-Icons"
svg_files = sorted(icons.rglob("*.svg"))
for svg in svg_files:
    document = ET.parse(svg)
    if document.getroot().get("shape-rendering") != "crispEdges":
        raise SystemExit(f"Pixel-art rendering hint missing: {svg.relative_to(root)}")

theme_index = (icons / "index.theme").read_text()
for section in ("[128x128/apps]", "[128x128/places]", "[128x128/status]", "[128x128/mimetypes]", "[512x512/apps]", "[512x512/places]", "[512x512/status]", "[512x512/mimetypes]", "[scalable/apps]", "[scalable/places]", "[scalable/status]", "[scalable/mimetypes]"):
    if section not in theme_index:
        raise SystemExit(f"Missing icon theme directory declaration: {section}")
for directory in ("apps", "places", "status", "mimetypes"):
    if not (icons / "scalable" / directory).is_dir():
        raise SystemExit(f"Missing icon directory: scalable/{directory}")
    if not (icons / "128x128" / directory).is_dir():
        raise SystemExit(f"Missing PNG icon directory: 128x128/{directory}")
    if not (icons / "512x512" / directory).is_dir():
        raise SystemExit(f"Missing native PNG icon directory: 512x512/{directory}")

png_files = sorted((icons / "128x128").rglob("*.png"))
native_png_files = sorted((icons / "512x512").rglob("*.png"))
for png in png_files:
    data = png.read_bytes()
    if data[:8] != b"\x89PNG\r\n\x1a\n":
        raise SystemExit(f"Invalid PNG signature: {png.relative_to(root)}")
    if data[:4] != bytes([137, 80, 78, 71]) or data[12:16] != b"IHDR":
        raise SystemExit(f"Missing PNG header: {png.relative_to(root)}")
    width = int.from_bytes(data[16:20], "big")
    height = int.from_bytes(data[20:24], "big")
    if (width, height) != (128, 128):
        raise SystemExit(f"Expected 128x128 PNG: {png.relative_to(root)} ({width}x{height})")
if len(png_files) < 33:
    raise SystemExit(f"Expected at least 33 legacy PNG icons, found {len(png_files)}")
for png in native_png_files:
    data = png.read_bytes()
    if data[:8] != b"\x89PNG\r\n\x1a\n":
        raise SystemExit(f"Invalid native PNG signature: {png.relative_to(root)} ({data[:8]!r})")
    if data[:4] != bytes([137, 80, 78, 71]) or data[12:16] != b"IHDR":
        raise SystemExit(f"Invalid native PNG header: {png.relative_to(root)} ({data[12:16]!r})")
    width = int.from_bytes(data[16:20], "big")
    height = int.from_bytes(data[20:24], "big")
    if (width, height) != (512, 512):
        raise SystemExit(f"Expected native 512x512 PNG: {png.relative_to(root)} ({width}x{height})")
if len(native_png_files) != 33:
    raise SystemExit(f"Expected exactly 33 native 512x512 PNG icons, found {len(native_png_files)}")

required_pngs = (
    "places/folder-music.png", "places/folder-videos.png",
    "places/drive-harddisk.png", "mimetypes/application-x-executable.png",
    "mimetypes/package-x-generic.png", "status/network-wired.png",
    "status/user-trash-full.png",
)
missing_pngs = [name for name in required_pngs if not (icons / "128x128" / name).is_file()]
if missing_pngs:
    raise SystemExit("Missing generated PNG icons: " + ", ".join(missing_pngs))
missing_native = [name for name in required_pngs if not (icons / "512x512" / name).is_file()]
if missing_native:
    raise SystemExit("Missing native 512x512 PNG icons: " + ", ".join(missing_native))

texture_sizes = {
    "panel-frame.png": (64, 64),
    "button-frame.png": (48, 48),
    "entry-frame.png": (48, 48),
    "gold-divider.png": (32, 5),
    "inventory-parchment.png": (128, 96),
    "inventory-slot.png": (40, 40),
    "inventory-slot-selected.png": (40, 40),
    "rupee-green.png": (24, 32),
    "inventory-tab.png": (64, 24),
    "inventory-tab-selected.png": (64, 24),
    "inventory-cursor.png": (16, 16),
    "heart-red.png": (16, 16),
}
texture_dir = root / "themes/Hyrule-Pixel/assets"
for name, expected in texture_sizes.items():
    path = texture_dir / name
    if not path.is_file():
        raise SystemExit(f"Missing theme texture: {path.relative_to(root)}")
    data = path.read_bytes()
    if data[:4] != bytes([137, 80, 78, 71]) or data[12:16] != b"IHDR":
        raise SystemExit(f"Invalid theme PNG: {path.relative_to(root)}")
    actual = (int.from_bytes(data[16:20], "big"), int.from_bytes(data[20:24], "big"))
    if actual != expected:
        raise SystemExit(f"Expected {expected[0]}x{expected[1]} theme PNG: {name} ({actual[0]}x{actual[1]})")

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
print(f"Validated {len(svg_files)} SVG, {len(png_files)} legacy PNG and {len(native_png_files)} native 512x512 PNG icon(s), pixel-art rendering, system icons, scripts, and 9-slice PNG textures, scripts, and theme files.")
PY
