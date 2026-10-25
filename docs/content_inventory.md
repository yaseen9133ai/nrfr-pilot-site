# Content inventory (Step 1)

Written 2026-10-25 by Claude Code, from read-only reads of the pilot (`../nrfr-pilot`). Nothing in the pilot was changed, and no file was copied. Baseline of the files listed here: `build/pilot_snapshot.csv` (taken 2026-10-25T09:59:51Z; replaced with Yaseen's approval at 2026-10-25T10:25:57Z after Yaseen deleted the pilot's `untitled folder/`, see `PROGRESS.md`). Updated the same day:

- Step 1 addendum: the page now lives in `site/`, and section e (Public release check) was added.
- Step 1 close-out: absolute paths replaced with relative ones; Yaseen's public-release decisions recorded in section d (top) and in section e. Yaseen is named "Yaseen (Research Assistant)" on the page and in repository files ("Yaseen" for short below).

This is a list of candidates, not an outline. The outline is `docs/page_outline.md` (Step 2).

- All paths are relative to the pilot folder.
- **Numbers?** says whether the file holds numbers the page could show, and in what form:
  - **CSV**: in cells a script can read by row key and column;
  - **MD table**: in a markdown table (a script can read it by section, row and column);
  - **MD text**: only in running text (hard to tag; see open question 3);
  - **No**.
- State of the pilot at this snapshot: steps 1–9 approved; step 10 (findings report) is done and waiting for Yaseen's decision (R057). R058 (unconfirmed hours) is also open (`progress_log.md`, Current status).

## Planned page sections

### 1. What we did

| Candidate source | What it contributes | Numbers? |
| --- | --- | --- |
| `docs/PILOT_PLAN.md` | Purpose ("prove the whole chain once"), scope, the 8 features and 6 families, the 10 steps, the rules and the definition of success | MD table + MD text (3 firms, 2021–2023, 27–32 h, 10 steps) |
| `reports/step10_findings.md` §1 Summary | One-paragraph summary and the verdict for each feature | MD text + MD table |
| `progress_log.md` Current status | Firms, region and mills; which steps are approved; what is open | MD text (bullets) |
| `reports/step3_candidates.md` | How the 3 firms and the region were chosen (5 candidates screened) | MD table + MD text |
| `data/interim/firm{1,2,3}_mills.csv` | The 12 mills: name, firm, coordinates and their source, ownership | CSV (coordinates, ownership %) |
| `review_queue.csv` R007, R011, R022, R027, R030, R045 | Decisions on scope: mills in scope, region boundary, whose hours count | No (text) |

### 2. Sources

| Candidate source | What it contributes | Numbers? |
| --- | --- | --- |
| `source_register.csv` | 34 sources: name, link, version, licence, access, download date. Shows which were used, which were checks only, which could not be obtained (PEAT_CIFOR), and which belong to the two firms not chosen | CSV (dates, versions; counts by status) |
| `data/raw_files.csv` | Download log: 602 records, with a `kept` column (173 raw, 1 header only, 396 CHIRPS files clipped then deleted, 32 Sentinel-2 window reads), bytes and SHA-256 | CSV |
| `reports/step5_raw_data.md` | What was saved at step 5, per source | MD table + MD text |
| `reports/step10_findings.md` §2 | "What was delivered": raw data, clips, tables, grid, tracking files, with counts | MD table |
| `progress_log.md` Step 2 entry | How the sources were checked (official pages only) | MD text |
| `review_queue.csv` R002, R003, R013–R021, R031 | Source choices and licence/access gaps | No (text) |

### 3. Raw → final CSVs, step by step

| Candidate source | What it contributes | Numbers? |
| --- | --- | --- |
| `data/raw_files.csv` | Layer 1: raw downloads (log only; the raw files themselves are excluded) | CSV |
| `data/interim/*.csv` (32 files at the top level) | Layer 2: extracts and clips. Mills, annual-report values and the page index (`firm*_ar_values.csv`, `firm*_ar_pages.csv`), certification statements, eMSPO certificates, WRO/sanctions searches, CHIRPS month list, ENCORE ratings, UML mills in Sarawak, OSM road-tag counts, palm tile list, boundary tests | CSV |
| `data/interim/sarawak_boundary.geojson` | The region boundary (geometry only) | No |
| `data/processed/firm{1,2,3}_*.csv` | Layer 3: per-feature results per firm (forest loss by mill, rainfall by mill, certification by mill-year, yield, debt-to-equity, WRO/sanctions), then the per-firm `_firm_year.csv` and `_static.csv` | CSV |
| `data/processed/pilot_firm_year.csv`, `pilot_static.csv` | Layer 4: the final tables (9 rows; 3 rows) | CSV |
| `data/processed/README_dataset.md` | Files, row and column counts, join key, how missing values and `NO_DEPENDENCY` are coded | MD table |
| `scripts/` (34 `.py`, 4 runners, 2 package lists) | Which script made which file; runners rebuild everything (step 8: 104 outputs identical in 3 builds; step 9: 10 outputs) | No (code). The counts are in `reports/step10_findings.md` §2 |
| `progress_log.md` Steps 4–9 | What each step produced, checks and pass/fail | MD text |
| `reports/step6_checksheet.md`, `reports/step8_checksheet.md` | Per-feature checks and results | MD table |

