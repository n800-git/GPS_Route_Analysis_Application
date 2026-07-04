"""
data_processing.py
------------------

Reads and validates GPS datasets.

Responsibilities
----------------
1. Load CSV
2. Validate mandatory columns
3. Parse timestamps
4. Validate coordinates
5. Detect missing values
6. Build validation summary

Author : Omkar Chunekar
"""

from pathlib import Path

import pandas as pd

from src.config import CSV_COLUMNS
from src.models import ProcessingResult
from src.models import ValidationSummary
from src.utils import (
    parse_timestamp,
    valid_coordinate,
    is_missing,
)


# =============================================================================
# REQUIRED COLUMNS
# =============================================================================

MANDATORY_COLUMNS = [
    CSV_COLUMNS["timestamp"],
    CSV_COLUMNS["latitude"],
    CSV_COLUMNS["longitude"],
    CSV_COLUMNS["altitude"],
]

OPTIONAL_COLUMNS = [
    CSV_COLUMNS["speed"],
    CSV_COLUMNS["heading"],
    CSV_COLUMNS["hdop"],
    CSV_COLUMNS["satellites"],
]


# =============================================================================
# CSV LOADER
# =============================================================================

def process_dataset(csv_path: Path) -> ProcessingResult:
    """
    Load and validate a GPS dataset.

    Parameters
    ----------
    csv_path : Path

    Returns
    -------
    ProcessingResult
    """

    summary = ValidationSummary()

    try:
        dataframe = pd.read_csv(csv_path)

    except Exception as error:

        summary.errors.append(str(error))

        return ProcessingResult(
            dataframe=pd.DataFrame(),
            validation=summary,
        )

    summary.total_records = len(dataframe)

    validate_required_columns(dataframe)

    dataframe = convert_timestamp_column(
        dataframe,
        summary,
    )

    dataframe = validate_records(
        dataframe,
        summary,
    )

    return ProcessingResult(
        dataframe=dataframe,
        validation=summary,
    )


# =============================================================================
# REQUIRED COLUMN CHECK
# =============================================================================

def validate_required_columns(
    dataframe: pd.DataFrame,
):
    """
    Raise an exception if mandatory columns
    are missing.
    """

    missing = []

    for column in MANDATORY_COLUMNS:

        if column not in dataframe.columns:
            missing.append(column)

    if missing:

        raise ValueError(
            f"Missing mandatory columns: {missing}"
        )


# =============================================================================
# TIMESTAMP CONVERSION
# =============================================================================

def convert_timestamp_column(
    dataframe: pd.DataFrame,
    summary: ValidationSummary,
):
    """
    Convert timestamp strings into datetime.
    """

    timestamp_column = CSV_COLUMNS["timestamp"]

    converted = []

    for value in dataframe[timestamp_column]:

        if is_missing(value):

            summary.missing_timestamp += 1

            converted.append(pd.NaT)

            continue

        try:

            converted.append(
                parse_timestamp(str(value))
            )

        except Exception:

            summary.missing_timestamp += 1

            converted.append(pd.NaT)

    dataframe[timestamp_column] = converted

    return dataframe

# =============================================================================
# RECORD VALIDATION
# =============================================================================

def validate_records(
    dataframe: pd.DataFrame,
    summary: ValidationSummary,
):
    """
    Validate every record in the dataset.

    Invalid rows are removed from the returned
    dataframe while their counts are recorded.
    """

    valid_rows = []

    latitude_column = CSV_COLUMNS["latitude"]
    longitude_column = CSV_COLUMNS["longitude"]
    altitude_column = CSV_COLUMNS["altitude"]

    has_speed = CSV_COLUMNS["speed"] in dataframe.columns
    has_heading = CSV_COLUMNS["heading"] in dataframe.columns

    for _, row in dataframe.iterrows():

        valid = True

        latitude = row[latitude_column]
        longitude = row[longitude_column]
        altitude = row[altitude_column]

        # ---------------------------------------------------------
        # Coordinate validation
        # ---------------------------------------------------------

        if (
            is_missing(latitude)
            or is_missing(longitude)
        ):

            summary.missing_coordinates += 1
            valid = False

        elif not valid_coordinate(
            latitude,
            longitude,
        ):

            summary.invalid_coordinates += 1
            valid = False

        # ---------------------------------------------------------
        # Altitude validation
        # ---------------------------------------------------------

        if is_missing(altitude):

            summary.missing_altitude += 1

        # ---------------------------------------------------------
        # Optional Speed
        # ---------------------------------------------------------

        if has_speed:

            if is_missing(
                row[CSV_COLUMNS["speed"]]
            ):
                summary.missing_speed += 1

        # ---------------------------------------------------------
        # Optional Heading
        # ---------------------------------------------------------

        if has_heading:

            if is_missing(
                row[CSV_COLUMNS["heading"]]
            ):
                summary.missing_heading += 1

        if valid:
            valid_rows.append(row)

    dataframe = pd.DataFrame(valid_rows)

    # -------------------------------------------------------------
    # Duplicate Removal
    # -------------------------------------------------------------

    rows_before = len(dataframe)

    dataframe = dataframe.drop_duplicates()

    rows_after = len(dataframe)

    summary.duplicate_records = (
        rows_before - rows_after
    )

    summary.valid_records = rows_after

    summary.invalid_records = (
        summary.total_records
        - summary.valid_records
    )

    dataframe = dataframe.reset_index(
        drop=True
    )

    return dataframe


# =============================================================================
# VALIDATION SUMMARY
# =============================================================================

def print_validation_summary(
    summary: ValidationSummary,
):
    """
    Print validation statistics.
    """

    print()

    print("=" * 70)
    print("Validation Summary")
    print("=" * 70)

    print(
        f"Total Records        : {summary.total_records}"
    )

    print(
        f"Valid Records        : {summary.valid_records}"
    )

    print(
        f"Invalid Records      : {summary.invalid_records}"
    )

    print(
        f"Duplicate Records    : {summary.duplicate_records}"
    )

    print(
        f"Missing Timestamp    : {summary.missing_timestamp}"
    )

    print(
        f"Missing Coordinates  : {summary.missing_coordinates}"
    )

    print(
        f"Invalid Coordinates  : {summary.invalid_coordinates}"
    )

    print(
        f"Missing Altitude     : {summary.missing_altitude}"
    )

    print(
        f"Missing Speed        : {summary.missing_speed}"
    )

    print(
        f"Missing Heading      : {summary.missing_heading}"
    )

    if summary.errors:

        print()

        print("Errors")

        for error in summary.errors:

            print(f" - {error}")

    print("=" * 70)