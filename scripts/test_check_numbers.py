"""Planted-error test for scripts/check_numbers.py.

Copies the pilot files listed in build/site_data.json ("inputs") into
build/planted_test/pilot/ (rule 13: local copies of pilot data go only in
build/), with copies of site_data.json and the two spec files. Then:

  1. runs check_numbers.py on the unchanged copies: it must pass;
  2. plants one error at a time (in a pilot file, in the spec, or in
     site_data.json), runs check_numbers.py, and expects exit 1 with a
     failure line that names the planted entry; then restores the copy;
  3. does the same with a copy of site/index.html (build/planted_test/
     index.html): the unchanged copy must pass, then one error at a time
     is planted in the page (number text, tags, notes, untagged digits,
     number words, no-tag reasons, the appendix, alt text, and notes in a
     block where nothing needs them, Step 5 decision 7).

The pilot itself is only read (the copies are made from it). The copies are
deleted at the end; the result is written to build/test_check_numbers.txt.
Exit 0 = every planted error caught and the baseline passes, 1 = otherwise,
2 = setup error.

Python standard library only.
"""

import csv
import html
import io
import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

SITE = Path(__file__).resolve().parent.parent
BUILD = SITE / 'build'
WORK = BUILD / 'planted_test'
CHECK = SITE / 'scripts' / 'check_numbers.py'
FINDINGS = 'pilot/reports/step10_findings.md'
GRID = 'pilot/reports/step9_grid.md'


def pilot_dir():
    p = Path(os.environ.get('PILOT_DIR') or '../nrfr-pilot')
    return (p if p.is_absolute() else SITE / p).resolve()


def fresh_copies(pilot, inputs):
    if WORK.exists():
        shutil.rmtree(WORK)
    for rel in inputs:
        dst = WORK / 'pilot' / rel
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(pilot / rel, dst)
    shutil.copyfile(BUILD / 'site_data.json', WORK / 'site_data.json')
    shutil.copyfile(SITE / 'docs' / 'number_sources.csv', WORK / 'number_sources.csv')
    shutil.copyfile(SITE / 'docs' / 'caveats.csv', WORK / 'caveats.csv')


def run_check(html=None):
    env = dict(os.environ, PILOT_DIR=str(WORK / 'pilot'))
    page = ['--html', str(html)] if html else []
    r = subprocess.run([sys.executable, '-B', str(CHECK), '--data', str(WORK / 'site_data.json'),
                        '--spec', str(WORK / 'number_sources.csv'), '--caveats', str(WORK / 'caveats.csv'),
                        '--report', str(WORK / 'report.txt')] + page, capture_output=True, text=True, env=env)
    return r.returncode, r.stdout + r.stderr


# ---- ways to plant an error (each edits one copy and asserts the edit is exact)

def replace(rel, old, new):
    def plant():
        p = WORK / rel
        text = p.read_text(encoding='utf-8')
        assert text.count(old) == 1, f'{rel}: planting text found {text.count(old)} times'
        p.write_text(text.replace(old, new), encoding='utf-8')
    return plant


def duplicate_line(rel, start):
    def plant():
        p = WORK / rel
        lines = p.read_text(encoding='utf-8').split('\n')
        hits = [i for i, ln in enumerate(lines) if ln.startswith(start)]
        assert len(hits) == 1, f'{rel}: line found {len(hits)} times'
        lines.insert(hits[0] + 1, lines[hits[0]])
        p.write_text('\n'.join(lines), encoding='utf-8')
    return plant


def edit_csv(rel, where, column, value):
    def plant():
        p = WORK / rel
        rows = list(csv.reader(io.StringIO(p.read_text(encoding='utf-8'), newline='')))
        head = rows[0]
        hits = [r for r in rows[1:] if all(r[head.index(k)] == v for k, v in where.items())]
        assert len(hits) == 1, f'{rel}: {len(hits)} rows match {where}'
        hits[0][head.index(column)] = value
        out = io.StringIO()
        csv.writer(out, lineterminator='\n').writerows(rows)
        p.write_text(out.getvalue(), encoding='utf-8')
    return plant


def edit_json(fn):
    def plant():
        p = WORK / 'site_data.json'
        data = json.loads(p.read_text(encoding='utf-8'))
        fn(data)
        p.write_text(json.dumps(data, ensure_ascii=False, indent=1) + '\n', encoding='utf-8')
    return plant


def number(data, ident):
    hits = [n for n in data['numbers'] if n['id'] == ident]
    assert len(hits) == 1, ident
    return hits[0]


