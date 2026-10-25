"""Snapshot of nrfr-pilot (read-only), and a check against it.

nrfr-pilot is read-only for this project. This script only opens its files
for reading and runs read-only git commands there. It writes only to
nrfr-pilot-site/build/.

Two scopes, set by SITE_SCOPE below:
  site   files the site might use: path, size, mtime and SHA-256.
  other  every other file in nrfr-pilot (raw downloads, rasters, copies):
         path, size and mtime only, so a write anywhere in the pilot shows up.
Ignored everywhere: .DS_Store (macOS Finder writes it when a folder is viewed).

Pilot path: the environment variable PILOT_DIR (default ../nrfr-pilot; a
relative value is read from nrfr-pilot-site/). --pilot overrides it.

Usage (from anywhere):
  python3 scripts/pilot_snapshot.py            take the baseline (refuses to
                                               overwrite an existing one)
  python3 scripts/pilot_snapshot.py --force    replace the baseline (only with
                                               Yaseen's approval)
  python3 scripts/pilot_snapshot.py --check    compare nrfr-pilot with the
                                               baseline; exit 0 = no change,
                                               1 = change, 2 = error

Outputs (nrfr-pilot-site/build/):
  pilot_snapshot.csv         one row per file: path, scope, size_bytes,
                             mtime_ns, mtime_utc, sha256 (site scope only)
  pilot_snapshot_info.json   pilot path, time taken, counts, git state
  pilot_snapshot_checks.log  one line appended per --check run

Python standard library only.
"""

import argparse
import csv
import datetime as dt
import fnmatch
import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path

SITE_ROOT = Path(__file__).resolve().parent.parent
BUILD = SITE_ROOT / 'build'
SNAPSHOT_CSV = BUILD / 'pilot_snapshot.csv'
INFO_JSON = BUILD / 'pilot_snapshot_info.json'
CHECK_LOG = BUILD / 'pilot_snapshot_checks.log'

# Files the site might use (paths relative to nrfr-pilot, fnmatch patterns;
# '*' also matches '/'). Everything else is scope "other".
SITE_SCOPE = [
    'CLAUDE.md',
    'evidence.csv',
    'feature_dictionary.csv',
    'progress_log.md',
    'review_queue.csv',
    'source_register.csv',
    'docs/PILOT_PLAN.md',
    'docs/methods/*.md',
    'data/raw_files.csv',
    'data/processed/*',
    'data/interim/*.csv',
    'data/interim/*.geojson',
    'reports/*',
    'scripts/*.py',
    'scripts/*.sh',
    'scripts/*.txt',
]
# data/interim/*.csv must not reach into the subfolders (AR page extracts,
# Sentinel-2 chips, palm tiles): those stay in scope "other".
SITE_SCOPE_EXCLUDE = [
    'data/interim/*/*',
    'scripts/__pycache__/*',
]
IGNORED_NAMES = {'.DS_Store'}

FIELDS = ['path', 'scope', 'size_bytes', 'mtime_ns', 'mtime_utc', 'sha256']


def default_pilot():
    """The one pilot-path setting: PILOT_DIR, default ../nrfr-pilot (relative to SITE_ROOT)."""
    p = Path(os.environ.get('PILOT_DIR') or '../nrfr-pilot')
    return p if p.is_absolute() else SITE_ROOT / p


def scope_of(rel):
    if any(fnmatch.fnmatchcase(rel, p) for p in SITE_SCOPE_EXCLUDE):
        return 'other'
    if any(fnmatch.fnmatchcase(rel, p) for p in SITE_SCOPE):
        return 'site'
    return 'other'


def sha256_of(path):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for block in iter(lambda: f.read(1 << 20), b''):
            h.update(block)
    return h.hexdigest()


def utc_text(ns):
    return dt.datetime.fromtimestamp(ns / 1e9, dt.timezone.utc).strftime('%Y-%m-%dT%H:%M:%S.%fZ')


