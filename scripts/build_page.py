"""Build the page: site/index.html and site/assets/style.css.

Reads only build/site_data.json (written by scripts/extract.py). Every number
on the page is inserted from that file, inside a <span> that carries its
source tag (CLAUDE.md, Step 3 decision 1):

  <span class="n" data-id="..." data-file="..." data-locator="..."
        data-column="..." data-raw="...">8,856.91 ha</span>

No number is typed in the text below. Digits that need no tag (Step 2
decision 4, Step 3 decision 5: review IDs, step and section numbers, years
used as labels, dates, versions, file names, ISIC codes, licence versions,
names and identifiers) sit in elements marked data-notag="<reason>". Text
quoted from the pilot sits in a span with its own tag (class "t"). The
appendix shows each tag as text in elements marked data-meta. Caveats are
listed in the block (data-block) that holds the numbers they belong to.
scripts/check_numbers.py checks all of this against the pilot.

Page form of a number (Step 3 decisions 2-6): the display from
site_data.json (source decimals, thousands separators, minus as U+2212), a
"+" on positive rainfall anomalies only, dates written for readers, en
dashes in year ranges, number words as digits, and the unit after a
no-break space (no space before %). FFB units are shown without spaces;
the printed form stays in data-unit-raw.

The images are copied by scripts/copy_images.py (run it first). Images and
captions are named here. The same input gives byte-identical output.
Exit 0 = written, 2 = site_data.json missing or unreadable.

Python standard library only.
"""

import html
import json
import re
import sys
from pathlib import Path

SITE = Path(__file__).resolve().parent.parent
DATA = SITE / 'build' / 'site_data.json'
OUT_HTML = SITE / 'site' / 'index.html'
OUT_CSS = SITE / 'site' / 'assets' / 'style.css'

NBSP = ' '
MINUS = '−'
MONTHS = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September',
          'October', 'November', 'December']
WORDS = {'one': '1', 'two': '2', 'three': '3', 'four': '4', 'five': '5', 'six': '6', 'seven': '7',
         'eight': '8', 'nine': '9', 'ten': '10', 'eleven': '11', 'twelve': '12'}
FIRMS = [('sop', 'SOP', 'sops'), ('ta_ann', 'Ta Ann', 'ta_anns'), ('spb', 'SPB', 'spbs')]
YEARS = ['2021', '2022', '2023']


def esc(s):
    return html.escape(s, quote=True)


# ------------------------------------------------------------ page forms

def reader_date(raw):
    """2026-10-24 -> 24 October 2026; 2026-10-23T07:01:46Z -> 23 October 2026, 07:01:46 UTC;
    10 Jul 2026 -> 10 July 2026; other forms unchanged."""
    m = re.fullmatch(r'(\d{4})-(\d{2})-(\d{2})(?:T(\d{2}:\d{2}:\d{2})Z)?', raw)
    if m:
        y, mo, d, t = m.groups()
        return f'{int(d)} {MONTHS[int(mo) - 1]} {y}' + (f', {t} UTC' if t else '')
    m = re.fullmatch(r'(\d{1,2}) ([A-Z][a-z]{2}) (\d{4})', raw)
    if m:
        full = [x for x in MONTHS if x[:3] == m.group(2)]
        if len(full) == 1:
            return f'{m.group(1)} {full[0]} {m.group(3)}'
    return raw


def dates_in_text(value):
    """Every ISO date in a date field, written for readers."""
    return re.sub(r'\b(\d{4}-\d{2}-\d{2})(?!T)\b', lambda m: reader_date(m.group(1)), value)


def page_form(n):
    if n['format'] == 'number':
        s = n['display']
        if n['label'].startswith('Rainfall anomaly (mm)') and not s.startswith(MINUS):
            s = '+' + s
    elif n['no_tag_reason'] == 'date':
        s = reader_date(n['raw'])
    elif n['no_tag_reason'] == 'year label':
        s = n['raw'].replace('-', '–')
    else:
        s = re.sub(r'\b(' + '|'.join(WORDS) + r')\b', lambda m: WORDS[m.group(1).lower()], n['raw'],
                   flags=re.I)
    unit = n['unit']
    if n['unit_source']:
        unit = re.sub(r'\s+', '', unit)
    if unit:
        s += ('' if unit == '%' else NBSP) + unit
    return s


# ------------------------------------------------------------ small markup helpers

def nt(reason, text):
    return f'<span class="nt" data-notag="{esc(reason)}">{esc(text)}</span>'


def yr(y):
    return nt('year label', y)


def stp(s):
    return nt('step number', s)


def sec(s):
    return nt('section number', s)


def ident(s):
    return nt('name or identifier', s)


def lic(s):
    return nt('licence version', s)


def rid(r):
    return f'<small class="rid" data-notag="review ID">{esc(r)}</small>'


def rids(ids):
    return ' '.join(rid(r) for r in ids)


def path(p):
    return f'<code class="path" data-notag="file name">{esc(p)}</code>'


def details(*parts):
    return ('<p class="details"><span class="details-label">Details in the pilot:</span> '
            + ', '.join(parts) + '.</p>')


# A table sits in its own box: on a narrow screen a wide table scrolls sideways inside the box, never the
# page. The box can take keyboard focus, so it can be scrolled with the arrow keys too.
TBL = 'class="tbl" role="region" tabindex="0"'


def attrs(d):
    return ' '.join(f'{k}="{esc(v)}"' for k, v in d.items())


def t(f, form=None, bold_prefix=False):
    """A text field quoted from the pilot, with its tag. form='date' writes its ISO dates
    for readers (the source value stays in data-value)."""
    a = {'class': 't', 'data-file': f['file'], 'data-locator': f['locator'], 'data-column': f['column']}
    value = f['value']
    shown = value
    if form == 'date':
        shown = dates_in_text(value)
        if shown != value:
            a['data-form'] = 'date'
            a['data-value'] = value
    body = esc(shown)
    if bold_prefix and ':' in shown:
        head, rest = body.split(':', 1)
        body = f'<b>{head}</b>:{rest}'
    body = re.sub(r'\bR\d{3}\b', lambda m: f'<small class="rid">{m.group(0)}</small>', body)
    return f'<span {attrs(a)}>{body}</span>'


# ------------------------------------------------------------ numbers and caveat blocks

class Page:
    def __init__(self, data):
        self.num = {n['id']: n for n in data['numbers']}
        self.order = [n['id'] for n in data['numbers']]
        self.cav = {c['id']: c['text'] for c in data['caveats']}
        self.cav_order = [c['id'] for c in data['caveats']]
        self.L = data['lists']

    def span(self, nid, tag='span'):
        n = self.num[nid]
        text = page_form(n)
        # Short numbers are kept on one line; long phrases may wrap on small screens.
        a = {'class': 'n nw' if len(text) <= 18 else 'n', 'data-id': nid, 'data-file': n['source']['file'],
             'data-locator': n['source']['locator'], 'data-column': n['source']['column'], 'data-raw': n['raw']}
        if n['unit_source']:
            a['data-unit-raw'] = n['unit_source']['raw']
        if n['caveats']:
            a['data-caveats'] = ' '.join(n['caveats'])
        return f'<{tag} {attrs(a)}>{esc(text)}</{tag}>'


class Block:
    """A part of the page whose numbers' caveats are listed inside it."""

    def __init__(self, page, bid, markers=True):
        self.p, self.bid, self.markers = page, bid, markers
        self.caveats = []
        self.marked = set()

    def _use(self, cid):
        if cid not in self.caveats:
            self.caveats.append(cid)
        return 'abcdefghijklmnopqrstuvwxyz'[self.caveats.index(cid)]

    def n(self, nid):
        out = self.p.span(nid)
        letters = [(self._use(c), c) for c in self.p.num[nid]['caveats']]
        if letters and self.markers:
            self.marked.update(c for _, c in letters)
            out += '<sup class="mks">' + ''.join(
                f'<a class="mk" href="#{self.bid}-{c}" title="See the note below">{k}</a>' for k, c in letters) + '</sup>'
        return out

    def tsp(self, nid):
        """A number inside SVG text."""
        for c in self.p.num[nid]['caveats']:
            self._use(c)
        return self.p.span(nid, tag='tspan')

    def note(self, cid):
        self._use(cid)
        return ''

    def needs(self, *cids):
        """A note that belongs to an element of the block rather than to a number (an image, a
        feature card, a missing value). The element carries data-needs, so scripts/check_numbers.py
        can tell a needed note from a stray one."""
        for c in cids:
            self._use(c)
        return f' data-needs="{" ".join(cids)}"'

    def notes(self):
        if not self.caveats:
            return ''
        items = ''.join(
            f'<li id="{self.bid}-{c}"><b class="mk-key">'
            f'{"abcdefghijklmnopqrstuvwxyz"[i] if c in self.marked else "–"}</b> '
            f'<span data-caveat="{c}">{esc(self.p.cav[c])}</span></li>'
            for i, c in enumerate(self.caveats))
        return f'<ul class="notes" aria-label="Notes">{items}</ul>'

    def wrap(self, inner, cls='blk', tag='div', notes=True, needs=''):
        return (f'<{tag} class="{cls}" data-block="{self.bid}" id="{self.bid}"{needs}>{inner}'
                f'{self.notes() if notes else ""}</{tag}>')


# ------------------------------------------------------------ figures

# Pixel size of each image (layout only: it lets the browser reserve the space, so links inside the
# page land in the right place). scripts/check_offline.py compares these with the files.
IMAGE_SIZES = {
    'step5_map_palm.png': (2080, 1755), 'step8_catchments_map.png': (1560, 1080),
    'step9_loss_2021.png': (1408, 936), 'step9_loss_2022.png': (1408, 936), 'step9_loss_2023.png': (1408, 936),
    'step9_distances.png': (1191, 1688), 'step9_zoom_check.png': (1744, 897),
    'step5_map_forest.png': (2080, 1755),
}


def figure(asset, alt, caption, credit, cls='', needs=''):
    """An image in a white frame (the pilot's maps are drawn on white; they are not recoloured in dark
    mode), linked to the full-size file so it can be opened and zoomed."""
    w, h = IMAGE_SIZES[asset]
    return (f'<figure class="fig {cls}"{needs}><a class="frame" href="assets/{asset}">'
            f'<img src="assets/{asset}" width="{w}" height="{h}" alt="{esc(alt)}" loading="lazy" decoding="async"></a>'
            f'<figcaption>{caption}<span class="credit">{credit}</span>'
            '<span class="imgnote">Numbers printed inside the image are the pilot’s own; they are not tagged on this page. '
            f'<a href="assets/{asset}">Open the full-size image</a> to zoom in.</span>'
            '</figcaption></figure>')


BOUNDARY = ('Boundary: geoBoundaries, from OpenStreetMap (Wambacher), © OpenStreetMap contributors, '
            '<abbr title="Open Database License">ODbL</abbr>.')
OSM = 'Roads: © OpenStreetMap contributors, <abbr title="Open Database License">ODbL</abbr>.'


def hansen(p):
    return ('Forest data: Hansen et al. (' + yr('2013') + ') Science; Hansen/UMD/Google/USGS/NASA, '
            + p.span('s0.hansen_dataset_version') + ', ' + lic('CC BY 4.0') + '.')


def uml():
    return ('Mill points: the firms’ published lists and eMSPO; other points from the Universal Mill List '
            '(Rainforest Alliance; WRI/GFW), unverified, no licence stated.')


# ------------------------------------------------------------ pipeline diagram (HTML and CSS)

