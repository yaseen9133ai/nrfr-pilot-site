"""Extract the page data from the pilot (read-only) into build/site_data.json.

Spec: docs/number_sources.csv (one row per number on the page) and
docs/caveats.csv (caveat wording). The short text lists the page needs
(sources and licences, attributions, mills, feature verdicts, gaps,
pending decisions) are defined in this file (LISTS below) and read from the pilot.

Pilot path: the environment variable PILOT_DIR (default ../nrfr-pilot; a
relative value is read from nrfr-pilot-site/). The pilot is only opened for
reading. The only file written is build/site_data.json.

Locators (Step 2 decision 3; a missing or ambiguous locator is an error):
  CSV       row_key = conditions joined by '; ' (col=v, col^=a|b, col$=v,
            col!=v ('!=' alone = not empty), col!^=v); '*' = all rows;
            'header' = the header row. source_file 'firm{1,2,3}_x.csv' = the
            three files together.
  Markdown  row_key = '<heading line> | <block>' where block is one of
            'table[; filters]', 'row=<first cell>', 'bullet=<label>',
            'paragraph=<label>', 'paragraph <n>', 'heading',
            'numbered list'. The heading must occur once; a block that is
            not found, or found more than once, is an error.
  column_or_computation: a column name; count(rows), count(columns),
            count(distinct c), sum(c), min(c), max(c), count(items);
            'text: "<quote>"' or 'text in <column>: "<quote>"'. A quote must
            occur once in its cell or block, and the value once in the quote,
            as a whole token (so '15' never matches inside '0.15' or '150').

Display (Step 2 decision 5): format 'number' keeps the source decimals and
sign, adds thousands separators and writes a minus as U+2212; no rounding.
Format 'as_is' keeps the source text (dates, versions, ranges, phrases).

The same input gives byte-identical output (no timestamps, fixed order).
Exit 0 = written; 1 = a value was not found, was ambiguous or differs from
the spec's expected value (nothing written, and an old site_data.json is
removed so it cannot be used by mistake); 2 = setup error.

Python standard library only.
"""

import csv
import hashlib
import io
import json
import os
import re
import sys
from decimal import Decimal, InvalidOperation
from pathlib import Path

SITE_ROOT = Path(__file__).resolve().parent.parent
BUILD = SITE_ROOT / 'build'
OUT = BUILD / 'site_data.json'
SPEC = SITE_ROOT / 'docs' / 'number_sources.csv'
CAVEATS = SITE_ROOT / 'docs' / 'caveats.csv'

MINUS = '−'
SPEC_COLUMNS = ['id', 'section', 'label', 'source_file', 'row_key', 'column_or_computation',
                'expected_value', 'format', 'unit', 'caveats', 'tag_required', 'note']
# Step 2 decision 4 and Step 3 decision 5: digits that need no tag on the page.
NO_TAG_REASONS = {'review ID', 'step number', 'section number', 'year label', 'date', 'version',
                  'file name', 'ISIC code', 'licence version', 'name or identifier'}


class SourceError(Exception):
    pass


def pilot_dir():
    """The one pilot-path setting: PILOT_DIR, default ../nrfr-pilot (relative to SITE_ROOT)."""
    p = Path(os.environ.get('PILOT_DIR') or '../nrfr-pilot')
    return (p if p.is_absolute() else SITE_ROOT / p).resolve()


# ---------------------------------------------------------------- pilot files

class Pilot:
    """Read-only access to pilot files, with a SHA-256 of every file read."""

    def __init__(self, root):
        self.root = root
        self.hashes = {}
        self._csv = {}
        self._md = {}

    def text(self, rel):
        full = (self.root / rel).resolve()
        if self.root not in full.parents:
            raise SourceError(f'{rel}: outside the pilot folder')
        if not full.is_file():
            raise SourceError(f'{rel}: file not found in the pilot')
        with open(full, 'rb') as f:
            data = f.read()
        self.hashes[rel] = hashlib.sha256(data).hexdigest()
        return data.decode('utf-8')

    def csv(self, rel):
        if rel not in self._csv:
            reader = csv.DictReader(io.StringIO(self.text(rel), newline=''))
            self._csv[rel] = (list(reader.fieldnames or []), list(reader))
        return self._csv[rel]

    def md(self, rel):
        if rel not in self._md:
            self._md[rel] = MdDoc(self.text(rel), rel)
        return self._md[rel]