### 4. The 8 features

| Candidate source | What it contributes | Numbers? |
| --- | --- | --- |
| `feature_dictionary.csv` (first 8 rows) | Family, type, unit, source, method, aggregation rule, reference date per feature | CSV (mostly text; thresholds in text) |
| `docs/methods/forest_loss.md`, `peat_overlap.md`, `rainfall_anomaly.md`, `encore.md`, `certification.md`, `ffb_yield.md`, `wro_sanctions.md`, `debt_to_equity.md` | One method card per feature: how it was built, source, script, aggregation rule, known limitations, how it is verified | MD text |
| `docs/PILOT_PLAN.md` Features, Mill → firm-year aggregation | The plan's definition of each feature and rule | MD table |
| `reports/step10_findings.md` §1 table, §3 table | Verdict per feature (built / built with flags / gap) and "what worked" with check results | MD table |
| `review_queue.csv` R004, R005, R008–R010, R012, R032–R041, R046–R048 | The decisions that shaped each feature | No (text) |
| `reports/step8_checks/step8_catchments_map.png` | Picture of the mill catchments (see a) | Numbers on image (areas in km²) |

### 5. Regional grid

| Candidate source | What it contributes | Numbers? |
| --- | --- | --- |
| `reports/step9_grid.md` | Outputs, columns, settings, roads, checks, gaps | MD table + MD text (medians, counts) |
| `docs/methods/regional_grid.md` | Method card: boundary, CRS, cells, pixel-to-cell rule, distances, rounding | MD text |
| `reports/step9_checks/grid_vs_sarawak_loss.csv` | Plan check: grid total vs Sarawak total, 2021–2023, with differences and result | CSV |
| `feature_dictionary.csv` (15 "Grid:" rows) | One row per grid column | CSV (text) |
| `data/interim/osm_roads_sarawak_tag_counts.csv` | Road length per OSM tag (e.g. track share) | CSV |
| `data/processed/sarawak_grid_1km.csv` | The grid itself (125,982 rows, 13 MB). Not for copying (see c); only if row counts are allowed (open question 4) | CSV |
| `reports/step9_maps/*.png` | Loss maps 2021–2023, distance maps, zoom check (see a) | On image |
| `review_queue.csv` R049–R056 | Grid decisions; R055 accepted as built; R056 not used | No (text) |

### 6. Evidence trail and worked example

| Candidate source | What it contributes | Numbers? |
| --- | --- | --- |
| `evidence.csv` | 207 rows, one per table value. Key: `table` + `firm` + `year` + `column` (no single row ID; static rows have `year` = "static"). `check_result`: 195 pass, 12 not checked. Also source, location (page), unit, reference date, boundary, method card, note | CSV |
| `reports/step10_findings.md` §5 | Worked example: SOP debt-to-equity 2022 = 0.2207, traced through 7 links | MD table |
| `reports/step7_trace_example.md` | The original trace, link by link | MD text |
| `reports/step10_checks/step7_trace_rerun_2026-10-24.txt` | Output of the trace re-run (pass) | Text |
| `data/processed/firm1_debt_to_equity.csv` | The row behind 0.2207 (debt, equity, line items) | CSV |
| `source_register.csv` row AR_SOP_2022; `data/raw_files.csv` row of `Annual-Report-2022.pdf` | Source and its logged SHA-256 (page numbers cited; the PDF itself is excluded) | CSV |
| `data/interim/firm{1,2,3}_checks.csv` | Check registers, 20 rows per firm | CSV |
| `docs/methods/debt_to_equity.md` | The method card used in the example | MD text |
| `reports/step5_maps/step5_R028_sepakau_imagery.png` | Optional: one check made visible (firm-map point vs eMSPO point) | On image |

### 7. Results

| Candidate source | What it contributes | Numbers? |
| --- | --- | --- |
| `data/processed/pilot_firm_year.csv` | 9 rows × 6 value columns: forest loss (ha), rainfall anomaly (mm), certification (%), FFB yield, debt-to-equity, WRO/sanctions count (empty in all 9 rows) | CSV |
| `data/processed/pilot_static.csv` | Peat overlap (empty for all 3 firms) and 50 ENCORE ratings (the same for all 3 firms) | CSV |
| `evidence.csv` | Unit, status, flag and note for every value (e.g. yield restatement flag, "not comparable", missing reasons) | CSV |
| `data/processed/firm{1,2,3}_certification_firm_year.csv` | Firm-reported mill-years behind the 100% (SOP 10/21, Ta Ann 4/9, SPB 6/6) | CSV |
| `data/processed/firm{1,2,3}_ffb_yield.csv` | Yield as printed, with unit wording (mt/ha vs Mt/WHa) | CSV |
| `data/processed/firm{1,2,3}_forest_loss_summary.csv`, `_forest_loss_by_mill.csv` | Loss per mill catchment (e.g. Metanik's share of SOP's loss) | CSV |
| `reports/step5_maps/step5_map_forest.png`, `step5_map_palm.png` | Context maps (see a) | On image |

