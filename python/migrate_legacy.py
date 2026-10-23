"""Convert the old HugoBlox website into the new site database (one-shot).

    python3.11 python/migrate_legacy.py [--source PATH]

Reads the old content/ folder of PATH (default: this repository) and writes
  data/people, data/publications, data/research, data/projects, data/events,
  data/funders.yaml and the images in assets/images/.
Run it again on a checkout of the old site to pick up papers added there in the
meantime, e.g.
    git worktree add ../old-site main
    python3.11 python/migrate_legacy.py --source ../old-site
Pages of the deployed old site (public/, see --deployed) that are no longer in its
content, e.g. replaced preprints, get a redirect to the paper with the same arXiv id or DOI.
Existing records are overwritten. Needs PyYAML (to read the old front matter).
"""

import argparse
import html
import re
import shutil
import sys
from pathlib import Path

import yaml

import sitedb

DST = sitedb.ROOT
IMAGES = DST / "assets" / "images"

GROUPS = {"Staff": "faculty", "Postdoc": "postdoc", "PhD Students": "phd", "Students": "student"}
LINK_ICONS = {"home": "website", "orcid": "orcid", "google-scholar": "scholar", "arxiv": "arxiv",
              "researcherid": "wos", "linkedin": "linkedin", "github": "github", "twitter": "twitter"}
PUB_TYPES = {"article-journal": "article", "manuscript": "preprint", "paper-conference": "proceedings",
             "chapter": "chapter"}
ROLES = {"full professor": "Full Professor", "associate professor": "Associate Professor",
         "assistant professor": "Assistant Professor", "phd student": "PhD Student",
         "visiting phd student": "Visiting PhD Student", "postdoctoral researcher": "Postdoctoral Researcher",
         "scholarship holder": "Scholarship Holder"}
# Spelling fixes for obvious typos in the old pages
NAME_FIXES = {"Duillio De Santis": "Duilio De Santis"}
# Names group members sign papers with that the automatic matching can't find
EXTRA_ALIASES = {"kam-chon-fai": ["Chon-Fai Kam"]}

RESEARCH = {
  # id: (order, short name, keywords used to suggest the research lines of a paper)
  "thermo": (1, "Thermodynamics", [
    "thermodynamic", "heat", "work extraction", "entropy production", "landauer", "quantum batter",
    "batteries", "battery", "refrigerator", "heat engine", "thermal machine", "ergotropy", "fluctuation theorem", "thermaliz",
    "irreversib"]),
  "qinfo": (2, "Information", [
    "entangle", "quantum information", "state transfer", "scrambling", "quantum communication",
    "quantum network", "quantum channel", "non-markovian", "collision model", "quantum computing",
    "quantum computation", "quantum circuit", "tomography", "classical shadow", "quantum resource",
    "quantum correlations", "darwinism"]),
  "metro": (3, "Metrology", [
    "metrolog", "estimation", "estimator", "fisher information", "sensing", "sensor", "thermometry",
    "probing", "quantum probe", "cramér-rao", "cramer-rao"]),
  "wqed": (4, "Waveguide QED", [
    "waveguide", "atom-photon", "photonic lattice", "photonic bath", "giant atom", "quantum emitter",
    "emitters", "photonic crystal", "bound state", "chiral", "coupled cavities", "non-hermitian"]),
  "mater": (5, "Materials", [
    "material", "tddft", "density functional", "floquet", "high-harmonic", "harmonic generation",
    "attosecond", "ultrafast", "laser pulse", "laser-driven", "electron dynamics", "graphene", "magnon",
    "phonon", "solid", "spectroscopy"]),
  "qml": (6, "Machine Learning", [
    "machine learning", "learning", "neural network", "reservoir comput", "extreme learning"]),
  "found": (7, "Foundations", [
    "foundation", "collapse model", "spontaneous collapse", "darwinism", "objectiv", "gravit",
    "macroscopic", "quantum-to-classical", "classicality", "wigner", "intersubjectiv",
    "levitated", "bell inequal", "contextual"]),
}