def expand(source_file):
    if '{1,2,3}' in source_file:
        return [source_file.replace('{1,2,3}', n) for n in '123']
    return [source_file]


# ---------------------------------------------------------------- conditions

OPS = ('!^=', '^=', '$=', '!=', '=')


def parse_conditions(text):
    conds = []
    for part in text.split('; '):
        best = None
        for op in OPS:
            i = part.find(op)
            if i > 0 and (best is None or i < best[0] or (i == best[0] and len(op) > len(best[1]))):
                best = (i, op)
        if best is None:
            raise SourceError(f'bad condition {part!r}')
        i, op = best
        conds.append((part[:i], op, part[i + len(op):]))
    return conds


def cond_ok(cell, op, val):
    alts = val.split('|')
    if op == '=':
        return cell == val
    if op == '!=':
        return cell != val
    if op == '^=':
        return any(cell.startswith(a) for a in alts)
    if op == '!^=':
        return not any(cell.startswith(a) for a in alts)
    if op == '$=':
        return any(cell.endswith(a) for a in alts)
    raise SourceError(f'unknown operator {op}')


def filter_rows(rows, header, conds, where):
    for col, _, _ in conds:
        if col not in header:
            raise SourceError(f'{where}: no column {col!r}')
    return [r for r in rows if all(cond_ok(r[c], op, v) for c, op, v in conds)]


def one(rows, where):
    if len(rows) != 1:
        raise SourceError(f'{where}: {len(rows)} rows match (need exactly 1)')
    return rows[0]


QUOTE = re.compile(r'text(?: in (?P<col>.+?))?: "(?P<quote>.*)"$')


def token_hits(text, value):
    """Start positions where value occurs in text as a whole token: an end that is a
    digit does not touch another digit, or a '.'/',' that continues a number; an end
    that is a letter does not touch a letter or digit."""
    hits, start = [], 0
    while True:
        i = text.find(value, start)
        if i < 0:
            return hits
        j = i + len(value)
        ok = True
        if i > 0:
            before = text[i - 1]
            if value[0].isdigit():
                ok = not (before.isdigit() or (before in '.,' and i > 1 and text[i - 2].isdigit()))
            elif value[0].isalpha():
                ok = not before.isalnum()
        if ok and j < len(text):
            after = text[j]
            if value[-1].isdigit():
                ok = not (after.isdigit() or (after in '.,' and j + 1 < len(text) and text[j + 1].isdigit()))
            elif value[-1].isalpha():
                ok = not after.isalnum()
        if ok:
            hits.append(i)
        start = i + 1


def value_in_quote(block_text, quote, value, where):
    n = block_text.count(quote)
    if n != 1:
        raise SourceError(f'{where}: quote found {n} times (need exactly 1): {quote!r}')
    hits = token_hits(quote, value)
    if len(hits) != 1:
        raise SourceError(f'{where}: value {value!r} found {len(hits)} times in the quote (need exactly 1)')
    return value


# ---------------------------------------------------------------- CSV lookups

def csv_cell(pilot, src, row_key, column):
    """One cell, by conditions. Returns its text."""
    header, rows = pilot.csv(src)
    if column not in header:
        raise SourceError(f'{src}: no column {column!r}')
    row = one(filter_rows(rows, header, parse_conditions(row_key), src), f'{src} | {row_key}')
    return row[column]


