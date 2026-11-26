#!/usr/bin/env python3
"""Generate crisp Hyrule 9-slice PNG textures with Pillow."""
from pathlib import Path

from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "themes" / "Hyrule-Pixel" / "assets"
PALETTE = {
    "deep": (9, 41, 29, 255),
    "forest": (18, 63, 43, 255),
    "green": (40, 120, 60, 255),
    "gold": (229, 184, 62, 255),
    "bright": (255, 243, 210, 255),
    "shadow": (74, 48, 24, 255),
    "transparent": (0, 0, 0, 0),
}


def frame(name, size, inset, fill, border, highlight, shadow):
    image = Image.new("RGBA", (size, size), PALETTE["transparent"])
    draw = ImageDraw.Draw(image)
    last = size - 1
    # Pixel-art corners and straight edges; the inner area stays stretch-safe.
    draw.rectangle((inset, inset, last - inset, last - inset), fill=PALETTE[fill])
    draw.rectangle((0, 0, last, last), outline=PALETTE[shadow], width=1)
    draw.rectangle((1, 1, last - 1, last - 1), outline=PALETTE[border], width=max(1, inset // 3))
    draw.line((inset, inset, last - inset, inset), fill=PALETTE[highlight], width=1)
    draw.line((inset, inset, inset, last - inset), fill=PALETTE[highlight], width=1)
    # Corner pixels make the frame read as carved 16-bit wood and gold.
    for x, y in ((2, 2), (last - 2, 2), (2, last - 2), (last - 2, last - 2)):
        draw.rectangle((x, y, x + 1, y + 1), fill=PALETTE[highlight])
    image.save(OUT / name, format="PNG", optimize=True)


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    frame("panel-frame.png", 48, 12, "forest", "gold", "bright", "shadow")
    frame("button-frame.png", 24, 6, "green", "gold", "bright", "shadow")
    frame("entry-frame.png", 24, 6, "paper" if "paper" in PALETTE else "bright", "gold", "bright", "shadow")
    # A repeatable 3-pixel divider tile for separators and menu decoration.
    divider = Image.new("RGBA", (24, 3), PALETTE["transparent"])
    draw = ImageDraw.Draw(divider)
    draw.line((0, 1, 23, 1), fill=PALETTE["gold"], width=1)
    draw.point((2, 0), fill=PALETTE["bright"])
    draw.point((21, 2), fill=PALETTE["shadow"])
    divider.save(OUT / "gold-divider.png", format="PNG", optimize=True)
    print(f"Generated {len(list(OUT.glob('*.png')))} Hyrule PNG textures in {OUT}")


if __name__ == "__main__":
    main()