# The diagram is HTML, not a drawing, so its text keeps the page's font size on a phone (at least 12 px)
# and wraps inside its box. Each lane: three boxes (each a list of parts: text, ['n', id] for a tagged
# number, ['nt', reason, text] for a no-tag item, ['path', name] for a folder or file name) and a style
# for the lane, or a style per box: 'data' solid, 'gap' dashed (could not be built), 'chk' dotted
# (checks or pictures only).
LANES = [
    (['Hansen forest change'], ['Sarawak forest clips'], ['Forest loss by mill'], 'data'),
    (['CHIRPS rainfall'], ['Monthly rainfall clips'], ['Rainfall by mill'], 'data'),
    (['Boundary, mill lists, UML'], ['Boundary, ', ['n', 's1.mills_all_firms'], '\u2011mill tables'],
     ['Catchments (', ['n', 's4.mill_points_that_set_the_catchments'], ' points)'], 'data'),
    (['eMSPO, RSPO, annual reports'], ['Certificate records'], ['Certification by mill'], 'data'),
    ([['n', 's2.annual_reports_used'], ' annual reports'], ['Typed figures, page index'], ['Yield, debt-to-equity'],
     'data'),
    (['CBP and EU lists'], ['Sanctions searches'], ['Sanctions: history missing'], ('data', 'data', 'gap')),
    (['ENCORE ratings'], ['ENCORE extract'], ['ENCORE ratings (static)'], 'data'),
    (['CIFOR peat not obtained'], ['No peat clip (gap)'], ['Peat: missing'], 'gap'),
    (['OpenStreetMap roads'], ['Sarawak roads'], ['Used for the grid only'], 'data'),
    ([['nt', 'name or identifier', 'Sentinel-2'], ', Forest Watch'], ['Check files in ', ['path', 'reports/']], None,
     'chk'),
    (['Palm map (Descals)'], ['Map pictures only'], None, 'chk'),
]
HEADS = [
    ('Raw sources', 'data/raw/', ['saved in ', ['nt', 'step number', 'steps 2'], ' and ', ['nt', 'step number', '5']]),
    ('Clips, extracts', 'data/interim/', ['made in ', ['nt', 'step number', 'step 5']]),
    ('Results per firm', 'data/processed/', ['made in ', ['nt', 'step number', 'step 6']]),
]
FINALS = [
    ([['path', 'pilot_firm_year.csv']], [['n', 's3.firm_year_table_rows'], ' rows'],
     'forest loss, rainfall, certification, yield, debt, sanctions'),
    ([['path', 'pilot_static.csv']], [['n', 's3.static_table_rows'], ' rows'], 'peat, ENCORE ratings'),
    (['grid of Sarawak'], [['n', 's5.grid_cells'], ' squares'], 'forest loss, distances to mill and road; peat'),
]
EVIDENCE_LINKS = ['source register', 'method cards', 'scripts', 'check results']


def dg_path(name):
    """A folder or file name that may wrap after a slash in a narrow box."""
    head, _, tail = esc(name).rpartition('/')
    inner = head.replace('/', '/<wbr>') + ('/<wbr>' if head else '') + tail if '/' in name else esc(name)
    return f'<code class="path" data-notag="file name">{inner}</code>'


def dg_parts(blk, parts):
    out = []
    for part in parts:
        if isinstance(part, list) and part[0] == 'nt':
            out.append(nt(part[1], part[2]))
        elif isinstance(part, list) and part[0] == 'path':
            out.append(dg_path(part[1]))
        elif isinstance(part, list):
            out.append(blk.n(part[1]))
        else:
            out.append(esc(part))
    return ''.join(out)


def dg_box(blk, parts, style):
    return f'<div class="dg-box dg-{style}"><span>{dg_parts(blk, parts)}</span></div>'


def dg_arrow(style):
    """An arrow between two boxes (drawn by CSS); screen readers hear "then"."""
    return f'<span class="dg-arr dg-{style}"><span class="vh">then</span></span>'


def diagram(page):
    blk = Block(page, 'pipeline', markers=False)
    empty = '<span aria-hidden="true"></span>'
    heads = [f'<div class="dg-head"><b>{esc(title)}</b>{dg_path(folder)}<span class="dg-sub">{dg_parts(blk, sub)}'
             '</span></div>' for title, folder, sub in HEADS]
    cells = [empty.join(heads)]
    for a, b, c, lane_style in LANES:
        styles = lane_style if isinstance(lane_style, tuple) else (lane_style,) * 3
        row = ''
        for i, box in enumerate((a, b, c)):
            if i > 0:
                row += dg_arrow(styles[i]) if box is not None else empty
            row += dg_box(blk, box, styles[i]) if box is not None else empty
        cells.append(row)
    finals = ''.join(f'<div class="dg-box dg-final"><b>{dg_parts(blk, title)}</b> {dg_parts(blk, count)}'
                     f'<span class="dg-in">{esc(inputs)}</span></div>' for title, count, inputs in FINALS)
    links = ''.join(f'<li>{esc(x)}</li>' for x in EVIDENCE_LINKS)
    down = '<span class="dg-down" aria-hidden="true"></span>'
    chart = (
        '<div class="dg">'
        f'<div class="dg-grid">{"".join(cells)}</div>'
        f'<p class="dg-mid">Final files, made in {stp("steps 7–9")}</p>{down}'
        f'<div class="dg-finals">{finals}</div>{down}'
        f'<div class="dg-box dg-final dg-ev"><b>{dg_path("evidence.csv")}: {blk.n("s3.evidence_file_rows")} rows,</b> '
        f'a row for each value of both tables, each pointing to:<ul class="dg-links">{links}</ul></div>'
        '<ul class="dg-legend" aria-label="Line styles">'
        '<li><span class="dg-key dg-data"></span>data</li>'
        '<li><span class="dg-key dg-gap"></span>gap (not built)</li>'
        '<li><span class="dg-key dg-chk"></span>checks or pictures</li></ul>'
        '</div>')
    words = (
        '<details class="dg-words"><summary>The diagram in words</summary><ol>'
        '<li><b>Raw sources</b> (' + path('data/raw/') + ', saved in ' + stp('steps 2') + ' and ' + stp('5')
        + '): Hansen forest change, CHIRPS rainfall, the Sarawak boundary, the firms’ mill lists, the '
        'Universal Mill List, eMSPO and RSPO records, ' + blk.n('s2.annual_reports_used') + ' annual reports, '
        'the US and EU sanctions lists, ENCORE, OpenStreetMap roads. The CIFOR peat map could not be obtained. '
        + ident('Sentinel-2') + ' images and the Global Forest Watch map were used only for checks; the palm map only for '
        'pictures.</li>'
        '<li><b>Clips and extracts</b> (' + path('data/interim/') + ', ' + stp('step 5') + '): the forest and '
        'rainfall layers cut to Sarawak, the ' + blk.n('s1.mills_all_firms') + ' mills, the figures typed from '
        'the reports with their pages, certificate records, sanctions searches, the ENCORE extract, the roads. '
        'No peat clip.</li>'
        '<li><b>Results per firm</b> (' + path('data/processed/') + ', ' + stp('step 6') + '): the catchments '
        'drawn from ' + blk.n('s4.mill_points_that_set_the_catchments') + ' mill points, then forest loss and '
        'rainfall by mill, certification by mill and year, yield, debt-to-equity, the sanctions search.</li>'
        '<li><b>Final files</b> (' + stp('steps 7–9') + '): ' + path('pilot_firm_year.csv') + ' ('
        + blk.n('s3.firm_year_table_rows') + ' rows), ' + path('pilot_static.csv') + ' ('
        + blk.n('s3.static_table_rows') + ' rows), the grid of Sarawak (' + blk.n('s5.grid_cells')
        + ' squares), and ' + path('evidence.csv') + ' (' + blk.n('s3.evidence_file_rows')
        + ' rows, each pointing to the source register, a method card, a script and a check result).</li>'
        '</ol></details>')
    return blk.wrap('<figure class="dg-fig" aria-labelledby="dg-title"><figcaption class="dg-title" id="dg-title">'
                    'How the raw sources became the final files</figcaption>' + chart + '</figure>' + words)


# ------------------------------------------------------------ sections

def head_of_section(num, anchor, title, message):
    return (f'<section id="{anchor}" aria-labelledby="{anchor}-h"><h2 id="{anchor}-h">'
            f'<span class="secno" data-notag="section number">{num}</span> {esc(title)}</h2>'
            f'<p class="message">{message}</p>')


def firm_name(p, fid):
    return [f for f in p.L['firms'] if f['firm_id'] == fid][0]['name']


def s1(p):
    b = Block(p, 's1-main')
    n = b.n
    firms = p.L['firms']
    names = ', '.join(t(f['name']) + f' ({short})' for f, (_, short, _) in zip(firms, FIRMS))
    body = (
        '<h3>The question</h3>'
        '<p>Can the whole chain be built once, from raw public sources to a small table, with a record of '
        'where every value came from? The pilot counts as a success if every step from download to table can '
        'be followed and repeated, even where a measure could not be built, as long as the missing piece is '
        'written down.</p>'
        '<h3>The scope</h3><ul>'
        f'<li>{n("s1.firms")} palm oil growers listed on the stock exchange: {names}.</li>'
        f'<li>Their {n("s1.mills_all_firms")} palm oil mills: SOP {n("s1.mills_sop")}, '
        f'Ta Ann {n("s1.mills_ta_ann")}, SPB {n("s1.mills_spb")}.</li>'
        '<li>A single region: the state of Sarawak, in Malaysia.</li>'
        f'<li>The years {n("s1.first_year")}–{n("s1.last_year")}.</li></ul>'
        '<h3>How the firms were chosen</h3>'
        f'<p>Sarawak has {n("s1.listed_growers_screened")} growers listed on the stock exchange whose mills are all '
        f'in the state. They were compared on how much of their data was public and usable, and {n("s1.firms")} '
        'were chosen.</p>'
        '<h3>What was measured and how</h3>'
        f'<p>{n("s1.features")} measures (the pilot calls them features) in {n("s1.feature_families")} groups, '
        'which the pilot calls families: land and maps, climate, dependence on nature, operations, rules and bans, '
        'and finance (section ' + sec('4') + '). The work ran in ' + n('s1.steps_in_the_pilot_plan') + ' steps, and each step was '
        'checked and approved before the next step started.</p>'
        '<h3>What came out</h3><ul>'
        f'<li>A firm-year table with {n("s1.rows_in_the_firm_year_table")} rows: each firm in each year.</li>'
        f'<li>A table of values that do not change by year, with {n("s3.static_table_rows")} rows.</li>'
        f'<li>A grid of {n("s5.cell_size_km")} squares covering Sarawak.</li>'
        f'<li>An evidence record for each of the {n("s1.values_with_an_evidence_row")} values in both tables.</li></ul>'
        '<h3>The short answer</h3>'
        f'<p>{n("s1.features_built_with_or_without_flags")} of the {n("s1.features")} features were built: '
        f'{n("s1.features_built_without_a_flag")} without a warning flag and {n("s1.features_built_with_flags")} '
        f'with flags. {n("s1.features_that_are_gaps")} are gaps. In the pilot’s words, the data turned out to be '
        '“less usable than it is collectable” (section ' + sec('8') + ').</p>'
        '<div class="keep"><p><b>Keep in mind.</b> This is a test of the method, not a dataset for use. The firms '
        'were chosen because their data was available; they do not stand for the industry. The findings are '
        'waiting for a decision (section ' + sec('9') + ').</p></div>')
    mills = Block(p, 's1-mills')
    rows = ''.join(f'<tr><td>{t(m["firm"])}</td><td>{t(m["name"])}</td></tr>' for m in p.L['mills'])
    mills_html = mills.wrap(
        f'<h3>The {mills.n("s1.mills_all_firms")} mills</h3>'
        '<p>Firm and mill name, in the pilot’s order. Map positions are not listed here.</p>'
        f'<div {TBL} aria-label="The mills by firm"><table><thead><tr><th scope="col">Firm</th><th scope="col">Mill</th></tr></thead>'
        f'<tbody>{rows}</tbody></table></div>')
    return (head_of_section('1', 'what-we-did', 'What we did',
                            'The pilot tested, on a small scale, whether data about palm oil growers can be '
                            'collected from public sources, built into tables, and traced back to where every value '
                            'came from.')
            + b.wrap(body) + mills_html
            + details(path('docs/PILOT_PLAN.md') + ' (Scope, Features, Steps)', path('reports/step3_candidates.md'),
                      path('reports/step10_findings.md') + ' ' + sec('§1'),
                      path('data/interim/firm1_mills.csv'), path('firm2_mills.csv'), path('firm3_mills.csv'),
                      path('progress_log.md') + ' (Current status)')
            + '</section>')


TOPICS = [
    ('Forest', 'Hansen Global Forest Change: tree cover and yearly tree-cover loss, from satellite'),
    ('Rainfall', 'CHIRPS: monthly rainfall'),
    ('Peat', 'CIFOR Global Wetlands: could not be obtained'),
    ('Dependency on nature', 'ENCORE ratings'),
    ('Certification', 'eMSPO certified-entity list, RSPO registry, and the firms’ annual reports'),
    ('Mill lists', 'the firms’ websites'),
    ('Import bans and sanctions', 'US Customs and Border Protection (CBP) Withhold Release Orders list, and the '
                                  'EU consolidated financial sanctions list'),
    ('Region boundary', 'geoBoundaries'),
    ('Roads', 'OpenStreetMap'),
    ('Mill points used to draw catchments', 'Universal Mill List'),
]