def set_number(ident, key, value):
    return edit_json(lambda d: number(d, ident).__setitem__(key, value))


def both(*plants):
    def plant():
        for p in plants:
            p()
    return plant


PLANTS = [
    # --- in a pilot file (the source changed after extraction)
    ('CSV cell', 's7.debt_to_equity_ratio_sop_2022',
     edit_csv('pilot/data/processed/pilot_firm_year.csv', {'firm_id': 'SOP', 'year': '2022'}, 'debt_to_equity', '0.2208')),
    ('CSV count with a filter', 's2.sources_downloaded',
     edit_csv('pilot/source_register.csv', {'source_id': 'RSPO'}, 'date_downloaded', '')),
    ('CSV sum', 's7.firm_reported_mill_years_sop',
     edit_csv('pilot/data/processed/firm1_certification_firm_year.csv', {'year': '2021'}, 'n_certified_firm_reported', '5')),
    ('Text in a CSV cell', 's7.largest_catchment_cells_share_of_sops_2022_forest_loss',
     replace('pilot/evidence.csv', 'and 63% of 2022 loss', 'and 64% of 2022 loss')),
    ('Unit read from a CSV cell', 's7.ffb_yield_unit_as_printed_sop_2022',
     edit_csv('pilot/evidence.csv', {'table': 'data/processed/firm1_firm_year.csv', 'year': '2022', 'column': 'ffb_yield'},
              'unit', 'mt/ha')),
    ('Markdown table cell', 's5.road_length_used_km',
     replace(GRID, '| **Used** | **152,089** | **76,361.9** |', '| **Used** | **152,089** | **76,361.8** |')),
    ('Markdown quote in a table row', 's2.size_of_the_kept_downloads',
     replace(FINDINGS, 'About 1.8 GB', 'About 1.9 GB')),
    ('Markdown table count with a filter', 's1.features_that_are_gaps',
     replace(FINDINGS, '| 2 | Peat overlap | **Gap** |', '| 2 | Peat overlap | **Built** |')),
    ('Numbered items', 's9.options_for_the_decision',
     replace(FINDINGS, '3. **Stop:** keep the pilot outputs as the record, with no further build.\n',
             '3. **Stop:** keep the pilot outputs as the record, with no further build.\n4. **Wait:** decide later.\n')),
    ('Markdown list item quote', 's5.distance_to_mill_median_km',
     replace('pilot/docs/methods/regional_grid.md', 'median 30.2 km', 'median 30.3 km')),
    ('Number in a quote changed', 's4.rainfall_check_mill_years_off',
     replace(FINDINGS, '**0 of 396** mill-years', '**0 of 3960** mill-years')),
    ('Missing locator (heading renamed)', 's5.road_length_used_km',
     replace(GRID, '## Roads inside Sarawak\n', '## Roads in Sarawak\n')),
    ('Ambiguous locator (table row duplicated)', 's5.road_length_used_km',
     duplicate_line(GRID, '| **Used** |')),
    ('List text in a markdown table', 'gaps',
     replace(FINDINGS, '| 10 | **GFW comparison limited** |', '| 10 | **GFW comparison narrow** |')),
    ('Pending decision recorded in the review queue', 'decisions_pending',
     edit_csv('pilot/review_queue.csv', {'item_id': 'R057'}, 'decision', '(c) Stop')),
    # --- in the spec
    ('Quote placed in the wrong table row (spec)', 's3.python_scripts_at_the_time_of_the_findings_report',
     edit_csv('number_sources.csv', {'id': 's3.python_scripts_at_the_time_of_the_findings_report'}, 'row_key',
              '## 2. What was delivered | row=Raw data')),
    ('Wrong expected value typed into the spec', 's7.forest_loss_ha_sop_2021',
     edit_csv('number_sources.csv', {'id': 's7.forest_loss_ha_sop_2021'}, 'expected_value', '8856.92')),
    ('Whole-token rule: value only inside a longer integer (10 in 104)', 's3.firm_table_rebuild_outputs_identical',
     both(edit_csv('number_sources.csv', {'id': 's3.firm_table_rebuild_outputs_identical'}, 'expected_value', '10'),
          edit_json(lambda d: number(d, 's3.firm_table_rebuild_outputs_identical').update(raw='10', display='10')))),
    ('Whole-token rule: value only inside a decimal (15 in 0.15)',
     's8.gfw_comparison_largest_possible_threshold_effect_on_forest_loss',
     both(edit_csv('number_sources.csv', {'id': 's8.gfw_comparison_largest_possible_threshold_effect_on_forest_loss'},
                   'expected_value', '15'),
          edit_json(lambda d: number(d, 's8.gfw_comparison_largest_possible_threshold_effect_on_forest_loss')
                    .update(raw='15', display='15')))),
    ('Forest-loss caveat removed from spec and data (decision 5)', 's7.forest_loss_ha_spb_2023',
     both(edit_csv('number_sources.csv', {'id': 's7.forest_loss_ha_spb_2023'}, 'caveats', ''),
          set_number('s7.forest_loss_ha_spb_2023', 'caveats', []))),
    ('ENCORE licence caveat removed from spec and data (decision 6)', 's4.encore_ratings_per_firm',
     both(edit_csv('number_sources.csv', {'id': 's4.encore_ratings_per_firm'}, 'caveats', 'encore_proxy'),
          set_number('s4.encore_ratings_per_firm', 'caveats', ['encore_proxy']))),
    ('No-tag reason outside decision 4 (spec and data)', 's1.firms',
     both(edit_csv('number_sources.csv', {'id': 's1.firms'}, 'tag_required', 'no: obvious'),
          edit_json(lambda d: number(d, 's1.firms').update(tag_required=False, no_tag_reason='obvious')))),
    # --- in site_data.json
    ('Raw value changed', 's7.forest_loss_ha_sop_2022', set_number('s7.forest_loss_ha_sop_2022', 'raw', '12532.78')),
    ('Display rounded', 's7.forest_loss_ha_sop_2021', set_number('s7.forest_loss_ha_sop_2021', 'display', '8,857')),
    ('Display with an added + sign', 's7.rainfall_anomaly_mm_sop_2021',
     set_number('s7.rainfall_anomaly_mm_sop_2021', 'display', '+170.57')),
    ('Display without thousands separators', 's5.sarawak_forest_loss_2021_ha',
     set_number('s5.sarawak_forest_loss_2021_ha', 'display', '72574.7590')),
    ('Unit changed', 's7.forest_loss_ha_sop_2021', set_number('s7.forest_loss_ha_sop_2021', 'unit', 'km²')),
    ('Tag points to another row', 's7.debt_to_equity_ratio_sop_2021',
     edit_json(lambda d: number(d, 's7.debt_to_equity_ratio_sop_2021')['source'].update(locator='firm_id=SOP; year=2022'))),
    ('Tag removed (untagged number)', 's6.evidence_rows', set_number('s6.evidence_rows', 'source', {})),
    ('Caveat removed in the data only', 's7.forest_loss_ha_ta_ann_2021',
     set_number('s7.forest_loss_ha_ta_ann_2021', 'caveats', [])),
    ('Entry deleted', 's1.firms', edit_json(lambda d: d['numbers'].remove(number(d, 's1.firms')))),
    ('Extra number not in the spec', 's7.extra_number',
     edit_json(lambda d: d['numbers'].append({'id': 's7.extra_number', 'raw': '99', 'display': '99'}))),
    ('List value changed', 'features', edit_json(lambda d: d['lists']['features'][0]['verdict'].update(value='Built'))),
    ('Caveat wording changed', 'caveats', edit_json(lambda d: d['caveats'][0].update(text='Forest loss.'))),
]


