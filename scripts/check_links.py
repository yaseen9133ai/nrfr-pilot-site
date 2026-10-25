"""Check the page's links and every pilot path and place it names (PROGRESS.md, Step 5, check 2).

  links     every in-page link (href="#...") points to an id on the page.
  images    every <img> is a file in site/ and sits inside a link to its own
            full-size file (Step 5 decision 5).
  paths     every pilot path on the page (elements marked data-notag="file
            name") exists in the pilot; {1,2,3} and * are expanded. A short
            name that is not in the pilot's top folder must be in exactly
            one of the folders that the page's other paths name (for example
            firm2_mills.csv in data/interim/); in none or in several = fail.
  places    what a "Details in the pilot" line names inside a file, right
            after its path, exists there:
              §1, §7.5 and §8       numbered headings (the findings report)
              (Scope, Features)     headings that contain each name
              (Steps 4–9)           a "Step N" heading for each step
              (Issues of Steps 2–9) the word "Issues" under each of those headings
              (R057)                a row whose first cell is the review ID
              (rows starting “X”)   a row whose first cell starts with X
            A bracket anywhere else in the line fails, so a new form cannot
            pass unchecked.

Pilot path: PILOT_DIR (default ../nrfr-pilot, relative to nrfr-pilot-site/).
--site DIR checks another copy of the page (a folder that holds index.html
and assets/, for example a downloaded copy of the live page); default site/.
Reads only: pilot files are opened for reading, no pilot code is run or
imported. Exit 0 = pass, 1 = a problem, 2 = setup error.

Python standard library only.
"""

import argparse
import csv
import io
import os
import re
import sys
from html.parser import HTMLParser
from pathlib import Path

SITE = Path(__file__).resolve().parent.parent
DEFAULT_ROOT = SITE / 'site'


def pilot_root():
    raw = os.environ.get('PILOT_DIR') or '../nrfr-pilot'
    p = Path(raw)
    if not p.is_absolute():
        p = SITE / raw
    return p.resolve()


class Page(HTMLParser):
    """Ids, links, images, and the file names in document order. A "Details in the pilot" line is
    kept as a list of ('path', name) and ('text', words) parts."""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.ids, self.hrefs, self.imgs, self.names, self.details = set(), [], [], [], []
        self.a_stack, self.name, self.in_details = [], None, False

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if a.get('id'):
            self.ids.add(a['id'])
        if tag == 'a':
            self.a_stack.append(a.get('href'))
            if a.get('href'):
                self.hrefs.append((a['href'], self.getpos()[0]))
        if tag == 'img':
            self.imgs.append((a.get('src') or '', self.a_stack[-1] if self.a_stack else None, self.getpos()[0]))
        if tag == 'p' and a.get('class') == 'details':
            self.in_details = True
            self.details.append([])
        if a.get('data-notag') == 'file name':
            self.name = [tag, '', self.getpos()[0]]

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)
        if tag == 'a':
            self.a_stack.pop()

    def handle_endtag(self, tag):
        if self.name and tag == self.name[0]:
            self.names.append((self.name[1], self.name[2]))
            if self.in_details:
                self.details[-1].append(('path', self.name[1]))
            self.name = None
        if tag == 'a' and self.a_stack:
            self.a_stack.pop()
        if tag == 'p':
            self.in_details = False

    def handle_data(self, d):
        if self.name:
            self.name[1] += d
        elif self.in_details:
            self.details[-1].append(('text', d))


def expand(pilot, rel):
    """The pilot files a page path stands for; [] if none."""
    rels = [rel.replace('{1,2,3}', d) for d in '123'] if '{1,2,3}' in rel else [rel]
    out = []
    for r in rels:
        hits = sorted(pilot.glob(r)) if '*' in r else ([pilot / r] if (pilot / r).exists() else [])
        if not hits:
            return []
        out += hits
    return out if all(h.resolve().is_relative_to(pilot) for h in out) else []


def resolve(pilot, names):
    """Each page name -> its pilot path (relative), or None. A short name that is not in the top
    folder is looked for in the folders of the page's other paths, and must be in exactly one."""
    folders = sorted({n.strip() if n.strip().endswith('/') else n.strip().rsplit('/', 1)[0] + '/'
                      for n, _ in names if '/' in n})
    out = []
    for name, line in names:
        rel = name.strip()
        if '/' not in rel and not expand(pilot, rel):
            found = [f + rel for f in folders if expand(pilot, f + rel)]
            rel = found[0] if len(found) == 1 else None
        out.append((name.strip(), rel if rel and expand(pilot, rel) else None, line))
    return out


def headings(text):
    return [(len(m[1]), m[2].strip(), m.start()) for m in re.finditer(r'^(#{1,6}) (.+)$', text, flags=re.M)]


def step_section(text, n):
    """The text under the heading "Step n" (up to the next heading of the same or a higher level)."""
    hs = headings(text)
    for i, (level, title, start) in enumerate(hs):
        if re.match(rf'Step {n}\b', title):
            end = next((s for lv, _, s in hs[i + 1:] if lv <= level), len(text))
            return text[start:end]
    return None


def first_cells(path):
    rows = list(csv.reader(io.StringIO(path.read_text(encoding='utf-8'))))
    return [r[0] for r in rows[1:] if r]


def step_range(s):
    m = re.fullmatch(r'(\d+)–(\d+)', s)
    return list(range(int(m[1]), int(m[2]) + 1)) if m else [int(s)]


