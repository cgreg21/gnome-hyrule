#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"
OUTPUT_DIR="$ROOT/docs/screenshots"
RUNTIME_DIR="${XDG_RUNTIME_DIR:-$(mktemp -d)}"
mkdir -p "$RUNTIME_DIR" "$OUTPUT_DIR"
chmod 700 "$RUNTIME_DIR"

XVFB_PID=""
SHELL_PID=""
cleanup() {
  [[ -n "$SHELL_PID" ]] && kill "$SHELL_PID" 2>/dev/null || true
  [[ -n "$XVFB_PID" ]] && kill "$XVFB_PID" 2>/dev/null || true
}
trap cleanup EXIT

export XDG_RUNTIME_DIR="$RUNTIME_DIR"
export DISPLAY=:99
Xvfb "$DISPLAY" -screen 0 1600x1000x24 -nolisten tcp >"$RUNTIME_DIR/xvfb.log" 2>&1 &
XVFB_PID=$!
X_SOCKET="/tmp/.X11-unix/X${DISPLAY#:}"
for _ in $(seq 1 50); do
  [[ -S "$X_SOCKET" ]] && break
  sleep 0.2
done
[[ -S "$X_SOCKET" ]]

export XDG_SESSION_TYPE=wayland
export GDK_BACKEND=x11
export XDG_CURRENT_DESKTOP=GNOME
export GNOME_SHELL_SESSION_MODE=user
export MUTTER_DEBUG_DUMMY_MODE_SPECS=1600x1000
export LIBGL_ALWAYS_SOFTWARE=1
export XDG_DATA_HOME="${XDG_DATA_HOME:-$HOME/.local/share}"
export XDG_CONFIG_HOME="${XDG_CONFIG_HOME:-$HOME/.config}"
bash "$ROOT/scripts/install.sh"

pipewire >"$RUNTIME_DIR/pipewire.log" 2>&1 &
wireplumber >"$RUNTIME_DIR/wireplumber.log" 2>&1 &
sleep 2
mkdir -p "$HOME/.themes"
rm -rf "$HOME/.themes/Hyrule-Pixel"
cp -a "$ROOT/themes/Hyrule-Pixel" "$HOME/.themes/"

USER_THEME_ID="user-theme@gnome-shell-extensions.gcampax.github.com"
gsettings set org.gnome.shell enabled-extensions "['$USER_THEME_ID']"
gsettings set org.gnome.shell.extensions.user-theme name 'Hyrule-Pixel'

# Devkit presents the nested Wayland desktop in a GTK window on the Xvfb display.
gnome-shell --devkit --wayland --unsafe-mode >"$RUNTIME_DIR/gnome-shell.log" 2>&1 &
SHELL_PID=$!
for _ in $(seq 1 40); do
  kill -0 "$SHELL_PID" 2>/dev/null || { cat "$RUNTIME_DIR/gnome-shell.log"; exit 1; }
  sleep 0.5
done
sleep 8

# Resize the Devkit host window and close Fedora's automatic first-run tour.
DEVKIT_WINDOW="$(xdotool search --onlyvisible --name 'Mutter Development Kit' | head -n 1)"
test -n "$DEVKIT_WINDOW"
xdotool windowmove "$DEVKIT_WINDOW" 0 0
xdotool windowsize "$DEVKIT_WINDOW" 1600 1000
sleep 2

# The welcome card is GNOME Tour, not part of the Shell theme. Close only the
# first-run helpers instead of relying on fragile screen coordinates.
ps -eo pid=,comm=,args= | grep -E '[g]nome-tour|[g]nome-initial-setup' || true
for app in gnome-tour gnome-initial-setup; do
  while read -r pid; do
    [[ -n "$pid" ]] && kill "$pid" 2>/dev/null || true
  done < <(ps -eo pid=,comm= | awk -v name="$app" '$2 == name {print $1}')
done
sleep 2
import -window root "$RUNTIME_DIR/devkit-after-tour-close.png"
WELCOME_PIXEL="$(magick "$RUNTIME_DIR/devkit-after-tour-close.png" -format '%[pixel:p{600,300}]' info:)"
[[ "$WELCOME_PIXEL" != "srgb(54,54,58)" ]] || {
  echo "GNOME Tour welcome dialog is still visible; refusing to capture screenshots."
  exit 1
}

gnome-shell --version | grep -q '51\.' || { gnome-shell --version; exit 1; }

capture() {
  local name="$1"
  sleep 2
  import -window root "$OUTPUT_DIR/$name"
  identify -format '%wx%h' "$OUTPUT_DIR/$name" | grep -q '^1600x1000$'
  [[ "$(identify -format '%k' "$OUTPUT_DIR/$name")" -ge 64 ]]
}

eval_shell() {
  gdbus call --session \
    --dest org.gnome.Shell \
    --object-path /org/gnome/Shell \
    --method org.gnome.Shell.Eval "$1"
}

rm -f "$OUTPUT_DIR"/shell-*.png
eval_shell 'Main.overview.show()'
capture shell-overview.png
eval_shell 'Main.overview.hide(); Main.panel.statusArea.dateMenu.menu.open()'
capture shell-calendar.png
eval_shell 'Main.panel.statusArea.dateMenu.menu.close(); Main.panel.statusArea.quickSettings.menu.open()'
capture shell-quick-settings.png
eval_shell 'Main.panel.statusArea.quickSettings.menu.close()'
notify-send --app-name="Hyrule Pixel" "Hyrule notification" "A message from the Hyrule screenshot test."
sleep 3
capture shell-notification.png

for screenshot in "$OUTPUT_DIR"/shell-*.png; do
  test -s "$screenshot"
  identify "$screenshot"
done
[[ "$(sha256sum "$OUTPUT_DIR"/shell-*.png | cut -d ' ' -f 1 | sort -u | wc -l)" -eq 4 ]]