def csv_value(pilot, src, row_key, comp, expected):
    files = expand(src)
    if row_key == 'header':
        if comp != 'count(columns)' or len(files) != 1:
            raise SourceError(f'{src}: header supports count(columns) on one file')
        return str(len(pilot.csv(files[0])[0]))
    rows = []
    for f in files:
        header, frows = pilot.csv(f)
        rows += frows if row_key == '*' else filter_rows(frows, header, parse_conditions(row_key), f)
    if comp == 'count(rows)':
        return str(len(rows))
    m = re.fullmatch(r'count\(distinct (.+)\)', comp)
    if m:
        return str(len({r[m.group(1)] for r in rows}))
    m = re.fullmatch(r'(sum|min|max)\((.+)\)', comp)
    if m:
        how, col = m.groups()
        if not rows:
            raise SourceError(f'{src} | {row_key}: no rows for {comp}')
        try:
            nums = [(Decimal(r[col]), r[col]) for r in rows]
        except (InvalidOperation, KeyError):
            raise SourceError(f'{src}: {col!r} is not numeric in every row')
        if how == 'sum':
            return str(sum(n for n, _ in nums))
        pick = min(nums) if how == 'min' else max(nums)
        return pick[1]
    m = QUOTE.fullmatch(comp)
    if m and m.group('col'):
        if len(files) != 1:
            raise SourceError(f'{src}: a quote needs one file')
        cell = csv_cell(pilot, files[0], row_key, m.group('col'))
        return value_in_quote(cell, m.group('quote'), expected, f'{src} | {row_key} | {m.group("col")}')
    if len(files) != 1:
        raise SourceError(f'{src}: a cell needs one file')
    return csv_cell(pilot, files[0], row_key, comp)


# ---------------------------------------------------------------- markdown

HEADING = re.compile(r'^#{1,6} \S')
LIST_ITEM = re.compile(r'^(\s*)([-*+]|\d+\.)\s+(.*)$')
TABLE_SEP = re.compile(r'^\|?[\s:|-]+\|?$')


def norm(s):
    """Cell or item text without markdown emphasis or code marks."""
    return s.replace('**', '').replace('`', '').strip()


def split_cells(line):
    s = line.strip()
    if s.startswith('|'):
        s = s[1:]
    if s.endswith('|') and not s.endswith('\\|'):
        s = s[:-1]
    return [c.strip() for c in re.split(r'(?<!\\)\|', s)]


class MdDoc:
    """Headings and the blocks directly under each (up to the next heading of any level)."""

    def __init__(self, text, rel):
        self.rel = rel
        self.sections = []
        heading, lines, fence = None, [], False
        for line in text.split('\n'):
            if line.lstrip().startswith('```'):
                fence = not fence
                lines.append(None)
                continue
            if fence:
                lines.append(None)
                continue
            if HEADING.match(line):
                self.sections.append((heading, lines))
                heading, lines = line.rstrip(), []
                continue
            lines.append(line)
        self.sections.append((heading, lines))

    def section(self, heading):
        hits = [lines for h, lines in self.sections if h == heading]
        if len(hits) != 1:
            raise SourceError(f'{self.rel}: heading found {len(hits)} times: {heading!r}')
        return hits[0]


def blocks(lines):
    """Split section lines into ('table', [rows]), ('item', marker, text) and ('para', text)."""
    out, para, table = [], [], []

    def flush():
        if para:
            out.append(('para', ' '.join(para)))
            para.clear()
        if table:
            out.append(('table', list(table)))
            table.clear()

    for line in lines:
        if line is None or not line.strip():
            flush()
            continue
        if line.strip().startswith('|'):
            if para:
                out.append(('para', ' '.join(para)))
                para.clear()
            table.append(line.strip())
            continue
        if table:
            out.append(('table', list(table)))
            table.clear()
        m = LIST_ITEM.match(line)
        if m:
            if para:
                out.append(('para', ' '.join(para)))
                para.clear()
            out.append(('item', m.group(2), m.group(3), len(m.group(1))))
            continue
        para.append(line.strip())
    flush()
    return out


