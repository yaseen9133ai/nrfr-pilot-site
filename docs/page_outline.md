# Page outline (Step 2)

Written 2026-10-25 by Claude Code for Yaseen (Research Assistant), from read-only reads of the pilot (`../nrfr-pilot`). No HTML and no extraction script were written. Nothing was computed except counts and sums of existing columns that the pilot itself states (listed in `docs/number_sources.csv`).

Status: **waiting for Yaseen's approval.** Proposals are marked "Proposal"; the open questions are at the end.

## How to read this outline

- **Paths:** pilot paths are relative to the pilot folder. On the page they appear as plain text, labelled "Pilot folder (not published)" (decided 2026-10-25).
- **Numbers:** every number planned for the page has one row in `docs/number_sources.csv` (291 rows), with its source file, row key and column, and the value as read on 2026-10-25. The outline names numbers in words and points to that file. A read-only check in Claude Code's scratchpad found all 291 expected values in their sources (see `PROGRESS.md`, Step 2).
- **Decisions applied** (`CLAUDE.md`, Public-release decisions):
  - "Yaseen (Research Assistant)";
  - "palm oil pilot", never the project's name;
  - a neutral purpose (project-internal content is never published);
  - the forest-loss caveat next to every forest-loss number;
  - UML points credited with "no licence stated";
  - "CC BY-SA 4.0" next to ENCORE content;
  - neutral, sourced wording about the 3 companies.

## Writing rules for the page

- **Plain words.** Short sentences. A technical term is explained the first time it appears, and it is in the glossary.
- **The pilot's own terms** for every result, gap and weak point: "built", "built with flags", "gap", "missing", "not checked", "firm-reported". Nothing is softened or made stronger.
- **Neutral about the firms.**
  - No ranking and no sorting by value. Firms always appear in the pilot's order: SOP, Ta Ann, SPB.
  - No colour scale that suggests good or bad.
  - No totals or averages across firms (the pilot computes none).
  - Never "clean", "compliant", "best" or "worst".
- **Missing stays missing.** An empty value is shown as "missing" with the pilot's reason, never as 0 or a dash without words.
- **Every section ends with a "Where the details are" line:** the pilot paths, as plain text.
- **Review IDs** (R0xx) in small print only (Proposal; open question 16).

## Page frame (top and bottom)

- **Title (Proposal):** "Palm oil pilot: from public data to a traceable table".
- **Byline:** Yaseen (Research Assistant). Built from the pilot's files with Claude Code.
- **Status line:** "The pilot's findings report (dated …) is waiting for a decision: scale up, change the plan, or stop." The date is tagged (number_sources section 0).
- **At a glance** (one row of short facts, all tagged): firms, mills, years, features, values traced, grid cells.
- **Contents:** links to the 10 sections, the glossary and the credits (these are links inside the page, not external).
- **Footer:**
  - credits for every source (`docs/content_inventory.md`, section b), including:
    - "© OpenStreetMap contributors, ODbL";
    - the UML credit with "no licence stated";
    - the ENCORE citation with "CC BY-SA 4.0";
    - the CBP sentence "This product uses U.S. Customs and Border Protection data, but is not endorsed by CBP."
  - the page's licence: text CC BY 4.0, ENCORE parts CC BY-SA 4.0, scripts MIT (`LICENSE.md`);
  - "This page adds no data or analysis to the pilot."

## The 10 sections

### 1. What we did

- **Message:** The pilot tested, once and on a small scale, whether data about palm oil growers can be collected from public sources, built into tables, and traced back to where every value came from.
- **Content:**
  - **The question:** can the whole chain be built once, from raw public sources to a small table, with a record for every value? Success, in the pilot's terms, means a traceable pipeline that can be re-run, even where a feature cannot be built, as long as the gap is recorded.
  - **The scope:**
    - 3 listed growers: Sarawak Oil Palms Berhad (SOP), Ta Ann Holdings Berhad (Ta Ann) and Sarawak Plantation Berhad (SPB);
    - their 12 palm oil mills (SOP 7, Ta Ann 3, SPB 2);
    - one region, the state of Sarawak in Malaysia;
    - the years 2021–2023.
  - **How the firms were chosen:** Sarawak has five listed growers with all their mills in the state. All five were compared on data availability, not name recognition, and 3 were chosen.
  - **What was measured:** 8 features in 6 families: geospatial, climate, dependency on nature, operational, regulatory, financial (section 4).
  - **How it was run:** 10 steps, each checked and approved before the next one started.
  - **What came out:**
    - a 9-row table (3 firms × 3 years);
    - a 3-row table of values that do not change by year;
    - a 1 km grid of Sarawak;
    - an evidence record for each of the 207 values.
  - **The short answer:** 6 of the 8 features were built (1 without flags, 5 with flags). 2 are gaps. The data turned out to be easier to collect than to use (section 8).
- **Images:** none. The pipeline diagram (section 3) is the first picture.
- **Caveats to show:**
  - This is a test of the method, not a dataset for use. 3 firms were chosen because their data was available; they do not stand for the industry.
  - The findings are waiting for a decision (section 10).
- **Where the details are:** `docs/PILOT_PLAN.md` (Scope, Features, Steps, Rules and success only), `reports/step3_candidates.md`, `reports/step10_findings.md` §1, `data/interim/firm1_mills.csv`, `firm2_mills.csv`, `firm3_mills.csv`, `progress_log.md` (Current status).
- **Numbers:** number_sources section "1 What we did" (17 rows).

### 2. Sources

