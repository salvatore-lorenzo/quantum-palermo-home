"""Create one .bib file in python/ for each paper announced by arxiv-bot.

Reads the messages saved by newpapers.py (newpapers_messages.jsonl):
  - "New paper" messages become @misc arXiv entries;
  - "Update" messages (the paper got published), and new papers that already
    carry a DOI, become @article entries.
Title, authors and the full abstract come from the arXiv API, journal details
from Crossref (falling back to the journal reference written in the message).
Papers already present in bibtexs/ or python/ are skipped, existing files are
never overwritten, and file names are chosen so that the new files can be moved
into bibtexs/ without clashing. Papers with no author in the group (anyone with
a file in data/people/, under their name or one of their aliases) are skipped too.
"""

import calendar
import json
import re
import sys
import unicodedata
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path

import sitedb

MESSAGES_FILE = Path(__file__).with_name("newpapers_messages.jsonl")
BIB_DIR = Path(__file__).resolve().parent.parent / "bibtexs"
# New .bib files are written here, next to this script
OUT_DIR = Path(__file__).resolve().parent
# One file per group member; names they sign papers with are listed as `aliases` there
PEOPLE_DIR = sitedb.table_dir("people")

# Title words left out of citation keys, as arXiv does
STOPWORDS = {"a", "an", "the", "of", "for", "in", "on", "at", "to", "by", "with", "and", "or",
             "under", "via", "from", "into", "as"}
# Lowercase surname prefixes, e.g. "Lo Monaco", "Di Fresco"
PARTICLES = {"da", "de", "del", "della", "di", "du", "la", "le", "lo", "van", "von", "der", "den"}

ATOM = {"a": "http://www.w3.org/2005/Atom", "arxiv": "http://arxiv.org/schemas/atom"}


def get(url):
  request = urllib.request.Request(url, headers={"User-Agent": "newpapers-bib/1.0"})
  with urllib.request.urlopen(request, timeout=30) as response:
    return response.read()


def clean(text):
  # Collapse the line breaks and repeated spaces found in arXiv titles and abstracts
  return " ".join(text.split()) if text else ""


def ascii_lower(text):
  text = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode()
  return re.sub(r"[^a-z0-9]", "", text.lower())


def field(content, name):
  # Value of a "**Name:** value" line in an arxiv-bot message
  match = re.search(rf"\*\*{name}:\*\*[ \t]*(.+)", content)
  return match.group(1).strip() if match else None


def parse_message(content, posted):
  arxiv = re.search(r"arxiv\.org/abs/(\d{4}\.\d{4,5})", content)
  if not arxiv:
    return None
  doi = field(content, "DOI")
  if doi:
    doi = re.sub(r"^https?://(dx\.)?doi\.org/", "", doi).strip("<>")
  return {
    "arxiv": arxiv.group(1),
    "title": field(content, "Title"),
    "authors": field(content, "Authors"),
    "announced": field(content, "Announced"),
    "abstract": field(content, "Abstract"),
    "journal": field(content, "New journal reference") or field(content, "Journal Reference"),
    "doi": doi,
    "posted": posted,
  }


def fetch_arxiv(ids):
  # One API call for all ids; returns {arxiv id: metadata}
  query = urllib.parse.urlencode({"id_list": ",".join(ids), "max_results": len(ids)})
  try:
    root = ET.fromstring(get("https://export.arxiv.org/api/query?" + query))
  except (OSError, ET.ParseError) as error:
    print(f"arXiv lookup failed ({error}): using only the text of the messages")
    return {}
  papers = {}
  for entry in root.findall("a:entry", ATOM):
    arxiv_id = re.sub(r"v\d+$", "", entry.findtext("a:id", "", ATOM).rsplit("/abs/", 1)[-1])
    category = entry.find("arxiv:primary_category", ATOM)
    papers[arxiv_id] = {
      "title": clean(entry.findtext("a:title", "", ATOM)),
      "authors": [clean(a.findtext("a:name", "", ATOM)) for a in entry.findall("a:author", ATOM)],
      "abstract": clean(entry.findtext("a:summary", "", ATOM)),
      "date": entry.findtext("a:published", "", ATOM)[:10],
      "category": category.get("term") if category is not None else "quant-ph",
    }
  return papers


