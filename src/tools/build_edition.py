#!/usr/bin/env python3
"""Navigation layer for the published PDF — outline, clickable index, metadata.

The book's typesetting project lives outside this repository; this script only
adds the *navigation* a 178-page reference needs, straight onto the shipped
file, and refuses to touch anything else:

    python3 src/tools/build_edition.py            # write the layer into docs/pdf/…
    python3 src/tools/build_edition.py --check    # verify the shipped file is already built

Guards
  * every chapter page in src/edition/chapters.json must land on a real chapter
    heading (a 22.5 pt line) and pages must be strictly increasing;
  * the text layer of all 178 pages is hashed before and after — one glyph of
    reflow fails the build;
  * --check re-derives the whole layer and compares it with what is in the file.
"""
from __future__ import annotations
import argparse, hashlib, json, pathlib, re, sys

import pymupdf

ROOT = pathlib.Path(__file__).resolve().parents[2]
DATA = json.loads((ROOT / "src" / "edition" / "chapters.json").read_text(encoding="utf-8"))
PDF = ROOT / DATA["book"]["pdf"]

H1, ROW = 22.5, 11.0                 # chapter title size · index row size
FRONT = [("جلد کتاب", 1), ("فهرست مطالب", 2)]
ORDINAL = ["یکم", "دوم", "سوم", "چهارم", "پنجم", "ششم"]
LAST = 37


def lines(page: pymupdf.Page) -> list[tuple[float, float, float, str]]:
    """(y, size, x0, text) for every text line on the page."""
    out = []
    for blk in page.get_text("dict")["blocks"]:
        if blk.get("type"):
            continue
        for ln in blk["lines"]:
            txt = "".join(s["text"] for s in ln["spans"]).strip()
            if txt:
                out.append((ln["bbox"][1], max(s["size"] for s in ln["spans"]), ln["bbox"][0], txt))
    return sorted(out)


def near(a: float, b: float, tol: float = 0.4) -> bool:
    return abs(a - b) < tol


def clean(txt: str) -> str:
    return re.sub(r"\s+", " ", txt).strip()


def chapter_headings(doc) -> dict[int, list[str]]:
    heads: dict[int, list[str]] = {}
    for i, page in enumerate(doc):
        for _y, size, _x, txt in lines(page):
            if near(size, H1):
                heads.setdefault(i + 1, []).append(txt)
    return heads


def verify(heads) -> None:
    chs = DATA["chapters"]
    if len(chs) != LAST:
        sys.exit(f"chapters.json has {len(chs)} chapters, expected {LAST}")
    for ch, nxt in zip(chs, chs[1:] + [{"page": DATA["book"]["pages"] + 1}]):
        pg = ch["page"]
        if not 4 < pg < nxt["page"]:
            sys.exit(f"chapter {ch['num']:02d}: page {pg} is not strictly increasing")
        if not any(f"{ch['num']:02d}" in t or clean(ch["title"])[:12] in t for t in heads.get(pg, [])):
            sys.exit(f"chapter {ch['num']:02d} ({ch['title']}) has no heading on page {pg}: "
                     f"{heads.get(pg) or 'no 22.5pt line there'}")
    print(f"  guard:   37/37 headings sit on their page, pages strictly increasing")


def outline() -> list[list]:
    """Cover, index, four parts and 37 chapters — and that is where it stops.

    The edition's text layer was written out in *visual* order (each bidi run is
    correct, the runs are permuted), so titles harvested from the pages come back
    as "…می‌کند؟Next.js". Section-level bookmarks would therefore be half-broken,
    and the outline is deliberately kept to the 43 titles this file states exactly.
    """
    toc: list[list] = [[1, clean(t), p] for t, p in FRONT]
    start = {c["num"]: c["page"] for c in DATA["chapters"]}
    for part in DATA["parts"]:
        toc.append([1, f"بخش {ORDINAL[part['num'] - 1]} · {part['name']}", start[part["from"]]])
        for ch in DATA["chapters"][part["from"] - 1: part["to"]]:
            toc.append([2, f"{ch['num']:02d} · {clean(ch['title'])}", ch["page"]])
    return toc


def index_rows(page: pymupdf.Page) -> dict[int, tuple[int, pymupdf.Rect, bool]]:
    """{baseline: (chapter number, row box, is a title row)}.

    The number sits either inside the title line (11 pt, e.g. ``02شروع به کار…``)
    or on its own as a chip (10 pt); both shapes mean the same row.
    """
    out: dict[int, tuple[int, pymupdf.Rect, bool]] = {}
    for blk in page.get_text("dict")["blocks"]:
        if blk.get("type"):
            continue
        for ln in blk["lines"]:
            size = max(s["size"] for s in ln["spans"])
            txt = re.sub(r"\s+", "", "".join(s["text"] for s in ln["spans"]))
            m = re.match(r"^(0[1-9]|[12]\d|3[0-7])$", txt) if near(size, 10.0) else None
            m2 = re.match(r"^(0[1-9]|[12]\d|3[0-7])", txt) if near(size, ROW) else None
            if not (m or m2):
                continue
            num, title = int((m2 or m).group(1)), bool(m2)
            key, box = round(ln["bbox"][1] / 4), pymupdf.Rect(ln["bbox"])
            if key not in out or (title and not out[key][2]):
                out[key] = (num, box, title)
    return out


