# how to print and bind

one volume = 27-48 sheets of paper (see the readme table) + 2 sheets of
cover stock + one evening. do the 2-sheet test first, every time. it
saves the whole stack.

## what's on the table

- `output/vol1-inside-odd.pdf` and `-even.pdf`
- `output/vol1-cover-front.pdf`, `output/vol1-cover-back.pdf`
- a4 80gsm paper for the inside. i use a pastel green; any tinted or
  cream 80-100gsm works. plain white is fine too, it's just less of a book
- a4 photo paper or card for the covers. i use 260gsm glossy inkjet photo
  paper; 250gsm cardstock also works and takes ink on both sides
- awl (or a thick needle pushed through a cork), a large-eye needle,
  waxed thread ~1.5m, 2 large binder clips, ruler, pencil, cutting mat
  or a thick magazine to punch into

## printing the inside: manual duplex

this is written for a printer that doesn't flip paper by itself (mine is an
epson l8050). two passes. if yours does duplex, print `vol1-inside.pdf`
two-sided, long edge, and skip to the covers.

1. open `vol1-inside-odd.pdf` in preview. file → print.
   - paper size: a4
   - media type: plain paper
   - print quality: standard (not photo. inkjet dye on 80gsm at photo
     quality soaks and shows through)
   - scale: 100%, no "fit to page"
2. **test first.** print pages 1-2 of the odd file only (that's book
   pages 1 and 3). two sheets come out face up, the later one on top.
3. take those two sheets. flip the stack like turning a page in a book
   (over the long edge). the top of the page stays at the top. printed
   side is now down, sheet with page 1 is on top.
4. load them in the rear feed. print pages 1-2 of `vol1-inside-even.pdf`
   (book pages 2 and 4).
5. check: page 2 should be on the back of page 1, same way up, page
   numbers at the outer bottom corners. if page 2 is upside down, next
   time flip over the short edge instead. if page 2 landed on the back
   of page 3, next time reverse the order (preview: paper handling →
   reverse page order) on the even pass.
6. once the test is right, print all of odd. wait for the stack to dry
   ten minutes. flip the whole stack the way that worked. print all of
   even. don't top up paper mid-pass.
7. let it sit half an hour before binding. dye ink on uncoated paper
   smudges when it's fresh.

## printing the cover

1. `vol1-cover-front.pdf` → print on one sheet of the photo paper,
   glossy side up in the rear feed.
   - media type: premium glossy (or "photo paper glossy")
   - print quality: high / photo
   - borderless: on
2. same for `vol1-cover-back.pdf`.
3. the back of photo paper is bare white and won't take ink. that's the
   inside of the cover. fine. (cardstock takes ink on both sides if you'd
   rather print the inside too.)
4. dry an hour flat before touching the printed side.

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