def scan(pilot):
    """Walk nrfr-pilot (read-only) and return {path: row}, plus ignored count."""
    rows, ignored = {}, 0
    for dirpath, dirnames, filenames in os.walk(pilot):
        dirnames.sort()
        for name in sorted(filenames):
            full = Path(dirpath) / name
            rel = full.relative_to(pilot).as_posix()
            if name in IGNORED_NAMES:
                ignored += 1
                continue
            st = os.stat(full)
            scope = scope_of(rel)
            rows[rel] = {
                'path': rel,
                'scope': scope,
                'size_bytes': str(st.st_size),
                'mtime_ns': str(st.st_mtime_ns),
                'mtime_utc': utc_text(st.st_mtime_ns),
                'sha256': sha256_of(full) if scope == 'site' else '',
            }
    return rows, ignored


def git_state(pilot):
    """Read-only git commands. No optional locks, so the index is not refreshed."""
    env = dict(os.environ, GIT_OPTIONAL_LOCKS='0')

    def run(*args):
        r = subprocess.run(['git', '--no-optional-locks', '-C', str(pilot), *args],
                           capture_output=True, text=True, env=env)
        return r.returncode, r.stdout.strip(), r.stderr.strip()

    code, top, err = run('rev-parse', '--show-toplevel')
    if code != 0:
        return {'is_repo': False, 'detail': err}
    state = {'is_repo': Path(top).resolve() == pilot, 'toplevel': top}
    if not state['is_repo']:
        state['detail'] = 'nrfr-pilot is inside another repository, not its own'
    _, state['commit'], _ = run('rev-parse', 'HEAD')
    _, state['status_porcelain'], _ = run('status', '--porcelain=v1', '--untracked-files=all')
    return state


def guard_output(pilot):
    # Never write inside nrfr-pilot.
    if BUILD.resolve() == pilot or pilot in BUILD.resolve().parents:
        sys.exit(f'ERROR: output folder {BUILD} is inside nrfr-pilot; refusing to write.')


