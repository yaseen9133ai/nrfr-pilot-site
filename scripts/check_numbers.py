"""Check build/site_data.json against the pilot, independently of extract.py.

This script does not import or reuse extract.py. It re-reads the spec
(docs/number_sources.csv, docs/caveats.csv) and every pilot source with its
own parsing code (regular expressions over whole sections, csv.reader rows,
its own number formatting), and compares the result with site_data.json:

  numbers   every spec row: the raw value read from the source again; the
            spec's expected value; display (Step 2 decision 5); unit and its
            source; the tag (file, locator, column); tag_required; caveats.
            No entry may be missing, extra, reordered or untagged.
  rules     decision 5 (forest-loss caveat on every forest-loss number, the
            Sarawak wording in section 5), decision 6 (ENCORE licence, UML
            caveat), decision 4 (only the listed reasons may skip a tag).
  lists     every text field re-read from its tag; each list complete and in
            the source's order (firms, sources, attributions, mills, features,
            gaps, pending decisions, decision options, full-build changes).
  inputs    the SHA-256 of every pilot file read equals the file now; the
            spec hashes equal the docs files now.
  page      site/index.html (Step 4; Step 3 decisions 1-6), read with its own
            HTML parser:
            - every element with data-id: its file, locator, column and raw
              value equal the spec and the source read again; its text equals
              the page form (decision 5 display, "+" only on rainfall
              anomalies, dates for readers, en dash in year ranges, number
              words as digits, unit after a no-break space except %, FFB unit
              without spaces and the printed unit in data-unit-raw); its
              caveats equal the spec, and each is listed in the same block;
            - every element with data-file and no data-id (text quoted from
              the pilot): its text equals the source read again;
            - every data-notag element: an allowed reason, and text of the
              form that reason allows; every data-meta element (appendix):
              equal to the spec field or the source value it names;
            - every data-caveat element: equal to docs/caveats.csv;
            - every note listed in a block is needed there (Step 5 decision
              7): by a number in the block (its spec caveats) or by an
              element that declares it with data-needs; data-needs is
              allowed only on an image (figure), a feature card (article)
              or a missing value (class "missing"), must name a caveat of
              docs/caveats.csv and must be listed in its block; the
              appendix block lists every caveat of docs/caveats.csv;
            - any other digit in the page text or in alt, title or
              aria-label text = untagged number; number words such as "three"
              = fail (decision 6); every spec number appears on the page.

Pilot path: PILOT_DIR (default ../nrfr-pilot, relative to nrfr-pilot-site/).
Reads only. Writes the report to build/check_numbers_report.txt. --no-html
skips the page part (for example before the page is built).
Exit 0 = all pass, 1 = at least one failure, 2 = setup error.

Python standard library only.
"""

import argparse
import csv
import hashlib
import io
import json
import os
import re
import sys
from decimal import Decimal
from html.parser import HTMLParser
from pathlib import Path

SITE = Path(__file__).resolve().parent.parent
DEFAULT_DATA = SITE / 'build' / 'site_data.json'
DEFAULT_SPEC = SITE / 'docs' / 'number_sources.csv'
DEFAULT_CAVEATS = SITE / 'docs' / 'caveats.csv'
DEFAULT_REPORT = SITE / 'build' / 'check_numbers_report.txt'
DEFAULT_HTML = SITE / 'site' / 'index.html'
ALLOWED_NO_TAG = ('review ID', 'step number', 'section number', 'year label', 'date', 'version',
                  'file name', 'ISIC code', 'licence version', 'name or identifier')


class Miss(Exception):
    """A value that cannot be located exactly once."""


def pilot_root():
    raw = os.environ.get('PILOT_DIR') or '../nrfr-pilot'
    p = Path(raw)
    if not p.is_absolute():
        p = SITE / raw
    return p.resolve()


# ------------------------------------------------------------ reading files

class Files:
    def __init__(self, root):
        self.root = root
        self.digest = {}
        self.cache = {}

    def raw(self, rel):
        if rel not in self.cache:
            path = (self.root / rel).resolve()
            if self.root not in path.parents or not path.is_file():
                raise Miss(f'{rel}: no such file in the pilot')
            blob = path.read_bytes()
            self.digest[rel] = hashlib.sha256(blob).hexdigest()
            self.cache[rel] = blob.decode('utf-8')
        return self.cache[rel]

    def table(self, rel):
        """(header list, list of row lists) via csv.reader."""
        key = ('csv', rel)
        if key not in self.cache:
            rows = list(csv.reader(io.StringIO(self.raw(rel), newline='')))
            self.cache[key] = (rows[0], rows[1:])
        return self.cache[key]


COND = re.compile(r'^(?P<col>[A-Za-z_][\w ]*?)(?P<op>!\^=|\^=|\$=|!=|=)(?P<val>.*)$')


def conditions(text):
    out = []
    for piece in re.split(r'; ', text):
        m = COND.match(piece)
        if not m:
            raise Miss(f'unreadable condition {piece!r}')
        out.append((m['col'], m['op'], m['val']))
    return out


def holds(cell, op, val):
    options = val.split('|')
    return {
        '=': lambda: cell == val,
        '!=': lambda: cell != val,
        '^=': lambda: any(cell[:len(o)] == o for o in options),
        '!^=': lambda: all(cell[:len(o)] != o for o in options),
        '$=': lambda: any(len(cell) >= len(o) and cell[len(cell) - len(o):] == o for o in options),
    }[op]()


