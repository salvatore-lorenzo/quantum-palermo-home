"""Read and write the site database in data/.

The database is a set of folders of YAML files, one file per record:

  data/people/<id>.yaml         group members, current and former
  data/publications/<id>.yaml   papers and preprints
  data/research/<id>.yaml       research lines
  data/projects/<id>.yaml       funded projects
  data/events/<id>.yaml         conferences, workshops, schools, seminars

The file name (without .yaml) is the record id, used to link records together.
Only the standard library is used, so the scripts also run with the system python3.
"""

import json
import re
import textwrap
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data"
TABLES = ["people", "publications", "research", "projects", "events"]

# Lowercase surname prefixes, e.g. "Lo Monaco", "Di Fresco"
PARTICLES = {"da", "de", "del", "della", "di", "du", "la", "le", "lo", "van", "von", "der", "den"}


def table_dir(table):
  return DATA_DIR / table


def record_path(table, record_id):
  return table_dir(table) / f"{record_id}.yaml"


def slugify(text):
  # "Bönsel 2025: Fibonacci" -> "bonsel-2025-fibonacci"
  text = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode()
  return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")


def ascii_lower(text):
  text = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode()
  return re.sub(r"[^a-z0-9]", "", text.lower())


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


def name_key(author):
  # (surname, first initial): "G. Massimo Palma" -> ("palma", "g")
  given, family = split_name(author)
  return ascii_lower(family), ascii_lower(given)[:1]


def match_key(name):
  # The key the website uses to recognise a group member in an author list:
  # lowercase letters only, so "G. Massimo Palma" and "G Massimo Palma" are the same.
  # Must stay in sync with layouts/partials/db/name-key.html
  return re.sub(r"[^\w]|[\d_]", "", name.lower())


# ---------------------------------------------------------------- writing YAML

_NOT_STRINGS = re.compile(
  r"(?i)^(y|n|yes|no|on|off|true|false|null|~|[-+]?(\d[\d_]*)?(\.\d*)?([eE][-+]?\d+)?|0x[0-9a-f]+|\.inf|\.nan)$")
_DATE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
_SEXAGESIMAL = re.compile(r"^[-+]?[\d_]+(:[0-5]?\d)+(\.\d*)?$")  # YAML 1.1 reads "15:00" as a number
_PLAIN_FIRST = re.compile(r"^[\w(/]", re.UNICODE)
_PLAIN_BAD = re.compile(r": |:$| #|^\s|\s$|\s\s|\t|[\"{}\[\]]")


def _plain_ok(text):
  if _DATE.match(text):
    return True
  return bool(text) and _PLAIN_FIRST.match(text) and not _PLAIN_BAD.search(text) \
    and not _NOT_STRINGS.match(text) and not _SEXAGESIMAL.match(text)


def _foldable(text):
  return len(text) > 90 and "\n" not in text and not re.search(r"\s\s|\t|^\s|\s$", text)


def _scalar(prefix, value, indent, out):
  pad = " " * (indent + 2)
  if isinstance(value, bool):
    out.append(f"{prefix} {'true' if value else 'false'}")
  elif isinstance(value, (int, float)):
    out.append(f"{prefix} {value}")
  else:
    text = str(value)
    if "\n" in text.strip("\n"):
      lines = textwrap.dedent(text.strip("\n")).split("\n")
      header = "|-" if not lines[0].startswith(" ") else "|2-"
      out.append(f"{prefix} {header}")
      out.extend(pad + line.rstrip() if line.strip() else "" for line in lines)
    elif _foldable(text) and not re.match(r"^\w+://\S+$", text):
      out.append(f"{prefix} >-")
      out.extend(pad + line for line in textwrap.wrap(text, 88, break_on_hyphens=False, break_long_words=False))
    elif _plain_ok(text):
      out.append(f"{prefix} {text}")
    else:
      out.append(f"{prefix} {json.dumps(text, ensure_ascii=False)}")


def _empty(value):
  return value is None or value == "" or value == [] or value == {}


def _mapping(record, indent, out):
  pad = " " * indent
  for key, value in record.items():
    if _empty(value):
      continue
    if isinstance(value, dict):
      out.append(f"{pad}{key}:")
      _mapping(value, indent + 2, out)
    elif isinstance(value, list):
      out.append(f"{pad}{key}:")
      _sequence(value, indent + 2, out)
    else:
      _scalar(f"{pad}{key}:", value, indent, out)


