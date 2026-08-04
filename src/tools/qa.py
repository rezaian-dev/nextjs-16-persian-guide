#!/usr/bin/env python3
"""Repository auditor — one command that says whether this repo is self-consistent.

    python3 src/tools/qa.py            # print a report, exit non-zero if anything drifted
    python3 src/tools/qa.py --json     # machine-readable counts (used when writing the README)

Four things rot silently in a documentation repository, so all four are checked here:
  1. the edition: page count, outline, clickable index, language, metadata, paper size;
  2. the data file: chapter headings, order, part coverage;
  3. the imagery: everything README and the Pages site reference exists, and the crops
     still match the file they were cut from;
  4. the prose: README numbers agree with the PDF, Persian digits and the house ezafe
     are used, and no markup GitHub strips appears in the README.
"""
from __future__ import annotations
import argparse, ast, hashlib, io, json, pathlib, re, sys, unicodedata

import pymupdf
from PIL import Image

ROOT = pathlib.Path(__file__).resolve().parents[2]
DATA = json.loads((ROOT / "src" / "edition" / "chapters.json").read_text(encoding="utf-8"))
PDF = ROOT / DATA["book"]["pdf"]
RTL, LTR = 'dir="rtl"', 'dir="ltr"'
fails: list[str] = []
notes: list[str] = []


def ok(label: str, cond, detail: str = "") -> bool:
    cond = bool(cond)
    print(f"  {'PASS' if cond else 'FAIL'}  {label}{(' — ' + detail) if detail else ''}")
    if not cond:
        fails.append(label)
    return cond


def fa(n: int) -> str:
    return "".join(chr(0x06F0 + int(d)) for d in str(n))


def read(p: pathlib.Path) -> str:
    return p.read_text(encoding="utf-8") if p.exists() else ""


def strip_noise(md: str) -> str:
    """Drop fenced code, inline code, links, HTML tags and table separator rows."""
    md = re.sub(r"```.*?```", "", md, flags=re.S)
    md = re.sub(r"`[^`\n]*`", " ", md)
    md = re.sub(r"!??\[[^\]]*\]\([^)]*\)", " ", md)      # markdown links and images
    md = re.sub(r"\]\([^)]*\)", " ", md)                     # the tail of a wrapped badge link
    md = re.sub(r"https?://\S+", " ", md)
    md = re.sub(r"<[^>]+>", " ", md)
    md = re.sub(r"^\|?[:\- |]+\|$", " ", md, flags=re.M)
    return md


def lines_of(page) -> list[tuple[float, str]]:
    out = []
    for blk in page.get_text("dict")["blocks"]:
        if blk.get("type"):
            continue
        for ln in blk["lines"]:
            txt = "".join(s["text"] for s in ln["spans"]).strip()
            if txt:
                out.append((max(s["size"] for s in ln["spans"]), txt))
    return out