# ---- planted errors in a copy of the page (each takes the page text and returns it with one error)

NB = ' '


def sub1(old, new):
    def plant(text):
        assert text.count(old) >= 1, f'page: {old[:60]!r} not found'
        return text.replace(old, new, 1)
    return plant


def sub_re(pattern, new, count=1, need=None):
    def plant(text):
        hits = len(re.findall(pattern, text, flags=re.S))
        assert hits >= 1 and (need is None or hits == need), f'page: {pattern[:60]!r} found {hits} times'
        return re.sub(pattern, new, text, count=count, flags=re.S)
    return plant


def in_main(snippet):
    return sub1('<main>', '<main>' + snippet)


def caveat_text(cid):
    rows = list(csv.DictReader(io.StringIO((SITE / 'docs' / 'caveats.csv').read_text(encoding='utf-8'))))
    return html.escape([r['text'] for r in rows if r['id'] == cid][0], quote=False)


def stray_note(block, cid):
    """A note added to a block where no number and no element needs it."""
    def plant(text):
        anchor = f'<ul class="notes" aria-label="Notes">'
        start = text.index(f'data-block="{block}"')
        at = text.index(anchor, start) + len(anchor)
        return (text[:at] + f'<li id="{block}-{cid}"><b class="mk-key">–</b> <span data-caveat="{cid}">'
                + caveat_text(cid) + '</span></li>' + text[at:])
    return plant


