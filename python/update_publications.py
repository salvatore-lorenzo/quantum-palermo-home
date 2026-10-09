"""Update the publication pages from the arxiv-bot posts on Discord, in one go.

Runs, in order:
  1. newpapers.py        save the latest arxiv-bot messages
  2. newbibs.py          turn them into .bib files in python/
  3. newpublications.py  create the pages in content/publication/ and move the .bib files to bibtexs/
Stops at the first script that fails.
"""

import subprocess
import sys
from pathlib import Path

SCRIPTS = ["newpapers.py", "newbibs.py", "newpublications.py"]
HERE = Path(__file__).resolve().parent


def main():
  for script in SCRIPTS:
    print(f"\n===== {script} =====", flush=True)
    result = subprocess.run([sys.executable, str(HERE / script)])
    if result.returncode != 0:
      sys.exit(f"{script} failed (exit code {result.returncode}): stopping here")
  print("\nall done")


if __name__ == "__main__":
  main()
