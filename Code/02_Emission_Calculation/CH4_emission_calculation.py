#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import rasterio
import numpy as np


# ============================================================
# 1. Working directory
# ============================================================

WORK_DIR = "/path/to/your/work_directory"

efficiency_dir = os.path.join(
    WORK_DIR, "combustion_efficiency"
)

density_dir = os.path.join(
    WORK_DIR, "aboveground_biomass_density"
)

landcover_dir = os.path.join(
    WORK_DIR, "landcover"
)

output_dir_base = os.path.join(
    WORK_DIR, "ch4_results"
)

os.makedirs(output_dir_base, exist_ok=True)


# ============================================================
# 2. CH4 emission factors
# ============================================================

emission_factors_ch4 = {
    61: 5.61,
    62: 5.61,
    71: 6.0,
    72: 6.0,
    81: 6.0,
    82: 6.0,
}


# ============================================================
# 3. Processing period
# ============================================================

start_year = 2001
end_year = 2022
skip_years = []


def get_target_years():
    """Return the years to be processed."""

    years = []

    for year in range(start_year, end_year + 1):
        if year not in skip_years:
            years.append(year)

    return years


# ============================================================
# 4. Find available monthly input data
# ============================================================

def get_available_months(year):
    """Find months with all required input datasets."""

    available_months = []

    for month in range(1, 13):

        month_str = f"{year}{str(month).zfill(2)}"

        # Combustion efficiency file patterns
        eff_file_patterns = [
            os.path.join(
                efficiency_dir,
                f"{month_str}_efficiency.tif"
            ),
            os.path.join(
                efficiency_dir,
                f"{month_str}.tif"
            ),
        ]

        # Aboveground biomass density file patterns
        den_file_patterns = [
            os.path.join(
                density_dir,
                f"{month_str}_density.tif"
            ),
            os.path.join(
                density_dir,
                f"{month_str}.tif"
            ),
        ]

        # Land-cover file patterns
        lc_file_patterns = [
            os.path.join(
                landcover_dir,
                f"{month_str}_glc.tif"
            ),
            os.path.join(
                landcover_dir,
                f"{month_str}.tif"
            ),
        ]

        eff_file = None
        den_file = None
        lc_file = None

        for pattern in eff_file_patterns:
            if os.path.exists(pattern):
                eff_file = pattern
                break

        for pattern in den_file_patterns:
            if os.path.exists(pattern):
                den_file = pattern
                break

        for pattern in lc_file_patterns:
            if os.path.exists(pattern):
                lc_file = pattern
                break

        if eff_file and den_file and lc_file:

            available_months.append(
                (month_str, eff_file, den_file, lc_file)
            )

            print(f"Found data for {month_str}")
            print(
                f"  Efficiency: "
                f"{os.path.basename(eff_file)}"
            )
            print(
                f"  Density: "
                f"{os.path.basename(den_file)}"
            )
            print(
                f"  Land cover: "
                f"{os.path.basename(lc_file)}"
            )

        else:

            if year == start_year:

                print(
                    f"Data incomplete for {month_str}"
                )

                print(
                    "  Efficiency file exists: "
                    f"{os.path.exists(eff_file_patterns[0])}"
                )

                print(
                    "  Density file exists: "
                    f"{os.path.exists(den_file_patterns[0])}"
                )

                print(
                    "  Land cover file exists: "
                    f"{os.path.exists(lc_file_patterns[0])}"
                )

    return available_months


# ============================================================
# 5. Calculate annual CH4 emissions
# ============================================================