def select(files, rel, key):
    header, rows = files.table(rel)
    if key == '*':
        return header, rows
    conds = conditions(key)
    idx = {}
    for col, _, _ in conds:
        if col not in header:
            raise Miss(f'{rel}: column {col!r} not in header')
        idx[col] = header.index(col)
    return header, [r for r in rows if all(holds(r[idx[c]], op, v) for c, op, v in conds)]


def single(rows, what):
    if len(rows) == 0:
        raise Miss(f'{what}: no row')
    if len(rows) > 1:
        raise Miss(f'{what}: {len(rows)} rows (ambiguous)')
    return rows[0]


def cell(files, rel, key, column):
    header, rows = select(files, rel, key)
    if column not in header:
        raise Miss(f'{rel}: column {column!r} not in header')
    return single(rows, f'{rel} [{key}]')[header.index(column)]


def is_digit(ch):
    return ch.isdigit()


def whole_token_count(text, value):
    """How often value occurs in text without being part of a longer number or word."""
    count = 0
    for m in re.finditer('(?=' + re.escape(value) + ')', text):
        a, b = m.start(), m.start() + len(value)
        prev = text[a - 1] if a else ''
        prev2 = text[a - 2] if a > 1 else ''
        nxt = text[b] if b < len(text) else ''
        nxt2 = text[b + 1] if b + 1 < len(text) else ''
        first, last = value[0], value[-1]
        if first.isdigit() and (is_digit(prev) or (prev in ('.', ',') and prev and is_digit(prev2))):
            continue
        if first.isalpha() and prev and prev.isalnum():
            continue
        if last.isdigit() and (is_digit(nxt) or (nxt in ('.', ',') and nxt and is_digit(nxt2))):
            continue
        if last.isalpha() and nxt and nxt.isalnum():
            continue
        count += 1
    return count


QUOTED = re.compile(r'^text(?: in (?P<col>.+?))?: "(?P<q>.*)"$')


def check_quote(container, quote, value, what):
    n = len(re.findall(re.escape(quote), container))
    if n != 1:
        raise Miss(f'{what}: quote occurs {n} times')
    k = whole_token_count(quote, value)
    if k != 1:
        raise Miss(f'{what}: {value!r} occurs {k} times in the quote as a whole token')
    return value


def from_csv(files, src, key, comp, expected):
    names = [src.replace('{1,2,3}', d) for d in '123'] if '{1,2,3}' in src else [src]
    if key == 'header':
        if comp != 'count(columns)':
            raise Miss(f'{src}: header only supports count(columns)')
        return str(len(files.table(names[0])[0]))
    picked = []
    header = None
    for n in names:
        header, rows = select(files, n, key)
        picked.extend((header, r) for r in rows)
    if comp == 'count(rows)':
        return str(len(picked))
    m = re.match(r'^count\(distinct (.+)\)$', comp)
    if m:
        return str(len(set(r[h.index(m[1])] for h, r in picked)))
    m = re.match(r'^(sum|min|max)\((.+)\)$', comp)
    if m:
        vals = [r[h.index(m[2])] for h, r in picked]
        if m[1] == 'sum':
            return str(sum(Decimal(v) for v in vals))
        chooser = min if m[1] == 'min' else max
        return chooser(vals, key=Decimal)
    q = QUOTED.match(comp)
    if q and q['col']:
        return check_quote(cell(files, names[0], key, q['col']), q['q'], expected, f'{src} [{key}] {q["col"]}')
    return cell(files, names[0], key, comp)


# ------------------------------------------------------------ markdown

def strip_marks(s):
    return re.sub(r'\*\*|`', '', s).strip()


def md_sections(text):
    """{heading line: [section texts]} with fenced code blanked out."""
    text = re.sub(r'^[ \t]*```.*?^[ \t]*```[^\n]*$', lambda m: '\n' * m.group(0).count('\n'),
                  text, flags=re.M | re.S)
    heads = list(re.finditer(r'^(#{1,6} \S[^\n]*?)[ \t]*$', text, flags=re.M))
    out = {}
    for i, h in enumerate(heads):
        end = heads[i + 1].start() if i + 1 < len(heads) else len(text)
        out.setdefault(h.group(1), []).append(text[h.end():end])
    return out


def cells_of(line):
    s = line.strip()
    s = s[1:] if s[:1] == '|' else s
    s = s[:-1] if s[-1:] == '|' and s[-2:] != '\\|' else s
    parts, buf, esc = [], '', False
    for ch in s:
        if esc:
            buf += ch
            esc = False
        elif ch == '\\':
            buf += ch
            esc = True
        elif ch == '|':
            parts.append(buf.strip())
            buf = ''
        else:
            buf += ch
    parts.append(buf.strip())
    return parts


ITEM = re.compile(r'^([ \t]*)(?:[-*+]|(\d+)\.)[ \t]+(.*)$')


def section_parts(body):
    """Tables, list items and paragraphs of one section body."""
    tables, items, paras = [], [], []
    for chunk in re.split(r'\n[ \t]*\n', body):
        lines = [ln for ln in chunk.split('\n') if ln.strip()]
        tbl, para = [], []
        for ln in lines + [None]:
            is_tbl = ln is not None and ln.lstrip().startswith('|')
            m = ITEM.match(ln) if ln is not None and not is_tbl else None
            if not is_tbl and tbl:
                tables.append(tbl)
                tbl = []
            if (ln is None or is_tbl or m) and para:
                paras.append(' '.join(para))
                para = []
            if ln is None:
                break
            if is_tbl:
                tbl.append(ln.strip())
            elif m:
                items.append({'indent': len(m.group(1)), 'numbered': m.group(2) is not None, 'text': m.group(3)})
            else:
                para.append(ln.strip())
    return tables, items, paras