def parse_table(rows, where):
    if len(rows) < 2 or not TABLE_SEP.match(rows[1]):
        raise SourceError(f'{where}: not a table')
    header = [norm(c) for c in split_cells(rows[0])]
    data = []
    for line in rows[2:]:
        cells = split_cells(line)
        if len(cells) != len(header):
            raise SourceError(f'{where}: a row has {len(cells)} cells, header {len(header)}')
        data.append(dict(zip(header, cells)))
    return header, data


def md_block(pilot, src, row_key):
    """Return (kind, payload) for a markdown locator."""
    heading, sep, block = row_key.partition(' | ')
    if not sep:
        raise SourceError(f'{src}: locator needs "<heading> | <block>": {row_key!r}')
    doc = pilot.md(src)
    bl = blocks(doc.section(heading))
    where = f'{src} | {row_key}'
    parts = block.split('; ')
    kind = parts[0]
    if kind in ('table',) or kind.startswith('row='):
        tables = [b for b in bl if b[0] == 'table']
        if len(tables) != 1:
            raise SourceError(f'{where}: {len(tables)} tables under the heading (need exactly 1)')
        header, data = parse_table(tables[0][1], where)
        if kind == 'table':
            conds = parse_conditions('; '.join(parts[1:])) if len(parts) > 1 else []
            for c, _, _ in conds:
                if c not in header:
                    raise SourceError(f'{where}: no column {c!r}')
            return 'rows', [r for r in data if all(cond_ok(norm(r[c]), op, v) for c, op, v in conds)]
        label = kind[len('row='):]
        return 'row', one([r for r in data if norm(r[header[0]]) == label], where)
    if len(parts) != 1:
        raise SourceError(f'{where}: filters only apply to tables')
    if kind == 'heading':
        return 'text', heading.lstrip('#').strip()
    if kind == 'numbered list':
        return 'items', [b for b in bl if b[0] == 'item' and b[1][0].isdigit() and b[3] == 0]
    if kind.startswith('bullet='):
        label = kind[len('bullet='):]
        hits = [b for b in bl if b[0] == 'item' and norm(b[2]).startswith(label)]
        return 'text', one(hits, where)[2]
    if kind.startswith('paragraph='):
        label = kind[len('paragraph='):]
        hits = [b for b in bl if b[0] == 'para' and norm(b[1]).startswith(label)]
        return 'text', one(hits, where)[1]
    m = re.fullmatch(r'paragraph (\d+)', kind)
    if m:
        paras = [b for b in bl if b[0] == 'para']
        n = int(m.group(1))
        if not 1 <= n <= len(paras):
            raise SourceError(f'{where}: there are {len(paras)} paragraphs')
        return 'text', paras[n - 1][1]
    raise SourceError(f'{where}: unknown block {kind!r}')


def md_value(pilot, src, row_key, comp, expected):
    kind, payload = md_block(pilot, src, row_key)
    where = f'{src} | {row_key}'
    if kind == 'rows':
        if comp != 'count(rows)':
            raise SourceError(f'{where}: a table supports count(rows)')
        return str(len(payload))
    if kind == 'items':
        if comp != 'count(items)':
            raise SourceError(f'{where}: a numbered list supports count(items)')
        return str(len(payload))
    m = QUOTE.fullmatch(comp)
    if kind == 'row':
        if m and m.group('col'):
            col = m.group('col')
            if col not in payload:
                raise SourceError(f'{where}: no column {col!r}')
            return value_in_quote(payload[col], m.group('quote'), expected, f'{where} | {col}')
        if m:
            raise SourceError(f'{where}: a quote in a table row must name its column')
        if comp not in payload:
            raise SourceError(f'{where}: no column {comp!r}')
        return norm(payload[comp])
    if not m or m.group('col'):
        raise SourceError(f'{where}: a list item, paragraph or heading needs text: "<quote>"')
    return value_in_quote(payload, m.group('quote'), expected, where)


