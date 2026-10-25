"""Copy the page's images from the pilot (read-only) into site/assets/.

IMAGES below is the selection (docs/page_outline.md, open question 10, as
taken up in Step 4). Each file is copied unchanged (no resizing), and
site/assets/manifest.csv records, for every image, the published name, the
pilot path, the size in bytes and the SHA-256 of the copy, which must equal
the SHA-256 of the pilot file.

Every image was looked at for personal data before it was added here
(PROGRESS.md, Step 4). An image that shows personal data is not added.

Pilot path: PILOT_DIR (default ../nrfr-pilot, relative to nrfr-pilot-site/).
Writes only in site/assets/. Exit 0 = copied, 1 = a file is missing or the
copy differs, 2 = setup error.

Python standard library only.
"""

import csv
import hashlib
import io
import os
import sys
from pathlib import Path

SITE = Path(__file__).resolve().parent.parent
ASSETS = SITE / 'site' / 'assets'
MANIFEST = ASSETS / 'manifest.csv'

# (published name in site/assets/, pilot path)
IMAGES = [
    ('step5_map_palm.png', 'reports/step5_maps/step5_map_palm.png'),
    ('step8_catchments_map.png', 'reports/step8_checks/step8_catchments_map.png'),
    ('step9_loss_2021.png', 'reports/step9_maps/step9_loss_2021.png'),
    ('step9_loss_2022.png', 'reports/step9_maps/step9_loss_2022.png'),
    ('step9_loss_2023.png', 'reports/step9_maps/step9_loss_2023.png'),
    ('step9_distances.png', 'reports/step9_maps/step9_distances.png'),
    ('step9_zoom_check.png', 'reports/step9_maps/step9_zoom_check.png'),
    ('step5_map_forest.png', 'reports/step5_maps/step5_map_forest.png'),
]


def pilot_dir():
    p = Path(os.environ.get('PILOT_DIR') or '../nrfr-pilot')
    return (p if p.is_absolute() else SITE / p).resolve()


def main():
    pilot = pilot_dir()
    if not pilot.is_dir():
        print(f'ERROR: pilot folder not found (PILOT_DIR): {pilot}')
        return 2
    if ASSETS.resolve() == pilot or pilot in ASSETS.resolve().parents:
        print('ERROR: site/assets/ is inside the pilot folder; refusing to write.')
        return 2
    ASSETS.mkdir(parents=True, exist_ok=True)
    rows, problems = [], []
    for name, rel in IMAGES:
        src = (pilot / rel).resolve()
        if pilot not in src.parents or not src.is_file():
            problems.append(f'{rel}: not found in the pilot')
            continue
        blob = src.read_bytes()
        digest = hashlib.sha256(blob).hexdigest()
        dst = ASSETS / name
        if not dst.is_file() or dst.read_bytes() != blob:
            dst.write_bytes(blob)
        if hashlib.sha256(dst.read_bytes()).hexdigest() != digest:
            problems.append(f'{name}: the copy differs from {rel}')
        rows.append([name, rel, str(len(blob)), digest])
    if problems:
        for p in problems:
            print(f'FAIL: {p}')
        return 1
    buf = io.StringIO()
    w = csv.writer(buf, lineterminator='\n')
    w.writerow(['asset', 'pilot_path', 'bytes', 'sha256'])
    w.writerows(rows)
    MANIFEST.write_text(buf.getvalue(), encoding='utf-8')
    total = sum(int(r[2]) for r in rows)
    print(f'Copied {len(rows)} images ({total:,} bytes) to site/assets/; wrote site/assets/manifest.csv.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
