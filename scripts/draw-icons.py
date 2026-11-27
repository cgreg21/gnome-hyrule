#!/usr/bin/env python3
"""Generate the Hyrule icon set with Cloudflare Workers AI / FLUX.1 Schnell."""
from __future__ import annotations

import base64
import io
import json
import os
import time
import urllib.error
import urllib.request
from pathlib import Path

from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[1] / "icons/Hyrule-Icons/512x512"
MODEL = "@cf/black-forest-labs/flux-1-schnell"
SIZE = 512
PALETTE = (
    "deep forest green, emerald, warm parchment ivory, antique gold, "
    "muted turquoise and brick red, rich dark brown outlines"
)
STYLE = (
    "premium hand-crafted 16-bit pixel art game icon, extremely detailed "
    "pixel clusters, crisp deliberate pixel edges, rich material texture, "
    "strong readable silhouette, intricate highlights and shadows, "
    "centered single object, front three-quarter view, fills about 78 percent "
    "of the square, isolated on a perfectly flat pure chroma-key magenta "
    "background #ff00ff, no cast shadow outside object, no border, no frame, "
    "no letters, no words, no watermark, no UI mockup. "
    f"Use this consistent Hyrule fantasy palette: {PALETTE}."
)

ICONS = {
    "apps": {
        "org.gnome.Nautilus": "an ornate Hyrule treasure chest used as a file manager symbol, carved dark wood panels, gold corner plates, tiny brass rivets, central Hylian-inspired crest, green enamel details",
        "org.gnome.Settings": "a finely machined golden fantasy gear, eight substantial teeth, engraved concentric rings, small emerald Triforce-inspired triangular centerpiece",
        "org.gnome.Software": "a fantasy potion merchant satchel with a faceted luminous blue rupee gemstone, leather stitching, brass clasp, potion-glass reflections",
        "org.gnome.Calculator": "an ancient Hyrule calculating device, rectangular dark green stone and brass body, parchment display, individually sculpted gold keys with tiny engraved arithmetic glyphs (abstract marks only)",
        "org.gnome.Calendar": "an ornate parchment adventurer calendar, red leather header, two brass rings, detailed date grid, one highlighted golden day, curled parchment corners",
        "utilities-terminal": "a compact ancient Sheikah-inspired command console, dark forest-green stone housing, glowing turquoise runic prompt symbol, brass controls and etched circuitry",
        "org.gnome.TextEditor": "an open cream parchment manuscript with a folded gold corner, several finely inked green writing lines, brass feather quill laid diagonally",
        "org.gnome.Loupe": "a detailed antique brass magnifying glass with a turquoise glass lens, bright specular glints, leather-wrapped handle",
        "org.gnome.clocks": "a finely engraved round Hyrule clock face, ivory dial, gold bezel, ornate hands, tiny rune-like hour markers, red second hand",
        "org.gnome.Music": "a small fantasy wooden lyre with golden strings and emerald inlays, carved soundboard, two detailed tuning pegs, musical fantasy atmosphere",
        "org.gnome.Maps": "a folded aged Hyrule world map, detailed coastlines and forest/mountain markings, a red and gold location pin, parchment creases",
        "org.gnome.SystemMonitor": "a Sheikah-inspired monitoring device, dark green stone screen with luminous turquoise waveform and gold graph ticks, engraved brass frame",
        "org.gnome.Screenshot": "an ornate fantasy camera lens inside a compact silver and slate camera body, blue glass reflections, brass shutter and red recording indicator",
        "org.gnome.DiskUtility": "a detailed ancient magical storage disk, layered golden metal platter, engraved concentric rings, dark green central hub and tiny runic markings",
    },
    "places": {
        "folder": "a sturdy golden Hyrule adventurer folder, recognizable tabbed folder silhouette, layered parchment interior, leather grain and brass rivets",
        "folder-documents": "a golden tabbed folder containing several neatly stacked parchment documents, visible rolled page edges, ink lines and wax seal",
        "folder-download": "a golden tabbed folder with a bold emerald downward arrow crystal emerging from it, engraved details and brass corners",
        "folder-pictures": "a golden tabbed folder containing a framed miniature landscape painting of Hyrule hills, sun and trees, vivid tiny pixels",
        "folder-music": "a golden tabbed folder with a small carved wooden lyre and gold musical notes emerging from the opening",
        "folder-videos": "a golden tabbed folder with a red inset play medallion, ivory triangular play glyph and detailed brass trim",
        "drive-harddisk": "a compact rugged Hyrule magical data-storage device, slate metal case, gold engraved bands, green status gem, visible mechanical seams",
    },
    "mimetypes": {
        "text-x-generic": "a single upright parchment document with folded corner, dense fine ink text lines, gold seal and green binding edge",
        "image-x-generic": "a richly detailed miniature landscape painting in a parchment picture frame, Hyrule mountains, forest, blue lake and golden sun",
        "audio-x-generic": "an ornate golden musical note carved from brass with turquoise enamel inlay, clear recognizable silhouette",
        "video-x-generic": "a carved red and gold play emblem set into a dark green stone tile, strong ivory triangular play symbol",
        "application-x-executable": "a small ancient green stone rune cartridge with a bright ivory activation triangle, gold circuitry and tiny glowing details",
        "package-x-generic": "a detailed sealed Hyrule supply crate, golden wood panels, crossed parchment label, brass corner protectors and emerald seal",
    },
    "status": {
        "network-wireless": "a magical wireless signal icon formed by three elegant golden radio arcs above a glowing emerald orb, isolated symbol",
        "network-wired": "a detailed brass and turquoise ethernet connector plug with visible contacts, short green cable, recognizable front view",
        "battery-full": "a sturdy golden energy cell battery, full bright emerald charge visible through a glass window, brass terminals and engraved bands",
        "bluetooth-active": "a brilliant turquoise magical Bluetooth rune crystal, angular interwoven symbol, gold edge facets, crisp isolated silhouette",
        "user-trash": "a small medieval iron waste bin with hinged lid, dark slate metal, gold rim, vertical embossed panels, empty and clean",
        "user-trash-full": "a medieval iron waste bin with open lid, parchment scraps and tiny colorful discarded objects visible inside, gold rim",
    },
}


