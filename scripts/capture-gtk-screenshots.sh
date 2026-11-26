#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"
OUTPUT_DIR="${1:-$ROOT/docs/screenshots}"
mkdir -p "$OUTPUT_DIR"

if ! command -v gnome-screenshot >/dev/null 2>&1; then
  echo "gnome-screenshot is required (install the gnome-screenshot package)." >&2
  exit 1
fi

capture_app() {
  local app="$1"
  local output="$2"
  local command_name="$3"

  if ! command -v "$command_name" >/dev/null 2>&1; then
    echo "Missing $command_name. Install the package providing $command_name." >&2
    return 1
  fi

  echo "Launching $app with GTK_THEME=Hyrule-Pixel..."
  GTK_THEME=Hyrule-Pixel "$command_name" >/tmp/hyrule-screenshot-app.log 2>&1 &
  local app_pid=$!
  sleep 5
  gnome-screenshot --window --file="$OUTPUT_DIR/$output"
  kill "$app_pid" 2>/dev/null || true
  wait "$app_pid" 2>/dev/null || true
  echo "Saved $OUTPUT_DIR/$output"
}

capture_app "GTK 3 Widget Factory" "gtk3-widget-factory.png" "gtk3-widget-factory"
capture_app "GTK 4 Demo" "gtk4-demo.png" "gtk4-demo"

echo
echo "GTK screenshots captured. For GNOME Shell screens (overview, calendar,"
echo "Quick Settings and lock screen), capture the real desktop manually and"
echo "save the PNG files in: $OUTPUT_DIR"
