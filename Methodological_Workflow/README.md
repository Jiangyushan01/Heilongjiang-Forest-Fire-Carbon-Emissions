# Methodological Workflow Documentation

This folder provides supplementary documentation of the main methodological steps used in this study to improve methodological transparency and reproducibility.

For methodological procedures implemented using Python or Google Earth Engine (GEE), the corresponding source code is provided in the `Code` directory of this repository. For procedures conducted using ArcGIS 10.8 or related extensions, for which no standalone source code was generated, this folder provides documentation of the methodological workflow, major processing steps, key parameter settings, and software implementation.

This folder currently contains the following documentation:

1. **01_Burned_Area_Fusion.md**  
   Describes the preprocessing of the FireCCI51 and MCD64A1 burned-area datasets, the monthly burned-area fusion rules, and the subsequent extraction of forest burned areas.

2. **02_Spatial_Autocorrelation.md**  
   Describes the workflow for Global Moran's I and Local Moran's I (LISA) analyses based on county-level administrative units, including the analytical purpose, spatial-relationship settings, significance testing, and main outputs.

3. **03_OLS_GWR_GTWR_Workflow.md**  
   Describes the preprocessing of driving-factor data and the implementation of the OLS, GWR, and GTWR models, including variable screening, spatial matching at the 0.1° grid scale, Z-score standardization, GTWR parameter settings, and software implementation. The GWR and GTWR models were implemented in ArcGIS 10.8 using the GTWR Add-in (GTWR Beta 1.0).
