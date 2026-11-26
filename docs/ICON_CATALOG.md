# Hyrule icon catalog

The Hyrule icon theme keeps its pixel-art PNG catalog generated from
`scripts/draw-icons.py`. The generator writes native 512×512 RGBA images;
there is no intermediate low-resolution bitmap and no resize operation.
The older 128×128 set remains available for compatibility.

## Visual conventions

- Draw directly into a 512×512 RGBA canvas. The design grid maps drawing
  primitives to native-resolution coordinates; Pillow rasterizes each shape
  directly at 512×512 without enlarging a bitmap.
- Use the shared forest, parchment, gold, and gemstone palette.
- Give folders, file types, and system states distinct silhouettes and symbols;
  avoid relying on a color change alone to distinguish related icons.

## Generated catalog

The generator currently produces 33 native 512×512 PNG icons:

- **Applications:** 14 application-specific icons.
- **Places:** standard, documents, downloads, pictures, music, video folders,
  and a hard-disk icon.
- **Mimetypes:** text, image, audio, video, executable, and package icons.
- **Status:** wireless and wired networking, battery, Bluetooth, empty trash,
  and full trash.

## Regenerate and validate

```bash
python -m pip install Pillow==11.1.0
python scripts/draw-icons.py
bash scripts/check.sh
```

The `Draw Hyrule icons` GitHub Actions workflow regenerates and commits PNGs
when the drawing script changes. The theme validation workflow checks the
generator, SVG assets, PNG dimensions, and required catalog entries.
