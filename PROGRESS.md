# Progress — palm oil pilot site

## Current status

_Replaced (not appended) at the end of every step._

- **Approved:**
  - Step 1 Setup, with the addendum (Yaseen (Research Assistant), 2026-10-25; Yaseen's hours: 1 h).
  - Step 2 Outline (Yaseen, 2026-10-25; Yaseen's hours: 1 h). Decisions: `CLAUDE.md`, "Step 2 decisions".
  - Step 3 Extraction + JSON (Yaseen, 2026-10-25; Yaseen's hours: 1 h). Decisions: `CLAUDE.md`, "Step 3 decisions".
  - Step 4 HTML (Yaseen, 2026-10-25; Yaseen's hours: 1 h). Decisions: `CLAUDE.md`, "Step 4 decisions: close-out".
  - Step 5 Checks, with its fix round (Yaseen, 2026-10-26; Yaseen's hours: 1 h for Step 5, 1 h for the fix round). Decisions: `CLAUDE.md`, "Step 5 decisions: fix round" and "Step 5 close-out decisions".
- **Step 6 Share: done (2026-10-26)** (Yaseen's hours: to fill). Decisions: `CLAUDE.md`, "Step 5 close-out decisions" 5–6 and "Step 6 close-out decisions".
  - First commit `bb7b84e6e50c798075b07348d0758db41d49f219` pushed to `main` at 2026-10-25T16:13:34Z (00:13 MYT on 26 October); second commit `0224831169387d3189af547d621a8e32277fcfbf` (this log).
  - **Live page: https://nrfr-pilot.vercel.app/** (Vercel, set up by Yaseen; root directory `site/`; deploys on every push to `main`). Checked on 2026-10-26: deployed from `0224831` (`main` at the time; its `site/` is the same as in `bb7b84e`). All 11 live files equal `site/` by SHA-256; `check_numbers.py` and `check_links.py` pass on the downloaded copy.
  - The close-out commit (EU licence in the sources table, live URL, this record) redeploys the page; the check after that redeploy is in the entry "Step 6 close-out" below.
- **PI's permission: received 2026-10-25** (rule 14).
- **Repository:** public on GitHub, remote `origin` https://github.com/yaseen9133ai/nrfr-pilot-site.git, branch `main`. Commits use Yaseen's GitHub no-reply address (Step 5 close-out decision 6). Every push to `main` also redeploys the live page.
- **Project name:** page title "NRFR palm oil pilot", the name once in the intro, "the pilot" elsewhere on the page (Step 5 close-out decision 4); folder names, paths and the repository may hold it (Step 5 decision 11).
- **Next:** none planned; all 6 steps are done. Any later change follows the same rules, and a push publishes it (rule 11).
- **Open items (Yaseen):** the open questions at the end of the entry "Step 6 close-out".
- **Paths:**
  - Pilot (read-only): `../nrfr-pilot`. Not a git repository. Every script reads it from `PILOT_DIR` (default `../nrfr-pilot`).
  - Site: `.` (this folder). Git repository, branch `main`, remote `origin`. Live: https://nrfr-pilot.vercel.app/.
  - Deployable page: `site/` (`site/index.html` + `site/assets/`). `build/` is for working files and is git-ignored.
- **Publication (decided by Yaseen, 2026-10-25):** public GitHub repository, with `site/` deployed on Vercel, at Step 6.
- **Pilot snapshot:**
  - Baseline 2026-10-25T10:25:57Z (`build/pilot_snapshot.csv`): 1,054 files. 213 in site scope (79,207,136 bytes, SHA-256, unchanged from the first baseline) and 841 other (2,605,108,622 bytes, size + mtime). 8 `.DS_Store` files ignored.
  - It replaces the first baseline (09:59:51Z, 1,084 files), with Yaseen's approval, after Yaseen deleted the pilot's `untitled folder/` (30 duplicate files). The old baseline is kept in `build/superseded/`.
  - Last check: see the entry "Step 6 close-out" (no change).
- **Pilot state at the snapshot:** steps 1–9 approved; step 10 (findings report) waiting for Yaseen's decision (R057), shown on the page as "decision pending". R058 (unconfirmed hours) is open in the pilot; it is not shown on the page (Step 4 decision 10).
- **Hours:** Claude Code about 3.2 h (Step 1 0.2 h + addendum 0.1 h + Step 1 close-out and Step 2 0.4 h + Step 2 close-out and Step 3 0.5 h + Step 3 close-out and Step 4 0.5 h + Step 4 close-out and Step 5 0.4 h + Step 5 fix round 0.6 h + Step 5 close-out and Step 6 0.3 h + Step 6 close-out 0.2 h; estimates from the system clock) · Yaseen 1 h (Step 1) + 1 h (Step 2) + 1 h (Step 3) + 1 h (Step 4) + 1 h (Step 5) + 1 h (fix round) + Step 6 (to fill).

## Steps

| # | Step | Status |
| --- | --- | --- |
| 1 | Setup: folders, rules, pilot snapshot, content inventory | Approved 2026-10-25 |
| 2 | Outline: page sections, what each shows, from which file; answers to the open questions | Approved 2026-10-25 |
| 3 | Extraction + JSON: scripts read the pilot and write the page data (with source tags) to `build/` | Approved 2026-10-25 |
| 4 | HTML: `site/index.html` + `site/assets/`, built from the JSON | Approved 2026-10-25 |
| 5 | Checks: every tagged number against its source; no untagged numbers; offline; exclusions; attributions | Approved 2026-10-26 (with its fix round) |
| 6 | Share: git remote, push to the public GitHub repository, Vercel deploy of `site/` (each only with Yaseen's approval; the PI's permission was recorded on 2026-10-25) | Done 2026-10-26: public repository; live at https://nrfr-pilot.vercel.app/ |

---

## Template

### Step N — <name>

- **Date:**
- **What was done:**
- **Files produced:**
- **Checks:**
- **Pass/fail:**
- **Hours:** Claude Code (active time): · Yaseen: to fill
- **Issues:**
- **Open questions:**

---

### Step 1 — Setup

- **Date:** 2026-10-25
- **What was done:**
  - Read the pilot's `progress_log.md` (Current status), `reports/step10_findings.md`, `review_queue.csv`, `source_register.csv`, `docs/PILOT_PLAN.md` and `data/processed/README_dataset.md`, and listed `reports/`, `data/` and `scripts/`. Read only.
  - Found the pilot at `../nrfr-pilot`. Created this folder beside it, with `scripts/`, `assets/`, `build/` and `docs/`. Ran `git init` (branch `main`, no remote, nothing committed).
  - Wrote `CLAUDE.md` with the site rules (pilot read-only, no hand-typed numbers, source tags, no new data, plain language, exclusions, attributions, offline static site with standard-library Python, one step at a time, snapshot check at the start and end of every step).
  - Wrote `scripts/pilot_snapshot.py` (standard library only, read-only on the pilot):
    - **Site scope** (files the site might use): the 5 tracking files and the pilot `CLAUDE.md`, `docs/PILOT_PLAN.md`, `docs/methods/*.md`, `data/raw_files.csv`, `data/processed/*`, `data/interim/*.csv` and `*.geojson` (top level only), `reports/**`, and `scripts/*.py|sh|txt`. Path, size, mtime and SHA-256.
    - **Other scope** (everything else, e.g. `data/raw/`, rasters, `untitled folder/`, `__pycache__/`): path, size and mtime, so a write anywhere in the pilot is caught.
    - `.DS_Store` is ignored (Finder writes it when a folder is viewed).
    - Git: records whether the pilot is a repository and, if so, the commit and `git status`. Uses `--no-optional-locks`, so git does not write to the index.
    - `--check` reports changed, missing and new files and any git change, appends a line to `build/pilot_snapshot_checks.log`, and exits 0 (no change), 1 (change) or 2 (error). Taking a new baseline over an existing one needs `--force`.
    - The script refuses to write inside the pilot.
  - Wrote `docs/content_inventory.md`:
    - one table per planned section (10), giving candidate files, what they contribute and whether they hold numbers;
    - a) the 32 PNG images in `reports/`, with personal-data and licence notes and a proposal for each;
    - b) attributions per source, and how to treat the sources with no stated licence;
    - c) files to exclude;
    - d) 15 open questions.
- **Files produced:**
  - `CLAUDE.md`
  - `PROGRESS.md`
  - `scripts/pilot_snapshot.py`
  - `build/pilot_snapshot.csv` (1,084 rows), `build/pilot_snapshot_info.json`, `build/pilot_snapshot_checks.log`
  - `docs/content_inventory.md`
  - Empty folder: `assets/` (removed in the addendum; replaced by `site/assets/`)
- **Checks:**
  - Snapshot taken at 2026-10-25T09:59:51Z. `--check` at 09:59:57Z: **no change** (exit 0).
  - Re-running without `--force` was refused, as intended (the baseline was not overwritten).
  - Self-test of `--check` on a small fake pilot folder in Claude Code's scratchpad (not saved in the site), 9 cases: no change → 0; site file edited with the same size → change; content restored → no change, with an mtime note; raw file touched → change; new file → change; deleted file → change; `.DS_Store` changed → ignored; second baseline without `--force` → refused. **9/9 pass.**
  - End of step, `--check` at 2026-10-25T10:05:16Z and again after writing this file at 10:05:58Z: **no change** (1,084 files, exit 0 both times).
  - Nothing written in the pilot: it is not a git repository (`git rev-parse`: "not a git repository"), so this was checked with the snapshot (every file's size and mtime, plus SHA-256 for site scope) and with `find -newermt "2026-10-25 17:50"` (no file or folder modified since the session started, `.DS_Store` excluded).
  - Personal-data search (read-only): the eMSPO contact fields occur only in `data/raw/MSPO/emspo_entity_*.json`. No e-mail address was found in any pilot file outside `data/raw/`.
  - `untitled folder/` in the pilot: all 30 files are byte-identical (SHA-256) to files elsewhere in the pilot.
  - Inventory counts were re-counted from the files: 32 top-level interim CSVs, 32 PNGs, 34 `.py` scripts, `data/raw/` 784 files and 2.41 GB.
  - Site `git status`: 6 untracked files (CLAUDE.md, the 3 build files, the inventory and the script). `PROGRESS.md` is added after that status.
- **Pass/fail:** Pass.
- **Hours:** Claude Code about 0.2 h (active time; estimate from the system clock, about 17:54–18:06 MYT. The start time is inferred: the first clock reading, 17:58, was taken after about 4 minutes of reading) · Yaseen: 1 h for Step 1 with the addendum (given at approval, 2026-10-25).
- **Issues:**
  - The pilot is not under git, so "nothing written" rests on the snapshot (size and mtime for files outside site scope, not hashes). A write that keeps both size and mtime the same would not be seen outside site scope.
  - `.DS_Store` files are ignored, so Finder activity does not trigger a stop. The pilot root's `.DS_Store` was modified at 17:52 MYT, before this session.
  - If Yaseen fills in the step 10 hours or decides R057 in the pilot, the next `--check` will report a change. The steps then stop until Yaseen approves a new baseline (`--force`).
  - Hours exist only in markdown in the pilot. The two files give different totals because they were written at different times: report §6, 13.7 h + Yaseen's step 10 time; Current status, 13.8 h, after the dataset README. See open question 2.
  - Some images lack on-image credits (the step 9 maps have no OSM/ODbL or geoBoundaries credit), so captions must carry them. Exact Hansen citation and Copernicus wording are not recorded in the pilot.
  - Not opened in Step 1: 21 of the 32 PNGs (17 of the 18 GFW screenshots, `step6_loss_patches_imagery.png`, `loss_patches_imagery_firm3.png`, `step9_loss_2022.png` and `step9_loss_2023.png`; their notes in the inventory come from the script that made them), and a non-output file in the pilot's `docs/`.
- **Open questions:** `docs/content_inventory.md`, section d (15 questions: audience, hours, markdown numbers, counted numbers, tag format, number format, images, attribution wording, the page's own notice, ENCORE, downloads, links, `untitled folder/`, mill table, a non-output file).

#### Step 1 addendum — public repository and `site/`

- **Date:** 2026-10-25
- **What was done:**
  - Yaseen decided that the repository will be public on GitHub and that the page will be deployed on Vercel later.
  - **`CLAUDE.md`:**
    - publication note;
    - rule 8 now puts the page in `site/` (`site/index.html` + `site/assets/`, the only folder Vercel publishes);
    - new rule 11: no git remote and no push until Yaseen approves at Step 6;
    - new rule 12: everything committed must be safe to publish (no personal data, raw downloads, annual-report PDFs or page extracts, or copies of pilot CSVs beyond what the page needs). It applies to every tracked file;
    - new rule 13: `build/` is for working files only and is git-ignored; local copies of pilot data go only there;
    - the Folders list was updated.
  - **Folders:** created `site/` and `site/assets/`. Removed the empty top-level `assets/` from Step 1, so nothing points to the old location.
  - **`.gitignore`** keeps out:
    - `build/`;
    - local copies of pilot data (`nrfr-pilot/`, `data/`, `local/`);
    - raw file types (`*.pdf`, `*.tif`, `*.tiff`, `*.nc`, `*.gpkg`, `*.pbf`, `*.xlsx`, `*.xls`, `*.zip`);
    - `.DS_Store`, virtual environments and caches;
    - `.vercel/` and `.env*`. These two were not in the request; they were added because Vercel is planned and the repository will be public.
  - **`docs/content_inventory.md`:**
    - images now go to `site/assets/`;
    - questions 11 and 12 were updated for a public page (the pilot is not published, so its paths are shown as text);
    - new question 16;
    - new **section e, Public release check**, in six parts: e1 personal data; e2 sources with no stated licence (eMSPO, RSPO, UML, annual reports); e3 share-alike and other licence terms (ENCORE CC BY-SA, ODbL, repository licence); e4 project-internal content; e5 statements about named companies; e6 repository safeguards. Each item has a proposed treatment, and 9 are marked "Yaseen decides".
  - **Read-only searches in the pilot for section e:** personal titles in the candidate files (none found); project-internal content (not quoted, because this repository will be public; the terms to scan for are kept only in the local `build/private_terms.txt`); and Yaseen's name.
- **Files produced or changed:** `CLAUDE.md` (changed), `.gitignore` (new), `site/` and `site/assets/` (new, empty), `docs/content_inventory.md` (changed), `PROGRESS.md` (this entry). `assets/` was removed (it was empty).
- **Checks:**
  - Pilot snapshot `--check` at the start (2026-10-25T10:08:51Z) and at the end (10:11:50Z): **no change** (1,084 files, exit 0). `find -newermt "2026-10-25 17:50"` in the pilot: nothing modified (`.DS_Store` excluded).
  - `git check-ignore` on 17 test paths:
    - **ignored**, as intended: `build/…`, `data/…`, `local/…`, `nrfr-pilot/…`, a PDF and a TIFF in `site/assets/`, `*.gpkg`, `.DS_Store` (root and `site/`), `.venv/`, `__pycache__/`, `.vercel/`, `.env.local`;
    - **not ignored**, as intended: `site/index.html`, `site/assets/map.png`, `scripts/build.py`, `docs/outline.md`.
  - Site `git status` (before this entry): branch `main`, no commits. Untracked: `.gitignore`, `CLAUDE.md`, `PROGRESS.md`, `docs/content_inventory.md`, `scripts/pilot_snapshot.py`. Ignored: the 3 files in `build/`. `git remote`: none.
- **Pass/fail:** Pass.
- **Hours:** Claude Code about 0.1 h (active time; estimate from the system clock, about 18:08–18:14 MYT) · Yaseen: included in the 1 h for Step 1.
- **Issues:**
  - `site/` and `site/assets/` are empty, and git does not track empty folders, so they will not show in `git status` until files are added. No placeholder file was added.
  - The committed planning files contained absolute paths with the local user name, and named Yaseen throughout. Resolved in the Step 1 close-out (relative paths; "Yaseen (Research Assistant)").
  - `build/` is git-ignored, so the pilot snapshot and any extracted JSON are not in the repository. The Step 5 checks can be run only where the pilot is present.
- **Open questions:** `docs/content_inventory.md`, section d, question 16 (public-release decisions), in addition to questions 1–15.

#### Step 1 close-out — approval, snapshot replacement and public-release decisions

- **Date:** 2026-10-25
- **Approval:** Yaseen approved Step 1 with the addendum. Yaseen's hours for Step 1: 1 h.
- **Pilot snapshot replaced (with Yaseen's approval):**
  - **What the check found:** the start-of-session `--check` (2026-10-25T10:22:34Z) reported a **change**: the 30 files of the pilot's `untitled folder/` were missing (missing 30, changed 0, new 0). The pilot root folder was modified at 18:19 MYT, after the previous session ended (18:14). Claude Code stopped and reported. Yaseen confirmed deleting the folder on purpose.
  - **Read-only check before the new baseline, as Yaseen asked:** no reference to the 30 files in the pilot's tracking files.
    - `grep -i "untitled"` in `CLAUDE.md`, `data/raw_files.csv`, `source_register.csv`, `evidence.csv`, `progress_log.md`, `review_queue.csv`, `feature_dictionary.csv`, `docs/` (plan and method cards), `scripts/`, `data/processed/` and `reports/`: **no match**.
    - A wider search of every text file in the pilot outside `data/raw/`: **no match**.
    - All 30 deleted files have a same-name, same-size original that is still present (for example `docs/PILOT_PLAN.md`, `scripts/step8_run_all.sh`, `reports/step9_maps/step9_loss_2021.png`). The originals in site scope have unchanged SHA-256.
  - **New baseline** `--force` at 2026-10-25T10:25:57Z: 1,054 files. 213 site scope, same count and bytes as before (79,207,136); 841 other (2,605,108,622 bytes). The old baseline was copied first to `build/superseded/pilot_snapshot_2026-10-25T095951Z.csv` and `pilot_snapshot_info_2026-10-25T095951Z.json`.
  - `--check` right after: **no change** (exit 0).
- **Public-release decisions recorded** (Yaseen, 2026-10-25), in `CLAUDE.md` (new section "Public-release decisions" and new rule 14) and in `docs/content_inventory.md` (top of section d; each item in section e marked **Decided**):
  1. **Name:** "Yaseen (Research Assistant)" on the page and in repository files; no full name, no student ID. The planning files use "Yaseen" for short after the first mention.
  2. **Relative paths** instead of absolute ones in `CLAUDE.md`, `PROGRESS.md` and `docs/` (`../nrfr-pilot` for the pilot, `.` for this folder). Done.
  3. **Git identity, repository-local:** `git config --local user.email` set to the address Yaseen gave. The address is not repeated in tracked files, so the planned e-mail scan stays clean. `user.name` was **not** set: the value given looked garbled. Open item.
  4. **Purpose:** neutral (proof that the data chain can be built and traced). Project-internal content is never published (worded as a general rule since the Step 5 fix round).
     - `CLAUDE.md` states this only as a general rule.
     - "Palm oil pilot" instead of the project's name until Yaseen confirms the PI's permission (open item).
     - Prose mentions of the name were removed from `CLAUDE.md`, `PROGRESS.md` and `docs/`, including a file name that contains it. The folder names `nrfr-pilot` and `nrfr-pilot-site` still contain it, and so do the relative paths, `scripts/pilot_snapshot.py` and `.gitignore` (open item; outline open question 8).
  5. **Forest-loss caveat** next to every forest-loss number (wording in `CLAUDE.md`; the grid version says "in Sarawak").
  6. **UML points** shown with credit and "no licence stated". **ENCORE content:** "CC BY-SA 4.0" next to it.
  7. **Licences** written:
     - `LICENSE.md`: which licence covers which part; links to the CC BY 4.0 and CC BY-SA 4.0 legal codes; the ENCORE citation; a third-party note; what is not yet decided;
     - `LICENSES/MIT.txt`: MIT for `scripts/`, "Copyright (c) 2026 Yaseen (Research Assistant)".

     The full CC legal-code texts were not copied: the licences allow a link to them.
  8. **Named companies:** factual, sourced, neutral wording; no judgements, no rankings.
  - New `CLAUDE.md` rule 14: **no push until the PI's permission is recorded in `PROGRESS.md`.**
- **Files changed or added:** `CLAUDE.md`, `PROGRESS.md`, `docs/content_inventory.md` (changed); `LICENSE.md`, `LICENSES/MIT.txt` (new); `.git/config` (local `user.email`; not a tracked file). Nothing committed.
- **Checks:** `grep` in `CLAUDE.md`, `PROGRESS.md`, `docs/`: no absolute path (`/Users/`) and no project name in prose (see the Step 2 checks for the final run).
- **Hours:** included in the Step 2 figure below.

---

### Step 2 — Outline

- **Date:** 2026-10-25
- **What was done:**
  - Read (read-only) the pilot's findings report (all sections), dataset README, Current status, plan, feature dictionary, source register, download log, evidence file, final tables, mill tables, certification and debt-to-equity tables, grid report and method card, grid check CSV and road tag counts, and the step 3 report.
  - Wrote **`docs/page_outline.md`**:
    - the page frame (title, byline, status line, at-a-glance, contents, footer with credits and licences);
    - writing rules (plain words, the pilot's own terms, neutral about the firms, missing stays missing);
    - the **10 sections** in the requested order. Each has a one-sentence message, the content in plain words, the images (paths in the pilot's `reports/`, with caption credits), the caveats to show, and the pilot paths as plain text;
    - the **pipeline diagram plan**: boxes and arrows from the raw sources to `pilot_firm_year.csv`, `pilot_static.csv`, the grid and `evidence.csv`; solid, dashed and dotted lines; step labels; evidence links; text version;
    - a **glossary** of 28 terms;
    - the data Step 3 will need, and the syntax of `docs/number_sources.csv`;
    - **20 open questions**, including what could not be sourced.
  - Wrote **`docs/number_sources.csv`**: 291 rows, one per number planned for the page, with columns `section`, `label`, `source_file`, `row_key`, `column_or_computation`, `expected_value`, `note`.
    - By section: header and credits 11, what we did 17, sources 14, raw to final 28, features 26, grid 30, evidence 25, results 66, gaps 28, hours 44, next decisions 2.
    - By source: 144 rows from CSV files, 147 from markdown (127 from the findings report).
    - 53 rows are counts, sums, minimums or maximums of existing columns. Each is used only where the pilot states the same figure (named in the note) or for a plain count of listed rows.
    - 129 rows quote the exact sentence or cell text that holds the number.
  - **Nothing new was computed.** No shares, averages or totals across firms. Firms are listed in the pilot's order.
  - The CSV was generated from a row list in Claude Code's scratchpad (`make_number_sources.py`, not saved in the site), so the quoting is exact.
- **Files produced:** `docs/page_outline.md` (new), `docs/number_sources.csv` (new). With the Step 1 close-out: `CLAUDE.md`, `PROGRESS.md` and `docs/content_inventory.md` changed; `LICENSE.md` and `LICENSES/MIT.txt` new. No HTML, no extraction script.
- **Checks:**
  - **Pilot snapshot:**
    - start of session: change found (the deleted folder; see the close-out entry);
    - after the new baseline (10:25:57Z): no change;
    - mid-step (10:43:55Z): **no change** (1,054 files, exit 0);
    - end of step: see the final line of this entry.
  - **`find -newermt "2026-10-25 18:25"`** in the pilot (`.DS_Store` excluded): nothing modified.
  - **Number list vs pilot:** a read-only checker in Claude Code's scratchpad (`verify_number_sources.py`, not saved in the site) looked up every row by its file, row key and column, or recomputed its count or sum, or found its exact quote (in the named markdown section or table row, or in the named CSV cell). **291 of 291 found as expected.**
  - **Negative test of that checker:** 9 planted errors, one per kind of lookup:
    - CSV cell; CSV count with a filter; CSV sum;
    - markdown table count with a filter; markdown table cell;
    - text in a CSV cell; markdown quote; numbered items;
    - a quote placed in the wrong table row.

    **9 of 9 caught**, exit 1.
  - **Repository text:** `grep` for `/Users/` and for the project name in capitals in `CLAUDE.md`, `PROGRESS.md`, `docs/`, `LICENSE.md`, `LICENSES/`: none (lower-case folder names remain, as recorded).
  - **Site `git status`:** untracked `.gitignore`, `CLAUDE.md`, `LICENSE.md`, `LICENSES/`, `PROGRESS.md`, `docs/`, `scripts/`. No commits, no remote.
- **Pass/fail:** Pass.
- **Hours:** Claude Code about 0.4 h for the Step 1 close-out and Step 2 together (active time; estimate from the system clock, about 18:22–18:47 MYT, including the stop for the snapshot change) · Yaseen: 1 h (given at approval, 2026-10-25).
- **Issues:**
  - **Weak quote matching in the checker:** for quoted text, it tests only that the expected value appears somewhere inside the quote. A one-digit value could match another digit in the same quote. Step 3/5 should match whole numbers, not substrings.
  - **Markdown sources:** 147 planned numbers live only in markdown (open question 3). If markdown is not allowed, sections 8 and 9 lose most of their numbers.
  - **Script count:** the findings report counts 33 Python scripts; the folder now holds 34 (open question 7).
  - **Hours totals:** two in the pilot (13.7 h + Yaseen's step 10 time in the report; 13.8 h in Current status). The plan uses the report's (open question 2).
  - **Numbers printed on images** (map legends, km² labels) cannot be tagged (open question 5).
  - **The first `AskUserQuestion` in this session was declined.** The snapshot decision then came in Yaseen's message; the git `user.name` question is still open.
  - **Garbled git name:** the brief's git `user.name` looked garbled, so it was not set (only `user.email`).
- **Open questions:** `docs/page_outline.md`, "Open questions" (20).
- **End of step:** pilot snapshot `--check` at 2026-10-25T10:45:22Z: **no change** (1,054 files, exit 0). Re-run after writing this line: see `build/pilot_snapshot_checks.log`.

#### Step 2 close-out — approval and decisions

- **Date:** 2026-10-25
- **Approval:** Yaseen approved Step 2. Yaseen's hours for Step 2: 1 h.
- **Decisions recorded** in `CLAUDE.md` (new section "Step 2 decisions"; public-release decision 3 updated; pilot path setting added near the top):
  1. `git config --local user.name "Yaseen"`: done. `user.email` unchanged (not repeated here).
  2. Folders keep their names. Every script takes the pilot path from `PILOT_DIR` (default `../nrfr-pilot`). A neutral GitHub repository name is a Step 6 decision. `scripts/pilot_snapshot.py` now reads `PILOT_DIR` (`--pilot` still overrides it); a check from another folder with a relative `PILOT_DIR` gave the same result.
  3. Markdown sources allowed, from a fixed locator only; prefer the CSV when the same number exists there; a missing or ambiguous locator is an error.
  4. No tag needed for review IDs, step and section numbers, years used as labels, dates, versions, file names, ISIC codes and licence versions.
  5. Number format: source decimals and signs kept, thousands separators, unit next to the number, no extra rounding.
  6. Tag format: accepted if it carries file, locator, column and raw value.
  7. Hours: headline 13.5 h for steps 1–9; step 10 (0.2 h) and the dataset README (0.1 h) as small additions; scripts as "33 at the time of the findings report".
- **Outline questions answered by these decisions:** 1 (git name), 2 (hours), 3 (markdown), 5 (digits without a tag), 6 (number format; the grid totals keep their 4 decimals), 7 (script count), 8 (folder names), 19 (tag format). Still open: 4 (counted numbers; Step 3 applied the outline's proposal), 9, 10–18, 20.

---

### Step 3 — Extraction + JSON

- **Date:** 2026-10-25
- **What was done:**
  - **Spec revised: `docs/number_sources.csv`** (291 → 302 rows). It is now the spec that `scripts/extract.py` reads. The Step 2 version is kept in `build/step3/number_sources_step2.csv` (git-ignored). The rewrite was made by a one-off script in Claude Code's scratchpad (`transform_spec.py`, not saved in the site), then 5 cells were corrected (unit `h` on 4 range rows; one caveat).
    - **New columns:** `id` (for example `s7.forest_loss_ha_sop_2021`), `format` (`number` 251 rows, `as_is` 51 rows: dates, versions, ranges, phrases, the word "five"), `unit`, `caveats`, `tag_required` (`yes` 280; `no: date` 13, `no: year label` 5, `no: version` 4; decision 4).
    - **Markdown locators tightened (decision 3):** every markdown row now names its heading and one block (`row=`, `bullet=`, `paragraph=`, `paragraph 1`, `heading`, `table`, `numbered list`); a quote in a table row names its column. Example: `header line (line 3)` became `# Step 10: Findings report | paragraph 1`.
    - **Moved to a CSV cell (decision 3, "prefer the CSV"):** 25 rows whose number also sits in a CSV cell (as the value or inside a text cell), for example the grid's 125,982 cells (`grid_vs_sarawak_loss.csv`, `grid_cells`), 4,111 edge cells and 123,769.32 km² (`feature_dictionary.csv` notes), 80.0% palm coverage and 22 tiles (`source_register.csv` notes), Ta Ann's 29.41% / 30.39% of SPB (`data/interim/firm2_mills.csv`). Interpretation used: a count or sum that the pilot states only in markdown stays markdown (the number does not exist in a CSV cell).
    - **Phrases split** where each number sits in a CSV cell: 8 phrases became 19 rows (for example "14.68 vs 14.50", "61% / 63% / 52%", "0.3443 / 0.2202 / 0.2301", "63/63 and 45/45").
    - **Hours (decision 7):** the row "13.7 + Yaseen's step 10 time" was removed; a row for the dataset README (Claude Code 0.1 h, `progress_log.md`, "Dataset README", bullet "Claude Code:") was added; the script row is labelled "at the time of the findings report".
    - **Labels:** the grid differences, loss pixels and GFW threshold rows now say "forest loss", so the caveat rule can see them.
    - Now: 187 rows from CSV, 115 from markdown (was 147); 53 counts, sums, minimums or maximums; 136 quotes.
  - **New `docs/caveats.csv`:** 20 caveats (id, wording, basis, where it applies). The two forest-loss caveats use the wording of public-release decision 5 (only the first letter capitalised). Caveat texts hold no numbers except years used as labels, step and section numbers, review IDs and the licence version. 147 numbers carry at least one caveat.
  - **`scripts/extract.py`:** reads the spec and the pilot (read-only, `PILOT_DIR`) and writes `build/site_data.json`:
    - `numbers`: one entry per spec row: `id`, `section`, `label`, `raw`, `display`, `format`, `unit` (+ `unit_source` where the unit is read from a cell: 14 FFB yield units from `evidence.csv`, the production unit from `firm2_ar_values.csv`), `source` (file, locator, column), `tag_required`, `no_tag_reason`, `caveats`.
    - `lists`: firms (3), sources with licence and download date (34), attribution wording the pilot records word for word (7) plus 2 "not recorded" notes, feature verdicts (8, with family, main reason and review IDs), gaps (16, with review IDs), pending decisions (R057, R058: both pending), decision options (3), full-build changes (14). Every text field carries its tag (file, locator, column, value).
    - `caveats`, `inputs` (SHA-256 of the 25 pilot files read), `spec_sha256`, `counts`. No timestamps and no absolute paths.
    - A quote must occur once in its cell or block, and the value once in the quote as a whole token (the Step 2 checker's weakness). Any error: nothing is written and an old `site_data.json` is removed.
  - **`scripts/check_numbers.py`:** independent check. It does not import `extract.py`; it has its own CSV reader (`csv.reader` rows), condition parser, markdown parser (regular expressions over whole sections), whole-token count and number formatting. It compares every spec row with the source and with `site_data.json`, applies the decision rules (forest-loss caveat, Sarawak wording in section 5, ENCORE licence, UML caveat, no-tag reasons), re-reads every list field from its tag, checks each list is complete and in source order, and checks the file hashes.
  - **`scripts/test_check_numbers.py`:** planted-error test (copies of the 25 pilot input files in `build/planted_test/`, deleted at the end).
  - **`scripts/scan_exclusions.py`** + **`build/private_terms.txt`** (git-ignored, 18 terms; its header names where the terms come from, without repeating them here).
- **Files produced or changed:**
  - New: `scripts/extract.py`, `scripts/check_numbers.py`, `scripts/test_check_numbers.py`, `scripts/scan_exclusions.py`, `docs/caveats.csv`.
  - Changed: `docs/number_sources.csv`, `scripts/pilot_snapshot.py` (`PILOT_DIR`), `CLAUDE.md`, `docs/page_outline.md` (a note on the new spec syntax), `PROGRESS.md`.
  - Working files (git-ignored): `build/site_data.json`, `build/check_numbers_report.txt`, `build/test_check_numbers.txt`, `build/private_terms.txt`, `build/step3/` (Step 2 spec copy; first-run JSON copy).
  - `.git/config`: `user.name`. No HTML, no images, nothing committed.
- **Checks:**
  - **Pilot snapshot:** start 2026-10-25T10:49:50Z **no change**; mid-step 11:04:01Z no change (also from `/tmp` with a relative `PILOT_DIR`); end 11:16:28Z **no change** (1,054 files, exit 0). `find -newermt "2026-10-25 18:49"` in the pilot (`.DS_Store` excluded): nothing modified. No `__pycache__` written anywhere.
  - **Extraction:** 302 of 302 numbers found, each equal to the spec's expected value; 8 lists built. Run twice (the second from `/tmp` with an absolute `PILOT_DIR`): both `bea2ddf77ce1206131a1fd896e3a9328c51026100e1cf971e0d2c8020af53cfb`, files byte-identical (`cmp`).
  - **`check_numbers.py`:** **pass**, 0 failures: 302 numbers, 51 rule checks, 197 list fields, 94 list-structure checks, 27 hashes (25 pilot files + 2 spec files).
  - **Planted errors (`test_check_numbers.py`):** baseline on unchanged copies: pass. **34 of 34 caught**, each by a failure line naming the planted entry:
    - in a pilot file (15): CSV cell; CSV count with a filter; CSV sum; text in a CSV cell; unit read from a cell; markdown table cell; markdown quote in a table row; markdown table count with a filter; numbered items; markdown list-item quote; a number in a quote changed; heading renamed (missing locator); table row duplicated (ambiguous locator); list text in a markdown table; R057 decided in the review queue;
    - in the spec (7): quote placed in the wrong table row; wrong expected value; whole-token rule (value only inside a longer integer, "10" in "104"; value only inside a decimal, "15" in "0.15"); forest-loss caveat removed; ENCORE licence caveat removed; a no-tag reason outside decision 4;
    - in `site_data.json` (12): raw value; display rounded; display with an added "+"; display without separators; unit; tag pointing to another row; tag removed; caveat removed; entry deleted; extra number not in the spec; list value; caveat wording.
  - **Exclusion scan** (`scan_exclusions.py build/site_data.json`): **clean**: e-mail 0, absolute paths 0, phone numbers 0, personal titles 0, possible full name or git e-mail 0, eMSPO contact field names and values 0 (compared with 38 contact texts and 9 phone numbers read from the 27 raw eMSPO files; values not shown), private terms 0 (18 terms in the local list, project name included). `docs/number_sources.csv` and `docs/caveats.csv`: also clean.
  - **Scan self-test** on a fake file in Claude Code's scratchpad (made-up e-mail, path, phone numbers, title, name, a contact field name and 4 private terms; no real personal data): all 7 categories found, exit 1. The file was deleted.
- **Pass/fail:** Pass.
- **Hours:** Claude Code about 0.5 h for the Step 2 close-out and Step 3 (active time; estimate from the system clock, about 18:49–19:20 MYT) · Yaseen: to fill.
- **Issues:**
  - **Found by the checker on its first run, then fixed in `extract.py`:** the attribution tags named the column without the quote (`text in licence` instead of `text in licence: "<quote>"`), and one "not recorded" note contained a digit ("Sentinel-2"; reworded without it).
  - **Whole-token rule refined** after the first extraction: a date followed by a letter (`2026-10-22T20:21:33Z`) is a whole token. Rule now: an end that is a digit must not touch another digit or a `.`/`,` that continues a number; an end that is a letter must not touch a letter or digit.
  - **How a number inside a sentence is "extracted":** the script confirms that the spec's quote occurs once at the locator and the value once inside it; the raw value is that matched text. Cell, count and sum rows are read from the source and then compared with the spec.
  - **`inputs` hashes:** if any of the 25 pilot files changes, `check_numbers.py` fails until `extract.py` is re-run (the snapshot check stops the steps first).
  - **Scan limits:** Yaseen's full name and student ID are not in the pilot files read, so the scan looks for "Yaseen" followed by a capitalised word and for the git e-mail; Yaseen can add the name to `build/private_terms.txt`. The eMSPO value comparison was not tested with a real value (that would copy personal data into a test file); field-name detection was.
  - **`build/private_terms.txt` is local only.** Where it is missing, the scan stops with exit 2.
  - **Tracked planning files (extra scan, not part of the brief):** `docs/page_outline.md` open question 1 quoted a suggested user name that contains the local part of the git e-mail. The question is answered, so the example was removed (the line now records the decision), and a line listing the decided questions was added above the list. A re-scan finds no name or e-mail hit in `CLAUDE.md` or the outline. Remaining hits there are general terms accepted in Step 1 and the folder name `nrfr-pilot` (the general terms were removed in the Step 5 fix round). The Step 5 scan of tracked files will need an explicit list of these accepted mentions.
  - **Step 2 said** the catchment areas in km² for Ta Ann and SPB could not be sourced. `evidence.csv` (`spatial_boundary`) does give the merged area of each firm in km². Not added (no new numbers without approval).
  - Open question 4 (counted numbers) was not answered explicitly; the outline's proposal was applied (counts only where the pilot states the figure, or plain counts of listed rows).
- **Not extractable:** nothing in the spec (302 of 302). Not in the pilot, so not extracted: the full Hansen citation, the Copernicus credit wording (both recorded as "not recorded" in `lists.attributions`), Yaseen's step 10 hours ("to fill"), and numbers printed on the map images.
- **Open questions for Step 4 (HTML):**
  1. **How tags appear in the HTML.** Proposal: each number in a `<span>` with `data-id` plus `data-file`, `data-locator`, `data-column` and `data-raw` (decision 6), and an appendix table "Where each number comes from" (id → pilot file, locator, column). Approve or change.
  2. **Units:** a space before every unit except `%` ("8,856.91 ha", "100.0%")? FFB units exactly as printed, including SOP 2022's "mt/ ha"?
  3. **Signs:** negatives are shown with the minus sign "−" (U+2212); no "+" is added to positive anomalies ("signs kept"). Confirm.
  4. **Dates and versions** need no tag. May the page rewrite them for reading ("22 October 2026" for `2026-10-22`; "1991–2020" for `1991-2020`), or show them exactly as in the source?
  5. **Digits inside names** not on the decision 4 list: "Sentinel-2", "UTM 49N", "EPSG:32649", "Note 19", "HTTP 500", "AR 2022". Avoid them in page text, or add them to the no-tag list?
  6. **Numbers written as words** ("three firms", "six of the eight"): treat as numbers that need a tag (only "five" is in the spec), or keep page text free of number words?
  7. **Pilot text in lists** (gap titles, feature reasons, source licences): show the pilot's wording as tagged small print, with plain-word headings written for the page (no digits), or plain words only?
  8. **Sarawak forest-loss caveat:** decision 5 swaps only the place, so it reads "...in Sarawak...; it is not land cleared by the firm." The outline had "by any one firm". Keep the decision's exact wording?
  9. **Still open from the outline:** 9 and 10 (images; resizing; the Sepakau image), 11 (Hansen and Copernicus wording), 12 (ENCORE: full table of 50 ratings or summary only; the table would need 50 more entries), 13 (downloads), 14 (mill table: names only?), 15 (a non-output file), 16 (review IDs in small print), 17 (licence of planning files and images), 18 (hours per person), 20.
  10. **Catchment areas in km²** for all 3 firms exist in `evidence.csv`: add them, or keep the planned numbers only?
  11. **Hours on the page:** 13.5 h, then "+ 0.2 h (step 10, Claude Code)" and "+ 0.1 h (dataset README, Claude Code)", with no new total. Confirm that no sum is shown.
- **End of step:** pilot snapshot `--check` at 2026-10-25T11:16:28Z: **no change** (1,054 files, exit 0). Re-run after writing this entry: see `build/pilot_snapshot_checks.log`.

#### Step 3 close-out — approval and decisions

- **Date:** 2026-10-25
- **Approval:** Yaseen approved Step 3. Yaseen's hours for Step 3: 1 h.
- **Decisions recorded** in `CLAUDE.md` (new section "Step 3 decisions: page format and content"; public-release decision 5 now points to the new forest-loss wording). They answer the Step 3 open questions 1–6, 8 (in part), 10 and 11, and, from the outline, 11 (credits), 12 (ENCORE), 14 (mill table), 16 (review IDs), 17 (licences) and 18 (hours per person):
  1. Tags in a `<span>` (file, locator, column, raw value); collapsible appendix "Where the numbers come from".
  2. A space before every unit except `%`; FFB units shown as "mt/ha" or "Mt/WHa", the printed form kept in the tag.
  3. The true minus sign everywhere; "+" only on rainfall anomalies.
  4. Dates written for readers; en dash for ranges.
  5. No tag for digits inside names and identifiers (Sentinel-2, UTM 49N, Note 19, HTTP 500, and similar).
  6. Counted numbers as digits with tags, never words.
  7. Forest-loss caveat: "Loss from any cause inside the catchment area, including replanting and logging; not necessarily land cleared by the firm."
  8. Hours: 13.5 h for steps 1–9, then "+ 0.2 h (findings report)" and "+ 0.1 h (dataset guide)", no new total; the Claude Code / Yaseen split, flagged "Claude Code hours mostly unconfirmed (R058)".
  9. ENCORE as a summary (rating counts per activity); mill table with the 12 mills, firm and name only; review IDs small and grey; catchment areas (km²) from `evidence.csv` added to the spec, tagged.
  10. Credits: Hansen et al. (2013) Science, Hansen/UMD/Google/USGS/NASA, CC BY 4.0; "Contains modified Copernicus Sentinel data (2021, 2024)"; "© OpenStreetMap contributors, ODbL" where roads appear; the others as in `site_data.json`.
  11. Planning files and images CC BY 4.0, with the data credits (`LICENSE.md` updated).
- **Changes made for these decisions** (details in the Step 4 entry): `docs/caveats.csv` (forest-loss wording), `docs/number_sources.csv` (302 → 319 rows), `scripts/extract.py` and `scripts/check_numbers.py` (mill list; new no-tag reason "name or identifier"; ENCORE licence rule now also in section 7), `LICENSE.md`. `extract.py` and `check_numbers.py` were re-run: **pass**.

---

### Step 4 — HTML

- **Date:** 2026-10-25
- **What was done:**
  - **Spec and data (Part A, decision 9 and what the page needed):**
    - `docs/number_sources.csv`, 302 → 319 rows:
      - 3 catchment areas (km²) from `evidence.csv`, `spatial_boundary` of each firm's forest-loss row: SOP 26,529.84, Ta Ann 4,782.52, SPB 543.83 (decision 9);
      - 12 ENCORE rating counts: 6 levels × 2 activities, plain counts of rows in `data/interim/encore_dependency_ratings.csv` (decision 9, "rating counts per activity"). Each activity's counts add up to 25; the "no dependency" counts (6 and 12) are the ones `README_dataset.md` states;
      - 2 illustration firm counts (10 and 30) from the findings report table §7.4, so "10 firms" and "30 firms" carry tags (decision 6). **Not in the brief.**
      - 2 edits: unit `%` on the palm-map share (the source prints "80.0%"); the certification day now reads "31 December" (was "31" only).
    - `docs/caveats.csv`: the two forest-loss caveats use the decision 7 wording. The Sarawak variant swaps only the place: "Loss from any cause inside Sarawak, including replanting and logging; not necessarily land cleared by the firm." (open question 2).
    - `scripts/extract.py`: new list `mills` (12 mills from `data/interim/firm{1,2,3}_mills.csv`, rows with `in_scope` = yes; firm and mill name, each tagged); reason "name or identifier" added to the no-tag reasons. `build/site_data.json`: 319 numbers, 9 lists, 26 pilot files read.
  - **`scripts/copy_images.py`** (new): copies 9 images from the pilot's `reports/` into `site/assets/`, unchanged (no resizing), and writes `site/assets/manifest.csv` (asset, pilot path, bytes, SHA-256). Each copy's SHA-256 equals the pilot file's.
  - **Images, looked at before copying** (all 9 opened and viewed in this session; PNG text chunks read too: only "Software: Matplotlib"):
    - copied: `step5_map_palm.png` (section 2), `step8_catchments_map.png` (section 4), `step9_loss_2021.png`, `_2022.png`, `_2023.png`, `step9_distances.png`, `step9_zoom_check.png` (section 5), `step5_R028_sepakau_imagery.png` (section 6), `step5_map_forest.png` (section 7). 4,672,821 bytes;
    - no third-party personal data on any of them. **The Sepakau image** shows the pilot's working note "For Yaseen to pick the point on the mill", the label R028, the mill ID, an eMSPO record ID and the two coordinates. It was copied, because Yaseen's name is public by decision and the Copernicus credit Yaseen gave (2021, 2024) matches its two scenes; Yaseen decides whether it stays (open question 1);
    - not copied: the loss-patch images (their satellite scenes are not covered by the credit wording given), the CBP and GFW screenshots, the step 6 catchment map (as planned in Step 1).
  - **`scripts/build_page.py`** (new): reads only `build/site_data.json`; writes `site/index.html` and `site/assets/style.css`.
    - Every number is a `<span class="n">` with `data-id`, `data-file`, `data-locator`, `data-column`, `data-raw` (and `data-unit-raw` for the FFB and production units, `data-caveats` where caveats apply). No number is typed in the text.
    - Page form (decisions 2–6): display from the JSON; "+" only on positive rainfall anomalies; dates for readers ("24 October 2026"; the download time as "23 October 2026, 07:01:46 UTC"); en dash in year ranges; number words as digits ("five" → 5, "Two of the 8" → "2 of the 8"); unit after a no-break space, none before `%`; FFB units without the space ("mt/ ha" stays in `data-unit-raw`).
    - Digits that need no tag sit in elements marked `data-notag` with the reason (review ID, step number, section number, year label, date, version, file name, licence version, name or identifier).
    - Text quoted from the pilot (firm and mill names, source names and licences, feature verdicts and main reasons, gap titles, decision options, full-build changes, attribution wording, the R057 and R058 items) sits in tagged spans (class `t`). Next to it, the page has plain-word lines written for readers.
    - Caveats: each block of the page (`data-block`) lists the caveats of the numbers in it, directly under the table or paragraph, and each number has a small letter that links to its note. The forest-loss caveat is therefore next to every forest-loss number.
    - Sections in the outline's order, then a glossary, the appendix "Where the numbers come from" (collapsible; all 319 numbers with label, page form, file, locator, column, raw value and printed unit) and the footer (credits and licences). Each section ends with "Details in the pilot:" and the pilot paths as plain text.
    - Pipeline diagram: inline SVG made by the script (360 units wide, readable at phone width): source → clip or extract → result per firm, then the final files and `evidence.csv` with its links to the register, method cards, scripts and checks. Solid = data, dashed = gap, dotted = checks or pictures only. Its counts are tagged `<tspan>` elements. A text version follows it.
    - R057 and R058 are shown as "decision pending" (read from `lists.decisions_pending`).
    - No JavaScript, no external files or fonts, `prefers-color-scheme` light and dark, mobile-first layout. The images carry `width` and `height` attributes (layout only, so in-page links land in the right place; see issues).
  - **`scripts/check_numbers.py`** extended (`--html`, default `site/index.html`; `--no-html` skips it). Its own HTML parser checks every `data-id` element against the spec and the source read again (tag, raw value, page form, printed unit, caveats, and each caveat listed in the same block); every quoted text span against the source; every `data-notag` element (allowed reason and form); every appendix field; every caveat note against `docs/caveats.csv`; any other digit in the page text or in `alt`, `title` or `aria-label` = fail; number words (one to twenty, tens, hundred, thousand, million, dozen, twice) = fail; every spec number must appear on the page.
  - **`scripts/check_offline.py`** (new): nothing loaded from outside `site/` (src, srcset, link, CSS `url()` and `@import`); no script, frame or embed element; every local reference exists; `site/` holds only `index.html` and `assets/`; every asset is used; the manifest matches the images; `width` and `height` equal each PNG's size.
  - **Name on the page:** "Yaseen (Research Assistant)" in all text written for the page. The short form appears only inside quoted pilot text (2 source-register cells) and in tags that name the findings report's heading "Decisions for Yaseen".
  - **`LICENSE.md`** (decision 11): planning files and images CC BY 4.0; a data-credits section; the style sheet under MIT with the scripts; ENCORE-derived parts of other files stay CC BY-SA 4.0.
- **Files produced or changed:**
  - New: `scripts/build_page.py`, `scripts/copy_images.py`, `scripts/check_offline.py`, `site/index.html`, `site/assets/style.css`, `site/assets/manifest.csv`, 9 images in `site/assets/`.
  - Changed: `CLAUDE.md`, `PROGRESS.md`, `LICENSE.md`, `docs/number_sources.csv`, `docs/caveats.csv`, `scripts/extract.py`, `scripts/check_numbers.py`.
  - Working files (git-ignored): `build/site_data.json`, `build/check_numbers_report.txt`, `build/test_check_numbers.txt`. Nothing committed.
- **Checks:**
  - **Pilot snapshot:** start 2026-10-25T11:21:16Z **no change**; end 11:48:11Z **no change** (1,054 files, exit 0). `find -newermt "2026-10-25 19:20"` in the pilot (`.DS_Store` excluded): nothing modified. No `__pycache__` written anywhere (scripts run with `python3 -B`).
  - **Extraction:** 319 of 319 numbers found as expected. SHA-256 of `site_data.json` `4788183b8893914e75bfbd1dd7002f3b4bc5704e3a7e591ef5ffe8bff57b14db`, the same on a second run.
  - **Build twice:** byte-identical. `site/index.html` `991c550e7beb97c5891b2b18a209f4a64a2928c0dc0981c3347978bac09c5315`; `site/assets/style.css` `295804f65f23d87fa8b16d49ee9d8daad9dd03bc74f666a293ac60f99b1349ca`.
  - **`check_numbers.py`:** **pass**, 0 failures: 319 numbers, 63 rule checks, 221 list fields, 107 list-structure checks, 28 hashes; page: 319 of 319 spec numbers shown, 687 number spans, 187 quoted text spans, 274 no-tag elements, 1,610 appendix fields, 254 caveat notes, 3,111 other text runs (0 digits, 0 number words).
  - **First run of the page check** found 14 real problems, all fixed in `build_page.py`: number words in page text ("one", "two"), "Sentinel-2" and "Steps 4–9" not marked, "RM’000" and "SHA-256" in plain text, and "Two" in 2 `alt` texts.
  - **Planted errors in copies of the page** (Claude Code's scratchpad, deleted afterwards): 18 kinds (number text, `data-raw`, locator, untagged digit, number word, forest-loss note removed, caveat wording, "+" on a ratio, hyphen for minus, missing space before a unit, FFB unit with a space, quoted text changed, no-tag reason misused and unknown, appendix field, digit in `alt`, unknown `data-id`, a spec number removed). **18 of 18 caught.** (A first planted locator change hit the firm-name span, whose new locator reads the same name; repeated on a number span: caught.)
  - **`test_check_numbers.py`** (Step 3 planted errors, now with the page check on): baseline **pass**, **34 of 34 caught**.
  - **`check_offline.py`:** **pass**. 11 loaded references, all local; 2 links to other sites (the CC BY 4.0 and CC BY-SA 4.0 licence pages), not loaded. The page icon is an empty inline `data:` icon, so the browser does not ask for `/favicon.ico`.
  - **`scan_exclusions.py`:** `site/index.html`, `site/assets/style.css`, `site/assets/manifest.csv`, `build/site_data.json`, `docs/number_sources.csv`, `docs/caveats.csv`, `LICENSE.md`, `scripts/build_page.py`, `scripts/check_offline.py`: **clean**. The other scripts show only the hits already known from Step 3: the folder name in the default pilot path (5 scripts) and `scan_exclusions.py`'s own search patterns. Three regular expressions in `check_numbers.py` matched the Windows-path pattern; they were rewritten with `[0-9]`.
  - **In a browser** (Playwright, page served from `site/` on localhost only; screenshots deleted afterwards): phone width 375 px and desktop 1280 px, light and dark. After two fixes (a long number phrase that widened the feature cards; images without a size, which moved in-page links), no horizontal page scroll at 375 px, and in-page links land on their sections. The server log shows requests for the page, the style sheet and the 9 images only.
- **Pass/fail:** Pass.
- **Hours:** Claude Code about 0.5 h for the Step 3 close-out and Step 4 (active time; estimate from the system clock, about 19:20–19:52 MYT) · Yaseen: to fill.
- **Issues:**
  - **Image sizes typed in `build_page.py`.** The `width` and `height` attributes are numbers typed in the script. They are layout attributes, not page text, and `check_offline.py` compares them with each file. Without them, in-page links landed in the wrong place (open question 3).
  - **Pilot inconsistency on an image:** the distance map's title says "max 153.4 km"; the grid report (and this page's text) says 153.5 km. Numbers on images are not tagged and are shown as they are (open question 4).
  - **Pilot text keeps the pilot's own words**, such as "WRO/sanctions history", "Hansen", "GFW". The plain-word line next to each item explains it.
  - **Size:** 9 images, 4.7 MB, copied unchanged (the forest map is 1.2 MB). Resizing would need a new tool or a decision (open question 5).
  - **"SHA-256"** was added to the identifier list, as "similar" to the examples in decision 5.
  - **The appendix makes the page long** (540 KB of HTML; it is closed by default).
  - **Not built in this step:** the full Step 5 checks (for example the scan of every tracked file with an accepted-mentions list, and attributions checked against `docs/content_inventory.md` section b).
- **Open questions for Yaseen:**
  1. **Sepakau image** (section 6): keep it, with its working note "For Yaseen to pick the point on the mill", the R028 label, the eMSPO record ID and the coordinates; or drop it?
  2. **Sarawak forest-loss caveat:** "...not necessarily land cleared by the firm" sits under Sarawak-wide numbers. Keep it as decided, or another wording for these numbers?
  3. **Image `width` and `height` attributes** typed in `build_page.py` (layout only, checked against the files): accept?
  4. **Distance map** says 153.4 km where the grid report says 153.5 km: leave it (images as they are), or add a note in the caption that names both pilot files?
  5. **Image size:** keep the copies unchanged (4.7 MB), or allow smaller copies?
  6. **Spec rows not in the brief:** the 12 ENCORE counts (made for decision 9) and the 2 illustration firm counts (for decision 6). Accept?
  7. **Licence links:** the footer links to the 2 CC licence pages (links only, nothing loaded). Keep, or show the addresses as plain text?
  8. **Loss-patch imagery** is not shown. Supply credit wording for its scenes if it should be.
- **End of step:** pilot snapshot `--check` at 2026-10-25T11:48:11Z: **no change** (1,054 files, exit 0). Re-run after writing this entry: see `build/pilot_snapshot_checks.log`.

#### Step 4 close-out — approval and decisions

- **Date:** 2026-10-25
- **Approval:** Yaseen approved Step 4. Yaseen's hours for Step 4: 1 h. Yaseen reviewed the page: content OK, no other wording notes.
- **Decisions recorded** in `CLAUDE.md` (new section "Step 4 decisions: close-out"; public-release decision 5 and Step 3 decisions 8 and 10 point to it). They answer the 8 Step 4 open questions and add decisions 9–11.
- **Changes made:**
  - **Sepakau image (decision 1):** removed from `scripts/copy_images.py`, `site/assets/` (file deleted), `site/assets/manifest.csv` (rewritten by the script: 8 images, 4,071,210 bytes) and the page (section 6 figure and its image size in `build_page.py`). The Copernicus credit covered only that image: removed from the footer, from the footer note on supplied wording, and from `LICENSE.md`. The Sentinel-2 images are still named as a source used for checks (Sources table, source register list).
  - **Sarawak-wide note (decision 2):** `docs/caveats.csv` `forest_loss_sarawak` = "Loss from any cause, including replanting and logging." The firm caveat is unchanged.
  - **Distance map (decision 4):** caption note: "the largest distance to a mill point in the map title (`reports/step9_maps/step9_distances.png`) differs in the last decimal from the 153.5 km in the grid's method card (`docs/methods/regional_grid.md`). Both are shown as the pilot has them." Two differences from the brief: (a) **153.4 km is not typed on the page**: it is printed only inside the image (the pilot's `step9_maps.py` formats the grid maximum, 153.450, with one decimal) and no pilot text file records it, so a typed 153.4 would break rule 2 (open question 1); (b) **153.5 km is in the grid's method card**, not in the grid report (`reports/step9_grid.md` says "to 153 km").
  - **Section 9 removed (decision 10):** `docs/number_sources.csv` 319 → 272 rows: the 46 `s9.*` rows (hours, full-build estimate, the 2 illustration firm counts), and `s10.open_review_items` ("Open items (2)" would no longer match the 1 item shown; not in the brief). `s10.options_for_the_decision` → `s9.options_for_the_decision`, section "9 Next decisions". Caveats `hours_unconfirmed`, `estimate_assumptions`, `illustration_only` removed (used only by section 9): 20 → 17. R058 removed from the pending decisions (`extract.py`, `check_numbers.py`). The full-build list is now open (not collapsed) in section 9, "What would need to change for a full build", without its hours item ("Time records", `FULL_BUILD_LEFT_OUT` in `build_page.py`). Contents list, section 1 cross-reference and the CSS of the hours table updated. No glossary term belonged only to section 9. `test_check_numbers.py`: the 3 planted errors that used `s9.step_1_setup_claude_code_h` now use `s5.road_length_used_km` (`reports/step9_grid.md`); the numbered-items plant uses the new id.
  - **"Claude Code" (decision 11):** on the page **105 → 1** (whole HTML file, tags and appendix included; visible text and attributes both 1). The one: gap 14, Yaseen's sentence word for word, then "This covers all 195 checked values." Elsewhere:
    - byline "Built from the pilot's files."; footer "built by script from the palm oil pilot's files, with an AI coding assistant" (open question 4);
    - section 6: "All 195 checks were automated self-checks. The planned manual reviews were waived, so no value was checked independently (section 8)."; worked example "pass (an automated check)";
    - caveat `self_checks`: "All checks were self-checks, done by the same party that built the values; no value was checked independently (R043)."; glossary "Self-check": "A check done by the same party that built the value, not by an independent reviewer.";
    - gap 14 title: the page shows "Self-checks" instead of the pilot's title (which names Claude Code); the section's intro says the title is shortened (open question 2);
    - tags: `s0.date_of_the_findings_report` quote shortened to "2026-10-24 · Status"; `s8.values_checked_only_by_claude_code` → `s8.checked_values_all_self_checks`, quote "All 195 checked values were checked"; `s6.evidence_rows_checked_by_claude_code` → `s6.evidence_rows_with_a_recorded_check`, locator `checked_by=Claude Code` → `checked_by!=` (rows with a checker recorded; same 195 rows, open question 3).
  - **Bug fixed (not in the brief):** in section 8, every gap item listed the notes of all 16 gaps (the builder entered every gap's numbers into each item's block). Each item now lists only its own notes (page notes 254 → 69). `check_numbers.py` did not catch this: it checks that each number's notes are in its block, not that each note in a block belongs to a number there (Step 5, check 1).
  - Docs: `docs/page_outline.md` and `docs/content_inventory.md` carry a one-line note under their section 9 heading.
- **Quick checks (Step 4 set), after the changes:**
  - `copy_images.py`: 8 images copied, manifest rewritten. `extract.py`: 272 numbers (202 from CSV, 70 from markdown), 9 lists, 25 pilot files read (`progress_log.md` no longer needed); `build/site_data.json` SHA-256 `e35b77ccdacb36f18f01deed87fc2e927b43b32c433e22ac1eadeb09f1664c80`.
  - `build_page.py` twice: byte-identical. `site/index.html` 441,350 bytes, SHA-256 `f80cb3cf787a877f3c81de2ce8828a82fae38dec60841cce43c4d60e9e862d73`; `style.css` `e2695643bb61cb5a80e40768994e4401680cd1afa12c1ae8a49b0301b732ad54`.
  - `check_numbers.py`: **pass**, 0 failures (272 of 272 spec numbers on the page; 591 number spans, 184 quoted text spans, 240 no-tag elements, 1,375 appendix fields, 69 notes, 2,444 other text runs with no digit or number word). `test_check_numbers.py`: baseline pass, **34 of 34** caught.
  - `check_offline.py`: **pass** (8 images, sizes match; 10 loaded references, all local; 2 licence links). `scan_exclusions.py` over the page, style sheet, manifest, `site_data.json`, spec and caveats: **clean**.

---

### Step 5 — Checks

- **Date:** 2026-10-25
- **What was done:** the six checks of the brief, plus the attribution check named in the Steps table. Nothing was built or changed in `site/`, `scripts/` or `docs/` during Step 5. Two throw-away check scripts were written in Claude Code's scratchpad (not in this folder): a page-level planted-error test and a link and path check.
- **Checks:**
  1. **Numbers.** `check_numbers.py` on `site/index.html`: **pass** (see the close-out above). Planted errors:
     - `test_check_numbers.py` (data, spec and pilot copies in `build/planted_test/`, deleted at the end): baseline pass, **34 of 34 caught**;
     - page copies (scratchpad, deleted at the end): baseline pass, **21 of 21 caught**: the 18 kinds from Step 4, plus: forest-loss note removed from a gap item, the Sarawak note put back in the old wording, a removed section 9 number put back.
     - **Limit found:** a note placed in a block where no number needs it is **not** caught (tested: exit 0). This is how the Step 4 gap-note bug passed. Adding the reverse check to `check_numbers.py` needs approval (open question 9).
  2. **Links and files.** 181 in-page links (53 targets): all targets exist. 8 images: all in `site/assets/`. 60 pilot paths named on the page (after expanding `{1,2,3}` and `*`; 48 in "Details in the pilot" lines; 12 short names resolved in the folder named before them): all exist in the pilot. The findings-report sections named (§1, 2, 3, 4, 5, 7.5, 8) and the headings named in brackets (Scope, Features, Steps, Current status, Steps 4–9, Known limitations in all 10 method cards) exist. `check_offline.py`: **pass**. In the browser, the page requested only `index.html`, `style.css` and the 8 images, all from the local server.
  3. **Privacy.** `scan_exclusions.py` over the 20 text files that would be committed, with the 18 terms of `build/private_terms.txt`. **No e-mail, phone number, eMSPO contact value, personal name or git e-mail in any file.** Hits, all checked one by one:
     - `site/` (4 files), `LICENSE.md`, `LICENSES/MIT.txt`, `docs/caveats.csv`, `docs/number_sources.csv`, `scripts/build_page.py`, `scripts/check_offline.py`: **clean**.
     - **Project name (term line 22):** only inside the folder names `nrfr-pilot` / `nrfr-pilot-site`, on 49 lines in 11 files: `.gitignore` 1, `CLAUDE.md` 4, `PROGRESS.md` 8, `docs/content_inventory.md` 6, `docs/page_outline.md` 2, and the default `PILOT_DIR` or docstrings of 6 scripts (`pilot_snapshot.py` 17, `extract.py` 4, `check_numbers.py` 2, `copy_images.py` 2, `scan_exclusions.py` 2, `test_check_numbers.py` 1). Accepted by Step 2 decision 2 for the folders; see open question 10.
     - **General terms (term lines 11–13 and 24, already accepted in Step 1):** in the rule texts and records of `CLAUDE.md`, `PROGRESS.md` and `docs/`, and in `scan_exclusions.py`'s docstring. None quoted project-internal content (open question 11; reworded as a general rule in the Step 5 fix round).
     - **Other patterns:** `PROGRESS.md` 2 and `docs/content_inventory.md` 1 "paths" = the text `/Users/` written as a search pattern; `docs/content_inventory.md` 5 "titles" = the list of titles that were searched for; 8 "eMSPO" = the contact field names in the exclusion list (no values); `scripts/scan_exclusions.py` = its own patterns.
     - **Images:** the 8 PNGs hold only a "Software: Matplotlib" text chunk (no EXIF or other text). Their content was viewed in Step 4.
     - Not scannable: Yaseen's full name and student ID (not in the term list).
  4. **Views.** Playwright, page served from `site/` on 127.0.0.1 only; 4 full-page screenshots (phone 390 px and desktop 1,280 px, light and dark) and 6 close-ups in `build/screenshots/` (git-ignored, 18.5 MB). The browser tool also wrote a page snapshot in `.playwright-mcp/` in this folder; it was deleted. No horizontal page scroll at 390 px. Contrast (WCAG ratio) of 20 text styles: dark mode all ≥ 6.1; light mode all ≥ 5.1 except the note letters. **Hard to read:**
     - **Note letters** (the small a, b, c after numbers and in front of notes), light mode: contrast 2.7–2.8 (guideline 4.5), and about 8 px after the numbers.
     - **Diagram text** (section 3) on a phone: 9–10.5 px; the legend is tiny; "pilot_firm_year.csv" touches its box edge.
     - **5 tables scroll sideways** on a phone (the 34 sources, the grid check, forest loss by a few pixels, FFB yield, ENCORE counts). In FFB yield the 2023 column is cut off, and the restated value crowds its cell.
     - **Text inside the map images** is unreadable at phone width (zoom check, distance map); there is no way to open an image at full size except pinch-zoom.
     - **Images stay white in dark mode** (the pilot's maps are drawn on white).
     - The page is long: 40,352 px at phone width (about 48 screens).
  5. **Plain language** (proposals only, **not applied**; numbers unchanged and still tagged; pilot quotes are not rewritten, a plain line can be added next to them):
     1. §1 "In the pilot's terms, success means a pipeline that can be traced and re-run…" → "The pilot counts as a success if every step from download to table can be followed and repeated, even where a measure could not be built, as long as the missing piece is written down."
     2. §1 "3 listed palm oil growers" / "5 listed growers" → "3 palm oil growers listed on the stock exchange" ("listed" can be read as "on a list").
     3. §1 "…in 6 families: geospatial, climate, dependency on nature, operational, regulatory and financial" → "…in 6 groups: land and maps, climate, dependence on nature, operations, rules and bans, and finance".
     4. §2 "The download log has 602 records: 174 files kept (1 of them only the file header), …; and 32 small reads of satellite images." → three short sentences: "The download log has 602 entries. 174 files were kept (about 1.8 GB, in 24 folders); 1 of them holds only column names. 396 monthly rainfall files were cut down to Sarawak and then deleted, because they were too large to keep; 32 entries are small pieces read from satellite images."
     5. §3 message "…through clips and results per firm…, and every rebuild of the scripts gave the same files." → "…through cut-down copies and results for each firm, to the final tables. Each time the scripts were run again, they produced exactly the same files."
     6. §3 "Results per firm (`data/processed/firm{1,2,3}_*.csv`)" → "Results per firm (`data/processed/`, a set of files for each firm)".
     7. §3 "33 Python scripts, 4 runner scripts and 2 package lists." → "33 Python programs, 4 scripts that run them in order, and 2 lists of the software they need."
     8. §3 "9 method cards; a feature dictionary with 23 rows…; a check register with 20 rows per firm." → "9 method cards (a short note per measure on how it was made); a list that describes every column (23 rows, 15 of them for the grid); a list of checks with 20 rows per firm."
     9. §3 "A review queue of 58 decisions: 56 decided and 2 open." → "A log of 58 questions that needed a decision: 56 decided and 2 still open." Also: section 9 now shows only R057, so a reader may look for the second open item (open question 5).
     10. §3 "The grid has no evidence rows; it is documented by its dictionary rows and its method card" → "The grid has no evidence record for each value; it is described by its column list and its method card instead."
     11. §4 forest-loss check "…matched the Global Forest Watch map at its 2 significant figures (…). Satellite patches: 6 pass, 2 partly plausible." → "…matched the Global Forest Watch website, which shows only the first 2 digits of each number (…). Satellite close-ups of the loss areas: 6 passed, 2 were only partly plausible."
     12. §4 rainfall "An independent recomputation found 0 of 396 mill-years off by more than 2 mm." → "A second, separate calculation found 0 of 396 mill-years that differed by more than 2 mm." ("Independent" clashes with "no value was checked independently".)
     13. §4 ENCORE "25 ecosystem services × 2 activities" → "25 kinds of benefit from nature (ENCORE calls them “ecosystem services”) × 2 activities"; "…agree for 50/50 ratings; 150 values pass." → "…agree for all 50/50 ratings, and all 150 values in the tables passed their check."
     14. §4 debt-to-equity "Every non-zero figure was found on its page (63/63 (SOP), 60/60 (Ta Ann), 46/46 (SPB)); 9/9 pass." → "Every figure that is not zero was found again on its report page: SOP 63/63, Ta Ann 60/60, SPB 46/46. All 9/9 values pass."
     15. §5 grid check "The differences are rounding only, and the pixel counts are the same." → "The small differences come only from rounding, and both totals count the same satellite pixels (the smallest squares of the satellite map)."
     16. §5 zoom-check caption → "Close-up check: the grid squares next to the satellite pixels they were made from, around the square with the most forest loss in 2021."
     17. §6 "(stacked unchanged into `pilot_firm_year.csv`)" → "(copied unchanged into the combined table `pilot_firm_year.csv`)"; "Its file fingerprint (SHA-256) was recomputed and is unchanged." → "A digital fingerprint of the file (SHA-256) was calculated again and still matches, so the file has not changed."
     18. §6 "the balance sheet (p151 (printed 149))" → "the balance sheet (page 151 of the file; printed page 149)". The page form of these 2 page numbers would need a rule (they are "as is" values).
     19. §7 certification "Firm-reported mill-years behind these values: SOP 10 of 21, …" → "How many mill-years (a mill in a given year) rest only on the firm's own statement: SOP 10 of 21, …".
     20. Units: "mt/ha", "Mt/WHa", "mt" and "AR 2022" are not explained on the page → add to the glossary "mt/ha: tonnes per hectare, as printed" and "AR: annual report"; the pilot's meaning of "Mt/WHa" should be confirmed before it is explained.
     21. §8 gap 4 "(an HTTP 500 error; 3 mills tried)" → "(the website returned a server error, “HTTP 500”; 3 mills were tried)".
     22. §8 gap 5 "SOP's printed yield matches production ÷ mature area only for 2021 (2022: 14.68 mt/ha vs 14.50 mt/ha; …)" → "SOP's printed yield equals its harvest divided by the area of mature palms only for 2021. For 2022 that sum gives 14.68 mt/ha against 14.50 mt/ha printed; for 2023, 15.31 mt/ha against 15.02 mt/ha."
     23. §8 gap 9 "…showed logging roads and broken canopy, not clearing. Metanik's catchment is…" → "…showed logging roads and gaps in the tree cover, not cleared land. Metanik, one of SOP's mills, has a catchment of…"; gap 10 "…the map shows few digits, so it cannot tell “more than” from “at least” the tree-cover threshold: a difference of at most 0.15 ha." → "The website shows only rounded numbers, so the pilot could not tell whether it counts forest as “more than” or “at least” the tree-cover threshold. Either way, the difference is at most 0.15 ha."
     24. §9 pilot text "This could cover any item in section 7.5" refers to the findings report, not this page; and the full-build items use the pilot's terms ("GFW API key", "not_checked", "GNW", "plan rule 3", "rule 1"). → add a plain line above the list: "In the pilot's own words; “section 7.5” is this list in the findings report."
  6. **Commit readiness** (no commit made; `git status`: no commits, 28 untracked files, nothing staged):
     - **Would be committed (28 files, 4,959,152 bytes):** `.gitignore` 774; `CLAUDE.md` 12,459; `LICENSE.md` 3,350; `LICENSES/MIT.txt` 1,084; `PROGRESS.md` 54,816 (this file, before this entry; about 78 KB after it); `docs/caveats.csv` 3,729; `docs/content_inventory.md` 38,591; `docs/number_sources.csv` 68,455; `docs/page_outline.md` 46,936; `scripts/build_page.py` 91,882; `scripts/check_numbers.py` 42,360; `scripts/check_offline.py` 6,954; `scripts/copy_images.py` 3,250; `scripts/extract.py` 31,100; `scripts/pilot_snapshot.py` 11,331; `scripts/scan_exclusions.py` 6,433; `scripts/test_check_numbers.py` 12,375; `site/index.html` 441,350; `site/assets/style.css` 9,621; `site/assets/manifest.csv` 1,092; 8 PNGs 4,071,210 (`step5_map_forest.png` 1,224,645, `step5_map_palm.png` 310,186, `step8_catchments_map.png` 224,160, `step9_distances.png` 581,116, `step9_loss_2021.png` 547,834, `step9_loss_2022.png` 547,108, `step9_loss_2023.png` 547,164, `step9_zoom_check.png` 88,997). Sizes before this entry was written.
     - **Ignored (22 files, 19,081,964 bytes):** `.DS_Store`; `build/` (snapshot and its log, `private_terms.txt`, `site_data.json`, check reports, `step3/`, `superseded/`, 10 screenshots).
     - **No PDF, raw download, page extract, personal data or pilot CSV copy** among the 28. `docs/number_sources.csv` and `docs/caveats.csv` hold source locators and short quotes, not copies of pilot CSVs.
     - **Flag 1, project name:** the folder name is in 11 of the 28 files (check 3). Once committed it stays in the history, even if the GitHub repository gets a neutral name at Step 6 (open question 10).
     - **Flag 2, rule texts:** public-release decision 4 and the Step 1 records were more specific than a general rule (open question 11; reworded in the Step 5 fix round).
     - **Flag 3, AI tools:** `CLAUDE.md`, `PROGRESS.md`, `docs/` and the script docstrings name Claude Code many times (decision 11 covers the page only). The commit attribution line would name it too.
  7. **Attributions** (against `docs/content_inventory.md`, section b): Hansen, geoBoundaries, OpenStreetMap, ENCORE, CBP, Universal Mill List, eMSPO, RSPO, annual reports, CHIRPS: as required. Copernicus: no longer needed (no Sentinel data shown). **Gaps (open question 8):** (a) Descals palm map: section b asks for "clipped to Sarawak"; the page does not say it; (b) EU sanctions list: section b asks for its licence when the page says the current list was searched; the footer names the list without a licence; (c) Global Forest Watch: section b asks for a GFW (WRI) and UMD/Hansen credit "if GFW check numbers are shown"; the forest-loss card shows the comparison results, and there is no GFW credit line.
- **Pilot snapshot:** start 2026-10-25T12:02:03Z (session start) and 12:12:56Z (start of Step 5): **no change**; end 12:21:22Z: **no change** (1,054 files, exit 0). `find -newermt "2026-10-25 20:00"` in the pilot (`.DS_Store` excluded): nothing modified. The pilot's `scripts/__pycache__/` dates from 23–24 October and is in the baseline. All scripts ran with `python3 -B`.
- **Pass/fail:** Pass (all checks); findings and proposals below for Yaseen.
- **Hours:** Claude Code about 0.4 h for the Step 4 close-out and Step 5 (active time; estimate from the system clock, about 20:02–20:25 MYT) · Yaseen: to fill.
- **Issues:**
  - A search in the pilot printed a few raw sanctions-list lines (public EU list) into Claude Code's session; nothing was written anywhere. Later searches excluded `data/raw/`.
- **Open questions for Yaseen:**
  1. **153.4 km** (decision 4): keep the caption without the typed number (as now), or allow it, for example as a number "printed in an image" with its own no-tag reason (a rule change)?
  2. **Gap 14 title:** the page shows "Self-checks" instead of the pilot's title, to keep "Claude Code" to the one sentence. Accept?
  3. **Section 6 tag:** the count of checked values now uses the locator `checked_by!=` (any checker recorded) instead of `checked_by=Claude Code`. Same 195 rows. Accept?
  4. **Footer:** "built by script from the palm oil pilot's files, with an AI coding assistant". Keep, change or remove?
  5. **"2 open"** in section 3 (pilot count, R057 and R058) while section 9 shows only R057: leave, or add "(including the decision in section 9)"?
  6. **Plain language:** which of the 24 proposals to apply?
  7. **Readability:** darker note letters in light mode; larger diagram text; a link on each image to the full-size file (local, in `site/assets/`); FFB table layout on phones. Which, if any?
  8. **Attributions:** add "clipped to Sarawak" for Descals, the EU list's licence, and a GFW (WRI) credit?
  9. **Checker:** add the reverse note check (each note in a block must belong to a number in that block, or be one of the block's named notes)?
  10. **Project name in the folder name** (11 files): commit as is, or change the default `PILOT_DIR` and the planning texts to a neutral name before the first commit?
  11. **Rule texts** about project-internal content: keep in the public planning files, or reword as a general rule before the first commit? (Decided: reworded, Step 5 decision 8.)
- **End of step:** pilot snapshot `--check` at 2026-10-25T12:21:22Z: **no change** (1,054 files, exit 0). Re-run after writing this entry: see `build/pilot_snapshot_checks.log`.

#### Step 5 fix round — decisions applied

- **Date:** 2026-10-25
- **Decisions:** Yaseen's 11 decisions on the Step 5 findings, recorded in `CLAUDE.md` ("Step 5 decisions: fix round"). Yaseen's hours for Step 5: 1 h. Decisions 1–3 (153.4 km untyped, the gap 14 title and the `checked_by!=` locator, the footer line) needed no change.
- **PI's permission (decision 10):** received 2026-10-25: publishing on public GitHub and Vercel is approved. This meets rule 14 for Step 6. Nothing was pushed; there is no remote.
- **Project name (decision 11):** may appear in folder names, paths and the repository. The 11 files that hold the folder name are unchanged. Page text still says "palm oil pilot" (public-release decision 4).
- **Plain language (decision 4).** All 24 rewrites were applied; none was skipped in full. Where a rewrite would have changed a fact, a pilot quote or a checked rule, the part was kept to the pilot:
  - **Applied as proposed:** 1, 2, 5, 6, 7, 9, 10, 12, 13, 15, 16, 17, 19, 21, 24. Checked against the pilot first: "the same pixels" (13, 15: `reports/step9_grid.md`, "the grid script counts the same pixels"); "all 150 values" (the static table holds 153 values, 3 of them the missing peat values; findings §2); "the most forest loss in 2021" (`reports/step9_grid.md`, zoom check); Metanik is an SOP mill.
  - **3:** applied, with "which the pilot calls families" kept, so the glossary entry "Family" still has a word to explain.
  - **4:** applied, except "holds only column names": the file is the CHIRPS NetCDF header (findings §2: "1 header-only file (the CHIRPS NetCDF header)"), so the page says "holds only its file header".
  - **8:** "a list that describes every column" would overstate: the feature dictionary has a row per feature and per grid column (ENCORE's 50 columns share a row). The page says "a list that describes each measure and each grid column".
  - **11 and 14, in part:** "6 pass, 2 partly plausible" and "63/63 (SOP), 60/60 (Ta Ann), 46/46 (SPB)" are each a single tagged value in the pilot's words and order, so they cannot be reworded or reordered. Rewrite 11 now reads "Satellite close-ups of the loss areas, in the pilot's words: 6 pass, 2 partly plausible."; rewrite 14 keeps the value in brackets.
  - **18:** applied without a new rule: in `docs/number_sources.csv` the 2 phrase rows ("p151 (printed 149)", "p215 (printed 213)") became 4 number rows from the same quotes in `evidence.csv` (`s6.example_balance_sheet_pdf_page` 151, `_printed_page` 149, `s6.example_borrowings_note_pdf_page` 215, `_printed_page` 213). The borrowings note got the same form as the balance sheet (not in the proposal), so the two adjacent page references read alike. Spec 272 → 274 rows.
  - **20:** glossary entries "mt, mt/ha", "Mt/WHa" and "AR". The meaning of "Mt/WHa" comes from the pilot's method card `docs/methods/ffb_yield.md` (SPB: "WHa – Weighted average hectarage", harvestable).
  - **22:** "that calculation" instead of "that sum" (it is a division). The order was checked: 14.68 and 15.31 are the pilot's production ÷ year-end mature area, 14.50 and 15.02 the printed values (`data/processed/firm1_ffb_yield.csv`).
  - **23:** "Metanik, one of SOP's mills" has the number word "one", which `check_numbers.py` rejects (Step 3 decision 6); the page says "SOP's Metanik mill has a catchment of …". Gap 10 keeps its first sentence on coverage ("covers 6 of 12 catchments").
  - Not changed: "2 open" in section 3 while section 9 shows only R057 (Step 5 open question 5 has no decision yet).
- **Readability (decision 5).** Measured with the same script in the browser (Playwright; page served from `site/` on 127.0.0.1), before (the Step 4 close-out page) and after:

  | Issue | Before | After |
  | --- | --- | --- |
  | Note letters, light mode | contrast 2.82–2.94 after numbers, 2.69 in front of notes; letters 6.7–10.6 px | 5.68–5.93 and 5.41 (new colour `--note-ink` #8a5a00); letters 12 px |
  | Note letters, dark mode | 7.13–7.85 and 6.85 | unchanged colour, 7.13–7.85 and 6.85; letters 12 px |
  | Diagram text at 390 px | drawing (SVG), text 8.6–10.5 px | HTML and CSS, text 13–14.4 px; 0 of 35 boxes overflow; 3 columns of 111 px, final files stacked; desktop 14–14.4 px |
  | Wide tables at 390 px | 4 tables wider than their 358 px box (sources 510 px, grid check 490, FFB 376, ENCORE 371) already scrolled inside the box, with no sign of more columns; not scrollable from the keyboard | the same 4 scroll inside the box (510, 503, 386, 371 px); a shadow at the edge shows there is more; each table box takes keyboard focus (`role="region"`, `tabindex`, a label) |
  | Page scrolls sideways | no, at 390 and 360 px | no, at 390 and 360 px |
  | Maps | not linked; in dark mode the image sat on white with a 1 px dark border | each of the 8 images links to its full-size file (the image and a caption link "Open the full-size image"); a white frame in both modes; no filter or recolouring |

  The page is longer at 390 px: 39,322 → 41,272 px (the taller diagram, the frames).
- **Credits (decision 6):**
  - palm map: "22 tiles clipped to Sarawak", as on the pilot's own map footer (`scripts/step5_maps.py`); the number is tagged (`s3.palm_map_tiles_clipped`), in the map caption and the footer;
  - EU sanctions list: the licence cell of `source_register.csv`, quoted and tagged;
  - Global Forest Watch: its name and licence cell from `source_register.csv`, "used only to check the forest-loss values; no screenshots are shown", and the Hansen/UMD credit for the tree-cover loss data;
  - `LICENSE.md`: "map tiles clipped to Sarawak" on the Descals line, and a line for the EU list and Global Forest Watch.
- **Note check (decision 7):** `check_numbers.py` now fails on any note in a block that no number in the block needs (by its spec caveats) and that no element declares with `data-needs`. `data-needs` is allowed only on an image (`figure`), a feature card (`article`) or a missing value (class "missing"); it must name a caveat of `docs/caveats.csv` that is listed in its block. The appendix must list exactly the caveats of `docs/caveats.csv`. `build_page.py` declares the notes of the images, the feature cards and the missing cells with `data-needs` (`Block.needs`).
- **Planted-error tests:** the page plants are now in `scripts/test_check_numbers.py` (in Step 5 they were a throw-away script): the 21 of Step 5, plus 5 new ones for decision 7 (a peat note in gap 9, a forest-loss note in the debt-to-equity block, the import-ban table's note removed, `data-needs` on a paragraph, a note removed from the appendix).
- **Planning files (decision 8):** every passage that said such plans or topics exist was reworded to the general rule "project-internal content is never published": `CLAUDE.md` public-release decision 4, `PROGRESS.md` (Step 1–5 records), `docs/content_inventory.md` (sections c, d, e4) and `docs/page_outline.md`. Also the docstring of `scripts/scan_exclusions.py` (committed too; not in the list of the decision). `build/private_terms.txt` is unchanged and local.
- **`README.md` (decision 9):** what the page is; how to rebuild it (`PILOT_DIR`, then `copy_images.py`, `extract.py`, `build_page.py`); how to run the checks; the licences. Its only digits are in the command name `python3` and the licence versions.
- **Also changed (not in the brief):**
  - **Bug fixed:** the zoom-check image (section 5) never got its Sarawak forest-loss note: the old code added the note after the block had been written. It now shows (page notes 69 → 70). The new note check would have caught it in a block without that note.
  - `check_offline.py` also checks that every link to a local file (the image links) points to a file in `site/`.
  - `.gitignore`: `.playwright-mcp/` (the browser tool writes screenshots there in this folder).
  - The diagram's words list and the sections around it are unchanged; the drawing code (`COLS`, `svg_*`) was removed.
- **Files changed:** `CLAUDE.md`, `PROGRESS.md`, `LICENSE.md`, `.gitignore`, `docs/number_sources.csv`, `docs/content_inventory.md`, `docs/page_outline.md`, `scripts/build_page.py`, `scripts/check_numbers.py`, `scripts/test_check_numbers.py`, `scripts/check_offline.py`, `scripts/scan_exclusions.py` (docstring), `site/index.html`, `site/assets/style.css`. New: `README.md`. Unchanged: `scripts/extract.py`, `scripts/copy_images.py`, `scripts/pilot_snapshot.py`, `docs/caveats.csv`, the 8 images and `site/assets/manifest.csv`.
- **Checks:**
  - **Pilot snapshot:** start 2026-10-25T15:23:08Z **no change**; end 15:53:44Z **no change** (1,054 files, exit 0). `find -newermt "2026-10-25 23:20"` in the pilot (`.DS_Store` excluded): nothing modified. All scripts ran with `python3 -B`.
  - **Extraction:** `copy_images.py` 8 images, manifest unchanged; `extract.py` 274 of 274 numbers (204 from CSV, 70 from markdown), twice: `build/site_data.json` SHA-256 `87a02e5e198b238a3b5494d480de28a7d6a30df597f75bde516f3156e5651e68` both times.
  - **Two builds:** byte-identical (`cmp`). `site/index.html` 441,729 bytes, SHA-256 `c15473146e5ae8b75ae05a40df277f28535feb483e891981c210b645317cf1e3`; `site/assets/style.css` 12,469 bytes, `ec28b709fb98f85db4f68444f3b3f73586da1cb527a966164378b6aafc6f034a`.
  - **`check_numbers.py`:** **pass**, 0 failures: 274 of 274 spec numbers on the page; 597 number spans, 187 quoted text spans, 245 no-tag elements, 1,385 appendix fields, 70 notes, 22 elements with `data-needs`, 54 note-need checks, 2,470 other text runs (no digit, no number word). Its first run found 1 failure, the number word "one" (rewrite 23); fixed.
  - **`test_check_numbers.py`:** baseline pass; **34 of 34** planted errors in data, spec and pilot copies caught; page baseline pass; **26 of 26** planted errors in the page copy caught. The appendix plant (P26) is caught by the older rule (a number's note missing from its block); the new appendix rule is a backstop, because every caveat belongs to at least one number in the appendix.
  - **`check_offline.py`:** **pass**: 8 images (sizes match), 10 loaded references (all local), 16 links to local files (all present), 2 licence links (not loaded). The local server logged requests for the page, the style sheet and the 8 images only.
  - **Link and path check** (Step 5 throw-away script, copied to Claude Code's scratchpad and extended to the image links; not saved here): 181 in-page links (53 targets) all found; 16 image links, each image links to its own file; 58 pilot paths named on the page all exist (was 60: the per-firm glob in section 3 became `data/processed/`); the findings sections and headings named exist. **Pass.**
  - **`scan_exclusions.py`** over the 21 text files that would be committed (with `README.md`): no e-mail, phone number, eMSPO contact value, personal name or git e-mail. Hits: the project name inside the folder name or the default path (term line 22) in 12 files: the 11 of Step 5 and `README.md` (approved, decision 11); `PROGRESS.md` 4 (with this entry) and `docs/content_inventory.md` 1 "paths" (each the text `/Users/` written as a search pattern); `docs/content_inventory.md` 5 "titles" and 8 "eMSPO" (the lists of what is searched for); `scripts/scan_exclusions.py` (its own patterns). **No general term (term lines 7–21, 23–24) in any file** (Step 5: lines 11–13 and 24 in several files).
  - **Screenshots** (git-ignored, `build/screenshots/fix-*`): full page and close-ups (diagram, a feature card with its notes, the FFB table, the palm map) at 390 px and 1,280 px, light and dark: 20 files. The Step 5 screenshots are kept.
  - **Commit readiness:** 29 files would be committed (the 28 of Step 5 + `README.md`), 5,007,804 bytes before this entry. No commit; no remote.
- **Pass/fail:** Pass.
- **Hours:** Claude Code about 0.6 h (active time; estimate from the system clock, about 23:20–23:58 MYT) · Yaseen: to fill.
- **Issues:**
  - The FFB table still needs sideways scrolling on a phone (386 px in a 358 px box); its "restated" note wraps to 3 short lines.
  - The edge shadow on wide tables is drawn with CSS backgrounds; a browser that does not support `background-attachment: local` shows the table without the shadow (it still scrolls).
- **Open questions for Yaseen:**
  1. **EU licence wording:** the page quotes the pilot's licence cell ("European Commission reuse notice (Decision 2011/833/EU); the CSV distribution is listed as CC BY 4.0."). The pilot's own notes say CC BY 4.0 is listed for CSV 1.0, while the file used is CSV 1.1 (reuse notice). Keep the cell as recorded, or quote only the reuse-notice part?
  2. **Step 5 open question 5** is still open: "2 open" in section 3 (R057 and R058) while section 9 shows only R057.
  3. **Link and path check:** keep it as a throw-away script, or add it to `scripts/` so it can be re-run (and named in `README.md`)?
  4. **Page text and the project name:** decision 11 covers folder names, paths and the repository; the page still says "palm oil pilot". Confirm that this stays.
- **End of step:** pilot snapshot `--check` at 2026-10-25T15:53:44Z: **no change** (1,054 files, exit 0). Re-run after writing this entry: see `build/pilot_snapshot_checks.log`.

#### Step 5 close-out — approval and decisions

- **Date:** 2026-10-26
- **Approval:** Yaseen approved Step 5 with its fix round. Yaseen's hours for the fix round: 1 h.
- **Decisions recorded** in `CLAUDE.md` (new section "Step 5 close-out decisions"; public-release decisions 3 and 4 and Step 5 decisions 3 and 11 point to it). Decisions 1–4 answer the 4 open questions of the fix round; 5 is the Step 6 go; 6 (the commit e-mail) was asked and decided during this step.
- **Changes made:**
  - **EU licence (decision 1):** `extract.py` reads "European Commission reuse notice (Decision 2011/833/EU)" from the licence cell of `source_register.csv` (row `EU_FSF`) as an attribution quote (`text in licence: "…"`, found exactly once in the cell, like the other attribution quotes; attributions 9 → 10). The footer now reads: "Licence of the file used (the CSV file, version 1.1), as recorded in the pilot: European Commission reuse notice (Decision 2011/833/EU)." The version is the `version` cell's "Consolidated Financial Sanctions File 1.1, CSV"; a version needs no tag (Step 2 decision 4). `docs/content_inventory.md` (sections b and e3) notes it. **Not changed:** section 2's table of all registered sources still shows every licence cell as recorded, the EU row's full cell included (open question 1).
  - **Section 3 (decision 2):** "A log of 58 questions that needed a decision: 56 decided." Spec row `s3.review_items_open` removed from `docs/number_sources.csv` (274 → 273 rows); `docs/page_outline.md` notes it.
  - **Link and path check (decision 3):** new `scripts/check_links.py`, from the fix round's scratchpad script, rewritten for the repository (pilot path from `PILOT_DIR`, no absolute path, standard library only, reads only). Two changes from the scratchpad version: the places named in "Details in the pilot" lines (§ numbers, headings in brackets, "Steps 4–9", "Issues of Steps 2–9", a review ID, "rows starting “Grid:”") are read from the page instead of being typed into the script, and a bracket of any other form fails; a short file name must be found in exactly one of the folders named on the page (the scratchpad had a fixed list). Added to the check list in `README.md`.
  - **Project name (decision 4):** `<title>` and `<h1>` are "NRFR palm oil pilot". The second part of the former title stays under the heading as a subtitle, "From public data to a traceable table" (new CSS rule `.subtitle`). Intro: "The NRFR palm oil pilot tried, …". Elsewhere "the pilot": section 1's message, the footer ("built by script from the pilot's files, with an AI coding assistant") and the page description (`<meta name="description">`). On the page the name appears 3 times: title, heading, intro.
  - **Commit e-mail (decision 6):** before the first commit, `git config --local user.email` was a personal address, which git writes into every commit, so the public history would have shown it. On Yaseen's choice it is now Yaseen's GitHub no-reply address (the account's public ID, looked up on api.github.com, + the account name). It is not in any tracked file.
  - `docs/content_inventory.md` section e (public release check): the rows on the git identity, the EU list, the project name and the hours section were out of date; each got a note.
- **Files changed:** `CLAUDE.md`, `PROGRESS.md`, `README.md`, `docs/number_sources.csv`, `docs/content_inventory.md`, `docs/page_outline.md`, `scripts/extract.py`, `scripts/build_page.py`, `site/index.html`, `site/assets/style.css`. New: `scripts/check_links.py`. Unchanged: the other scripts, `docs/caveats.csv`, `LICENSE.md`, `LICENSES/MIT.txt`, the 8 images and `site/assets/manifest.csv`.
- **Checks** (all scripts with `python3 -B`; full output in `build/final_checks.txt`, git-ignored):
  - **Pilot snapshot:** start 2026-10-25T16:00:03Z **no change**; before the final run 16:12:08Z **no change** (1,054 files, exit 0). End of step: see the Step 6 entry.
  - **Extraction:** `copy_images.py` 8 images (4,071,210 bytes), manifest unchanged; `extract.py` 273 of 273 numbers (204 from CSV, 69 from markdown), twice: `build/site_data.json` SHA-256 `3d7efa7953ce2e418f45e69cf4a53421efbbaf2334530f03a09be8aa4bbbca3f` both times.
  - **Two builds:** byte-identical (`cmp`). `site/index.html` 440,801 bytes, SHA-256 `1a698f41788dab02f9664521e08548cbc56d1b42f44641d2df3e1073e2de019d`; `site/assets/style.css` 12,546 bytes, `e1b935b2bda5054fd1cc46f9226bdd5c5d3767ee09a947e40912bc7bdf68b556`.
  - **`check_numbers.py`:** **pass**, 0 failures: 273 of 273 spec numbers on the page; 595 number spans, 187 quoted text spans, 246 no-tag elements, 1,380 appendix fields, 70 notes, 22 elements with `data-needs`, 54 note-need checks, 2,468 other text runs.
  - **`test_check_numbers.py`:** baseline pass; **34 of 34** planted errors in data, spec and pilot copies caught; page baseline pass; **26 of 26** in the page copy caught.
  - **`check_offline.py`:** **pass**: 8 images (sizes match), 10 loaded references (all local), 16 links to local files, 2 licence links (not loaded).
  - **`check_links.py`:** **pass**: 181 in-page links (53 targets); 8 images, each inside a link to its own file; 82 pilot paths on the page (52 distinct, standing for 67 pilot files and folders; 12 short names found in a folder named on the page); 9 "Details in the pilot" lines, 25 places in them checked file by file. Planted errors (a throw-away script in Claude Code's scratchpad, not saved here): **10 of 10** caught (a link to a missing id, a missing pilot path, a heading name, a numbered heading, a review ID, an image linked to another image, a bracket not after a path, a short name in no named folder, a step with no "Issues" line, "rows starting" with no such row). One plant was wrong at first ("Steps 1–10": every one of those steps has an "Issues" line, so the check rightly passed it); it was replaced by "Steps 2–11", which is caught.
  - **`scan_exclusions.py`** over the 22 text files that will be committed: no e-mail address, phone number, eMSPO contact value, personal title outside the search lists, personal name or git e-mail; the personal address that was the git e-mail until this step (searched for separately) is in no file. Hits, each checked: the project name (term line 22) in 15 files: the 12 of the fix round, and `scripts/check_links.py` (default `PILOT_DIR`), `scripts/build_page.py` and `site/index.html` (3 each: title, heading, intro; decision 4); `PROGRESS.md` 5 (with this entry) and `docs/content_inventory.md` 1 "paths" (the text `/Users/` written as a search pattern); `docs/content_inventory.md` 5 "titles" and 8 "eMSPO" (the lists of what is searched for); `scripts/scan_exclusions.py` (its own patterns). No other private term in any file.
- **Pass/fail:** Pass.

### Step 6 — Share

- **Date:** 2026-10-26
- **Go:** Yaseen approved the first commit and the push to `main` (Step 5 close-out decision 5; rule 11). The PI's permission is recorded (2026-10-25; rule 14). The Vercel deploy is not part of this go and was not started.
- **Before the commit** (`git status`: no commits, 30 untracked files, nothing staged):
  - **30 files:** 22 text files (`.gitignore`, `CLAUDE.md`, `LICENSE.md`, `LICENSES/MIT.txt`, `PROGRESS.md`, `README.md`, 4 in `docs/`, 9 in `scripts/`, `site/index.html`, `site/assets/style.css`, `site/assets/manifest.csv`) and the 8 PNGs in `site/assets/`. Sizes: the list after the push, below.
  - **No PDF** (no file ends in `.pdf` or starts with `%PDF`); **no raw data** (nothing from `data/raw/`; no raster, NetCDF, GIS, JSON, spreadsheet or archive file); **no copy of a pilot CSV** (every committed file was compared by size and SHA-256 with every file in the pilot: the only identical files are the 8 PNGs, the approved image copies; the 3 committed CSVs are the spec, the notes and the image manifest); **no `build/` file**; **no absolute path**; **no e-mail address in any file** (the commit e-mail is set only in `.git/config`).
  - Checked against `docs/content_inventory.md`, section e (rule 12): personal data, licences, share-alike terms, project-internal content and statements about named companies as decided there.
- **Commit:** `bb7b84e6e50c798075b07348d0758db41d49f219`, "Initial public release of the NRFR palm oil pilot page", 2026-10-26 00:13:26 +08:00. Author and committer: Yaseen, with the GitHub no-reply address. The message ends with a `Co-Authored-By` line that names Claude (Anthropic's no-reply address), as Claude Code adds to its commits (the Step 5 commit-readiness check, flag 3, noted it).
- **Committed (30 files, 5,041,623 bytes, from `git ls-tree -l`):** `.gitignore` 867; `CLAUDE.md` 16,429; `LICENSE.md` 3,623; `LICENSES/MIT.txt` 1,084; `PROGRESS.md` 99,349; `README.md` 3,956; `docs/caveats.csv` 3,729; `docs/content_inventory.md` 39,075; `docs/number_sources.csv` 69,602; `docs/page_outline.md` 47,030; `scripts/build_page.py` 95,917; `scripts/check_links.py` 10,744; `scripts/check_numbers.py` 44,885; `scripts/check_offline.py` 7,553; `scripts/copy_images.py` 3,250; `scripts/extract.py` 31,299; `scripts/pilot_snapshot.py` 11,331; `scripts/scan_exclusions.py` 6,427; `scripts/test_check_numbers.py` 19,824; `site/index.html` 440,801; `site/assets/style.css` 12,546; `site/assets/manifest.csv` 1,092; 8 PNGs 4,071,210 (`step5_map_forest.png` 1,224,645, `step5_map_palm.png` 310,186, `step8_catchments_map.png` 224,160, `step9_distances.png` 581,116, `step9_loss_2021.png` 547,834, `step9_loss_2022.png` 547,108, `step9_loss_2023.png` 547,164, `step9_zoom_check.png` 88,997).
- **Remote and push:** `git remote add origin https://github.com/yaseen9133ai/nrfr-pilot-site.git` (the repository existed, was public and had no commits: `git ls-remote` listed no refs before the push). `git push -u origin main` at 2026-10-25T16:13:34Z (2026-10-26 00:13 MYT): new branch `main`, no error, no credential prompt (the keychain had a GitHub login). `main` tracks `origin/main`.
- **Check after the push:** `git ls-remote origin`: `HEAD` and `refs/heads/main` = `bb7b84e6e50c798075b07348d0758db41d49f219`, equal to the local `HEAD`.
- **This entry:** written after the push and committed as a second commit, "Record the first commit and push in PROGRESS.md", pushed to `main` the same way (its hash is in `git log`; a file cannot hold the hash of the commit that contains it).
- **Pilot snapshot:** start 2026-10-25T16:00:03Z **no change**; after the push 16:13:51Z **no change** (1,054 files, exit 0). `find -newermt "2026-10-26 00:00"` in the pilot (`.DS_Store` excluded): nothing modified. All scripts ran with `python3 -B`.
- **Pass/fail:** Pass (commit, push, remote check). Step 6 is not finished: the Vercel deploy is left.
- **Hours:** Claude Code about 0.3 h for the Step 5 close-out and this part of Step 6 (active time; estimate from the system clock, about 00:00–00:20 MYT) · Yaseen: to fill.
- **Issues:**
  - The GitHub account name contains the local part of the personal e-mail address the repository used before. The repository URL shows the account name in any case; the address itself is in no file and in no commit.
  - Reading the EU licence cell printed the whole `EU_FSF` row of the pilot's `source_register.csv` into Claude Code's session, including its notes cell, which names 3 listed persons from the public EU list (the search hits that were not the firm). Nothing was written anywhere; the names are in no file of this repository.
- **Open questions for Yaseen:**
  1. **EU licence in section 2:** the table of all registered sources still shows the EU row's licence cell in full ("as recorded", like every other row), including "the CSV distribution is listed as CC BY 4.0". Keep it, or shorten that row to the reuse-notice part as in the credits?
  2. **`README.md` title:** still "Palm oil pilot: from public data to a traceable table" (decision 4 covered the page). Change it to match the page title?
  3. **Vercel deploy:** when Yaseen gives the go (rule 11). The page needs no build step: the output directory is `site/`.
- **End of step:** pilot snapshot `--check` at 2026-10-25T16:13:51Z: **no change** (1,054 files, exit 0). Re-run after writing this entry: see `build/pilot_snapshot_checks.log`.

#### Step 6 close-out — live page check

- **Date:** 2026-10-26
- **Brief (Yaseen):** check the live page (https://nrfr-pilot.vercel.app/; Vercel, root directory `site/`, deploys on push to `main`); fix the EU licence in the sources table; compare the live files with `site/`; run the checks on the live copy; add the live URL; mark Step 6 done; commit and push; after the redeploy, compare again. Decisions recorded in `CLAUDE.md`, "Step 6 close-out decisions".
- **1. EU licence:** the Part A fix (Step 5 close-out decision 1) had been applied locally **to the credits only**: the sources table in section 2 showed every licence cell as recorded, the EU row in full, and this was left as the Step 6 open question 1. So the live page showed "the CSV distribution is listed as CC BY 4.0" in the table, as expected. Now fixed (decision 1): `extract.py` has one list, `LICENCE_PARTS`, of licence cells quoted only in part (`EU_FSF`: "European Commission reuse notice (Decision 2011/833/EU)"), used by both the sources list and the credits; the quote is checked to occur exactly once in the cell (`text in licence: "…"`). The table cell reads "European Commission reuse notice (Decision 2011/833/EU) (the part for the file used: the CSV file, version 1.1)" (`LICENCE_FILE_USED` in `build_page.py`). "listed as CC BY 4.0" is no longer on the page.
- **2. Live vs local, before the fix** (2026-10-25T16:20:44Z, 00:20 MYT; `curl`, read-only, into `build/live/`, git-ignored): `/` and `/index.html` both HTTP 200, the same 440,801 bytes; the 10 files of `site/assets/` HTTP 200, with the expected content types. SHA-256 of all **11 files equal** to `site/` at `0224831` and to the working tree at that time: **0 differences**. The live page was deployed from `0224831` (`main` at the time; its `site/` is the same as in `bb7b84e`, the second commit changed only `PROGRESS.md`).
- **3. Checks on the live copy** (before the fix; `python3 -I -B`): `check_numbers.py --html build/live/index.html`: **pass**, 0 failures, 273 of 273 spec numbers on the page (report in `build/live_check/`). `check_links.py --site build/live`: **pass** (181 in-page links, 8 images each linked to its own file, 82 pilot paths, 25 places in the "Details in the pilot" lines). `check_links.py` got the option `--site` for this (default `site/`); the 10 planted errors of the Step 5 close-out were run again through it: 10 of 10 caught.
- **4. Live URL:** in `README.md` (with how to check a downloaded copy) and in this log (Current status, Steps table). Step 6 marked done.
- **Checks after the fix** (all with `python3 -B`; output in `build/final_checks.txt`):
  - Extraction: 273 of 273 numbers, twice: `build/site_data.json` SHA-256 `e2765a6f068e4ab7210aaf7f2d191d646c666128ff0d7e70eb7de9294ea19b7f` both times.
  - Two builds byte-identical. `site/index.html` 440,933 bytes, SHA-256 `9aba6a7053e5df8e4fda6160fff7d4841c0fdd4fce02d9ff7905738b0574e9f6`; `site/assets/style.css` unchanged (`e1b935b2…`); images and manifest unchanged.
  - `check_numbers.py` **pass**, 0 failures (273 of 273; no-tag elements 246 → 247, the version in the EU row). `test_check_numbers.py`: 34 of 34 and 26 of 26 caught. `check_offline.py` **pass**. `check_links.py` **pass**.
- **Files changed:** `CLAUDE.md`, `PROGRESS.md`, `README.md`, `docs/content_inventory.md`, `scripts/extract.py`, `scripts/build_page.py`, `scripts/check_links.py`, `site/index.html`.
- **5. Commit, push and the check after the redeploy:** below.