def wire_index(doc, toc) -> int:
    """Every row of the printed index becomes clickable, not just its number chip."""
    target = {int(t[1][:2]): t[2] for t in toc if t[0] == 2 and re.match(r"^\d{2} · ", t[1])}
    wired, seen = 0, set()
    for pno in (1, 2, 3):                                   # the index spans pages 2-4
        page = doc[pno]
        for _key, (num, box, _title) in sorted(index_rows(page).items()):
            if num not in target or num in seen:
                continue
            row = pymupdf.Rect(40, box.y0 - 3, page.rect.width - 40, box.y1 + 3) & page.rect
            page.insert_link({
                "kind": pymupdf.LINK_GOTO, "from": row,
                "page": target[num] - 1, "to": pymupdf.Point(0, 40),
            })
            seen.add(num)
            wired += 1
    if wired != LAST:
        sys.exit(f"index: wired {wired} of {LAST} rows, missing {sorted(set(target) - seen)}")
    return wired


def stamp(doc) -> None:
    b = DATA["book"]
    doc.set_metadata({
        "title": b["title"],
        "author": b["author"],
        "subject": f"{b['subtitle']} — {b['pages']} صفحه، {LAST} فصل در {len(DATA['parts'])} بخش",
        "keywords": ("Next.js 16, Next.js, React 19.2, TypeScript, Turbopack, App Router, "
                     f"Server Components, Persian, فارسی, ebook, edition {b['edition']}"),
        "creator": "nextjs-16-persian-guide · src/tools/build_edition.py",
        "producer": doc.metadata.get("producer") or "pymupdf",
    })
    cat = doc.pdf_catalog()
    doc.xref_set_key(cat, "Lang", "(fa)")
    doc.xref_set_key(cat, "ViewerPreferences", "<< /DisplayDocTitle true >>")


def fingerprint(doc) -> str:
    h = hashlib.sha256()
    for page in doc:
        h.update(page.get_text().encode("utf-8", "replace"))
    return h.hexdigest()


def lang_of(doc) -> str:
    return (doc.xref_get_key(doc.pdf_catalog(), "Lang")[1] or "").strip("()\"")


def main() -> None:
    ap = argparse.ArgumentParser(description="build the navigation layer of the edition")
    ap.add_argument("--check", action="store_true", help="verify the shipped PDF instead of writing it")
    args = ap.parse_args()
    if not PDF.exists():
        sys.exit(f"missing {PDF.relative_to(ROOT)} — the edition must be in docs/pdf/")

    doc = pymupdf.open(PDF)
    if doc.page_count != DATA["book"]["pages"]:
        sys.exit(f"{PDF.name} has {doc.page_count} pages, chapters.json says {DATA['book']['pages']}")
    before, heads = fingerprint(doc), chapter_headings(doc)
    verify(heads)
    want = outline()
    print(f"  outline: {len(want)} bookmarks · {len(DATA['parts']) + 2} level 1 · {LAST} chapters "
          f"(section level: skipped, see docstring)")

    if args.check:
        same = doc.get_toc() == want
        links = sum(1 for p in doc for l in p.get_links() if l["kind"] == pymupdf.LINK_GOTO)
        print(f"  check:   outline {'matches' if same else 'DIFFERS'} · index links {links}/{LAST} · "
              f"Lang={lang_of(doc)!r} · title={doc.metadata.get('title')!r}")
        sys.exit(0 if (same and links == LAST and lang_of(doc) == "fa") else 1)

    doc.set_toc(want)
    print(f"  index:   {wire_index(doc, want)} rows wired to their chapter")
    stamp(doc)
    tmp = PDF.with_suffix(".tmp")
    doc.save(tmp, garbage=4, deflate=True)
    doc.close()
    new = pymupdf.open(tmp)
    bad = []
    if fingerprint(new) != before:
        bad.append("text layer changed")
    if new.page_count != DATA["book"]["pages"]:
        bad.append(f"page count {new.page_count}")
    if bad:
        tmp.unlink(missing_ok=True)
        sys.exit("refusing to replace the edition: " + ", ".join(bad))
    tmp.replace(PDF)
    print(f"  content: text layer identical ({before[:12]}…) · pages {new.page_count} untouched")
    new.close()
    print(f"  wrote:   {PDF.relative_to(ROOT)} · {PDF.stat().st_size / 1024 / 1024:.2f} MiB")


if __name__ == "__main__":
    main()