- **Message:** Everything came from public sources, and each one was registered with its link, version, licence and download date before it was used.
- **Content:**
  - **The register:** 34 sources:
    - 24 downloaded;
    - 1 could not be obtained (the peat map);
    - 1 used only for checks on its website (Global Forest Watch);
    - 8 belonging to the 2 candidate firms that were not chosen.
  - **What each source gave, in plain words** (one table, Proposal):
    - **forest:** Hansen Global Forest Change (tree cover and yearly loss, from satellite);
    - **rainfall:** CHIRPS (monthly rainfall);
    - **peat:** CIFOR Global Wetlands (not obtained);
    - **dependency on nature:** ENCORE ratings;
    - **certification:** eMSPO certified-entity list, RSPO registry, and the firms' annual reports;
    - **yield and debt:** 9 annual reports (3 firms × 3 years);
    - **mill lists:** the firms' websites;
    - **import bans and sanctions:** US CBP Withhold Release Orders list and EU consolidated sanctions list;
    - **region boundary:** geoBoundaries;
    - **roads:** OpenStreetMap;
    - **map context only:** Descals et al. 2024 oil palm map;
    - **mill points used to draw catchments:** Universal Mill List;
    - **checks only:** Copernicus Sentinel-2 images and the Global Forest Watch map.
  - **Licence column:** as recorded in `source_register.csv`, including "not stated" (eMSPO, RSPO, UML) and "not checked" (annual reports, firm websites, Sentinel-2).
  - **The download log:**
    - 602 records;
    - 174 files kept (1 of them only the file header), about 1.8 GB, in 24 source folders;
    - 396 monthly rainfall files clipped to Sarawak and then deleted (they were too large to keep);
    - 32 small satellite-image reads.
  - **Not on this page:** the raw files themselves, annual-report pages and personal data are not published here.
- **Images:** Proposal, optional: `reports/step5_maps/step5_map_palm.png` (oil palm extent 2021 with SOP mills).
  - Caption: Descals et al. 2024, v1.2, DOI, CC BY 4.0 (on the image); boundary credit "geoBoundaries, © OpenStreetMap contributors, ODbL".
  - Caption must also say: "Used only for maps. The palm layer covers 80.0% of Sarawak (hatched areas have no data). Shows SOP mills only; Sepakau at the firm-map point that was later replaced (R028)."
- **Caveats to show:**
  - Licences not checked for the annual reports, firm websites and Sentinel-2. No licence stated for eMSPO, RSPO and the UML; they are used with credit.
  - The CIFOR peat map allows research and educational use only (named only as the gap).
- **Where the details are:** `source_register.csv`, `data/raw_files.csv`, `reports/step5_raw_data.md`, `reports/step10_findings.md` §2.
- **Numbers:** section "2 Sources" (14 rows). Versions, DOIs and access dates for the credits: section "0 Header and credits" (11 rows).

### 3. Raw data to final CSVs, step by step

- **Message:** The data moved through four layers, from raw downloads to two final tables, and every run of the scripts gave the same files.
- **Content:**
  - **The pipeline diagram** (plan below), then four short steps:
    1. **Raw downloads** (`data/raw/`, logged in `data/raw_files.csv`): saved once, never edited.
    2. **Clips and extracts** (`data/interim/`):
       - satellite and rainfall layers cut to Sarawak: tree cover, loss year, palm extent (22 tiles), monthly rainfall 1991–2023 (396 monthly layers, no missing months);
       - the 12-mill tables;
       - figures typed from the annual reports, with their page numbers;
       - certificate records;
       - sanctions searches;
       - the ENCORE extract;
       - the roads.
    3. **Results per firm** (`data/processed/firm1_…`, `firm2_…`, `firm3_…`): forest loss by mill, rainfall by mill, certification by mill and year, yield, debt-to-equity, sanctions search. Then one firm-year table and one static table per firm.
    4. **Final tables:**
       - `pilot_firm_year.csv`: 9 rows × 9 columns. 54 values, of which 9 are missing and 45 filled;
       - `pilot_static.csv`: 3 rows × 53 columns. 153 values, of which 3 are missing;
       - `evidence.csv`: 207 rows × 19 columns;
       - the grid (section 5).
  - **How missing values are written:** as an empty cell, never 0, and each has a recorded reason. "NO_DEPENDENCY" is an ENCORE rating ("no dependency"), not a missing value.
  - **Why two tables:** values that do not change by year (peat, ENCORE) are kept apart, so one value does not look like three yearly ones.
  - **The tools:** 33 Python scripts, 4 runner scripts and 2 package lists.
    - Rebuilding the firm tables gave 104 identical outputs in 3 builds.
    - Rebuilding the grid gave 10 identical outputs in 3 builds.
  - **The records kept alongside:**
    - 9 method cards;
    - a feature dictionary (23 rows);
    - a check register (20 rows per firm);
    - a review queue of 58 decisions: 56 decided, 2 open. (Step 5 close-out: the page shows the 58 and the 56 only; the "2 open" count is dropped.)
- **Images:** the pipeline diagram, drawn for the page (inline SVG in `site/index.html`, no external files). It shows only file and step names; any count on it is tagged.
- **Caveats to show:**
  - The raw files are not published.
  - The grid has no evidence rows; it is documented by its dictionary rows and method card (R053).
  - The script count is the report's (33); the scripts folder now holds 34, because the report's own check script was added after the count (open question 7).
- **Where the details are:** `data/processed/README_dataset.md`, `scripts/step8_run_all.sh`, `scripts/step9_run_all.sh`, `reports/step6_checksheet.md`, `reports/step8_checksheet.md`, `progress_log.md` (Steps 4–9), `feature_dictionary.csv`.
- **Numbers:** section "3 Raw to final CSVs" (28 rows).

### 4. The 8 features

