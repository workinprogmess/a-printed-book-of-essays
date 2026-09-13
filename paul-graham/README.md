# paul graham, on paper

86 of his essays in seven volumes. all of them are free at
[paulgraham.com](https://www.paulgraham.com/articles.html). these are the
ones that read best away from a screen, sorted by what they're about so you
can pick up one book for one mood.

## the volumes

| vol | theme | essays | words | a4 sheets |
|----|----|----|----|----|
| one | [on work that's yours](pdfs/1-on-work-thats-yours/) | 10 | 34.5k | 38 |
| two | [on kids and learning](pdfs/2-on-kids-and-learning/) | 14 | 24.7k | 34 |
| three | [on writing](pdfs/3-on-writing/) | 12 | 18.2k | 27 |
| four | [on making things](pdfs/4-on-making-things/) | 12 | 33.6k | 39 |
| five | [on startups](pdfs/5-on-startups/) | 13 | 38.9k | 43 |
| six | [on money and investors](pdfs/6-on-money-and-investors/) | 12 | 37.6k | 43 |
| seven | [on society](pdfs/7-on-society/) | 13 | 42.1k | 48 |

each folder has `read.pdf`, `ereader.pdf`, the print passes, and the two
covers. see [the root readme](../README.md#read-it-three-ways).

## why split this way

pg writes about a handful of things over and over, from different angles
and decades apart. reading by theme lets the essays talk to each other: the
2004 one and the 2024 one on the same question, side by side. and a
40-sheet book is what one evening of printing and binding produces, so
seven small books instead of one fat one.

the order inside a volume is deliberate. shorter, more direct essays first,
so you're in before the long one arrives. the long one closes.

## what each volume holds

**one · on work that's yours.** the difference between work you're told to
do and work you choose, and why the second kind is where anything good comes
from. starts with a project of one's own and ends with how to do great work,
the longest and the sum of all the rest.

a project of one's own · the bus ticket theory of genius · how to think for
yourself · the lesson to unlearn · how to work hard · the right kind of
stubborn · what to do · when to do what you love · life is short · how to do
great work

**two · on kids and learning.** what school does and doesn't do, what he
tells his own kids, what he wishes he'd been told, and how to learn anything
as an adult. the four at the end are habits of mind that carry over.

having kids · lies we tell kids · what you'll wish you'd known · early work ·
being a noob · the need to read · beyond smart · copy what you like · the
island test · the top idea in your mind · good and bad procrastination · how
to disagree · keep your identity small · maker's schedule, manager's
schedule

**three · on writing.** the shortest volume. how he writes, why simply,
and what an essay is for. read it in one sitting, then write something.

writing, briefly · write simply · write like you talk · writes and write-nots
· putting ideas into words · how to write usefully · good writing · the best
essay · the shape of the essay field · the age of the essay · what you (want
to) want · how to get new ideas

**four · on making things.** taste, design, research, and the difference
between them. what makers owe their users. why new ideas look wrong at
first. how to do what you love closes it, because that's the question under
all of it.

taste for makers · hackers and painters · design and research · six
principles for making new things · the other half of "artists ship" · the
hardware renaissance · crazy new ideas · heresy · what i've learned from
users · superlinear returns · how art can be good · how to do what you love

**five · on startups.** the ones a founder would actually reread. ideas,
growth, doing things that don't scale, then the newest: founder mode, how
universities should prepare founders, how to earn a billion dollars.

how to get startup ideas · organic startup ideas · schlep blindness ·
frighteningly ambitious startup ideas · do things that don't scale · startup
= growth · before the startup · startups in 13 sentences · the reddits · how
to start google · founder mode · how universities should prepare founders ·
how to earn a billion dollars

**six · on money and investors.** how wealth is made, how people get rich
now, and then the practical half: staying alive, the equity equation,
reading investors, raising money. donate unrestricted closes it, which is
where the money is supposed to go.

how to make wealth · how people get rich now · billionaires build · ramen
profitable · default alive or default dead? · the fatal pinch · the equity
equation · investor herd dynamics · high resolution fundraising · how to
convince investors · how to raise money · donate unrestricted

**seven · on society.** the arguments. what you can't say opens it, then
inequality from three angles, the refragmentation, cities, conformism, and
the two long recent ones on wokeness and brands. the volume most likely to
get a pencil.

what you can't say · inequality and risk · economic inequality · modeling a
wealth tax · how to convert between wealth and income tax · the
refragmentation · cities and ambition · the four quadrants of conformism ·
orthodox privilege · the two kinds of moderate · haters · the origins of
wokeness · the brand age

## not placed

about 130 essays aren't in these seven. the lisp and programming-language
essays, the early hacker pieces (great hackers, why nerds are unpopular,
mind the gap), the long memoirs (what i worked on, how to start a startup, a
student's guide to startups), the older investor guides, and one-offs. add a
volume in [volumes.py](volumes.py) if you want them; the tool doesn't care
how many there are.

## files

- [volumes.py](volumes.py) — the lists. edit this.
- [parse.py](parse.py) — reads his html. you shouldn't need to touch it.
- `essays/` — his pages as fetched, so the build is reproducible.
- `pdfs/` — the output, one folder per volume.