# Research lines of each project, from the project descriptions
PROJECT_RESEARCH = {
  "aspeqct": ["thermo", "qinfo"], "harnessing": ["wqed"], "hyqelm": ["qml"], "qucom": ["found"],
  "qureco": ["qml", "thermo"], "thence": ["mater", "wqed"], "times": ["mater"],
}
# Funding programme, where the old pages state it
PROJECT_PROGRAMME = {
  "harnessing": "PRIN — funded by the European Union, NextGenerationEU",
  "qureco": "Funded by the European Union, NextGenerationEU",
  "hyqelm": "Funded by the European Union, NextGenerationEU — MUR",
  "qucom": "Horizon Europe — European Commission",
  "times": "Marie Skłodowska-Curie Actions — Doctoral Network",
}
FUNDING_LOGOS = re.compile(r"finanziato|logo-ce|marie-curie|PastedGraphic-2", re.I)

FUNDERS = [
  ("University of Palermo", "https://www.unipa.it", "unipa.jpeg"),
  ("MUR — PRIN", "https://prin.mur.gov.it/", "prin.jpeg"),
  ("Marie Skłodowska-Curie Actions", "https://marie-sklodowska-curie-actions.ec.europa.eu/", "marie-curie.jpg"),
  ("Horizon Europe", "https://qucom.eu/", "corsimo.jpg"),
  ("EPSRC", "https://gow.epsrc.ukri.org/NGBOViewGrant.aspx?GrantRef=EP/T028106/1", "epsrc.jpg"),
  ("The Royal Society", "https://royalsociety.org/", "royal.png"),
  ("IBM", "", "ibm.png"),
]


def front_matter(path):
  text = path.read_text(encoding="utf-8").replace("\t", "  ")
  match = re.match(r"^---\s*\n(.*?)\n---\s*(?:\n|$)(.*)$", text, re.S)
  return yaml.safe_load(match.group(1)) or {}, match.group(2)


def html_to_md(text):
  """Old page bodies (simple HTML) -> (markdown paragraphs, image file names)."""
  text = re.sub(r"<!--.*?-->|<style.*?</style>|<script.*?</script>|<title>.*?</title>", "", text, flags=re.S)
  images = re.findall(r"<img[^>]*?src=\"\.?/?([^\"]+)\"", text)
  text = re.sub(r"<img[^>]*>", "\n\n", text)
  text = re.sub(r"<a [^>]*href=\"([^\"]+)\"[^>]*>(.*?)</a>", r"[\2](\1)", text, flags=re.S)
  text = re.sub(r"</?(b|strong)>", "**", text)
  text = re.sub(r"</?(i|em)>", "*", text)
  text = re.sub(r"<br\s*/?>|</?p[^>]*>|</?div[^>]*>|</?section[^>]*>", "\n\n", text)
  text = re.sub(r"<[^>]+>", "", text)
  text = html.unescape(text)
  paragraphs = [" ".join(p.split()) for p in re.split(r"\n\s*\n", text)]
  return "\n\n".join(p for p in paragraphs if p), images


def copy_image(src, dst):
  dst.parent.mkdir(parents=True, exist_ok=True)
  shutil.copyfile(src, dst)


def clean_tables():
  for table in sitedb.TABLES:
    shutil.rmtree(sitedb.table_dir(table), ignore_errors=True)
  for sub in ["people", "research", "projects", "events", "funders"]:
    shutil.rmtree(IMAGES / sub, ignore_errors=True)


# ---------------------------------------------------------------- people