PAGE_PLANTS = [
    ('Number text changed', 's7.forest_loss_ha_sop_2021', sub1(f'>8,856.91{NB}ha<', f'>8,856.92{NB}ha<')),
    ('data-raw changed', 's7.forest_loss_ha_sop_2021', sub1('data-raw="8856.91"', 'data-raw="8856.92"')),
    ('Locator changed', 's7.debt_to_equity_ratio_sop_2021',
     sub1('data-locator="firm_id=SOP; year=2021" data-column="debt_to_equity" data-raw="0.3463"',
          'data-locator="firm_id=SOP; year=2022" data-column="debt_to_equity" data-raw="0.3463"')),
    ('Untagged digit in text', 'untagged digit', in_main('<p>About 42 mills.</p>')),
    ('Number word in text', 'number written as a word', in_main('<p>About three mills.</p>')),
    ('Forest-loss note removed from a results block', 's7-forest',
     sub_re(r'<li id="s7-forest-forest_loss">.*?</li>', '', need=1)),
    ('Forest-loss note removed from a gap item (gap 9)', 'gap-9',
     sub_re(r'<li id="gap-9-forest_loss">.*?</li>', '', need=1)),
    ('Caveat wording changed', 'note forest_loss',
     sub1('not necessarily land cleared by the firm.</span>', 'not land cleared by the firm.</span>')),
    ('Sarawak note back to the old wording', 'note forest_loss_sarawak',
     sub1('<span data-caveat="forest_loss_sarawak">Loss from any cause, including replanting and logging.</span>',
          '<span data-caveat="forest_loss_sarawak">Loss from any cause inside Sarawak, including replanting and '
          'logging; not necessarily land cleared by the firm.</span>')),
    ('"+" added to a ratio', 's7.debt_to_equity_ratio_sop_2021',
     sub_re(r'(data-id="s7\.debt_to_equity_ratio_sop_2021"[^>]*>)0\.3463<', r'\g<1>+0.3463<')),
    ('Hyphen instead of the minus sign', 's5.grid_minus_sarawak_forest_loss_2022_ha',
     sub_re(r'(data-id="s5\.grid_minus_sarawak_forest_loss_2022_ha"[^>]*>)−', r'\g<1>-')),
    ('No space before a unit', 's7.forest_loss_ha_sop_2021', sub1(f'>8,856.91{NB}ha<', '>8,856.91ha<')),
    ('FFB unit with a space', 's7.ffb_yield_unit_as_printed_sop_2022', sub1(f'>14.50{NB}mt/ha<', f'>14.50{NB}mt/ ha<')),
    ('Quoted pilot text changed', 'text differs from the source',
     sub1('data-column="firm">Sarawak Oil Palms Berhad<', 'data-column="firm">Sarawak Oil Palm Berhad<')),
    ('No-tag reason misused (digits as a review ID)', 'not of the form',
     sub1('<small class="rid" data-notag="review ID">R043</small>', '<small class="rid" data-notag="review ID">42</small>')),
    ('Unknown no-tag reason', 'not allowed',
     sub1('<small class="rid" data-notag="review ID">R043</small>', '<small class="rid" data-notag="obvious">R043</small>')),
    ('Appendix field changed', 'meta s1.firms.raw',
     sub1('<code data-meta="raw" data-for="s1.firms">3</code>', '<code data-meta="raw" data-for="s1.firms">4</code>')),
    ('Digit in alt text', 'attribute text',
     sub1('alt="Map of Sarawak showing industrial', 'alt="Map 2 of Sarawak showing industrial')),
    ('Unknown data-id', 's5.grid_cells_x', sub1('data-id="s5.grid_cells"', 'data-id="s5.grid_cells_x"')),
    ('Spec number removed from the page', 's1.listed_growers_screened',
     sub_re(r'<span class="n[^"]*" data-id="s1\.listed_growers_screened"[^>]*>[^<]*</span>', '', count=0)),
    ('Removed hours number put back (section 9 row)', 's9.steps_1_9_total_h',
     in_main('<div data-block="x"><span class="n" data-id="s9.steps_1_9_total_h" data-file="reports/step10_findings.md" '
             'data-locator="## 6. Hours | row=Steps 1–9" data-column="Step total (h)" data-raw="13.5">13.5' + NB
             + 'h</span></div>')),
    # --- Step 5 decision 7: a note in a block where nothing needs it
    ('Note in a block where nothing needs it (peat note in gap 9)', "note peat_missing in block 'gap-9'",
     stray_note('gap-9', 'peat_missing')),
    ('Note in a block where nothing needs it (forest-loss note in the debt-to-equity block)',
     "note forest_loss in block 's7-debt'", stray_note('s7-debt', 'forest_loss')),
    ('Named note removed (import-ban table)', 'declared, but not listed',
     sub_re(r'<li id="s7-wro-wro_missing">.*?</li>', '', need=1)),
    ('data-needs on a paragraph', 'allowed only on',
     sub1('<p>The largest single catchment', '<p data-needs="forest_loss">The largest single catchment')),
    ('Note removed from the appendix list', 'appendix',
     sub_re(r'<li id="appendix-borders">.*?</li>', '', need=1)),
]


