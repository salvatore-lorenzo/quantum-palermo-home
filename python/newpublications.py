"""Add a record to data/publications/ for each .bib file made by newbibs.py.

Each .bib file in python/ becomes data/publications/<id>.yaml (the id comes from
the citation key, e.g. lomonaco2026whocansample -> lomonaco-2026-whocansample).
Existing records are left untouched, except that the published version of a
paper (@article, @inproceedings, ...) replaces the record of its arXiv preprint
(@misc with the same arXiv id): the old address of the preprint then redirects
to the published paper. Research lines are suggested from the keywords listed in
data/research/: check them in the new files.
Once a .bib file is added (or its paper is already on the site), it is moved
from python/ to bibtexs/.
"""

import re
import shutil
import sys
from pathlib import Path

import sitedb

NEW_BIB_DIR = Path(__file__).resolve().parent
BIBTEX_DIR = NEW_BIB_DIR.parent / "bibtexs"

TYPES = {"article": "article", "misc": "preprint", "unpublished": "preprint", "inproceedings": "proceedings",
         "conference": "proceedings", "incollection": "chapter", "inbook": "chapter", "book": "book",
         "phdthesis": "thesis", "mastersthesis": "thesis"}
MONTHS = {m: i for i, m in enumerate(["jan", "feb", "mar", "apr", "may", "jun", "jul", "aug", "sep", "oct",
                                      "nov", "dec"], 1)}
ACCENTS = {"'": "́", "`": "̀", "^": "̂", '"': "̈", "~": "̃", "=": "̄",
           ".": "̇", "c": "̧", "v": "̌", "u": "̆", "H": "̋", "k": "̨"}


# ---------------------------------------------------------------- BibTeX

def _braced(text, i):
  # Value of the {...} group starting at text[i], and the index after it
  depth = 0
  for j in range(i, len(text)):
    depth += {"{": 1, "}": -1}.get(text[j], 0)
    if depth == 0:
      return text[i + 1:j], j + 1
  raise ValueError("unbalanced braces")


def parse_bib(text):
  """[(entry type, citation key, {field: value}, entry text)] of a .bib file."""
  entries = []
  for match in re.finditer(r"@(\w+)\s*\{\s*([^,\s]+)\s*,", text):
    kind, key = match.group(1).lower(), match.group(2)
    if kind in ("comment", "string", "preamble"):
      continue
    _, end = _braced(text, text.index("{", match.start()))
    fields, i = {}, match.end()
    field = re.compile(r"\s*([A-Za-z][\w-]*)\s*=\s*")
    while True:
      found = field.match(text, i, end)
      if not found:
        break
      name, j = found.group(1).lower(), found.end()
      if text[j] == "{":
        value, j = _braced(text, j)
      elif text[j] == '"':
        k = text.index('"', j + 1)
        value, j = text[j + 1:k], k + 1
      else:
        bare = re.compile(r"[^,}\s]+").match(text, j)
        value, j = bare.group(0), bare.end()
      fields[name] = " ".join(value.split())
      comma = re.compile(r"\s*,").match(text, j)
      if not comma:
        break
      i = comma.end()
    entries.append((kind, key, fields, text[match.start():end].strip()))
  return entries


def latex_to_text(text):
  # {\"o} or \"{o} or \"o -> ö; braces outside $...$ are removed
  def accent(m):
    import unicodedata
    return unicodedata.normalize("NFC", m.group(2) + ACCENTS[m.group(1)])
  parts = text.split("$")
  for n in range(0, len(parts), 2):  # outside maths
    part = re.sub(r"\{?\\([\'`^\"~=.])\{?(\w)\}?\}?", accent, parts[n])
    part = re.sub(r"\{?\\([cvuHk])\{(\w)\}\}?", accent, part)
    part = part.replace(r"\&", "&").replace(r"\%", "%").replace("---", "—").replace("--", "–")
    parts[n] = part.replace("{", "").replace("}", "")
  return " ".join("$".join(parts).split())


def bib_authors(value):
  # "Lo Monaco, Gabriele and Lorenzo, Salvatore" -> ["Gabriele Lo Monaco", "Salvatore Lorenzo"]
  names = []
  for author in re.split(r"\s+and\s+", value):
    author = latex_to_text(author)
    if "," in author:
      family, given = [p.strip() for p in author.split(",", 1)]
      author = f"{given} {family}".strip()
    if author and author.lower() != "others":
      names.append(author)
  return names


def bib_date(fields):
  year = re.search(r"\d{4}", fields.get("year", ""))
  if not year:
    return None
  month = fields.get("month", "").strip().lower()
  month = int(month) if month.isdigit() else MONTHS.get(month[:3], 1)
  return f"{year.group(0)}-{month:02d}-01"


