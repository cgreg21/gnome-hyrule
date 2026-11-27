#!/usr/bin/env python3
"""Validate every image URL and 9-slice declaration in the Hyrule CSS."""

from pathlib import Path
import re

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
THEME = ROOT / "themes" / "Hyrule-Pixel"
STYLESHEETS = {
    "GNOME Shell": THEME / "gnome-shell" / "gnome-shell.css",
    "GTK 3": THEME / "gtk-3.0" / "gtk.css",
    "GTK 4": THEME / "gtk-4.0" / "gtk.css",
}
URL_PATTERN = re.compile(r"""url\(\s*(["']?)(.*?)\1\s*\)""", re.IGNORECASE)
BLOCK_PATTERN = re.compile(r"([^{}]+)\{([^{}]*)\}")
BORDER_IMAGE_PATTERN = re.compile(
    r"""border-image\s*:\s*url\(\s*(["']?)(.*?)\1\s*\)\s*([^;]+);""",
    re.IGNORECASE,
)
EXPECTED_ASSETS = {
    "GNOME Shell": {"panel-frame.png", "button-frame.png", "entry-frame.png",
                    "inventory-parchment.png", "inventory-slot.png",
                    "inventory-slot-selected.png", "headerbar-stone.png", "triforce.png"},
    "GTK 3": {"button-frame.png", "entry-frame.png", "panel-frame.png",
              "inventory-parchment.png", "inventory-tab.png",
              "inventory-tab-selected.png", "inventory-slot.png",
              "inventory-slot-selected.png", "gold-divider.png", "headerbar-stone.png"},
    "GTK 4": {"button-frame.png", "entry-frame.png", "panel-frame.png",
              "inventory-parchment.png", "inventory-tab.png",
              "inventory-tab-selected.png", "inventory-slot.png",
              "inventory-slot-selected.png", "gold-divider.png", "headerbar-stone.png"},
}


def fail(message):
    raise SystemExit(f"CSS image validation failed: {message}")


def image_dimensions(path):
    try:
        with Image.open(path) as image:
            image.verify()
        with Image.open(path) as image:
            if image.format != "PNG":
                fail(f"{path.relative_to(ROOT)} is not PNG")
            if image.mode != "RGBA":
                fail(f"{path.relative_to(ROOT)} must use RGBA, got {image.mode}")
            return image.size
    except (OSError, ValueError) as error:
        fail(f"cannot decode {path.relative_to(ROOT)}: {error}")


def validate_border_image(css_name, css, dimensions):
    for match in BORDER_IMAGE_PATTERN.finditer(css):
        reference, slice_value = match.group(2), match.group(3)
        if reference not in dimensions:
            fail(f"{css_name}: border-image references unvalidated image {reference}")
        slices = slice_value.split("/", 1)[0]
        numbers = re.findall(r"(?<![\w.])\d+(?:\.\d+)?", slices)
        if len(numbers) not in (1, 4):
            fail(f"{css_name}: unsupported 9-slice values for {reference}: {slice_value.strip()}")
        values = [float(value) for value in numbers]
        if len(values) == 1:
            top = right = bottom = left = values[0]
        else:
            top, right, bottom, left = values
        width, height = dimensions[reference]
        if left + right >= width or top + bottom >= height:
            fail(f"{css_name}: 9-slice corners consume {reference} ({width}x{height})")
        if min(values) <= 0:
            fail(f"{css_name}: non-positive 9-slice inset for {reference}")


def main():
    total_references = 0
    total_border_images = 0
    for css_name, stylesheet in STYLESHEETS.items():
        if not stylesheet.is_file():
            fail(f"missing stylesheet {stylesheet.relative_to(ROOT)}")
        css = re.sub(r"/\*.*?\*/", "", stylesheet.read_text(), flags=re.DOTALL)
        dimensions = {}
        references = URL_PATTERN.findall(css)
        if not references:
            fail(f"{css_name}: no CSS image URLs found")
        for _, reference in references:
            if not reference or reference.startswith(("/", "data:", "http:", "https:")):
                fail(f"{css_name}: image URL must be a local relative path: {reference}")
            path = (stylesheet.parent / reference).resolve()
            if not path.is_relative_to(THEME.resolve()):
                fail(f"{css_name}: image path escapes the theme directory: {reference}")
            if not path.is_file():
                fail(f"{css_name}: missing image {reference}")
            if path.suffix.lower() != ".png":
                fail(f"{css_name}: only PNG assets are allowed in CSS: {reference}")
            dimensions[reference] = image_dimensions(path)
            total_references += 1

        for selector, declarations in BLOCK_PATTERN.findall(css):
            if "background-image" in declarations and "url(" in declarations:
                if "background-repeat" not in declarations:
                    fail(f"{css_name}: background image has no explicit repeat mode in {selector.strip()}")
        validate_border_image(css_name, css, dimensions)
        border_count = len(BORDER_IMAGE_PATTERN.findall(css))
        total_border_images += border_count

        used_names = {Path(reference).name for _, reference in references}
        missing = EXPECTED_ASSETS[css_name] - used_names
        if missing:
            fail(f"{css_name}: required PNG assets are not used: {', '.join(sorted(missing))}")

        if css_name == "GTK 3" and "iconview.view cell" not in css:
            fail("GTK 3: icon view cells must use the inventory PNG frame")
        if css_name == "GTK 4" and ".nautilus-desktop gridview > child" not in css:
            fail("GTK 4: Nautilus desktop grid cells must use the inventory PNG frame")
        if css_name == "GNOME Shell" and "#dash .dash-item-container > .app-well-app .overview-icon" not in css:
            fail("GNOME Shell: app grid must use the inventory PNG frame")

        print(f"{css_name}: {len(references)} image references, "
              f"{len(dimensions)} distinct RGBA PNGs, {border_count} 9-slice borders")

    print(f"Validated {total_references} CSS image references and "
          f"{total_border_images} 9-slice declarations across all stylesheets.")


if __name__ == "__main__":
    main()