def request_image(prompt: str, token: str, account_id: str) -> bytes:
    url = f"https://api.cloudflare.com/client/v4/accounts/{account_id}/ai/run/{MODEL}"
    payload = json.dumps({"prompt": prompt, "steps": 4}).encode()
    request = urllib.request.Request(
        url, data=payload,
        headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"},
        method="POST",
    )
    for attempt in range(5):
        try:
            with urllib.request.urlopen(request, timeout=180) as response:
                data = response.read()
            try:
                result = json.loads(data)
            except json.JSONDecodeError:
                return data
            if result.get("success") is False:
                raise RuntimeError(json.dumps(result.get("errors", result), ensure_ascii=False))
            encoded = result.get("result", {}).get("image")
            if not encoded:
                raise RuntimeError(f"Cloudflare response has no result.image: {str(result)[:500]}")
            return base64.b64decode(encoded)
        except urllib.error.HTTPError as error:
            detail = error.read().decode("utf-8", "replace")
            if error.code not in (429, 500, 502, 503, 504) or attempt == 4:
                raise RuntimeError(f"Cloudflare AI HTTP {error.code}: {detail}") from error
            time.sleep(2 ** attempt * 3)
        except (urllib.error.URLError, TimeoutError):
            if attempt == 4:
                raise
            time.sleep(2 ** attempt * 3)
    raise RuntimeError("Image generation failed after retries")


def make_transparent(image: Image.Image) -> Image.Image:
    image = image.convert("RGBA")
    if image.width < SIZE or image.height < SIZE:
        raise ValueError(f"Model returned undersized image {image.size}; refusing to upscale")
    if image.size != (SIZE, SIZE):
        image = image.resize((SIZE, SIZE), Image.Resampling.LANCZOS)
    # Remove only the connected chroma-key background, preserving enclosed details.
    draw = ImageDraw.Draw(image)
    for point in ((0, 0), (SIZE - 1, 0), (0, SIZE - 1), (SIZE - 1, SIZE - 1)):
        ImageDraw.floodfill(image, point, (0, 0, 0, 0), thresh=72)
    return image


def main() -> None:
    token = os.environ.get("CLOUDFLARE_API_TOKEN")
    account_id = os.environ.get("CLOUDFLARE_ACCOUNT_ID")
    if not token or not account_id:
        raise SystemExit(
            "Missing CLOUDFLARE_API_TOKEN or CLOUDFLARE_ACCOUNT_ID. "
            "Configure both as GitHub Actions secrets before generating icons."
        )

    ROOT.mkdir(parents=True, exist_ok=True)
    total = sum(len(items) for items in ICONS.values())
    done = 0
    for category, items in ICONS.items():
        target = ROOT / category
        target.mkdir(parents=True, exist_ok=True)
        for name, subject in items.items():
            prompt = f"{subject}. {STYLE}"
            print(f"[{done + 1}/{total}] Generating {category}/{name}.png", flush=True)
            raw = request_image(prompt, token, account_id)
            with Image.open(io.BytesIO(raw)) as source:
                image = make_transparent(source)
                output = target / f"{name}.png"
                image.save(output, format="PNG", optimize=True)
            done += 1
            time.sleep(1)
    print(f"Generated {done} AI-created 512x512 PNG icons with FLUX.1 Schnell.")


if __name__ == "__main__":
    main()
