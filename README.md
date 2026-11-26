# Hyrule Pixel

A user-installable GNOME desktop theme inspired by 16/32-bit Zelda-era JRPG pixel art.

## Included

- GNOME Shell stylesheet (GNOME 51 target; live-session validation still required)
- GTK 3 light/dark stylesheets
- Best-effort GTK 4 stylesheet
- Small starter set of pixel-style SVG icons
- User-local install and uninstall scripts

## Install

Run from the repository root:

```bash
bash scripts/install.sh
```

Enable **Hyrule-Pixel** in GNOME Tweaks under Appearance → Shell (the GNOME User Themes extension is required). Select **Hyrule-Icons** under Icons.

The scripts only write to `$XDG_DATA_HOME` (or `~/.local/share` when unset). They do not modify system directories.

Uninstall:

```bash
bash scripts/uninstall.sh
```

## Compatibility notes

- Target: GNOME Shell 51. The stylesheet is an initial implementation, not a claim of verified GNOME 51 runtime compatibility.
- GTK 4/libadwaita applications may ignore third-party GTK stylesheets.
- GDM and the lock screen are intentionally not modified by the user-local installer.

See [docs/COMPATIBILITY.md](docs/COMPATIBILITY.md) for known limitations.

## License

Personal-use project. Artwork and styles in this repository are original project assets; Zelda and related trademarks belong to their respective owners.