- **Message:** Eight measures describe each firm. Six could be built, and each comes with the pilot's own warning about what it can and cannot show.
- **Content:**
  - **Mill catchments first** (needed for forest loss and rainfall):
    - each mill gets the land that is closer to it than to any other mill (a tessellation);
    - the map is cut at the Sarawak border;
    - it is drawn from 90 mill points: the firms' 12 mills and 78 points from the Universal Mill List;
    - a firm's catchments are merged into one area.
  - **One card per feature**, in the plan's order. Each card gives: family, what it measures, source, how the firm-year value is made, how it was checked, verdict, main warning.
    1. **Forest loss** (geospatial; built with flags).
       - What it is: hectares of tree-cover loss each year in the firm's merged catchments, where "forest" means more than 30% tree cover in 2000.
       - Check: 18 of 18 yearly values matched Global Forest Watch at its 2 significant figures (differences −1.5% to +1.8%), for 2 cells per firm; satellite patches: 6 pass, 2 partly plausible.
    2. **Peat overlap** (geospatial; gap). The share of the catchment on peat. The peat map could not be downloaded; no substitute was used.
    3. **Rainfall anomaly** (climate; built).
       - What it is: each year's rainfall minus the 1991–2020 average, in mm, averaged over the firm's mills.
       - Check: 0 of 396 mill-years off by more than 2 mm in an independent recomputation.
    4. **ENCORE dependency ratings** (dependency; built with flags).
       - What it is: 50 ratings (25 ecosystem services × 2 activities: growing perennial crops; making vegetable oils), from very high to very low or "no dependency".
       - Check: the two ENCORE files agree for 50/50 ratings; 150 values pass. Marked **CC BY-SA 4.0** with the citation.
    5. **Certification** (operational; built with flags).
       - What it is: the share of the firm's mills certified (MSPO or RSPO) on 31 December of each year.
       - Check: eMSPO records equal the live site (63/63 and 45/45 fields); 9/9 pass.
    6. **FFB yield** (operational; built with flags).
       - What it is: tonnes of fresh fruit bunches per hectare, exactly as each annual report prints it.
       - Check: 9/9 pass; 1 restatement found.
    7. **Import bans and sanctions** (regulatory; gap). Searches of the current US and EU lists found no match, but the lists do not show 2021–2023, so the count is missing.
    8. **Debt-to-equity** (financial; built with flags).
       - What it is: borrowings divided by total equity, for the whole group, from each year's annual report.
       - Check: every non-zero figure found on its page (63/63, 60/60, 46/46); 9/9 pass.
- **Images:** `reports/step8_checks/step8_catchments_map.png`: the catchments of all 12 firm mills in the shared tessellation of 90 points, with areas in km².
  - Caption: "Mill points: firms' published lists and eMSPO; other points from the Universal Mill List (Rainforest Alliance; WRI/GFW), July 2026 file, unverified, **no licence stated**. Boundary: geoBoundaries, © OpenStreetMap contributors, ODbL."
  - Some labels overlap. The km² labels on the image cannot be tagged (open question 5).
- **Caveats to show** (each on its card):
  - **Forest loss:** "Tree-cover loss from any cause in the catchment area, including replanting and logging. It is not land cleared by the firm." In addition: areas come from pixel counts, which the Hansen documentation advises against for definitive area estimates.
  - **ENCORE:** the same 50 ratings for all 3 firms (an activity-level proxy, not firm data); May 2026 version, not 2021–2023.
  - **Certification:** 100% in every firm-year only because the firms' own statements fill 20 of the 36 mill-years.
  - **FFB yield:** units and hectare bases differ between firms, so yields cannot be compared between firms (R048).
  - **Import bans and sanctions:** "missing" does not mean zero. The pilot found no match in the current lists; 2021–2023 was not checked.
  - **Debt-to-equity:** whole-group figures, including non-palm business (R007).
  - **Peat:** missing for all 3 firms; no substitute.
- **Where the details are:** `feature_dictionary.csv`, and one method card per feature in `docs/methods/`: `forest_loss.md`, `peat_overlap.md`, `rainfall_anomaly.md`, `encore.md`, `certification.md`, `ffb_yield.md`, `wro_sanctions.md`, `debt_to_equity.md`. Also `reports/step10_findings.md` §1 and §3.
- **Numbers:** section "4 The 8 features" (26 rows).

### 5. Grid

- **Message:** A grid of 1 km squares covers all of Sarawak, with yearly forest loss and distances to the nearest mill and road in each square, and its total matches the state-wide total.
- **Content:**
  - **What it is:** 125,982 squares of 1 km. 4,111 of them are edge squares, cut by the border. Together they cover 123,769.32 km². Each square has 15 columns.
  - **What each square holds:** forest loss 2021, 2022 and 2023 (ha); distance to the nearest mill point; distance to the nearest road (km); peat (empty).
  - **The check:** forest loss summed over all squares equals the Sarawak total computed separately, each year. One small table: year, Sarawak total, grid total, difference. The differences are rounding only. Result: pass.
  - **Roads used:** OpenStreetMap, 152,089 road sections, 76,361.9 km, 20 road types. Tracks are 46% of that length.
  - **Distances:**
    - to the nearest mill point: median 30.2 km, at most 153.5 km;
    - to the nearest road: median 0.84 km, at most 28.0 km.
  - **Reproducible:** 3 builds gave identical files.
- **Images:**
  - `reports/step9_maps/step9_loss_2021.png`, `step9_loss_2022.png`, `step9_loss_2023.png`: forest loss per square, with mills and roads. Proposal: show 2021 large and the other two small.
  - `reports/step9_maps/step9_distances.png`: distance to mill and to road.
  - Optional: `reports/step9_maps/step9_zoom_check.png` (squares against the satellite pixels they were built from).
  - Caption credits on all of them: Hansen/UMD/Google/USGS/NASA (CC BY 4.0); "© OpenStreetMap contributors, ODbL"; geoBoundaries; Universal Mill List points with "no licence stated". The images themselves carry no OSM or geoBoundaries credit.