def s2(p):
    b = Block(p, 's2-main')
    n = b.n
    topics = ''.join(f'<tr><th scope="row">{esc(k)}</th><td>{esc(v)}</td></tr>' for k, v in TOPICS)
    topics += (f'<tr><th scope="row">Yield and debt</th><td>{n("s2.annual_reports_used")} annual reports, '
               'a report for each firm and year</td></tr>'
               '<tr><th scope="row">Map pictures only</th><td>Descals et al. ' + yr('2024')
               + ' oil palm map</td></tr>'
               '<tr><th scope="row">Checks only</th><td>Copernicus ' + ident('Sentinel-2')
               + ' satellite images and the Global Forest Watch map</td></tr>')
    body = (
        '<ul>'
        f'<li><b>{n("s2.sources_registered")} sources</b> in the register: {n("s2.sources_downloaded")} downloaded; '
        f'{n("s2.sources_that_could_not_be_obtained")} could not be obtained (the peat map); '
        f'{n("s2.sources_used_only_for_checks")} used only for checks on its website (Global Forest Watch); '
        f'{n("s2.sources_of_the_two_firms_not_chosen")} belong to the candidate firms that were not chosen.</li>'
        f'<li><b>The download log</b> has {n("s2.download_records_in_the_log")} entries. '
        f'{n("s2.files_kept")} files were kept (about {n("s2.size_of_the_kept_downloads")}, in '
        f'{n("s2.raw_source_folders")} folders); {n("s2.files_kept_as_header_only")} of them holds only its file '
        f'header. {n("s2.rainfall_files_clipped_then_deleted")} monthly rainfall files were cut down to Sarawak and '
        'then deleted, because they were too large to keep; '
        f'{n("s2.satellite_image_window_reads")} entries are small pieces read from satellite images.</li></ul>'
        '<h3>What each source gave</h3>'
        f'<div {TBL} aria-label="What each source gave"><table><thead><tr><th scope="col">Topic</th><th scope="col">Source</th></tr></thead>'
        f'<tbody>{topics}</tbody></table></div>'
        '<div class="keep"><p><b>Licences.</b> Not checked by the pilot for the annual reports, the firms’ websites '
        'and the ' + ident('Sentinel-2') + ' images. No licence is stated for eMSPO, the RSPO registry and the '
        'Universal Mill List; the pilot used them with credit. The CIFOR peat map allows research and educational '
        'use only; it is named here only as the gap. The raw files, annual-report pages and personal data are '
        'not published on this page.</p></div>')
    srcs = Block(p, 's2-sources')
    rows = ''.join(f'<tr><td>{t(s["name"])}</td><td>{t(s["licence"])}</td><td>'
                   + (t(s['date_downloaded'], form='date') if s['date_downloaded']['value'] else 'not downloaded')
                   + '</td></tr>' for s in p.L['sources'])
    table = srcs.wrap(
        f'<details><summary>All {srcs.n("s2.sources_registered")} registered sources, with the licence as '
        'recorded</summary>'
        f'<div {TBL} aria-label="Registered sources"><table class="small"><thead><tr><th scope="col">Source</th><th scope="col">Licence '
        '(as recorded)</th><th scope="col">Downloaded</th></tr></thead>'
        f'<tbody>{rows}</tbody></table></div></details>')
    fig = Block(p, 's2-fig')
    figure_html = fig.wrap(figure(
        'step5_map_palm.png',
        'Map of Sarawak showing industrial oil palm in blue and smallholder oil palm in orange, SOP’s mills as '
        'black dots, and hatched areas where the palm map has no data.',
        'Oil palm extent in Sarawak, with SOP’s mills. The palm map is used only for pictures. It covers '
        + fig.n('s2.share_of_sarawak_covered_by_the_palm_map') + ' of Sarawak (hatched areas have no data). '
        'Only SOP’s mills are shown, with the Sepakau mill at the firm’s map point that was later replaced '
        + rid('R028') + '.',
        'Palm data: Descals, A. (' + yr('2024') + '), Global oil palm extent and planting year from '
        + yr('1990') + ' to ' + yr('2021') + ', ' + fig.n('s0.descals_oil_palm_dataset_version') + ', Zenodo, '
        'DOI ' + fig.n('s0.descals_oil_palm_doi') + ', ' + lic('CC BY 4.0') + '; ' + fig.n('s3.palm_map_tiles_clipped')
        + ' tiles clipped to Sarawak. ' + BOUNDARY))
    return (head_of_section('2', 'sources', 'Sources',
                            'Everything came from public sources, and each source was registered with its link, '
                            'version, licence and download date before it was used.')
            + b.wrap(body) + table + figure_html
            + details(path('source_register.csv'), path('data/raw_files.csv'), path('reports/step5_raw_data.md'),
                      path('reports/step10_findings.md') + ' ' + sec('§2'))
            + '</section>')


def s3(p):
    b = Block(p, 's3-main')
    n = b.n
    steps = (
        '<ol class="layers">'
        '<li><b>Raw downloads</b> (' + path('data/raw/') + ', logged in ' + path('data/raw_files.csv')
        + '): saved once and never edited.</li>'
        '<li><b>Clips and extracts</b> (' + path('data/interim/') + '): the satellite and rainfall layers cut '
        f'to Sarawak (tree cover, year of loss, palm extent from {n("s3.palm_map_tiles_clipped")} map tiles, and '
        f'monthly rainfall for {n("s3.rainfall_months_period")}: {n("s3.monthly_rainfall_layers_clipped")} '
        'monthly layers, no missing months); the mill tables; the figures typed from the annual reports, with '
        'their page numbers; certificate records; sanctions searches; the ENCORE extract; the roads.</li>'
        '<li><b>Results per firm</b> (' + path('data/processed/') + ', a set of files for each firm): forest loss by mill, '
        'rainfall by mill, certification by mill and year, yield, debt-to-equity and the sanctions search; then '
        'a firm-year table and a static table for each firm.</li>'
        '<li><b>Final tables</b>:<ul>'
        f'<li>{path("pilot_firm_year.csv")}: {n("s3.firm_year_table_rows")} rows × '
        f'{n("s3.firm_year_table_columns")} columns. {n("s3.firm_year_values")} values: '
        f'{n("s3.firm_year_values_filled")} filled, {n("s3.firm_year_values_missing")} missing.</li>'
        f'<li>{path("pilot_static.csv")}: {n("s3.static_table_rows")} rows × {n("s3.static_table_columns")} '
        f'columns. {n("s3.static_values")} values, of which {n("s3.static_values_missing")} are missing.</li>'
        f'<li>{path("evidence.csv")}: {n("s3.evidence_file_rows")} rows × {n("s3.evidence_file_columns")} '
        'columns.</li>'
        '<li>The grid (section ' + sec('5') + ').</li></ul></li></ol>')
    body = (
        steps +
        '<h3>How missing values are written</h3>'
        '<p>As an empty cell, never as zero, and each has a recorded reason. “NO_DEPENDENCY” is an ENCORE rating '
        '(“no dependency”), not a missing value.</p>'
        '<h3>Why a separate static table</h3>'
        '<p>Values that do not change by year (peat, ENCORE) are kept apart, so that such a value is not repeated '
        'as if it were measured every year.</p>'
        '<h3>Tools and records</h3><ul>'
        f'<li>{n("s3.python_scripts_at_the_time_of_the_findings_report")} Python programs, '
        f'{n("s3.runner_scripts")} scripts that run them in order, and {n("s3.package_lists")} lists of the software '
        'they need.</li>'
        f'<li>Rebuilding the firm tables gave {n("s3.firm_table_rebuild_outputs_identical")} identical outputs in '
        f'{n("s3.firm_table_rebuild_builds")} builds; rebuilding the grid gave '
        f'{n("s3.grid_rebuild_outputs_identical")} identical outputs in {n("s3.grid_rebuild_builds")} builds.</li>'
        f'<li>{n("s3.method_cards")} method cards (a short note per measure on how it was made); a list that '
        f'describes each measure and each grid column ({n("s3.feature_dictionary_rows")} rows, '
        f'{n("s3.feature_dictionary_rows_for_grid_columns")} of them for the grid); a list of checks with '
        f'{n("s3.check_register_rows_per_firm")} rows per firm.</li>'
        f'<li>A log of {n("s3.review_items")} questions that needed a decision: {n("s3.review_items_decided")} '
        'decided.</li></ul>'
        '<div class="keep"><p><b>Keep in mind.</b> The raw files are not published. The grid has no evidence record '
        'for each value; it is described by its column list and its method card instead ' + rid('R053') + '.</p></div>')
    return (head_of_section('3', 'raw-to-final', 'From raw data to the final tables, step by step',
                            'The data moved from raw downloads, through cut-down copies and results for each firm, to '
                            'the final tables. Each time the scripts were run again, they produced exactly the same '
                            'files.')
            + diagram(p) + b.wrap(body)
            + details(path('data/processed/README_dataset.md'), path('scripts/step8_run_all.sh'),
                      path('scripts/step9_run_all.sh'), path('reports/step6_checksheet.md'),
                      path('reports/step8_checksheet.md'), path('progress_log.md') + ' (' + stp('Steps 4–9') + ')',
                      path('feature_dictionary.csv'))
            + '</section>')


def feature_card(p, f, what, check, extra_notes=()):
    b = Block(p, f'feat-{f["number"]}')
    needs = b.needs(*extra_notes) if extra_notes else ''
    verdict = f['verdict']['value'].lower()
    cls = 'gap' if verdict == 'gap' else ('flag' if 'flag' in verdict else 'built')
    inner = (f'<h3>{t(f["feature"])}</h3>'
             f'<p class="verdict v-{cls}">Verdict: {t(f["verdict"])}</p>'
             f'<p><b>What it is.</b> {what(b)}</p>'
             f'<p><b>How it was checked.</b> {check(b)}</p>'
             f'<p class="pilot-note"><b>The pilot’s main reason:</b> {t(f["main_reason"])}</p>')
    return b.wrap(inner, cls='card blk', tag='article', needs=needs)


