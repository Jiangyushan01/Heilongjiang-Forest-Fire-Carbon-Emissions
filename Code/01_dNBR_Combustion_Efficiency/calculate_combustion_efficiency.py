import ee
import time

# Earth Engine project and study area
PROJECT_ID = "your-earth-engine-project"
ROI_ASSET = "projects/your-project/assets/heilongjiang"

# Processing period
START_YEAR = 2001
END_YEAR = 2022

# NBR data period required for dNBR calculation
NBR_START_YEAR = START_YEAR - 1
NBR_END_YEAR = END_YEAR + 1

ee.Authenticate()
ee.Initialize(project=PROJECT_ID)

roi = ee.FeatureCollection(ROI_ASSET)

# Load GLC-FCS30D data
annual = ee.ImageCollection(
    "projects/sat-io/open-datasets/GLC-FCS30D/annual"
)

GLC_FCS30D_annual = annual.mosaic()

# Build the GLC-FCS30D time series for the processing period
GLC_FCS30D = ee.Image()

for year in range(START_YEAR, END_YEAR + 1):

    band_index = year - 1999

    GLC_FCS30D = GLC_FCS30D.addBands(
        GLC_FCS30D_annual.select(f"b{band_index}")
        .rename(f"GLC_FCS30D_{year}")
    )

# Load Landsat annual NBR data
NBR = (
    ee.ImageCollection(
        "LANDSAT/COMPOSITES/C02/T1_L2_ANNUAL_NBR"
    )
    .filterDate(
        f"{NBR_START_YEAR}-01-01",
        f"{NBR_END_YEAR + 1}-01-01"
    )
    .filterBounds(roi)
)

# Neighborhood interpolation
def interpolateIDW(image):
    return image.unmask().reduceNeighborhood(
        reducer=ee.Reducer.mean(),
        kernel=ee.Kernel.square(3),
        skipMasked=True
    )

# Calculate combustion efficiency for each year
for year in range(START_YEAR, END_YEAR + 1):

    # NBR before the fire
    NBR_before = (
        NBR.filter(
            ee.Filter.calendarRange(
                year - 1,
                year - 1,
                "year"
            )
        )
        .select("NBR")
        .reduce(ee.Reducer.intervalMean(30, 70))
        .clip(roi)
    )

    # NBR after the fire
    NBR_after = (
        NBR.filter(
            ee.Filter.calendarRange(
                year + 1,
                year + 1,
                "year"
            )
        )
        .select("NBR")
        .reduce(ee.Reducer.intervalMean(30, 70))
        .clip(roi)
        .reproject(
            crs="EPSG:4326",
            scale=30
        )
    )

    # Calculate dNBR
    dNBR_raw = NBR_before.subtract(NBR_after).rename("dNBR")
    dNBR_interpolated = interpolateIDW(dNBR_raw)

    # Load annual land-cover classification
    glc_current = (
        GLC_FCS30D
        .select(f"GLC_FCS30D_{year}")
        .rename("GLC")
    )

    # Forest classes
    remap_values = [
        51, 52, 61, 62, 71, 72, 81, 82, 91, 92
    ]

    remap = glc_current.remap(
        remap_values,
        ee.List.repeat(1, len(remap_values)),
        0
    )

    # Apply forest mask and dNBR threshold
    dNBR_mask = (
        dNBR_interpolated
        .updateMask(remap.eq(1))
        .reproject(
            crs="EPSG:4326",
            scale=30
        )
        .where(
            dNBR_interpolated.lt(-9),
            -9
        )
        .where(
            dNBR_interpolated.gt(9),
            9
        )
        .updateMask(
            dNBR_interpolated.gt(0.2)
        )
        .clip(roi)
    )

    # Calculate combustion efficiency
    def calculate_CF(glc_img, dnbr_img):

        conifer_mask = (
            glc_img.eq(71)
            .Or(glc_img.eq(72))
            .Or(glc_img.eq(81))
            .Or(glc_img.eq(82))
        )

        deciduous_mask = (
            glc_img.eq(51)
            .Or(glc_img.eq(52))
            .Or(glc_img.eq(61))
            .Or(glc_img.eq(62))
        )

        mixed_forest_mask = (
            glc_img.eq(91)
            .Or(glc_img.eq(92))
        )

        conifer_cf = (
            dnbr_img.expression(
                "dNBR < 1 ? exp(1.029 * dNBR - 1.052) : 1",
                {"dNBR": dnbr_img}
            )
            .rename("conifer_cf")
        )

        deciduous_cf = (
            dnbr_img.expression(
                "dNBR < 1 ? exp(1.669 * dNBR - 1.618) : 1",
                {"dNBR": dnbr_img}
            )
            .rename("deciduous_cf")
        )

        mixed_cf = (
            conifer_cf.add(deciduous_cf)
            .divide(2)
            .rename("mixed_cf")
        )

        cf_image = ee.Image(0).toFloat().rename("CF")

        cf_image = cf_image.where(
            conifer_mask,
            conifer_cf
        )

        cf_image = cf_image.where(
            deciduous_mask,
            deciduous_cf
        )

        cf_image = cf_image.where(
            mixed_forest_mask,
            mixed_cf
        )

        return cf_image.updateMask(remap.eq(1))

    cf_image = calculate_CF(
        glc_current,
        dNBR_mask
    )

    # Prepare the final 30 m image
    cf_image_final = (
        cf_image
        .reproject(
            crs="EPSG:4326",
            scale=30
        )
        .clip(roi)
    )

    # Export combustion efficiency to GEE Asset
    asset_id = (
        f"{ROI_ASSET.rsplit('/', 1)[0]}/"
        f"CF_classified_{year}"
    )

    task = ee.batch.Export.image.toAsset(
        image=cf_image_final,
        description=f"CF_classified_{year}_export",
        assetId=asset_id,
        region=roi.geometry(),
        scale=30,
        maxPixels=1e13
    )

    task.start()

    print(
        f"Task started for {year}: {task.id}"
    )

    start_time = time.time()
    timeout = 3600

    while (
        task.active()
        and (time.time() - start_time) < timeout
    ):

        status = task.status()
        state = status["state"]

        print(
            f"{year}: {state}"
        )

        if state in [
            "COMPLETED",
            "FAILED",
            "CANCELED"
        ]:
            break

        time.sleep(120)

    final_status = task.status()

    if final_status["state"] == "COMPLETED":

        print(
            f"Export completed: {asset_id}"
        )

    elif final_status["state"] == "FAILED":

        print(
            f"Export failed for {year}: "
            f"{final_status.get('error_message', 'Unknown error')}"
        )

    else:

        print(
            f"Task not completed for {year}: "
            f"{final_status['state']}"
        )