Note for the page: yields are not comparable between firms (R048) and ENCORE gives no between-firm information (R036). The page should not rank or compare firms on these.

### 8. Gaps and findings

| Candidate source | What it contributes | Numbers? |
| --- | --- | --- |
| `reports/step10_findings.md` §4 | The 16 issues, each with what it means and its review item | MD table (numbers inside cells) |
| `evidence.csv` rows with `status` = missing | The 12 missing values and their recorded reasons | CSV |
| `docs/methods/peat_overlap.md`, `wro_sanctions.md` | The two gap features | MD text |
| `docs/methods/*.md` "Known limitations" | Limitations per feature | MD text |
| `review_queue.csv` R014, R019–R021, R023, R033–R038, R040, R043, R044, R046–R048, R052, R055, R056 | The decisions behind each gap | No (text) |
| `progress_log.md` Issues of steps 2–9 | Issues as logged at the time | MD text |
| `reports/step6_checks/step6_loss_patches_imagery.png`, `reports/step8_checks/loss_patches_imagery_firm{2,3}.png` | Visual for gap 9 (Hansen also counts logging) | On image |

### 9. Hours and full-build estimate

_Removed from the page at the Step 4 close-out (`CLAUDE.md`, Step 4 decision 10); section 10 below became section 9. Kept here as the Step 1 record._

| Candidate source | What it contributes | Numbers? |
| --- | --- | --- |
| `reports/step10_findings.md` §6 | Hours per step and person, which figures were confirmed | MD table |
| `reports/step10_findings.md` §7 | Split by kind of work; per extra firm 0.9–2.3 h; per extra region 3.0–7.2 h; illustration for 10 and 30 firms; what would need to change | MD table + MD text |
| `progress_log.md` Hours line of each step; Current status | Hours as logged; Current status gives 13.8 h including the dataset README | MD text |
| `review_queue.csv` R011, R058 | Whose hours count; unconfirmed hours (open) | No (text) |

The hours exist only in markdown, not in any CSV (open question 3). The two files give totals at different points: 13.7 h + Yaseen's step 10 time (report) and 13.8 h (Current status, after the README). Yaseen's step 10 hours are "to fill" (open question 2).

### 10. Next decisions

| Candidate source | What it contributes | Numbers? |
| --- | --- | --- |
| `reports/step10_findings.md` §8 | The three options (scale up, change plan, stop), listed without a recommendation | No |
| `reports/step10_findings.md` §7.5 | What would need to change for a full build | MD text |
| `review_queue.csv` R057, R058 | The two open items | No |
| `progress_log.md` Current status, "Next" | What waits for whom | No |

## a) Map and image files in `reports/`

32 PNG files. "Viewed" = opened in Step 1. None of the images viewed show personal data.

| File | Shows | Viewed | Personal data | Licence and credit notes | Proposal |
| --- | --- | --- | --- | --- | --- |
| `step5_maps/step5_map_forest.png` | Hansen tree cover 2000 and loss years over Sarawak, 7 SOP mills, 7 mill close-ups | Yes | None | Credit on image: "Hansen/UMD/Google/USGS/NASA … (CC BY 4.0)". The boundary (geoBoundaries, ODbL) is named but its licence is not on the image. Uses the SOP firm-map points, so Sepakau is the superseded point (R028) | Show (sections 2 or 7). Caption adds the geoBoundaries/OSM ODbL credit and the Sepakau note |
| `step5_maps/step5_map_palm.png` | Descals 2024 oil palm extent 2021, SOP mills; hatched areas have no source tile | Yes | None | Credit on image: Descals et al. 2024, v1.2, DOI, CC BY 4.0. Boundary credit as above | Show (section 2). Caption says the palm layer is used only for maps and covers 80.0% of Sarawak |
| `step5_maps/step5_R028_sepakau_imagery.png` | Sentinel-2 views from 2021 and 2024, firm-map point vs eMSPO point for Sepakau | Yes | None (mill coordinates and an eMSPO track ID) | On image: "Copernicus Sentinel-2 data (ESA)", not the exact Legal Notice wording; the Sentinel-2 licence text was not checked (source_register). Internal wording on image ("R028", "For Yaseen to pick the point") | Ask. If shown, caption adds the Copernicus wording |
| `step5_checks/cbp_wro_dashboard_2026-10-23.png` | Screenshot of the CBP WRO dashboard | Yes | None | Contains the CBP seal; CBP terms require "not endorsed by CBP" | Do not show |
| `step6_checks/gfw_SOP-0{2,5}_202{1,2,3}.png` (6), `step8_checks/gfw_{TAANN-02,TAANN-03,SPB-01,SPB-02}_202{1,2,3}.png` (12) | Screenshots of the Global Forest Watch / Global Nature Watch web map tooltip | 1 of 18 (`gfw_SOP-02_2021.png`) | None in the one viewed | Screenshots of a third-party site whose terms were not read (source_register GFW_GNW) | Do not show. Use the transcribed CSVs (`gfw_comparison*.csv`) for numbers |
| `step6_checks/step6_catchments_map.png` | Catchments, SOP cells only (step 6 version) | Yes | None | On image: boundary "geoBoundaries MYS ADM1 (ODbL)", "Universal Mill List" (no licence stated) | Do not show; replaced by the step 8 map |
| `step8_checks/step8_catchments_map.png` | Catchments of all 12 firm mills in the shared tessellation (90 points), with areas in km² | Yes | None | As above. UML points shown as dots (no stated licence, R021) | Show (section 4). Some labels overlap |
| `step6_checks/step6_loss_patches_imagery.png` (4.9 MB) | SOP loss patches on Sentinel-2, before and after | No (same script as the firm 2 image) | Not expected (satellite imagery) | Credit on image: Copernicus Sentinel-2 (ESA), Earth Search; Hansen named, without licence text. 4.9 MB is large for a page | Ask (section 8, gap 9) |
| `step8_checks/loss_patches_imagery_firm2.png`, `loss_patches_imagery_firm3.png` | Ta Ann and SPB loss patches on Sentinel-2 | Firm 2 yes; firm 3 no | None in firm 2 | As above | Ask (section 8) |
| `step9_maps/step9_loss_2021.png`, `_2022.png`, `_2023.png` | Forest loss per 1 km cell, with mills and OSM roads | 2021 yes; 2022–2023 same script | None | On image: Hansen, OSM roads and UML named, but no "© OpenStreetMap contributors" or ODbL notice and no geoBoundaries credit | Show 1 or 3 (section 5). The caption carries the OSM, geoBoundaries and Hansen credits |
| `step9_maps/step9_distances.png` | Distance to nearest mill point and nearest OSM road | Yes | None | Same as above | Show (section 5), with the same caption credits |
| `step9_maps/step9_zoom_check.png` | Grid cells vs the Hansen pixels they were built from (largest 2021 cell) | Yes | None | Hansen credit needed in the caption | Optional (section 5 or 6) |

