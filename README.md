# on paper

essays worth reading slowly, laid out as small books you print and bind at
home. starting with paul graham.

![cover and title page](guide/cover.png)

## why

some writing is better on paper. you read it on the floor, in the sun, on
a train, with a pencil. you underline. you argue in the margin. you finish
an essay and sit with it instead of clicking the next one. and a thing you
printed, folded, punched, and sewed yourself is a different object from a
pdf. you feel each word a little more because your hands made the page it
sits on.

this repo is that, for essays that live on the open web. pick a volume,
print it two-sided, add a cover, sew four holes. an evening's work. the
guide walks you through all of it, including the first time.

## what's here

- **[paul graham](paul-graham/)** — 86 of his essays in seven volumes, by
  theme: on work that's yours, on kids and learning, on writing, on making
  things, on startups, on money and investors, on society. [why they're
  split this way, and what each one holds](paul-graham/README.md).

more authors as they come. the structure is one folder per author; see
[adding an author](#adding-an-author).

## read it, three ways

every volume folder under `paul-graham/pdfs/` has:

| file | what for |
|----|----|
| `read.pdf` | the whole book on a screen, cover to cover, a4 |
| `ereader.pdf` | a5, one page at a time, no spreads. for a kindle, remarkable, or tablet |
| `print-odd.pdf` + `print-even.pdf` | the two passes for a printer that doesn't flip paper |
| `print-duplex.pdf` | the same pages in one file, for a printer that does |
| `cover-front.pdf`, `cover-back.pdf` | one sheet of card or photo paper each |

so:

1. **just read.** download `read.pdf` or `ereader.pdf`. done.
2. **print and bind.** download the print files and the covers, then follow
   [the guide](guide/how-to-print-and-bind.md). it covers the two-sheet
   duplex test, the paper, the holes, and the sewing, step by step.
3. **make it yours.** change which essays, the order, the cover colour, the
   type. rebuild. see [changing things](#changing-things).

## paper

what i use: a4 80gsm pastel green for the inside, 260gsm glossy inkjet
photo paper for the covers, an epson l8050 that doesn't duplex. any tinted
or cream 80-100gsm paper works for the inside. plain white is fine too, it's
just less of a book. 250gsm cardstock works for covers and takes ink on both
sides. one 100-sheet pack does two volumes.

## changing things

you need python 3, node, google chrome, ghostscript, and poppler.

```sh
brew install ghostscript poppler          # mac
sudo apt install ghostscript poppler-utils   # debian / ubuntu
npm install
```

then, from the repo root:

```sh
python3 tool/fetch.py paul-graham 3     # downloads any essay you added to the volume
python3 tool/build.py paul-graham 3     # lays out volume 3
node tool/make-pdf.mjs paul-graham 3    # renders all seven pdfs into paul-graham/pdfs/3-on-writing/
```

- **which essays, what order, how many volumes**: `paul-graham/volumes.py`. slugs are the file names on his site.
- **capitals**: everything is lowercase, his prose included. `LOWERCASE = False` in `volumes.py` keeps his.
- **the cover colour**: `--cover` at the top of `tool/styles.css`.
- **margins and type size**: the same place. the binding side gets 32mm because stab stitching eats it and the book never opens flat. the outer side gets 50mm for a pencil.
- **fonts**: charter, bodoni 72, and helvetica neue, which ship with macos. on linux or windows, [guide/fonts.md](guide/fonts.md) lists free fonts that sit close.

or don't run anything yourself. clone the repo and tell your agent (claude
code, codex, whichever) what you want. [AGENTS.md](AGENTS.md) tells it how
this repo works.

## adding an author

one folder, three things in it:

- `volumes.py` — `AUTHOR` (name, site, url pattern) and `VOLUMES`
- `parse.py` — turns one saved page from that site into clean paragraphs. `paul-graham/parse.py` is the model
- `README.md` — why the volumes are split the way they are

then `fetch`, `build`, `make-pdf` with the folder name. the layout, the cover, and the guide are shared.

## how it's laid out

- ink only inside. the paper is the colour.
- each essay opens as a spread: title alone on the left page, text from the right.
- footnotes stay at the end of each essay, where the author put them.
- every page carries the author on the left and the essay title on the right, small.
- charter at 10pt on a 128mm measure, about 72 characters a line. it was drawn for cheap paper and low-resolution printers, which is what this is.
- the cover is a deep green, the author in bodoni over the theme in a light sans, both the same width.

## on the essays

they're their authors'. paul graham's are free to read at
[paulgraham.com](https://www.paulgraham.com/articles.html) and they're here
so you can print them for yourself. read them, bind them, give a copy to a
friend. don't sell them.

## licence

the tool, the layout, and the guide are mit. see [LICENSE](LICENSE).