def check_edition(doc) -> dict:
    print("\n\033[1medition — the shipped PDF\033[0m")
    book = DATA["book"]
    ok(f"page count is {book['pages']}", doc.page_count == book["pages"], f"{doc.page_count} pages")
    toc = doc.get_toc()
    want = len(DATA["chapters"]) + len(DATA["parts"]) + 2
    ok("outline present", len(toc) == want, f"{len(toc)} bookmarks, expected {want}")
    links = sum(1 for p in doc for l in p.get_links() if l["kind"] == pymupdf.LINK_GOTO)
    ok("index rows are clickable", links == len(DATA["chapters"]), f"{links} GoTo links")
    lang = (doc.xref_get_key(doc.pdf_catalog(), "Lang")[1] or "").strip('()"')
    ok("document language is fa", lang == "fa", repr(lang))
    ok("readers show the title, not the filename",
       "DisplayDocTitletrue" in doc.xref_get_key(doc.pdf_catalog(), "ViewerPreferences")[1].replace(" ", ""))
    m = doc.metadata
    ok("title metadata", m.get("title") == book["title"], repr(m.get("title")))
    ok("author metadata", m.get("author") == book["author"], repr(m.get("author")))
    ok(f"edition {book['edition']} stamped in the keywords", f"edition {book['edition']}" in (m.get("keywords") or ""))
    ok("A4 portrait on every page",
       all(round(p.rect.width) == 595 and round(p.rect.height) == 842 for p in doc))

    body = "".join(p.get_text() for p in doc)
    head_pages = {i + 1 for i, pg in enumerate(doc) for size, _t in lines_of(pg) if abs(size - 22.5) < 0.4}
    counts = {
        "pages": doc.page_count,
        "bookmarks": len(toc),
        "index_links": links,
        "chapters": len(DATA["chapters"]),
        "parts": len(DATA["parts"]),
        "sections": sum(1 for i, pg in enumerate(doc) if i
                        for size, t in lines_of(pg) if abs(size - 16.5) < 0.4 and len(t) > 2),
        "code_windows": sum(1 for p in doc for dr in p.get_drawings()
                            if dr.get("fill") and all(abs(a - b) < 0.02 for a, b in zip(dr["fill"], (0.06, 0.09, 0.16)))
                            and dr["rect"].width > 200 and dr["rect"].height > 25),
        "interview_boxes": sum(1 for p in doc for size, t in lines_of(p) if "🎤" in t),
        "practice": sum(1 for p in doc for size, t in lines_of(p) if "✏️" in t),
        "summaries": sum(1 for p in doc for size, t in lines_of(p) if "📌" in t),
        "compare": sum(1 for p in doc for size, t in lines_of(p)
                         if "✅" in t and "❌" in t and "درست" in t and "اشتباه" in t),
        "mini_projects": body.count("مفاهیم کلیدی"),
        "words": len(re.findall(r"[\u0600-\u06FF][\u0600-\u06FF\u200c\u2005]*", body)),
        "kib": round(PDF.stat().st_size / 1024),
        "heading_pages": len(head_pages),
    }
    ok("each chapter opens on its own heading page", counts["heading_pages"] == len(DATA["chapters"]),
       f"{counts['heading_pages']} pages carry a 22.5 pt heading")
    notes.append(f"edition sha256 {hashlib.sha256(PDF.read_bytes()).hexdigest()[:16]} · {counts['kib']} KiB")
    return counts


def check_data() -> None:
    print("\n\033[1mdata — src/edition/chapters.json\033[0m")
    chs, book = DATA["chapters"], DATA["book"]
    ok("37 chapters", len(chs) == 37, str(len(chs)))
    ok("numbered 1…37 without gaps", [c["num"] for c in chs] == list(range(1, 38)))
    ok("pages strictly increasing", all(a["page"] < b["page"] for a, b in zip(chs, chs[1:])))
    ok("the first chapter opens after the index", chs[0]["page"] == 5, f"p{chs[0]['page']}")
    ok("the last chapter reaches the last page", chs[-1]["page"] + 2 == book["pages"],
       f"{chs[-1]['title']} starts on p{chs[-1]['page']} of {book['pages']}")
    start = {c["num"]: c["page"] for c in chs}
    covered = [n for p in DATA["parts"] for n in range(p["from"], p["to"] + 1)]
    ok("parts cover every chapter exactly once", covered == list(range(1, 38)))
    ok("part page ranges do not overlap", all(
        start[p["from"]] < start[DATA["parts"][i + 1]["from"]] for i, p in enumerate(DATA["parts"][:-1])))
    ok("titles unique", len({c["title"] for c in chs}) == 37)
    ok("every chapter has a subtitle", all(len(c["subtitle"]) > 8 for c in chs))
    ok("ezafe written as هٔ", "ۀ" not in json.dumps(DATA, ensure_ascii=False))
    for i, part in enumerate(DATA["parts"]):
        nxt = DATA["parts"][i + 1] if i + 1 < len(DATA["parts"]) else None
        last = start[nxt["from"]] - 1 if nxt else book["pages"]
        print(f"        بخش {fa(i + 1)} · {part['name']}: فصل {fa(part['from'])}–{fa(part['to'])}"
              f" · ص {fa(start[part['from']])}–{fa(last)}")


DPI = 300          # the density of the rasters the edition itself carries


def avatar_spec() -> tuple[int, int]:
    """The avatar's file size and the box the README paints it in — read out of make_avatar.py."""
    src = read(ROOT / "src" / "tools" / "make_avatar.py")
    return (int(re.search(r"^AVATAR = (\d+)", src, re.M).group(1)),
            int(re.search(r"^PAINT = (\d+)", src, re.M).group(1)))