def table_rows(lines, what):
    if len(lines) < 2 or not re.fullmatch(r'\|?[\s:|-]+\|?', lines[1]):
        raise Miss(f'{what}: no table separator')
    head = [strip_marks(c) for c in cells_of(lines[0])]
    rows = []
    for ln in lines[2:]:
        cs = cells_of(ln)
        if len(cs) != len(head):
            raise Miss(f'{what}: ragged table row')
        rows.append(dict(zip(head, cs)))
    return head, rows


def md_locate(files, src, locator):
    if ' | ' not in locator:
        raise Miss(f'{src}: locator has no block part: {locator!r}')
    heading, block = locator.split(' | ', 1)
    found = md_sections(files.raw(src)).get(heading, [])
    if len(found) != 1:
        raise Miss(f'{src}: heading {heading!r} occurs {len(found)} times')
    tables, items, paras = section_parts(found[0])
    what = f'{src} [{locator}]'
    first, *filters = block.split('; ')
    if first == 'table' or first.startswith('row='):
        if len(tables) != 1:
            raise Miss(f'{what}: {len(tables)} tables')
        head, rows = table_rows(tables[0], what)
        if first == 'table':
            conds = conditions('; '.join(filters)) if filters else []
            for c, _, _ in conds:
                if c not in head:
                    raise Miss(f'{what}: no column {c!r}')
            return ('rows', [r for r in rows if all(holds(strip_marks(r[c]), op, v) for c, op, v in conds)])
        want = first[4:]
        return ('row', single([r for r in rows if strip_marks(r[head[0]]) == want], what))
    if filters:
        raise Miss(f'{what}: filters on a non-table block')
    if first == 'heading':
        return ('text', re.sub(r'^#+\s*', '', heading))
    if first == 'numbered list':
        return ('items', [i for i in items if i['numbered'] and i['indent'] == 0])
    if first.startswith('bullet='):
        lab = first[len('bullet='):]
        return ('text', single([i['text'] for i in items if strip_marks(i['text']).startswith(lab)], what))
    if first.startswith('paragraph='):
        lab = first[len('paragraph='):]
        return ('text', single([p for p in paras if strip_marks(p).startswith(lab)], what))
    m = re.fullmatch(r'paragraph (\d+)', first)
    if m:
        k = int(m[1])
        if k < 1 or k > len(paras):
            raise Miss(f'{what}: no paragraph {k}')
        return ('text', paras[k - 1])
    raise Miss(f'{what}: unknown block')


def from_md(files, src, locator, comp, expected):
    kind, got = md_locate(files, src, locator)
    what = f'{src} [{locator}]'
    if kind in ('rows', 'items'):
        if comp != {'rows': 'count(rows)', 'items': 'count(items)'}[kind]:
            raise Miss(f'{what}: wrong computation {comp!r}')
        return str(len(got))
    q = QUOTED.match(comp)
    if kind == 'row':
        if q:
            if not q['col'] or q['col'] not in got:
                raise Miss(f'{what}: quote needs an existing column')
            return check_quote(got[q['col']], q['q'], expected, what)
        if comp not in got:
            raise Miss(f'{what}: no column {comp!r}')
        return strip_marks(got[comp])
    if not q or q['col']:
        raise Miss(f'{what}: needs text: "<quote>"')
    return check_quote(got, q['q'], expected, what)


def source_value(files, src, locator, comp, expected):
    if src[-3:] == '.md':
        return from_md(files, src, locator, comp, expected)
    if src[-4:] == '.csv':
        return from_csv(files, src, locator, comp, expected)
    raise Miss(f'{src}: unsupported file type')


def shown(raw, fmt):
    """Decision 5, written differently from extract.py on purpose."""
    if fmt == 'as_is':
        return raw
    m = re.fullmatch(r'(-?)([\d,]+)((?:\.\d+)?)', raw)
    if not m or not re.fullmatch(r'\d+|\d{1,3}(,\d{3})+', m[2]):
        raise Miss(f'not a plain number: {raw!r}')
    return ('−' if m[1] else '') + format(int(m[2].replace(',', '')), ',') + m[3]


def text_field(files, f):
    """Re-read a list field from its tag; return the value found."""
    src, loc, col = f['file'], f['locator'], f['column']
    if src[-4:] == '.csv':
        q = QUOTED.match(col)
        if q and q['col']:
            container = cell(files, src, loc, q['col'])
            if len(re.findall(re.escape(q['q']), container)) != 1:
                raise Miss(f'{src} [{loc}] {q["col"]}: wording not found exactly once')
            return q['q']
        return cell(files, src, loc, col)
    kind, got = md_locate(files, src, loc)
    if kind == 'row':
        if col not in got:
            raise Miss(f'{src} [{loc}]: no column {col!r}')
        return strip_marks(got[col])
    if kind == 'text' and col == 'text':
        return strip_marks(got)
    raise Miss(f'{src} [{loc}]: cannot read {col!r}')


# ------------------------------------------------------------ the page