def fetch_crossref(doi):
  try:
    work = json.loads(get("https://api.crossref.org/works/" + urllib.parse.quote(doi)))["message"]
  except (OSError, ValueError, KeyError):
    return {}
  date = (work.get("published") or work.get("issued") or {}).get("date-parts", [[None]])[0]
  return {
    "authors": [f"{a['family']}, {a['given']}" if a.get("given") else a["family"]
                for a in work.get("author", []) if a.get("family")],
    "journal": (work.get("short-container-title") or work.get("container-title") or [None])[0],
    "volume": work.get("volume"),
    "number": work.get("issue"),
    "pages": work.get("article-number") or work.get("page"),
    "publisher": work.get("publisher"),
    "year": date[0],
    "month": date[1] if len(date) > 1 else None,
  }


def split_name(author):
  # "Gabriele Lo Monaco" or "Lo Monaco, Gabriele" -> ("Gabriele", "Lo Monaco")
  if "," in author:
    family, given = author.split(",", 1)
    return given.strip(), family.strip()
  words = author.replace(" et al.", "").split()
  i = len(words) - 1
  while i > 1 and words[i - 1].lower() in PARTICLES:
    i -= 1
  return " ".join(words[:i]), " ".join(words[i:])


def surname(author):
  # "Gabriele Lo Monaco" or "Lo Monaco, Gabriele" -> "lomonaco"
  return ascii_lower(split_name(author)[1])


def name_key(author):
  # (surname, first initial): "G. Massimo Palma" -> ("palma", "g"), "Salvatore Di Lorenzo" -> ("dilorenzo", "s")
  given, family = split_name(author)
  return ascii_lower(family), ascii_lower(given)[:1]


def group_members():
  # Name keys of everyone in data/people/, from their name and their aliases
  members = set()
  for person in sitedb.records("people").values():
    if not person.get("name"):
      continue
    for name in [person["name"]] + list(person.get("aliases") or []):
      members.add(name_key(name))
    # Each word of the surname too, for papers signed with one of two surnames ("Silvia Casulleras")
    initial = ascii_lower(split_name(person["name"])[0])[:1]
    words = [w for w in (person.get("sort") or "").split() if w.lower() not in PARTICLES]
    members.update((ascii_lower(w), initial) for w in words)
  return members


def citation_key(author, year, title):
  # arXiv style: surname + year + first four meaningful title words
  words = [ascii_lower(w) for w in title.split()]
  words = [w for w in words if w and w not in STOPWORDS]
  return f"{surname(author)}{year}{''.join(words[:4])}"