AVATAR_PX, AVATAR_PAINT = avatar_spec()


def portrait_xref(doc):
    """The cover image that sits where the portrait ring was measured."""
    for im in doc[0].get_images(full=True):
        rects = doc[0].get_image_rects(im[0])
        if rects and im[2] >= 300 and abs(rects[0].x0 - 371.7) < 8 and abs(rects[0].width - 72) < 8:
            return im[0]
    return None


def published_shots() -> tuple[dict, tuple[int, int], tuple[int, int]]:
    """The cards the gallery must show, the page each one clicks through to, the file size that box
    needs and the CSS box itself — read out of `make_shots.py`, so qa quotes one source at a time."""
    src = read(ROOT / "src" / "tools" / "make_shots.py")
    shot = ast.literal_eval(re.search(r"^SHOT = (\([^)]*\))", src, re.M).group(1))
    card = ast.literal_eval(re.search(r"^CARD_PX = (\([^)]*\))", src, re.M).group(1))
    body = re.search(r"^SHOTS = \{(.*)\}$", src, re.M | re.S).group(1)
    return dict(ast.literal_eval("{" + " ".join(body.split()) + "}")), shot, card



def portrait_bytes(doc) -> bytes | None:
    xref = portrait_xref(doc)
    return doc.extract_image(xref)["image"] if xref else None


def portrait_size(doc) -> tuple[int, int]:
    xref = portrait_xref(doc)
    if not xref:
        return (560, 560)
    info = doc.extract_image(xref)
    return (info["width"], info["height"])


counts_extra: dict = {}


