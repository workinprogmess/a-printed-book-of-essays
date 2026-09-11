# fonts

the layout uses three typefaces that ship with macos. if you're on linux or
windows, or just want different ones, the fallback stacks in
[styles.css](styles.css) already list free fonts that sit close. install
them and the build picks them up.

| role | mac font | free fallback | where |
|----|----|----|----|
| body text | charter | bitstream charter | free from bitstream; [practicaltypography.com/charter.html](https://practicaltypography.com/charter.html) |
| body text, alt | | source serif 4 | [google fonts](https://fonts.google.com/specimen/Source+Serif+4) |
| titles, author line | bodoni 72 | bodoni moda | [google fonts](https://fonts.google.com/specimen/Bodoni+Moda) |
| titles, alt | | libre bodoni | [google fonts](https://fonts.google.com/specimen/Libre+Bodoni) |
| theme line on the cover | helvetica neue light | inter (light) | [google fonts](https://fonts.google.com/specimen/Inter) |

to use something else entirely, change `--text`, `--display`, and the
`.lk-theme` font-family in `styles.css`. two things to keep: the body face
should be sturdy at 10pt on uncoated paper, and the title face should have
a real lowercase, because everything is set in it.