Other image-like files: `data/interim/step6_s2_chips/` (16 Sentinel-2 GeoTIFF chips) and the palm tiles are rasters, not page images; excluded (see c).

Images would be copied into `site/assets/` unchanged. Whether resizing a copy is allowed is open question 7.

## b) Attributions

From `source_register.csv` (`licence` column), with the place where exact wording is recorded. "Shown" = the page shows data, maps or numbers from this source.

| Source (source_id) | Licence as recorded | What the page must carry | Exact wording recorded in |
| --- | --- | --- | --- |
| Hansen Global Forest Change v1.13 (HANSEN_GFC) | CC BY 4.0 | Credit (Hansen/UMD/Google/USGS/NASA), dataset version, licence, and a note that the data was clipped and thresholded (> 30% cover) | Licence sentence: source_register. On-image credit: `step5_map_forest.png`. Full citation (Hansen et al. 2013): **not recorded in the pilot** (open question 8) |
| Descals 2024 oil palm extent (PALM_DESCALS2024) | CC BY 4.0 | Credit: Descals, A. (2024), "Global oil palm extent and planting year from 1990 to 2021", v1.2, Zenodo, DOI 10.5281/zenodo.13379129; licence; "clipped to Sarawak" | `data/raw/PALM_DESCALS2024/zenodo_record_13379129.json` (title, creator, DOI, licence); on-image credit |
| geoBoundaries Malaysia ADM1 (BOUNDARY_GEOB) | ODbL 1.0 (from OpenStreetMap, Wambacher) | "geoBoundaries" + "© OpenStreetMap contributors", ODbL 1.0 notice. Share-alike applies to adapted databases, not to map images | `data/raw/BOUNDARY_GEOB/geoBoundaries-MYS-ADM1_api_metadata.json` (boundarySource, licence, licenseSource) |
| OpenStreetMap roads (ROADS_OSM) | ODbL 1.0 | "© OpenStreetMap contributors" and that the data is available under the ODbL (OSM copyright page wording, quoted in source_register notes). Snapshot date 2026-10-22 | source_register notes |
| Copernicus Sentinel-2 L2A (S2_L2A) | "free, full and open"; licence text **not checked** | Credit for Copernicus Sentinel data (ESA) with year(s); the usual Legal Notice wording ("Contains modified Copernicus Sentinel data [year]") must be confirmed | On-image credit only; licence not checked (source_register; findings §4 item 15) |
| CHIRPS v2.0 (CHIRPS) | Public domain (waiver) | Nothing required. Proposal: cite Funk et al. (2015) as a courtesy | `data/raw/CHIRPS/README-CHIRPS.txt`, "DATA SET CITATION" |
| ENCORE (ENCORE) | CC BY-SA 4.0; third-party datasets excluded; images need UNEP permission | Required citation, template from ENCORE file 01: "ENCORE Partners (Global Canopy, UNEP FI, and UNEP-WCMC) (year). ENCORE: Exploring Natural Capital Opportunities, Risks and Exposure. [On-line], [month/year of the version downloaded], Cambridge, UK: ENCORE Partners. DOI 10.34892/dz3x-y059." Filled in: year 2026, version May 2026 (source_register `version`). Share-alike: any ENCORE ratings shown on the page must be offered under CC BY-SA 4.0. No ENCORE images | source_register `licence` (citation template from file 01) |
| EU consolidated financial sanctions list (EU_FSF) | EC reuse notice (Decision 2011/833/EU); CSV listed as CC BY 4.0 | Source credit (European Commission) and licence, if the page says the current list was searched. The page quotes only the part that applies to the file used, CSV 1.1: "European Commission reuse notice (Decision 2011/833/EU)" (CC BY 4.0 is listed for CSV 1.0): in the credits since Step 5 close-out, in the sources table since Step 6 close-out | source_register; `data/raw/EU_FSF/data_europa_eu_catalogue_record.json` |
| US CBP WRO and Findings (CBP_WRO) | Public domain; Data Portal terms | Verbatim: "This product uses U.S. Customs and Border Protection data, but is not endorsed by CBP." No CBP seal or logo | source_register `licence` |
| Global Forest Watch / Global Nature Watch (GFW_GNW) | Tree cover loss data CC BY 4.0; site terms **not read** | If GFW check numbers are shown: credit GFW (WRI) and UMD/Hansen. No screenshots | source_register |
| CIFOR Global Wetlands (PEAT_CIFOR) | Research and educational use only | Not obtained, so no data is shown. The page names it only as the gap | – |