- **Caveats to show:**
  - **Forest loss** (next to every loss figure, wording adapted for the grid): "Tree-cover loss from any cause in Sarawak, including replanting and logging. It is not land cleared by any one firm."
  - **Roads:** an OpenStreetMap snapshot of 22 October 2026, not 2021–2023. Tracks are included.
  - **Borders:** roads and mills outside Sarawak are not used, so distances near the borders can be too long.
  - **Mill points:** for 93,588 squares (74%), the nearest mill point is an unverified UML point.
  - **Peat:** empty in all 125,982 squares.
- **Where the details are:** `reports/step9_grid.md`, `docs/methods/regional_grid.md`, `reports/step9_checks/grid_vs_sarawak_loss.csv`, `data/interim/osm_roads_sarawak_tag_counts.csv`, `feature_dictionary.csv` (rows starting "Grid:").
- **Numbers:** section "5 Grid" (30 rows).

### 6. Evidence trail and a worked example

- **Message:** Every one of the 207 values in the two tables has an evidence row that leads to its source page, method, script and check, and one value is followed here link by link.
- **Content:**
  - **What an evidence row holds** (19 columns, in plain words): the value, the source and the exact place in it (page, table or map layer), the unit, the date it refers to, the area it covers, the method card, the script, how it was checked, the result, who checked it and when, and a note.
  - **Results:**
    - 195 pass, 0 fail;
    - 12 not checked: the 12 missing values (9 import-ban/sanctions values, 3 peat values);
    - all 195 checks were done by Claude Code.
  - **Worked example:** SOP, debt-to-equity, 2022 = 0.2207, as a 7-link chain:
    1. The value in the table.
    2. Its evidence row: source the SOP Annual Report 2022; reference date 2022-12-31; whole group.
    3. The source: registered, downloaded at the logged time, with its file fingerprint recomputed and unchanged.
    4. The pages: the balance sheet (PDF page 151, printed 149) shows loans and borrowings of 446,125 (non-current) and 314,829 (current) and total equity of 3,447,314 (RM'000). The borrowings note (PDF page 215, printed 213) gives the line items.
    5. The method card: hire purchase (1,875) counts as debt; lease liabilities (1,550) are left out; 760,954 ÷ 3,447,314 = 0.220738, shown as 0.2207.
    6. The scripts that compute and record it.
    7. The check: pass, by Claude Code, 2026-10-24. The trace was re-run on 2026-10-24 and passed again.
  - **Same chain for other kinds of value:** map and rainfall values trace to a map layer and a result row; certification to the eMSPO record or the annual-report statement; missing values to a row giving the reason.
- **Images:** none required; the chain is drawn as a short vertical list with arrows (HTML/CSS only). Optional: `reports/step5_maps/step5_R028_sepakau_imagery.png`, as "one check made visible" (open question 10: it has internal labels and needs the Copernicus wording).
- **Caveats to show:**
  - All checks were self-checks by Claude Code. Yaseen's manual checks were waived, so no value was checked independently.
  - The annual report itself is not published here. It is cited by title, year and page.
- **Where the details are:** `evidence.csv`, `reports/step10_findings.md` §5, `reports/step7_trace_example.md`, `reports/step10_checks/step7_trace_rerun_2026-10-24.txt`, `data/processed/firm1_debt_to_equity.csv`, `docs/methods/debt_to_equity.md`, `source_register.csv` (AR_SOP_2022).
- **Numbers:** section "6 Evidence trail" (25 rows).

### 7. Results

- **Message:** The tables hold the values the pilot could build for 2021–2023, but several of them cannot be compared between firms, so they are shown with their warnings and not as a ranking.
- **Content** (Proposal: one small table per feature, rows = firms in pilot order, columns = 2021, 2022, 2023, each table with its warning directly above it):
  - **Forest loss (ha):** 9 values. Each table cell carries a marker linked to the caveat, plus the largest catchment cell's share of the firm's area and of that year's loss, from the evidence notes (the pilot's flag, R040).
  - **Rainfall anomaly (mm):** 9 values, with + or − (built without a flag).
  - **Certification (%):** 9 values, all 100.0. Next to them: firm-reported mill-years SOP 10 of 21, Ta Ann 4 of 9, SPB 6 of 6 (20 of 36 in all).
  - **FFB yield:** 9 values, each with its unit as printed (mt/ha, Mt/WHa). Ta Ann 2022 flagged: "restated in AR 2023: 16.82".
  - **Debt-to-equity:** 9 values.
  - **Import bans and sanctions:** 9 cells, each shown as "missing: not checked for 2021–2023 (current lists only); current lists: no match".
  - **Static table:**
    - peat overlap: "missing" for all 3 firms, with the reason;
    - ENCORE: the same 50 ratings for all 3 firms, 18 of them "no dependency". Proposal: one table of the 50 ratings (25 services × 2 activities) under a "CC BY-SA 4.0" label and the ENCORE citation (open question 12).
- **Images:** `reports/step5_maps/step5_map_forest.png`: tree cover in 2000 and loss years over Sarawak, with the 7 SOP mills.
  - Caption: Hansen credit (on the image); geoBoundaries / OSM ODbL credit; forest-loss caveat; "Shows SOP mills only; Sepakau at the firm-map point that was later replaced (R028)."
- **Caveats to show:**
  - **Forest loss:** the decision 5 wording, next to the table and on each value.
  - **FFB yield:** not comparable between firms (R048). Ta Ann's 2022 and 2023 yields are not comparable with each other (R046).
  - **Certification:** firm-reported, group-level statements (R038).
  - **Debt-to-equity:** whole group (R007).
  - **ENCORE:** gives no difference between firms (R036).
  - **Linked firms:** Ta Ann owns part of SPB, so 2 of the 3 firms are linked (section 8).