def record_from_bib(kind, fields, entry, research):
  title = latex_to_text(fields.get("title", ""))
  abstract = latex_to_text(fields.get("abstract", ""))
  doi = re.sub(r"^https?://(dx\.)?doi\.org/", "", fields.get("doi", ""))
  return {
    "title": title,
    "authors": bib_authors(fields.get("author", "")),
    "date": bib_date(fields),
    "type": TYPES.get(kind, "other"),
    "journal": latex_to_text(fields.get("journal") or fields.get("booktitle") or ""),
    "volume": fields.get("volume", ""),
    "issue": fields.get("number") or fields.get("issue", ""),
    "pages": fields.get("pages", "").replace("--", "-"),
    "doi": doi,
    "arxiv": re.sub(r"v\d+$", "", fields.get("eprint", "")),
    "url": fields.get("url", ""),
    "research": sitedb.suggest_research(title, abstract, research),
    "abstract": abstract,
    "bibtex": sitedb.drop_bib_field(entry, "abstract"),
  }


# ---------------------------------------------------------------- the database

def new_id(key):
  # Citation key -> record id, the way the old site named its pages: artini2025coherent -> artini-2025-coherent
  base = sitedb.slugify(re.sub(r"(\d+)", r"-\1-", key))
  for suffix in [""] + [f"-{c}" for c in "bcdefghijklmnopqrstuvwxyz"]:
    if not sitedb.record_path("publications", base + suffix).exists():
      return base + suffix
  raise FileExistsError(f"too many records named {base}")


def records_mentioning(arxiv_id, doi):
  # (id, fields) of the records with this arXiv id or DOI
  found = []
  for rid, fields in sitedb.records("publications").items():
    if (arxiv_id and fields.get("arxiv", "").lower() == arxiv_id.lower()) or \
       (doi and fields.get("doi", "").lower() == doi.lower()):
      found.append((rid, fields))
  return found


def move_to_bibtexs(bib):
  target = BIBTEX_DIR / bib.name
  if target.exists():
    print(f"      kept python/{bib.name}: bibtexs/{bib.name} already exists")
    return
  shutil.move(str(bib), str(target))
  print(f"      moved python/{bib.name} to bibtexs/")


def main():
  bib_files = sorted(NEW_BIB_DIR.glob("*.bib"))
  if not bib_files:
    print("no .bib files in python/: run newbibs.py first")
    return
  research = sitedb.records("research")

  for bib in bib_files:
    try:
      entries = parse_bib(bib.read_text(encoding="utf-8"))
    except ValueError as error:
      print(f"error python/{bib.name}: {error}, nothing changed")
      continue
    if len(entries) != 1:
      print(f"error python/{bib.name}: expected one entry, found {len(entries)}: nothing changed")
      continue
    kind, key, fields, entry = entries[0]
    record = record_from_bib(kind, fields, entry, research)
    if not (record["title"] and record["authors"] and record["date"]):
      print(f"error python/{bib.name}: title, author or year missing: nothing changed")
      continue

    matches = records_mentioning(record["arxiv"], record["doi"])
    if record["type"] == "preprint" and matches:
      print(f"skip  python/{bib.name}: already on the site as data/publications/{matches[0][0]}.yaml")
      move_to_bibtexs(bib)
      continue
    published = [rid for rid, f in matches if f.get("type") != "preprint"]
    if published:
      print(f"skip  python/{bib.name}: published version already on the site as data/publications/{published[0]}.yaml")
      move_to_bibtexs(bib)
      continue

    # The preprint records of this paper are replaced: their addresses now lead to the new record
    base = sitedb.slugify(re.sub(r"(\d+)", r"-\1-", key))
    rid = base if base in [old_id for old_id, _ in matches] else new_id(key)
    redirects = []
    for old_id, old in matches:
      if old_id != rid:
        redirects.append(f"/publications/{old_id}/")
      redirects += list(old.get("legacy_urls") or [])
      for field in ("research", "abstract"):
        if not record[field]:
          record[field] = old.get(field) or record[field]
    record["legacy_urls"] = redirects
    path = sitedb.write_record("publications", rid, record)
    print(f"wrote data/publications/{path.name}  (from python/{bib.name})")
    for old_id, _ in matches:
      if old_id != rid:
        sitedb.record_path("publications", old_id).unlink()
      print(f"      replaced the preprint data/publications/{old_id}.yaml")
    move_to_bibtexs(bib)


if __name__ == "__main__":
  sys.exit(main())
