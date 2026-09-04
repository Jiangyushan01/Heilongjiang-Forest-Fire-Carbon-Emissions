import ee
import geemap
import os

# Earth Engine project
PROJECT_ID = "your-earth-engine-project"

# GEE asset directory
ASSET_BASE = "projects/your-project/assets"

# Local output directory
OUTPUT_DIR = "/path/to/your/output_directory"

# Processing period
START_YEAR = 2001
END_YEAR = 2022

ee.Initialize(project=PROJECT_ID)

os.makedirs(
    OUTPUT_DIR,
    exist_ok=True
)

# Download combustion efficiency for each year
for year in range(START_YEAR, END_YEAR + 1):

    asset_path = (
        f"{ASSET_BASE}/CF_classified_{year}"
    )

    output_path = (
        f"{OUTPUT_DIR}/CF_classified_{year}.tif"
    )

    asset_image = ee.Image(asset_path)

    geemap.download_ee_image(
        image=asset_image,
        filename=output_path,
        crs="EPSG:4326",
        scale=30
    )

    print(
        f"Combustion efficiency GeoTIFF "
        f"download completed: {year}"
    )