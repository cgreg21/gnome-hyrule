# Hyrule Pixel

A user-installable GNOME desktop theme inspired by 16/32-bit Zelda-era JRPG pixel art.

## Components

- GNOME Shell theme (requires the User Themes extension)
- GTK 3 theme
- GTK 4 stylesheet (best-effort; libadwaita applications may ignore it)
- Hyrule Pixel icon theme
- User-local install and uninstall scripts

## Install

```bash
./scripts/install.sh
```

Then enable **Hyrule-Pixel** in GNOME Tweaks under Appearance → Shell, and select **Hyrule-Icons** under Icons.

The installer only writes to `~/.local/share/themes` and `~/.local/share/icons`.

## Compatibility

Target: GNOME Shell 51. The Shell stylesheet is a starting point and must be validated against a live GNOME 51 session. GTK 4/libadwaita applications may not honor third-party GTK stylesheets.

## License

Personal-use project. Artwork and styles are original project assets; Zelda and related trademarks belong to their respective owners.
