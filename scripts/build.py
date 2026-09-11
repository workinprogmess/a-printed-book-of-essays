"""build book.html + cover.html for one volume.

usage: python3 scripts/build.py [volume-number]

reads the essays that scripts/fetch.py saved into essays/, turns pg's
old-school <font>/<br><br> markup into clean paragraphs, and writes the
two html files that paged.js lays out.
"""
from __future__ import annotations

import datetime
import html
import re
import sys
from pathlib import Path

PROJECT = Path(__file__).resolve().parent.parent
ESSAYS = PROJECT / "essays"
sys.path.insert(0, str(PROJECT))

LOWERCASE = True   # set False to keep pg's capitals
PRINTED = datetime.date.today().strftime("%B %Y").lower()

# ---------------------------------------------------------------------------
# volumes. edit here to swap essays in and out. order = reading order.
# ---------------------------------------------------------------------------
from volumes import VOLUMES  # noqa: E402


# ---------------------------------------------------------------------------
# parsing pg's html
# ---------------------------------------------------------------------------
def lower_text(fragment: str) -> str:
    """lowercase the text between tags, leave the tags alone."""
    return re.sub(r">([^<]+)<", lambda m: ">" + m.group(1).lower() + "<", f">{fragment}<")[1:-1]


def parse_essay(slug: str) -> dict:
    path = ESSAYS / f"{slug}.html"
    if not path.exists():
        sys.exit(f"essays/{slug}.html is missing. run: python3 scripts/fetch.py")
    raw_bytes = path.read_bytes()
    try:
        raw = raw_bytes.decode("utf-8")
    except UnicodeDecodeError:
        raw = raw_bytes.decode("cp1252", errors="replace")  # pg's older pages
    m = re.search(r'<img[^>]*alt="([^"]+)"[^>]*/?>', raw)
    title = html.unescape(m.group(1)).strip() if m else slug
    start = m.end() if m else 0
    body = raw[start:]
    end = body.find("</font></td></tr></table>")
    if end != -1:
        body = body[:end]

    body = re.sub(r"<!--.*?-->", "", body, flags=re.S)
    body = re.sub(r"<script.*?</script>", "", body, flags=re.S)

    # footnote references: <font color=#dddddd>[<a href="#f1n"><font color=#dddddd>1</font></a>]</font>
    # pg wraps these in different <font> colours over the years; accept any
    body = re.sub(
        r'(?:<font[^>]*>)?\[<a href="#f(\d+)n">(?:<font[^>]*>)?\d+(?:</font>)?</a>\](?:</font>)?',
        r'<sup class="fn">\1</sup>', body)
    # notes: [<a name="f1n"><font color=#000000>1</font></a>]
    body = re.sub(r'\[<a name="f(\d+)n">(?:<font[^>]*>)?\d+(?:</font>)?</a>\]',
                  r'<span class="note-no">\1</span>', body)
    body = re.sub(r"<b>Notes?</b>", "<h3>notes</h3>", body)

    body = re.sub(r"<img[^>]*>", "", body)
    body = re.sub(r"</?(?:table|tr|td|p)\b[^>]*>", "", body)  # remnants of the yc banner table
    body = re.sub(r"<a\s[^>]*>", "", body, flags=re.S | re.I)
    body = re.sub(r"</a\s*>", "", body, flags=re.I)
    body = re.sub(r"</?u>", "", body)
    body = re.sub(r"</?font[^>]*>", "", body)
    body = re.sub(r"</?xa[^>]*>", "", body)
    body = re.sub(r"<br\s*/?>\s*<br\s*/?>", "\n\n", body)
    body = re.sub(r"<br\s*/?>", "<br>", body)

    blocks = []
    in_notes = False
    for chunk in re.split(r"\n\s*\n", body):
        chunk = chunk.strip()
        if not chunk:
            continue
        if "Want to start a startup?" in chunk and len(chunk) < 200:
            continue  # pg's old yc banner line
        chunk = re.sub(r"\s*\n\s*", " ", chunk) if not chunk.startswith("<pre") else chunk
        if chunk.startswith("<h3>"):
            in_notes = True
        # older essays mark footnotes as plain text: "[3]" in the body, "[3] ..." in the notes
        if in_notes and re.match(r"\[(\d+)\]", chunk):
            chunk = re.sub(r"^\[(\d+)\]\s*", r'<span class="note-no">\1</span>', chunk)
        elif not in_notes:
            chunk = re.sub(r"\s*\[(\d+)\]", r'<sup class="fn">\1</sup>', chunk)
        if chunk.startswith(("<h3>", "<pre", "<blockquote", "<ul", "<ol")):
            blocks.append(chunk)
        elif chunk.startswith('<span class="note-no">'):
            blocks.append(f'<p class="note">{chunk}</p>')
        else:
            blocks.append(f"<p>{chunk}</p>")

    date = ""
    if blocks and re.fullmatch(r"<p>(?:[A-Z][a-z]+ )?\d{4}(?:,? ?rev\.? [A-Z][a-z]+ \d{4})?</p>", blocks[0]):
        date = re.sub(r"</?p>", "", blocks.pop(0)).lower()
    elif blocks and re.fullmatch(r"<p>[A-Z][a-z]+ \d{4}.{0,60}</p>", blocks[0]):
        date = re.sub(r"</?p>", "", blocks.pop(0)).lower()

    for i, b in enumerate(blocks):
        if re.match(r"<p><b>Thanks</b>|<p>Thanks to ", b):
            blocks[i] = b.replace("<p>", '<p class="thanks">', 1)

    text = re.sub(r"<[^>]+>", " ", " ".join(blocks))
    words = len(html.unescape(text).split())
    if LOWERCASE:
        blocks = [lower_text(b) for b in blocks]
    return {"slug": slug, "title": title, "date": date, "blocks": blocks, "words": words}