def migrate_people(src):
  people, folder_ids = {}, {}
  for index in sorted((src / "content" / "authors").glob("*/_index.md")):
    data, body = front_matter(index)
    old_name = (data.get("title") or "").strip()
    name = NAME_FIXES.get(old_name, old_name)
    pid = sitedb.slugify(name)
    folder_ids[index.parent.name.lower()] = pid
    groups = [g for g in data.get("user_groups") or [] if g]
    role = " ".join((data.get("role") or "").split())
    role = ROLES.get(role.lower(), role)
    if groups:
      group, status = GROUPS[groups[0]], "current"
    else:
      group, status = ("postdoc" if "postdoc" in role.lower() else "phd"), "alumni"
    links, email = {}, (data.get("email") or "").strip()
    for item in data.get("social") or []:
      link = (item.get("link") or "").strip()
      if not link or link.endswith(("/record/", "arxiv.org/a/", "/in/")):
        continue
      if item.get("icon") == "envelope":
        email = email or link.replace("mailto:", "")
      elif item.get("icon") in LINK_ICONS:
        links[LINK_ICONS[item["icon"]]] = link if re.match(r"https?://", link) else "https://" + link
    organizations = [{"name": o.get("name"), "url": o.get("url")} for o in data.get("organizations") or []
                     if o.get("name")]
    education = [{"degree": c.get("course"), "institution": c.get("institution"),
                  "url": c.get("url_institution") or "", "year": c.get("year")}
                 for c in (data.get("education") or {}).get("courses") or [] if c.get("course")]
    bio, _ = html_to_md(body)
    bio = re.sub(r"^Short bio\s*", "", bio)
    record = {
      "name": name,
      "sort": (data.get("last_name") or sitedb.split_name(name)[1]).strip(),
      "role": role,
      "group": group,
      "status": status,
      "email": email if "@" in email and email != "quantum.unipa.it" else "",
      "links": links,
      "organizations": organizations,
      "interests": [i.strip() for i in data.get("interests") or [] if i and i.strip()],
      "education": education,
      "aliases": list(EXTRA_ALIASES.get(pid, [])),
      "bio": bio,
    }
    people[pid] = {"record": record, "old_url": f"/author/{old_name.lower().replace(' ', '-')}/"}
    avatar = next(index.parent.glob("avatar.*"), None)
    if avatar:
      copy_image(avatar, IMAGES / "people" / f"{pid}{avatar.suffix.lower()}")
  return people, folder_ids


def add_aliases(people, publications):
  # Every spelling of a member's name found in the papers: same surname and first
  # initial, but a different match key (e.g. "Diana A. Chisholm", "G Massimo Palma")
  keys = {sitedb.name_key(p["record"]["name"]): pid for pid, p in people.items()}
  for extra_pid, extra in EXTRA_ALIASES.items():
    for name in extra:
      keys[sitedb.name_key(name)] = extra_pid
  report = []
  for pub in publications.values():
    for author in pub["record"]["authors"]:
      pid = keys.get(sitedb.name_key(author))
      if not pid:
        continue
      record = people[pid]["record"]
      known = {sitedb.match_key(n) for n in [record["name"]] + record["aliases"]}
      if sitedb.match_key(author) not in known:
        record["aliases"].append(author)
        report.append(f"  {pid}: {author}")
  return report


# ---------------------------------------------------------------- publications

def bib_field(bib, name):
  match = re.search(rf"\b{name}\s*=\s*[{{\"](.*?)[}}\"]\s*,?\s*\n", bib, re.I | re.S)
  return " ".join(match.group(1).split()) if match else ""


def migrate_publications(src, research):
  publications = {}
  for index in sorted((src / "content" / "publication").glob("*/index.md")):
    data, _ = front_matter(index)
    cite = index.parent / "cite.bib"
    bib = sitedb.drop_bib_field(cite.read_text(encoding="utf-8").strip(), "abstract") if cite.exists() else ""
    links = {l.get("name"): l.get("url") for l in data.get("links") or []}
    arxiv = ""
    if links.get("arXiv"):
      arxiv = re.sub(r"v\d+$", "", links["arXiv"].rstrip("/").rsplit("/", 1)[-1])
    elif bib_field(bib, "eprint"):
      arxiv = bib_field(bib, "eprint")
    kind = PUB_TYPES.get((data.get("publication_types") or ["article-journal"])[0], "article")
    title = " ".join((data.get("title") or "").split()).replace("---", "—").replace("--", "–")
    abstract = " ".join((data.get("abstract") or "").split())
    journal = (data.get("publication") or "").replace("*", "").strip()
    if kind == "preprint" and journal.lower().startswith("arxiv"):
      journal = ""
    record = {
      "title": title,
      "authors": [" ".join(a.split()) for a in data.get("authors") or []],
      "date": str(data.get("date"))[:10],
      "type": kind,
      "journal": journal,
      "volume": bib_field(bib, "volume"),
      "issue": bib_field(bib, "number") or bib_field(bib, "issue"),
      "pages": bib_field(bib, "pages"),
      "doi": (data.get("doi") or "").strip(),
      "arxiv": arxiv,
      "url": links.get("URL") or "",
      "research": sitedb.suggest_research(title, abstract, research),
      "keywords": [t for t in data.get("tags") or [] if t and t.strip()],
      "abstract": abstract,
      "bibtex": bib,
    }
    pid = sitedb.slugify(index.parent.name)
    publications[pid] = {"record": record, "old_urls": [f"/publication/{pid}/"]}
  return publications