MONTH_NAMES = ('January February March April May June July August September October November December').split()
NOTAG_FORMS = {
    'review ID': r'R\d{3}',
    'step number': r'(?:[Ss]teps? )?\d{1,2}(?:–\d{1,2})?',
    'section number': r'(?:§|[Ss]ection )?\d{1,2}(?:\.\d{1,2})?',
    'year label': r'(?:19|20)\d\d(?:–(?:19|20)\d\d)?',
    'date': r'(?:\d{1,2} )?(?:' + '|'.join(MONTH_NAMES) + r')(?: \d{4})?(?:, [0-9]{2}:[0-9]{2}:[0-9]{2} UTC)?',
    'version': r'(?:[A-Za-z]+-\d{4}-)?v?\d+(?:\.\d+)*',
    'file name': r'[\w.{}*,/-]*(?:\.(?:csv|md|py|sh|txt|png|json|geojson|gpkg)|/)',
    'ISIC code': r'[A-Z](?:_\d+)+',
    'licence version': r'CC BY(?:-SA)? \d\.\d|ODbL \d\.\d',
    'name or identifier': r'Sentinel-\d|UTM \d\d[NS]|Note \d{1,3}|HTTP \d{3}|AR \d{4}|EPSG:[0-9]{4,5}|ADM\d|SHA-256',
}
NUMBER_WORDS = re.compile(r'\b(?:one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve|thirteen|fourteen|'
                          r'fifteen|sixteen|seventeen|eighteen|nineteen|twenty|thirty|forty|fifty|sixty|seventy|'
                          r'eighty|ninety|hundred|thousand|million|billion|dozen|twice|thrice)\b', re.I)
WORD_DIGITS = {w: str(i) for i, w in enumerate('one two three four five six seven eight nine ten eleven twelve'.split(), 1)}
VOID = {'area', 'base', 'br', 'col', 'embed', 'hr', 'img', 'input', 'link', 'meta', 'source', 'track', 'wbr'}
TEXT_ATTRS = ('alt', 'title', 'aria-label', 'placeholder')
NEEDS_HOSTS = ('figure', 'article')   # and any element of class "missing"
APPENDIX_BLOCK = 'appendix'


def for_readers(raw):
    """A date as the page writes it; independent of build_page.py."""
    # [0-9] after a colon, so this text does not look like a Windows path to scan_exclusions.py
    m = re.match(r'^(\d{4})-(\d\d)-(\d\d)(T([0-9]{2}:[0-9]{2}:[0-9]{2})Z)?$', raw)
    if m:
        out = '%d %s %s' % (int(m[3]), MONTH_NAMES[int(m[2]) - 1], m[1])
        return out + (', %s UTC' % m[5] if m[4] else '')
    m = re.match(r'^(\d{1,2}) ([A-Z][a-z][a-z]) (\d{4})$', raw)
    if m:
        hits = [x for x in MONTH_NAMES if x.startswith(m[2])]
        if len(hits) == 1:
            return '%s %s %s' % (m[1], hits[0], m[3])
    return raw


def page_form(row, raw, unit):
    if row['format'] == 'number':
        s = shown(raw, 'number')
        if row['label'].startswith('Rainfall anomaly (mm)') and not s.startswith('−'):
            s = '+' + s
    elif row['tag_required'] == 'no: date':
        s = for_readers(raw)
    elif row['tag_required'] == 'no: year label':
        s = raw.replace('-', '–')
    else:
        s = re.sub(r'(?i)\b(' + '|'.join(WORD_DIGITS) + r')\b', lambda m: WORD_DIGITS[m[1].lower()], raw)
    if unit:
        s = s + (unit if unit == '%' else '\u00a0' + unit)
    return s


class Page(HTMLParser):
    """Collects tagged elements (contexts), loose text and attribute text, with the enclosing data-block."""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.stack, self.ctx, self.loose, self.attr_text, self.problems, self.needs = [], [], [], [], [], []

    def _attr_text(self, tag, a):
        for k in TEXT_ATTRS:
            if a.get(k):
                self.attr_text.append((f'<{tag} {k}>', a[k], self.getpos()[0]))

    def handle_starttag(self, tag, attrs):
        a = {k: (v if v is not None else '') for k, v in attrs}
        self._attr_text(tag, a)
        if 'data-needs' in a:
            self.needs.append({'tag': tag, 'a': a, 'block': a.get('data-block') or self.block(),
                               'line': self.getpos()[0]})
        if tag in VOID:
            return
        kind = None
        for key, k in (('data-id', 'number'), ('data-notag', 'notag'), ('data-meta', 'meta'),
                       ('data-caveat', 'caveat'), ('data-file', 'text')):
            if key in a:
                kind = k
                break
        idx = None
        if kind:
            idx = len(self.ctx)
            self.ctx.append({'kind': kind, 'a': a, 'parts': [], 'block': self.block(),
                             'line': self.getpos()[0], 'inside': self.inner()})
        self.stack.append((tag, idx, a.get('data-block')))

    def handle_startendtag(self, tag, attrs):
        self._attr_text(tag, {k: (v or '') for k, v in attrs})

    def handle_endtag(self, tag):
        for i in range(len(self.stack) - 1, -1, -1):
            if self.stack[i][0] == tag:
                del self.stack[i:]
                return
        self.problems.append(f'line {self.getpos()[0]}: </{tag}> without an opening tag')

    def inner(self):
        for _, idx, _ in reversed(self.stack):
            if idx is not None:
                return idx
        return None

    def block(self):
        for _, _, b in reversed(self.stack):
            if b:
                return b
        return None

    def handle_data(self, data):
        if any(t in ('style', 'script') for t, _, _ in self.stack):
            if data.strip():
                self.problems.append(f'line {self.getpos()[0]}: inline style or script element')
            return
        idx = self.inner()
        if idx is not None:
            self.ctx[idx]['parts'].append(data)
        else:
            self.loose.append((data, self.getpos()[0]))


