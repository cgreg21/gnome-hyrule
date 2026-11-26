# Hyrule icon catalog

The 33 native 512×512 PNG icons are generated individually with Cloudflare
Workers AI and the FLUX.1 Schnell text-to-image model. Each prompt describes
the exact GNOME application, folder, file type or system status symbol while
sharing the Hyrule fantasy pixel-art art direction and palette.

The generator writes transparent RGBA PNGs. It requests a clean chroma-key
background and removes only background pixels connected to the image edges.
Images are reduced to 512×512 when the provider returns a larger canvas; the
generator refuses to enlarge a smaller source image. The 128×128 compatibility
set remains available separately.

## Catalog

- **Applications:** 14 application-specific illustrations.
- **Places:** 7 folders and storage illustrations.
- **Mimetypes:** 6 file-type illustrations.
- **Status:** 6 network, power, Bluetooth and trash illustrations.

## Generation

See [the README](../README.md#ai-generated-icon-artwork) for Cloudflare
Workers AI account setup, GitHub Actions secrets and generation instructions.

The **Generate Hyrule AI icons** workflow uses FLUX.1 Schnell and commits the
resulting 512×512 PNG files. The free Cloudflare Workers AI allocation is
limited to 10,000 Neurons per day; consult the provider's live pricing before
running a full batch.