def md_text(pilot, src, row_key, column):
    """A text field from markdown: a table cell (column name) or a whole block ('text')."""
    kind, payload = md_block(pilot, src, row_key)
    if kind == 'row':
        if column not in payload:
            raise SourceError(f'{src} | {row_key}: no column {column!r}')
        return norm(payload[column])
    if kind == 'text' and column == 'text':
        return norm(payload)
    raise SourceError(f'{src} | {row_key}: cannot read {column!r} as text')


# ---------------------------------------------------------------- numbers

def lookup(pilot, src, row_key, comp, expected):
    if src.endswith('.md'):
        return md_value(pilot, src, row_key, comp, expected)
    if src.endswith('.csv'):
        return csv_value(pilot, src, row_key, comp, expected)
    raise SourceError(f'{src}: only .csv and .md sources are read')


PLAIN = re.compile(r'(-?)(\d{1,3}(?:,\d{3})+|\d+)(\.\d+)?')


def display(raw, fmt):
    if fmt == 'as_is':
        return raw
    m = PLAIN.fullmatch(raw)
    if not m:
        raise SourceError(f'format "number" needs a plain number, got {raw!r}')
    sign, whole, frac = m.groups()
    digits = whole.replace(',', '')
    groups = []
    while len(digits) > 3:
        groups.insert(0, digits[-3:])
        digits = digits[:-3]
    groups.insert(0, digits)
    return (MINUS if sign else '') + ','.join(groups) + (frac or '')


def tag(file, locator, column):
    return {'file': file, 'locator': locator, 'column': column}


def unit_of(pilot, unit):
    """A literal unit, or '@file | row_key | column' read from a CSV cell."""
    if not unit.startswith('@'):
        return unit, None
    parts = unit[1:].split(' | ')
    if len(parts) != 3 or not parts[0].endswith('.csv'):
        raise SourceError(f'bad unit locator {unit!r}')
    src, row_key, column = parts
    value = csv_cell(pilot, src, row_key, column)
    return value, dict(tag(src, row_key, column), raw=value)


