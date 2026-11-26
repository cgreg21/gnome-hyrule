# Compatibility and scope

## GNOME Shell 51

The theme targets GNOME Shell 51. GNOME Shell CSS selectors and widget internals can change between releases. This initial stylesheet uses common panel, popup-menu, overview, search-entry, quick-toggle, and notification selectors, but it has not yet been rendered in a GNOME 51 session.

Before calling the theme stable, test it in a disposable GNOME 51 user session and inspect the Shell stylesheet parser output. Do not copy theme files into system directories to test them.

## GTK

GTK 3 stylesheets are provided. GTK 4 support is best-effort: libadwaita applications may intentionally ignore user GTK stylesheets and use their own design tokens.

## Out of scope

The installer does not change GDM, system-wide defaults, the lock screen, or system files. Those require separate, version-sensitive configuration and should not be mixed into a safe per-user theme installer.

## Current asset coverage

The icon theme currently contains a few starter SVGs and inherits missing icons from Adwaita and hicolor. It is not yet a complete icon pack.
