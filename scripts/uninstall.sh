#!/usr/bin/env bash
set -euo pipefail
DATA_DIR="${XDG_DATA_HOME:-$HOME/.local/share}"
rm -rf "$DATA_DIR/themes/Hyrule-Pixel" "$DATA_DIR/icons/Hyrule-Icons"
printf 'Removed Hyrule-Pixel and Hyrule-Icons from your user profile.\n'
