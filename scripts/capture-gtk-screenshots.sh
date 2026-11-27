#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"
OUTPUT_DIR="${1:-$ROOT/docs/screenshots}"
mkdir -p "$OUTPUT_DIR"
rm -f "$OUTPUT_DIR"/*.png

for command_name in xdotool import openbox; do
  command -v "$command_name" >/dev/null || {
    echo "Missing required command: $command_name" >&2
    exit 1
  }
done

openbox >/tmp/hyrule-openbox.log 2>&1 &
WM_PID=$!
trap 'kill "$WM_PID" 2>/dev/null || true' EXIT
sleep 2

capture_app() {
  local title="$1"
  local output="$2"
  local command_name="$3"
  local window_id=""

  command -v "$command_name" >/dev/null || {
    echo "Missing $command_name; install its GTK demo package." >&2
    return 1
  }

  echo "Launching $title with Hyrule-Pixel..."
  GTK_THEME=Hyrule-Pixel "$command_name" >/tmp/hyrule-app.log 2>&1 &
  local app_pid=$!

  for _ in $(seq 1 30); do
    window_id="$(xdotool search --onlyvisible --pid "$app_pid" 2>/dev/null | head -n 1 || true)"
    [[ -n "$window_id" ]] && break
    sleep 1
  done

  if [[ -z "$window_id" ]]; then
    cat /tmp/hyrule-app.log >&2 || true
    kill "$app_pid" 2>/dev/null || true
    return 1
  fi

  xdotool windowactivate --sync "$window_id"
  sleep 3
  timeout 20s import -window "$window_id" "$OUTPUT_DIR/$output"

  case "$command_name" in
    gtk3-widget-factory)
      for page in 2 3; do
        xdotool mousemove --window "$window_id" "$((510 + page * 75))" 14 click 1
        sleep 2
        timeout 20s import -window "$window_id" "$OUTPUT_DIR/gtk3-page-$page.png"
      done
      ;;
    gtk4-demo)
      xdotool mousemove --window "$window_id" 50 159 click 1
      sleep 2
      timeout 20s import -window "$window_id" "$OUTPUT_DIR/gtk4-themes.png"
      xdotool mousemove --window "$window_id" 50 125 click 1
      sleep 2
      timeout 20s import -window "$window_id" "$OUTPUT_DIR/gtk4-frames.png"
      ;;
  esac

  kill "$app_pid" 2>/dev/null || true
  wait "$app_pid" 2>/dev/null || true
  echo "Captured $OUTPUT_DIR/$output"
}

capture_app "GTK 3 Widget Factory" "gtk3-widget-factory.png" "gtk3-widget-factory"
capture_app "GTK 4 Demo" "gtk4-demo.png" "gtk4-demo"
capture_app "GTK 4 Widget Factory" "gtk4-widget-factory.png" "gtk4-widget-factory"
