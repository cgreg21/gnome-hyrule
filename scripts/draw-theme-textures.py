#!/usr/bin/env python3
"""Draw detailed, stretch-safe Hyrule pixel-art 9-slice PNG frames."""
from pathlib import Path

from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "themes" / "Hyrule-Pixel" / "assets"

C = {
    "clear": (0, 0, 0, 0),
    "outline": (24, 23, 18, 255),
    "deep": (20, 43, 35, 255),
    "wood": (76, 48, 28, 255),
    "wood_light": (126, 83, 43, 255),
    "wood_high": (164, 119, 65, 255),
    "gold_shadow": (117, 72, 24, 255),
    "gold": (213, 157, 55, 255),
    "gold_light": (255, 222, 130, 255),
    "cream": (255, 242, 199, 255),
    "leaf_dark": (31, 91, 55, 255),
    "leaf": (65, 143, 73, 255),
    "leaf_light": (139, 190, 91, 255),
    "gem_dark": (20, 78, 91, 255),
    "gem": (41, 157, 166, 255),
    "gem_light": (145, 231, 220, 255),
}


def rect(draw, box, color):
    draw.rectangle(box, fill=C[color])


def line(draw, points, color):
    draw.line(points, fill=C[color], width=1)


def diamond(draw, cx, cy, radius, color):
    draw.polygon(
        [(cx, cy - radius), (cx + radius, cy), (cx, cy + radius), (cx - radius, cy)],
        fill=C[color],
    )


def draw_corner(draw, x, y, size, sx, sy):
    # The 16x16 corner is the fixed, non-stretched part of each frame.
    rect(draw, (x, y, x + size - 1, y + size - 1), "wood")
    rect(draw, (x + 1, y + 1, x + size - 2, y + size - 2), "wood_light")
    rect(draw, (x + 2, y + 2, x + size - 3, y + size - 3), "deep")
    # Gold stepped inlay, intentionally chunky at native pixel size.
    line(draw, [(x + 3, y + 2), (x + size - 4, y + 2)], "gold_light")
    line(draw, [(x + 2, y + 3), (x + 2, y + size - 4)], "gold_light")
    line(draw, [(x + size - 3, y + 3), (x + size - 3, y + size - 4)], "gold")
    line(draw, [(x + 3, y + size - 3), (x + size - 4, y + size - 3)], "gold")
    # Leaf scroll with a turquoise jewel at the corner's inner end.
    cx, cy = x + (11 if sx < 0 else 4), y + (11 if sy < 0 else 4)
    rect(draw, (cx - 2, cy - 2, cx + 2, cy + 2), "leaf_dark")
    diamond(draw, cx, cy, 3, "leaf")
    line(draw, [(cx - sx, cy + sy), (cx - 4 * sx, cy + 4 * sy)], "leaf_light")
    rect(draw, (cx - 1, cy - 1, cx, cy), "cream")
    gx, gy = x + (5 if sx < 0 else 10), y + (5 if sy < 0 else 10)
    diamond(draw, gx, gy, 2, "gem_dark")
    diamond(draw, gx, gy, 1, "gem")
    draw.point((gx - 1, gy - 1), fill=C["gem_light"])
    # Tiny brass rivets.
    for rx, ry in ((x + 4, y + 4), (x + size - 5, y + 4),
                   (x + 4, y + size - 5), (x + size - 5, y + size - 5)):
        draw.point((rx, ry), fill=C["gold_light"])