**Sources with no stated licence** (all show "All rights reserved" or nothing):

| Source | Used in the pilot for | Proposed treatment |
| --- | --- | --- |
| eMSPO (MSPO) | Mill coordinates (Ta Ann, SPB, Sepakau) and certification periods | Name it as a source ("eMSPO Certified Entity list, MSPO, accessed 2026-10-23"). Show only facts the pilot derived (status, dates, counts, mill names). No copy of records, no screenshots, and none of the contact fields. State that no licence is stated (R021) |
| RSPO registry (RSPO) | Search for RSPO certificates (none found) | Name it as a source; state the result only ("no record found"). State that no licence is stated (R019) |
| Universal Mill List (UML) | 78 of 90 tessellation points; coordinate cross-check | Name it as a source (Rainforest Alliance; WRI/GFW, file of July 2026), with its own caveat that it is unverified. Its points appear as dots on the catchment and grid maps; no table of UML records. State that no licence is stated (R021). Showing the dots: open question 7 |
| Annual reports, 9 (AR_SOP/TAANN/SPB_2021–2023) and firm websites (MILLS_SOP, MILLS_TAANN, MILLS_SPB) | Debt, equity, yield, certification statements; mill lists | Licences **not checked** (step 3). Cite by title, year and page number. Show only the figures used and short quotes. No PDFs, page images or extracts. No company logos |

The page also needs its own notice: who made it, and under what terms (open question 9).

## c) Files to exclude

