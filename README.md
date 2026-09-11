# pg on paper

paul graham's essays as small books you print and bind at home.

seven volumes, sorted by what they're about. a4, printed two-sided on
whatever paper you like, bound with needle and thread. this repo is the
tool that lays them out and the guide for putting them together. the
essays themselves are pg's; you download them from his site when you build.

![cover and title page](guide/cover.png)

## the volumes

| vol | theme | essays | sheets |
|----|----|----|----|
| one | on work that's yours | 10 | 38 |
| two | on kids and learning | 14 | 34 |
| three | on writing | 12 | 27 |
| four | on making things | 12 | 39 |
| five | on startups | 13 | 43 |
| six | on money and investors | 12 | 43 |
| seven | on society | 13 | 48 |

the full lists are in [volumes.py](volumes.py). 86 essays of his roughly
220. the lisp essays, the early hacker pieces, and the long memoirs aren't
placed yet. add your own volume if you want them.

## make one

you need python 3, node, google chrome, ghostscript, and poppler.

```sh
# mac
brew install ghostscript poppler
# debian/ubuntu
sudo apt install ghostscript poppler-utils
```

then:

```sh
npm install
python3 scripts/fetch.py 1        # downloads volume one's essays into essays/
python3 scripts/build.py 1        # lays it out
node scripts/make-pdf.mjs 1       # renders the pdfs into output/
```

`output/` now has:

- `vol1-preview.pdf` — the whole book, cover to cover, for reading on screen
- `vol1-inside-odd.pdf`, `vol1-inside-even.pdf` — the two passes for a printer that doesn't duplex
- `vol1-inside.pdf` — the same pages in one file, for a printer that does
- `vol1-cover-front.pdf`, `vol1-cover-back.pdf` — one sheet of card or photo paper each

then read [the guide](guide/how-to-print-and-bind.md). it walks through the
two-sheet duplex test, the cover, the four holes, and the sewing.

## make it yours

- **which essays**: edit [volumes.py](volumes.py). slugs are the file names on paulgraham.com. add a volume, drop an essay, reorder.
- **capitals**: everything is lowercase, pg's prose included. `LOWERCASE = False` in `scripts/build.py` keeps his capitals.
- **the cover colour**: `--cover` at the top of [styles.css](styles.css).
- **margins and type size**: the same place. the binding side gets 32mm because stab stitching eats it and the book never opens flat. the outer side gets 50mm for a pencil.
- **fonts**: charter, bodoni 72, and helvetica neue, which ship with macos. on linux or windows, see [fonts.md](fonts.md) for free fonts that sit close.

## how it's laid out

- ink only inside. the paper is the colour.
- each essay opens as a spread: title alone on the left page, text from the right.
- footnotes stay at the end of each essay, as pg has them.
- every page carries "paul graham" on the left and the essay title on the right, small.
- charter at 10pt on a 128mm measure, about 72 characters a line. it was drawn for cheap paper and low-resolution printers, which is what this is.

## on the essays

they're paul graham's, and they're free to read at [paulgraham.com](https://www.paulgraham.com/articles.html).
this repo doesn't include them and doesn't redistribute them. `fetch.py`
downloads them to your machine the way a browser does, and `essays/` and
`output/` are gitignored so they stay there. make copies for yourself,
not for sale.

## licence

the code, layout, and guide are mit. see [LICENSE](LICENSE).
