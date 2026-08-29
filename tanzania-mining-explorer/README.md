# Ngao Exploration Console

A clickable exploration-targeting workbench for Tanzania. It puts a modelled
hyperspectral anomaly surface, the licence cadastre, and the infrastructure that
decides whether a deposit is worth anything into one scored frame, and answers a
single question: **where should the next exploration dollar go, and is that ground
available?**

Single file, no build step, no server, no API key required.

```
open tanzania-mining-explorer/index.html
```

---

## What it does

**Commodities.** Gold, copper, silver, rare earths, cobalt, nickel and zinc. One
drives the heat surface; the rest stay on as scoring inputs so polymetallic ground
scores as polymetallic ground.

**The spectral model.** Each commodity carries a library of the features the model
keys on — direct mineralogy (sericite at 2200 nm, Fe-carbonate at 2320 nm, the
Nd³⁺ triplet at 580 / 745 / 802 nm, serpentine Mg-OH at 2325 nm) and *vegetation
proxies*, where the mineral is read through what grows over it: the red-edge
inflection shift in *Brachystegia* over arsenic-bearing regolith, Cu-induced
chlorosis, Co and Zn metallophytes. The vegetation family is what lets the surface
see through transported cover, and it is listed per commodity in the rail.

**The score.** Every block — held or open — carries the same weighted score out of
100:

| Weight | Component | What it reads |
|---:|---|---|
| 28% | Spectral anomaly | Mean normalised response across the block, not its hottest pixel |
| 22% | Infrastructure access | Haul to rail or port, grid proximity, trunk-road distance |
| 18% | Geological fit | Terrane membership, distance to the nearest deposit-scale system |
| 14% | Tenure opportunity | Availability, expiry runway, competitive pressure |
| 10% | Access & consent | Protected-area overlap, terrain, settlement density |
| 8% | Data confidence | Hyperspectral scene count, survey vintage, drilling density |

Because the weighting is identical for a licence and for vacant ground, the two are
directly comparable — which is the point. The best opportunity is rarely the highest
anomaly; it is a good anomaly on ground about to come free within trucking distance
of a railhead.

**Tenure.** Every licence has a passport: type, holder, declared minerals, work
commitment against expenditure to date, block co-ordinates in graticular format,
and what has actually been excavated — ore and waste moved, strip ratio, head grade,
contained metal, royalty class, last return. Open ground is drawn dashed with its
rank; a proposed application shrinks to fit whatever blocks are genuinely free.

**Our ground.** Nine licences, the crews deployed on them, every programme running
(diamond and RC drilling, ground gravity, IP/resistivity, fixed-loop EM, soil and
auger geochemistry, trenching, petrography), the reports those programmes produced,
and the assay batches sitting in laboratories.

**Lab and reports.** The assay queue is treated as a first-class part of the picture
rather than an administrative detail, because a stalled batch stops a programme just
as effectively as a dry hole. Batches carry laboratory, method, dispatch date, quoted
turnaround, days past commitment and stage. Reports open as documents, with downhole
strip logs, gravity profiles, IP pseudo-sections, reflectance spectra and population
histograms.

## Keyboard

`1`–`4` switch workspace · `/` focus search · `+` `−` zoom · `F` fit Tanzania ·
`Esc` clear selection

## Google Maps

The console renders its own Tanzania basemap — coastline, lakes, relief, terranes,
rail, roads, ports, generation, transmission — and needs no key and no network.
Selecting **Google Satellite** or **Hybrid** loads the Maps JavaScript API and hands
the map transform over to it; every overlay is then redrawn on Google's projection,
so imagery becomes the basemap under the same tenure, heat and scoring layers.

Supply a key either by pasting it into the dialog (kept in `localStorage`) or by
opening the page as `index.html?key=YOUR_KEY`. Where `maps.googleapis.com` is
unreachable or blocked by a content-security policy, the console reports it once and
stays on its own basemap; nothing else changes.

## Files

| Path | |
|---|---|
| `index.html` | The whole application — standalone, openable from disk |
| `tools/build-artifact.mjs` | Strips the document wrapper for hosts that supply their own `<head>` |
| `dist/ngao-exploration-console.html` | Generated output of the above |

Run `node tools/build-artifact.mjs` after editing `index.html`.

## What is real and what is not

**Real:** the geography. Terranes and greenstone belts, mineral districts (Geita,
Bulyanhulu, North Mara, Kabanga, Ngualla, Panda Hill, Lupa, Mpanda, Ntaka Hill),
the Central Line, TAZARA and SGR alignments, trunk roads, the ports, generation
from Julius Nyerere HPP down to Nyakato, the transmission backbone, and the national
parks and reserves that function as hard exclusions. The spectral features listed per
commodity are real absorption features and real biogeochemical responses.

**Simulated:** the anomaly surface. It is a physically-reasoned model — seeded
kernels on those real districts, a terrane term, and multi-octave noise, rank-
normalised so a value means the same thing across commodities — not a processed
scene.

**Synthetic:** licence numbers, holders, scores, assays, crews, reports and
laboratory queues. Holder names are invented; no real company's tenure or results are
represented here. This is a working prototype of the tool, not a feed from the Mining
Cadastre.
