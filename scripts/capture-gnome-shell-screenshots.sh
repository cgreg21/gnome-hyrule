#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"
OUTPUT_DIR="$ROOT/docs/screenshots"
RUNTIME_DIR="${XDG_RUNTIME_DIR:-$(mktemp -d)}"
mkdir -p "$RUNTIME_DIR" "$OUTPUT_DIR"
chmod 700 "$RUNTIME_DIR"

XVFB_PID=""
WESTON_PID=""
SHELL_PID=""
cleanup() {
  [[ -n "$SHELL_PID" ]] && kill "$SHELL_PID" 2>/dev/null || true
  [[ -n "$WESTON_PID" ]] && kill "$WESTON_PID" 2>/dev/null || true
  [[ -n "$XVFB_PID" ]] && kill "$XVFB_PID" 2>/dev/null || true
}
trap cleanup EXIT

export XDG_RUNTIME_DIR="$RUNTIME_DIR"
export DISPLAY="${DISPLAY:-:99}"
Xvfb "$DISPLAY" -screen 0 1600x1000x24 -nolisten tcp >"$RUNTIME_DIR/xvfb.log" 2>&1 &
XVFB_PID=$!
X_SOCKET="/tmp/.X11-unix/X${DISPLAY#:}"
for _ in $(seq 1 50); do
  [[ -S "$X_SOCKET" ]] && break
  sleep 0.2
done
[[ -S "$X_SOCKET" ]]

weston --backend=x11 --socket=wayland-1 --width=1600 --height=1000 --use-pixman --no-config >"$RUNTIME_DIR/weston.log" 2>&1 &
WESTON_PID=$!
for _ in $(seq 1 100); do
  [[ -S "$RUNTIME_DIR/wayland-1" ]] && break
  sleep 0.2
done
[[ -S "$RUNTIME_DIR/wayland-1" ]] || { cat "$RUNTIME_DIR/weston.log"; exit 1; }

export WAYLAND_DISPLAY=wayland-1
export XDG_SESSION_TYPE=wayland
export GDK_BACKEND=wayland
export LIBGL_ALWAYS_SOFTWARE=1
export XDG_DATA_HOME="${XDG_DATA_HOME:-$HOME/.local/share}"
export XDG_CONFIG_HOME="${XDG_CONFIG_HOME:-$HOME/.config}"
bash "$ROOT/scripts/install.sh"
mkdir -p "$HOME/.themes"
rm -rf "$HOME/.themes/Hyrule-Pixel"
cp -a "$ROOT/themes/Hyrule-Pixel" "$HOME/.themes/"

USER_THEME_ID="user-theme@gnome-shell-extensions.gcampax.github.com"
gsettings set org.gnome.shell enabled-extensions "['$USER_THEME_ID']"
gsettings set org.gnome.shell.extensions.user-theme name 'Hyrule-Pixel'

gnome-shell --devkit --wayland >"$RUNTIME_DIR/gnome-shell.log" 2>&1 &
SHELL_PID=$!
for _ in $(seq 1 100); do
  kill -0 "$SHELL_PID" 2>/dev/null || { cat "$RUNTIME_DIR/gnome-shell.log"; exit 1; }
  if grep -q 'Running GNOME Shell' "$RUNTIME_DIR/gnome-shell.log"; then break; fi
  sleep 0.5
done
sleep 8
gnome-shell --version | grep -q '51\.' || { gnome-shell --version; exit 1; }

capture() {
  local name="$1"
  sleep 2
  import -window root "$OUTPUT_DIR/$name"
  identify -format '%wx%h' "$OUTPUT_DIR/$name" | grep -q '^1600x1000$'
}

rm -f "$OUTPUT_DIR"/shell-*.png
xdotool key Super_L
capture shell-overview.png
xdotool key Escape
sleep 1
xdotool mousemove 800 14 click 1
capture shell-calendar.png
xdotool key Escape
sleep 1
xdotool mousemove 1550 14 click 1
capture shell-quick-settings.png
xdotool key Escape
notify-send --app-name="Hyrule Pixel" "Hyrule notification" "A message from the Hyrule screenshot test."
capture shell-notification.png

for screenshot in "$OUTPUT_DIR"/shell-*.png; do
  test -s "$screenshot"
  identify "$screenshot"
done
