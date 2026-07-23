#!/usr/bin/env python3
"""Gallery cards for the Pages site and the README — a whole A4 page at the size it is shown.

The card is a *page*, not a crop: the reader is deciding whether this book has the layout they
expect, and one paragraph of body text painted at 500 px tells them nothing a caption could not.
So each card holds the entire page, and the grid is six small ones in a row — the shape a book
thumbnail has in every store that shows books.

Two numbers make that honest instead of blurry:

*  **The box.** A rail card is `150px`–`190px` wide, so the file must carry `320px` — about two
   pixels per CSS pixel, which is what a Retina screen needs to show a file pixel one for one.
*  **The pixels.** `320×453` is not a shrunk copy of the 300 dpi preview. The page is rasterised
   straight from the PDF's own vectors at exactly that density, encoded PNG, no resampling, no
   filter, no quality step in between. Small here means *fewer pixels*, never *worse ones*.

Reading a paragraph is one click away, and it is the same page: every card links to
`docs/assets/page-*.png` — `2479×3508`, the edition's real density, lossless.

    python3 src/tools/make_shots.py            # write docs/assets/shot-*.png
    python3 src/tools/make_shots.py --check    # fail if the shipped cards are stale

Guards, because "it looked fine once" is not a contract:

*  the six pages are read from `make_previews.SHOTS`, so a card and a full preview can never
   disagree about which page of the book they show;
*  every file is exactly the same box, so the grid has no card jumping against its neighbours;
*  the page must carry real text and must not be near-blank — a card of nothing stops the build;
*  the PNG must decode back to the exact pixels the renderer produced.
"""
from __future__ import annotations
import argparse, pathlib, sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from make_previews import DPI, OUT, PDF, SHOTS as PAGES, png_lossless  # one place per decision

import pymupdf
from PIL import Image, ImageStat

# the CSS box of a rail card, and the file that box needs: shot = 2 × card, so density is 1.7×–2.1×
CARD_PX = (150, 190)
SHOT = (320, 453)                        # px; 320 / 594.96 pt of A4 width
A4 = (594.96, 841.92)                    # pt, the edition's own page box

# card file → the full-page file it links to. Spelled out because `qa.py` reads this literal; the
# guard below keeps it equal to the page list `make_previews.py` publishes, so neither can drift.
SHOTS = {"shot-cover": "page-cover", "shot-toc": "page-toc", "shot-chapter": "page-chapter",
         "shot-code": "page-code", "shot-workshop": "page-workshop", "shot-interview": "page-interview"}
if SHOTS != {f"shot-{k[5:]}": k for k in PAGES}:
    sys.exit("SHOTS no longer matches make_previews.SHOTS — one card per published page, same names")


def shot_bytes(doc, page_no: int) -> bytes:
    """Rasterise one whole page at the card's own density and encode it without loss."""
    page = doc[page_no - 1]
    if (round(page.rect.width), round(page.rect.height)) != (round(A4[0]), round(A4[1])):
        sys.exit(f"page {page_no}: {page.rect.width:.1f}×{page.rect.height:.1f} pt is not the A4 "
                 f"the card size was chosen for")
    words = page.get_text("words")
    if len(words) < 5:
        sys.exit(f"page {page_no}: {len(words)} words — that page has nothing to preview")

    zoom = SHOT[0] / page.rect.width
    pix = page.get_pixmap(matrix=pymupdf.Matrix(zoom, zoom), alpha=False)
    img = Image.frombytes("RGB", (pix.width, pix.height), pix.samples)
    # the renderer rounds its clip outward, so the extra row/column sits on the right and bottom
    if img.width - SHOT[0] not in (0, 1) or img.height - SHOT[1] not in (0, 1):
        sys.exit(f"page {page_no}: render came out {img.width}×{img.height}, expected {SHOT[0]}×{SHOT[1]}(+1)")
    if img.size != SHOT:
        img = img.crop((0, 0, SHOT[0], SHOT[1]))
    stdev = ImageStat.Stat(img.convert("L")).stddev[0]
    if stdev < 12:
        sys.exit(f"page {page_no}: the card is near-blank (stdev {stdev:.1f})")

    return png_lossless(img)


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--check", action="store_true", help="fail if the shipped files differ")
    args = ap.parse_args()

    doc = pymupdf.open(PDF)
    rows, stale = [], []
    for name, (page_no, caption) in PAGES.items():
        out = OUT / (name.replace("page-", "shot-") + ".png")
        blob = shot_bytes(doc, page_no)
        state = "unchanged"
        if out.exists() and out.read_bytes() == blob:
            pass
        elif args.check:
            state, stale = "STALE", stale + [out.name]
        else:
            out.write_bytes(blob)
            state = "written"
        rows.append(f"  {out.name}  {SHOT[0]}×{SHOT[1]}  {len(blob) / 1024:6.0f} KiB  "
                    f"p{page_no}  {caption}  {state}")
    print("\n".join(rows))
    full = (round(A4[0] * DPI / 72), round(A4[1] * DPI / 72))
    print(f"\n  card box {CARD_PX[0]}–{CARD_PX[1]} px · file {SHOT[0]}×{SHOT[1]} px · density "
          f"{SHOT[0] / CARD_PX[1]:.1f}×–{SHOT[0] / CARD_PX[0]:.1f}× the box · each card links to the "
          f"same page at {full[0]}×{full[1]} px")
    if stale:
        sys.exit(f"{', '.join(stale)} are stale — run without --check")


if __name__ == "__main__":
    main()
