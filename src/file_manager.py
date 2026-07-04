"""
file_manager.py
---------------

Responsible for:

• Discovering CSV datasets
• Creating output folders
• Returning paths used throughout the project
"""

from pathlib import Path

from src.config import DATA_DIR
from src.config import OUTPUT_DIR
from src.config import CSV_EXTENSION


def discover_datasets():
    """
    Discover every CSV file present in the data folder.

    Returns
    -------
    list[Path]
        Sorted list of CSV files.
    """

    csv_files = sorted(DATA_DIR.glob(f"*{CSV_EXTENSION}"))

    return csv_files


def create_output_folder(dataset_path: Path):
    """
    Creates an output directory for a dataset.

    Example

    Dataset_A_Clean_GPS.csv

    becomes

    output/
        Dataset_A_Clean_GPS/

    Parameters
    ----------
    dataset_path : Path

    Returns
    -------
    Path
        Output directory
    """

    folder_name = dataset_path.stem

    output_folder = OUTPUT_DIR / folder_name

    output_folder.mkdir(parents=True, exist_ok=True)

    return output_folder


def print_dataset_summary(csv_files):
    """
    Display all discovered datasets.
    """

    print("\nDatasets discovered\n")

    for index, file in enumerate(csv_files, start=1):

        print(f"{index}. {file.name}")

    print()

from pathlib import Path


# =============================================================================
# OUTPUT DIRECTORIES
# =============================================================================

OUTPUT_DIRECTORY = Path("output")


def get_dataset_output_directory(
    dataset_name: str,
) -> Path:
    """
    Create (if required) and return the
    output directory for a dataset.
    """

    directory = OUTPUT_DIRECTORY / dataset_name

    directory.mkdir(
        parents=True,
        exist_ok=True,
    )

    return directory


def build_output_path(
    dataset_name: str,
    filename: str,
) -> Path:
    """
    Build a file path inside the dataset
    output directory.
    """

    return (
        get_dataset_output_directory(
            dataset_name
        )
        / filename
    )