def calculate_ch4_for_year(year):

    output_dir = os.path.join(
        output_dir_base,
        f"output_ch4_{year}"
    )

    os.makedirs(output_dir, exist_ok=True)

    print(
        f"\nStarting CH4 emission calculation "
        f"for {year}..."
    )

    print("Checking input data directories...")

    print(
        "  Efficiency directory: "
        f"{'OK' if os.path.exists(efficiency_dir) else 'NOT FOUND'}"
    )

    print(
        "  Density directory: "
        f"{'OK' if os.path.exists(density_dir) else 'NOT FOUND'}"
    )

    print(
        "  Land-cover directory: "
        f"{'OK' if os.path.exists(landcover_dir) else 'NOT FOUND'}"
    )

    months_data = get_available_months(year)

    if not months_data:

        print(
            f"No complete input data found for {year}."
        )

        return 0

    print(
        f"Found {len(months_data)} month(s) of "
        f"complete data for {year}."
    )

    success_count = 0

    for month_data in months_data:

        month_str, eff_file, den_file, lc_file = month_data

        print("\n" + "=" * 60)
        print(f"Processing: {month_str}")

        print("Input files:")

        print(
            f"  Efficiency: "
            f"{os.path.basename(eff_file)}"
        )

        print(
            f"  Density: "
            f"{os.path.basename(den_file)}"
        )

        print(
            f"  Land cover: "
            f"{os.path.basename(lc_file)}"
        )

        out_file = os.path.join(
            output_dir,
            f"{month_str}_ch4.tif"
        )

        try:

            # Check input file sizes
            skip_month = False

            for f_path, f_name in [
                (eff_file, "Efficiency"),
                (den_file, "Density"),
                (lc_file, "Land cover")
            ]:

                size = os.path.getsize(f_path)

                print(
                    f"  {f_name} file size: "
                    f"{size:,} bytes"
                )

                if size == 0:

                    print(
                        f"  {f_name} file is empty. "
                        f"Skipping {month_str}."
                    )

                    skip_month = True
                    break

            if skip_month:
                continue

            # Read input data
            with rasterio.open(eff_file) as eff:

                efficiency = eff.read(1)
                efficiency_nodata = eff.nodata
                meta = eff.meta.copy()

            with rasterio.open(den_file) as den:

                density = den.read(1)
                density_nodata = den.nodata

            with rasterio.open(lc_file) as lc:

                landcover = lc.read(1)
                landcover_nodata = lc.nodata

            # Check raster dimensions
            if not (
                efficiency.shape
                == density.shape
                == landcover.shape
            ):

                print(
                    f"Input raster dimensions do not match "
                    f"for {month_str}: "
                    f"Efficiency {efficiency.shape} / "
                    f"Density {density.shape} / "
                    f"Land cover {landcover.shape}"
                )

                continue

            # Create valid data mask
            valid_mask = np.ones(
                efficiency.shape,
                dtype=bool
            )

            if efficiency_nodata is not None:
                valid_mask &= (
                    efficiency != efficiency_nodata
                )

            if density_nodata is not None:
                valid_mask &= (
                    density != density_nodata
                )

            if landcover_nodata is not None:
                valid_mask &= (
                    landcover != landcover_nodata
                )

            # Calculate CH4 emissions
            ch4_emission = np.zeros_like(
                efficiency,
                dtype=np.float64
            )

            emission_factor = np.zeros_like(
                landcover,
                dtype=np.float64
            )

            for code, factor in emission_factors_ch4.items():

                emission_factor[
                    (landcover == code) & valid_mask
                ] = factor

            ch4_emission[valid_mask] = (
                efficiency[valid_mask]
                * density[valid_mask]
                * 0.09
                * emission_factor[valid_mask]
            ) * 0.001

            # Set NoData values
            ch4_emission[~valid_mask] = (
                meta.get("nodata", -9999)
            )

            # Update output raster metadata
            meta.update({
                "dtype": "float64",
                "nodata": meta.get("nodata", -9999),
                "compress": "lzw"
            })

            # Save output raster
            with rasterio.open(
                out_file,
                "w",
                **meta
            ) as dst:

                dst.write(
                    ch4_emission,
                    1
                )

            # Calculate total CH4 emissions
            valid_ch4 = ch4_emission[valid_mask]

            total_emission = np.sum(
                valid_ch4
            )

            print(
                f"Completed {month_str}. "
                f"Total CH4 emissions: "
                f"{total_emission:.4f} Mg"
            )

            success_count += 1

        except Exception as e:

            print(
                f"Error processing {month_str}: "
                f"{str(e)}"
            )

            import traceback
            traceback.print_exc()

    print(
        f"\nCompleted {year}: "
        f"{success_count}/{len(months_data)} "
        f"months processed successfully."
    )

    return success_count


# ============================================================
# 6. Main program
# ============================================================

def main():

    print(
        "Starting CH4 emission calculation "
        "for 2001-2022..."
    )

    target_years = get_target_years()

    print(
        f"\nTarget years: {target_years}"
    )

    print(
        f"Number of years: "
        f"{len(target_years)}"
    )

    total_success_count = 0

    for i, year in enumerate(
        target_years,
        1
    ):

        print("\n" + "=" * 60)

        print(
            f"Progress: {i}/{len(target_years)} "
            f"(Year: {year})"
        )

        success_count = (
            calculate_ch4_for_year(year)
        )

        total_success_count += (
            success_count
        )

    print("\n" + "=" * 60)

    print(
        "CH4 emission calculation "
        "for 2001-2022 completed."
    )

    print(
        f"Total successfully processed months: "
        f"{total_success_count}"
    )


if __name__ == "__main__":
    main()