- **Where the details are:** `data/processed/pilot_firm_year.csv`, `data/processed/pilot_static.csv`, `evidence.csv`, `data/processed/README_dataset.md`, `data/processed/firm1_certification_firm_year.csv` (and `firm2_`, `firm3_`), `data/processed/firm1_ffb_yield.csv` (and `firm2_`, `firm3_`), `data/processed/firm1_forest_loss_summary.csv` (and `firm2_`, `firm3_`).
- **Numbers:** section "7 Results" (66 rows: the 45 filled values plus flags).

### 8. Gaps and findings

- **Message:** Two features could not be built, and the pilot records 16 weak points in all. None of them was filled, estimated or worked around.
- **Content:** the 16 items of the findings report, in plain words, grouped. Each item has one line on what it means, with the review ID in small print.
  - **Data that could not be had:**
    - **Peat map:** the provider's portal did not respond. Peat is missing for all 3 firms and all grid squares.
    - **Sanctions history:** the official lists hold only current entries, so 2021–2023 is missing in all 9 firm-years.
    - **MSPO history:** the eMSPO history service failed (3 mills tried), so earlier certificate periods could not be seen.
  - **Weak evidence:**
    - **Certification:** relies on the firms' own statements for 20 of the 36 mill-years.
    - **Self-checks only:** all 195 checked values were checked by Claude Code.
    - **Limited forest-loss comparison:** Global Forest Watch covers 2 cells per firm (6 of 12 catchments), at 2 significant figures; the strict-threshold question changes at most 0.15 ha.
    - **Unverified mill points:** 78 of the 90 points come from the Universal Mill List, which is unverified. They set the catchment edges, and they are the nearest point for 93,588 of 125,982 squares (74%).
  - **Things that cannot be compared:**
    - **Yield:** units differ. SOP's printed yield matches production ÷ mature area only for 2021 (2022: 14.68 vs 14.50; 2023: 15.31 vs 15.02).
    - **Ta Ann 2022 yield:** 16.02 in AR 2022, but 16.82 in AR 2023 with the same production (703,625 mt).
    - **Borrowings:** line items have different names across firms. Without hire purchase, SOP's ratio would be 0.3443 / 0.2202 / 0.2301.
    - **ENCORE:** all 3 firms get the same 50 ratings.
    - **Linked firms:** Ta Ann owns 29.41% of SPB (30.39% in 2021).
  - **Limits of the method:**
    - **Forest loss counts more than clearing:** 2 of the 8 satellite patches showed logging roads and broken canopy, not clearing.
    - **One very large cell:** Metanik's catchment is 20,079 km², 76% of SOP's merged area (26,530 km²). It gives 61% / 63% / 52% of SOP's loss in 2021–2023.
    - **Roads:** a 2026 snapshot (22 October 2026); tracks are 46% of the length; borders not crossed.
  - **Licences not checked:** the 9 annual reports, Sentinel-2 and the Global Forest Watch site terms. No licence is stated for RSPO, eMSPO and the UML.
  - **Other points** (item 16): the palm map covers 80.0% of Sarawak and is used only for pictures; mill points and roads are 2026 positions.
- **Images:** Proposal, optional: `reports/step8_checks/loss_patches_imagery_firm2.png` (Ta Ann loss patches on Sentinel-2, before and after; viewed in Step 1). Alternative: `reports/step6_checks/step6_loss_patches_imagery.png` (SOP, 4.9 MB, not viewed). Either needs the Copernicus credit wording (open question 11) and the forest-loss caveat.
- **Caveats to show:**
  - These are the pilot's own findings, not new analysis.
  - The forest-loss caveat sits next to the Metanik shares.
- **Where the details are:** `reports/step10_findings.md` §4, `review_queue.csv`, `docs/methods/*.md` ("Known limitations"), `progress_log.md` (Issues of Steps 2–9).
- **Numbers:** section "8 Gaps and findings" (28 rows).

### 9. Hours and full-build estimate

_Removed from the page at the Step 4 close-out (`CLAUDE.md`, Step 4 decision 10); section 10 below became section 9. Kept here as the Step 2 record._

- **Message:** Steps 1–9 took 13.5 logged hours, under the plan's 27–32 hour limit, but most of the figures are unconfirmed estimates.
- **Content:**
  - **Hours table:** steps 1–9, with Claude Code, Yaseen (Research Assistant) and step totals. Totals: 5.2 + 8.3 = 13.5 h, which is 42–50% of the limit.
  - **Step 10:** Claude Code 0.2 h; Yaseen's time is "to fill". Total so far: 13.7 h plus Yaseen's step 10 time.
  - **How time was counted:** Claude Code's step 5 figure is active time, confirmed (2.7 h wall-clock, of which 0.6 h active). The others are estimates, never confirmed (1 of 9 confirmed).
  - **Estimate for a full build (from the findings report):**
    - one-off, region-wide work 6.7–7.8 h, and per-firm work 5.7–6.8 h for the 3 firms;
    - about 0.9–2.3 h per extra firm in a region already built;
    - about 3.0–7.2 h per extra region (region-wide work only);
    - illustration only: 10 firms 19.8–29.6 h, 30 firms 37.8–75.6 h.
  - **What these assume, in short:** scripts reused unchanged; firms like the pilot firms; manual checks still waived; no new method decisions.
  - **What was not measured:** firms that would break those assumptions (step 3 found two: a June year-end, unnamed mills, unreadable report text). Also whether 10 or 30 suitable firms exist in one region: step 3 found 5 listed growers in Sarawak and recommended 3.
