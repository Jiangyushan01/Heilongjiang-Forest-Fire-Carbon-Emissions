# Driving Factor Preprocessing and OLS, GWR, and GTWR Modeling Workflow

## 1. Purpose

To investigate the relationships between different driving factors and forest fire CO₂ emissions, as well as their spatial and temporal heterogeneity, Ordinary Least Squares (OLS), Geographically Weighted Regression (GWR), and Geographically and Temporally Weighted Regression (GTWR) models were applied sequentially in this study.

Before model construction, the forest fire CO₂ emission data and all driving factors were spatially harmonized, matched to a common spatial scale, and standardized.

## 2. Driving Factors and Data Preprocessing

Forest fire CO₂ emissions were used as the dependent variable. Candidate driving factors included meteorological, topographic, vegetation, human-activity, and socioeconomic variables:

- Mean Air Temperature (MAT)
- Total Precipitation (TP)
- Wind Speed (WS)
- Relative Humidity (RH)
- Potential Evaporation (PEV)
- Slope (SLP)
- Aspect (ASP)
- Elevation (ELE)
- Fractional Vegetation Cover (FVC)
- Distance to Nearest Railway (D_rail)
- Distance to Nearest Road (D_road)
- Population Density (PD)
- Gross Domestic Product (GDP)

To ensure consistency in spatial scale, a **0.1° grid** covering Heilongjiang Province was established and used as the basic spatial analysis unit for regression modeling.

The original forest fire CO₂ emission data at 30 m spatial resolution were aggregated to the 0.1° grid. The driving factors were spatially matched to the corresponding 0.1° grid cells according to their original spatial resolutions and data characteristics. For variables containing multiple original spatial units within a single grid cell, appropriate spatial aggregation was performed according to the characteristics of each variable.

After spatial matching, grid-year records with zero forest fire CO₂ emissions were excluded. A total of **4,698 valid grid-year observations** were retained for subsequent regression analyses.

To eliminate the influence of differences in measurement units and magnitude among variables, forest fire CO₂ emissions and all driving factors were standardized using **Z-score standardization**.

## 3. OLS Model and Variable Screening

The OLS model was first used to examine the global linear relationships between forest fire CO₂ emissions and the candidate driving factors.

The OLS model was implemented in **R** using the `lm()` function from the `stats` package.

During the OLS analysis:

- Variance Inflation Factors (VIFs) were calculated to assess multicollinearity among the explanatory variables.
- Statistical significance tests were performed for the candidate driving factors.
- All VIF values were below 5, indicating no serious multicollinearity among the explanatory variables.

The OLS significance test indicated that MAT and GDP were not statistically significant. Therefore, the OLS results were initially used as a criterion for variable screening.

Because OLS is a global regression model, its significance results may not fully capture spatial and temporal heterogeneity in the relationships between driving factors and forest fire CO₂ emissions. Therefore, GTWR models with and without MAT and GDP were further compared.

The comparison showed that including MAT and GDP did not improve the overall model fit. These two variables were therefore excluded from the final model.

The final set of explanatory variables used for the OLS, GWR, and GTWR model comparison consisted of:

- TP
- WS
- RH
- PEV
- SLP
- ASP
- ELE
- FVC
- D_rail
- D_road
- PD

A total of **11 explanatory variables** were retained.

## 4. GWR Model

The GWR model was further constructed based on the OLS framework.

GWR incorporates spatial location into the local regression process, allowing regression coefficients to vary across space and thereby capturing spatial non-stationarity in the relationships between different driving factors and forest fire CO₂ emissions.

Unlike OLS, which estimates a single global coefficient for each explanatory variable, GWR estimates local regression coefficients for different spatial locations, making it possible to characterize spatial differences in both the direction and magnitude of the effects of the driving factors.

## 5. GTWR Model

The GTWR model was constructed by further incorporating the temporal dimension into the GWR framework, allowing both spatial and temporal non-stationarity in the relationships between the driving factors and forest fire CO₂ emissions to be characterized.

The following spatiotemporal information was used in the GTWR model:

- Spatial coordinates: longitude and latitude
- Temporal variable: Year
- Number of valid observations: 4,698 grid-year observations

GTWR constructs a spatiotemporal distance based on the spatial and temporal distances among observations, which is then used to determine local weights.

The main GTWR parameter settings used in this study were as follows:

- Kernel function: **fixed Gaussian kernel**
- Distance metric: **Euclidean distance**
- Bandwidth optimization method: **AICc**
- Optimal bandwidth: **0.114996**
- Spatiotemporal distance ratio: **0.8149**

The GTWR model estimated local regression coefficients for different spatial locations and years, allowing the spatiotemporal heterogeneity in the relationships between the driving factors and forest fire CO₂ emissions to be examined.

## 6. Software and GTWR Add-in

The OLS model was implemented in **R**.

The GWR and GTWR models were implemented in **ArcGIS 10.8** using the **GTWR Add-in (GTWR Beta 1.0)**, an extension for implementing the GTWR method proposed by Huang et al.

GTWR is not a native analytical tool in ArcGIS 10.8; therefore, the GTWR Add-in was used to conduct the corresponding GWR and GTWR analyses.

The GTWR method used in this study follows:

> Huang, B.; Wu, B.; Barry, M. Geographically and Temporally Weighted Regression for Modeling Spatio-Temporal Variation in House Prices. *International Journal of Geographical Information Science*, 2010, 24, 383–401.

## 7. Model Evaluation

The following indicators were used to evaluate and compare the performance of the OLS, GWR, and GTWR models:

- Coefficient of determination (R²)
- Adjusted coefficient of determination (Adjusted R²)
- Corrected Akaike Information Criterion (AICc)

Higher values of R² and Adjusted R² indicate greater explanatory power of the model, whereas lower AICc values indicate a better balance between model fit and model complexity.

The three models were compared using these evaluation metrics to assess the improvement in model performance after incorporating spatial and temporal non-stationarity.
