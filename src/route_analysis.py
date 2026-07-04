"""
route_analysis.py
-----------------

Performs statistical analysis on a cleaned GPS dataset.

Responsibilities
----------------
1. Calculate total distance
2. Calculate mission duration
3. Calculate altitude statistics
4. Calculate optional speed statistics
5. Calculate optional heading statistics

Author : Omkar Chunekar
"""

from __future__ import annotations

import pandas as pd

from src.config import CSV_COLUMNS
from src.models import RouteStatistics
from src.utils import (
    haversine_distance,
    metres_to_kilometres,
    mission_duration,
)


# =============================================================================
# MAIN ANALYSIS
# =============================================================================

def analyse_route(dataframe: pd.DataFrame) -> RouteStatistics:
    """
    Analyse a cleaned GPS dataframe.

    Parameters
    ----------
    dataframe : pandas.DataFrame

    Returns
    -------
    RouteStatistics
    """

    statistics = RouteStatistics()

    if dataframe.empty:
        return statistics

    statistics.total_distance_m = calculate_total_distance(
        dataframe
    )

    statistics.total_distance_km = metres_to_kilometres(
        statistics.total_distance_m
    )

    calculate_mission_duration(
        dataframe,
        statistics,
    )

    calculate_altitude_statistics(
        dataframe,
        statistics,
    )

    calculate_speed_statistics(
        dataframe,
        statistics,
    )

    calculate_heading_statistics(
        dataframe,
        statistics,
    )

    return statistics


# =============================================================================
# DISTANCE
# =============================================================================

def calculate_total_distance(
    dataframe: pd.DataFrame,
) -> float:
    """
    Calculate total travelled distance.
    """

    latitude = CSV_COLUMNS["latitude"]
    longitude = CSV_COLUMNS["longitude"]

    total_distance = 0.0

    for index in range(1, len(dataframe)):

        previous = dataframe.iloc[index - 1]
        current = dataframe.iloc[index]

        total_distance += haversine_distance(
            previous[latitude],
            previous[longitude],
            current[latitude],
            current[longitude],
        )

    return total_distance

# =============================================================================
# MISSION DURATION
# =============================================================================

def calculate_mission_duration(
    dataframe: pd.DataFrame,
    statistics: RouteStatistics,
):
    """
    Calculate total mission duration.
    """

    timestamp_column = CSV_COLUMNS["timestamp"]

    start_time = dataframe.iloc[0][timestamp_column]

    end_time = dataframe.iloc[-1][timestamp_column]

    seconds, text = mission_duration(
        start_time,
        end_time,
    )

    statistics.mission_duration_seconds = seconds
    statistics.mission_duration_text = text


# =============================================================================
# ALTITUDE
# =============================================================================

def calculate_altitude_statistics(
    dataframe: pd.DataFrame,
    statistics: RouteStatistics,
):
    """
    Calculate altitude statistics.
    """

    altitude = CSV_COLUMNS["altitude"]

    statistics.maximum_altitude = float(
        dataframe[altitude].max()
    )

    statistics.minimum_altitude = float(
        dataframe[altitude].min()
    )

    statistics.average_altitude = float(
        dataframe[altitude].mean()
    )


# =============================================================================
# SPEED
# =============================================================================

def calculate_speed_statistics(
    dataframe: pd.DataFrame,
    statistics: RouteStatistics,
):
    """
    Calculate speed statistics if available.
    """

    speed_column = CSV_COLUMNS["speed"]

    if speed_column not in dataframe.columns:
        return

    speed = dataframe[speed_column].dropna()

    if speed.empty:
        return

    statistics.average_speed = float(
        speed.mean()
    )

    statistics.maximum_speed = float(
        speed.max()
    )


# =============================================================================
# HEADING
# =============================================================================

def calculate_heading_statistics(
    dataframe: pd.DataFrame,
    statistics: RouteStatistics,
):
    """
    Calculate average heading if available.
    """

    heading_column = CSV_COLUMNS["heading"]

    if heading_column not in dataframe.columns:
        return

    heading = dataframe[heading_column].dropna()

    if heading.empty:
        return

    statistics.average_heading = float(
        heading.mean()
    )


# =============================================================================
# CONSOLE OUTPUT
# =============================================================================

def print_route_statistics(
    statistics: RouteStatistics,
):
    """
    Display route statistics.
    """

    print()

    print("=" * 70)
    print("Route Analysis")
    print("=" * 70)

    print(
        f"Distance (m)          : "
        f"{statistics.total_distance_m:.2f}"
    )

    print(
        f"Distance (km)         : "
        f"{statistics.total_distance_km:.3f}"
    )

    print(
        f"Mission Duration      : "
        f"{statistics.mission_duration_text}"
    )

    print(
        f"Maximum Altitude      : "
        f"{statistics.maximum_altitude:.2f}"
    )

    print(
        f"Minimum Altitude      : "
        f"{statistics.minimum_altitude:.2f}"
    )

    print(
        f"Average Altitude      : "
        f"{statistics.average_altitude:.2f}"
    )

    if statistics.average_speed is not None:

        print(
            f"Average Speed         : "
            f"{statistics.average_speed:.2f}"
        )

        print(
            f"Maximum Speed         : "
            f"{statistics.maximum_speed:.2f}"
        )

    if statistics.average_heading is not None:

        print(
            f"Average Heading       : "
            f"{statistics.average_heading:.2f}"
        )

    print("=" * 70)