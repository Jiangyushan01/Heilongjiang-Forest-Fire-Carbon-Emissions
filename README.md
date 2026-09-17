# Heilongjiang Forest Fire Carbon Emissions

## Project Overview

This repository provides the source code and methodological workflow documentation used in the study of forest fire carbon emissions in Heilongjiang Province, China, during 2001–2022.

For methodological procedures implemented using Python or Google Earth Engine (GEE), the corresponding source code is provided in this repository. For procedures conducted using ArcGIS 10.8 or related extensions, for which no standalone source code was generated, supplementary documentation of the methodological workflow, major processing steps, key parameter settings, and software implementation is provided to improve methodological transparency and reproducibility.

## Study Scope

- Study area: Heilongjiang Province, China
- Study period: 2001–2022
- Spatial resolution: 30 m for emission estimation

## Repository Structure

```text
Code/
├── 01_dNBR_Combustion_Efficiency/
│   ├── calculate_combustion_efficiency.py
│   └── export_combustion_efficiency.py
│
└── 02_Emission_Calculation/
    ├── CO2_emission_calculation.py
    ├── CO_emission_calculation.py
    └── CH4_emission_calculation.py

Methodological_Workflow/
├── README.md
├── 01_Burned_Area_Fusion.md
├── 02_Spatial_Autocorrelation.md
└── 03_OLS_GWR_GTWR_Workflow.md

## Code Description

| Script | Description |
|---|---|
| `calculate_combustion_efficiency.py` | Calculates combustion efficiency based on dNBR and forest land-cover information. |
| `export_combustion_efficiency.py` | Exports the combustion efficiency results from Google Earth Engine to GeoTIFF format. |
| `CO2_emission_calculation.py` | Estimates forest fire CO₂ emissions in Heilongjiang Province, China, during 2001–2022. |
| `CO_emission_calculation.py` | Estimates forest fire CO emissions in Heilongjiang Province, China, during 2001–2022. |
| `CH4_emission_calculation.py` | Estimates forest fire CH₄ emissions in Heilongjiang Province, China, during 2001–2022. |

## Methodological Workflow

In addition to the source code provided above, the `Methodological_Workflow` folder provides supplementary documentation of the main methodological steps described in the manuscript.

1. **`01_Burned_Area_Fusion.md`**  
   Describes the preprocessing of the FireCCI51 and MCD64A1 burned-area datasets, the monthly fusion rules, and the extraction of forest burned areas.

2. **`02_Spatial_Autocorrelation.md`**  
   Describes the workflow and related settings for Global Moran's I and Local Moran's I (LISA) analyses based on county-level administrative units.

3. **`03_OLS_GWR_GTWR_Workflow.md`**  
   Describes the preprocessing of driving-factor data and the implementation workflow and main parameter settings for the OLS, GWR, and GTWR models.
