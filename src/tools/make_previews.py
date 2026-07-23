#!/usr/bin/env python3
"""Page previews and the author portrait for the Pages site / README, cut from the edition.

Nothing here is designed — it is photography of the actual PDF, so a reader sees the real page
they are about to download. Quality is the whole point of this file, so it follows the ceiling
the edition itself sets:

    python3 src/tools/make_previews.py            # write docs/assets/*.png
    python3 src/tools/make_previews.py --check    # fail if the shipped images are stale

*  The cover art lives in the PDF as a 2118 × 1970 px raster placed on 508 × 473 pt, i.e.
   300 dpi of genuine detail. Rendering above that only interpolates, below it throws detail
   away, so every preview is rasterised at exactly 300 dpi (2480 × 3509 px for this A4 page).
*  Everything ships as PNG: the pages are type and flat colour, where a lossless file is both
   sharper and smaller than a high-quality JPEG. The encoder is checked — the PNG must decode
   back to the exact pixels the renderer produced, byte for byte.
*  The portrait is not rendered at all: it is the 560 × 560 px image the cover embeds, extracted
   from the file, so it is the original pixels with no resampling in between.
"""
from __future__ import annotations
import argparse, io, json, pathlib, sys

from PIL import Image

import pymupdf

ROOT = pathlib.Path(__file__).resolve().parents[2]
DATA = json.loads((ROOT / "src" / "edition" / "chapters.json").read_text(encoding="utf-8"))
PDF, OUT = ROOT / DATA["book"]["pdf"], ROOT / "docs" / "assets"

DPI = 300                      # the real detail density of the edition's own rasters
ZOOM = DPI / 72.0              # PDF user space is 72 pt per inch

# file name → (physical page, what the caption says). One image per kind of page.
SHOTS = {
    "page-cover":     (1,   "جلد کتاب"),
    "page-toc":       (2,   "فهرست مطالب"),
    "page-chapter":   (5,   "سرآغاز فصل ۱"),
    "page-code":      (7,   "پنجرهٔ ترمینال و جعبهٔ هدف"),
    "page-workshop":  (155, "کارگاه مینی‌پروژه‌ها"),
    "page-interview": (174, "پرسش‌های مصاحبه با پاسخ"),
}
# the circular portrait on the cover, measured from the cyan ring (77.8 pt square)
AUTHOR_BOX = pymupdf.Rect(368.6, 662.9, 446.4, 740.6)


def png_lossless(img: Image.Image) -> bytes:
    """Encode as PNG and prove nothing was lost on the way out."""
    buf = io.BytesIO()
    img.save(buf, "PNG", optimize=True, compress_level=9)
    blob = buf.getvalue()
    back = Image.open(io.BytesIO(blob))
    back.load()
    if back.size != img.size or back.convert("RGB").tobytes() != img.convert("RGB").tobytes():
        sys.exit("PNG round-trip is not pixel-identical — refusing to write a lossy file")
    return blob


def render(doc, page_no: int) -> tuple[bytes, tuple[int, int]]:
    page = doc[page_no - 1]
    pix = page.get_pixmap(matrix=pymupdf.Matrix(ZOOM, ZOOM), alpha=False)
    want_w, want_h = round(page.rect.width * ZOOM), round(page.rect.height * ZOOM)
    if abs(pix.width - want_w) > 1 or abs(pix.height - want_h) > 1:
        sys.exit(f"page {page_no}: got {pix.width}×{pix.height}, expected {want_w}×{want_h}")
    img = Image.frombytes("RGB", (pix.width, pix.height), pix.samples)
    return png_lossless(img), img.size


def author_portrait(doc) -> tuple[bytes, tuple[int, int], str]:
    """Pull the cover's own embedded portrait out of the file, untouched."""
    for im in doc[0].get_images(full=True):
        xref = im[0]
        info = doc.extract_image(xref)
        rects = doc[0].get_image_rects(xref)
        if not rects or info["width"] < 300:
            continue
        r = rects[0]
        if abs(r.x0 - AUTHOR_BOX.x0) < 8 and abs(r.y0 - AUTHOR_BOX.y0) < 8 and abs(r.width - 72) < 8:
            size = (info["width"], info["height"])
            if info["ext"] == "png":                      # already lossless: ship it as it is
                probe = Image.open(io.BytesIO(info["image"]))
                probe.load()
                if probe.size == size and probe.mode == "RGB":
                    return info["image"], size, f"embedded xref {xref}, {info['ext']}"
            img = Image.open(io.BytesIO(info["image"])).convert("RGB")
            return png_lossless(img), img.size, f"embedded xref {xref}, re-encoded lossless"
    # no raster to steal → photograph the ring at the cover's own density instead
    pix = doc[0].get_pixmap(clip=AUTHOR_BOX, matrix=pymupdf.Matrix(ZOOM, ZOOM), alpha=False)
    img = Image.frombytes("RGB", (pix.width, pix.height), pix.samples)
    return png_lossless(img), img.size, "rendered from the cover"


def main() -> None:
    ap = argparse.ArgumentParser(description="cut the site's imagery out of the edition at full quality")
    ap.add_argument("--check", action="store_true", help="compare against what is committed")
    args = ap.parse_args()
    if not PDF.exists():
        sys.exit(f"missing {PDF.relative_to(ROOT)} — run src/tools/build_edition.py first")
    OUT.mkdir(parents=True, exist_ok=True)
    doc = pymupdf.open(PDF)
    if doc.page_count != DATA["book"]["pages"]:
        sys.exit("page count changed since chapters.json was written")

    want: dict[str, bytes] = {}
    dims: dict[str, tuple[int, int]] = {}
    for name, (pg, _cap) in SHOTS.items():
        want[name], dims[name] = render(doc, pg)
    want["author"], dims["author"], how = author_portrait(doc)
    print(f"  author source: {how}")
    for name in SHOTS:
        if dims[name] != next(iter(dims.values())):
            sys.exit(f"{name}: {dims[name]} differs from {next(iter(dims))} — a page is not A4")
    print(f"  pages rendered at {DPI} dpi → {next(iter(dims.values()))[0]}×{next(iter(dims.values()))[1]} px")

    stale = []
    for name, blob in want.items():
        f = OUT / f"{name}.png"
        now = f.read_bytes() if f.exists() else None
        same = now == blob
        print(f"  {f.name:<20} {dims[name][0]}×{dims[name][1]:<6} {len(blob) / 1024:>7.0f} KiB  "
              + ("unchanged" if same else ("STALE" if now else "new")))
        if not same:
            stale.append(f)
    if args.check:
        sys.exit(0 if not stale else f"{len(stale)} image(s) no longer match the edition: "
                                     f"{[str(x.relative_to(ROOT)) for x in stale]}")
    for name, blob in want.items():
        if OUT / f"{name}.png" in stale:
            (OUT / f"{name}.png").write_bytes(blob)
    print(f"  wrote {len(stale)} file(s) into {OUT.relative_to(ROOT)}/")


if __name__ == "__main__":
    main()
