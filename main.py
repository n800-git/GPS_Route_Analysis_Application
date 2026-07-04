"""
GPS Assignment

Main Application Entry Point
"""

from pathlib import Path

from src.config import (
    VERBOSE,
    PROJECT_NAME,
    PROJECT_VERSION,
    AUTHOR,
)

from src.file_manager import (
    discover_datasets,
    build_output_path,
)

from src.data_processing import process_dataset
from src.route_analysis import analyse_route
from src.map_generator import create_route_map
from src.geojson_export import export_geojson
from src.report_generator import generate_report
from src.logger import get_logger


def print_header():

    print("=" * 60)
    print(PROJECT_NAME)
    print(f"Version {PROJECT_VERSION}")
    print(f"Author : {AUTHOR}")
    print("=" * 60)


def print_footer(processed):

    print("\n" + "=" * 60)
    print("PROCESSING COMPLETE")
    print("=" * 60)

    print(f"Datasets processed : {processed}")
    print("Interactive Maps   : Generated")
    print("GeoJSON Files      : Generated")
    print("HTML Reports       : Generated")
    print("Log File           : logs/gps_assignment.log")

    print("=" * 60)


def main():

    logger = get_logger()

    datasets = discover_datasets()

    if not datasets:

        print("No CSV datasets found.")
        logger.warning("No datasets found.")
        return

    if VERBOSE:
        print_header()
        print(f"\nDatasets discovered : {len(datasets)}\n")

    processed = 0

    for dataset in datasets:

        try:

            if VERBOSE:
                print("-" * 60)
                print(f"Processing : {dataset.name}")
                print("-" * 60)

            logger.info(f"Processing dataset: {dataset.name}")

            result = process_dataset(dataset)

            statistics = analyse_route(
                result.dataframe
            )

            dataset_name = dataset.stem

            map_file = build_output_path(
                dataset_name,
                "map.html",
            )

            geojson_file = build_output_path(
                dataset_name,
                "route.geojson",
            )

            report_file = build_output_path(
                dataset_name,
                "report.html",
            )

            create_route_map(
                result.dataframe,
                map_file,
            )

            export_geojson(
                result.dataframe,
                geojson_file,
            )

            generate_report(
                dataset_name=dataset_name,
                validation_summary=result.validation,
                route_statistics=statistics,
                output_file=report_file,
            )

            processed += 1

            logger.info(
                f"Finished dataset: {dataset.name}"
            )

            if VERBOSE:

                print("✓ Validation complete")
                print("✓ Route analysis complete")
                print("✓ HTML map created")
                print("✓ GeoJSON exported")
                print("✓ HTML report generated\n")

        except Exception as error:

            logger.exception(
                f"Failed processing {dataset.name}"
            )

            print(
                f"ERROR processing {dataset.name}"
            )

            print(error)

    if VERBOSE:
        print_footer(processed)

    logger.info(
        f"Application finished successfully. "
        f"Datasets processed: {processed}"
    )

if __name__ == "__main__":
    main()