def check_assets() -> None:
    print("\n\033[1massets — what the docs point at\033[0m")
    readme, site = read(ROOT / "README.md"), read(ROOT / "docs" / "index.html")
    refs = set(re.findall(r"\]\((\./[^)#\s]+)\)", readme))            # markdown links
    refs |= set(re.findall(r'(?:src|href)="(\./[^"#\s]+)"', readme))     # and the HTML the README uses
    for ref in sorted(refs):
        ok(f"README → {ref}", (ROOT / ref[2:]).exists())
    refs = set(re.findall(r'(?:src|href)="((?!https?:|#|mailto:|data:)[^"]+)"', site))
    for ref in sorted(refs):
        ok(f"site → {ref}", (ROOT / "docs" / ref).exists() or (ROOT / ref).exists())

    doc = pymupdf.open(ROOT / DATA["book"]["pdf"])
    rect = doc[0].rect
    page_px = (round(rect.width * DPI / 72), round(rect.height * DPI / 72))
    want = {name: page_px for name in ("page-cover", "page-toc", "page-chapter",
                                      "page-code", "page-workshop", "page-interview")}
    want["author"] = portrait_size(doc)
    want["avatar"] = (AVATAR_PX, AVATAR_PX)   # the README's round headshot, made for a 120 px box
    cards, SHOT_IMG, CARD = published_shots()
    for name in cards:
        want[name] = SHOT_IMG
    want["social-card"] = (1254, 627)          # the banner's own width, half of its height
    # Favicons and the apple-touch icon: small, square, referenced from <head>.
    for name, px in (("next-logo-32", 32), ("next-logo-64", 64), ("next-logo-128", 128)):
        want[name] = (px, px)
    # The published master images stay at the root. Optimized web assets and fonts
    # live in subdirectories and are validated separately in check_prose().
    have = {p.stem: p for p in (ROOT / "docs" / "assets").glob("*")
            if p.is_file() and p.suffix.lower() == ".png"}
    ok(f"docs/assets holds exactly the {len(want)} published images", set(have) == set(want),
       f"{sorted(set(have) ^ set(want))}")
    ok("every asset ships as PNG (lossless, no ring around glyphs)",
       have and all(p.suffix == ".png" for p in have.values()),
       f"{sorted({p.suffix for p in have.values()})}")
    for name, (w, h) in want.items():
        p = have.get(name)
        if not p:
            ok(f"{name}.png exists", False, "missing")
            continue
        im = Image.open(p)
        size = f"{im.format} {im.size[0]}×{im.size[1]} · {p.stat().st_size / 1024:.0f} KiB"
        if name.startswith("page-"):
            size += f" · {DPI} dpi of an A4 page"
        elif name.startswith("shot-"):
            size += f" · a whole A4 page for a {CARD[0]}–{CARD[1]} px card, {SHOT_IMG[0] / CARD[1]:.1f}× the box"
        # The avatar's corners and the favicons' rounded mark must be transparent.
        transparent = name == "avatar" or name.startswith("next-logo-")
        mode = "RGBA" if transparent else "RGB"
        ok(f"{p.name} is {w}×{h} {mode} PNG",
           im.size == (w, h) and im.format == "PNG" and im.mode == mode, size)
    ok("previews are cut at the sizes the gallery promises",
       all(Image.open(p).size == page_px for n, p in have.items() if n.startswith("page-"))
       and all(Image.open(p).size == SHOT_IMG for n, p in have.items() if n.startswith("shot-")),
       f"pages {page_px[0]}×{page_px[1]} at {DPI} dpi · cards {SHOT_IMG[0]}×{SHOT_IMG[1]} "
       f"for a {CARD[0]}–{CARD[1]} px box")
    av = have.get("avatar")
    if av:
        im = Image.open(av)
        r, g, b, a = im.convert("RGBA").split()
        corners = [a.getpixel(xy) for xy in ((0, 0), (im.width - 1, 0), (0, im.height - 1),
                                             (im.width - 1, im.height - 1))]
        centre = a.getpixel((im.width // 2, im.height // 2))
        ok("the avatar is a circle, not a square with hard corners",
           max(corners) == 0 and centre == 255, f"corner alpha {corners[0]} · centre alpha {centre}")
        ok("the avatar file is denser than the box it is painted in",
           im.width >= AVATAR_PAINT * 2, f"{im.width} px file for a {AVATAR_PAINT} px box "
           f"({im.width / AVATAR_PAINT:.0f}×)")
    blob = portrait_bytes(doc)
    if blob and "author" in have:
        ok("author.png is the cover's embedded portrait, byte for byte",
           have["author"].read_bytes() == blob, f"{len(blob) / 1024:.0f} KiB")
    banner = ROOT / "src" / "banner" / "banner.png"
    if banner.exists():
        im = Image.open(banner).convert("RGB")
        ok("banner is the 1254² master", im.size == (1254, 1254), f"{im.size}")
        card = ROOT / "docs" / "assets" / "social-card.png"
        if card.exists():
            buf = io.BytesIO()
            im.crop((0, 0, im.width, im.width // 2)).save(buf, "PNG", optimize=True, compress_level=9)
            ok("social-card.png is the banner's title band, uncropped and unresampled",
               buf.getvalue() == card.read_bytes(), f"{card.stat().st_size / 1024:.0f} KiB")
    total = sum(p.stat().st_size for p in have.values())
    counts_extra["assets_kib"] = total // 1024
    ok("the imagery stays light enough for the landing page", 2 << 20 < total < 12 << 20,
       f"{total / 1e6:.1f} MB across {len(have)} files")
    empties = [p for p in ROOT.rglob("*") if p.is_file() and p.stat().st_size == 0
               and ".git" not in p.parts and p.name != ".nojekyll"]   # an empty .nojekyll is the point
    ok("no empty files", not empties, f"{[p.name for p in empties]}")
    def ignorable(q: pathlib.Path) -> bool:
        """True when .gitignore already covers q — junk that can never reach a commit."""
        rel = q.relative_to(ROOT)
        for pat in (line.strip().rstrip("/") for line in read(ROOT / ".gitignore").splitlines()):
            if pat and not pat.startswith(("#", "!")) and (pat in rel.parts or rel.match(pat) or rel.match(pat + "/*")):
                return True
        return False

    junk = sorted({q for pat in ("*.tmp", "*.pyc", "__pycache__", ".DS_Store", "Thumbs.db")
                   for q in ROOT.rglob(pat) if ".git" not in q.parts})
    real = [q for q in junk if not ignorable(q)]
    ok("no build junk that git could commit", not real, f"{[q.name for q in real]}")
    if len(junk) != len(real):
        notes.append(f"{len(junk) - len(real)} gitignored artefact(s) in the tree — never committed")
    ok("one edition, one home", len(list(ROOT.rglob("*.pdf"))) == 1,
       f"{[str(p.relative_to(ROOT)) for p in ROOT.rglob('*.pdf')]}")


# letters that exist in the Arabic block but in no Persian word — a slipped keyboard or a bad
# transliteration leaves exactly these behind (heh-do-chashmee for ه, ډ-for چ, noon-ghunna for ن …)
FOREIGN_LETTERS = set("\u06be\u0689\u068d\u0691\u0693\u0695\u0696\u0697\u0699\u069a\u069b\u06ba\u06bb"
                      "\u06bc\u06bd\u06c0\u06c1\u06c3\u06c5\u06c6\u06c7\u06c8\u06c9\u06ca\u06cb\u06cd"
                      "\u06d3\u06d5\u0671\u0673\u0677\u0679\u067b\u067d\u0680\u0682\u0687\u068b\u0690")


def foreign_letters(txt: str) -> list[str]:
    """Letters Persian never writes — the signature of a bad transliteration in generated prose."""
    found = {c for c in txt if c in FOREIGN_LETTERS}
    found |= {c for c in txt if "\ufef0" <= c <= "\ufefc"}        # Arabic presentation forms
    return sorted(found)

def first_strong(txt: str) -> str:
    """First letter/number of a block — what GitHub's dir="auto" resolves against."""
    for ch in re.sub(r"[^\w]+", " ", re.sub(r"<[^>]+>", "", txt), flags=re.U):
        if ch.strip() and unicodedata.category(ch)[0] in ("L", "N"):
            return ch
    return ""


def first_strong_blocks(raw: str) -> None:
    """Every block must START with a Persian letter. GitHub stamps dir="auto" on each <p>, <li>
    and <h*>, so a Latin first letter silently flips that single block to LTR mid-document."""
    txt = re.sub(r"```.*?```", " ", raw, flags=re.S)          # code fences stay LTR on purpose
    txt = re.sub(r"!\[[^\]]*\]\([^)]*\)", " ", txt)          # images (badge rows) are LTR by design
    txt = re.sub(r"<[^>]+>", " ", txt)
    txt = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", txt)      # keep the link text, drop the URL
    bad = []
    for block in re.split(r"\n\s*\n", txt):
        b = block.strip()
        if not b or b.startswith(("<", "|", "---")):
            continue
        b = re.sub(r"^#{1,6}\s*", "", b)                       # headings get dir="auto" too
        b = re.sub(r"^(?:[-*]|\d+\.)\s+", "", b)
        c = first_strong(b.replace("`", "").replace("*", ""))
        if c.isascii() and c.isalnum():
            bad.append(b[:44])
    ok("every block starts with a Persian letter (dir=auto safe)", not bad, f"{bad[:2]}")


def check_prose(counts: dict) -> None:
    """Validate the coordinated README and responsive Pages presentation.

    The landing page deliberately keeps presentation in ``assets/site.css`` and
    behavior in ``assets/site.js``. These checks focus on durable contracts
    (content, accessibility, responsive behavior and asset references), rather
    than coupling QA to a particular card/grid implementation.
    """
    print("\n\033[1mprose — README.md and the Pages site\033[0m")
    readme = read(ROOT / "README.md")
    site = read(ROOT / "docs" / "index.html")
    css = read(ROOT / "docs" / "assets" / "site.css")
    js = read(ROOT / "docs" / "assets" / "site.js")

    ok("README.md exists", bool(readme.strip()))
    ok("Pages landing page exists", bool(site.strip()))
    if not readme or not site:
        return

    # GitHub-safe, mobile-safe README structure.
    ok("Persian README content declares RTL", RTL in readme)
    ok("README has no wide Markdown tables", not re.search(r"^\s*\|.*\|\s*$", readme, re.M))
    ok("README disclosure groups are balanced",
       readme.count("<details>") == readme.count("</details>") == len(DATA["parts"]),
       f"{readme.count('<details>')} groups")
    ok("README has no markup GitHub strips",
       not re.search(r"\s(?:style|bgcolor)=", readme, re.I))
    ok("README imagery has no fixed height", not any("height=" in tag for tag in re.findall(r"<img [^>]*>", readme)))

    # The chapter index remains a projection of the canonical JSON data.
    rows = re.findall(
        r"^(\d+)\. \[([^\]]+)\]\(\./docs/pdf/[^)]+#page=(\d+)\)",
        readme,
        re.M,
    )
    ok("37 chapter links in the README", len(rows) == len(DATA["chapters"]), f"{len(rows)} links")
    drift = []
    for pos, (num, title, page) in enumerate(rows):
        if pos >= len(DATA["chapters"]):
            drift.append(num)
            continue
        chapter = DATA["chapters"][pos]
        if (int(num), title.strip(), int(page)) != (chapter["num"], chapter["title"], chapter["page"]):
            drift.append(num)
    ok("README chapter links agree with chapters.json", not drift, f"drift at {drift[:3]}")
    ok(f"{fa(counts['pages'])} pages matches the PDF", f"{fa(counts['pages'])} صفحه" in readme)
    ok(f"{fa(counts['chapters'])} chapters matches the data file", f"{fa(counts['chapters'])} فصل" in readme)
    ok(f"the code-window count agrees ({fa(counts['code_windows'])})",
       f"{fa(counts['code_windows'])} پنجرهٔ کد" in readme)

    # Prose hygiene shared by the README and landing page.
    prose = readme + site
    ok("house ezafe only", "ۀ" not in prose and "هٔ" in prose)
    ok("no letter outside the Persian alphabet", not foreign_letters(prose),
       f"{[f'U+{ord(c):04X}' for c in foreign_letters(prose)][:4]}")
    ok("no ZWNJ pile-ups", "‌‌" not in prose and not re.search(r"‌[،.:؛)!؟]", prose))
    ok("no insecure links", not re.findall(r'(?:href=|\]\()"?http://', readme + site)
       and "http://www.w3.org" not in readme)
    ok("no placeholders left", not re.search(r"TODO|FIXME|Lorem ipsum", site + readme))

    # Semantic and metadata contracts of the Pages site.
    ok("site declares Persian language and direction", '<html lang="fa" dir="rtl">' in site)
    ok("site ships Book JSON-LD", '"@type":"Book"' in re.sub(r"\s+", "", site))
    ok("site has canonical and absolute social image metadata",
       '<link rel="canonical" href="https://' in site and 'property="og:image" content="https://' in site)
    title = re.search(r"<title>(.*?)</title>", site, re.S)
    ok("site title names the book", bool(title) and "Next.js 16" in title.group(1))
    ok("site page count agrees with the edition", f"{fa(counts['pages'])} صفحه" in site)
    ok("site exposes a skip link and labelled navigation",
       'class="skip-link"' in site and 'aria-label="ناوبری اصلی"' in site)
    ok("mobile menu has an accessible state contract",
       'class="menu-toggle"' in site and 'aria-controls="mobile-menu"' in site
       and 'aria-expanded="false"' in site and 'Escape' in js
       and 'aria-label="بستن منو"' in site)
    ok("responsive cover uses srcset", "cover-hero-480.webp 480w" in site
       and "cover-hero-720.webp 720w" in site
       and re.search(r"cover-hero\.webp \d+w", site) is not None)
    ok("preview images are lazy loaded", site.count('loading="lazy"') >= 6)

    # The numeral-font regression that prompted the redesign: all Persian metrics
    # explicitly use Vazirmatn; JetBrains Mono remains limited to Latin/code labels.
    font_dir = ROOT / "docs" / "assets" / "fonts"
    fonts = [
        "Vazirmatn-Regular.woff2", "Vazirmatn-Medium.woff2",
        "Vazirmatn-Bold.woff2", "Vazirmatn-ExtraBold.woff2",
        "JetBrainsMono-Regular.woff2", "JetBrainsMono-Bold.woff2",
    ]
    ok("all six local font files exist", all((font_dir / name).is_file() for name in fonts))
    font_license = read(font_dir / "OFL.txt")
    ok("font copyright notices and OFL license ship with the files",
       "Vazirmatn Project Authors" in font_license
       and "JetBrains Mono Project Authors" in font_license
       and "SIL OPEN FONT LICENSE Version 1.1" in font_license)
    ok("site has no remote font dependency", "fonts.googleapis.com" not in site + css
       and "fonts.gstatic.com" not in site + css)
    flat = re.sub(r"\s+", "", css)
    ok("Persian metrics use the Persian font",
       "font-family:Vazirmatn,Tahoma,sans-serif" in flat)
    ok("Latin and code labels use the mono font",
       "font-family:JetBrainsMono,Consolas,monospace" in flat)

    # Responsive CSS and optimized publishing assets are first-class deliverables.
    # The online edition: every page of the PDF, reachable and deep-linkable.
    reader = ROOT / "docs" / "book" / "index.html"
    ok("the online edition ships", reader.exists())
    if reader.exists():
        rd = reader.read_text(encoding="utf-8")
        n_img = len(list((ROOT / "docs" / "book" / "pages").glob("p*.webp")))
        ok("the reader holds every page of the edition", n_img == counts["pages"],
           f"{n_img} images / {counts['pages']} pages")
        missing = [c["num"] for c in DATA["chapters"] if f'id="ch-{c["num"]:02d}"' not in rd]
        ok("every chapter is deep-linkable", not missing, f"missing {missing}" if missing else "")
        ok("the reader lazy-loads all but the first pages",
           rd.count('loading="lazy"') >= counts["pages"] - 2)
        page_imgs = re.findall(r"<img[^>]*>", rd)
        sized = [t for t in page_imgs if "width=" in t and "height=" in t]
        ok("the reader reserves space for every page",
           len(page_imgs) == counts["pages"] and len(sized) == len(page_imgs),
           f"{len(sized)}/{len(page_imgs)} sized")
        ok("the site links the online edition", 'href="book/"' in site)

    ok("site links the shared stylesheet and script",
       'href="assets/site.css"' in site and 'src="assets/site.js"' in site)
    ok("site includes desktop, tablet and compact breakpoints",
       all(f"@media(max-width:{width}px)" in flat for width in (1023, 767, 390)))
    ok("reduced-motion users are respected", "@media(prefers-reduced-motion:reduce)" in flat)
    ok("keyboard focus remains visible", ":focus-visible" in css)
    web = ROOT / "docs" / "assets" / "web"
    optimized = [
        "readme-hero-architecture.webp", "cover-hero.webp", "cover-hero-480.webp", "cover-hero-720.webp",
        "preview-toc.webp", "preview-chapter.webp", "preview-code.webp",
        "preview-workshop.webp", "preview-interview.webp", "author.webp",
    ]
    ok("optimized WebP publishing assets exist", all((web / name).is_file() for name in optimized),
       f"{sum((web / name).is_file() for name in optimized)}/{len(optimized)} files")

    for tag in ("section", "details", "div"):
        opened = len(re.findall(fr"<{tag}(?:\s|>)", site))
        closed = len(re.findall(fr"</{tag}>", site))
        ok(f"<{tag}> balanced in the site", opened == closed, f"{opened} open / {closed} close")

def main() -> None:
    ap = argparse.ArgumentParser(description="audit the repository")
    ap.add_argument("--json", action="store_true", help="print the counts as JSON")
    args = ap.parse_args()
    if not PDF.exists():
        sys.exit(f"missing {PDF.relative_to(ROOT)}")
    with pymupdf.open(PDF) as doc:
        counts = check_edition(doc)
    check_data()
    check_assets()
    check_prose(counts)
    files = sorted(str(p.relative_to(ROOT)) for p in ROOT.rglob("*")
                   if p.is_file() and ".git" not in p.parts and "__pycache__" not in p.parts)
    print("\n\033[1mnotes\033[0m")
    for line in (notes or ["none"]):
        print(f"   · {line}")
    print(f"   · inventory: {len(files)} files · {len([f for f in files if '/' not in f])} at the root")
    if counts_extra.get("assets_kib"):
        _cards, shot_img, card = published_shots()
        print(f"   · imagery: {counts_extra['assets_kib'] / 1024:.1f} MB of lossless PNG · whole pages at "
              f"{DPI} dpi, gallery cards at {shot_img[0]} px for a {card[0]}–{card[1]} px box")
    if args.json:
        print(json.dumps({**counts, **counts_extra, "files": len(files)}, ensure_ascii=False, indent=2))
        return
    if fails:
        sys.exit(f"\n  \033[31m{len(fails)} check(s) failed\033[0m: {', '.join(fails[:6])}")
    print("\n  all checks passed ✅")


if __name__ == "__main__":
    main()
