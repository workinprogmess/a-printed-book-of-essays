"""parser for paulgraham.com pages.

pg's html is 2001-style: one big <font> block, paragraphs separated by
<br><br>, footnotes either as linked [1] or plain text [1]. this turns one
saved page into clean paragraphs.

every author folder has one of these. it must expose:

    parse_essay(path: Path, lowercase: bool) -> {"slug", "title", "date", "blocks", "words"}

where blocks is a list of html fragments (<p>, <h3>, <blockquote>, <pre>,
<p class="note">, <p class="thanks">) that tool/build.py lays out.
"""
from __future__ import annotations

import html
import re
from pathlib import Path


def lower_text(fragment: str) -> str:
    """lowercase the text between tags, leave the tags alone."""
    return re.sub(r">([^<]+)<", lambda m: ">" + m.group(1).lower() + "<", f">{fragment}<")[1:-1]


def balance_inline(block: str) -> str:
    """close any <i>/<b> left open inside one block; drop closes with no open."""
    for tag in ("i", "b"):
        depth = 0
        out = []
        for piece in re.split(rf"(</?{tag}>)", block):
            if piece == f"<{tag}>":
                if depth == 0:
                    out.append(piece)
                depth = 1
            elif piece == f"</{tag}>":
                if depth == 1:
                    out.append(piece)
                depth = 0
            else:
                out.append(piece)
        if depth == 1:
            # close before a trailing </p> so the paragraph stays well-formed
            joined = "".join(out)
            if joined.endswith("</p>"):
                joined = joined[:-4] + f"</{tag}></p>"
            else:
                joined += f"</{tag}>"
            block = joined
        else:
            block = "".join(out)
    return block


def parse_essay(path: Path, lowercase: bool = True) -> dict:
    """turn one saved paulgraham.com page into {title, date, blocks, words}."""
    slug = path.stem
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

    # pg's pages occasionally leave an <i> or <b> unclosed (taste for makers,
    # last footnote) or close one twice (good writing, thanks line). browsers
    # forgive that at the paragraph end; paged.js doesn't, and the italic
    # runs to the end of the book. balance every block on its own.
    blocks = [balance_inline(b) for b in blocks]

    text = re.sub(r"<[^>]+>", " ", " ".join(blocks))
    words = len(html.unescape(text).split())
    if lowercase:
        blocks = [lower_text(b) for b in blocks]
    return {"slug": slug, "title": title, "date": date, "blocks": blocks, "words": words}