def s4(p):
    b = Block(p, 's4-catch')
    n = b.n
    catch = b.wrap(
        '<h3>First, mill catchments</h3>'
        '<p>Forest loss and rainfall are measured around each firm’s mills. Each mill gets the land that is closer '
        'to it than to any other mill point (a “tessellation”), and the map is cut at the Sarawak border. The '
        f'points are {n("s4.mill_points_that_set_the_catchments")} mill points: the firms’ '
        f'{n("s4.firm_mills_among_the_points")} mills and {n("s4.universal_mill_list_points_among_the_points")} '
        'points from the Universal Mill List (list points within '
        f'{n("s4.uml_points_dropped_near_a_firm_mill_km")} of a firm mill were dropped). A firm’s catchments '
        f'are merged into a single area: SOP {n("s4.merged_catchment_area_km2_sop")}, Ta Ann '
        f'{n("s4.merged_catchment_area_km2_ta_ann")}, SPB {n("s4.merged_catchment_area_km2_spb")}.</p>')
    fig = Block(p, 's4-fig')
    fig_html = fig.wrap(figure(
        'step8_catchments_map.png',
        'Map of Sarawak divided into mill catchments. The catchments of the pilot firms’ mills are shaded blue '
        'and labelled with their areas; other mill points are black dots.',
        f'The catchments of the {fig.n("s4.firm_mills_among_the_points")} firm mills (blue), in the shared map of '
        f'{fig.n("s4.mill_points_that_set_the_catchments")} mill points. Some labels overlap.',
        uml() + ' ' + BOUNDARY))
    F = {f['number']: f for f in p.L['features']}
    cards = [
        feature_card(p, F['1'],
                     lambda b: ('Hectares of tree-cover loss each year inside the firm’s merged catchment, where '
                                f'“forest” means more than {b.n("s4.tree_cover_threshold_for_forest")} tree cover in '
                                + yr('2000') + '.'),
                     lambda b: (f'{b.n("s4.forest_loss_check_values_matching_gfw")} yearly values matched the Global '
                                'Forest Watch website, which shows only the first '
                                f'{b.n("s4.forest_loss_check_gfw_precision")} digits of each number (differences '
                                f'{b.n("s4.forest_loss_check_range_of_differences")}), for '
                                f'{b.n("s4.forest_loss_check_cells_per_firm_compared")} catchments per firm. Satellite '
                                'close-ups of the loss areas, in the pilot’s words: '
                                f'{b.n("s4.forest_loss_check_satellite_patches")}.'),
                     extra_notes=['forest_loss']),
        feature_card(p, F['2'],
                     lambda b: 'The share of the catchment that lies on peat.',
                     lambda b: 'Not checked: the peat map could not be downloaded, and no substitute was used.',
                     extra_notes=['peat_missing']),
        feature_card(p, F['3'],
                     lambda b: ('Each year’s rainfall minus the ' + b.n('s4.rainfall_baseline') + ' average for the '
                                'same place, in mm, averaged over the firm’s mills.'),
                     lambda b: (f'A second, separate calculation found {b.n("s4.rainfall_check_mill_years_off")} '
                                f'mill-years that differed by more than {b.n("s4.rainfall_check_tolerance_mm")}.')),
        feature_card(p, F['4'],
                     lambda b: (f'{b.n("s4.encore_ratings_per_firm")} ratings of how much an activity depends on '
                                f'nature: {b.n("s4.encore_ecosystem_services")} kinds of benefit from nature (ENCORE '
                                'calls them “ecosystem services”) × '
                                f'{b.n("s4.encore_activities")} activities (growing perennial crops; making vegetable '
                                'and animal oils and fats), from very high to very low, or no dependency. '
                                '<span class="licence-tag">ENCORE content, ' + lic('CC BY-SA 4.0') + '</span>'),
                     lambda b: (f'ENCORE’s ratings file and its detail file agree for all '
                                f'{b.n("s4.encore_check_ratings_equal_between_two_files")} ratings, and all '
                                f'{b.n("s4.encore_check_values_passing")} values in the tables passed their check.')),
        feature_card(p, F['5'],
                     lambda b: ('The share of the firm’s mills that were certified (MSPO or RSPO) on '
                                + b.n('s4.certification_day') + ' of each year.'),
                     lambda b: (f'eMSPO records equal the live website '
                                f'({b.n("s4.certification_check_emspo_fields_equal_to_the_live_site_sop_step")} and '
                                f'{b.n("s4.certification_check_emspo_fields_equal_to_the_live_site_ta_ann_a")} '
                                f'fields); {b.n("s4.certification_check_result")} pass. These checks test the method; '
                                'the evidence itself is weak (section ' + sec('8') + ').'),
                     extra_notes=['certification_firm_reported']),
        feature_card(p, F['6'],
                     lambda b: ('Tonnes of fresh fruit bunches (FFB) harvested per hectare, exactly as each annual '
                                'report prints it.'),
                     lambda b: (f'{b.n("s4.yield_check_result")} pass; {b.n("s4.yield_check_restatements_found")} '
                                'restatement found.'),
                     extra_notes=['ffb_not_comparable']),
        feature_card(p, F['7'],
                     lambda b: ('The number of import bans (US Withhold Release Orders) and EU financial sanctions '
                                'in force against the firm.'),
                     lambda b: ('Searches of the current US and EU lists found no match, but the lists do not show '
                                + yr('2021') + '–' + yr('2023') + ', so the count is missing.'),
                     extra_notes=['wro_missing']),
        feature_card(p, F['8'],
                     lambda b: ('Borrowings divided by total equity, for the whole group, from each year’s annual '
                                'report.'),
                     lambda b: (f'Every figure that is not zero was found again on its report page '
                                f'({b.n("s4.debt_to_equity_check_figures_found")}). All '
                                f'{b.n("s4.debt_to_equity_check_result")} values pass.'),
                     extra_notes=['dte_whole_group']),
    ]
    return (head_of_section('4', 'features', 'The measures (features)',
                            'Each firm is described by a set of measures. Most could be built, and each comes with the '
                            'pilot’s own warning about what it can and cannot show.')
            + catch + fig_html + '<div class="cards">' + ''.join(cards) + '</div>'
            + details(path('feature_dictionary.csv'),
                      'the method cards in ' + path('docs/methods/') + ': ' + ', '.join(path(x) for x in (
                          'forest_loss.md', 'peat_overlap.md', 'rainfall_anomaly.md', 'encore.md',
                          'certification.md', 'ffb_yield.md', 'wro_sanctions.md', 'debt_to_equity.md')),
                      path('reports/step10_findings.md') + ' ' + sec('§1') + ' and ' + sec('§3'))
            + '</section>')


def s5(p):
    b = Block(p, 's5-main')
    n = b.n
    body = (
        f'<p>The grid has {n("s5.grid_cells")} squares of {n("s5.cell_size_km")}. {n("s5.edge_cells")} of them are '
        f'edge squares, cut by the border. Together they cover {n("s5.area_of_sarawak_covered_km2")}. Each square has '
        f'{n("s5.grid_columns")} columns, including forest loss in ' + yr('2021') + ', ' + yr('2022') + ' and '
        + yr('2023') + ' (ha), the distance to the nearest mill point and to the nearest road (km), and peat, '
        f'which is empty in all {n("s5.grid_cells_with_no_peat_value_all_cells")} squares.</p>'
        f'<p>Rebuilding the grid gave identical files in {n("s3.grid_rebuild_builds")} builds.</p>')
    chk = Block(p, 's5-check')
    rows = ''
    for y in YEARS:
        rows += (f'<tr><th scope="row">{yr(y)}</th><td>{chk.n(f"s5.sarawak_forest_loss_{y}_ha")}</td>'
                 f'<td>{chk.n(f"s5.grid_forest_loss_{y}_ha")}</td>'
                 f'<td>{chk.n(f"s5.grid_minus_sarawak_forest_loss_{y}_ha")}</td>'
                 f'<td>{chk.n(f"s5.forest_loss_pixels_{y}")}</td></tr>')
    check_html = chk.wrap(
        '<h3>The check: the grid adds up to Sarawak</h3>'
        '<p>Forest loss summed over all squares was compared with the Sarawak total computed separately. The small '
        'differences come only from rounding, and both totals count the same satellite pixels (the smallest squares '
        'of the satellite map).</p>'
        f'<div {TBL} aria-label="The grid check"><table class="num"><thead><tr><th scope="col">Year</th><th scope="col">Sarawak total'
        '</th><th scope="col">Grid total</th><th scope="col">Grid minus Sarawak</th><th scope="col">Loss pixels'
        f'</th></tr></thead><tbody>{rows}</tbody></table></div>')
    roads = Block(p, 's5-roads')
    rn = roads.n
    roads_html = roads.wrap(
        '<h3>Roads and distances</h3><ul>'
        f'<li>Roads: OpenStreetMap, {rn("s5.road_ways_used")} road sections, {rn("s5.road_length_used_km")}, '
        f'{rn("s5.road_types_used")} road types. Tracks make up {rn("s5.track_length_km")}, '
        f'{rn("s5.track_share_of_road_length")} of the length. Data as of {rn("s5.road_data_date")}.</li>'
        f'<li>Distance to the nearest mill point: median {rn("s5.distance_to_mill_median_km")}, at most '
        f'{rn("s5.distance_to_mill_maximum_km")}.</li>'
        f'<li>Distance to the nearest road: median {rn("s5.distance_to_road_median_km")}, at most '
        f'{rn("s5.distance_to_road_maximum_km")}.</li>'
        f'<li>For {rn("s5.cells_whose_nearest_mill_point_is_a_uml_point")} squares '
        f'({rn("s5.share_of_cells_whose_nearest_mill_point_is_a_uml_point")}), the nearest mill point is a '
        'Universal Mill List point.</li></ul>')
    f1 = Block(p, 's5-fig-loss')
    loss_needs = f1.needs('forest_loss_sarawak')
    loss_credit = hansen(p) + ' ' + OSM + ' ' + BOUNDARY + ' ' + uml()
    loss_html = f1.wrap(
        figure('step9_loss_2021.png',
               'Map of Sarawak in square grid cells, shaded from light to dark blue by forest loss in the year, with '
               'mill points and roads.',
               'Forest loss per square in ' + yr('2021') + ', with mill points and roads.', loss_credit, cls='wide',
               needs=loss_needs)
        + '<div class="pair">'
        + figure('step9_loss_2022.png', 'The same map of forest loss per square for the next year.',
                 'Forest loss per square in ' + yr('2022') + '.', 'Credits as above.', needs=loss_needs)
        + figure('step9_loss_2023.png', 'The same map of forest loss per square for the year after.',
                 'Forest loss per square in ' + yr('2023') + '.', 'Credits as above.', needs=loss_needs)
        + '</div>')
    f2 = Block(p, 's5-fig-dist')
    dist_needs = f2.needs('uml_unverified', 'roads_snapshot', 'borders')
    dist_html = f2.wrap(
        figure('step9_distances.png',
               'Maps of Sarawak, top and bottom: the distance from each grid square to the nearest mill point, and to '
               'the nearest road, shaded in blue bands.',
               'Distance from each square to the nearest mill point (top) and to the nearest road (bottom). '
               '<span class="capnote">Note: the largest distance to a mill point in the map title ('
               + path('reports/step9_maps/step9_distances.png') + ') differs in the last decimal from the '
               + f2.n('s5.distance_to_mill_maximum_km') + ' in the grid’s method card ('
               + path('docs/methods/regional_grid.md') + '). Both are shown as the pilot has them.</span>',
               OSM + ' ' + BOUNDARY + ' ' + uml(), needs=dist_needs)
        + figure('step9_zoom_check.png',
                 'Close-up of a small area: grid squares shaded by forest loss on the left, and the satellite loss '
                 'pixels they were built from on the right.',
                 'Close-up check: the grid squares next to the satellite pixels they were made from, around the square '
                 'with the most forest loss in ' + yr('2021') + '.', hansen(p), needs=f2.needs('forest_loss_sarawak')))
    return (head_of_section('5', 'grid', 'The grid of Sarawak',
                            'A grid of square cells covers all of Sarawak, with yearly forest loss and the distances '
                            'to the nearest mill and road in each square, and its total matches the state-wide total.')
            + b.wrap(body) + check_html + roads_html + loss_html + dist_html
            + details(path('reports/step9_grid.md'), path('docs/methods/regional_grid.md'),
                      path('reports/step9_checks/grid_vs_sarawak_loss.csv'),
                      path('data/interim/osm_roads_sarawak_tag_counts.csv'),
                      path('feature_dictionary.csv') + ' (rows starting “Grid:”)')
            + '</section>')


