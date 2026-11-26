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
for svg in sorted(icons.rglob("*.svg")):
    ET.parse(svg)

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
print(f"Validated {len(list(icons.rglob('*.svg')))} SVG icon(s) and required theme files.")
PY