def check_page(html_text, spec, raw_by_id, unit_by_id, cav_text, files, fail, count):
    pg = Page()
    pg.feed(html_text)
    pg.close()
    for p in pg.problems:
        fail('page', 'html', p)
    by_id = {s['id']: s for s in spec}
    notes = {}
    for c in pg.ctx:
        c['text'] = ''.join(c['parts'])
        if c['kind'] == 'caveat':
            count('page notes')
            cid = c['a']['data-caveat']
            if cav_text.get(cid) != c['text']:
                fail('page', f'note {cid} (line {c["line"]})', 'text differs from docs/caveats.csv')
            notes.setdefault(c['block'], set()).add(cid)
    seen = set()
    for c in pg.ctx:
        a, text, where = c['a'], c['text'], f'line {c["line"]}'
        if c['inside'] is not None:
            fail('page', where, f'{c["kind"]} element nested inside another tagged element')
        if c['kind'] == 'number':
            count('page numbers')
            nid = a['data-id']
            row = by_id.get(nid)
            if row is None:
                fail('page', f'{nid} ({where})', 'data-id not in the spec (untraced number)')
                continue
            seen.add(nid)
            if (a.get('data-file'), a.get('data-locator'), a.get('data-column')) != \
                    (row['source_file'], row['row_key'], row['column_or_computation']):
                fail('page', f'{nid} ({where})', 'tag (file, locator, column) differs from the spec')
            if nid not in raw_by_id:
                fail('page', f'{nid} ({where})', 'source could not be read, so the number cannot be checked')
                continue
            if a.get('data-raw') != raw_by_id[nid]:
                fail('page', f'{nid} ({where})', f'data-raw {a.get("data-raw")!r} != source {raw_by_id[nid]!r}')
            unit = unit_by_id.get(nid)
            if row['unit'].startswith('@'):
                if a.get('data-unit-raw') != unit:
                    fail('page', f'{nid} ({where})', 'data-unit-raw differs from the unit cell')
                unit = ''.join((unit or '').split())
            elif 'data-unit-raw' in a:
                fail('page', f'{nid} ({where})', 'data-unit-raw on a fixed unit')
            want = page_form(row, raw_by_id[nid], unit)
            if text != want:
                fail('page', f'{nid} ({where})', f'shows {text!r}; page form is {want!r}')
            want_c = [x for x in row['caveats'].split('; ') if x]
            if a.get('data-caveats', '').split() != want_c:
                fail('page', f'{nid} ({where})', f'data-caveats {a.get("data-caveats")!r} != spec {want_c}')
            if c['block'] is None:
                fail('page', f'{nid} ({where})', 'number outside any data-block')
            for x in want_c:
                if x not in notes.get(c['block'], set()):
                    fail('page', f'{nid} ({where})', f'caveat {x!r} not listed in its block {c["block"]!r}')
        elif c['kind'] == 'text':
            count('page texts')
            f = {'file': a.get('data-file', ''), 'locator': a.get('data-locator', ''), 'column': a.get('data-column', '')}
            try:
                value = text_field(files, f)
            except (Miss, ValueError, IndexError, KeyError) as e:
                fail('page', f'text ({where})', str(e))
                continue
            if a.get('data-form') == 'date':
                want = re.sub(r'\b(\d{4}-\d\d-\d\d)(?!T)\b', lambda m: for_readers(m[1]), value)
                if a.get('data-value') != value or want == value:
                    fail('page', f'text ({where})', 'data-value differs from the source, or no date to rewrite')
            else:
                want = value
            if text != want:
                fail('page', f'text ({where}) {f["file"]} [{f["locator"]}] {f["column"]}',
                     'text differs from the source')
        elif c['kind'] == 'notag':
            count('page no-tag')
            reason = a['data-notag']
            if reason not in NOTAG_FORMS:
                fail('page', where, f'no-tag reason {reason!r} not allowed (decision 4; Step 3 decision 5)')
            elif not re.fullmatch(NOTAG_FORMS[reason], text):
                fail('page', where, f'{text!r} is not of the form allowed for {reason!r}')
        elif c['kind'] == 'meta':
            count('page meta')
            nid, field = a.get('data-for'), a['data-meta']
            row = by_id.get(nid)
            want = None
            if row is not None:
                want = {'label': row['label'], 'file': row['source_file'], 'locator': row['row_key'],
                        'column': row['column_or_computation'], 'raw': raw_by_id.get(nid),
                        'unit_raw': unit_by_id.get(nid) if row['unit'].startswith('@') else None}.get(field)
            if want is None or text != want:
                fail('page', f'meta {nid}.{field} ({where})', 'differs from the spec or the source')
    # the reverse direction: every note in a block is needed there (Step 5 decision 7)
    needed = {}
    for c in pg.ctx:
        row = by_id.get(c['a'].get('data-id')) if c['kind'] == 'number' else None
        if row is not None:
            needed.setdefault(c['block'], set()).update(x for x in row['caveats'].split('; ') if x)
    for e in pg.needs:
        count('page named notes')
        where = f'line {e["line"]} <{e["tag"]} data-needs>'
        if e['tag'] not in NEEDS_HOSTS and 'missing' not in e['a'].get('class', '').split():
            fail('page', where, 'data-needs is allowed only on an image (figure), a feature card (article) or a '
                                'missing value')
        ids = e['a']['data-needs'].split()
        if not ids:
            fail('page', where, 'data-needs names no note')
        for x in ids:
            if x not in cav_text:
                fail('page', f'{where} {x}', 'not a caveat of docs/caveats.csv')
            elif x not in notes.get(e['block'], set()):
                fail('page', f'{where} {x}', f'declared, but not listed in its block {e["block"]!r}')
        needed.setdefault(e['block'], set()).update(ids)
    for block, listed in notes.items():
        if block == APPENDIX_BLOCK:
            continue
        for cid in sorted(listed):
            count('page note needs')
            if cid not in needed.get(block, set()):
                fail('page', f'note {cid} in block {block!r}', 'no number or element in the block needs it')
    count('page note needs')
    if notes.get(APPENDIX_BLOCK, set()) != set(cav_text):
        fail('page', f'block {APPENDIX_BLOCK!r}', 'the appendix does not list exactly the caveats of docs/caveats.csv')
    for nid in [s['id'] for s in spec if s['id'] not in seen]:
        fail('page', nid, 'spec number not shown on the page')
    for text, line in pg.loose:
        count('page text runs')
        for m in re.finditer(r'\d', text):
            snippet = text[max(0, m.start() - 25):m.start() + 25].replace('\n', ' ')
            fail('page', f'line {line}', f'untagged digit: ...{snippet}...')
            break
        for m in NUMBER_WORDS.finditer(text):
            fail('page', f'line {line}', f'number written as a word: {m[0]!r} (decision 6)')
    for what, text, line in pg.attr_text:
        if re.search(r'\d', text) or NUMBER_WORDS.search(text):
            fail('page', f'line {line} {what}', f'digit or number word in attribute text: {text!r}')
    return len(seen)