def s6(p):
    b = Block(p, 's6-main')
    n = b.n
    body = (
        f'<p>An evidence row has {n("s6.evidence_row_columns")} columns. In plain words: the value; the source and the '
        'exact place in it (page, table or map layer); the unit; the date it refers to; the area it covers; the '
        'method card; the script; how it was checked, the result, who checked it and when; and a note.</p>'
        '<ul>'
        f'<li><b>{n("s6.evidence_rows_pass")}</b> values pass their check and <b>{n("s6.evidence_rows_fail")}</b> '
        f'fail.</li>'
        f'<li><b>{n("s6.evidence_rows_not_checked")}</b> are “not checked”: these are the missing values '
        f'({n("s6.missing_values_wro_sanctions")} import-ban and sanctions values, '
        f'{n("s6.missing_values_peat_overlap")} peat values).</li>'
        f'<li>All {n("s6.evidence_rows_with_a_recorded_check")} checks were automated self-checks. The planned '
        'manual reviews were waived, so no value was checked independently (section ' + sec('8') + ').</li></ul>')
    ex = Block(p, 's6-example')
    e = ex.n
    chain = (
        f'<h3>A worked example: SOP, debt-to-equity, {e("s6.example_firm_year")} = {e("s6.example_value_in_the_table")}'
        '</h3>'
        f'<p>The value is followed through {e("s6.links_in_the_worked_example")} links. Amounts are in thousands '
        'of Malaysian ringgit, as the report prints them.</p>'
        '<ol class="chain">'
        f'<li><b>The value in the table:</b> {e("s6.example_value_in_the_table")}, in '
        + path('data/processed/firm1_firm_year.csv') + ' (copied unchanged into the combined table '
        + path('pilot_firm_year.csv') + '), row SOP ' + yr('2022') + ', column “debt_to_equity”.</li>'
        f'<li><b>Its evidence row:</b> value {e("s6.example_value_in_the_evidence_row")}; source: the SOP Annual '
        f'Report ' + yr('2022') + f'; reference date {e("s6.example_reference_date")}; area: the whole group.</li>'
        f'<li><b>The source:</b> registered in the source register and downloaded on '
        f'{e("s6.example_report_downloaded_utc")}. A digital fingerprint of the file (' + ident('SHA-256') + ') was '
        'calculated again and still matches, so the file has not changed.</li>'
        f'<li><b>The pages:</b> the balance sheet (page {e("s6.example_balance_sheet_pdf_page")} of the file; printed '
        f'page {e("s6.example_balance_sheet_printed_page")}) shows loans and borrowings '
        f'of {e("s6.example_loans_and_borrowings_non_current_rm_000")} (non-current) and '
        f'{e("s6.example_loans_and_borrowings_current_rm_000")} (current), and total equity of '
        f'{e("s6.example_total_equity_rm_000")}. The borrowings note (page {e("s6.example_borrowings_note_pdf_page")} '
        f'of the file; printed page {e("s6.example_borrowings_note_printed_page")}) gives the line items.</li>'
        f'<li><b>The method card:</b> hire purchase ({e("s6.example_hire_purchase_counted_as_debt_rm_000")}) counts '
        f'as debt; lease liabilities ({e("s6.example_lease_liabilities_left_out_rm_000")}) are left out. '
        f'{e("s6.example_debt_rm_000")} ÷ {e("s6.example_total_equity_rm_000")} = {e("s6.example_ratio_recomputed")}, '
        f'shown as {e("s6.example_value_in_the_table")}.</li>'
        '<li><b>The scripts</b> that compute and record it: ' + path('scripts/step6_financials.py') + ' and '
        + path('scripts/step7_firm_year_table.py') + '.</li>'
        f'<li><b>The check:</b> pass (an automated check), on {e("s6.example_check_date")}. The trace was re-run on '
        f'{e("s6.example_trace_re_run_date")} and passed again.</li></ol>'
        '<p>The chain is the same for other kinds of value. Map and rainfall values lead to a map layer and a '
        'result row; certification leads to the eMSPO record or to the annual-report statement; a missing value '
        'leads to a row that gives the reason.</p>'
        '<div class="keep"><p><b>Keep in mind.</b> The annual report itself is not published here; it is cited by '
        'title, year and page.</p></div>')
    return (head_of_section('6', 'evidence', 'The evidence trail, with a worked example',
                            'Every value in both tables has an evidence row that leads to its source page, method, '
                            'script and check. Here a single value is followed link by link.')
            + b.wrap(body) + ex.wrap(chain)
            + details(path('evidence.csv'), path('reports/step10_findings.md') + ' ' + sec('§5'),
                      path('reports/step7_trace_example.md'),
                      path('reports/step10_checks/step7_trace_rerun_2026-10-24.txt'),
                      path('data/processed/firm1_debt_to_equity.csv'), path('docs/methods/debt_to_equity.md'),
                      path('source_register.csv'))
            + '</section>')


def year_table(blk, caption, idfmt, cell=None, cls='num'):
    head = ''.join(f'<th scope="col">{yr(y)}</th>' for y in YEARS)
    rows = ''
    for key, short, _ in FIRMS:
        cells = ''.join(f'<td>{cell(key, y) if cell else blk.n(idfmt.format(f=key, y=y))}</td>' for y in YEARS)
        rows += f'<tr><th scope="row">{short}</th>{cells}</tr>'
    return (f'<div {TBL} aria-label="{esc(caption)}"><table class="{cls}"><caption>{caption}</caption><thead><tr><th scope="col">Firm</th>'
            f'{head}</tr></thead><tbody>{rows}</tbody></table></div>')


ENCORE_LEVELS = [('very_high', 'Very high'), ('high', 'High'), ('moderate', 'Moderate'), ('low', 'Low'),
                 ('very_low', 'Very low'), ('no_dependency', 'No dependency (ENCORE “N/A”)')]


def encore_citation(blk):
    return ('ENCORE Partners (Global Canopy, UNEP FI, and UNEP-WCMC) (' + yr('2026') + '). ENCORE: Exploring '
            'Natural Capital Opportunities, Risks and Exposure. [On-line], '
            + blk.n('s0.encore_version_and_citation_year') + ', Cambridge, UK: ENCORE Partners. DOI '
            + blk.n('s0.encore_doi') + '.')


def s7(p):
    intro = ('<p>Each table shows the firms in the pilot’s order (SOP, Ta Ann, SPB), not ranked. Read each table '
             'with the notes under it.</p>')
    fl = Block(p, 's7-forest')
    forest = fl.wrap(
        '<h3>Forest loss</h3>' + year_table(fl, 'Forest loss in the firm’s merged catchment (hectares)',
                                            's7.forest_loss_ha_{f}_{y}')
        + '<p>The largest single catchment in each firm’s area, and its share of the firm’s forest loss:</p>'
        + f'<div {TBL} aria-label="Largest catchment"><table class="num"><caption>Largest catchment: share of the firm’s area and of its forest '
          'loss</caption><thead><tr><th scope="col">Firm</th><th scope="col">Share of area</th>'
        + ''.join(f'<th scope="col">Loss {yr(y)}</th>' for y in YEARS) + '</tr></thead><tbody>'
        + ''.join(f'<tr><th scope="row">{short}</th><td>{fl.n(f"s7.largest_catchment_cells_share_of_{pk}_area")}</td>'
                  + ''.join(f'<td>{fl.n(f"s7.largest_catchment_cells_share_of_{pk}_{y}_forest_loss")}</td>'
                            for y in YEARS) + '</tr>'
                  for _, short, pk in FIRMS)
        + '</tbody></table></div>')
    rf = Block(p, 's7-rain')
    rain = rf.wrap('<h3>Rainfall anomaly</h3>'
                   + year_table(rf, 'Rainfall compared with the average for the same place (mm; + wetter, − drier)',
                                's7.rainfall_anomaly_mm_{f}_{y}')
                   + '<p>Built without a warning flag; every mill has data in every year.</p>')
    cf = Block(p, 's7-cert')
    cert = cf.wrap(
        '<h3>Certification</h3>' + year_table(cf, 'Share of the firm’s mills certified on the last day of the year',
                                              's7.certification_{f}_{y}')
        + f'<p>How many mill-years (a mill in a given year) rest only on the firm’s own statement: SOP '
          f'{cf.n("s7.firm_reported_mill_years_sop")} of '
          f'{cf.n("s7.mill_years_in_scope_sop")}, Ta Ann {cf.n("s7.firm_reported_mill_years_ta_ann")} of '
          f'{cf.n("s7.mill_years_in_scope_ta_ann")}, SPB {cf.n("s7.firm_reported_mill_years_spb")} of '
          f'{cf.n("s7.mill_years_in_scope_spb")} ({cf.n("s7.firm_reported_mill_years_all_firms")} of '
          f'{cf.n("s7.mill_years_in_scope_all_firms")} in all).</p>')
    yf = Block(p, 's7-yield')

    def ycell(f, y):
        out = yf.n(f's7.ffb_yield_unit_as_printed_{f}_{y}')
        if f == 'ta_ann' and y == '2022':
            out += (' <small class="flag">restated in ' + ident('AR 2023') + ': '
                    + yf.n('s7.ta_ann_2022_yield_as_restated_in_ar_2023') + '</small>')
        return out
    yld = yf.wrap('<h3>FFB yield</h3>'
                  + year_table(yf, 'Fresh fruit bunches per hectare, with the unit each report prints', None, cell=ycell))
    df = Block(p, 's7-debt')
    debt = df.wrap('<h3>Debt-to-equity</h3>'
                   + year_table(df, 'Borrowings divided by total equity (whole group)', 's7.debt_to_equity_ratio_{f}_{y}'))
    wf = Block(p, 's7-wro')
    wro_needs = wf.needs('wro_missing')
    wro = wf.wrap('<h3>Import bans and sanctions</h3>'
                  + year_table(wf, 'Count of import bans and sanctions in force', None,
                               cell=lambda f, y: f'<span class="missing"{wro_needs}>missing</span>')
                  + '<p>Every cell is missing: the years were not checked, because the lists hold current entries only. '
                    'The current lists show no match.</p>')
    st = Block(p, 's7-static')
    peat_needs = st.needs('peat_missing')
    enc_rows = ''.join(
        f'<tr><th scope="row">{label}</th><td>{st.n(f"s7.encore_ratings_perennial_{lid}")}</td>'
        f'<td>{st.n(f"s7.encore_ratings_oils_{lid}")}</td></tr>' for lid, label in ENCORE_LEVELS)
    static = st.wrap(
        '<h3>Values that do not change by year</h3>'
        f'<p><b>Peat overlap:</b> <span class="missing"{peat_needs}>missing</span> for every firm.</p>'
        '<p><b>ENCORE dependency ratings</b> <span class="licence-tag">ENCORE content, ' + lic('CC BY-SA 4.0')
        + '</span>: every firm gets the same ' + st.n('s4.encore_ratings_per_firm') + ' ratings, '
        + st.n('s4.encore_no_dependency_ratings_per_firm') + ' of them “no dependency”. The ratings per activity:</p>'
        f'<div {TBL} aria-label="ENCORE ratings per activity"><table class="num"><caption>Number of ENCORE ratings at each level, per activity (the same '
        'for all firms)</caption><thead><tr><th scope="col">Rating</th><th scope="col">Growing perennial crops</th>'
        '<th scope="col">Making vegetable and animal oils and fats</th></tr></thead>'
        f'<tbody>{enc_rows}</tbody></table></div>'
        '<p class="cite">Adapted from: ' + encore_citation(st) + ' Licence: ' + lic('CC BY-SA 4.0') + '.</p>')
    lk = Block(p, 's7-linked')
    linked = lk.wrap(f'<p><b>Linked firms.</b> Ta Ann owns {lk.n("s8.ta_anns_share_of_spb")} of SPB '
                     f'({lk.n("s8.ta_anns_share_of_spb_in_2021")} in ' + yr('2021') + '), so these firms are not '
                     'independent of each other. SPB’s mills are not counted for Ta Ann.</p>')
    fig = Block(p, 's7-fig')
    fig_needs = fig.needs('forest_loss_sarawak')
    fig_html = fig.wrap(figure(
        'step5_map_forest.png',
        'Map of Sarawak showing tree cover in grey and forest loss in blue for earlier years and orange for the '
        'pilot’s years, with SOP’s mills and a small close-up panel for each mill.',
        'Tree cover and forest loss over Sarawak, with SOP’s mills. Only SOP’s mills are shown, with the Sepakau '
        'mill at the firm’s map point that was later replaced ' + rid('R028') + '.',
        hansen(p) + ' ' + BOUNDARY, needs=fig_needs))
    return (head_of_section('7', 'results', 'Results',
                            'The tables hold the values the pilot could build for ' + yr('2021') + '–' + yr('2023')
                            + '. Several of them cannot be compared between firms, so they are shown with their '
                              'warnings and not as a ranking.')
            + intro + forest + rain + cert + yld + debt + wro + static + linked + fig_html
            + details(path('data/processed/pilot_firm_year.csv'), path('data/processed/pilot_static.csv'),
                      path('evidence.csv'), path('data/processed/README_dataset.md'),
                      path('data/processed/firm{1,2,3}_certification_firm_year.csv'),
                      path('data/processed/firm{1,2,3}_ffb_yield.csv'),
                      path('data/processed/firm{1,2,3}_forest_loss_summary.csv'),
                      path('data/interim/encore_dependency_ratings.csv'))
            + '</section>')