def check_place(path, what):
    """Problems with one named place inside one pilot file ([] = found)."""
    rel = path.name
    if what.startswith('§'):
        if path.suffix != '.md':
            return [f'{rel}: {what} named in a file that is not markdown']
        num = what[1:]
        ok = any(re.match(re.escape(num) + r'\.?\s', t) for _, t, _ in headings(path.read_text(encoding='utf-8')))
        return [] if ok else [f'{rel}: no heading numbered {num}']
    if re.fullmatch(r'R\d{3}', what):
        return [] if what in first_cells(path) else [f'{rel}: no row for {what}']
    m = re.fullmatch(r'rows starting “(.+)”', what)
    if m:
        return [] if any(c.startswith(m[1]) for c in first_cells(path)) else [f'{rel}: no row starting {m[1]!r}']
    text = path.read_text(encoding='utf-8')
    m = re.fullmatch(r'Issues of Steps? ([\d–]+)', what)
    if m:
        out = []
        for n in step_range(m[1]):
            sec = step_section(text, n)
            if sec is None or not re.search(r'\bIssues\b', sec):
                out.append(f'{rel}: no "Issues" under Step {n}')
        return out
    m = re.fullmatch(r'Steps? ([\d–]+)', what)
    if m:
        return [f'{rel}: no heading "Step {n}"' for n in step_range(m[1]) if step_section(text, n) is None]
    titles = [t for _, t, _ in headings(text)]
    return [f'{rel}: no heading with {w!r}' for w in (x.strip() for x in what.split(','))
            if not any(re.search(r'\b' + re.escape(w) + r'\b', t) for t in titles)]


def details_places(pilot, line, resolved):
    """The places named right after each path of one "Details in the pilot" line."""
    places, problems = [], []
    for i, (kind, value) in enumerate(line):
        if kind != 'path':
            continue
        rel = resolved.get(value.strip())
        nxt = next((j for j in range(i + 1, len(line)) if line[j][0] == 'path'), len(line))
        tail = ''.join(v for _, v in line[i + 1:nxt])
        named = []
        m = re.match(r'\s*((?:§\d+(?:\.\d+)?(?:,\s*|\s+and\s+)?)+)', tail)
        if m:
            named += re.findall(r'§\d+(?:\.\d+)?', m[1])
            tail = tail[m.end():]
        m = re.match(r'\s*\(([^()]*)\)', tail)
        if m:
            named.append(m[1].strip())
            tail = tail[m.end():]
        if '(' in tail or ')' in tail:
            problems.append(f'details line: a bracket that does not follow a path: {tail.strip()!r}')
        for what in named:
            if rel is None:
                continue
            for f in expand(pilot, rel):
                places.append((f'{f.relative_to(pilot).as_posix()} {what}', check_place(f, what)))
    return places, problems


def main():
    ap = argparse.ArgumentParser(description=__doc__.split('\n')[0])
    ap.add_argument('--site', default=str(DEFAULT_ROOT), help='folder with index.html and assets/ (default site/)')
    root = Path(ap.parse_args().site).resolve()
    index = root / 'index.html'
    pilot = pilot_root()
    if not index.is_file():
        print(f'ERROR: index.html not found in {root}.')
        return 2
    if not pilot.is_dir():
        print(f'ERROR: pilot folder not found (PILOT_DIR: {pilot}).')
        return 2
    page = Page()
    page.feed(index.read_text(encoding='utf-8'))
    problems = []
    # links
    internal = [(h, line) for h, line in page.hrefs if h.startswith('#')]
    for h, line in internal:
        if h[1:] not in page.ids:
            problems.append(f'index.html line {line}: link to a missing id: {h}')
    print(f'In-page links: {len(internal)} ({len({h for h, _ in internal})} targets).')
    # images
    for src, href, line in page.imgs:
        if not (root / src).is_file():
            problems.append(f'index.html line {line}: image not in the page folder: {src}')
        if href != src:
            problems.append(f'index.html line {line}: {src} does not sit inside a link to its own file')
    print(f'Images: {len(page.imgs)}, each checked for its file and its link to the full-size file.')
    # paths
    resolved = resolve(pilot, page.names)
    distinct = {}
    for name, rel, line in resolved:
        distinct.setdefault(name, rel)
        if rel is None:
            problems.append(f'index.html line {line}: pilot path not found: {name}')
    files = {name: len(expand(pilot, rel)) for name, rel in distinct.items() if rel}
    short = sorted(n for n, rel in distinct.items() if rel and rel != n)
    print(f'Pilot paths named on the page: {len(resolved)} ({len(distinct)} distinct, standing for '
          f'{sum(files.values())} pilot files and folders); short names found in a folder named on the page: '
          f'{len(short)}.')
    # places in "Details in the pilot" lines
    rel_by_name = {name: rel for name, rel, _ in resolved}
    nplaces = 0
    for line in page.details:
        places, probs = details_places(pilot, line, rel_by_name)
        problems += probs
        for where, probs_ in places:
            nplaces += 1
            problems += probs_
    print(f'"Details in the pilot" lines: {len(page.details)}; places named in them, checked file by file: {nplaces}.')
    for p in problems:
        print(f'FAIL: {p}')
    print('Result: ' + ('PASS' if not problems else 'FAIL'))
    return 1 if problems else 0


if __name__ == '__main__':
    sys.exit(main())
