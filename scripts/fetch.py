"""download the essays for every volume from paulgraham.com into essays/.

the essays are paul graham's. this repo does not include them. you fetch
them yourself, the same way a browser does, and they stay on your machine
(essays/ is gitignored).

usage: python3 scripts/fetch.py            # everything in volumes.py
       python3 scripts/fetch.py 3          # one volume
       python3 scripts/fetch.py --force    # re-download
"""
from __future__ import annotations

import shutil
import subprocess
import sys
import time
import urllib.request
from pathlib import Path

PROJECT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT))
from volumes import VOLUMES  # noqa: E402

ESSAYS = PROJECT / "essays"
ESSAYS.mkdir(exist_ok=True)

args = sys.argv[1:]
force = "--force" in args
nums = [int(a) for a in args if a.isdigit()]
wanted = [s for n in (nums or VOLUMES) for s in VOLUMES[n]["essays"]]

def download(url: str) -> bytes | None:
    """urllib first; curl as a fallback for python installs without ssl certs."""
    req = urllib.request.Request(url, headers={"User-Agent": "pg-on-paper (personal print edition)"})
    try:
        return urllib.request.urlopen(req, timeout=30).read()
    except Exception:  # noqa: BLE001
        if shutil.which("curl"):
            r = subprocess.run(["curl", "-sL", "--max-time", "30", url], capture_output=True)
            if r.returncode == 0:
                return r.stdout
        return None


seen = set()
for slug in wanted:
    if slug in seen:
        continue
    seen.add(slug)
    target = ESSAYS / f"{slug}.html"
    if target.exists() and not force:
        print(f"  {slug:16s} already here")
        continue
    url = f"https://www.paulgraham.com/{slug}.html"
    data = download(url)
    if not data or b"<html" not in data[:200].lower():
        print(f"  {slug:16s} FAILED  (check the slug at {url})")
        continue
    target.write_bytes(data)
    print(f"  {slug:16s} {len(data):7d} bytes")
    time.sleep(0.5)  # be polite to his server
print(f"{len(seen)} essays in essays/")