def gap_lines(b):
    """The plain-word line for each gap. Each entry is a function, so that only the numbers of
    the item being written are entered in its block (and only their caveats are listed under it)."""
    n = b.n
    return {
        '1': lambda: 'The provider’s data portal did not respond. Peat is missing for every firm and every grid square.',
        '2': lambda: (f'The official lists hold only current entries, so the count is missing in all '
              f'{n("s8.wro_sanctions_firm_years_missing")} firm-years. The current lists show no match.'),
        '3': lambda: (f'Firm-reported mill-years: {n("s8.certification_firm_reported_mill_years_per_firm")} '
              f'({n("s8.certification_firm_reported_mill_years_all_firms")}). The statements are for the whole '
              'group, with no dates or certificate numbers per mill.'),
        '4': lambda: ('The eMSPO history service failed (the website returned a server error, “' + ident('HTTP 500')
              + f'”; {n("s8.mspo_history_mills_tried")} mills were tried), so earlier certificate periods could not '
              'be seen.'),
        '5': lambda: ('Units differ between firms. SOP’s printed yield equals its harvest divided by the area of mature '
              'palms only for ' + yr('2021') + '. For ' + yr('2022') + ' that calculation gives '
              + n('s8.sop_yield_2022_production_over_year_end_mature_area_finding_only') + ' against '
              + n('s8.sop_yield_2022_as_printed') + ' printed; for ' + yr('2023') + ', '
              + n('s8.sop_yield_2023_production_over_year_end_mature_area_finding_only') + ' against '
              + n('s8.sop_yield_2023_as_printed') + '. No conversion was made.'),
        '6': lambda: (f'Ta Ann’s yield for {yr("2022")} is {n("s8.ta_ann_2022_yield_as_printed_in_ar_2022")} in '
              f'{ident("AR 2022")}, but {n("s8.ta_ann_2022_yield_as_printed_in_ar_2023")} in {ident("AR 2023")}, '
              f'with the same production ({n("s8.ta_ann_2022_production_mt")}).'),
        '7': lambda: ('The firms name their borrowing line items differently. Hire purchase counts as debt; without it, '
              'SOP’s ratio would be ' + n('s8.sop_debt_to_equity_without_hire_purchase_2021') + ' / '
              + n('s8.sop_debt_to_equity_without_hire_purchase_2022') + ' / '
              + n('s8.sop_debt_to_equity_without_hire_purchase_2023') + ' (' + yr('2021') + ' / ' + yr('2022')
              + ' / ' + yr('2023') + '). The figures cover the whole group.'),
        '8': lambda: (f'Every firm gets the same {n("s8.encore_ratings_the_same_for_all_firms")} ratings '
              f'({n("s8.encore_no_dependency_ratings_per_firm")} of them “no dependency”), so ENCORE shows no '
              'difference between firms.'),
        '9': lambda: (f'{n("s8.satellite_patches_showing_logging_not_clearing")} satellite patches showed logging roads and '
              'gaps in the tree cover, not cleared land. SOP’s Metanik mill has a catchment of '
              f'{n("s8.metanik_catchment_area_km2")}, '
              f'{n("s8.metanik_share_of_sops_area")} of SOP’s merged area ({n("s8.sops_merged_catchment_area_km2")}), '
              f'and gives {n("s8.metanik_share_of_sops_forest_loss_2021")} / '
              f'{n("s8.metanik_share_of_sops_forest_loss_2022")} / {n("s8.metanik_share_of_sops_forest_loss_2023")} '
              'of SOP’s forest loss in ' + yr('2021') + '–' + yr('2023') + '.'),
        '10': lambda: (f'The comparison with Global Forest Watch covers {n("s8.gfw_comparison_catchments_covered")} catchments. '
               'The website shows only rounded numbers, so the pilot could not tell whether it counts forest as “more '
               'than” or “at least” the tree-cover threshold. Either way, the difference is at most '
               f'{n("s8.gfw_comparison_largest_possible_threshold_effect_on_forest_loss")}.'),
        '11': lambda: (f'{n("s8.uml_points_among_the_mill_points")} of the {n("s8.mill_points_in_all")} mill points come from '
               f'the Universal Mill List, with positions as of {n("s8.uml_positions_date")}. They set the edges of the '
               f'firms’ catchments, and they are the nearest mill point for '
               f'{n("s8.grid_cells_with_a_uml_point_as_nearest_mill")} of {n("s8.grid_cells_in_all")} grid squares '
               f'({n("s8.share_of_grid_cells_with_a_uml_point_as_nearest_mill")}).'),
        '12': lambda: (f'The roads are an OpenStreetMap snapshot of {n("s8.roads_snapshot_date")}, not ' + yr('2021') + '–'
               + yr('2023') + f'. Tracks are {n("s8.track_share_of_road_length")} of the road length. Roads and mills '
               'across the border are not used.'),
        '13': lambda: (f'SPB is partly owned by Ta Ann ({n("s8.ta_anns_share_of_spb")}; '
               f'{n("s8.ta_anns_share_of_spb_in_2021")} in ' + yr('2021') + '), so these firms are linked.'),
        # The only mention of Claude Code on the page (CLAUDE.md, Step 4 decision 11).
        '14': lambda: ('All checks were done by the AI coding assistant (Claude Code) that built the pipeline; the planned '
               'manual reviews were waived, so no value was checked independently. This covers all '
               f'{n("s8.checked_values_all_self_checks")} checked values.'),
        '15': lambda: (f'Not checked: the licences of the {n("s8.annual_reports_with_licences_not_checked")} annual reports, '
               'the ' + ident('Sentinel-2') + ' licence and the site terms of the Global Forest Watch map. No licence '
               'is stated for RSPO, eMSPO and the Universal Mill List; they were used with credit.'),
        '16': lambda: (f'The palm map covers {n("s2.share_of_sarawak_covered_by_the_palm_map")} of Sarawak and is used only '
               'for pictures. Mill points and roads are recent positions, not those of the pilot’s years.'),
    }


# Gap titles written for the page instead of the pilot's title: the pilot's title for item 14 names
# Claude Code, which the page names only once, in that item's line (CLAUDE.md, Step 4 decision 11).
GAP_TITLES_FOR_PAGE = {'14': 'Self-checks'}


def s8(p):
    items = []
    for g in p.L['gaps']:
        b = Block(p, f'gap-{g["number"]}')
        line = gap_lines(b)[g['number']]()
        title = esc(GAP_TITLES_FOR_PAGE[g['number']]) if g['number'] in GAP_TITLES_FOR_PAGE else t(g['issue'])
        items.append(b.wrap(f'<p class="gap-title">{title} {rids(g["review_ids"])}</p><p>{line}</p>',
                            cls='blk gap', tag='li'))
    hb = Block(p, 's8-head')
    head = hb.wrap(f'<p>{hb.n("s1.features_that_are_gaps")} features could not be built, and the pilot records '
                   f'{hb.n("s8.weak_points_recorded")} weak points in all. None of them was filled, estimated or worked '
                   'around. These are the pilot’s own findings, in its order, with its title for each (the self-check '
                   'item’s title is shortened here) and the review items in small grey print.</p>')
    return (head_of_section('8', 'gaps', 'Gaps and findings',
                            'Some features could not be built, and the pilot lists every weak point it found. None '
                            'was filled, estimated or worked around.')
            + head + '<ol class="gaps">' + ''.join(items) + '</ol>'
            + details(path('reports/step10_findings.md') + ' ' + sec('§4'), path('review_queue.csv'),
                      path('docs/methods/*.md') + ' (Known limitations)', path('progress_log.md')
                      + ' (Issues of ' + stp('Steps 2–9') + ')')
            + '</section>')


def pending_badge(p, rid_):
    d = [x for x in p.L['decisions_pending'] if x['item_id'] == rid_][0]
    label = 'decision pending' if d['status'] == 'pending' else 'decided'
    return f'<span class="badge badge-{d["status"]}">{label} {rid(rid_)}</span>'


# Left out of the full-build list on the page: the hours item, with the hours section (CLAUDE.md, Step 4 decision 10).
FULL_BUILD_LEFT_OUT = {'Time records'}


def s9(p):
    b = Block(p, 's9-main')
    opts = ''.join(f'<li>{t(o["text"], bold_prefix=True)}</li>' for o in p.L['decision_options'])
    changes = ''.join(f'<li>{t(c["text"], bold_prefix=True)}</li>' for c in p.L['full_build_changes']
                      if c['title'] not in FULL_BUILD_LEFT_OUT)
    pend = ''.join(f'<li>{t(d["item"])} {pending_badge(p, d["item_id"])}</li>' for d in p.L['decisions_pending'])
    body = (
        f'<p>The findings report lists {b.n("s9.options_for_the_decision")} options, without a recommendation. '
        'They can be combined. This page takes no side.</p>'
        f'<ol class="options">{opts}</ol>'
        f'<h3>The open decision</h3><ul class="pending">{pend}</ul>'
        '<h3>What would need to change for a full build</h3>'
        '<p>Listed in the pilot, not decided. In the pilot’s own words; “section ' + sec('7.5') + '” is this list '
        'in the findings report.</p>'
        f'<ul class="changes small">{changes}</ul>')
    return (head_of_section('9', 'next', 'Next decisions',
                            'The pilot ends with a decision that has not been made yet: scale up, change the plan, or '
                            'stop. ' + pending_badge(p, 'R057'))
            + b.wrap(body)
            + details(path('reports/step10_findings.md') + ' ' + sec('§7.5') + ' and ' + sec('§8'),
                      path('review_queue.csv') + ' (' + rid('R057') + ')',
                      path('progress_log.md') + ' (Current status)')
            + '</section>')


GLOSSARY = [
    ('Catchment', 'The land that belongs to a mill on the map: every place closer to that mill than to any other mill '
                  'point. A firm’s catchment is all its mills’ catchments merged.'),
    ('Tessellation', 'The way the catchments are drawn: the map is split into areas, an area for each mill point, '
                     'holding the places nearest to that point.'),
    ('Mill point', 'The map position of a palm oil mill, from the firms and eMSPO, or from the Universal Mill List.'),
    ('Universal Mill List (UML)', 'A public list of palm oil mill positions (Rainforest Alliance; WRI/GFW). '
                                  'Unverified; no licence stated.'),
    ('Feature', 'A single measure in the tables, for example forest loss or debt-to-equity.'),
    ('Family', 'A group of features: geospatial, climate, dependency, operational, regulatory, financial.'),
    ('Firm-year', 'A firm in a given year: a row of the main table.'),
    ('Static value', 'A value that does not change by year (peat overlap, ENCORE), kept in its own table.'),
    ('Evidence row', 'A line in the evidence file for a single value: where it came from, how it was made, how it '
                     'was checked.'),
    ('Source tag', 'On this page: the file, row and column in the pilot where a number comes from.'),
    ('Gap', 'A feature that could not be built. Recorded, not filled.'),
    ('Flag', 'A warning the pilot attached to a value.'),
    ('Missing', 'An empty value with a recorded reason. Not zero.'),
    ('Not checked', 'The check status of a missing value.'),
    ('Self-check', 'A check done by the same party that built the value, not by an independent reviewer.'),
    ('Tree-cover loss (Hansen)', 'Satellite-detected loss of tree cover from any cause, including clearing, '
                                 'replanting and logging.'),
    ('ENCORE rating', 'How much an activity depends on a part of nature: very high to very low, or no dependency.'),
    ('NO_DEPENDENCY', 'ENCORE’s “N/A”: the activity does not depend on that service. A rating, not a missing value.'),
    ('MSPO, RSPO, eMSPO', 'Palm oil certification schemes (Malaysian Sustainable Palm Oil; Roundtable on Sustainable '
                          'Palm Oil), and MSPO’s online list of certified sites.'),
    ('Mill-year', 'A mill in a given year.'),
    ('Firm-reported', 'Based on the firm’s own statement in its annual report, not on a certificate record.'),
    ('FFB yield', 'Fresh fruit bunches harvested per hectare, as the firm reports it.'),
    ('mt, mt/ha', 'Tonnes; tonnes per hectare, as printed in the annual report.'),
    ('Mt/WHa', 'How SPB prints its yield: tonnes per “weighted average hectarage”, its harvestable area (the pilot’s '
               'method card for FFB yield).'),
    ('AR', 'Annual report, as in “AR” followed by the year of the report.'),
    ('Debt-to-equity', 'Borrowings divided by total equity, for the whole group.'),
    ('Restatement', 'A figure that a later annual report prints differently for the same year.'),
    ('WRO', 'Withhold Release Order: a US order that stops certain imports.'),
    ('Grid square, edge square', 'A square of the grid; an edge square is cut by the Sarawak border.'),
    ('OpenStreetMap (OSM)', 'A public map made by volunteers, used here for roads.'),
]


def glossary(p):
    b = Block(p, 'glossary-main')
    rain = ('A year’s rainfall minus the ' + b.n('s4.rainfall_baseline') + ' average for the same place, in mm.')
    items = GLOSSARY[:16] + [('Rainfall anomaly', None)] + GLOSSARY[16:]
    dl = ''.join(f'<dt>{esc(k)}</dt><dd>{rain if v is None else esc(v)}</dd>' for k, v in items)
    return ('<section id="glossary" aria-labelledby="glossary-h"><h2 id="glossary-h">Words used on this page</h2>'
            + b.wrap(f'<dl class="glossary">{dl}</dl>') + '</section>')