| Path | Why |
| --- | --- |
| `data/raw/**` (784 files, 2.41 GB on disk; the findings report's "about 1.8 GB" counts the 174 kept downloads, not the unpacked palm zip) | Raw downloads (site rule 6). Includes: the 9 annual-report PDFs; eMSPO entity records `data/raw/MSPO/emspo_entity_*.json`, which hold **personal data** (fields `picName`, `picPhone`, `picEmail`, `directorName`, `directorPhone`, `directorEmail`, `entityEmail`, `entityPhone`, addresses); the EU sanctions list (names of listed persons); UML.xlsx (no licence); ENCORE files (images need UNEP permission); OSM, Hansen, Sentinel-2 and palm rasters |
| `data/interim/ar_pages/` (9 PDFs) | Annual-report page extracts (site rule 6) |
| `data/interim/*.tif`, `data/interim/osm_roads_sarawak.gpkg`, `data/interim/step6_s2_chips/`, `data/interim/palm_descals2024_extent2021_sarawak/` | Rasters and large derived layers (up to 71 MB). The page uses the maps made from them |
| `data/processed/sarawak_grid_1km.gpkg` (41.7 MB), `sarawak_grid_1km.csv` (13.3 MB), `sarawak_mill_catchments.geojson` (3.5 MB) | Too large to copy; the page uses the grid report, the check CSV and the maps. If the grid were offered as a download, ODbL share-alike would apply (OSM-derived distances): open question 11 |
| `data/processed/*_v1_step6.*` | Superseded step 6 tessellation |
| `data/processed/firm*_loss_patches_selected.csv` | Intermediate patch lists (up to 214 KB); not needed |
| `untitled folder/` (30 files) | All 30 were byte-identical copies of files elsewhere in the pilot (checked by SHA-256 on 2026-10-25). Deleted by Yaseen on 2026-10-25; none of the 30 was referenced in the pilot's tracking files, method cards or scripts. The site uses the originals |
| `scripts/__pycache__/`, `.DS_Store` (8), `outputs/` (empty) | Scratch |
| A file in the pilot's `docs/` that is not a pilot output (not named here) | Not a pilot output; not opened, so not checked (open question 15) |
| `reports/step5_checks/cbp_wro_dashboard_2026-10-23.png` | CBP seal (see a) |
| `reports/step6_checks/gfw_*.png`, `reports/step8_checks/gfw_*.png` (18) | Third-party site screenshots, terms not read (see a) |
| `reports/step5_checks/eu_sanctionsmap_autocomplete_*.json` | Raw search responses; the "Wagner" control lists sanctioned names |
| `reports/step5_checks/emspo_site_view_2026-10-23.json`, `reports/step8_checks/emspo_site_view_firms23_2026-10-24.json` | Raw captures of eMSPO pages (mill-level fields only; no contact fields found). Not needed on the page |
| `reports/*/gfw_upload_*.geojson` | Polygons uploaded to GFW; not needed |
| `CLAUDE.md` (pilot) | Instructions for Claude Code, not content |

Personal data search (2026-10-25, read-only): no e-mail address and no eMSPO contact field was found in any file outside `data/raw/` (`untitled folder/`, since deleted, held only copies of files that were searched). The contact fields occur only in `data/raw/MSPO/emspo_entity_*.json`. Mill coordinates are business sites from published sources.

## d) Open questions for Step 2

**Decided by Yaseen on 2026-10-25 (Step 1 close-out):**

- Q12 (links): pilot paths are shown as plain text.
- Q13 (`untitled folder/`): deleted by Yaseen; it was not a selection for the site.
- Q16 (public release): all of it. Name "Yaseen (Research Assistant)"; relative paths; repository-local git e-mail; UML points shown with credit and "no licence stated"; ENCORE content marked CC BY-SA 4.0; licences MIT (scripts), CC BY 4.0 (page text), CC BY-SA 4.0 (ENCORE-derived content); a neutral purpose (project-internal content is never published); the project name not used in page text (Step 5 decision 11: it may appear in folder names, paths and the repository). Hours and the estimate are shown (section 9 is in the Step 2 brief).
- Q9 (the page's own notice), in part: author "Yaseen (Research Assistant)"; terms as in `LICENSE.md`.

Questions 1–8, 10, 11, 14 and 15 are still open. `docs/page_outline.md` makes a proposal for each.

1. **Audience and status.** Who reads the page? Should it show review IDs (R0xx) or keep them in the links only? Step 10 is not yet approved (R057): should the page say "findings, waiting for decision"?
2. **Hours.** Which total: the report's 13.7 h + Yaseen's step 10 time, or Current status's 13.8 h (after the README)? Yaseen's step 10 hours are "to fill" and R058 is open. If Yaseen fills them in nrfr-pilot, the snapshot check will flag the change, and the baseline must be replaced with approval.
3. **Numbers held only in markdown.** Hours, the full-build estimate, grid medians and many counts exist only in markdown tables or text. May the extraction script read markdown tables (tag = file + section + row + column)? And what happens to numbers that appear only in running text: quoted with a tag to a line, or left out?
4. **Counted numbers.** May a script count or sum existing columns (for example 195 pass in `evidence.csv`, 34 rows in `source_register.csv`), if the check script also matches the pilot's stated figure? Proposal: allowed only where the pilot states the same figure; no new statistics (no recomputed medians or shares).
5. **Source tag format.** `evidence.csv` has no single row ID. Proposal: `file | key=value;… | column` (for example `data/processed/pilot_firm_year.csv | firm_id=SOP;year=2022 | debt_to_equity`) and, for markdown, `file | section | row | column`. Approve or change.
6. **Number format.** Show values exactly as stored (8856.91), or with thousands separators (8,856.91)? Any rounding? Proposal: as stored, with thousands separators only; the check script allows only that change.
7. **Images.** Which ones to show (proposals in a)? May copies be resized or compressed (one is 4.9 MB)? Are maps with UML dots acceptable, given that the UML states no licence? Show the R028 image with its internal labels?
8. **Attribution wording not recorded in the pilot** (the Hansen citation, the Copernicus Legal Notice wording). May Claude Code read the official pages to copy the exact wording (read only, nothing downloaded, nothing added to nrfr-pilot)? Or will Yaseen supply it? How should the page treat licences the pilot marked "not checked" (annual reports, Sentinel-2, GNW site terms)?
9. **The page's own notice.** Author and byline (name or organisation), and terms: the ENCORE part must be CC BY-SA 4.0 if ratings are shown.
10. **ENCORE on the page.** Show all 50 ratings (identical for the 3 firms), or only what the pilot states (the same 50 ratings, 18 `NO_DEPENDENCY` each)?
11. **Downloads.** Should the page offer the final tables (`pilot_firm_year.csv`, `pilot_static.csv`, `evidence.csv`) or the grid as files? This brings in ODbL (grid) and CC BY-SA (ENCORE) terms. A public repository would also publish them. Proposal: no downloads; name the nrfr-pilot paths.
12. ~~**Links to pilot paths.** The page will be public and the pilot is not, so a link would lead nowhere.~~ Decided 2026-10-25: each path is shown as plain text, labelled "pilot folder (not published)".
13. ~~**`untitled folder/`** in the pilot (made 2026-10-24, 30 copies): was this a selection for the site?~~ Decided: deleted by Yaseen, 2026-10-25.
14. **Mill table.** Show the 12 mills with coordinates, or names and firms only?
15. **A non-output file** in the pilot's `docs/`: exclude, or may Claude Code open it to check whether it adds background? (Proposal taken up in the outline: exclude it and do not open it.)
16. ~~**Public release decisions** marked "Yaseen decides" in section e.~~ Decided 2026-10-25 (see the top of this section and section e).

## e) Public release check

Decided by Yaseen on 2026-10-25: the repository will be public on GitHub, and `site/` will be deployed on Vercel. Everything committed is public, not only `site/`: also `CLAUDE.md`, `PROGRESS.md`, `docs/` (this file included) and `scripts/`. Nothing is committed yet.

These items may not be fit for public release. "Yaseen decides" marked the ones that needed a decision (open question 16). All of them were decided on 2026-10-25; each is marked **Decided** below, and the decisions are also in `CLAUDE.md` (Public-release decisions). This section quotes no personal data and no project-internal content, because it will be public too.

### e1. Personal data

| Item | Where | Proposed treatment |
| --- | --- | --- |
| eMSPO contact fields: names, phone numbers and e-mails of mill contacts and directors | Only in `data/raw/MSPO/emspo_entity_*.json` (pilot) | Never copied or committed. The Step 5 check scans every tracked file for e-mail addresses, phone numbers and these fields with values |
| Names of listed persons in sanctions data | `data/raw/EU_FSF/` and `reports/step5_checks/eu_sanctionsmap_autocomplete_Wagner.json` (pilot) | Excluded. The page says only that the current lists were searched, with no match for the 3 firms |
| Yaseen's name, decisions and hours | Pilot files name Yaseen often (on 57 lines of `review_queue.csv`, 21 rows of `evidence.csv` and 17 lines of `reports/step10_findings.md`, and on the R028 image). Also this repository's `PROGRESS.md` and this file | **Decided:** "Yaseen (Research Assistant)" on the page and in repository files; no full name, no student ID. Hours per person: section 9 of the outline proposes showing them under that name (open question in `docs/page_outline.md`) |
| Local user name in absolute paths (`/Users/<user>/projects/…`) | This repository: `CLAUDE.md`, `PROGRESS.md`, this file. (`build/` also, but it is git-ignored) | **Decided:** relative paths (`../nrfr-pilot`, `.`) in `CLAUDE.md`, `PROGRESS.md` and `docs/`; done 2026-10-25. `build/` files still hold the absolute path; they are git-ignored |
| Git author name and e-mail | Every commit; public on GitHub | **Decided:** repository-local `user.email` set to the address Yaseen gave. `user.name` is open (the value given was unclear). Since then: `user.name` "Yaseen" (Step 2 close-out); `user.email` Yaseen's GitHub no-reply address, set before the first commit (Step 5 close-out decision 6) |
| Person names in annual-report quotes | `evidence.csv` notes; `data/interim/firm*_ar_certification_statements.csv` | Search on 2026-10-25: no personal titles (Dato', Datuk, Tan Sri, Encik, Puan, Mr., Mrs., Ms., Dr.) in the candidate pilot files. Every quote shown is checked again in Step 5 |
| Mill coordinates | `data/interim/firm*_mills.csv`; the maps | Business sites from published sources (firm map, eMSPO). Not personal data. Show |

### e2. Sources with no stated licence

| Source | What the page would use | Proposed treatment |
| --- | --- | --- |
| eMSPO (MSPO) | Certification periods; 6 of the 12 mill coordinates (Sepakau, Ta Ann's 3, SPB's 2) | Show only facts the pilot derived: status on 31 December, dates, counts, mill names. Attribute ("eMSPO Certified Entity list, MSPO, accessed 2026-10-23"). No copied records, screenshots or raw captures. State that no licence is stated (R021) |
| RSPO registry | One negative result: no record under any status for the 3 firms | Attribute; state the result only; state that no licence is stated (R019). Low risk |
| Universal Mill List (UML) | 78 of the 90 points that set the catchment edges. Shown as dots on the step 8 catchment map and the step 9 maps | **Decided:** (a) the maps are shown, with credit and "no licence stated". The options were: (a) show the maps with attribution and "unverified; no licence stated"; (b) also ask Rainforest Alliance for permission before Step 6; (c) leave out the maps with UML dots. Never a UML table, name list or download |
| Annual reports (9) and firm websites (3) | Debt, equity, yield, certification statements, mill lists | Licences not checked. Figures, short quotes and page numbers only. No PDFs, page images, extracts or logos (rule 12; `.gitignore` blocks `*.pdf`) |

### e3. Share-alike and other licence terms

| Item | Issue | Proposed treatment |
| --- | --- | --- |
| ENCORE, CC BY-SA 4.0 | ENCORE ratings shown on the page, and any committed file that holds them (for example page data in `site/`), are adapted material. They must be offered under CC BY-SA 4.0 with the required citation. No ENCORE images (they need UNEP permission). Third-party datasets inside ENCORE are not covered | **Decided:** ENCORE content is marked "CC BY-SA 4.0" next to it, with the ENCORE citation; the repository licence allows it (`LICENSE.md`). How much ENCORE content is shown is still question 10 |
| OpenStreetMap roads and geoBoundaries, ODbL 1.0 | Map images are "produced works": attribution and the ODbL notice are enough. A committed file holding grid, road or catchment data could be a derivative database, which brings in share-alike | Commit no grid, road or catchment data; summary numbers only. Captions carry "© OpenStreetMap contributors, ODbL" |
| Hansen, Descals, EU sanctions list (CC BY 4.0) | Attribution and a note of changes (clipped, threshold) | Credit lines as in section b. EU sanctions list: the page quotes the reuse notice, which applies to the file used (CSV 1.1; Step 5 close-out decision 1) |
| Copernicus Sentinel-2 | Licence text not checked by the pilot | Confirm the wording before Step 6 (question 8), or do not show the imagery |
| CBP | Data Portal terms | The verbatim "not endorsed by CBP" statement; no seal or logo |
| GFW / GNW | Site terms not read | Screenshots not used |
| Repository licence | A public repository without a licence file means "all rights reserved" for its code and text | **Decided:** MIT for scripts, CC BY 4.0 for page text, CC BY-SA 4.0 for ENCORE-derived content. Written 2026-10-25: `LICENSE.md` (overview, CC licence links, ENCORE citation, third-party note) and `LICENSES/MIT.txt`. Not yet covered: the planning files and the images in `site/assets/` |

### e4. Project-internal content

| Item | Where | Proposed treatment |
| --- | --- | --- |
| Non-output files | Files in the pilot that are not pilot outputs, not opened | Excluded and not cited (question 15) |
| Project-internal content | Anything in the pilot's planning files beyond what the pilot produced | **Decided:** never published, quoted or summarised. The page describes the pilot neutrally, as proof that the data chain can be built and traced. The terms to scan for are kept only in the local, git-ignored `build/private_terms.txt` |
| The project name | Titles of the pilot's plan and report, and the folder names of the pilot and of this repository | **Decided:** page text and prose say "palm oil pilot". The name may appear in folder names, paths and the repository (Step 5 decision 11, 2026-10-25). On the page since Step 5 close-out decision 4 (2026-10-26): the title "NRFR palm oil pilot", the name once in the intro, "the pilot" elsewhere |
| Hours and the full-build estimate | `reports/step10_findings.md` §6–7 | **Decided:** shown (section 9 of the page, in Yaseen's Step 2 brief). Removed from the page by Step 4 decision 10 |
| Internal process: review IDs, decisions by name, waived manual checks | `review_queue.csv`, `progress_log.md`, the report | Proposal: present these as findings in plain words (for example "all checks were self-checks; no value was checked independently"), with review IDs in small print only. Decided with question 1 |
| Links to pilot paths | Every section | The pilot is not published, so paths are shown as text (question 12) |
| This repository's planning files | `CLAUDE.md`, `PROGRESS.md`, `docs/` | Public too, so they follow the same rules. They name file paths, field names and review IDs; they hold no personal data and no project-internal content. Absolute paths and Yaseen's name: see e1 |

### e5. Statements about named companies

| Item | Risk | Proposed treatment |
| --- | --- | --- |
| Forest loss per firm | The figure is loss inside the firm's mill catchments (tessellation cells around mill points; Metanik's cell is 20,079 km²), from any stand-replacing cause including replanting and logging (R040). It is not land owned or cleared by the firm. Without that context, a public figure could read as an accusation | **Decided:** the caveat (loss from any cause in the catchment area, including replanting and logging; not land cleared by the firm) sits next to every forest-loss number. No ranking of firms |
| WRO/sanctions | "Missing" could be misread either way | Say "no match in the current lists; 2021–2023 not checked". Never "clean" or "compliant" |
| Certification 100% | Overstates what is known | Say that 20 of the 36 mill-years rest on the firms' own statements (R038) |
| FFB yield, ENCORE | Not comparable between firms (R048); identical for all firms (R036) | No comparison or ranking between firms |
| Company names | Trademarks | Names in text only; no logos |
| All statements about the 3 firms | Wording could read as a judgement | **Decided:** factual, sourced and neutral wording only; no judgements |

### e6. Repository safeguards

- `.gitignore` (written 2026-10-25) keeps out:
  - `build/`, and local copies of pilot data (`nrfr-pilot/`, `data/`, `local/`);
  - raw file types (`*.pdf`, `*.tif`, `*.tiff`, `*.nc`, `*.gpkg`, `*.pbf`, `*.xlsx`, `*.xls`, `*.zip`);
  - `.DS_Store`, virtual environments and caches;
  - `.vercel/` and `.env*`.
- Proposed for Step 5, and before any commit, a scan of every tracked file for:
  - e-mail addresses and phone numbers;
  - eMSPO contact fields with values;
  - absolute local paths (if Yaseen chooses relative paths);
  - files of a raw type.
- Also proposed for Step 5: `site/` holds only `index.html` and `assets/`; the page loads nothing from outside; size limits.
