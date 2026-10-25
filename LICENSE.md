# Licences

This repository holds a static web page about a palm oil pilot, and the scripts that build and check it. Different parts are under different licences.

Author and licensor: Yaseen (Research Assistant), 2026.

| Part | Licence | Text |
| --- | --- | --- |
| Scripts: everything in `scripts/`, and the style sheet they write (`site/assets/style.css`) | MIT License | [`LICENSES/MIT.txt`](LICENSES/MIT.txt) |
| Page text: the text written for `site/index.html` | Creative Commons Attribution 4.0 International (CC BY 4.0) | https://creativecommons.org/licenses/by/4.0/legalcode |
| Planning files: `CLAUDE.md`, `PROGRESS.md`, everything in `docs/` | CC BY 4.0 | https://creativecommons.org/licenses/by/4.0/legalcode |
| Images: the pilot's map and check images copied into `site/assets/` (`*.png`), and `site/assets/manifest.csv` | CC BY 4.0 for the drawing, with the data credits below | https://creativecommons.org/licenses/by/4.0/legalcode |
| ENCORE-derived content: every part of the page that shows or describes ENCORE ratings, marked "CC BY-SA 4.0" on the page, and any repository file that holds those ratings | Creative Commons Attribution-ShareAlike 4.0 International (CC BY-SA 4.0) | https://creativecommons.org/licenses/by-sa/4.0/legalcode |

## ENCORE

The ENCORE-derived content is adapted from:

ENCORE Partners (Global Canopy, UNEP FI, and UNEP-WCMC) (2026). ENCORE: Exploring Natural Capital Opportunities, Risks and Exposure. [On-line], May 2026, Cambridge, UK: ENCORE Partners. DOI 10.34892/dz3x-y059.

It is shared under CC BY-SA 4.0, as the ENCORE terms require. This includes ENCORE-derived parts of files that are otherwise under CC BY 4.0 (for example the ENCORE rows of `docs/number_sources.csv` and the ENCORE summary on the page). Third-party datasets inside ENCORE are not covered by that licence. No ENCORE images are used.

## Images and data credits

The images in `site/assets/` were drawn by the palm oil pilot's scripts. They show third-party data, which keeps its own terms. Each image's caption on the page names the data it shows:

- Hansen et al. (2013) Science; Hansen/UMD/Google/USGS/NASA, Global Forest Change, CC BY 4.0;
- Descals et al. 2024, global oil palm extent, CC BY 4.0, map tiles clipped to Sarawak;
- © OpenStreetMap contributors, ODbL (roads, and the geoBoundaries boundary, which comes from OpenStreetMap);
- Universal Mill List points (Rainforest Alliance; WRI/GFW): no licence stated.

## Third-party material

The licences above do not cover third-party material on the page or in this repository. It keeps its own terms, and the page credits each source next to where it is used:

- data credits and map layers (for example Hansen Global Forest Change, CHIRPS, geoBoundaries, OpenStreetMap, Descals et al. 2024);
- the Universal Mill List points shown on maps (no licence stated);
- facts taken from eMSPO and the RSPO registry (no licence stated);
- the results of searches and checks against the EU consolidated financial sanctions list (European Commission reuse notice, as recorded in the pilot) and the Global Forest Watch map (WRI; tree cover loss data CC BY 4.0, site terms not read);
- figures and short quotes from company annual reports, and company names (no logos are used).

The list of sources and the attributions they require is in `docs/content_inventory.md`, section b.

Decided by Yaseen (Research Assistant), 2026-10-25: planning files and images CC BY 4.0, with the data credits above (`CLAUDE.md`, Step 3 decision 11). The Copernicus credit was removed with the only image that showed Sentinel data (`CLAUDE.md`, Step 4 decision 1).
