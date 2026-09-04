\# Heilongjiang Forest Fire Carbon Emissions



\## Project Overview



This repository contains the source code used to estimate forest fire carbon emissions in Heilongjiang Province, China, during 2001–2022.



\## Study Scope



\- Study area: Heilongjiang Province, China

\- Study period: 2001–2022

\- Spatial resolution: 30 m for emission estimation



\## Repository Structure



Code/

├── 01\_dNBR\_Combustion\_Efficiency/

│   ├── calculate\_combustion\_efficiency.py

│   └── export\_combustion\_efficiency.py

│

└── 02\_Emission\_Calculation/

&#x20;   ├── CO2\_emission\_calculation.py

&#x20;   ├── CO\_emission\_calculation.py

&#x20;   └── CH4\_emission\_calculation.py



\## Code Description



| Script | Description |

|---|---|

| `calculate\_combustion\_efficiency.py` | Calculates combustion efficiency based on dNBR and forest land-cover information. |

| `export\_combustion\_efficiency.py` | Exports the combustion efficiency results from Google Earth Engine to GeoTIFF format. |

| `CO2\_emission\_calculation.py` | Estimates forest fire CO₂ emissions in Heilongjiang Province, China, during 2001–2022. |

| `CO\_emission\_calculation.py` | Estimates forest fire CO emissions in Heilongjiang Province, China, during 2001–2022. |

| `CH4\_emission\_calculation.py` | Estimates forest fire CH₄ emissions in Heilongjiang Province, China, during 2001–2022. |

