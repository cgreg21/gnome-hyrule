#!/usr/bin/env python3
"""Show the Hyrule inventory PNG sprites in a real GTK 3 or GTK 4 window."""
import sys
from pathlib import Path

import gi

version = sys.argv[1]
gi.require_version("Gtk", version + ".0")
from gi.repository import GdkPixbuf, Gtk

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "themes" / "Hyrule-Pixel" / "assets"


def add(container, child):
    if version == "3":
        container.pack_start(child, False, False, 6)
    else:
        container.append(child)


def make_label(text, css_class=None):
    label = Gtk.Label(label=text)
    label.set_xalign(0)
    if css_class:
        label.add_css_class(css_class) if version == "4" else label.get_style_context().add_class(css_class)
    return label


def make_sprite(filename, description):
    pixbuf = GdkPixbuf.Pixbuf.new_from_file(str(ASSETS / filename))
    pixbuf = pixbuf.scale_simple(pixbuf.get_width() * 2, pixbuf.get_height() * 2, GdkPixbuf.InterpType.NEAREST)
    image = Gtk.Image.new_from_pixbuf(pixbuf)
    image.set_tooltip_text(description)
    return image


def main():
    window = Gtk.Window(title="Hyrule Pixel — Inventory")
    window.set_default_size(720, 420)
    root = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=14)
    root.set_margin_top(22)
    root.set_margin_bottom(22)
    root.set_margin_start(24)
    root.set_margin_end(24)
    window.set_child(root) if version == "4" else window.add(root)

    title = make_label("HYRULE  /  INVENTORY")
    title.set_markup("<span weight='bold' size='large'>HYRULE  /  INVENTORY</span>")
    add(root, title)
    subtitle = make_label("Equipment, vitality and rupees")
    add(root, subtitle)

    hud = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=12)
    hud_frame = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
    hud_frame.add_css_class("hyrule-inventory-hud") if version == "4" else hud_frame.get_style_context().add_class("hyrule-inventory-hud")
    hud_frame.set_child(hud) if version == "4" else hud_frame.add(hud)
    for filename, description in (
        ("heart-red.png", "Full heart"),
        ("heart-red.png", "Full heart"),
        ("heart-half.png", "Half heart"),
        ("heart-empty.png", "Empty heart"),
        ("heart-empty.png", "Empty heart"),
    ):
        add(hud, make_sprite(filename, description))
    add(hud, Gtk.Separator(orientation=Gtk.Orientation.VERTICAL))
    add(hud, make_sprite("rupee-green.png", "Green rupee"))
    add(hud, make_label("245"))
    add(hud, make_sprite("triforce.png", "Triforce"))
    add(root, hud_frame)

    add(root, make_label("EQUIPMENT"))
    slots = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=14)
    for filename, description in (
        ("inventory-cursor.png", "Selected item cursor"),
        ("rupee-blue.png", "Blue rupee"),
        ("rupee-red.png", "Red rupee"),
        ("triforce.png", "Triforce emblem"),
    ):
        slot = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        slot.add_css_class("hyrule-inventory-slot") if version == "4" else slot.get_style_context().add_class("hyrule-inventory-slot")
        slot.set_size_request(76, 76)
        slot.set_halign(Gtk.Align.CENTER)
        slot.set_valign(Gtk.Align.CENTER)
        slot.set_child(make_sprite(filename, description)) if version == "4" else slot.add(make_sprite(filename, description))
        add(slots, slot)
    add(root, slots)

    footer = make_label("PIXEL ART ASSETS  •  NATIVE PNG  •  GTK " + version)
    add(root, footer)
    if version == "3":
        window.connect("destroy", Gtk.main_quit)
        window.show_all()
        Gtk.main()
    else:
        application = Gtk.Application(application_id="org.hyrule.PixelInventory")
        def activate(app):
            window.set_application(app)
            window.present()
        application.connect("activate", activate)
        application.run([])


if __name__ == "__main__":
    main()
