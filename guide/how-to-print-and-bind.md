# how to print and bind

one volume = 27-48 sheets of paper (the table in `paul-graham/README.md`) + 2 sheets of
cover stock + one evening. do the 2-sheet test first, every time. it
saves the whole stack.

## what's on the table

- the volume's folder under `paul-graham/pdfs/`, say `1-on-work-thats-yours/`:
  `print-odd.pdf`, `print-even.pdf` (or `print-duplex.pdf` if your printer
  flips paper), `cover-front.pdf`, `cover-back.pdf`
- a4 80gsm paper for the inside. i use a pastel green; any tinted or
  cream 80-100gsm works. plain white is fine too, it's just less of a book
- a4 photo paper or card for the covers. i use 260gsm glossy inkjet photo
  paper; 250gsm cardstock also works and takes ink on both sides
- awl (or a thick needle pushed through a cork), a large-eye needle,
  waxed thread ~1.5m, 2 large binder clips, ruler, pencil, cutting mat
  or a thick magazine to punch into

## printing the inside: manual duplex

this is written for a printer that doesn't flip paper by itself (mine is an
epson l8050). two passes, one flip, both passes in reverse order. if yours
does duplex, print `print-duplex.pdf` two-sided, long edge, and skip to the
covers.

settings for both passes: a4, plain paper, standard quality (not photo:
inkjet dye on 80gsm at photo quality soaks and shows through), 100%, no
"fit to page".

the logic, so you can reason about it when something goes sideways: the
printer stacks sheets face-up with the last one on top, and it feeds from
the top of whatever you load. so print the odd pass in reverse and page 1
ends up on top of the pile. flip the whole pile once and page 1 is at the
bottom, the last sheet on top. so the even pass runs in reverse as well:
the highest even page prints first, onto the back of the highest odd page,
and page 2 prints last, onto the back of page 1. when it finishes, the book
is lying face-down on the tray in order.

1. **test with one sheet first.** print page 3 of `print-odd.pdf` (book
   page 5, the first numbered page). flip it as in step 3, feed it, print
   page 3 of `print-even.pdf` (book page 6). page 6 should be on the back
   of page 5, upright, "6" at the bottom left. if it's upside down, your
   printer wants a short-edge flip.
2. **odd pass, reversed.**

   ```sh
   lp -o media=A4 -o outputorder=reverse -o fit-to-page=false print-odd.pdf
   ```

   (print dialog: paper handling → reverse page order.) let it finish
   completely. page 1 is on top. the blank sheets that come out are the
   right-hand pages before each essay opener; they belong. count the
   stack: it must equal the page count of `print-odd.pdf`.
3. **the flip.** pick up the whole pile. hold it in front of you, page 1
   facing you, upright. turn it over the way you turn a page in a book,
   left edge swinging right. you now see the blank back of the last sheet;
   the top of the page is still up. don't rotate it, don't square or fan
   it. lower it into the rear feed, top edge down into the slot, the side
   facing you still facing you.
4. **even pass, reversed too.**

   ```sh
   lp -o media=A4 -o outputorder=reverse -o fit-to-page=false print-even.pdf
   ```

   if you want one more check before committing 40 sheets, print only the
   last page of `print-even.pdf` first; it should land on the back of the
   last odd page.
5. **if the printer stalls mid-pass** (the l8050 does, with a full tray):
   don't reload or cancel from the printer. note the number on the last
   sheet that came out, cancel the job on the computer, and resend from
   the next page onward, still reversed. the pile stays whole.
6. wait ten minutes before handling, half an hour before binding. dye
   ink on uncoated paper smudges when it's fresh.

## printing the cover

two sheets of photo paper or card, one for the front and one for the back.
their unprinted sides face the first and last pages of the book.

if your stock takes ink on both sides (photo paper's matte back does, a
little duller), print the insides green too: `cover-inside.pdf` is a plain
sheet of the cover colour. do the inside first, plain paper mode, standard
quality, borderless; dry it ten minutes; then the outside. that way the
glossy face is the last thing to touch the rollers.

1. `cover-front.pdf` → one sheet, glossy side up in the rear feed.
   - media type: premium glossy (or "photo paper glossy")
   - print quality: high / photo
   - borderless: on
2. same for `cover-back.pdf`.
3. dry an hour flat before touching the printed side.

the last 20mm or so of a borderless sheet prints a little soft on most
inkjets, because the sheet is leaving the rollers. the layout keeps text
above that line. if your printer is worse there, raise the cover padding in
`tool/styles.css`.

## the stack

from top: front cover (glossy out) · all inside pages in order · back cover
(glossy out). tap the stack square on the table, spine edge (left) and
bottom edge. clip it with the two binder clips on the right side, away
from the spine. slide a strip of scrap paper under each clip so it
doesn't dent the cover.

## holes

4 holes along the left edge, 14mm in from the spine.

on a4 (297mm tall), measure from the top edge:

```
hole 1:  30mm
hole 2: 109mm
hole 3: 188mm
hole 4: 267mm
```

mark them in pencil on the back cover. push the awl straight down
through the whole stack into the cutting mat. go slowly, keep it
vertical. wiggle it a little to widen each hole so the needle passes
without tearing the paper.

## sewing (four-hole japanese stab binding)

thread the needle with ~1.5m of waxed thread. single, not doubled.
"front" = cover side. "back" = back cover side. holes numbered 1 at the
top, 4 at the bottom.

```
 1.  from the back, up through hole 2. leave a 10cm tail at the back.
 2.  around the spine edge to the back, up through hole 2 again.
 3.  on the front, down to hole 3. go through 3 to the back.
 4.  around the spine to the front, through 3 to the back again.
 5.  on the back, down to hole 4. go through 4 to the front.
 6.  around the spine to the back, through 4 to the front again.
 7.  around the bottom edge to the back, through 4 to the front again.
 8.  on the front, up to hole 3. through 3 to the back.
 9.  on the back, up to hole 2. through 2 to the front.
10.  on the front, up to hole 1. through 1 to the back.
11.  around the spine to the front, through 1 to the back again.
12.  around the top edge to the front, through 1 to the back again.
13.  on the back, down to hole 2. you're next to the tail.
```

pull everything snug as you go. tie the two ends in a square knot at
the back of hole 2, trim to 5mm, push the knot into the hole with the
awl so it hides. done.

what it should look like: every hole has a loop over the spine, the top
and bottom holes also have a loop over the edge, and the thread runs
between the holes on both front and back. no gaps.

## if it goes wrong

- thread snaps: tie on a new length with a square knot at the back and
  keep going. the knot hides under a stitch.
- holes tear on the paper: the awl was too thin for the stack,
  or you wiggled too hard. next volume, widen more gently.
- the book doesn't open flat: it never will. that's stab binding. the
  32mm gutter is for this.
- cover cracks at the holes: glossy photo paper can. a dab of clear
  glue on the back of each hole before punching, dried, stops it.

## next volumes

a 100-sheet pack does two volumes. all seven need three packs. a 20-sheet
pack of photo paper does ten covers.