def build_entry(msg, arxiv):
  # Returns (entry type, author list, year, fields), or None if there is too little to go on
  title = arxiv.get("title") or msg["title"]
  if not title:
    return None
  authors = arxiv.get("authors") or (msg["authors"] or "").split(", ")
  abstract = arxiv.get("abstract") or (msg["abstract"] or "").replace(" [truncated]", "")
  date = msg["announced"] or arxiv.get("date") or msg["posted"]
  year, month = int(date[:4]), int(date[5:7])
  arxiv_url = f"https://arxiv.org/abs/{msg['arxiv']}"

  if not (msg["doi"] or msg["journal"]):
    return "misc", authors, year, {
      "title": title,
      "author": " and ".join(authors),
      "abstract": abstract,
      "year": year,
      "month": calendar.month_abbr[month],
      "eprint": msg["arxiv"],
      "archivePrefix": "arXiv",
      "primaryClass": arxiv.get("category", "quant-ph"),
      "url": arxiv_url,
    }

  journal = fetch_crossref(msg["doi"]) if msg["doi"] else {}
  authors = journal.get("authors") or authors
  if journal.get("year"):
    year, month = journal["year"], journal["month"]
  else:
    # No Crossref record: take the year from the journal reference, if it has one
    ref_year = re.search(r"\b(19|20)\d{2}\b", msg["journal"] or "")
    year, month = (int(ref_year.group(0)), None) if ref_year else (year, month)
  venue = journal.get("journal") or msg["journal"]
  is_proceedings = not journal and "proceedings" in (venue or "").lower()
  return ("inproceedings" if is_proceedings else "article"), authors, year, {
    "title": title,
    "author": " and ".join(authors),
    "abstract": abstract,
    ("booktitle" if is_proceedings else "journal"): venue,
    "volume": journal.get("volume"),
    "number": journal.get("number"),
    "pages": journal.get("pages"),
    "year": year,
    "month": calendar.month_abbr[month] if month else None,
    "publisher": journal.get("publisher"),
    "doi": msg["doi"],
    "url": f"https://doi.org/{msg['doi']}" if msg["doi"] else arxiv_url,
    "eprint": msg["arxiv"],
    "archivePrefix": "arXiv",
  }


def free_path(base):
  # python/<base>.bib, or <base>b.bib, <base>c.bib, ... if the name is taken here or in bibtexs/
  for suffix in [""] + list("bcdefghijklmnopqrstuvwxyz"):
    name = f"{base}{suffix}.bib"
    if not (OUT_DIR / name).exists() and not (BIB_DIR / name).exists():
      return OUT_DIR / name
  raise FileExistsError(f"too many {base}*.bib files")


def main():
  records = [json.loads(line) for line in MESSAGES_FILE.open(encoding="utf-8") if line.strip()]
  messages = [m for m in (parse_message(r["content"], r["date"]) for r in records) if m]
  bib_files = list(BIB_DIR.glob("*.bib")) + list(OUT_DIR.glob("*.bib"))
  existing = {p: p.read_text(encoding="utf-8", errors="replace").lower() for p in bib_files}

  def found_in(text):
    return next((f"{p.parent.name}/{p.name}" for p, bib in existing.items() if text.lower() in bib), None)

  members = group_members()
  if not members:
    sys.exit(f"no group members found in {PEOPLE_DIR}")
  arxiv = fetch_arxiv(sorted({m["arxiv"] for m in messages}))
  for msg in messages:
    # A published paper is recognised by its DOI (or journal reference), a preprint by its arXiv id
    where = found_in(msg["doi"] or msg["journal"] or msg["arxiv"])
    if where:
      print(f"skip  {msg['arxiv']}: already in {where}")
      continue
    entry = build_entry(msg, arxiv.get(msg["arxiv"], {}))
    if not entry:
      print(f"skip  {msg['arxiv']}: no title found on arXiv or in the message")
      continue
    kind, authors, year, fields = entry
    # arxiv-bot sometimes tags the wrong person (e.g. "Salvatore Di Lorenzo" for "Salvatore Lorenzo")
    if not any(name_key(a) in members for a in authors):
      shown = ", ".join(authors[:4]) + (", ..." if len(authors) > 4 else "")
      print(f"skip  {msg['arxiv']}: no author from the group ({shown})")
      continue
    key = citation_key(authors[0], year, fields["title"])
    lines = [f"  {name} = {{{value}}}," for name, value in fields.items() if value]
    text = f"@{kind}{{{key},\n" + "\n".join(lines) + "\n}\n"

    preprint = found_in(msg["arxiv"]) if kind != "misc" else None
    path = free_path(f"{surname(authors[0])}{year}")
    path.write_text(text, encoding="utf-8")
    existing[path] = text.lower()
    print(f"wrote python/{path.name}" + (f"  (preprint version in {preprint})" if preprint else ""))


if __name__ == "__main__":
  main()
