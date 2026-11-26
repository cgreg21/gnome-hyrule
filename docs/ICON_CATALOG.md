# Hyrule icon catalog

The Hyrule icon theme keeps its pixel-art PNG catalog generated from
`scripts/draw-icons.py`.

## Visual conventions

- Draw on a 32×32 logical canvas, then scale to 128×128 with nearest-neighbour
  sampling so pixel edges stay sharp.
- Use the shared forest, parchment, gold, and gemstone palette.
- Give folders, file types, and system states distinct silhouettes and symbols;
  avoid relying on a color change alone to distinguish related icons.

## Generated catalog

The generator currently produces 33 PNG icons:

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
