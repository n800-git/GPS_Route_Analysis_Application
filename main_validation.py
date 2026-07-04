from src.file_manager import discover_datasets
from src.data_processing import (
    process_dataset,
    print_validation_summary,
)
from src.route_analysis import (
    analyse_route,
    print_route_statistics,
)

datasets = discover_datasets()

for dataset in datasets:

    print(f"\nProcessing: {dataset.name}")

    result = process_dataset(dataset)

    print_validation_summary(result.validation)

    statistics = analyse_route(result.dataframe)

    print_route_statistics(statistics)