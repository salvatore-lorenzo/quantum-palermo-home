"""Create a page in content/publication/ for each .bib file made by newbibs.py.

Runs `academic import <file> content/publication/ --compact` on every .bib file
in python/, which writes content/publication/<citation key>/index.md and
cite.bib. Existing pages are left untouched, except that the published version
of a paper (@article, @inproceedings, ...) replaces the page of its arXiv
preprint (@misc with the same arXiv id). Every new page keeps a link to arXiv.
Once a .bib file is imported (or its paper is already on the site), it is moved
from python/ to bibtexs/.
"""

import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

NEW_BIB_DIR = Path(__file__).resolve().parent
BIBTEX_DIR = NEW_BIB_DIR.parent / "bibtexs"
PUBLICATION_DIR = NEW_BIB_DIR.parent / "content" / "publication"


def bib_field(text, name):
  match = re.search(rf"\b{name}\s*=\s*\{{([^}}]*)\}}", text, re.IGNORECASE)
  return match.group(1).strip() if match else None


def is_preprint(bib_text):
  return bib_text.lstrip().lower().startswith("@misc")


def page_names():
  return {p.name for p in PUBLICATION_DIR.iterdir() if p.is_dir()}


def pages_mentioning(*ids):
  # Pages whose cite.bib contains one of the given arXiv ids or DOIs
  patterns = [re.compile(rf"(?<![\d.]){re.escape(i)}(?!\d)", re.IGNORECASE) for i in ids if i]
  found = []
  for page in sorted(PUBLICATION_DIR.iterdir()):
    cite = page / "cite.bib"
    if cite.is_file():
      text = cite.read_text(encoding="utf-8", errors="replace")
      if any(p.search(text) for p in patterns):
        found.append((page, text))
  return found


def run_academic(bib):
  # Returns the names of the pages created, or None if academic failed
  before = page_names()
  try:
    result = subprocess.run(["academic", "import", str(bib), f"{PUBLICATION_DIR}/", "--compact"])
  except FileNotFoundError:
    sys.exit("the `academic` command was not found (pip install academic)")
  if result.returncode != 0:
    return None
  return sorted(page_names() - before)


def ensure_arxiv_link(page, arxiv_id):
  # academic adds the arXiv link from the eprint field; add it by hand if it is missing
  index = page / "index.md"
  text = index.read_text(encoding="utf-8")
  if f"arxiv.org/abs/{arxiv_id}" in text:
    return
  link = f"- name: arXiv\n  url: https://arxiv.org/abs/{arxiv_id}\n"
  if "\nlinks:\n" in text:
    text = text.replace("\nlinks:\n", "\nlinks:\n" + link, 1)
  else:
    end = text.index("\n---", 3) + 1  # closing line of the front matter
    text = text[:end] + "links:\n" + link + text[end:]
  index.write_text(text, encoding="utf-8")


def move_to_bibtexs(bib):
  target = BIBTEX_DIR / bib.name
  if target.exists():
    print(f"      kept python/{bib.name}: bibtexs/{bib.name} already exists")
    return
  shutil.move(bib, target)
  print(f"      moved python/{bib.name} to bibtexs/")


def main():
  bib_files = sorted(NEW_BIB_DIR.glob("*.bib"))
  if not bib_files:
    print("no .bib files in python/: run newbibs.py first")
    return

  for bib in bib_files:
    text = bib.read_text(encoding="utf-8")
    arxiv_id, doi = bib_field(text, "eprint"), bib_field(text, "doi")
    matches = pages_mentioning(arxiv_id, doi)

    if is_preprint(text) and matches:
      print(f"skip  python/{bib.name}: already on the site as content/publication/{matches[0][0].name}/")
      move_to_bibtexs(bib)
      continue
    published = [page for page, cite in matches if not is_preprint(cite)]
    if published:
      print(f"skip  python/{bib.name}: published version already on the site as content/publication/{published[0].name}/")
      move_to_bibtexs(bib)
      continue

    # Preprint pages of this paper: moved aside, then deleted if the import works, restored otherwise
    old_pages = [page for page, _ in matches]
    with tempfile.TemporaryDirectory() as tmp:
      for page in old_pages:
        shutil.move(page, Path(tmp) / page.name)
      created = run_academic(bib)
      if not created:
        for page in old_pages:
          shutil.move(Path(tmp) / page.name, page)
        if created is None:
          print(f"error python/{bib.name}: academic failed, nothing changed")
        else:
          print(f"skip  python/{bib.name}: a page with the same name already exists in content/publication/")
        continue

    for name in created:
      if arxiv_id:
        ensure_arxiv_link(PUBLICATION_DIR / name, arxiv_id)
      print(f"wrote content/publication/{name}/index.md  (from python/{bib.name})")
    for page in old_pages:
      print(f"      replaced the preprint page content/publication/{page.name}/")
    move_to_bibtexs(bib)


if __name__ == "__main__":
  main()
