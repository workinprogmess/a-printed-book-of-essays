# for agents

you're in `a-printed-book-of-essays`: essays from the open web laid out as printable,
bindable a4 books, one folder per author. a person will usually ask you one
of five things. here is how each one goes.

## "print me paul graham volume 3" / "i want the pdfs"

nothing to build. the pdfs are committed.

- `paul-graham/pdfs/3-on-writing/print-odd.pdf` and `print-even.pdf` for a printer that doesn't duplex, or `print-duplex.pdf` for one that does
- `cover-front.pdf` and `cover-back.pdf` on card or photo paper; `cover-inside.pdf` is a plain sheet of the cover colour for their backs
- `read.pdf` for a screen, `ereader.pdf` for a kindle or tablet

point them at `guide/how-to-print-and-bind.md`. if they're about to print,
the one thing to insist on is the two-sheet duplex test in that guide before
the whole stack.

## "swap an essay" / "add an essay" / "reorder"

1. edit `paul-graham/volumes.py`. slugs are the file names on paulgraham.com (`https://www.paulgraham.com/<slug>.html`).
2. `python3 tool/fetch.py paul-graham <vol>` downloads anything new into `paul-graham/essays/`.
3. `python3 tool/build.py paul-graham <vol>` then `node tool/make-pdf.mjs paul-graham <vol>`.
4. check `paul-graham/pdfs/<n>-<theme>/read.pdf`. rasterise a few pages (`pdftoppm -r 40 -png`) and look at them; the parser is regex over 2001-era html and a new essay can surprise it.
5. update the volume table in `paul-graham/README.md` if the sheet count changed.

## "change the cover colour / margins / type"

`tool/styles.css`. the variables at the top: `--cover`, `--gutter`, `--outer`,
`--body-size`, `--text`, `--display`. rebuild every volume you want changed
(build + make-pdf per volume). the e-reader edition is `tool/ereader.css`,
loaded after `styles.css`.

## "add another author"

make `<author>/` with:

- `volumes.py` — `AUTHOR = {"name", "site", "url"}` (url has `{slug}` in it), `VOLUMES = {1: {"title", "essays": [slugs]}}`, optional `LOWERCASE`.
- `parse.py` — `parse_essay(path, lowercase) -> {"slug", "title", "date", "blocks", "words"}`. `blocks` is a list of html fragments: `<p>`, `<h3>`, `<blockquote>`, `<pre>`, `<p class="note">`, `<p class="thanks">`. footnote refs are `<sup class="fn">n</sup>`. start from `paul-graham/parse.py` and change what the new site's html needs.
- `README.md` — why the volumes are split that way and what each holds.

then fetch, build, make-pdf with the new folder name. the layout, covers,
and guide are shared and need nothing.

## "it won't build"

- `no chrome found`: install google chrome or set `CHROME_PATH`.
- `gs` or `pdfinfo` missing: `brew install ghostscript poppler` or `apt install ghostscript poppler-utils`.
- `<author>/essays/<slug>.html is missing`: run `tool/fetch.py`.
- fetch fails with an ssl error: the script falls back to curl on its own. if curl is also missing, download the page by hand into `essays/`.
- chrome produced more pages than expected: paged.js and chrome disagree about a blank sheet. `make-pdf.mjs` handles the known case; if it warns, open the raw pdf and look.

## conventions

- everything lowercase in this repo: docs, commits, the books themselves.
- pdfs are committed. after any rebuild, commit the changed pdfs with the change that caused them.
- don't commit `*/.build/` (intermediate html) or `node_modules/`.
- the essays are their authors'. keep the licence note in `README.md` and `LICENSE` intact.
