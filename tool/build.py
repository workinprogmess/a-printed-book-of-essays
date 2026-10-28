"""lay out one volume as book.html + cover.html (+ book-ereader.html).

usage: python3 tool/build.py <author-folder> <volume-number>
       python3 tool/build.py paul-graham 3

reads <author>/volumes.py for the lists and <author>/parse.py for how to
read that author's pages. writes into <author>/.build/.
"""
from __future__ import annotations

import datetime
import html
import importlib.util
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TOOL = ROOT / "tool"
PRINTED = datetime.date.today().strftime("%B %Y").lower()
ROMAN = {1: "one", 2: "two", 3: "three", 4: "four", 5: "five", 6: "six", 7: "seven", 8: "eight", 9: "nine", 10: "ten"}


def load(author_dir: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, author_dir / f"{name}.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def slugify(s: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", s.lower().replace("'", "")).strip("-")


HEAD = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>{title}</title>
<link rel="stylesheet" href="{styles}">
<script>window.PagedConfig = {{ auto: false }};</script>
<script src="../../tool/vendor/paged.polyfill.js"></script>
</head>
<body class="{cls}" data-styles="{styles}">
<main id="out"></main>
<template id="src">
"""
TAIL = """
</template>
<script src="../../tool/render.js"></script>
</body>
</html>
"""
def build(author: str, volume: int) -> Path:
    author_dir = ROOT / author
    cfg = load(author_dir, "volumes")
    parser = load(author_dir, "parse")
    vol = cfg.VOLUMES[volume]
    lowercase = getattr(cfg, "LOWERCASE", True)
    author_name = cfg.AUTHOR["name"]
    essays = []
    for slug in vol["essays"]:
        path = author_dir / "essays" / f"{slug}.html"
        if not path.exists():
            sys.exit(f"{author}/essays/{slug}.html is missing. run: python3 tool/fetch.py {author} {volume}")
        essays.append(parser.parse_essay(path, lowercase))
    roman = ROMAN[volume]
    theme = vol["title"]
    out = author_dir / ".build"
    out.mkdir(exist_ok=True)
    esc = lambda s: html.escape(s, quote=False)
    site = cfg.AUTHOR["site"]

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
    <p class="essay-meta">{e["date"]}<br>{site}/{e["slug"]}.html</p>
  </div>
  <div class="essay-body">
{chr(10).join(e["blocks"])}
  </div>
</section>""")

    total_words = sum(e["words"] for e in essays)

    body = f"""
<article class="book">

<section class="title-page">
  <p class="tp-author">{esc(author_name)}</p>
  <hr>
  <h1 class="tp-title">{esc(theme)}</h1>
  <hr>
  <p class="tp-volume">essays, volume {roman}</p>
  <p class="tp-foot">printed at home, {PRINTED}</p>
</section>

<section class="colophon">
  <p>{len(essays)} essays, {total_words:,} words. all of them are at {site}, free, as they should be. this is one reader's copy, printed at home to be read away from a screen, with a pencil.</p>
  <p>a printed book of essays<br>github.com/workinprogmess/a-printed-book-of-essays</p>
</section>

<section class="contents">
  <h2>contents</h2>
  <ol class="toc">
{toc}
  </ol>
</section>
{"".join(parts)}
</article>
"""
    title = f"{author_name} {theme} · volume {roman}"
    # paged.js resolves break/page rules against the content fragment before it is
    # attached to the page, so the edition class has to sit on the article, not <body>.
    (out / "book.html").write_text(HEAD.format(title=title, cls="book-doc", styles="../../tool/styles.css")
                                   + body.replace('<article class="book">', '<article class="book print">', 1) + TAIL, "utf-8")
    (out / "book-ereader.html").write_text(HEAD.format(title=title, cls="book-doc", styles="../../tool/styles.css,../../tool/ereader.css")
                                           + body.replace('<article class="book">', '<article class="book ereader">', 1) + TAIL, "utf-8")

    back_list = "\n".join(
        f'<li><span class="c-no">{i+1:02d}</span>{esc(e["title"].lower())}</li>'
        for i, e in enumerate(essays))
    cover = HEAD.format(title=f"cover · volume {roman}", cls="cover-doc", styles="../../tool/styles.css") + f"""
<section class="cover front"><div class="fr">
  <p class="cv-author">{esc(author_name)}</p>
  <hr>
  <h1 class="cv-title">{esc(theme)}</h1>
  <hr>
  <p class="cv-volume">essays, volume {roman}</p>
  <p class="cv-foot"><span>{PRINTED}</span><span>a printed book of essays</span></p>
</div></section>
<section class="cover back"><div class="fr">
  <ol class="cv-list">
{back_list}
  </ol>
  <p class="cv-back-foot">{len(essays)} essays · {total_words:,} words · {site}</p>
</div></section>
""" + TAIL
    (out / "cover.html").write_text(cover, "utf-8")
    (out / "name.txt").write_text(f"{volume}-{slugify(theme)}", "utf-8")

    for e in essays:
        print(f"  {e['slug']:14s} {e['words']:6d}  {e['date']:16s} {e['title']}")
    print(f"{author} · volume {volume} · {theme}: {len(essays)} essays, {total_words:,} words")
    return out




if __name__ == "__main__":
    if len(sys.argv) < 3:
        sys.exit("usage: python3 tool/build.py <author-folder> <volume-number>")
    build(sys.argv[1], int(sys.argv[2]))
