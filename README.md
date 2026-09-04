# Heilongjiang Forest Fire Carbon Emissions

## Project Overview

This repository contains the source code used to estimate forest fire carbon emissions in Heilongjiang Province, China, during 2001–2022.

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
```

## Code Description

| Script | Description |
|---|---|
| `calculate_combustion_efficiency.py` | Calculates combustion efficiency based on dNBR and forest land-cover information. |
| `export_combustion_efficiency.py` | Exports the combustion efficiency results from Google Earth Engine to GeoTIFF format. |
| `CO2_emission_calculation.py` | Estimates forest fire CO₂ emissions in Heilongjiang Province, China, during 2001–2022. |
| `CO_emission_calculation.py` | Estimates forest fire CO emissions in Heilongjiang Province, China, during 2001–2022. |
| `CH4_emission_calculation.py` | Estimates forest fire CH₄ emissions in Heilongjiang Province, China, during 2001–2022. |