# ---------------------------------------------------------------- research, projects, events

def migrate_research(src):
  lines = {}
  for rid, (order, short, keywords) in RESEARCH.items():
    data, _ = front_matter(src / "content" / "research_lines" / rid / "index.md")
    hero = data["sections"][0]["content"]
    body, _ = html_to_md(hero["text"])
    body = body.replace("physical quantitiy", "physical quantity")
    caption = ""
    picture = re.search(r"\s*\(Picture: (.*?)\)\s*$", body)
    if picture:
      caption, body = picture.group(1), body[:picture.start()]
    title = hero["title"].replace("Machine learning", "Machine Learning")
    lines[rid] = {
      "title": title,
      "short": short,
      "order": order,
      "summary": re.split(r"(?<=[.!?])\s", body, 1)[0],
      "image_caption": caption,
      "keywords": keywords,
      "body": body,
    }
    featured = next((src / "content" / "research_lines" / rid).glob("featured.*"))
    copy_image(featured, IMAGES / "research" / f"{rid}{featured.suffix.lower()}")
  return lines


def migrate_projects(src, folder_ids):
  projects = {}
  for index in sorted((src / "content" / "projects").glob("*/index.md")):
    pid = index.parent.name
    data, body = front_matter(index)
    text, images = html_to_md(body)
    website = next((l.get("url") for l in data.get("links") or [] if l.get("url")), "")
    figures = [i for i in images if not FUNDING_LOGOS.search(i)]
    logos = [i for i in images if FUNDING_LOGOS.search(i)]
    if pid == "times":
      logos.append("marie-curie-actions-black.jpg")
    for image in figures + logos:
      copy_image(index.parent / image, IMAGES / "projects" / pid / image)
    featured = next(index.parent.glob("featured.*"))
    copy_image(featured, IMAGES / "projects" / pid / f"logo{featured.suffix.lower()}")
    projects[pid] = {
      "acronym": data["title"].strip() if len(data["title"]) < 20 else "",
      "title": data["title"].strip(),
      "programme": PROJECT_PROGRAMME.get(pid, ""),
      "date": str(data.get("date"))[:10],
      "status": "active",
      "website": website,
      "team": [folder_ids.get(a.lower(), a) for a in data.get("authors") or []],
      "research": PROJECT_RESEARCH.get(pid, []),
      "figures": [{"file": f} for f in figures],
      "funding_logos": logos,
      "body": text,
    }
  return projects


