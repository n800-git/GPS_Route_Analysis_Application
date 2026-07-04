"""
models.py
---------

Data models used throughout the project.

Author : Omkar Chunekar
"""

from dataclasses import dataclass, field
from typing import Optional

import pandas as pd


@dataclass
class ValidationSummary:
    """
    Stores validation statistics.
    """

    total_records: int = 0
    valid_records: int = 0
    invalid_records: int = 0

    duplicate_records: int = 0

    missing_timestamp: int = 0
    missing_coordinates: int = 0
    invalid_coordinates: int = 0

    missing_altitude: int = 0

    missing_speed: int = 0
    missing_heading: int = 0

    errors: list[str] = field(default_factory=list)


@dataclass
class ProcessingResult:
    """
    Returned by data_processing.py.
    """

    dataframe: pd.DataFrame

    validation: ValidationSummary


@dataclass
class RouteStatistics:
    """
    Stores route analysis results.
    """

    total_distance_m: float = 0.0
    total_distance_km: float = 0.0

    mission_duration_seconds: int = 0
    mission_duration_text: str = "00:00:00"

    maximum_altitude: Optional[float] = None
    minimum_altitude: Optional[float] = None
    average_altitude: Optional[float] = None

    average_speed: Optional[float] = None
    maximum_speed: Optional[float] = None

    average_heading: Optional[float] = None