- **Images:** none.
- **Caveats to show:**
  - Only 1 of Claude Code's 9 step figures was confirmed (R058, open).
  - Yaseen's step 10 hours are not yet filled in.
  - The 10- and 30-firm figures are an illustration, not a plan or a recommendation.
  - They include no fix for the gaps and none of the changes in section 10.
- **Where the details are:** `reports/step10_findings.md` §6 and §7, `progress_log.md` (Hours of each step; Current status), `review_queue.csv` (R011, R058).
- **Numbers:** section "9 Hours and estimate" (44 rows).

### 10. Next decisions

- **Message:** The pilot ends with a decision that has not been made yet: scale up, change the plan, or stop.
- **Content:**
  - **The 3 options**, listed without a recommendation, as in the findings report:
    1. **Scale up:** a full build with the current plan and methods, with the gaps kept as gaps.
    2. **Change the plan:** change sources, checks, rules, features or scope first.
    3. **Stop:** keep the pilot's outputs as the record.

    Options can be combined.
  - **What a full build would need to change** (listed, not decided; plain-word version of §7.5):
    - a reachable peat source;
    - roads matched to each year;
    - full-precision forest-loss comparisons;
    - a source for past sanctions and import bans;
    - MSPO history;
    - a rule for comparing yields;
    - independent checks;
    - verified mill points;
    - a rule for linked firms;
    - licence checks;
    - a border rule;
    - firm screening;
    - the approval process for many firms;
    - confirmed time records.
  - **Open items:** 2 (the decision itself, R057; unconfirmed hours, R058).
- **Images:** none.
- **Caveats to show:** this page takes no side among the options.
- **Where the details are:** `reports/step10_findings.md` §7.5 and §8, `review_queue.csv` (R057, R058), `progress_log.md` (Current status).
- **Numbers:** section "10 Next decisions" (2 rows).

If Yaseen decides R057 or fills in the hours in the pilot, sections 9 and 10 and the status line change. The extraction (Step 3) reads them from the pilot's files, and the snapshot check stops the steps until a new baseline is approved.

## Pipeline diagram plan

Purpose: one picture of how raw public sources became the final files. It is drawn for the page as inline SVG (no external files, works offline). Below 600 px wide it stacks top to bottom. A text version (an ordered list) sits beside it for screen readers.

```
LAYER 1: RAW SOURCES          LAYER 2: CLIPS & EXTRACTS       LAYER 3: PER FIRM              LAYER 4: FINAL
(data/raw/, raw_files.csv)    (data/interim/)                 (data/processed/firmN_…)       (data/processed/, root)

Hansen forest ───────────────▶ Sarawak forest clips ─────────▶ forest loss by mill ──┐
CHIRPS rainfall ─────────────▶ monthly rainfall clips ───────▶ rainfall by mill ─────┤
geoBoundaries boundary ──────▶ Sarawak boundary ──┐                                   │
Firm mill lists + eMSPO ─────▶ 12-mill tables ────┼─▶ catchments (90 points) ─────────┤
Universal Mill List ─────────▶ UML points ────────┘   (feeds forest + rainfall)       │
eMSPO + RSPO + reports ──────▶ certificate records ──────────▶ certification ────────┤
9 annual reports ────────────▶ typed figures + page index ───▶ yield, debt-to-equity ┼─▶ firmN_firm_year ─┐
CBP list + EU list ──────────▶ sanctions searches ───────────▶ sanctions (missing) ──┘                    ├─▶ pilot_firm_year.csv (9 rows)
ENCORE ──────────────────────▶ ENCORE extract ───────────────────────────────────────────▶ firmN_static ──┤
CIFOR peat  - - - - - - - - -▶ (not obtained: gap) - - - - - - - - - - - - - - - - - - - -▶ peat (missing) ┴─▶ pilot_static.csv (3 rows)
OpenStreetMap roads ─────────▶ Sarawak roads ──────┐
Hansen clips + boundary + mill points ─────────────┴──────────────────────────────────────────────────────▶ sarawak_grid_1km (125,982 squares)

Checks only (dotted): Sentinel-2 images, Global Forest Watch map ·····▶ check files (reports/)
Palm map (Descals) ·····▶ map pictures only

Alongside the final tables: evidence.csv (207 rows, one per value)
   ├── points to source_register.csv (each source)
   ├── points to docs/methods/ (one method card per feature)
   ├── points to scripts/ (the script that made the value)
   └── points to the check result (check registers, check sheets)
```

- **Boxes:** one per source (layer 1) and one per file group (layers 2–4). Final files are drawn larger.
- **Arrows:** solid = data flow; dashed = a gap (peat; sanctions history); dotted = used only for checks or pictures.
- **Labels on arrows** (small): the step that does it: step 5 (save and clip), step 6 (features), step 7 (firm tables and evidence), step 8 (all 3 firms combined), step 9 (grid).
- **Evidence links:** thin lines from `evidence.csv` to both final tables ("one row per value") and to the register, method cards, scripts and checks.
- **Counts on the diagram:** 9 rows, 3 rows, 207 rows, 125,982 squares, 90 points, 12 mills. Each is tagged (sections 1, 3, 4, 5 of `docs/number_sources.csv`).
- **Colours:** one neutral colour for data, one for gaps; colour is never the only signal (dashes and labels too).

## Glossary