def write_csv(path, rows):
    with open(path, 'w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=FIELDS, lineterminator='\n')
        w.writeheader()
        for rel in sorted(rows):
            w.writerow(rows[rel])


def read_csv(path):
    with open(path, newline='', encoding='utf-8') as f:
        return {r['path']: r for r in csv.DictReader(f)}


def counts(rows):
    out = {}
    for scope in ('site', 'other'):
        sel = [r for r in rows.values() if r['scope'] == scope]
        out[scope] = {'files': len(sel), 'bytes': sum(int(r['size_bytes']) for r in sel)}
    return out


def take(pilot, force):
    if SNAPSHOT_CSV.exists() and not force:
        sys.exit(f'ERROR: {SNAPSHOT_CSV} exists. Use --check to compare, or --force to replace '
                 'the baseline (only with Yaseen\'s approval).')
    BUILD.mkdir(exist_ok=True)
    taken = dt.datetime.now(dt.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
    rows, ignored = scan(pilot)
    write_csv(SNAPSHOT_CSV, rows)
    info = {
        'pilot_root': str(pilot),
        'site_root': str(SITE_ROOT),
        'taken_utc': taken,
        'script': 'scripts/pilot_snapshot.py',
        'counts': counts(rows),
        'ignored_names': sorted(IGNORED_NAMES),
        'ignored_files': ignored,
        'site_scope_patterns': SITE_SCOPE,
        'site_scope_exclude': SITE_SCOPE_EXCLUDE,
        'git': git_state(pilot),
        'snapshot_csv_sha256': sha256_of(SNAPSHOT_CSV),
    }
    with open(INFO_JSON, 'w', encoding='utf-8') as f:
        json.dump(info, f, indent=2, ensure_ascii=False)
        f.write('\n')
    c = info['counts']
    print(f'Snapshot taken {taken} of {pilot}')
    print(f"  site scope : {c['site']['files']} files, {c['site']['bytes']:,} bytes (SHA-256)")
    print(f"  other scope: {c['other']['files']} files, {c['other']['bytes']:,} bytes (size + mtime)")
    print(f'  ignored    : {ignored} .DS_Store files')
    g = info['git']
    print(f"  git        : {'repo, commit ' + g.get('commit', '') if g['is_repo'] else 'not a git repository'}")
    print(f'Wrote {SNAPSHOT_CSV} and {INFO_JSON}')


def check(pilot):
    if not SNAPSHOT_CSV.exists() or not INFO_JSON.exists():
        print(f'ERROR: no baseline in {BUILD}; run without --check first.')
        return 2
    base = read_csv(SNAPSHOT_CSV)
    with open(INFO_JSON, encoding='utf-8') as f:
        info = json.load(f)
    problems = []
    if sha256_of(SNAPSHOT_CSV) != info.get('snapshot_csv_sha256'):
        problems.append('BASELINE: build/pilot_snapshot.csv differs from the hash in pilot_snapshot_info.json')
    if info.get('pilot_root') != str(pilot):
        problems.append(f"PILOT PATH: baseline {info.get('pilot_root')} vs now {pilot}")

    now, _ = scan(pilot)
    changed, touched = [], []
    missing = sorted(set(base) - set(now))
    new = sorted(set(now) - set(base))
    for rel in sorted(set(base) & set(now)):
        b, n = base[rel], now[rel]
        if b['scope'] == 'site' and n['scope'] == 'site':
            if b['sha256'] != n['sha256'] or b['size_bytes'] != n['size_bytes']:
                changed.append((rel, 'site', f"size {b['size_bytes']} -> {n['size_bytes']}, sha256 differs"))
            elif b['mtime_ns'] != n['mtime_ns']:
                touched.append(rel)
        elif b['size_bytes'] != n['size_bytes'] or b['mtime_ns'] != n['mtime_ns']:
            changed.append((rel, n['scope'], f"size {b['size_bytes']} -> {n['size_bytes']}, "
                                             f"mtime {b['mtime_utc']} -> {n['mtime_utc']}"))

    g_base, g_now = info.get('git', {}), git_state(pilot)
    for key in ('is_repo', 'commit', 'status_porcelain'):
        if g_base.get(key) != g_now.get(key):
            problems.append(f'GIT {key}: {g_base.get(key)!r} -> {g_now.get(key)!r}')

    stamp = dt.datetime.now(dt.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
    print(f"Check {stamp} against baseline {info.get('taken_utc')} ({len(base)} files)")
    for rel, scope, what in changed:
        print(f'  CHANGED [{scope}] {rel}: {what}')
    for rel in missing:
        print(f"  MISSING [{base[rel]['scope']}] {rel}")
    for rel in new:
        print(f"  NEW     [{now[rel]['scope']}] {rel}")
    for p in problems:
        print(f'  {p}')
    for rel in touched:
        print(f'  note: mtime changed, content identical (not a change): {rel}')
    fail = bool(changed or missing or new or problems)
    result = 'CHANGE' if fail else 'NO CHANGE'
    print(f'Result: {result} (changed {len(changed)}, missing {len(missing)}, new {len(new)}, '
          f'other problems {len(problems)}; {len(now)} files now)')
    BUILD.mkdir(exist_ok=True)
    with open(CHECK_LOG, 'a', encoding='utf-8') as f:
        f.write(f"{stamp}\tbaseline {info.get('taken_utc')}\t{result}\tchanged={len(changed)}\t"
                f"missing={len(missing)}\tnew={len(new)}\tproblems={len(problems)}\t"
                f"touched={len(touched)}\tfiles_now={len(now)}\n")
    return 1 if fail else 0


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--pilot', default=str(default_pilot()),
                    help='path to nrfr-pilot (default: $PILOT_DIR, else ../nrfr-pilot)')
    ap.add_argument('--check', action='store_true', help='compare with the baseline; write nothing but the log')
    ap.add_argument('--force', action='store_true', help='replace an existing baseline')
    args = ap.parse_args()
    pilot = Path(args.pilot).resolve()
    if not pilot.is_dir():
        print(f'ERROR: nrfr-pilot not found at {pilot}')
        return 2
    guard_output(pilot)
    if args.check:
        return check(pilot)
    take(pilot, args.force)
    return 0


if __name__ == '__main__':
    sys.exit(main())