def make_frame(name, size, slice_size, center_color):
    image = Image.new("RGBA", (size, size), C["clear"])
    d = ImageDraw.Draw(image)
    last = size - 1
    # Four corner plates.
    draw_corner(d, 0, 0, slice_size, -1, -1)
    draw_corner(d, size - slice_size, 0, slice_size, 1, -1)
    draw_corner(d, 0, size - slice_size, slice_size, -1, 1)
    draw_corner(d, size - slice_size, size - slice_size, slice_size, 1, 1)

    # Straight edge rails: the middle segment is deliberately periodic so it
    # can stretch without distorting any of the corner artwork.
    mid = size // 2
    for offset, y in enumerate((0, 1, 2, 3, 4, 5)):
        col = ("outline", "gold_shadow", "gold", "gold_light", "wood_light", "wood")
        line(d, [(slice_size, y), (size - slice_size - 1, y)], col[offset])
        line(d, [(slice_size, last - y), (size - slice_size - 1, last - y)], col[offset])
    for offset, x in enumerate((0, 1, 2, 3, 4, 5)):
        col = ("outline", "gold_shadow", "gold", "gold_light", "wood_light", "wood")
        line(d, [(x, slice_size), (x, size - slice_size - 1)], col[offset])
        line(d, [(last - x, slice_size), (last - x, size - slice_size - 1)], col[offset])

    # Engraved repeating Hyrule marks on the stretchable edge sections.
    for px in range(slice_size + 5, size - slice_size - 4, 8):
        diamond(d, px, 3, 1, "cream")
        diamond(d, px, last - 3, 1, "gold_light")
    for py in range(slice_size + 5, size - slice_size - 4, 8):
        diamond(d, 3, py, 1, "cream")
        diamond(d, last - 3, py, 1, "gold_light")

    # The central 9-slice region remains transparent; the CSS background
    # supplies the panel fill and keeps text/content crisp.
    image.save(OUT / name, format="PNG", optimize=True)



def make_headerbar_stone():
    """Create a seamless stone-and-brass strip for GTK title bars."""
    image = Image.new("RGBA", (128, 48), C["deep"])
    d = ImageDraw.Draw(image)
    # Dark stone blocks with subtly varied pixel facets.
    for tile_x in (0, 32, 64, 96):
        rect(d, (tile_x + 1, 7, tile_x + 30, 40), "wood")
        rect(d, (tile_x + 2, 8, tile_x + 29, 39), "deep")
        line(d, [(tile_x + 3, 10), (tile_x + 28, 10)], "wood_light")
        line(d, [(tile_x + 3, 37), (tile_x + 28, 37)], "outline")
        # A tiny stepped Hylian diamond is repeated with the tile.
        cx = tile_x + 16
        diamond(d, cx, 23, 7, "gold_shadow")
        diamond(d, cx, 23, 5, "gold")
        diamond(d, cx, 23, 3, "gold_light")
        diamond(d, cx, 23, 1, "gem")
        # Corner rivets and stone chips.
        for px, py in ((tile_x + 4, 12), (tile_x + 27, 12),
                       (tile_x + 4, 35), (tile_x + 27, 35)):
            d.point((px, py), fill=C["gold_light"])
        d.point((tile_x + 8, 17), fill=C["wood_high"])
        d.point((tile_x + 23, 30), fill=C["wood_high"])
    # Continuous brass rails make adjacent tiles seamless.
    for y, color in ((0, "outline"), (1, "gold_shadow"), (2, "gold"),
                     (3, "gold_light"), (44, "outline"), (45, "gold_shadow"),
                     (46, "gold"), (47, "gold_light")):
        line(d, [(0, y), (127, y)], color)
    image.save(OUT / "headerbar-stone.png", format="PNG", optimize=True)


def make_divider():
    image = Image.new("RGBA", (32, 5), C["clear"])
    d = ImageDraw.Draw(image)
    line(d, [(0, 2), (31, 2)], "gold_shadow")
    line(d, [(0, 1), (31, 1)], "gold")
    line(d, [(0, 0), (31, 0)], "gold_light")
    for x in (2, 10, 18, 26):
        diamond(d, x, 2, 1, "cream")
    image.save(OUT / "gold-divider.png", format="PNG", optimize=True)



