#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""RTL EPUB for the Next.js 16 handbook — chapter-grouped page images from the official PDF."""
from __future__ import annotations

import io
import json
import uuid
from pathlib import Path

import pymupdf
from ebooklib import epub
from PIL import Image

ROOT = Path(__file__).resolve().parents[2]
PDF = ROOT / "docs" / "pdf" / "Nextjs16-Persian-Guide.pdf"
OUT = ROOT / "docs" / "pdf" / "Nextjs16-Persian-Guide.epub"
META = ROOT / "src" / "edition" / "chapters.json"

CSS = """
body { font-family: Tahoma, sans-serif; direction: rtl; text-align: right; color: #0f172a; margin: 0; padding: 0.4em; line-height: 1.8; }
h1 { font-size: 1.55em; margin: 0.2em 0 0.6em; }
.kicker { letter-spacing: 0.18em; color: #64748b; font-size: 0.75em; direction: ltr; text-align: center; }
.cover { text-align: center; padding: 1.5em 0; }
.page { margin: 0 0 0.8em; }
.page img { width: 100%; height: auto; border-radius: 6px; }
.sub { color: #475569; }
.toc-list { list-style: none; padding: 0; }
.toc-list li { padding: 0.35em 0; border-bottom: 1px dashed #e2e8f0; }
.toc-part { font-weight: 700; color: #0f172a; margin-top: 1em; border: 0; }
.n { display: inline-block; min-width: 2em; color: #334155; direction: ltr; }
"""


def jpeg_page(page, max_w=1080, quality=72) -> bytes:
    pix = page.get_pixmap(matrix=pymupdf.Matrix(1.35, 1.35), alpha=False)
    im = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
    if im.width > max_w:
        h = int(im.height * max_w / im.width)
        im = im.resize((max_w, h), Image.Resampling.LANCZOS)
    buf = io.BytesIO()
    im.save(buf, "JPEG", quality=quality, optimize=True)
    return buf.getvalue()


def xhtml(body: str) -> str:
    return f'<div dir="rtl" lang="fa">{body}</div>'


def main() -> None:
    data = json.loads(META.read_text(encoding="utf-8"))
    book_meta = data["book"]
    chapters = data["chapters"]
    parts = data["parts"]
    doc = pymupdf.open(str(PDF))
    n_pages = len(doc)

    book = epub.EpubBook()
    book.set_identifier("urn:uuid:" + str(uuid.uuid5(uuid.NAMESPACE_URL, "nextjs-16-persian-guide/1.0.0")))
    book.set_title(book_meta["title"])
    book.set_language("fa")
    book.add_author(book_meta["author"])
    book.add_metadata("DC", "description", "مرجع فارسی Next.js 16 — از App Router تا معماری Production")
    book.add_metadata("DC", "publisher", "Persian Developer Handbook")
    book.add_metadata("DC", "date", str(book_meta["year"]))
    book.add_metadata("DC", "rights", book_meta["license"])
    book.set_direction("rtl")

    css = epub.EpubItem(uid="style", file_name="styles/book.css", media_type="text/css", content=CSS.encode())
    book.add_item(css)
    book.set_cover("images/cover.jpg", jpeg_page(doc[0], max_w=1200, quality=82), create_page=True)

    title = epub.EpubHtml(title="صفحه عنوان", file_name="title.xhtml", lang="fa")
    title.content = xhtml(
        '<section class="cover"><div class="kicker">PERSIAN DEVELOPER HANDBOOK</div>'
        f"<h1>{book_meta['title']}</h1>"
        f'<p class="sub">{book_meta["subtitle"]}</p>'
        f'<p>{book_meta["author"]} · ویرایش {book_meta["edition"]}</p></section>'
    )
    title.add_item(css)
    book.add_item(title)

    toc_items = []
    for p in parts:
        toc_items.append(f'<li class="toc-part">بخش {p["num"]} · {p["name"]}</li>')
        for ch in chapters:
            if p["from"] <= ch["num"] <= p["to"]:
                toc_items.append(
                    f'<li><span class="n">{ch["num"]:02d}</span> <a href="ch-{ch["num"]:02d}.xhtml">{ch["title"]}</a></li>'
                )
    toc_page = epub.EpubHtml(title="فهرست مطالب", file_name="toc.xhtml", lang="fa")
    toc_page.content = xhtml('<h1>فهرست مطالب</h1><ul class="toc-list">' + "".join(toc_items) + "</ul>")
    toc_page.add_item(css)
    book.add_item(toc_page)

    spine = ["nav", title, toc_page]
    nav_toc = [epub.Link("title.xhtml", "صفحه عنوان", "title"), epub.Link("toc.xhtml", "فهرست مطالب", "toc")]
    part_map = {p["num"]: p for p in parts}

    for i, ch in enumerate(chapters):
        start = ch["page"] - 1
        end = (chapters[i + 1]["page"] - 2) if i + 1 < len(chapters) else n_pages - 1
        imgs = []
        body = [f'<h1>{ch["num"]:02d} — {ch["title"]}</h1>', f'<p class="sub">{ch["subtitle"]}</p>']
        for pno in range(start, end + 1):
            name = f"p{pno+1:03d}.jpg"
            data = jpeg_page(doc[pno])
            book.add_item(epub.EpubItem(uid=name, file_name=f"images/{name}", media_type="image/jpeg", content=data))
            body.append(f'<div class="page"><img src="images/{name}" alt="صفحه {pno+1}"/></div>')
            imgs.append(name)
        item = epub.EpubHtml(title=ch["title"], file_name=f"ch-{ch['num']:02d}.xhtml", lang="fa")
        item.content = xhtml("".join(body))
        item.add_item(css)
        book.add_item(item)
        spine.append(item)
        nav_toc.append(item)
        print(f"  ch {ch['num']:02d} pages {start+1}-{end+1} ({len(imgs)} img)")

    book.toc = nav_toc
    book.add_item(epub.EpubNcx())
    book.add_item(epub.EpubNav())
    book.spine = spine
    OUT.parent.mkdir(parents=True, exist_ok=True)
    epub.write_epub(str(OUT), book, {})
    print(f"EPUB -> {OUT} ({OUT.stat().st_size // 1024} KB)")


if __name__ == "__main__":
    main()