| Term | Plain meaning |
| --- | --- |
| Catchment | The land that belongs to a mill on the map: every place closer to that mill than to any other mill. A firm's catchment is all its mills' catchments merged. |
| Tessellation (Voronoi) | The way the catchments are drawn: the map is split into areas, one per mill point, each holding the places nearest to that point. |
| Mill point | The map location of a palm oil mill. 12 come from the firms and eMSPO; the others come from the Universal Mill List. |
| Universal Mill List (UML) | A public list of palm oil mill locations (Rainforest Alliance; WRI/GFW). Unverified; no licence stated. |
| Feature | One measure in the table, for example forest loss or debt-to-equity. |
| Family | A group of features: geospatial, climate, dependency, operational, regulatory, financial. |
| Firm-year | One firm in one year: one row of the main table. |
| Static value | A value that does not change by year (peat overlap, ENCORE). Kept in its own table. |
| Evidence row | One line in `evidence.csv` for one value: where it came from, how it was made, how it was checked. |
| Source tag | On this page: the file, row and column in the pilot where a number comes from. |
| Gap | A feature that could not be built. Recorded, not filled. |
| Flag | A warning the pilot attached to a value. |
| Missing | An empty value with a recorded reason. Not zero. |
| Not checked | The check status of a missing value. |
| Self-check | A check done by the same party that built the value (here, Claude Code). |
| Tree-cover loss (Hansen) | Satellite-detected loss of tree cover from any cause, including clearing, replanting and logging. |
| Rainfall anomaly | A year's rainfall minus the 1991–2020 average for the same place, in mm. |
| ENCORE rating | How much an activity depends on a part of nature (very high to very low, or no dependency). |
| NO_DEPENDENCY | ENCORE's "N/A": the activity does not depend on that service. A rating, not a missing value. |
| MSPO / RSPO / eMSPO | Palm oil certification schemes (Malaysian Sustainable Palm Oil; Roundtable on Sustainable Palm Oil) and MSPO's online list of certified sites. |
| Mill-year | One mill in one year. |
| Firm-reported | Based on the firm's own statement in its annual report, not on a certificate record. |
| FFB yield | Fresh fruit bunches harvested per hectare, as the firm reports it. |
| Debt-to-equity | Borrowings divided by total equity, for the whole group. |
| Restatement | A figure that a later annual report prints differently for the same year. |
| WRO | Withhold Release Order: a US order that stops certain imports. |
| Grid square (cell) / edge square | One 1 km square of the grid; an edge square is cut by the Sarawak border. |
| OpenStreetMap (OSM) | A public map made by volunteers, used here for roads. |

## Data the page will need (for Step 3)

The 291 planned numbers come from 21 pilot files: `reports/step10_findings.md` (127 rows), `data/processed/pilot_firm_year.csv` (53), `evidence.csv` (30), `source_register.csv` (14), `reports/step9_checks/grid_vs_sarawak_loss.csv` (12), `feature_dictionary.csv` (8), `data/raw_files.csv` (7), `reports/step9_grid.md` (6), `docs/methods/regional_grid.md` (6), `data/processed/README_dataset.md` (5), `data/processed/firm1_debt_to_equity.csv` (5), the 3 certification firm-year files (8), `docs/PILOT_PLAN.md` (2), `data/processed/pilot_static.csv` (2), the 3 mill tables (4), `reports/step3_candidates.md` (1), `data/interim/osm_roads_sarawak_tag_counts.csv` (1).

Text that is not a number (firm and mill names, units, verdicts, notes, licences) comes from the same files. Copies of pilot files go only into `build/` (rule 13).

### Syntax of `docs/number_sources.csv`

> **Updated in Step 3 (2026-10-25).** The file is now the spec for `scripts/extract.py`: 302 rows, with the new columns `id`, `format`, `unit`, `caveats` and `tag_required`. Markdown locators name a block (`row=`, `bullet=`, `paragraph=`, `paragraph <n>`, `heading`, `table`, `numbered list`), and a quote in a table row names its column (`text in <column>: "<quote>"`). Rows were moved to a CSV cell where one holds the same number (Step 2 decision 3). The full syntax is in the docstring of `scripts/extract.py`; caveat wording is in `docs/caveats.csv`; the changes are listed in `PROGRESS.md`, Step 3. The table below is the Step 2 version.

| Column | Meaning |
| --- | --- |
| `section` | Page section (0 = header and credits) |
| `label` | What the number is, in words |
| `source_file` | Pilot path; `firm{1,2,3}` means the three files together |
| `row_key` | CSV: `column=value` conditions joined by `; ` (`^=` starts with, with `\|` for "or"; `$=` ends with; `!=` with nothing after it means "not empty"; `!^=` does not start with); `*` = all rows; `header` = the header row. Markdown: the heading, then `\| row=<first cell>` for a table row or `\| table` for the whole table (optionally with a condition). Other text after `\|` only says where to look |
| `column_or_computation` | A column name (the cell itself); or `count(rows)`, `count(columns)`, `count(distinct <column>)`, `sum(<column>)`, `min(<column>)`, `max(<column>)`, `count(numbered items)`; or `text: "<quote>"` / `text in <column>: "<quote>"` for a number inside a sentence or a text cell, quoted exactly |
| `expected_value` | The value as read on 2026-10-25, exactly as stored (no thousands separators added, no rounding). Some rows hold one phrase with two or more numbers, exactly as the pilot writes it (for example "18 of 18" or "6.7–7.8") |
| `note` | Where the pilot states the same figure, display notes, caveats, cross-references to open questions |

Computed rows (53: counts, sums, minimum and maximum) are used only where the pilot states the same figure, or where the result is a plain count of rows the page lists (open question 4).

## Open questions

Decided by Yaseen on 2026-10-25 (Step 2 approval): questions 1, 2, 3, 5, 6, 7, 8 and 19. See `CLAUDE.md`, "Step 2 decisions", and `PROGRESS.md`, Step 2 close-out. The other questions are still open.