def parse_program(body, dates):
  """Days of talks of the QRC2024 page: tabs of event rows plus modals with the abstracts."""
  modals = {}
  for mid, inner in re.findall(r"<div class=\"modal fade\" id=\"(\w+)\".*?>(.*?)\n</div>", body, re.S):
    title = re.search(r"<h6>\s*Title:\s*(.*?)</h6>", inner, re.S)
    abstract = re.search(r"<p>\s*Abstract:\s*(.*?)</p>", inner, re.S)
    modals[mid.lower()] = (" ".join(title.group(1).split()) if title else "",
                           " ".join(abstract.group(1).split()) if abstract else "")
  labels = re.findall(r"data-bs-target=\"#day\d\"[^>]*>([^<]+)</button>", body)
  days = []
  for n, pane in enumerate(re.split(r"<div class=\"tab-pane", body)[1:]):
    slots = []
    for row in re.split(r"<div class=\"event-row", pane)[1:]:
      time = re.search(r"event-time\">([^<]*)<", row).group(1).strip()
      pause = re.search(r"event-description-break\">(.*?)</div>", row, re.S)
      talk = re.search(r"data-bs-target=\"#(\w+)\">([^<]+)</h4>\s*<p[^>]*>(.*?)</p>", row, re.S)
      if pause and time:
        slots.append({"time": time, "break": " ".join(re.sub(r"<[^>]+>", " ", pause.group(1)).split())})
      elif talk:
        title, abstract = modals.get(talk.group(1).lower(), ("", ""))
        short_title = " ".join(re.sub(r"<br\s*/?>", " ", talk.group(3)).split())
        slots.append({"time": time, "speaker": talk.group(2).strip(), "title": title or short_title,
                      "abstract": abstract})
    days.append({"date": dates[n], "label": labels[n].strip() if n < len(labels) else "", "slots": slots})
  return days


EVENT_FIXES = {
  # obvious word cuts in the old QRC2024 description
  "tools for tum computation": "tools for quantum computation",
  "solved by QRC and, bly, the": "solved by QRC and, notably, the",
}
EVENT_INFO = {
  # id: (kind, start, end) - QRC2024 dates come from the page text (the old front matter said May)
  "blinh2025": ("conference", "2025-12-14", "2025-12-18"),
  "qrc2024": ("course", "2024-10-15", "2024-10-18"),
  "topness2025": ("conference", "2025-04-27", "2025-05-01"),
  "wqed2025": ("workshop", "2025-09-01", "2025-09-06"),
}


def migrate_events(src):
  events = {}
  for index in sorted((src / "content" / "news").glob("*/index.md")):
    eid = index.parent.name.lower()
    data, body = front_matter(index)
    live = body.split("<!--<html")[0]
    header = re.search(r"<header.*?</header>", live, re.S).group(0)
    title = re.search(r"<h2 class=\"text-primary\">(.*?)</h2>", header, re.S).group(1).strip()
    directors = re.search(r"Directors of the Course:\s*(.*?)</p>", header, re.S).group(1)
    directors = [d.strip() for d in re.split(r"\s+[–-]\s+|,|<br>", directors) if d.strip()]
    school_directors = re.search(r"Directors of the School:\s*(.*?)</p>", header, re.S).group(1).strip()
    section = re.search(r"<section class=\"mb-5\">(.*?)</section>", live, re.S).group(1)
    for old, new in EVENT_FIXES.items():
      section = section.replace(old, new)
    registration = re.search(r"<a href=\"([^\"]+)\">REGISTER</a>", section)
    section = re.sub(r"<p>If you want to join us.*?</p>", "", section, flags=re.S)
    description, logos = html_to_md(section)
    kind, start, end = EVENT_INFO[eid]
    days = [f"{start[:8]}{int(start[8:]) + i:02d}" for i in range(4)]
    for logo in logos:
      copy_image(index.parent / logo, IMAGES / "events" / eid / logo)
    banner = next(index.parent.glob("featured.*"), None)
    if banner:
      copy_image(banner, IMAGES / "events" / eid / f"banner{banner.suffix.lower()}")
    events[eid] = {
      "record": {
        "title": title,
        "short": re.search(r"<h1>(.*?)</h1>", header).group(1).strip(),
        "kind": kind,
        "start": start,
        "end": end,
        "venue": "Ettore Majorana Foundation and Centre for Scientific Culture",
        "city": "Erice, Italy",
        "series": "International School on Nonequilibrium Phenomena",
        "series_directors": school_directors,
        "directors": directors,
        "website": data.get("external_link") or "",
        "registration": registration.group(1) if registration else "",
        "logos": logos,
        "description": description,
        "program": parse_program(live, days) if "tab-pane" in live else [],
      },
      "old_urls": [f"/news/{eid}/", f"/pastevents/{eid}/"],
    }
  # The only seminar on the old site: a placeholder with date and speaker
  data, _ = front_matter(src / "content" / "seminars" / "Paolo Erdman" / "index.md")
  events["seminar-2024-03-paolo-erdman"] = {
    "record": {
      "title": "Seminar by Paolo Erdman",
      "kind": "seminar",
      "start": str(data["date"])[:16].replace(" ", "T") + ":00",
      "speaker": "Paolo Erdman",
      "venue": "Department of Physics and Chemistry, University of Palermo",
      "city": "Palermo, Italy",
    },
    "old_urls": ["/seminars/paolo-erdman/"],
  }
  return events