# ---------------------------------------------------------------------------
# html
# ---------------------------------------------------------------------------
HEAD = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>{title}</title>
<link rel="stylesheet" href="styles.css">
<script>window.PagedConfig = {{ auto: false }};</script>
<script src="vendor/paged.polyfill.js"></script>
</head>
<body class="{cls}">
<main id="out"></main>
<template id="src">
"""
TAIL = """
</template>
<script src="render.js"></script>
</body>
</html>
"""
ROMAN = {1: "one", 2: "two", 3: "three", 4: "four", 5: "five", 6: "six", 7: "seven", 8: "eight"}


def build(volume: int) -> None:
    vol = VOLUMES[volume]
    essays = [parse_essay(s) for s in vol["essays"]]
    roman = ROMAN[volume]
    theme = vol["title"]
    esc = lambda s: html.escape(s, quote=False)

    toc = "\n".join(
        f'<li><a href="#e{i+1}"><span class="toc-no">{i+1:02d}</span>'
        f'<span class="toc-title">{esc(e["title"].lower())}</span>'
        f'<span class="toc-date">{e["date"]}</span></a></li>'
        for i, e in enumerate(essays))

    parts = []
    for i, e in enumerate(essays):
        t = e["title"].lower()
        parts.append(f"""
<section class="essay" id="e{i+1}">
  <div class="essay-head">
    <p class="essay-no">{i+1:02d}</p>
    <h2 class="essay-title" data-title="{html.escape(t)}">{esc(t)}</h2>
    <p class="essay-meta">{e["date"]}<br>paulgraham.com/{e["slug"]}.html</p>
  </div>
  <div class="essay-body">
{chr(10).join(e["blocks"])}
  </div>
</section>""")

    total_words = sum(e["words"] for e in essays)

    doc = HEAD.format(title=f"paul graham {theme} · volume {roman}", cls="book-doc") + f"""
<article class="book">

<section class="title-page">
  <div class="lockup">
    <div><h1 class="lk-author" data-fit="128">paul graham</h1></div>
    <div><h2 class="lk-theme" data-fit="128">{esc(theme)}</h2></div>
    <p class="lk-volume">essays, volume {roman}</p>
  </div>
  <p class="tp-foot">printed at home, {PRINTED}</p>
</section>

<section class="colophon">
  <p>{len(essays)} essays, {total_words:,} words. all of them are at paulgraham.com, free, as they should be. this is one reader's copy, printed at home to be read away from a screen, with a pencil.</p>
  <p>made with pg-on-paper. github.com/workinprogmess/pg-on-paper</p>
</section>

<section class="contents">
  <h2>contents</h2>
  <ol class="toc">
{toc}
  </ol>
</section>
{"".join(parts)}
</article>
""" + TAIL
    (PROJECT / "book.html").write_text(doc, "utf-8")

    back_list = "\n".join(
        f'<li><span class="c-no">{i+1:02d}</span>{esc(e["title"].lower())}</li>'
        for i, e in enumerate(essays))
    cover = HEAD.format(title=f"cover · volume {roman}", cls="cover-doc") + f"""
<section class="cover front">
  <div class="lockup">
    <div><h1 class="lk-author" data-fit="156">paul graham</h1></div>
    <div><h2 class="lk-theme" data-fit="156">{esc(theme)}</h2></div>
    <p class="lk-volume">essays, volume {roman}</p>
  </div>
  <p class="cv-foot"><span>{PRINTED}</span><span>pg-on-paper</span></p>
</section>
<section class="cover back">
  <ol class="cv-list">
{back_list}
  </ol>
  <p class="cv-back-foot">{len(essays)} essays · {total_words:,} words · paulgraham.com</p>
</section>
""" + TAIL
    (PROJECT / "cover.html").write_text(cover, "utf-8")

    for e in essays:
        print(f"  {e['slug']:14s} {e['words']:6d}  {e['date']:16s} {e['title']}")
    print(f"volume {volume} · {theme}: {len(essays)} essays, {total_words:,} words")


if __name__ == "__main__":
    nums = [a for a in sys.argv[1:] if a.isdigit()]
    build(int(nums[0]) if nums else 1)
