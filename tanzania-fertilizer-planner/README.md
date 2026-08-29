# Mbolea — fertiliser demand & territory planner

A single-file, zero-dependency planning console for the **Coast–Morogoro corridor of Tanzania**
(≈ 520 × 510 km centred on Dar es Salaam). Draw a circle on the map and it returns the
fertiliser tonnage inside it, split by product and by crop, plus the sales KPIs for whoever
has to cover that ground.

Open `index.html` in any browser. No build step, no network calls except the webfont.

## What it does

- **Click-drag a territory.** Every circle reports cropland, farming households, season
  tonnage by product, and district split. Default is 100 km across — one day's driving —
  and the diameter box takes any number.
- **Portfolio switching.** Choose the basal (DAP / TSP / Minjingu Mazao / NPK 20-10-10),
  the top dressing (Urea / CAN / SA) and the potash source. Nutrient demand is met basal
  first, then potash, then the nitrogen balance, and every tonnage and price recalculates.
- **Three map layers.** Fertiliser demand (t/km²), dominant crop, and yield gap
  ($ of reachable output per km²).
- **Nine crops** — maize, paddy rice, cassava, cashew, sugarcane, sisal, sunflower,
  sorghum & millet, horticulture. Click one to map it alone; alt-click to drop it from
  the demand calculation entirely.
- **Sales KPIs per route** — volume target at your market share, revenue, agro-dealers
  needed against outlets that already exist, calls per month, drive time to the edge,
  and a Prime / Viable / Thin grade.
- **Auto-plan** greedily places non-overlapping routes over the highest-demand ground.
- **Territory brief** produces a plain-text hand-out per rep.

Keyboard: focus the map, then `Enter` drops a route, arrows move it, `[` / `]` resize,
`Delete` removes. Shift multiplies the step.

## The data underneath

The field layer is a **modelled cropping surface, not a field survey.** A 0.055° grid
(≈ 37 km² per cell) is scored for rainfall, floodplain and coastal position, road and
market access, and protected-area status; cropped area is then allocated to the crops that
dominate each agro-ecological zone — cane and paddy in the Kilombero and Rufiji floodplains,
cashew and cassava on the coastal sands, sisal along the Tanga–Korogwe corridor, sorghum and
sunflower on the Dodoma-side drylands. Parks and reserves carry no cropland.

Nutrient rates per hectare use Tanzanian blanket recommendations by crop
(N–P₂O₅–K₂O), scaled by the two adoption sliders. Products are allocated from nutrients at
label analysis.

**Calibrate against dealer sell-out before anyone's quota depends on it.** Swapping the
generated grid for real inputs — a district crop census, NDVI-classified plots, ward-level
sell-out — is a change to `buildCells()` alone; everything downstream is unchanged.
