"""Scan files for content that must not be published (CLAUDE.md rules 6 and 12).

Usage: python3 scripts/scan_exclusions.py [file ...]   (default: build/site_data.json)

Checks, each reported as a count (matched values are never printed, so the
report itself holds no personal or private data):
  e-mail      e-mail addresses
  paths       absolute local paths (/Users/, /home/, /private/, /var/folders/, /tmp/, C:\\, ~/)
  phone       Malaysian and international phone-number patterns
  emspo       eMSPO contact field names (picName, directorPhone, ...), and their
              values: read at run time from the pilot's data/raw/MSPO/emspo_*.json
              (read-only) and searched for in the files
  titles      personal titles (Dato', Datuk, Tan Sri, Encik, Puan, Mr., Mrs., Ms., Dr.)
  name        "Yaseen" followed by a capitalised word (a possible full name),
              other than "Yaseen (Research Assistant)"; the repository-local git
              user.email and its local part (read from .git/config)
  private     terms in build/private_terms.txt (git-ignored; public-release
              decision 4: project-internal terms, and the project name);
              a hit is reported by its line number in that file

Pilot path: PILOT_DIR (default ../nrfr-pilot, relative to nrfr-pilot-site/).
Exit 0 = nothing found, 1 = something found, 2 = setup error (for example
build/private_terms.txt missing).

Python standard library only.
"""

import json
import os
import re
import subprocess
import sys
from pathlib import Path

SITE = Path(__file__).resolve().parent.parent
PRIVATE = SITE / 'build' / 'private_terms.txt'
CONTACT_KEYS = ('picName', 'picPhone', 'picEmail', 'directorName', 'directorPhone', 'directorEmail',
                'entityEmail', 'entityPhone', 'address1', 'address2')

PATTERNS = {
    'e-mail': [r'[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}'],
    'paths': [r'/Users/', r'/home/', r'/private/', r'/var/folders/', r'/tmp/', r'[A-Za-z]:\\', r'(?<![\w.])~/'],
    'phone': [r'(?<![\d.,])(?:\+?60[\s-]?|0)1\d[\s-]?\d{3,4}[\s-]?\d{4}(?![\d.,])',
              r'(?<![\d.,])(?:\+?60[\s-]?|0)[3-9][\s-]?\d{3,4}[\s-]?\d{4}(?![\d.,])',
              r'\+\d{2,3}[\s-]\d{1,4}[\s-]?\d{3,4}[\s-]?\d{3,4}'],
    'titles': [r"\bDato'?\b", r'\bDatuk\b', r'\bTan Sri\b', r'\bEncik\b', r'\bPuan\b',
               r'\bMrs?\.(?=\s)', r'\bMs\.(?=\s)', r'\bDr\.(?=\s)'],
    'name': [r'\bYaseen\s+(?!\(Research Assistant\))[A-Z][a-z]+'],
}


def pilot_dir():
    p = Path(os.environ.get('PILOT_DIR') or '../nrfr-pilot')
    return (p if p.is_absolute() else SITE / p).resolve()


def contact_values(pilot):
    """Values of the eMSPO contact fields, from the pilot's raw records (read-only)."""
    texts, phones, nfiles = set(), set(), 0
    for f in sorted((pilot / 'data' / 'raw' / 'MSPO').glob('emspo_*.json')):
        nfiles += 1

        def walk(o):
            if isinstance(o, dict):
                for k, v in o.items():
                    if k in CONTACT_KEYS and isinstance(v, (str, int)) and str(v).strip():
                        s = str(v).strip()
                        if 'Phone' in k:
                            d = re.sub(r'\D', '', s)
                            if len(d) >= 7:
                                phones.add(d)
                        elif len(s) >= 5:
                            texts.add(s.lower())
                    walk(v)
            elif isinstance(o, list):
                for v in o:
                    walk(v)
        walk(json.loads(f.read_text(encoding='utf-8')))
    return texts, phones, nfiles


def git_email():
    r = subprocess.run(['git', '-C', str(SITE), 'config', '--local', '--get', 'user.email'],
                       capture_output=True, text=True)
    return r.stdout.strip() if r.returncode == 0 else ''


def private_terms():
    terms = []
    for i, line in enumerate(PRIVATE.read_text(encoding='utf-8').splitlines(), 1):
        t = line.strip()
        if t and not t.startswith('#'):
            terms.append((i, t))
    return terms


def main():
    files = [Path(a).resolve() for a in sys.argv[1:]] or [SITE / 'build' / 'site_data.json']
    if not PRIVATE.is_file():
        print(f'ERROR: {PRIVATE.relative_to(SITE)} is missing (the private term list; see its header '
              'in PROGRESS.md, Step 3). Nothing scanned.')
        return 2
    pilot = pilot_dir()
    if not (pilot / 'data' / 'raw' / 'MSPO').is_dir():
        print(f'ERROR: pilot eMSPO records not found under PILOT_DIR ({pilot}).')
        return 2
    texts, phones, nfiles = contact_values(pilot)
    email = git_email()
    terms = private_terms()
    total = 0
    for path in files:
        text = path.read_text(encoding='utf-8')
        # SHA-256 hashes are not phone numbers; blank them before the phone patterns run.
        plain = re.sub(r'\b[0-9a-f]{64}\b', ' ', text)
        low = plain.lower()
        found = {}
        for check, pats in PATTERNS.items():
            n = sum(len(re.findall(p, plain)) for p in pats)
            found[check] = n
        found['emspo'] = sum(low.count(k.lower()) for k in CONTACT_KEYS if len(k) > 0) + \
            sum(1 for v in texts if v in low)
        runs = {re.sub(r'\D', '', m) for m in re.findall(r'[\d][\d\s-]{5,}[\d]', plain)}
        found['emspo'] += sum(1 for p in phones if any(p in r for r in runs))
        if email:
            found['name'] += low.count(email.lower()) + low.count(email.split('@')[0].lower())
        hits = [i for i, t in terms
                if re.search(r'(?<![A-Za-z0-9])' + r'\s+'.join(map(re.escape, t.split())) + r'(?![A-Za-z0-9])',
                             plain, flags=re.I)]
        found['private'] = len(hits)
        n = sum(found.values())
        total += n
        shown = path.relative_to(SITE) if SITE in path.parents else path.name
        print(f'{shown}: ' + ', '.join(f'{k} {v}' for k, v in found.items())
              + (f'  (private term lines: {hits})' if hits else '')
              + ('  CLEAN' if n == 0 else '  FOUND'))
    print(f'Compared with {len(texts)} eMSPO contact texts and {len(phones)} phone numbers '
          f'from {nfiles} raw eMSPO files (values not shown); {len(terms)} private terms; '
          f'git user.email {"set" if email else "not set"} (not shown).')
    print('Result: ' + ('CLEAN' if total == 0 else 'FOUND'))
    return 0 if total == 0 else 1


if __name__ == '__main__':
    sys.exit(main())