def make_parchment_panel():
    image = Image.new("RGBA", (128, 96), C["clear"])
    d = ImageDraw.Draw(image)
    # A softly mottled parchment field, kept inside the 16 px 9-slice frame.
    for y in range(16, 80):
        for x in range(16, 112):
            shade = ((x * 7 + y * 11) % 13) - 6
            base = (222 + shade, 190 + shade, 124 + shade // 2, 255)
            d.point((x, y), fill=base)
    rect(d, (16, 16, 111, 79), "wood")
    rect(d, (18, 18, 109, 77), "gold_shadow")
    rect(d, (19, 19, 108, 76), "wood_light")
    for y in range(20, 76):
        for x in range(20, 108):
            shade = ((x * 3 + y * 5) % 9) - 4
            d.point((x, y), fill=(226 + shade, 198 + shade, 143 + shade, 255))
    # Faint map-like contour marks and paper flecks.
    for x, y in ((29, 31), (42, 62), (76, 28), (94, 58), (61, 70), (101, 39)):
        d.point((x, y), fill=(185, 151, 94, 255))
        d.point((x + 1, y), fill=(238, 216, 169, 255))
    for x in range(27, 101, 16):
        diamond(d, x, 20, 1, "gold_shadow")
        diamond(d, x, 75, 1, "gold_shadow")
    # Layered carved frame and jewel-like corner details.
    for x, y in ((0, 0), (112, 0), (0, 80), (112, 80)):
        rect(d, (x, y, x + 15, y + 15), "wood")
        rect(d, (x + 2, y + 2, x + 13, y + 13), "gold")
        rect(d, (x + 4, y + 4, x + 11, y + 11), "deep")
        cx, cy = x + (8 if x == 0 else 7), y + (8 if y == 0 else 7)
        diamond(d, cx, cy, 5, "gold_light")
        diamond(d, cx, cy, 3, "gem_dark")
        diamond(d, cx, cy, 2, "gem")
        d.point((cx - 1, cy - 2), fill=C["gem_light"])
    # Continuous rails bridge the corners.
    for yy, color in ((0, "outline"), (1, "gold_shadow"), (2, "gold"), (3, "gold_light"),
                      (92, "outline"), (93, "gold_shadow"), (94, "gold"), (95, "gold_light")):
        line(d, [(16, yy), (111, yy)], color)
    for xx, color in ((0, "outline"), (1, "gold_shadow"), (2, "gold"), (3, "gold_light"),
                      (124, "outline"), (125, "gold_shadow"), (126, "gold"), (127, "gold_light")):
        line(d, [(xx, 16), (xx, 79)], color)
    image.save(OUT / "inventory-parchment.png", format="PNG", optimize=True)


def make_inventory_slot(selected=False):
    image = Image.new("RGBA", (40, 40), C["clear"])
    d = ImageDraw.Draw(image)
    rect(d, (1, 1, 38, 38), "outline")
    rect(d, (2, 2, 37, 37), "gold_light" if selected else "wood")
    rect(d, (4, 4, 35, 35), "gold_shadow" if selected else "wood_light")
    rect(d, (6, 6, 33, 33), "deep")
    rect(d, (8, 8, 31, 31), "wood" if selected else "deep")
    # Recessed inner bevel and tiny corner rivets.
    line(d, [(8, 8), (31, 8)], "gold" if selected else "wood_high")
    line(d, [(8, 8), (8, 31)], "gold" if selected else "wood_high")
    line(d, [(9, 31), (31, 31)], "outline")
    for x, y in ((4, 4), (35, 4), (4, 35), (35, 35)):
        d.point((x, y), fill=C["cream"] if selected else C["gold"])
    if selected:
        diamond(d, 20, 4, 2, "gold_light")
        diamond(d, 20, 35, 2, "gold_light")
    image.save(OUT / ("inventory-slot-selected.png" if selected else "inventory-slot.png"),
               format="PNG", optimize=True)


def make_rupee():
    image = Image.new("RGBA", (24, 32), C["clear"])
    d = ImageDraw.Draw(image)
    d.polygon([(12, 1), (21, 9), (21, 23), (12, 30), (3, 23), (3, 9)],
              fill=C["gem_dark"])
    d.polygon([(12, 3), (19, 10), (19, 22), (12, 28), (5, 22), (5, 10)],
              fill=C["gem"])
    d.polygon([(12, 4), (17, 10), (12, 15), (7, 10)], fill=C["gem_light"])
    d.polygon([(7, 12), (11, 16), (11, 25), (5, 21), (5, 11)], fill=(30, 112, 132, 255))
    d.polygon([(13, 16), (19, 11), (19, 22), (13, 27)], fill=(24, 111, 124, 255))
    line(d, [(12, 2), (19, 9)], "cream")
    image.save(OUT / "rupee-green.png", format="PNG", optimize=True)



def make_inventory_tab(selected=False):
    image = Image.new("RGBA", (64, 24), C["clear"])
    d = ImageDraw.Draw(image)
    edge = "gold_light" if selected else "gold_shadow"
    rect(d, (2, 5, 61, 23), "outline")
    rect(d, (3, 4, 60, 21), edge)
    rect(d, (5, 6, 58, 20), "wood_light" if selected else "wood")
    rect(d, (7, 8, 56, 18), "deep")
    line(d, [(9, 9), (54, 9)], "gold" if selected else "wood_high")
    # Stepped leaf engraving at both ends leaves the center clear for a label.
    for x, flip in ((12, 1), (51, -1)):
        diamond(d, x, 14, 4, "leaf_dark")
        diamond(d, x, 14, 2, "leaf")
        d.point((x - 1, 12), fill=C["leaf_light"])
        line(d, [(x + flip, 14), (x + 3 * flip, 11)], "gold_light")
    if selected:
        line(d, [(20, 20), (43, 20)], "gold_light")
        diamond(d, 32, 3, 2, "gold_light")
    image.save(OUT / ("inventory-tab-selected.png" if selected else "inventory-tab.png"),
               format="PNG", optimize=True)


def make_item_cursor():
    image = Image.new("RGBA", (16, 16), C["clear"])
    d = ImageDraw.Draw(image)
    # Classic stepped pointer with dark outline and a warm highlight.
    d.polygon([(1, 1), (14, 8), (9, 9), (12, 14), (9, 15), (6, 10), (2, 14)],
              fill=C["outline"])
    d.polygon([(3, 3), (11, 8), (7, 9), (10, 13), (8, 13), (5, 8), (3, 11)],
              fill=C["gold_light"])
    line(d, [(3, 3), (3, 10)], "cream")
    image.save(OUT / "inventory-cursor.png", format="PNG", optimize=True)


def make_heart():
    image = Image.new("RGBA", (16, 16), C["clear"])
    d = ImageDraw.Draw(image)
    d.polygon([(1, 4), (4, 1), (7, 3), (8, 4), (11, 1), (14, 4),
               (14, 8), (8, 15), (1, 8)], fill=C["outline"])
    d.polygon([(2, 4), (4, 2), (7, 4), (8, 5), (11, 2), (13, 4),
               (13, 8), (8, 13), (2, 8)], fill=(185, 48, 52, 255))
    d.polygon([(3, 4), (5, 3), (7, 5), (5, 6)], fill=(255, 164, 151, 255))
    image.save(OUT / "heart-red.png", format="PNG", optimize=True)


def make_colored_rupee(filename, colors):
    image = Image.new("RGBA", (24, 32), C["clear"])
    d = ImageDraw.Draw(image)
    dark, body, light, shade = colors
    d.polygon([(12, 1), (21, 9), (21, 23), (12, 30), (3, 23), (3, 9)], fill=dark)
    d.polygon([(12, 3), (19, 10), (19, 22), (12, 28), (5, 22), (5, 10)], fill=body)
    d.polygon([(12, 4), (17, 10), (12, 15), (7, 10)], fill=light)
    d.polygon([(7, 12), (11, 16), (11, 25), (5, 21), (5, 11)], fill=shade)
    d.polygon([(13, 16), (19, 11), (19, 22), (13, 27)], fill=dark)
    d.line([(12, 2), (19, 9)], fill=C["cream"], width=1)
    image.save(OUT / filename, format="PNG", optimize=True)


def make_triforce():
    image = Image.new("RGBA", (32, 30), C["clear"])
    d = ImageDraw.Draw(image)
    gold = (213, 157, 55, 255)
    light = (255, 222, 130, 255)
    dark = (117, 72, 24, 255)
    # Three separate triangles keep the classic negative-space center.
    triangles = [
        [(16, 1), (2, 27), (30, 27)],
        [(9, 14), (2, 27), (16, 27)],
        [(23, 14), (16, 27), (30, 27)],
    ]
    for points in triangles:
        d.polygon(points, fill=dark)
    d.polygon([(16, 3), (4, 25), (28, 25)], fill=gold)
    d.polygon([(16, 5), (7, 23), (25, 23)], fill=light)
    d.polygon([(9, 16), (4, 25), (14, 25)], fill=gold)
    d.polygon([(23, 16), (18, 25), (28, 25)], fill=gold)
    d.line([(16, 5), (8, 21)], fill=C["cream"], width=1)
    image.save(OUT / "triforce.png", format="PNG", optimize=True)


def make_heart_variant(filename, state):
    image = Image.new("RGBA", (16, 16), C["clear"])
    d = ImageDraw.Draw(image)
    outline = [(1, 4), (4, 1), (7, 3), (8, 4), (11, 1), (14, 4),
               (14, 8), (8, 15), (1, 8)]
    d.polygon(outline, fill=C["outline"])
    if state == "empty":
        d.polygon([(2, 4), (4, 2), (7, 4), (8, 5), (11, 2), (13, 4),
                   (13, 8), (8, 13), (2, 8)], fill=(77, 65, 60, 255))
        d.polygon([(3, 5), (5, 4), (7, 6), (8, 7), (11, 4), (12, 5),
                   (12, 8), (8, 12), (3, 8)], fill=(45, 43, 42, 255))
    elif state == "half":
        d.polygon([(2, 4), (4, 2), (7, 4), (8, 5), (11, 2), (13, 4),
                   (13, 8), (8, 13), (2, 8)], fill=(70, 65, 60, 255))
        d.polygon([(2, 4), (4, 2), (7, 4), (8, 5), (8, 13), (2, 8)],
                  fill=(185, 48, 52, 255))
        d.polygon([(3, 4), (5, 3), (7, 5), (5, 6)], fill=(255, 164, 151, 255))
    image.save(OUT / filename, format="PNG", optimize=True)


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    make_frame("panel-frame.png", 64, 16, "deep")
    make_frame("button-frame.png", 48, 12, "deep")
    make_frame("entry-frame.png", 48, 12, "deep")
    make_divider()
    make_headerbar_stone()
    make_parchment_panel()
    make_inventory_slot()
    make_inventory_slot(selected=True)
    make_rupee()
    make_inventory_tab()
    make_inventory_tab(selected=True)
    make_item_cursor()
    make_heart()
    make_colored_rupee("rupee-red.png", ((91, 24, 31, 255), (190, 48, 57, 255), (255, 166, 151, 255), (125, 31, 45, 255)))
    make_colored_rupee("rupee-blue.png", ((20, 54, 105, 255), (48, 112, 190, 255), (164, 220, 255, 255), (27, 77, 143, 255)))
    make_triforce()
    make_heart_variant("heart-empty.png", "empty")
    make_heart_variant("heart-half.png", "half")
    print("Generated detailed Hyrule pixel-art 9-slice PNG textures.")


if __name__ == "__main__":
    main()