def main():
    pilot = pilot_dir()
    data_path = BUILD / 'site_data.json'
    if not pilot.is_dir() or not data_path.is_file():
        print('ERROR: needs the pilot (PILOT_DIR) and build/site_data.json (run scripts/extract.py first)')
        return 2
    if WORK.resolve() == pilot or pilot in WORK.resolve().parents:
        print('ERROR: build/ is inside the pilot folder; refusing to write.')
        return 2
    inputs = [i['file'] for i in json.loads(data_path.read_text(encoding='utf-8'))['inputs']]
    lines = []
    fresh_copies(pilot, inputs)
    code, out = run_check()
    base_ok = code == 0
    lines.append(f'Baseline (unchanged copies of {len(inputs)} pilot files): '
                 f'{"PASS" if base_ok else "FAIL"} (exit {code})')
    if not base_ok:
        lines.append(out)
    caught = 0
    for i, (what, marker, plant) in enumerate(PLANTS, 1):
        fresh_copies(pilot, inputs)
        try:
            plant()
        except AssertionError as e:
            lines.append(f'{i:2}. {what}: could not plant ({e})')
            continue
        code, out = run_check()
        named = [ln.strip() for ln in out.splitlines() if ln.startswith('  [') and marker in ln]
        ok = code == 1 and bool(named)
        caught += ok
        lines.append(f'{i:2}. {what} [{marker}]: {"caught" if ok else "NOT CAUGHT"} (exit {code})')
        if named:
            lines.append(f'      {named[0]}')
    lines.append(f'Planted errors caught (data, spec, pilot copies): {caught} of {len(PLANTS)}.')
    # the page
    fresh_copies(pilot, inputs)
    page_text = (SITE / 'site' / 'index.html').read_text(encoding='utf-8')
    page_copy = WORK / 'index.html'
    page_copy.write_text(page_text, encoding='utf-8')
    code, out = run_check(page_copy)
    page_ok = code == 0
    lines.append(f'Page baseline (unchanged copy of site/index.html): {"PASS" if page_ok else "FAIL"} (exit {code})')
    if not page_ok:
        lines.append(out)
    page_caught = 0
    for i, (what, marker, plant) in enumerate(PAGE_PLANTS, 1):
        try:
            planted = plant(page_text)
        except (AssertionError, ValueError) as e:
            lines.append(f'P{i:02}. {what}: could not plant ({e})')
            continue
        page_copy.write_text(planted, encoding='utf-8')
        code, out = run_check(page_copy)
        named = [ln.strip() for ln in out.splitlines() if ln.startswith('  [') and marker in ln]
        ok = code == 1 and bool(named)
        page_caught += ok
        lines.append(f'P{i:02}. {what} [{marker}]: {"caught" if ok else "NOT CAUGHT"} (exit {code})')
        if named:
            lines.append(f'      {named[0]}')
    shutil.rmtree(WORK)
    lines.append(f'Planted errors caught (page): {page_caught} of {len(PAGE_PLANTS)}. '
                 f'Copies in {WORK.relative_to(SITE)} deleted.')
    passed = base_ok and caught == len(PLANTS) and page_ok and page_caught == len(PAGE_PLANTS)
    lines.append('Result: ' + ('PASS' if passed else 'FAIL'))
    text = '\n'.join(lines) + '\n'
    print(text, end='')
    (BUILD / 'test_check_numbers.txt').write_text(text, encoding='utf-8')
    return 0 if passed else 1


if __name__ == '__main__':
    sys.exit(main())
