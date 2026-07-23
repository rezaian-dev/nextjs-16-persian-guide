#!/usr/bin/env python3
"""Social preview (1254 × 627) for the Pages site, cut from the repository banner.

No new artwork is invented here: the banner is composed as a square so that its top 2 : 1 band
already reads as a standalone card — title, subtitle, the four technology pills and the live code
window. This script crops exactly that band, losslessly and at the banner's own resolution: the
master is 1254 × 1254 px, so the card is 1254 × 627 and nothing is resampled. (A 1280 × 640 JPEG
used to be written here; the upscale it needed was the only thing making it softer.)

    python3 src/tools/make_card.py            # write docs/assets/social-card.png
    python3 src/tools/make_card.py --check    # fail if it is stale

Set the same file in GitHub → Settings → Social preview so link unfurling matches.
"""
from __future__ import annotations
import argparse, io, pathlib, sys

from PIL import Image

ROOT = pathlib.Path(__file__).resolve().parents[2]
BANNER = ROOT / "src" / "banner" / "banner.png"
OUT = ROOT / "docs" / "assets" / "social-card.png"
RATIO = 2.0                                  # the band's width : height


def card() -> bytes:
    if not BANNER.exists():
        sys.exit(f"missing {BANNER.relative_to(ROOT)}")
    im = Image.open(BANNER).convert("RGB")
    band_h = round(im.width / RATIO)
    if im.width < 1000 or band_h > im.height:
        sys.exit(f"banner is {im.width}×{im.height}; a {RATIO:g} : 1 title band does not fit")
    band = im.crop((0, 0, im.width, band_h))
    buf = io.BytesIO()
    band.save(buf, "PNG", optimize=True, compress_level=9)
    blob = buf.getvalue()
    back = Image.open(io.BytesIO(blob))
    back.load()
    if back.size != band.size or back.convert("RGB").tobytes() != band.tobytes():
        sys.exit("the PNG card is not pixel-identical to the banner crop — refusing to write it")
    return blob


def main() -> None:
    ap = argparse.ArgumentParser(description="crop the banner's title band into the social preview")
    ap.add_argument("--check", action="store_true", help="compare against what is committed")
    args = ap.parse_args()
    blob, now = card(), (OUT.read_bytes() if OUT.exists() else None)
    im = Image.open(io.BytesIO(blob))
    label = f"{im.width}×{im.height} {len(blob) / 1024:>5.0f} KiB"
    if now == blob:
        print(f"  {OUT.name:<18} {label}  unchanged")
        return
    print(f"  {OUT.name:<18} {label}  {'STALE' if now else 'new'}")
    if args.check:
        sys.exit(1)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_bytes(blob)
    print(f"  wrote {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