def add_deployed_redirects(deployed, publications):
  # Pages of the deployed site (public/) that are no longer in content/, typically preprints whose
  # published version has another name: they redirect to the record with the same arXiv id or DOI
  deployed = deployed / "publication"
  if not deployed.is_dir():
    return 0
  by_key = {}
  for pid, pub in publications.items():
    for key in (pub["record"]["arxiv"], pub["record"]["doi"].lower(), sitedb.ascii_lower(pub["record"]["title"])):
      if key:
        by_key[key] = pid
  added = 0
  for page in sorted(deployed.glob("*/index.html")):
    url = f"/publication/{page.parent.name}/"
    if page.parent.name in publications:
      continue
    html_text = page.read_text(encoding="utf-8", errors="replace")
    keys = re.findall(r"arxiv\.org/abs/(\d{4}\.\d{4,5})", html_text) + \
      [d.lower() for d in re.findall(r"doi\.org/(10\.[^\"'<\s]+)", html_text)] + \
      [sitedb.ascii_lower(html.unescape(t).rsplit(" | ", 1)[0])
       for t in re.findall(r'<meta property="og:title" content="([^"]*)"', html_text)]
    target = next((by_key[k] for k in keys if k in by_key), None)
    if target and url not in publications[target]["old_urls"]:
      publications[target]["old_urls"].append(url)
      added += 1
  return added


def main():
  parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
  parser.add_argument("--source", default=str(DST), help="root of the old site (default: this repository)")
  parser.add_argument("--deployed", default=str(DST / "public"),
                      help="the old site as deployed, to redirect its stale pages (default: public/)")
  args = parser.parse_args()
  src, deployed = Path(args.source).resolve(), Path(args.deployed).resolve()
  if not (src / "content" / "authors").is_dir():
    sys.exit(f"{src} does not look like the old site: content/authors/ is missing")
  clean_tables()

  research = migrate_research(src)
  for rid, record in research.items():
    sitedb.write_record("research", rid, record)
  research_fields = {rid: {"keywords": r["keywords"]} for rid, r in research.items()}

  people, folder_ids = migrate_people(src)
  publications = migrate_publications(src, research_fields)
  report = add_aliases(people, publications)
  redirected = add_deployed_redirects(deployed, publications)
  for pid, person in people.items():
    record = dict(person["record"], legacy_urls=[person["old_url"]])
    sitedb.write_record("people", pid, record)
  for pid, pub in publications.items():
    sitedb.write_record("publications", pid, dict(pub["record"], legacy_urls=pub["old_urls"]))

  for pid, record in migrate_projects(src, folder_ids).items():
    sitedb.write_record("projects", pid, record)
  for eid, event in migrate_events(src).items():
    sitedb.write_record("events", eid, dict(event["record"], legacy_urls=event["old_urls"]))

  funders = [{"name": n, "url": u, "logo": f} for n, u, f in FUNDERS]
  for funder in funders:
    copy_image(src / "content" / "sponsors" / funder["logo"], IMAGES / "funders" / funder["logo"])
  (sitedb.DATA_DIR / "funders.yaml").write_text(
    sitedb.dump_list(funders, "Logos shown at the bottom of the home page (images in assets/images/funders/)"),
    encoding="utf-8")

  tagged = sum(1 for p in publications.values() if p["record"]["research"])
  print(f"people {len(people)}, publications {len(publications)} ({tagged} with suggested research lines), "
        f"research {len(research)}")
  print(f"old addresses of the deployed site redirected to their current paper: {redirected}")
  print("name variants added as aliases:\n" + "\n".join(report))


if __name__ == "__main__":
  main()