def appendix(p):
    b = Block(p, 'appendix', markers=False)
    rows = []
    for nid in p.order:
        n = p.num[nid]
        src = n['source']
        unit_raw = ''
        if n['unit_source']:
            unit_raw = (' · unit as printed: <code data-meta="unit_raw" data-for="' + esc(nid) + '">'
                        + esc(n['unit_source']['raw']) + '</code>')
        rows.append(
            f'<li><p><span data-meta="label" data-for="{esc(nid)}">{esc(n["label"])}</span>: {b.n(nid)}</p>'
            f'<p class="tag"><code data-meta="file" data-for="{esc(nid)}">{esc(src["file"])}</code> · '
            f'<span data-meta="locator" data-for="{esc(nid)}">{esc(src["locator"])}</span> · '
            f'<span data-meta="column" data-for="{esc(nid)}">{esc(src["column"])}</span> · raw value '
            f'<code data-meta="raw" data-for="{esc(nid)}">{esc(n["raw"])}</code>{unit_raw}</p></li>')
    for c in p.cav_order:
        b.note(c)
    inner = ('<details><summary>Where the numbers come from (every number on this page, with its source tag)</summary>'
             '<p>Each number on this page carries a source tag: the pilot file, the place in it (row key, or heading '
             'and block for markdown), the column (or the exact quote) and the raw value. The same tag sits in the '
             'page code around each number. Paths are relative to the pilot folder, which is not published.</p>'
             '<ol class="sources-list">' + ''.join(rows) + '</ol>'
             '<h3>The notes used on this page</h3>' + b.notes() + '</details>')
    return ('<section id="numbers" aria-labelledby="numbers-h"><h2 id="numbers-h">Appendix</h2>'
            + b.wrap(inner, notes=False) + '</section>')


def credits(p):
    b = Block(p, 'credits')
    A = {}
    for a in p.L['attributions']:
        if a.get('recorded'):
            A.setdefault(a['source_id'], []).append(a['wording'])
    S = {s['source_id']: s for s in p.L['sources']}
    osm_notice = [w for w in A['ROADS_OSM'] if w['value'].startswith('©')][0]
    items = [
        '<li><b>Forest:</b> Hansen et al. (' + yr('2013') + ') Science. Hansen/UMD/Google/USGS/NASA, '
        + t(S['HANSEN_GFC']['name']) + ', ' + b.n('s0.hansen_dataset_version') + '. “' + t(A['HANSEN_GFC'][0])
        + '” Clipped to Sarawak; “forest” means more than ' + b.n('s4.tree_cover_threshold_for_forest')
        + ' tree cover.</li>',
        '<li><b>Roads:</b> ' + t(osm_notice) + ', available under the Open Database License (ODbL); data as of '
        + b.n('s0.openstreetmap_data_date') + '.</li>',
        '<li><b>Boundary:</b> ' + t(S['BOUNDARY_GEOB']['name']) + '. ' + t(A['BOUNDARY_GEOB'][0])
        + '; © OpenStreetMap contributors, ODbL.</li>',
        '<li><b>Oil palm map:</b> Descals, A. (' + yr('2024') + '), Global oil palm extent and planting year from '
        + yr('1990') + ' to ' + yr('2021') + ', ' + b.n('s0.descals_oil_palm_dataset_version') + ', Zenodo, DOI '
        + b.n('s0.descals_oil_palm_doi') + ', ' + lic('CC BY 4.0') + '; ' + b.n('s3.palm_map_tiles_clipped')
        + ' tiles clipped to Sarawak.</li>',
        '<li><b>Rainfall:</b> ' + t(S['CHIRPS']['name']) + ', version ' + b.n('s0.chirps_version') + '.</li>',
        '<li><b>Dependency on nature:</b> ' + encore_citation(b) + ' ' + lic('CC BY-SA 4.0') + '.</li>',
        '<li><b>Mill points:</b> ' + t(S['UML']['name']) + ', file of ' + b.n('s0.universal_mill_list_file_date')
        + '; unverified; no licence stated.</li>',
        '<li><b>Certification:</b> eMSPO Certified Entity list (MSPO), accessed ' + b.n('s0.emspo_access_date')
        + ', and the RSPO registry, accessed ' + b.n('s0.rspo_registry_access_date') + '; no licence stated. '
        'No contact details are shown.</li>',
        '<li><b>Import bans:</b> ' + t(A['CBP_WRO'][0]) + '</li>',
        '<li><b>Sanctions:</b> ' + t(S['EU_FSF']['name']) + '. Licence of the file used (the CSV file, version '
        + nt('version', '1.1') + '), as recorded in the pilot: ' + t(A['EU_FSF'][0]) + '.</li>',
        '<li><b>Forest-loss check:</b> ' + t(S['GFW_GNW']['name']) + '. Licence as recorded in the pilot: '
        + t(S['GFW_GNW']['licence']) + ' Used only to check the forest-loss values; no screenshots are shown. '
        'The tree-cover loss data is Hansen/UMD/Google/USGS/NASA (see Forest above).</li>',
        '<li><b>Company figures:</b> the firms’ annual reports, cited by title, year and page; their licences were '
        'not checked. No report pages or logos are shown.</li>',
    ]
    inner = (
        '<h2 id="credits-h">Credits and licences</h2>'
        '<ul class="credits">' + ''.join(items) + '</ul>'
        '<p class="small">The wording of the Hansen citation was supplied by Yaseen (Research Assistant); it is not '
        'recorded in the pilot.</p>'
        '<h3>This page</h3>'
        '<p>By Yaseen (Research Assistant), built by script from the pilot’s files, with an AI coding '
        'assistant. This page adds no '
        'data or analysis to the pilot. Page text: <a rel="license" href="https://creativecommons.org/licenses/by/4.0/">'
        + lic('CC BY 4.0') + '</a>. ENCORE content: <a rel="license" '
        'href="https://creativecommons.org/licenses/by-sa/4.0/">' + lic('CC BY-SA 4.0') + '</a>. Images: the pilot’s '
        'drawings, ' + lic('CC BY 4.0') + ', with the data credits in each caption. Scripts: MIT License. Third-party '
        'material keeps its own terms.</p>')
    return f'<footer class="site-footer" aria-labelledby="credits-h">{b.wrap(inner)}</footer>'


def header(p):
    b = Block(p, 'top')
    n = b.n
    glance = [
        (n('s1.firms'), 'firms'), (n('s1.mills_all_firms'), 'mills'),
        (n('s1.first_year') + '–' + n('s1.last_year'), 'years'), (n('s1.features'), 'features'),
        (n('s1.values_with_an_evidence_row'), 'values traced'), (n('s5.grid_cells'), 'grid squares'),
    ]
    tiles = ''.join(f'<li><span class="big">{v}</span><span class="what">{w}</span></li>' for v, w in glance)
    toc = [('what-we-did', 'What we did'), ('sources', 'Sources'), ('raw-to-final', 'From raw data to the final tables'),
           ('features', 'The measures (features)'), ('grid', 'The grid of Sarawak'),
           ('evidence', 'The evidence trail'), ('results', 'Results'), ('gaps', 'Gaps and findings'),
           ('next', 'Next decisions')]
    toc_html = ''.join(f'<li><a href="#{a}">{esc(x)}</a></li>' for a, x in toc)
    toc_html += ('<li class="extra"><a href="#glossary">Words used on this page</a></li>'
                 '<li class="extra"><a href="#numbers">Where the numbers come from</a></li>'
                 '<li class="extra"><a href="#credits">Credits and licences</a></li>')
    inner = (
        '<p class="kicker">A public-data pilot, explained</p>'
        '<h1>NRFR palm oil pilot</h1>'
        '<p class="subtitle">From public data to a traceable table</p>'
        '<p class="byline">By Yaseen (Research Assistant). Built from the pilot’s files.</p>'
        f'<p class="status">The pilot’s findings report, dated {n("s0.date_of_the_findings_report")}, is waiting for a '
        'decision: scale up, change the plan, or stop. ' + pending_badge(p, 'R057') + '</p>'
        '<p class="lede">The NRFR palm oil pilot tried, once and on a small scale, to build a table about palm oil growers '
        'from public sources only, and to keep a record of where every value came from. This page shows what it '
        'produced, what worked and what did not, in the pilot’s own terms. It adds nothing to it.</p>'
        f'<ul class="glance" aria-label="At a glance">{tiles}</ul>'
        '<p class="small">Every number on this page comes from the pilot’s files and carries a source tag; see '
        '“<a href="#numbers">Where the numbers come from</a>”. File paths name places in the pilot folder, which is '
        'not published.</p>'
        f'<nav aria-label="Contents"><h2 class="toc-h">Contents</h2><ol class="toc">{toc_html}</ol></nav>')
    return f'<header class="site-header">{b.wrap(inner)}</header>'


def build_html(data):
    p = Page(data)
    body = (header(p) + '<main>' + s1(p) + s2(p) + s3(p) + s4(p) + s5(p) + s6(p) + s7(p) + s8(p) + s9(p)
            + glossary(p) + appendix(p) + '</main>' + credits(p))
    return ('<!doctype html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n'
            '<meta name="viewport" content="width=device-width, initial-scale=1">\n'
            '<meta name="color-scheme" content="light dark">\n'
            '<meta name="description" content="What the pilot built from public data, how every value '
            'can be traced to its source, and what did not work.">\n'
            '<title>NRFR palm oil pilot</title>\n'
            '<link rel="icon" href="data:,">\n'
            '<link rel="stylesheet" href="assets/style.css">\n</head>\n<body>\n'
            '<a class="skip" href="#what-we-did">Skip to the content</a>\n'
            + body.replace('</section>', '</section>\n') + '\n</body>\n</html>\n')


