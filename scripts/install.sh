#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"
THEME_DIR="${XDG_DATA_HOME:-$HOME/.local/share}/themes"
ICON_DIR="${XDG_DATA_HOME:-$HOME/.local/share}/icons"

mkdir -p "$THEME_DIR" "$ICON_DIR"
rm -rf "$THEME_DIR/Hyrule-Pixel" "$ICON_DIR/Hyrule-Icons"
cp -a "$ROOT/themes/Hyrule-Pixel" "$THEME_DIR/"
cp -a "$ROOT/icons/Hyrule-Icons" "$ICON_DIR/"

if command -v gtk-update-icon-cache >/dev/null 2>&1; then
  gtk-update-icon-cache -f -t "$ICON_DIR/Hyrule-Icons" >/dev/null 2>&1 || true
fi

printf 'Installed Hyrule-Pixel and Hyrule-Icons in your user profile.\n'
printf 'Enable the Shell theme with the GNOME User Themes extension and GNOME Tweaks.\n'
