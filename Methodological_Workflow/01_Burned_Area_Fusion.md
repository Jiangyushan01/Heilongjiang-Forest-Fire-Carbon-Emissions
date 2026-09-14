# Burned Area Data Fusion Workflow

## 1. Input Data

Two satellite-based burned-area products were used in this study:

- **FireCCI51**: 250 m spatial resolution, monthly temporal resolution, covering 2001–2020.
- **MCD64A1**: 500 m spatial resolution, monthly temporal resolution, covering 2001–2022.

Both burned-area products were acquired through the Google Earth Engine (GEE) platform and processed at the monthly scale.

## 2. Data Preprocessing

FireCCI51 and MCD64A1 data were first clipped to the Heilongjiang Province study area and reprojected to a common coordinate system.

Burned areas were calculated based on raster geometry, and the processed burned-area data were converted to polygon features containing burn perimeters, burned-area information, and the corresponding year and month.

## 3. Burned Area Fusion

Because FireCCI51 has a finer spatial resolution than MCD64A1, priority was given to FireCCI51 during the fusion process.

The fusion procedure was conducted separately for each year and month as follows:

1. FireCCI51 and MCD64A1 burned-area data were matched according to year and month.
2. The MCD64A1 burned-area polygons were converted to point features.
3. The MCD64A1 point features were spatially overlaid with the FireCCI51 burned-area polygons from the corresponding year and month.
4. When an MCD64A1 point fell within a FireCCI51 burned-area polygon, the corresponding MCD64A1 polygon feature was considered spatially overlapping and was removed.
5. MCD64A1 polygon features that did not overlap with FireCCI51 were retained.
6. The retained MCD64A1 polygons were merged with the FireCCI51 burned-area polygons to generate the final monthly fused burned-area dataset.

This rule-based fusion procedure was designed to retain the burned-area information from the higher-resolution product while supplementing non-overlapping burned areas detected by MCD64A1.

## 4. Extraction of Forest Burned Areas

The monthly fused burned-area data were further spatially overlaid with the corresponding annual GLC_FCS30D land-cover dataset to extract burned areas located within forest regions.

GLC_FCS30D classifies forests into five forest types:

- Evergreen Broadleaf Forest (EBF)
- Deciduous Broadleaf Forest (DBF)
- Evergreen Needleleaf Forest (ENF)
- Deciduous Needleleaf Forest (DNF)
- Mixed Forest (MF)

No burned pixels were identified in EBF or MF during the 2001–2022 study period. Therefore, only DBF, ENF, and DNF were retained for the subsequent forest fire carbon emission estimation.

The extracted forest burned-area data were subsequently used for carbon emission estimation at the 30 m spatial scale.
