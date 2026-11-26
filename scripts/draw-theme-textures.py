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


def make_divider():
    image = Image.new("RGBA", (32, 5), C["clear"])
    d = ImageDraw.Draw(image)
    line(d, [(0, 2), (31, 2)], "gold_shadow")
    line(d, [(0, 1), (31, 1)], "gold")
    line(d, [(0, 0), (31, 0)], "gold_light")
    for x in (2, 10, 18, 26):
        diamond(d, x, 2, 1, "cream")
    image.save(OUT / "gold-divider.png", format="PNG", optimize=True)


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    make_frame("panel-frame.png", 64, 16, "deep")
    make_frame("button-frame.png", 48, 12, "deep")
    make_frame("entry-frame.png", 48, 12, "deep")
    make_divider()
    print("Generated detailed Hyrule pixel-art 9-slice PNG textures.")


if __name__ == "__main__":
    main()
