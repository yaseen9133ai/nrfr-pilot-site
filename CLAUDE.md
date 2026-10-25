# Palm oil pilot site

A static web page that explains a palm oil pilot to a non-technical audience. It presents what the pilot already produced; it adds nothing to it.

- Pilot (source, read-only): `../nrfr-pilot` (the folder beside this one)
- Site (this folder): `.`
- Paths in this repository are relative: to this folder, or to the pilot folder where a file says so.
- Pilot path setting: every script takes the pilot path from one setting, the environment variable `PILOT_DIR` (default `../nrfr-pilot`; a relative value is read from this folder).
- Publication (decided by Yaseen (Research Assistant), 2026-10-25): this repository will be **public on GitHub**, and the page will be deployed on **Vercel**, which publishes only `site/`. Both happen at Step 6, not before, and only after the PI's permission is recorded (rule 14; recorded on 2026-10-25, Step 5 decision 10).

At the start of every session, read the Current status in `PROGRESS.md`.

## Rules

1. **The pilot is READ-ONLY.** Never write, move, rename or delete anything in it, and never run a script that writes in it (this includes the pilot's own scripts and runners, and importing pilot scripts, which would write `__pycache__`). Read or copy only. Copies go into this folder.
2. **No hand-typed numbers.** Every number on the page comes from a script in `scripts/` that reads the pilot's CSVs and tracking files. No number is typed into HTML, templates or page text by hand.
3. **Every number carries a source tag** (file, row key, column). A check script compares every tagged number in the HTML with its source and fails on any mismatch or untagged number.
4. **No new data, analysis or features.** Gaps and weak points are shown honestly, as findings, in the pilot's own terms. Nothing is filled, estimated or substituted.
5. **Plain language** for a non-technical audience. Each section names the pilot path where the details live, as plain text (the pilot is not published, so a link would lead nowhere).
6. **Exclude:**
   - personal data (eMSPO contact names, phone numbers, e-mails);
   - raw annual-report PDFs and page extracts;
   - raw downloads (`data/raw/`);
   - scratch files and copies (for example `__pycache__/`, `.DS_Store`; the pilot's `untitled folder/` was deleted by Yaseen on 2026-10-25).
7. **Attributions:** include every attribution the source licences require (list in `docs/content_inventory.md`, section b).
8. **Static site:** the deployable page lives in `site/`: `site/index.html` + `site/assets/`. Vercel will publish only `site/`. Works offline: no CDN, web fonts, analytics or other external calls. Build and check scripts use the Python standard library only.
9. **One step at a time.** At the end of each step, update `PROGRESS.md`, then STOP and report. Never start the next step.
10. **Pilot snapshot.** At the start and at the end of every step, run `python3 scripts/pilot_snapshot.py --check`. Any change (exit code not 0) = stop and report. Replace the baseline (`--force`) only with Yaseen's approval.
11. **No remote, no push.** Do not add a git remote or push until Yaseen approves it at Step 6.
12. **Everything committed must be safe to publish.** The repository will be public. Do not commit:
    - personal data;
    - raw downloads;
    - annual-report PDFs or page extracts;
    - copies of pilot CSVs beyond what the page needs.

    This applies to every tracked file, including `CLAUDE.md`, `PROGRESS.md`, `docs/` and `scripts/`, not only `site/`. Before committing, check against `docs/content_inventory.md`, section e (Public release check).
13. **`build/` holds working files only** (pilot snapshot, extracted data, check output, local copies of pilot data). It is git-ignored and never deployed. Local copies of pilot data go only in `build/`.
14. **No push until the PI's permission is recorded in `PROGRESS.md`.** This comes on top of rule 11: even with Yaseen's Step 6 approval, nothing is pushed and nothing is deployed until `PROGRESS.md` records the PI's permission.

## Public-release decisions (Yaseen, 2026-10-25)

1. **Name.** Yaseen appears as "Yaseen (Research Assistant)" on the page and in repository files (the planning files use "Yaseen" for short after that). No full name and no student ID.
2. **Paths.** `CLAUDE.md`, `PROGRESS.md` and `docs/` use relative paths, never absolute ones.
3. **Git identity.** Set for this repository only (`git config --local`): `user.email` = the address Yaseen gave on 2026-10-25. It is stored in `.git/config` and not repeated in tracked files, so the e-mail scan before any commit stays clean. `user.name` = "Yaseen" (set 2026-10-25, Step 2 close-out). Since 2026-10-26 (Step 5 close-out decision 6), `user.email` = Yaseen's GitHub no-reply address, because git writes the author e-mail into every commit and the repository is public.
4. **Purpose and name of the pilot.** Describe the pilot neutrally: a proof that the data chain can be built and traced (raw public sources → tables → evidence for every value). Project-internal content is never published: the page and the repository describe only what the pilot produced, in neutral terms, and never quote or summarise project-internal documents. The terms to scan for are kept only in the local, git-ignored `build/private_terms.txt`. Call it the "palm oil pilot" in prose. On the page, since Step 5 close-out decision 4: the title "NRFR palm oil pilot", the name once in the intro, "the pilot" elsewhere. The project's name may appear in folder names, paths and the repository (Step 5 decision 11); the folders keep their names (`nrfr-pilot`, `nrfr-pilot-site`; Step 2 decision 2 below).
5. **Forest-loss caveat.** Next to every forest-loss number. Wording since Step 3 decision 7 (below): "Loss from any cause inside the catchment area, including replanting and logging; not necessarily land cleared by the firm." Sarawak-wide numbers have their own wording since Step 4 decision 2 (below).
6. **Third-party content.**
   - Universal Mill List (UML) points: shown, with credit and the words "no licence stated".
   - ENCORE content: "CC BY-SA 4.0" stated next to it, with the ENCORE citation.
7. **Licences of this repository** (`LICENSE.md`):
   - scripts: MIT (`LICENSES/MIT.txt`);
   - page text: CC BY 4.0;
   - ENCORE-derived content: CC BY-SA 4.0.

   Third-party material keeps its own terms (`docs/content_inventory.md`, section b).
8. **Named companies.** Factual, sourced and neutral wording only. No judgements, no rankings, no words such as "clean", "compliant", "worst" or "best".

## Step 2 decisions: numbers and sources (Yaseen, 2026-10-25)

1. **Git name.** `git config --local user.name "Yaseen"` (public-release decision 3).
2. **Folders keep their names** (`nrfr-pilot`, `nrfr-pilot-site`). The pilot path comes from one setting, `PILOT_DIR` (default `../nrfr-pilot`), in every script. A neutral GitHub repository name is a Step 6 decision.
3. **Markdown sources are allowed**, read only from a fixed locator: file + heading + table row (by its first cell) or list item / paragraph (by its label) + column or exact quote. Prefer the CSV when the same number exists in a CSV cell. A missing or ambiguous locator is an error.
4. **No tag needed for:** review IDs, step and section numbers, years used as labels, dates, versions, file names, ISIC codes, licence versions. Every other number is tagged.
5. **Number format:** source decimals and signs kept, thousands separators added, unit next to the number, no extra rounding.
6. **Source tag:** accepted if it carries file, locator, column and raw value.
7. **Hours:** headline 13.5 h for steps 1–9; step 10 (0.2 h) and the dataset README (0.1 h) shown as small additions; scripts shown as "33 at the time of the findings report".

The number list is `docs/number_sources.csv` (spec for `scripts/extract.py`); caveat wording is in `docs/caveats.csv`.

## Step 3 decisions: page format and content (Yaseen, 2026-10-25)

1. **Tags.** Each number on the page sits in a `<span>` that carries its file, locator, column and raw value. A collapsible appendix, "Where the numbers come from", lists every number with its tag.
2. **Units.** A space before every unit except `%`. FFB units are shown as "mt/ha" or "Mt/WHa"; the printed form (for example "mt/ ha") stays in the tag.
3. **Signs.** The true minus sign "−" everywhere. "+" is added only to rainfall anomalies.
4. **Dates and ranges.** Dates are written for readers ("24 October 2026"); ranges use an en dash ("1991–2020").
5. **No-tag list** (adds to Step 2 decision 4): digits inside names and identifiers, such as Sentinel-2, UTM 49N, Note 19, HTTP 500, and similar.
6. **Counted numbers in text** are digits with tags, never words ("3 firms", not "three firms").
7. **Forest-loss caveat wording:** "Loss from any cause inside the catchment area, including replanting and logging; not necessarily land cleared by the firm." (Public-release decision 5 updated.)
8. **Hours.** 13.5 h for steps 1–9, then "+ 0.2 h (findings report)" and "+ 0.1 h (dataset guide)", with no new total. The Claude Code / Yaseen split is shown, flagged "Claude Code hours mostly unconfirmed (R058)". *Superseded by Step 4 decision 10: the hours section was removed.*
9. **Content.**
   - ENCORE as a summary (rating counts per activity), not the 50 ratings.
   - Mill table: the 12 mills, firm and name only, no coordinates.
   - Review IDs small and grey.
   - The catchment areas (km²) from `evidence.csv` are added to `docs/number_sources.csv`, tagged.
10. **Credits.**
    - Hansen et al. (2013) Science; Hansen/UMD/Google/USGS/NASA; CC BY 4.0.
    - "Contains modified Copernicus Sentinel data (2021, 2024)". *Removed by Step 4 decision 1, with the only image that showed Sentinel data.*
    - "© OpenStreetMap contributors, ODbL" wherever roads appear.
    - The other credits as recorded in `build/site_data.json`.
11. **Licences.** The planning files (`CLAUDE.md`, `PROGRESS.md`, `docs/`) and the images in `site/assets/` are CC BY 4.0, with the data credits above (`LICENSE.md`).

## Step 4 decisions: close-out (Yaseen, 2026-10-25)

1. **Sepakau check image dropped** (it showed a working note, Yaseen's name and an eMSPO record ID). Removed from `site/assets/`, the manifest and the page. The Copernicus credit covered only that image, so it was removed too (page footer, `LICENSE.md`).
2. **Sarawak-wide forest-loss note:** "Loss from any cause, including replanting and logging." The firm caveat (Step 3 decision 7) stays on the firm numbers.
3. **Image sizes** typed in `scripts/build_page.py` (`width`/`height`, layout only, checked by `scripts/check_offline.py`): accepted.
4. **Distance map caption:** a note that the map title and the grid's figure (153.5 km) differ, naming both pilot files.
5. **Images** stay unchanged copies (no resizing).
6. **Spec rows** for the 12 ENCORE counts and the 2 illustration firm counts: accepted. (The 2 firm counts were in section 9 and went with it, decision 10.)
7. **Licence links** in the footer stay (links only, nothing loaded).
8. **No loss-patch images.**
9. **Page reviewed** by Yaseen: content OK, no other wording notes.
10. **Section 9 "Hours and the full-build estimate" removed**, with its numbers, tags, captions and appendix rows (its rows are removed from `docs/number_sources.csv`, its caveats from `docs/caveats.csv`). R058 is removed from the pending decisions. The list "What would need to change for a full build" is shown in the Next decisions section, without the hours item. Section 10 became section 9.
11. **"Claude Code" appears once on the page**, in the Gaps and findings section: "All checks were done by the AI coding assistant (Claude Code) that built the pipeline; the planned manual reviews were waived, so no value was checked independently." Elsewhere, neutral wording ("automated check", "self-check", "checked by the pilot's scripts", "the pilot team").

## Step 5 decisions: fix round (Yaseen, 2026-10-25)

1. **153.4 km stays untyped** (it is printed only inside the distance map): accepted. Rule 2 unchanged.
2. **Gap 14 title** "Self-checks" on the page, and the section 6 locator `checked_by!=`: accepted.
3. **Footer line** "built by script from the palm oil pilot's files, with an AI coding assistant": kept. (Since Step 5 close-out decision 4: "from the pilot's files".)
4. **Plain language:** the 24 rewrites of the Step 5 entry are applied, except where a rewrite would change a fact or a number's meaning; such a rewrite is skipped or kept to the pilot's facts, and reported in `PROGRESS.md`.
5. **Readability:**
   - note letters: contrast at least 4.5:1 in both modes;
   - pipeline diagram: text at least 12 px on a 390 px screen (HTML and CSS instead of a drawing);
   - every wide table scrolls sideways inside its own box on phones; the page itself never scrolls sideways;
   - maps: each image links to its full-size file; in dark mode the maps keep a white frame (no recolouring).
6. **Credits added:** the palm map's "clipped to Sarawak" note (as on the pilot's own map), the EU sanctions list's licence, and Global Forest Watch.
7. **Note check:** `scripts/check_numbers.py` fails on a note in a block where no number needs it. A note that belongs to an image, a feature card or a missing value is declared on that element (`data-needs`), and only there. Planted-error tests for it are in `scripts/test_check_numbers.py`.
8. **Planning files:** `CLAUDE.md`, `PROGRESS.md` and `docs/` state only the general rule: project-internal content is never published. `build/private_terms.txt` stays local.
9. **`README.md`** for the repository: what the page is, how to rebuild it and run the checks, the licences. No numbers typed in it.
10. **PI's permission received (2026-10-25):** publishing on public GitHub and Vercel is approved, recorded in `PROGRESS.md`. This meets rule 14 for Step 6. Push and deploy still happen only in Step 6, after Yaseen's go (rule 11).
11. **Project name:** may appear in folder names, paths and the repository. No change to the files that hold the folder name. (On the page: Step 5 close-out decision 4.)

## Step 5 close-out decisions (Yaseen, 2026-10-26)

Step 5 with its fix round approved by Yaseen (Yaseen's hours for the fix round: 1 h).

1. **EU licence:** the credit quotes only the part that applies to the file used (CSV 1.1): "European Commission reuse notice (Decision 2011/833/EU)", a quote from the licence cell of the pilot's `source_register.csv`, tagged (CC BY 4.0 is listed for CSV 1.0).
2. **Section 3:** the "2 open" count is dropped; the log line shows the questions and the decided ones only.
3. **Link and path check:** `scripts/check_links.py`, in the README's check list.
4. **Project name on the page:** the page title is "NRFR palm oil pilot"; the name is used once in the intro; elsewhere the page says "the pilot". (Updates public-release decision 4 and Step 5 decision 3.)
5. **Step 6 go:** Yaseen approves the first commit and the push to the public GitHub repository (rule 11; the PI's permission is recorded, rule 14). Remote `origin`: https://github.com/yaseen9133ai/nrfr-pilot-site.git, branch `main`. The Vercel deploy is not part of this go.
6. **Commit e-mail:** the GitHub no-reply address, set with `git config --local` before the first commit, so the personal address the repository had until then is not published in the commit history (public-release decision 3).

## Steps

1 Setup · 2 Outline · 3 Extraction + JSON · 4 HTML · 5 Checks · 6 Share. Details and status: `PROGRESS.md`.

## Traceability on the page

number on page → source tag (file, row key, column) → pilot file → the pilot's own chain (evidence.csv → source page → method card → script → check result)

## Folders

- `site/` the deployable page: `site/index.html` and `site/assets/` (CSS, images copied from the pilot). The only folder Vercel publishes.
- `scripts/` build and check scripts (standard library only)
- `build/` working files only, git-ignored: pilot snapshot, extracted JSON, check output, local copies of pilot data
- `docs/` planning notes (content inventory, page outline, number sources, caveats). Committed, so public
- `README.md` what the page is, how to rebuild it and run the checks, the licences
- `LICENSE.md`, `LICENSES/` licence notice and texts
- `.gitignore` keeps `build/`, local copies of pilot data, raw file types, `.DS_Store`, virtual environments and caches out of git