def _sequence(items, indent, out):
  pad = " " * indent
  for item in items:
    if isinstance(item, dict):
      lines = []
      _mapping(item, indent + 2, lines)
      lines[0] = pad + "- " + lines[0][indent + 2:]
      out.extend(lines)
    elif isinstance(item, list):
      raise ValueError("lists of lists are not supported")
    else:
      _scalar(f"{pad}-", item, indent, out)


def dump(record, comment=None):
  """YAML text of a record (a dict); empty values are left out."""
  out = [f"# {line}".rstrip() for line in comment.split("\n")] if comment else []
  _mapping(record, 0, out)
  return "\n".join(out) + "\n"


def dump_list(items, comment=None):
  """YAML text of a list of records."""
  out = [f"# {line}".rstrip() for line in comment.split("\n")] if comment else []
  _sequence(items, 0, out)
  return "\n".join(out) + "\n"


def write_record(table, record_id, record, comment=None):
  path = record_path(table, record_id)
  path.parent.mkdir(parents=True, exist_ok=True)
  path.write_text(dump(record, comment), encoding="utf-8")
  return path


# ---------------------------------------------------------------- reading YAML
# A small reader for the top-level fields the scripts need (strings and lists of
# strings). Nested mappings are skipped. Hugo reads the full files.

def _unquote(text):
  text = text.strip()
  if text.startswith('"'):
    return json.loads(text)
  if text.startswith("'") and text.endswith("'"):
    return text[1:-1].replace("''", "'")
  return re.sub(r"\s+#.*$", "", text)


def read_fields(path):
  """Top-level scalar and list-of-scalar fields of a YAML record."""
  fields, key, block, items = {}, None, None, None
  lines = Path(path).read_text(encoding="utf-8").split("\n") + [""]
  for line in lines:
    if block is not None:
      if line.startswith("  ") or not line.strip():
        block.append(line[2:])
        continue
      style, body = block[0], block[1:]
      while body and not body[-1].strip():
        body.pop()
      fields[key] = "\n".join(body) if style.startswith("|") else " ".join(l.strip() for l in body if l.strip())
      block = None
    if items is not None:
      match = re.match(r"^\s+-\s+(.*)$", line)
      if match and not re.match(r"^\s+-\s+\w+:\s", line):
        items.append(_unquote(match.group(1)))
        continue
      if line.startswith(" "):
        items = None  # list of mappings: skipped
        fields.pop(key, None)
        continue
      items = None
    match = re.match(r"^([A-Za-z_][\w-]*):\s*(.*)$", line)
    if not match:
      continue
    key, rest = match.group(1), match.group(2)
    if rest.startswith(("|", ">")):
      block = [rest]
    elif rest in ("", "[]"):
      items = []
      fields[key] = items
    elif rest.startswith("["):
      fields[key] = [_unquote(x) for x in rest.strip("[]").split(",") if x.strip()]
    else:
      fields[key] = _unquote(rest)
  return fields


def records(table):
  """{id: fields} for every record of a table."""
  return {p.stem: read_fields(p) for p in sorted(table_dir(table).glob("*.yaml"))}


# ---------------------------------------------------------------- BibTeX

def drop_bib_field(bib, name):
  """BibTeX entry without the field `name` (braces inside the value are matched)."""
  match = re.search(rf"(^|,)\s*{name}\s*=\s*", bib, re.I | re.M)
  if not match:
    return bib
  i, depth = match.end(), 0
  if bib[i] == "{":
    for j in range(i, len(bib)):
      depth += {"{": 1, "}": -1}.get(bib[j], 0)
      if depth == 0:
        break
  elif bib[i] == '"':
    j = bib.index('"', i + 1)
  else:
    j = re.search(r"[,}\n]", bib[i:]).start() + i - 1
  end = j + 1
  if bib[end:end + 1] == ",":
    end += 1
  return (bib[:match.start()] + match.group(1) + bib[end:]).replace(",,", ",")


# ---------------------------------------------------------------- research lines

def suggest_research(title, abstract, research):
  """Research line ids whose keywords appear in a paper (title words count three times).

  `research` is records("research"): each line lists its `keywords`. At most two
  lines are returned, best match first. These are suggestions: check them by hand."""
  title, abstract = (title or "").lower(), (abstract or "").lower()
  scores, in_title = {}, False
  for line_id, line in research.items():
    words = [w.lower() for w in line.get("keywords") or []]
    hits = sum(title.count(w) for w in words)
    in_title = in_title or hits > 0
    score = 3 * hits + sum(abstract.count(w) for w in words)
    if score >= 2:
      scores[line_id] = score
  if not in_title and not re.search(r"quantum|qubit", abstract):
    return []  # matches only in a non-quantum abstract, e.g. the ecology papers
  return sorted(scores, key=lambda k: -scores[k])[:2]
