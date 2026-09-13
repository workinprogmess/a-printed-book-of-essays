"""download an author's essays into <author>/essays/.

the repo already carries the essays for the volumes it ships. you only need
this when you add an essay to volumes.py, or add a new author.

usage: python3 tool/fetch.py paul-graham            # everything in volumes.py
       python3 tool/fetch.py paul-graham 3          # one volume
       python3 tool/fetch.py paul-graham --force    # re-download
"""
from __future__ import annotations

import shutil
import subprocess
import sys
import time
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if len(sys.argv) < 2:
    sys.exit("usage: python3 tool/fetch.py <author-folder> [volume] [--force]")
AUTHOR_DIR = ROOT / sys.argv[1]
sys.path.insert(0, str(AUTHOR_DIR))
from volumes import AUTHOR, VOLUMES  # noqa: E402

ESSAYS = AUTHOR_DIR / "essays"
ESSAYS.mkdir(exist_ok=True)

args = sys.argv[2:]
force = "--force" in args
nums = [int(a) for a in args if a.isdigit()]
wanted = [s for n in (nums or VOLUMES) for s in VOLUMES[n]["essays"]]

def download(url: str) -> bytes | None:
    """urllib first; curl as a fallback for python installs without ssl certs."""
    req = urllib.request.Request(url, headers={"User-Agent": "on-paper (personal print edition)"})
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
    url = AUTHOR["url"].format(slug=slug)
    data = download(url)
    if not data or b"<html" not in data[:200].lower():
        print(f"  {slug:16s} FAILED  (check the slug at {url})")
        continue
    target.write_bytes(data)
    print(f"  {slug:16s} {len(data):7d} bytes")
    time.sleep(0.5)  # be polite to his server
print(f"{len(seen)} essays in {AUTHOR_DIR.name}/essays/")
