"""which essays go in which volume, in reading order.

slugs are the file names on paulgraham.com: https://www.paulgraham.com/<slug>.html
edit freely. add a volume, drop an essay, reorder. then:

    python3 scripts/fetch.py        # downloads anything new into essays/
    python3 scripts/build.py 3      # lays out volume 3
    node scripts/make-pdf.mjs 3     # renders the print files
"""

VOLUMES = {
    1: {
        "title": "on work that's yours",
        "essays": ["own", "genius", "think", "lesson", "hwh", "persistence",
                   "do", "when", "vb", "greatwork"],
    },
    2: {
        "title": "on kids and learning",
        "essays": ["kids", "lies", "hs", "early", "noob", "read", "smart",
                   "copy", "island", "top", "procrastination", "disagree",
                   "identity", "makersschedule"],
    },
    3: {
        "title": "on writing",
        "essays": ["writing44", "simply", "talk", "writes", "words", "useful",
                   "goodwriting", "best", "field", "essay", "want", "getideas"],
    },
    4: {
        "title": "on making things",
        "essays": ["taste", "hp", "desres", "newthings", "artistsship", "hw",
                   "newideas", "heresy", "users", "superlinear", "goodart",
                   "love"],
    },
    5: {
        "title": "on startups",
        "essays": ["startupideas", "organic", "schlep", "ambitious", "ds",
                   "growth", "before", "13sentences", "reddits", "google",
                   "foundermode", "prepare", "earn"],
    },
    6: {
        "title": "on money and investors",
        "essays": ["wealth", "richnow", "ace", "ramenprofitable", "aord",
                   "pinch", "equity", "herd", "hiresfund", "convince", "fr",
                   "donate"],
    },
    7: {
        "title": "on society",
        "essays": ["say", "inequality", "ineq", "wtax", "winc", "re", "cities",
                   "conformism", "orth", "mod", "fh", "woke", "brandage"],
    },
}