# ------------------------------------------------------------ the checks

def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--data', default=str(DEFAULT_DATA))
    ap.add_argument('--spec', default=str(DEFAULT_SPEC))
    ap.add_argument('--caveats', default=str(DEFAULT_CAVEATS))
    ap.add_argument('--report', default=str(DEFAULT_REPORT))
    ap.add_argument('--html', default=str(DEFAULT_HTML))
    ap.add_argument('--no-html', action='store_true', help='skip the page part')
    args = ap.parse_args()

    root = pilot_root()
    if not root.is_dir():
        print(f'ERROR: pilot folder not found (PILOT_DIR): {root}')
        return 2
    try:
        data = json.loads(Path(args.data).read_text(encoding='utf-8'))
        spec_rows = list(csv.reader(io.StringIO(Path(args.spec).read_text(encoding='utf-8'), newline='')))
        cav_rows = list(csv.reader(io.StringIO(Path(args.caveats).read_text(encoding='utf-8'), newline='')))
    except (OSError, ValueError) as e:
        print(f'ERROR: {e}')
        return 2

    files = Files(root)
    fails = []
    tally = {}

    def fail(area, ident, msg):
        fails.append(f'[{area}] {ident}: {msg}')

    def count(area):
        tally[area] = tally.get(area, 0) + 1

    # caveats file
    ch = cav_rows[0]
    caveats = [dict(zip(ch, r)) for r in cav_rows[1:]]
    cav_ids = [c['id'] for c in caveats]
    want_cav = [{'id': c['id'], 'text': c['text'], 'basis': c['basis']} for c in caveats]
    if data.get('caveats') != want_cav:
        fail('caveats', 'docs/caveats.csv', 'caveat list in site_data.json differs from docs/caveats.csv')
    count('caveats')

    # numbers
    sh = spec_rows[0]
    need = ['id', 'section', 'label', 'source_file', 'row_key', 'column_or_computation',
            'expected_value', 'format', 'unit', 'caveats', 'tag_required']
    if any(c not in sh for c in need):
        print('ERROR: spec header is missing columns')
        return 2
    col = {c: sh.index(c) for c in sh}
    spec = [{c: r[col[c]] for c in need} for r in spec_rows[1:]]
    ids = [s['id'] for s in spec]
    if len(set(ids)) != len(ids):
        fail('numbers', 'spec', 'duplicate ids in the spec')
    got = data.get('numbers', [])
    got_ids = [n.get('id') for n in got]
    for missing in [i for i in ids if i not in got_ids]:
        fail('numbers', missing, 'in the spec but not in site_data.json')
    for extra in [i for i in got_ids if i not in ids]:
        fail('numbers', extra, 'in site_data.json but not in the spec (untraced number)')
    if [i for i in got_ids if i in ids] != [i for i in ids if i in got_ids]:
        fail('numbers', 'order', 'site_data.json is not in spec order')
    by_id = {n.get('id'): n for n in got}
    raw_by_id, unit_by_id = {}, {}

    for s in spec:
        ident = s['id']
        count('numbers')
        n = by_id.get(ident)
        if n is None:
            continue
        try:
            raw = source_value(files, s['source_file'], s['row_key'], s['column_or_computation'],
                               s['expected_value'])
        except (Miss, ValueError, IndexError, KeyError, ArithmeticError) as e:
            fail('numbers', ident, f'source: {e}')
            continue
        raw_by_id[ident] = raw
        if raw != s['expected_value']:
            fail('numbers', ident, f'source now gives {raw!r}; spec expects {s["expected_value"]!r}')
        if n.get('raw') != raw:
            fail('numbers', ident, f'raw in site_data.json {n.get("raw")!r} != source {raw!r}')
        try:
            want_display = shown(raw, s['format'])
        except Miss as e:
            fail('numbers', ident, f'display: {e}')
            want_display = None
        if want_display is not None and n.get('display') != want_display:
            fail('numbers', ident, f'display {n.get("display")!r} != {want_display!r} (decision 5)')
        tagd = n.get('source') or {}
        if not (tagd.get('file') and tagd.get('locator') and tagd.get('column') and n.get('raw') not in (None, '')):
            fail('numbers', ident, 'untagged: file, locator, column or raw value missing (decision 6)')
        if (tagd.get('file'), tagd.get('locator'), tagd.get('column')) != \
                (s['source_file'], s['row_key'], s['column_or_computation']):
            fail('numbers', ident, 'tag differs from the spec')
        for key in ('section', 'label', 'format'):
            if n.get(key) != s[key]:
                fail('numbers', ident, f'{key} differs from the spec')
        # unit
        u = s['unit']
        if u.startswith('@'):
            try:
                usrc, ukey, ucol = u[1:].split(' | ')
                uval = cell(files, usrc, ukey, ucol)
            except (Miss, ValueError) as e:
                fail('numbers', ident, f'unit: {e}')
                uval = None
            else:
                unit_by_id[ident] = uval
                if n.get('unit_source') != {'file': usrc, 'locator': ukey, 'column': ucol, 'raw': uval}:
                    fail('numbers', ident, 'unit tag differs')
        else:
            uval = u
            unit_by_id[ident] = u
            if n.get('unit_source') is not None:
                fail('numbers', ident, 'unit tag present for a fixed unit')
        if uval is not None and n.get('unit') != uval:
            fail('numbers', ident, f'unit {n.get("unit")!r} != {uval!r}')
        # tag rule (decision 4)
        req = s['tag_required']
        if req == 'yes':
            if n.get('tag_required') is not True or n.get('no_tag_reason') is not None:
                fail('numbers', ident, 'tag_required differs from the spec')
        else:
            reason = req[4:] if req[:4] == 'no: ' else ''
            if reason not in ALLOWED_NO_TAG:
                fail('rules', ident, f'no-tag reason {req!r} is not in decision 4')
            if n.get('tag_required') is not False or n.get('no_tag_reason') != reason:
                fail('numbers', ident, 'tag_required differs from the spec')
        # caveats
        want = [c for c in s['caveats'].split('; ') if c]
        if n.get('caveats') != want:
            fail('numbers', ident, f'caveats {n.get("caveats")} != spec {want}')
        for c in want:
            if c not in cav_ids:
                fail('rules', ident, f'caveat {c!r} not defined in docs/caveats.csv')
        lab = s['label'].lower()
        sec = s['section'].split(' ')[0]
        if 'loss' in lab and not s['label'].startswith('Forest loss check'):
            count('rules')
            need_c = 'forest_loss_sarawak' if sec == '5' else 'forest_loss'
            if need_c not in want:
                fail('rules', ident, f'forest-loss number without the {need_c} caveat (decision 5)')
        if 'encore' in lab and 'check' not in lab and sec in ('0', '4', '7', '8'):
            count('rules')
            if 'encore_licence' not in want:
                fail('rules', ident, 'ENCORE number without the CC BY-SA 4.0 caveat (decision 6)')
        if re.search(r'\buml\b|universal mill list', lab):
            count('rules')
            if 'uml_unverified' not in want:
                fail('rules', ident, 'UML number without the UML caveat (decision 6)')

    # lists
    L = data.get('lists', {})

    def verify_fields(name, obj, path):
        if isinstance(obj, dict):
            if {'file', 'locator', 'column', 'value'} <= set(obj):
                count('list fields')
                try:
                    v = text_field(files, obj)
                except (Miss, ValueError, IndexError) as e:
                    fail('lists', f'{name}{path}', str(e))
                    return
                if v != obj['value']:
                    fail('lists', f'{name}{path}', f'value {obj["value"]!r} != source {v!r}')
                return
            for k, v in obj.items():
                verify_fields(name, v, f'{path}.{k}')
        elif isinstance(obj, list):
            for i, v in enumerate(obj):
                verify_fields(name, v, f'{path}[{i}]')

    for name, items in L.items():
        verify_fields(name, items, '')

    def expect(name, cond, msg):
        count('list structure')
        if not cond:
            fail('lists', name, msg)

    F = 'reports/step10_findings.md'

    def safe(name, fn):
        try:
            fn()
        except (Miss, ValueError, KeyError, IndexError, TypeError) as e:
            fail('lists', name, f'cannot check: {e}')

    def firms():
        h, rows = files.table('data/processed/pilot_firm_year.csv')
        order = list(dict.fromkeys(r[h.index('firm_id')] for r in rows))
        expect('firms', [f['firm_id'] for f in L.get('firms', [])] == order, 'firm ids or order differ')

    def sources():
        h, rows = files.table('source_register.csv')
        order = [r[h.index('source_id')] for r in rows]
        got_s = L.get('sources', [])
        expect('sources', [s['source_id'] for s in got_s] == order, 'source ids or order differ')
        for s in got_s:
            expect('sources', s['name']['locator'] == f'source_id={s["source_id"]}', f'{s["source_id"]}: wrong row')

    def attributions():
        for a in L.get('attributions', []):
            if a.get('recorded'):
                expect('attributions', a['wording']['file'] == 'source_register.csv'
                       and a['wording']['locator'] == f'source_id={a["source_id"]}', f'{a["source_id"]}: wrong row')
            else:
                expect('attributions', bool(a.get('note')) and not re.search(r'\d', a['note']),
                       f'{a["source_id"]}: a not-recorded note must be plain words without numbers')

    def mills():
        want = []
        for d in '123':
            src = f'data/interim/firm{d}_mills.csv'
            _, rows = select(files, src, 'in_scope^=yes')
            h = files.table(src)[0]
            want += [r[h.index('mill_id')] for r in rows]
        got_m = L.get('mills', [])
        expect('mills', [m['mill_id'] for m in got_m] == want, 'mill ids or order differ')
        for m in got_m:
            expect('mills', m['name']['locator'] == m['firm']['locator'] == f'mill_id={m["mill_id"]}',
                   f'{m["mill_id"]}: wrong row')

    def md_table(heading):
        secs = md_sections(files.raw(F)).get(heading, [])
        if len(secs) != 1:
            raise Miss(f'{heading!r} occurs {len(secs)} times')
        tables, _, _ = section_parts(secs[0])
        if len(tables) != 1:
            raise Miss(f'{heading!r}: {len(tables)} tables')
        return table_rows(tables[0], heading)

    def features():
        head, rows = md_table('## 1. Summary')
        got_f = L.get('features', [])
        expect('features', [f['number'] for f in got_f] == [strip_marks(r[head[0]]) for r in rows],
               'feature rows differ from the findings table')
        for f, r in zip(got_f, rows):
            expect('features', f['verdict']['value'] == strip_marks(r['Verdict']), f'{f["number"]}: verdict')
            expect('features', f['review_ids'] == list(dict.fromkeys(re.findall(r'R\d{3}', r['Main reason (review items)']))),
                   f'{f["number"]}: review IDs')
            expect('features', f['family']['locator'] == f'feature={strip_marks(r["Feature"])}',
                   f'{f["number"]}: family row')

    def gaps():
        head, rows = md_table('## 4. What failed or is weak')
        got_g = L.get('gaps', [])
        expect('gaps', [g['number'] for g in got_g] == [strip_marks(r[head[0]]) for r in rows],
               'gap rows differ from the findings table')
        for g, r in zip(got_g, rows):
            expect('gaps', g['review_ids'] == list(dict.fromkeys(re.findall(r'R\d{3}', r['Review item / log entry']))),
                   f'{g["number"]}: review IDs')

    def pending():
        got_p = L.get('decisions_pending', [])
        expect('decisions_pending', [p['item_id'] for p in got_p] == ['R057'], 'R057 expected (Step 4 decision 10)')
        for p in got_p:
            dec = cell(files, 'review_queue.csv', f'item_id={p["item_id"]}', 'decision')
            expect('decisions_pending', p['status'] == ('pending' if dec == '' else 'decided'),
                   f'{p["item_id"]}: status')

    def options():
        secs = md_sections(files.raw(F)).get('## 8. Decisions for Yaseen', [])
        _, items, _ = section_parts(secs[0])
        numbered = [strip_marks(i['text']) for i in items if i['numbered'] and i['indent'] == 0]
        got_o = L.get('decision_options', [])
        expect('decision_options', [o['text']['value'] for o in got_o] == numbered, 'options differ')
        expect('decision_options', [o['title'] for o in got_o] == [t.split(':')[0] for t in numbered], 'titles differ')

    def changes():
        h = '### 7.5 What would need to change for a full build (listed, not decided)'
        secs = md_sections(files.raw(F)).get(h, [])
        _, items, _ = section_parts(secs[0])
        bullets = [strip_marks(i['text']) for i in items if not i['numbered'] and i['indent'] == 0]
        got_c = L.get('full_build_changes', [])
        expect('full_build_changes', [c['text']['value'] for c in got_c] == bullets, 'items differ')
        expect('full_build_changes', [c['title'] for c in got_c] == [t.split(':')[0] for t in bullets], 'titles differ')

    for name, fn in [('firms', firms), ('sources', sources), ('attributions', attributions),
                     ('mills', mills), ('features', features), ('gaps', gaps), ('decisions_pending', pending),
                     ('decision_options', options), ('full_build_changes', changes)]:
        if name not in L:
            fail('lists', name, 'list missing from site_data.json')
            continue
        safe(name, fn)
    for name in L:
        if name not in ('firms', 'sources', 'attributions', 'mills', 'features', 'gaps', 'decisions_pending',
                        'decision_options', 'full_build_changes'):
            fail('lists', name, 'unexpected list (not checked)')

    # the page
    html_note = 'page not checked (--no-html)'
    if not args.no_html:
        hp = Path(args.html)
        if not hp.is_file():
            fail('page', str(hp), 'page not found (build it, or pass --no-html)')
        else:
            shown_n = check_page(hp.read_text(encoding='utf-8'), spec, raw_by_id, unit_by_id,
                                 {c['id']: c['text'] for c in caveats}, files, fail, count)
            html_note = f'page {hp.name}: {shown_n} of {len(spec)} spec numbers shown'

    # inputs and spec hashes
    listed = {i['file']: i['sha256'] for i in data.get('inputs', [])}
    for rel, digest in sorted(files.digest.items()):
        count('inputs')
        if rel not in listed:
            fail('inputs', rel, 'read by the check but not listed in site_data.json inputs')
        elif listed[rel] != digest:
            fail('inputs', rel, 'file changed since extraction (SHA-256 differs)')
    for rel in sorted(set(listed) - set(files.digest)):
        fail('inputs', rel, 'listed in site_data.json but not needed by any entry')
    for rel, path in (('docs/number_sources.csv', Path(args.spec)), ('docs/caveats.csv', Path(args.caveats))):
        count('inputs')
        if data.get('spec_sha256', {}).get(rel) != hashlib.sha256(path.read_bytes()).hexdigest():
            fail('inputs', rel, 'spec changed since extraction (SHA-256 differs)')

    # report
    lines = [f'check_numbers.py: {args.data}',
             'Checked: ' + ', '.join(f'{k} {v}' for k, v in tally.items()),
             html_note,
             f'Failures: {len(fails)}']
    lines += [f'  {f}' for f in fails]
    lines.append('Result: ' + ('PASS' if not fails else 'FAIL'))
    text = '\n'.join(lines) + '\n'
    print(text, end='')
    report = Path(args.report)
    report.parent.mkdir(parents=True, exist_ok=True)
    report.write_text(text, encoding='utf-8')
    return 1 if fails else 0


if __name__ == '__main__':
    sys.exit(main())