def read_spec():
    with open(SPEC, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        if reader.fieldnames != SPEC_COLUMNS:
            raise SourceError(f'{SPEC.name}: columns must be {SPEC_COLUMNS}')
        return list(reader)


def read_caveats():
    with open(CAVEATS, newline='', encoding='utf-8') as f:
        return [{'id': r['id'], 'text': r['text'], 'basis': r['basis']} for r in csv.DictReader(f)]


def build_numbers(pilot, spec, caveat_ids, errors):
    out, seen = [], set()
    for r in spec:
        where = r['id']
        try:
            if r['id'] in seen:
                raise SourceError('duplicate id')
            seen.add(r['id'])
            if r['format'] not in ('number', 'as_is'):
                raise SourceError(f'unknown format {r["format"]!r}')
            req = r['tag_required']
            if req != 'yes':
                reason = req[len('no: '):] if req.startswith('no: ') else None
                if reason not in NO_TAG_REASONS:
                    raise SourceError(f'tag_required must be "yes" or "no: <reason>" (decision 4): {req!r}')
            caveats = [c for c in r['caveats'].split('; ') if c]
            for c in caveats:
                if c not in caveat_ids:
                    raise SourceError(f'unknown caveat {c!r}')
            raw = lookup(pilot, r['source_file'], r['row_key'], r['column_or_computation'], r['expected_value'])
            if raw != r['expected_value']:
                raise SourceError(f'source gives {raw!r}, spec expects {r["expected_value"]!r}')
            unit, unit_source = unit_of(pilot, r['unit'])
            out.append({
                'id': r['id'],
                'section': r['section'],
                'label': r['label'],
                'raw': raw,
                'display': display(raw, r['format']),
                'format': r['format'],
                'unit': unit,
                'unit_source': unit_source,
                'source': tag(r['source_file'], r['row_key'], r['column_or_computation']),
                'tag_required': req == 'yes',
                'no_tag_reason': None if req == 'yes' else req[len('no: '):],
                'caveats': caveats,
            })
        except SourceError as e:
            errors.append(f'{where}: {e}')
    return out


# ---------------------------------------------------------------- text lists

FINDINGS = 'reports/step10_findings.md'
SUMMARY = '## 1. Summary'
WEAK = '## 4. What failed or is weak'
CHANGES = '### 7.5 What would need to change for a full build (listed, not decided)'
OPTIONS = '## 8. Decisions for Yaseen'
REVIEW_ID = re.compile(r'\bR\d{3}\b')


def review_ids(text):
    """Review IDs in the order they first appear, each once."""
    return list(dict.fromkeys(REVIEW_ID.findall(text)))

# Attribution wording that the pilot records word for word (source_register.csv).
ATTRIBUTION_QUOTES = [
    ('HANSEN_GFC', 'licence', 'This work is licensed under a Creative Commons Attribution 4.0 International License.'),
    ('ENCORE', 'licence', 'ENCORE Partners (Global Canopy, UNEP FI, and UNEP-WCMC) (year). ENCORE: Exploring '
                          'Natural Capital Opportunities, Risks and Exposure. [On-line], [month/year of the '
                          'version downloaded], Cambridge, UK: ENCORE Partners. DOI 10.34892/dz3x-y059.'),
    ('ROADS_OSM', 'notes', '© OpenStreetMap contributors'),
    ('ROADS_OSM', 'notes', 'Provide credit to OpenStreetMap by displaying our attribution notice'),
    ('ROADS_OSM', 'notes', 'Make clear that the data is available under the Open Database License.'),
    ('BOUNDARY_GEOB', 'notes', 'Boundary source: OpenStreetMap, Wambacher'),
    ('CBP_WRO', 'licence', 'This product uses U.S. Customs and Border Protection data, but is not endorsed by CBP.'),
    # Only the part that applies to the file used (CSV 1.1); CC BY 4.0 is listed for CSV 1.0 (Step 5 close-out).
    ('EU_FSF', 'licence', 'European Commission reuse notice (Decision 2011/833/EU)'),
]
# Wording the page needs but the pilot does not record (open question for Yaseen).
ATTRIBUTION_NOT_RECORDED = [
    ('HANSEN_GFC', 'The full Hansen et al. citation is not recorded in the pilot.'),
    ('S2_L2A', 'The Copernicus credit wording for the satellite images is not recorded in the pilot.'),
]


def tfield(file, locator, column, value):
    return dict(tag(file, locator, column), value=value)


def csv_tfield(pilot, file, locator, column):
    return tfield(file, locator, column, csv_cell(pilot, file, locator, column))


def md_tfield(pilot, file, locator, column):
    return tfield(file, locator, column, md_text(pilot, file, locator, column))


def md_table_firsts(pilot, file, heading):
    """First-cell labels of the one table under a heading, in file order."""
    kind, rows = md_block(pilot, file, f'{heading} | table')
    return [norm(next(iter(r.values()))) for r in rows]


def md_item_labels(pilot, file, heading, numbered):
    bl = blocks(pilot.md(file).section(heading))
    items = [b for b in bl if b[0] == 'item' and b[3] == 0 and b[1][0].isdigit() == numbered]
    return [norm(b[2]).split(':')[0] + ':' for b in items]


def build_lists(pilot, errors):
    lists = {}

    def guard(name, fn):
        try:
            lists[name] = fn()
        except SourceError as e:
            errors.append(f'list {name}: {e}')

    def firms():
        _, rows = pilot.csv('data/processed/pilot_firm_year.csv')
        out = []
        for fid in dict.fromkeys(r['firm_id'] for r in rows):
            out.append({'firm_id': fid, 'name': csv_tfield(pilot, 'data/processed/pilot_firm_year.csv',
                                                           f'firm_id={fid}; year=2021', 'firm')})
        return out

    def sources():
        _, rows = pilot.csv('source_register.csv')
        return [{'source_id': r['source_id'],
                 'name': csv_tfield(pilot, 'source_register.csv', f'source_id={r["source_id"]}', 'name'),
                 'licence': csv_tfield(pilot, 'source_register.csv', f'source_id={r["source_id"]}', 'licence'),
                 'date_downloaded': csv_tfield(pilot, 'source_register.csv', f'source_id={r["source_id"]}',
                                               'date_downloaded')}
                for r in rows]

    def attributions():
        out = []
        for sid, col, quote in ATTRIBUTION_QUOTES:
            cell = csv_cell(pilot, 'source_register.csv', f'source_id={sid}', col)
            if cell.count(quote) != 1:
                raise SourceError(f'{sid} {col}: wording found {cell.count(quote)} times (need exactly 1)')
            out.append({'source_id': sid, 'recorded': True,
                        'wording': tfield('source_register.csv', f'source_id={sid}', f'text in {col}: "{quote}"',
                                          quote)})
        for sid, note in ATTRIBUTION_NOT_RECORDED:
            out.append({'source_id': sid, 'recorded': False, 'note': note})
        return out

    def mills():
        out = []
        for n in '123':
            src = f'data/interim/firm{n}_mills.csv'
            header, rows = pilot.csv(src)
            for r in filter_rows(rows, header, parse_conditions('in_scope^=yes'), src):
                loc = f'mill_id={r["mill_id"]}'
                out.append({'mill_id': r['mill_id'], 'firm': csv_tfield(pilot, src, loc, 'firm'),
                            'name': csv_tfield(pilot, src, loc, 'mill_name')})
        return out

    def features():
        out = []
        for n in md_table_firsts(pilot, FINDINGS, SUMMARY):
            loc = f'{SUMMARY} | row={n}'
            name = md_tfield(pilot, FINDINGS, loc, 'Feature')
            reason = md_tfield(pilot, FINDINGS, loc, 'Main reason (review items)')
            out.append({'number': n, 'feature': name,
                        'family': csv_tfield(pilot, 'feature_dictionary.csv', f'feature={name["value"]}', 'family'),
                        'verdict': md_tfield(pilot, FINDINGS, loc, 'Verdict'),
                        'main_reason': reason,
                        'review_ids': review_ids(reason['value'])})
        return out

    def gaps():
        out = []
        for n in md_table_firsts(pilot, FINDINGS, WEAK):
            loc = f'{WEAK} | row={n}'
            ref = md_tfield(pilot, FINDINGS, loc, 'Review item / log entry')
            out.append({'number': n, 'issue': md_tfield(pilot, FINDINGS, loc, 'Issue'),
                        'review_ref': ref, 'review_ids': review_ids(ref['value'])})
        return out

    def decisions_pending():
        out = []
        # R058 (unconfirmed hours) is not shown: the hours section was removed (CLAUDE.md, Step 4 decision 10).
        for rid in ('R057',):
            decision = csv_tfield(pilot, 'review_queue.csv', f'item_id={rid}', 'decision')
            out.append({'item_id': rid,
                        'item': csv_tfield(pilot, 'review_queue.csv', f'item_id={rid}', 'item'),
                        'decision': decision,
                        'status': 'pending' if decision['value'] == '' else 'decided'})
        return out

    def decision_options():
        out = []
        for i, label in enumerate(md_item_labels(pilot, FINDINGS, OPTIONS, numbered=True), 1):
            f = md_tfield(pilot, FINDINGS, f'{OPTIONS} | bullet={label}', 'text')
            out.append({'number': str(i), 'title': label[:-1], 'text': f})
        return out

    def full_build_changes():
        out = []
        for label in md_item_labels(pilot, FINDINGS, CHANGES, numbered=False):
            f = md_tfield(pilot, FINDINGS, f'{CHANGES} | bullet={label}', 'text')
            out.append({'title': label[:-1], 'text': f, 'review_ids': review_ids(f['value'])})
        return out

    guard('firms', firms)
    guard('sources', sources)
    guard('attributions', attributions)
    guard('mills', mills)
    guard('features', features)
    guard('gaps', gaps)
    guard('decisions_pending', decisions_pending)
    guard('decision_options', decision_options)
    guard('full_build_changes', full_build_changes)
    return lists


# ---------------------------------------------------------------- main

def sha256_file(path):
    with open(path, 'rb') as f:
        return hashlib.sha256(f.read()).hexdigest()


def main():
    pilot_root = pilot_dir()
    if not pilot_root.is_dir():
        print(f'ERROR: pilot folder not found (PILOT_DIR): {pilot_root}')
        return 2
    if BUILD.resolve() == pilot_root or pilot_root in BUILD.resolve().parents:
        print('ERROR: build/ is inside the pilot folder; refusing to write.')
        return 2
    errors = []
    try:
        spec = read_spec()
        caveats = read_caveats()
    except (OSError, SourceError) as e:
        print(f'ERROR: {e}')
        return 2
    pilot = Pilot(pilot_root)
    numbers = build_numbers(pilot, spec, {c['id'] for c in caveats}, errors)
    lists = build_lists(pilot, errors)

    if errors:
        print(f'FAIL: {len(errors)} problem(s); nothing written.')
        for e in errors:
            print(f'  {e}')
        if OUT.exists():
            OUT.unlink()
            print(f'Removed the old {OUT.relative_to(SITE_ROOT)} so it cannot be used by mistake.')
        return 1

    data = {
        'about': {
            'what': 'Page data for the palm oil pilot site, read from the pilot files (read-only).',
            'made_by': 'scripts/extract.py',
            'pilot': 'the pilot folder (setting PILOT_DIR); every file path below is relative to it',
            'numbers': 'one entry per row of docs/number_sources.csv, in its order',
            'display': 'Step 2 decision 5: source decimals and sign kept, thousands separators added, '
                       'minus written as U+2212, no rounding; format as_is keeps the source text',
            'tag': 'Step 2 decision 6: file, locator, column and raw value',
        },
        'spec_sha256': {
            'docs/number_sources.csv': sha256_file(SPEC),
            'docs/caveats.csv': sha256_file(CAVEATS),
        },
        'inputs': [{'file': rel, 'sha256': pilot.hashes[rel]} for rel in sorted(pilot.hashes)],
        'counts': {
            'numbers': len(numbers),
            'numbers_tag_required': sum(1 for n in numbers if n['tag_required']),
            'numbers_with_caveats': sum(1 for n in numbers if n['caveats']),
            'numbers_from_csv': sum(1 for n in numbers if n['source']['file'].endswith('.csv')),
            'numbers_from_markdown': sum(1 for n in numbers if n['source']['file'].endswith('.md')),
            'lists': {k: len(v) for k, v in lists.items()},
        },
        'caveats': caveats,
        'numbers': numbers,
        'lists': lists,
    }
    BUILD.mkdir(exist_ok=True)
    text = json.dumps(data, ensure_ascii=False, indent=1) + '\n'
    with open(OUT, 'w', encoding='utf-8', newline='\n') as f:
        f.write(text)
    c = data['counts']
    print(f'Wrote {OUT.relative_to(SITE_ROOT)}: {c["numbers"]} numbers '
          f'({c["numbers_from_csv"]} from CSV, {c["numbers_from_markdown"]} from markdown; '
          f'{c["numbers_tag_required"]} need a tag on the page), '
          + ', '.join(f'{k} {v}' for k, v in c['lists'].items())
          + f'; {len(data["inputs"])} pilot files read.')
    print(f'SHA-256 {hashlib.sha256(text.encode("utf-8")).hexdigest()}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