CSS = r"""/* Palm oil pilot site. Written by scripts/build_page.py. No external fonts or files. */
:root {
  --bg: #fbfaf7; --surface: #ffffff; --ink: #1d232a; --muted: #5d6670; --line: #d9d6cf;
  --accent: #245b8f; --accent-soft: #e8f0f7; --note-bg: #fbf4e4; --note-line: #c98a1b; --note-ink: #8a5a00;
  --gap: #8a4b2f; --gap-soft: #f6ebe5; --flag-soft: #fdf3dc; --ok-soft: #e7f2ea;
  --code-bg: #f1efea; --shadow: 0 1px 2px rgba(0,0,0,.05); --scroll-shade: rgba(0,0,0,.45);
  color-scheme: light dark;
}
@media (prefers-color-scheme: dark) {
  :root {
    --bg: #15191e; --surface: #1c2229; --ink: #e7e9ec; --muted: #a2abb5; --line: #343c46;
    --accent: #8cbcec; --accent-soft: #1f2d3b; --note-bg: #2a2418; --note-line: #d9a441; --note-ink: #d9a441;
    --gap: #e6a68a; --gap-soft: #2e221d; --flag-soft: #2c2716; --ok-soft: #1c2b22;
    --code-bg: #242b33; --shadow: none; --scroll-shade: rgba(255,255,255,.4);
  }
}
*, *::before, *::after { box-sizing: border-box; }
html { -webkit-text-size-adjust: 100%; }
body {
  margin: 0; background: var(--bg); color: var(--ink);
  font: 1.0625rem/1.6 system-ui, -apple-system, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
}
.skip { position: absolute; left: -999px; top: 0; }
.skip:focus { left: 1rem; top: 1rem; background: var(--surface); padding: .5rem; z-index: 2; }
.site-header, main, .site-footer { max-width: 46rem; margin: 0 auto; padding: 0 1rem; }
.site-header { padding-top: 2rem; }
h1 { font-size: 1.85rem; line-height: 1.2; margin: .25rem 0 .75rem; letter-spacing: -.01em; }
h2 { font-size: 1.45rem; line-height: 1.25; margin: 2.75rem 0 .5rem; padding-top: 1rem; border-top: 1px solid var(--line); }
h3 { font-size: 1.1rem; margin: 1.6rem 0 .4rem; }
p, ul, ol, dl { margin: 0 0 .9rem; }
ul, ol { padding-left: 1.3rem; }
li { margin: .2rem 0; }
a { color: var(--accent); }
code { font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace; font-size: .86em;
  background: var(--code-bg); padding: .05em .3em; border-radius: 3px; overflow-wrap: anywhere; }
.kicker { text-transform: uppercase; letter-spacing: .08em; font-size: .8rem; color: var(--muted); margin: 0; }
.subtitle { font-size: 1.25rem; line-height: 1.3; margin: -.4rem 0 .75rem; }
.byline { color: var(--muted); }
.lede { font-size: 1.1rem; }
.status { background: var(--surface); border: 1px solid var(--line); border-left: 4px solid var(--accent);
  padding: .6rem .8rem; border-radius: 4px; }
.message { font-size: 1.08rem; color: var(--ink); border-left: 3px solid var(--accent); padding-left: .75rem; }
.secno { display: inline-block; min-width: 1.6em; color: var(--accent); }
.glance { list-style: none; padding: 0; display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: .5rem; }
.glance li { background: var(--surface); border: 1px solid var(--line); border-radius: 6px; padding: .6rem .75rem;
  margin: 0; box-shadow: var(--shadow); }
.glance .big { display: block; font-size: 1.35rem; font-weight: 650; line-height: 1.2; }
.glance .what { color: var(--muted); font-size: .9rem; }
.toc-h { border: 0; margin-top: 1.5rem; padding-top: 0; font-size: 1.1rem; }
.toc { columns: 1; }
.toc .extra { list-style: none; margin-left: -1.3rem; }
.small, table.small { font-size: .9rem; }
.details { font-size: .9rem; color: var(--muted); background: var(--code-bg); padding: .55rem .75rem; border-radius: 4px;
  margin-top: 1.25rem; }
.details-label { font-weight: 650; color: var(--ink); }
.keep { background: var(--surface); border: 1px solid var(--line); border-radius: 6px; padding: .65rem .85rem;
  margin: 1rem 0; }
.keep p { margin: 0; }
.notes { list-style: none; padding: .55rem .8rem; margin: .6rem 0 1.1rem; background: var(--note-bg);
  border-left: 3px solid var(--note-line); border-radius: 0 4px 4px 0; font-size: .9rem; }
.notes li { margin: .15rem 0; padding-left: 1.4em; text-indent: -1.4em; }
.mk-key { display: inline-block; width: 1.2em; text-indent: 0; color: var(--note-ink); }
.mks { line-height: 0; }
.mk { font-size: .75rem; text-decoration: none; color: var(--note-ink); font-weight: 700; padding: 0 .1em; }
.rid { font-size: .78em; color: var(--muted); font-weight: 400; white-space: nowrap; }
.n { font-variant-numeric: tabular-nums; }
.nw { white-space: nowrap; }
.tbl { overflow-x: auto; max-width: 100%; margin: .5rem 0 .75rem; -webkit-overflow-scrolling: touch;
  background: linear-gradient(to right, var(--surface) 30%, transparent) left / 1.5rem 100% no-repeat local,
    linear-gradient(to left, var(--surface) 30%, transparent) right / 1.5rem 100% no-repeat local,
    radial-gradient(farthest-side at 0 50%, var(--scroll-shade), transparent) left / .9rem 100% no-repeat scroll,
    radial-gradient(farthest-side at 100% 50%, var(--scroll-shade), transparent) right / .9rem 100% no-repeat scroll,
    var(--surface); }
.tbl:focus-visible, .fig a:focus-visible { outline: 2px solid var(--accent); outline-offset: 2px; }
table { border-collapse: collapse; width: 100%; font-size: .95rem; background: transparent; }
caption { text-align: left; font-size: .9rem; color: var(--muted); padding: 0 0 .35rem; caption-side: top; }
th, td { border-bottom: 1px solid var(--line); padding: .4rem .5rem; text-align: left; vertical-align: top; }
thead th { border-bottom: 2px solid var(--line); font-weight: 650; }
table.num td, table.num thead th:not(:first-child) { text-align: right; }
table.num th[scope="row"] { white-space: nowrap; }
.missing { font-style: italic; color: var(--gap); }
.flag { display: block; color: var(--muted); margin-top: .2rem; }
.licence-tag { display: inline-block; font-size: .8rem; border: 1px solid var(--line); border-radius: 3px;
  padding: 0 .35rem; color: var(--muted); white-space: nowrap; }
.cite { font-size: .85rem; color: var(--muted); }
.badge { display: inline-block; font-size: .8rem; font-weight: 600; border-radius: 999px; padding: .05rem .6rem;
  border: 1px solid var(--line); white-space: nowrap; }
.badge-pending { background: var(--flag-soft); border-color: var(--note-line); }
.badge-decided { background: var(--ok-soft); }
.cards { display: grid; grid-template-columns: minmax(0, 1fr); gap: .9rem; margin: 1rem 0; }
.card { background: var(--surface); border: 1px solid var(--line); border-radius: 8px; padding: .4rem 1rem .2rem;
  box-shadow: var(--shadow); }
.card h3 { margin-top: .6rem; }
.verdict { font-weight: 600; display: inline-block; padding: .05rem .55rem; border-radius: 4px; font-size: .9rem; }
.v-built { background: var(--ok-soft); }
.v-flag { background: var(--flag-soft); }
.v-gap { background: var(--gap-soft); color: var(--gap); }
.pilot-note { font-size: .88rem; color: var(--muted); }
.fig { margin: 1.25rem 0; }
.fig .frame { display: block; background: #fff; padding: .4rem; border: 1px solid var(--line); border-radius: 6px; }
.fig img { display: block; width: 100%; height: auto; }
figcaption { font-size: .9rem; margin-top: .45rem; }
figcaption .credit, figcaption .imgnote { display: block; color: var(--muted); font-size: .85rem; margin-top: .25rem; }
figcaption .capnote { display: block; margin-top: .25rem; }
.pair { display: grid; grid-template-columns: minmax(0, 1fr); gap: .75rem; }
.chain { list-style: none; padding-left: 0; counter-reset: link; }
.chain li { position: relative; padding: .55rem .8rem .55rem 2.6rem; margin: 0 0 1.1rem; background: var(--surface);
  border: 1px solid var(--line); border-radius: 6px; counter-increment: link; }
.chain li::before { content: counter(link); position: absolute; left: .7rem; top: .55rem; width: 1.4rem; height: 1.4rem;
  border-radius: 50%; background: var(--accent); color: var(--bg); font-size: .8rem; font-weight: 700;
  text-align: center; line-height: 1.4rem; }
.chain li:not(:last-child)::after { content: "↓"; position: absolute; left: 1.1rem; bottom: -1.15rem; color: var(--muted); }
.layers > li { margin-bottom: .55rem; }
ol.gaps { padding-left: 1.6rem; }
ol.gaps > li { margin: 0 0 1rem; }
.gap-title { font-weight: 650; margin-bottom: .2rem; }
.gaps .notes { margin-top: .3rem; }
.options li { margin-bottom: .5rem; }
.changes li { margin-bottom: .45rem; }
ul.pending { list-style: none; padding-left: 0; }
dl.glossary dt { font-weight: 650; margin-top: .6rem; }
dl.glossary dd { margin: 0 0 .2rem; }
details { margin: .75rem 0; }
summary { cursor: pointer; font-weight: 600; color: var(--accent); }
.sources-list { font-size: .85rem; padding-left: 2.2rem; }
.sources-list li { margin-bottom: .55rem; border-bottom: 1px dotted var(--line); padding-bottom: .4rem; }
.sources-list p { margin: 0; }
.sources-list .tag { color: var(--muted); overflow-wrap: anywhere; }
.dg-fig { margin: 1.25rem auto; max-width: 42rem; }
.dg-title { font-weight: 650; margin-bottom: .6rem; }
.dg { font-size: .8125rem; line-height: 1.3; }
.dg code { font-size: 1em; background: none; padding: 0; }
.dg-grid { display: grid; grid-template-columns: minmax(0, 1fr) .75rem minmax(0, 1fr) .75rem minmax(0, 1fr);
  row-gap: .45rem; }
.dg-head { text-align: center; padding-bottom: .15rem; }
.dg-head b, .dg-head code, .dg-sub { display: block; }
.dg-head code, .dg-sub, .dg-in { color: var(--muted); }
.dg-box { display: flex; align-items: center; justify-content: center; text-align: center; padding: .3rem .25rem;
  border: 1.5px solid var(--ink); border-radius: 4px; background: var(--surface); overflow-wrap: break-word;
  hyphens: manual; }
.dg-box.dg-gap { border-style: dashed; border-color: var(--gap); background: var(--gap-soft); }
.dg-box.dg-chk { border: 2px dotted var(--muted); }
.dg-box.dg-final { display: block; padding: .45rem .5rem; border: 2px solid var(--accent); background: var(--accent-soft); }
.dg-final b, .dg-in { display: block; }
.dg-arr { position: relative; align-self: center; height: 0; margin: 0 .35rem 0 .05rem;
  border-top: 1.5px solid var(--ink); }
.dg-arr::after { content: ""; position: absolute; right: -.35rem; top: -.33rem; border-left: .4rem solid var(--ink);
  border-top: .3rem solid transparent; border-bottom: .3rem solid transparent; }
.dg-arr.dg-gap { border-top-style: dashed; border-top-color: var(--gap); }
.dg-arr.dg-gap::after { border-left-color: var(--gap); }
.dg-arr.dg-chk { border-top: 2px dotted var(--muted); }
.dg-arr.dg-chk::after { border-left-color: var(--muted); }
.dg-mid { text-align: center; font-weight: 650; margin: 1rem 0 0; }
.dg-down { display: block; position: relative; width: 0; height: .8rem; margin: .15rem auto .5rem;
  border-left: 1.5px solid var(--ink); }
.dg-down::after { content: ""; position: absolute; left: -.33rem; bottom: -.35rem; border-top: .4rem solid var(--ink);
  border-left: .3rem solid transparent; border-right: .3rem solid transparent; }
.dg-finals { display: grid; grid-template-columns: minmax(0, 1fr); gap: .45rem; }
.dg-ev { text-align: center; }
.dg-links { list-style: none; padding: 0; margin: .45rem 0 0; display: flex; flex-wrap: wrap; justify-content: center;
  gap: .35rem; }
.dg-links li { margin: 0; padding: .1rem .5rem; border: 1px solid var(--accent); border-radius: 999px;
  background: var(--surface); }
.dg-legend { list-style: none; padding: 0; margin: .8rem 0 0; display: flex; flex-wrap: wrap; gap: .3rem 1.2rem;
  color: var(--muted); }
.dg-legend li { margin: 0; }
.dg-key { display: inline-block; width: 1.8rem; margin-right: .4rem; vertical-align: middle;
  border-top: 1.5px solid var(--ink); }
.dg-key.dg-gap { border-top-style: dashed; border-top-color: var(--gap); }
.dg-key.dg-chk { border-top: 2px dotted var(--muted); }
.vh { position: absolute; width: 1px; height: 1px; overflow: hidden; clip: rect(0 0 0 0); white-space: nowrap; }
.dg-words { font-size: .95rem; }
.site-footer { margin-top: 3rem; padding-bottom: 3rem; }
.site-footer h2 { margin-top: 0; }
.credits { font-size: .92rem; }
@media (max-width: 39.99rem) {
  table.num { font-size: .84rem; }
  table.num th, table.num td { padding: .35rem .3rem; }
}
@media (min-width: 40rem) {
  body { font-size: 1.0625rem; }
  h1 { font-size: 2.3rem; }
  .glance { grid-template-columns: repeat(3, minmax(0, 1fr)); }
  .toc { columns: 2; column-gap: 2rem; }
  .pair { grid-template-columns: repeat(2, minmax(0, 1fr)); }
  .dg { font-size: .875rem; }
  .dg-grid { grid-template-columns: minmax(0, 1fr) 1.2rem minmax(0, 1fr) 1.2rem minmax(0, 1fr); }
  .dg-finals { grid-template-columns: repeat(3, minmax(0, 1fr)); }
}
@media (min-width: 60rem) {
  .site-header, main, .site-footer { max-width: 50rem; }
  .cards { grid-template-columns: repeat(2, minmax(0, 1fr)); }
}
@media print {
  details > *:not(summary) { display: block; }
  .skip, .mks { display: none; }
}
"""


def main():
    try:
        data = json.loads(DATA.read_text(encoding='utf-8'))
    except (OSError, ValueError) as e:
        print(f'ERROR: cannot read {DATA.relative_to(SITE)} ({e}); run scripts/extract.py first.')
        return 2
    page = build_html(data)
    OUT_HTML.parent.mkdir(parents=True, exist_ok=True)
    OUT_CSS.parent.mkdir(parents=True, exist_ok=True)
    OUT_HTML.write_text(page, encoding='utf-8', newline='\n')
    OUT_CSS.write_text(CSS, encoding='utf-8', newline='\n')
    print(f'Wrote {OUT_HTML.relative_to(SITE)} ({len(page.encode("utf-8")):,} bytes) and '
          f'{OUT_CSS.relative_to(SITE)} ({len(CSS.encode("utf-8")):,} bytes).')
    return 0


if __name__ == '__main__':
    sys.exit(main())
