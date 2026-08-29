# Sarawat Terroir Engine

A single-file, clickable decision tool for a Saudi coffee company: where the Kingdom
already grows coffee, where it could, and how those parcels compare with the Yemen
districts that define the reference for highland Arabian arabica.

Open `index.html` in a browser. No build step, no dependencies.

## Tabs

| Tab | What it answers |
|---|---|
| Operations | What the eight producing estates yielded, cost in water, and are flagged for |
| Expansion | Which of twenty Saudi parcels to plant next, ranked, filtered, and paired to a Yemen analogue |
| Yemen benchmark | Twelve heritage districts: cup scores, 2015–2025 yield history, rain, fog, altitude |
| Terroir match | One Saudi parcel against one Yemen district across eleven normalised factors |
| Crop cycle | Vegetation calendar, irrigation demand by month, inputs, labour, pest pressure |
| Scoring model | The weights behind every score — drag them and the whole tool re-ranks |

## Maps

The map is a built-in renderer: real coastlines and borders, with a hillshaded
elevation model of the Sarawat range built from ridge geometry plus fractal
roughness. Pan, zoom, and click a marker to select a site.

Press **Google map** on any map to swap in live Google Maps imagery. It asks once for
a Maps JavaScript API key and keeps it in `localStorage` on that browser only. This
works when the file is served from your own domain or opened locally; a published
artifact sandbox blocks third-party map scripts, and the tool says so and stays on
the built-in relief model.

## Data

Sites are real growing districts with real coordinates. The agronomic values —
rainfall, fog days, soil, water security, yields, cup scores — are modelled estimates
assembled for demonstration, not field survey. The Scoring model tab spells out what
the model does and does not know.
