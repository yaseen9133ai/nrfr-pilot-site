# Palm oil pilot: from public data to a traceable table

A static web page that explains a palm oil pilot to a non-technical audience: what it built from public data, how every value can be traced back to its source, and what did not work. The page presents what the pilot produced; it adds no data or analysis.

- **The page** is `site/index.html` with `site/assets/`. Only `site/` is published.
- **Live:** https://nrfr-pilot.vercel.app/ (Vercel publishes `site/` on every push to `main`).
- **Every number on the page** is inserted by a script from the pilot's own files and carries a source tag: the pilot file, the row, the column and the raw value. The page's appendix, "Where the numbers come from", lists every number with its tag.
- **It works offline:** no scripts, web fonts, analytics or other requests to other sites.

## What you need

- Python, standard library only (nothing to install).
- The pilot folder. The pilot itself is not published, so the page can be rebuilt and checked only where the pilot folder is present. The scripts never write in it.
- Every script reads the pilot's location from the environment variable `PILOT_DIR`. The default is `../nrfr-pilot`; a relative value is read from this folder.

## Rebuild the page

Run from this folder, in this order (`-B` stops Python from writing cache files):

```sh
export PILOT_DIR=../nrfr-pilot                  # where the pilot folder is (this is the default)
python3 -B scripts/pilot_snapshot.py --check    # confirms the pilot is unchanged since the local baseline
python3 -B scripts/copy_images.py               # copies the map images into site/assets/ and writes their manifest
python3 -B scripts/extract.py                   # reads the pilot, writes build/site_data.json
python3 -B scripts/build_page.py                # writes site/index.html and site/assets/style.css
```

- `extract.py` reads the list of numbers in `docs/number_sources.csv` (file, locator, column and expected value of each) and the notes in `docs/caveats.csv`. It stops if any number cannot be found exactly where the list says.
- `build_page.py` reads only `build/site_data.json`. The same input gives a byte-identical page.
- `pilot_snapshot.py` without `--check` takes the local baseline the first time (it refuses to replace an existing one without `--force`).

## Run the checks

```sh
python3 -B scripts/check_numbers.py       # every number and quoted text on the page, read again from the pilot; notes; no untagged digits
python3 -B scripts/test_check_numbers.py  # planted errors in copies of the data and the page: each one must be caught
python3 -B scripts/check_offline.py       # nothing loaded from outside site/; every local file, link and image size checked
python3 -B scripts/check_links.py         # every in-page link, image link, pilot path and heading named on the page exists
python3 -B scripts/scan_exclusions.py site/index.html docs/*.csv   # personal data, absolute paths and terms that must not be published
```

- To check a downloaded copy of the live page instead, give its folder: `check_numbers.py --html <folder>/index.html` and `check_links.py --site <folder>`.
- Each check ends with its result (`PASS` or `CLEAN`) and writes nothing in the pilot. Reports go to `build/`, which is git-ignored.
- `scan_exclusions.py` also needs a local term list, `build/private_terms.txt`, which is not in the repository; without it the scan stops.

## Folders

- `site/` the published page.
- `scripts/` the build and check scripts.
- `docs/` planning notes: content inventory, page outline, the number list and the notes.
- `build/` working files (extracted data, check reports, local copies); git-ignored, never published.
- `CLAUDE.md` working rules and decisions; `PROGRESS.md` the progress log.

## Licences

- Scripts and the style sheet they write: MIT License (`LICENSES/MIT.txt`).
- Page text, planning files, and the pilot's images in `site/assets/`: CC BY 4.0, with the data credits shown on the page.
- ENCORE-derived content: CC BY-SA 4.0, with the ENCORE citation.
- Third-party material keeps its own terms; the page credits each source where it is used.

Details: `LICENSE.md`. Author: Yaseen (Research Assistant).
