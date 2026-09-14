# Spatial Autocorrelation Analysis Workflow

## 1. Purpose

Spatial autocorrelation analysis was conducted to characterize the spatial clustering of forest fire CO₂ emissions in Heilongjiang Province.

County-level administrative units were used as the basic spatial analysis units, and forest fire CO₂ emissions in each county were used as the analysis variable. Both Global Moran's I and Local Moran's I (LISA) were applied.

## 2. Global Moran's I

Global Moran's I was first used to evaluate the overall spatial autocorrelation of forest fire CO₂ emissions across the study area.

The interpretation of Global Moran's I is as follows:

- **Moran's I > 0** indicates positive spatial autocorrelation, meaning that spatial units with similar emission levels tend to cluster together.
- **Moran's I < 0** indicates negative spatial autocorrelation, meaning that spatial units with dissimilar emission levels tend to be spatially adjacent.
- **Moran's I close to 0** indicates an approximately random spatial distribution.

The statistical significance of the global spatial autocorrelation was evaluated using the corresponding Z-score and p-value.

## 3. Local Moran's I / LISA

Local Moran's I, a Local Indicator of Spatial Association (LISA), was further applied to identify local spatial clusters and spatial outliers.

Significant local spatial association patterns were classified into four categories:

- **High–High (H–H):** a high-emission county surrounded mainly by neighboring counties with high emission levels.
- **Low–Low (L–L):** a low-emission county surrounded mainly by neighboring counties with low emission levels.
- **High–Low (H–L):** a high-emission county surrounded mainly by neighboring counties with low emission levels.
- **Low–High (L–H):** a low-emission county surrounded mainly by neighboring counties with high emission levels.

H–H and L–L clusters represent positive local spatial autocorrelation, whereas H–L and L–H clusters represent negative local spatial autocorrelation.

## 4. Spatial Relationships and Significance Testing

Both Global Moran's I and Local Moran's I (LISA) analyses were conducted using the Spatial Statistics Tools in **ArcGIS 10.8**.

Spatial relationships among county-level administrative units were defined according to the corresponding spatial-relationship settings used in each analysis tool and were used to construct the spatial-weight relationships.

For the Local Moran's I analysis, a significance level of **p < 0.05** was used, and a **False Discovery Rate (FDR)** correction was applied to reduce the potential influence of multiple testing on the identification of statistically significant local spatial clusters.

## 5. Software and Outputs

The spatial autocorrelation analyses were conducted in **ArcGIS 10.8**.

The main outputs included:

- Global Moran's I;
- Z-score;
- p-value;
- LISA cluster maps;
- H–H, L–L, H–L, and L–H cluster categories.

These outputs were used to characterize both the overall spatial clustering and the local spatial heterogeneity of forest fire CO₂ emissions in Heilongjiang Province.