1. ~~**Git `user.name`.**~~ Decided 2026-10-25: "Yaseen", repository-local.
2. **Hours total.** The findings report gives 13.7 h plus Yaseen's step 10 time. Current status gives 13.8 h, because it adds 0.1 h for the dataset README. Proposal: the report's figures (planned rows), with a note that 0.1 h for the README came later. Yaseen's step 10 hours are "to fill", and R058 is open.
3. **Numbers held only in markdown.** 147 of the 291 rows come from markdown (127 from the findings report). These cover hours, estimates, check results, grid medians and most counts. Proposal: the extraction reads markdown tables (heading + row + column) and exact quotes (heading + quote), and the check script verifies them the same way. The alternative is to leave these numbers out, which would remove most of sections 8 and 9.
4. **Counted numbers.** 53 rows are counts or sums of existing columns (for example 195 pass rows in `evidence.csv`; 20 firm-reported mill-years). Proposal: allowed only where the pilot states the same figure (noted in each row) or for a plain count of rows the page lists. No new statistics (no shares, averages or totals across firms).
5. **Digits that are not data.** Which digit strings need no tag? Proposal: no tag for
   - review IDs (R034);
   - step numbers and section numbers;
   - file names and paths;
   - licence names and versions (CC BY 4.0, ODbL 1.0);
   - report names (AR 2022);
   - note numbers (Note 19);
   - ISIC codes;
   - DOIs inside citations;
   - HTTP status codes;
   - "3 firms × 3 years" style phrases that repeat tagged numbers.

   Tagged: dataset versions and dates in the credits (planned in section 0). Numbers printed on images (map legends, km² labels) cannot be tagged; the images are shown as they are. Approve or change.
6. **Number format.** Proposal:
   - values as stored, with thousands separators added (8,856.91; 72,574.7590);
   - a real minus sign;
   - "+" for positive rainfall anomalies;
   - no rounding.

   The check script would allow only those changes. Question: should the grid totals be shown to 4 decimals as stored, or rounded to 2 decimals as in the pilot's Current status? Rounding would be a change the check must allow.
7. **Script count.** The findings report says 33 Python scripts. The pilot's `scripts/` now holds 34, because `step10_check_report.py` was added after the count. Proposal: show the report's 33 with a one-line note, or leave the count out.
8. **Folder names.** `nrfr-pilot` and `nrfr-pilot-site` contain the project name. It appears in the relative paths (`CLAUDE.md`, `PROGRESS.md`, `docs/`), in `scripts/pilot_snapshot.py` (default pilot path and docstring) and in `.gitignore`, and it would be the default GitHub repository name. The page itself shows pilot paths relative to the pilot folder, without the folder name. Rename before Step 6 if the PI's permission is not given?
9. **The PI's permission** to use the project name is an open item (`PROGRESS.md`). Until it is recorded, nothing is pushed (`CLAUDE.md` rule 14).
10. **Images** (inventory question 7). Approve the proposed set:
    - section 4: catchment map;
    - section 5: grid loss maps, distance map, optional zoom check;
    - section 7: forest map;
    - optional: palm map (section 2), the Sepakau imagery (section 6), one loss-patch image (section 8).

    May copies be resized or compressed? Should the Sepakau image, with its internal labels ("R028", "For Yaseen to pick the point"), be shown at all?
11. **Attribution wording not recorded in the pilot** (inventory question 8): the full Hansen citation and the Copernicus Sentinel-2 wording. May Claude Code read the official pages to copy them, or will Yaseen supply them? Without the Copernicus wording, no Sentinel-2 image is shown.
12. **ENCORE on the page** (inventory question 10): the full table of 50 ratings (under CC BY-SA 4.0), or only the summary (the same 50 ratings for all firms, 18 "no dependency")?
13. **Downloads** (inventory question 11). Proposal: none. The page names the pilot paths.
14. **Mill table** (inventory question 14). Proposal: names, firm and coordinate source only, without coordinates (24 more tagged numbers otherwise).
15. **A non-output file in the pilot's `docs/`** (inventory question 15). Proposal: exclude it and do not open it.
16. **Review IDs on the page** (inventory question 1). Proposal: small print after each finding. The status line says "waiting for a decision".
17. **Licence of the planning files and images.** `LICENSE.md` covers scripts, page text and ENCORE content. Not yet covered: `CLAUDE.md`, `PROGRESS.md` and `docs/`, and the map images copied into `site/assets/`. Proposal: CC BY 4.0 for the planning files; for the images, CC BY 4.0 for the pilot's own drawing, with the third-party data credited in each caption.
18. **Hours per person.** Show Claude Code and "Yaseen (Research Assistant)" in separate columns (planned), or the totals only?
19. **Source tag format** (inventory question 5). This outline uses the `docs/number_sources.csv` syntax above. Proposal: the page tag has the same three parts plus the quote where there is one, for example `data-src="reports/step10_findings.md | ## 2. What was delivered | text: 33 Python scripts"`. Approve or change.
20. **Could not be sourced.** These are not planned:
    - **Hansen citation:** the full Hansen et al. citation (authors, year, journal) is not in the pilot (question 11).
    - **Copernicus credit:** the wording is not in the pilot. The scene years can be sourced (`source_register.csv`, S2_L2A).
    - **Numbers on the map images:** cannot be tagged.
    - **Yaseen's step 10 hours:** "to fill" in the pilot.
    - **Catchment areas in km²** for Ta Ann and SPB: only hectares in `firm2_forest_loss_summary.csv` and `firm3_forest_loss_summary.csv`. Converting them would be a new computation. Only the SOP and Metanik figures in km² are stated.
    - **Not stated in the pilot:** a single total of hours including all of step 10, a share of values that passed, and totals across firms or years. Computing them would add analysis.
    - **The non-output file in the pilot's `docs/`:** not opened.
