"""
utils.py
---------

Common utility functions used throughout the GPS Assignment.

This module provides:

• Timestamp conversion
• Haversine distance calculation
• Coordinate validation
• Numeric validation
• Safe rounding
• Dataset summary formatting

Author  : <Your Name>
Python  : 3.13+
"""

from __future__ import annotations

from datetime import datetime
from math import radians, sin, cos, sqrt, atan2

from src.config import (
    EARTH_RADIUS_METRES,
    MIN_LATITUDE,
    MAX_LATITUDE,
    MIN_LONGITUDE,
    MAX_LONGITUDE,
)


# =============================================================================
# TIMESTAMP
# =============================================================================

def parse_timestamp(timestamp: str):
    """
    Convert ISO-8601 timestamp into datetime.
    """
  
    return datetime.strptime(
        timestamp, "%Y-%m-%dT%H:%M:%S"
    )


# =============================================================================
# DISTANCE
# =============================================================================

def haversine_distance(
    lat1: float,
    lon1: float,
    lat2: float,
    lon2: float,
) -> float:
    """
    Calculate great-circle distance between two GPS coordinates.

    Returns
    -------
    float
        Distance in metres.
    """

    lat1 = radians(lat1)
    lon1 = radians(lon1)

    lat2 = radians(lat2)
    lon2 = radians(lon2)

    delta_lat = lat2 - lat1
    delta_lon = lon2 - lon1

    a = (
        sin(delta_lat / 2) ** 2
        + cos(lat1) * cos(lat2) * sin(delta_lon / 2) ** 2
    )

    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    return EARTH_RADIUS_METRES * c


# =============================================================================
# VALIDATION
# =============================================================================

def valid_coordinate(latitude: float, longitude: float) -> bool:
    """
    Validate latitude and longitude.
    """

    if latitude < MIN_LATITUDE:
        return False

    if latitude > MAX_LATITUDE:
        return False

    if longitude < MIN_LONGITUDE:
        return False

    if longitude > MAX_LONGITUDE:
        return False

    return True


def is_missing(value) -> bool:
    """
    Returns True if a value is missing.
    """

    if value is None:
        return True

    try:
        if value != value:
            return True
    except Exception:
        pass

    return False


# =============================================================================
# NUMERIC HELPERS
# =============================================================================

def safe_round(value, digits: int = 2):
    """
    Round only numeric values.

    Missing values are returned unchanged.
    """

    if is_missing(value):
        return value

    return round(float(value), digits)


def metres_to_kilometres(distance_m: float) -> float:
    """
    Convert metres to kilometres.
    """

    return distance_m / 1000.0


# =============================================================================
# TIME
# =============================================================================

def mission_duration(start: datetime, end: datetime):
    """
    Return mission duration.

    Returns
    -------
    tuple
        (seconds, HH:MM:SS string)
    """

    duration = end - start

    total_seconds = int(duration.total_seconds())

    hours = total_seconds // 3600

    minutes = (total_seconds % 3600) // 60

    seconds = total_seconds % 60

    formatted = f"{hours:02d}:{minutes:02d}:{seconds:02d}"

    return total_seconds, formatted


# =============================================================================
# REPORT HELPERS
# =============================================================================

def print_heading(title: str):
    """
    Print a formatted console heading.
    """

    line = "=" * 70

    print()

    print(line)

    print(title)

    print(line)


def print_key_value(key: str, value):
    """
    Pretty console output.
    """

    print(f"{key:<35}: {value}")