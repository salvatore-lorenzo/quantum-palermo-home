# quantum.unipa.it

Website of the Quantum Theory Group, Department of Physics and Chemistry – Emilio Segrè, University of Palermo.

This guide explains the three everyday jobs: **people**, **publications** and **events**. Everything is done by editing small text files in the `data/` folder; the website is rebuilt from them.

- [The workflow](#the-workflow)
- [1. People: add, update, remove](#1-people)
- [2. Publications: add, update, remove](#2-publications)
- [3. Events: upcoming and past events, seminars](#3-events)
- [Publishing the site](#publishing-the-site)
- [How the site works](#how-the-site-works)

---

## The workflow

1. **Change the files**: the records in `data/`, the images in `assets/images/`.
2. **Preview** in a terminal opened in this folder:

   ```sh
   hugo server
   ```

   and open <http://localhost:1313>. The page reloads every time you save a file. If something is wrong, the terminal shows an `ERROR` line that names the file to fix (see [Checks](#checks)). Stop the preview with `Ctrl+C`.
3. **Publish** (see [Publishing the site](#publishing-the-site)) and commit the changes to git.

### YAML in five rules

Records are written in YAML, a plain text format:

```yaml
name: Maria Rossi              # key: value
interests:                     # a list: one "- " per item
  - Open quantum systems
  - Quantum thermodynamics
links:                         # a group of keys: indent them by two spaces
  orcid: https://orcid.org/0000-0002-1825-0097
abstract: >-                   # >- long text: lines are joined into one paragraph
  We study the thermodynamics
  of $\mathcal{N}$ qubits.
bio: |                         # | text whose line breaks are kept (Markdown paragraphs)
  First paragraph.

  Second paragraph, with a [link](https://example.org).
```

1. Indent with **spaces**, never tabs.
2. Text that contains `: ` (colon and space) or starts with a symbol (`[`, `{`, `*`, `&`, `!`, `#`, `@`…) goes in quotes: `title: "Quantum chaos: a review"`.
3. Inside `>-` and `|` blocks you can write anything, with no quotes, including LaTeX: `$\alpha$`.
4. arXiv ids must be quoted, otherwise they are read as numbers: `arxiv: "2610.12015"`.
5. Anything after ` #` is a comment.

---

## 1. People

Each member has one file, `data/people/<id>.yaml`, and one photo, `assets/images/people/<id>.jpg`. The **id** is the file name, e.g. `maria-rossi`: lowercase, words separated by `-`. Their page is `/people/<id>/`.

### Add a person

**Step 1.** Create `data/people/maria-rossi.yaml` (or copy an existing file and change it):

```yaml
name: Maria Rossi
sort: Rossi
role: PhD Student
group: phd
status: current
email: maria.rossi@unipa.it
links:
  orcid: https://orcid.org/0000-0002-1825-0097
  scholar: https://scholar.google.com/citations?user=XXXXXXXXXXXX
  arxiv: https://arxiv.org/a/rossi_m_1
organizations:
  - name: University of Palermo
    url: https://www.unipa.it
interests:
  - Open quantum systems
  - Quantum thermodynamics
education:
  - degree: MSc in Physics
    institution: University of Palermo
    year: 2025
aliases:
  - M. Rossi
bio: |
  I obtained my Master's degree in Physics at the University of Palermo in 2025.

  I am now a PhD student working on quantum thermodynamics.
```

| Field | | |
|---|---|---|
| `name` | **required** | as it should appear on the site |
| `sort` | **required** | the last name; people are listed alphabetically by it |
| `group` | **required** | `faculty`, `postdoc`, `phd` or `student`: the section of the People page |
| `status` | **required** | `current`, or `alumni` for former members |
| `role` | | free text shown under the name: `Full Professor`, `Visiting PhD Student`… |
| `email` | | |
| `links` | | any of `website`, `orcid`, `scholar`, `arxiv`, `wos` (Web of Science), `github`, `linkedin`, `twitter` |
| `organizations` | | affiliations, each with `name` and optional `url` |
| `interests` | | list of research interests |
| `education` | | degrees, each with `degree`, `institution`, optional `url`, `year` (newest are shown first) |
| `aliases` | | other spellings of the name on papers, see below |
| `bio` | | Markdown text; leave an empty line between paragraphs |

**Step 2.** Add the photo as `assets/images/people/maria-rossi.jpg`: same name as the YAML file, `.jpg`, `.png` or `.webp` (not `.heic`). Any size: it is cropped to a portrait and resized automatically. Without a photo the page shows the initials.

**Step 3.** Preview with `hugo server`. Maria now appears on the People page in her group, in alphabetical order, and:

- every paper on the site with an author called `Maria Rossi` or `M. Rossi` shows her name as a link and is listed on her page;
- her page shows the research lines of her papers and the projects whose `team` includes `maria-rossi`;
- the arxiv-bot pipeline recognises her new papers as papers of the group.

### Update a person

Edit the file. For example, after the PhD defence of someone staying as a postdoc: `role: Postdoctoral Researcher` and `group: postdoc`. To change the photo, replace the image file (same name).

**A paper doesn't appear on someone's page?** The author name on the paper is spelled differently. Add that spelling to `aliases`:

```yaml
aliases:
  - G. M. Palma
  - G Massimo Palma
```

Matching ignores dots, spaces and capitals: `G. M. Palma` and `G M Palma` are the same.

### When someone leaves the group: make them alumni

Don't delete the file, change one line:

```yaml
status: alumni
```

and, if you like, update `role` to their last position here. They move to **Former members** on the People page; their page stays, marked "Former member"; their papers keep the link to them.

### Remove a person completely

1. Delete `data/people/<id>.yaml` and `assets/images/people/<id>.*`.
2. Remove the id from the `team:` lists in `data/projects/`. You don't need to search for them: the preview stops with a message for each project that still lists the person, e.g.

   ```
   ERROR data/projects/times.yaml: team member "maria-rossi" has no file in data/people/
   ```

3. Their papers stay on the site, with their name no longer linked, and the arxiv-bot pipeline no longer imports their new papers. Their page address (`/people/<id>/`) stops working.

---

## 2. Publications

Each paper is one file, `data/publications/<id>.yaml`, e.g. `artini-2025-coherentheatexchangeprethermalizing.yaml`. There are three ways to add one.

### A. Automatically, from the arxiv-bot posts on Discord (the usual way)

```sh
python3 python/update_publications.py
```

It needs an internet connection and the Discord bot token, in `python/discord_token.txt` (never committed) or in the `DISCORD_BOT_TOKEN` environment variable. It runs three scripts:

1. `newpapers.py` saves the latest arxiv-bot messages (`python/newpapers_messages.jsonl`);
2. `newbibs.py` writes one `.bib` file for each new paper with at least one author in `data/people/`, with title, authors and abstract from arXiv and journal details from Crossref;
3. `newpublications.py` turns each `.bib` file into a record in `data/publications/` and moves the `.bib` file to `bibtexs/`. Papers already on the site (same arXiv id or DOI) are skipped.

When the bot announces that a preprint **was published**, its record is replaced by the published version (journal, volume, pages, DOI), keeping the abstract and the research lines; the old address of the preprint redirects to the new one.

**Then check the new files** (`git status` lists them). In particular the `research` field: the research lines are guessed from the words of the title and abstract (the `keywords` of each line in `data/research/`), so correct them if needed.

### B. From a BibTeX entry, for any paper

1. Copy the BibTeX of the paper (arXiv "Export BibTeX citation", the journal's "Export citation", Google Scholar, INSPIRE…) into a new file in the `python/` folder, e.g. `python/rossi2026.bib`. **One entry per file.**
2. Run

   ```sh
   python3 python/newpublications.py
   ```

3. Check the new file in `data/publications/` (research lines!).

The same rules as above apply: a paper already on the site is skipped, a published version replaces its preprint.

### C. By hand

Create `data/publications/<surname>-<year>-<some-title-words>.yaml`:

```yaml
title: >-
  Coherent heat exchange in a prethermalizing open quantum system
authors:
  - Simone Artini
  - Mauro Paternostro
  - Salvatore Lorenzo
date: 2026-05-01
type: article
journal: Phys. Rev. A
volume: "113"
issue: "5"
pages: "052203"
doi: 10.1103/q5vb-dfgj
arxiv: "2505.01234"
url: https://link.aps.org/doi/10.1103/q5vb-dfgj
research:
  - thermo
abstract: >-
  We investigate a simple model exhibiting a prethermal phase, ...
bibtex: |
  @article{artini2025coherent,
    title = {Coherent heat exchange in a prethermalizing open quantum system},
    ...
  }
```

| Field | | |
|---|---|---|
| `title` | **required** | LaTeX between `$…$` is rendered |
| `authors` | **required** | names as on the paper; group members are linked automatically (by `name` or `aliases` in `data/people/`) |
| `date` | **required** | `YYYY-MM-DD`; use day `01` if you only know the month. Lists are sorted by it |
| `type` | **required** | `article`, `preprint`, `proceedings`, `chapter`, `book`, `thesis` or `other` |
| `journal`, `volume`, `issue`, `pages` | | |
| `doi` | | without `https://doi.org/` |
| `arxiv` | | the arXiv id, **in quotes** |
| `url` | | link used when there is no DOI |
| `research` | | research line ids: `thermo` (Thermodynamics), `qinfo` (Information), `metro` (Metrology), `wqed` (Waveguide QED), `mater` (Materials), `qml` (Machine Learning), `found` (Foundations) |
| `keywords` | | list of keywords |
| `abstract` | | |
| `bibtex` | | shown in the "Cite" box and included in the BibTeX file of all publications |

### Update a publication

Edit its file. The most common case is a preprint that got published and was not picked up by the bot: change `type: preprint` to `type: article` and add `journal`, `volume`, `issue`, `pages`, `doi` and the publication `date`; keep `arxiv`.

### Remove a publication

Delete its file. If it was a duplicate of another record, add its old address to the record you keep, so that links to it still work:

```yaml
legacy_urls:
  - /publications/<id-of-the-deleted-file>/
```

(`legacy_urls` fields already in the files keep the addresses of the old site working: leave them.)

---

## 3. Events

Each event is one file, `data/events/<id>.yaml`, e.g. `qrc2024.yaml`, plus an optional folder of images, `assets/images/events/<id>/`.

### Upcoming and past: automatic

You never move an event by hand. When the site is built, every event is compared with today's date:

- it is **upcoming** until its `end` date (or its `start` date, if it has no end) **included**;
- from the next day it is **past**.

| | Upcoming | Past |
|---|---|---|
| Events page | "Upcoming" section, soonest first | "Past events" section, most recent first (seminars are listed under "Seminars") |
| Home page | "Coming up": the next three events, seminars included | "Recent events": the last three (seminars excluded), when nothing is coming up |
| Event page | shows the Register button (if `registration` is set) | the Register button disappears, "past event" appears above the title |

**Because the site is rebuilt only when you publish it, publish again after an event** (any update does it, e.g. the next batch of publications); until then the online site still shows it as upcoming.

### Add a conference, workshop, school or course

**Step 1.** Create `data/events/qtw2027.yaml`:

```yaml
title: Quantum Thermodynamics Workshop
short: QTW2027
kind: workshop
start: 2027-03-10
end: 2027-03-12
venue: Department of Physics and Chemistry, University of Palermo
city: Palermo, Italy
directors:
  - S. Lorenzo
  - M. Paternostro
website: https://qtw2027.example.org
registration: https://qtw2027.example.org/register
logos:
  - unipa.png
description: |
  The workshop brings together experts in quantum thermodynamics ...

  A second paragraph, with a [link](https://example.org).
```

| Field | | |
|---|---|---|
| `title` | **required** | |
| `kind` | **required** | `conference`, `workshop`, `school`, `course`, `seminar` or `other` |
| `start` | **required** | `YYYY-MM-DD`; for a seminar with a time: `2026-11-05T15:00:00` |
| `end` | | last day, for events of more than one day |
| `short` | | acronym shown above the title on the cards |
| `venue`, `city` | | |
| `directors` | | list of names |
| `series`, `series_directors` | | e.g. the International School on Nonequilibrium Phenomena of the Erice events |
| `speaker` | | for seminars; linked if a group member |
| `website` | | "Event website" button |
| `registration` | | "Register" button, shown only while the event is upcoming |
| `logos` | | partner logos: file names in the event's image folder |
| `description` | | Markdown text |
| `program` | | the programme, see below |

**Step 2 (optional).** Images go in `assets/images/events/qtw2027/`:

- `banner.png` (or `.jpg`): the banner of the cards and of the event page. It is shown on a dark blue background, so a logo on a dark or transparent background looks best;
- the partner logos listed in `logos`.

**Step 3 (optional): the programme.** One block per day, with talks and breaks; abstracts become "Abstract" buttons that open in place. Group members among the speakers are linked to their page. Put the times in quotes.

```yaml
program:
  - date: 2027-03-10
    slots:
      - time: "9:00 - 9:30"
        break: Registration
      - time: "9:30 - 10:20"
        speaker: Maria Rossi
        title: Title of the talk
        abstract: >-
          The abstract of the talk.
      - time: "10:20 - 10:50"
        break: Coffee break
  - date: 2027-03-11
    slots:
      - time: "9:00 - 9:50"
        speaker: John Smith
        title: Another talk
```

### Add a seminar

```yaml
title: "Seminar: Quantum batteries"
kind: seminar
start: 2026-11-05T15:00:00
speaker: Maria Rossi
venue: Aula Majorana, Department of Physics and Chemistry
city: Palermo, Italy
description: |
  Abstract of the talk.
```

Name the file after the date and speaker, e.g. `data/events/seminar-2026-11-rossi.yaml`. A seminar is shown under "Upcoming" (and on the home page) until its day, and always in the "Seminars" list.

The **group calendar** at the bottom of the Events page is the Outlook calendar of the group (its address is `calendarICS` in `hugo.toml`): seminars added there appear on the site automatically, without touching the website. Add a file here when you also want a page for the seminar.

### Update or remove an event

- Postponed, new link, new programme: edit the file.
- Remove: delete `data/events/<id>.yaml` and the folder `assets/images/events/<id>/`.

---

## Publishing the site

```sh
hugo --gc --minify --cleanDestinationDir
rsync -avuzh ./public/ salvatore.lorenzo@sftp.unipa.it:/mnt/home/salvatore.lorenzo/www-quantum
```

The first command builds the whole site into `public/`, the second copies it to the university server. Then commit the changes to git.

The addresses of the old site (`/author/…`, `/publication/…`, `/research_lines/…`, `/news/…`, `/join_us/`…) redirect to the new pages. `rsync` without `--delete` leaves the files of the old site on the server; to remove them, add `--delete` once (it deletes everything on the server that isn't in `public/`).

---

## How the site works

Built with [Hugo](https://gohugo.io) (extended edition, 0.128 or later) and nothing else: no theme, no Go modules, no Node.

### The database

`data/` is a small database: each folder is a table, each file a record, and the file name is the record's id.

| Table | One file per | Page |
|---|---|---|
| `data/people/` | group member, current or former | `/people/<id>/` |
| `data/publications/` | paper or preprint | `/publications/<id>/` |
| `data/research/` | research line | `/research/<id>/` |
| `data/projects/` | funded project | `/projects/<id>/` |
| `data/events/` | conference, workshop, school, course, seminar | `/events/<id>/` |
| `data/funders.yaml` | (one list) logos at the bottom of the home page | — |

The pages are generated from the records (`content/*/_content.gotmpl`), and the links between records are computed at every build:

- **authors → people**: an author is linked to a member when the name matches the member's `name` or one of the `aliases`;
- **publications → research lines**: the `research` field. Research pages list their papers and the members with at least two of them; people pages show the research lines of their papers;
- **projects → people, research lines**: the `team` and `research` fields.

**Research lines** (`data/research/<id>.yaml`): `title`, `short` (label of the chips), `order`, `summary` (one sentence for the cards), `body`, `keywords` (used to suggest the research lines of new papers), `image_caption`; image `assets/images/research/<id>.*`.
**Projects** (`data/projects/<id>.yaml`): `title`, `acronym`, `programme`, `date` (for ordering), `website`, `team`, `research`, `body`, `figures`, `funding_logos`; images in `assets/images/projects/<id>/`, the card logo is `logo.*`.
**Text pages**: home page text `content/_index.md`, Join us `content/join.md`, section introductions `content/<section>/_index.md`. Menu, email, address, map and calendar: `hugo.toml`.

### Checks

Every build checks the database. A required field that is missing or a link to a record that doesn't exist stops the build with a message naming the file to fix, for example:

```
ERROR data/publications/rossi-2026-test.yaml: unknown research line "thermos" (see data/research/)
ERROR data/people/maria-rossi.yaml: group "PhD" is not one of [faculty postdoc phd student]
```

### Files

```
data/               the database
content/            text pages; the _content.gotmpl files generate the pages of each table
layouts/            HTML templates; layouts/partials/db/ holds the database logic and checks
assets/css, js      style and scripts (light/dark theme, publication filters, copy BibTeX)
assets/images/      images, resized and converted to WebP at build time
static/             copied as is: fonts (Jura for text and headings, OFL licence; Inter and Manrope unused), KaTeX, favicon
python/             the publication pipeline; sitedb.py reads and writes the database;
                    migrate_legacy.py converted the old HugoBlox site (one-off)
                    hero_orbits.py draws the orbits behind the home-page title
bibtexs/            the .bib files already imported by the pipeline
QuniPa_Logo/        the logo package (all versions, guidelines, colours); assets/images/logo.svg (horizontal) and
                    logo-mark.svg (emblem) come from it, coloured through the --logo-* CSS variables for light and
                    dark; static/favicon.* and apple-touch-icon.png come from its web-icons/
```
