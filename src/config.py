# =============================================================================
# PROJECT INFORMATION
# =============================================================================

PROJECT_NAME = "GPS Route Analysis Assignment"

PROJECT_VERSION = "1.0.0"

AUTHOR = "Omkar Chunekar"

"""
config.py
---------

Central configuration file for the GPS Assignment project.

Author  : Omkar Chunekar
Python  : 3.13+
Project : GPS Dataset Processing

This module stores:

1. Folder locations
2. Input/Output paths
3. CSV column definitions
4. Validation limits
5. Map styling
6. Plot styling
"""

from pathlib import Path

# =============================================================================
# PROJECT DIRECTORIES
# =============================================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

DATA_DIR = PROJECT_ROOT / "data"

OUTPUT_DIR = PROJECT_ROOT / "output"

# =============================================================================
# FILE DISCOVERY
# =============================================================================

CSV_EXTENSION = ".csv"

# =============================================================================
# REQUIRED CSV COLUMNS
# =============================================================================

CSV_COLUMNS = {
    "timestamp": "Timestamp",
    "latitude": "Latitude",
    "longitude": "Longitude",
    "altitude": "Altitude",
    "speed": "Speed_kmph",
    "heading": "Heading_deg",
    "hdop": "HDOP",
    "satellites": "Satellites",
}

# =============================================================================
# GPS VALIDATION LIMITS
# =============================================================================

MIN_LATITUDE = -90.0
MAX_LATITUDE = 90.0

MIN_LONGITUDE = -180.0
MAX_LONGITUDE = 180.0

MIN_ALTITUDE = -500.0
MAX_ALTITUDE = 10000.0

MIN_SPEED = 0.0
MAX_SPEED = 500.0

MIN_HEADING = 0.0
MAX_HEADING = 360.0

# =============================================================================
# EARTH PARAMETERS
# =============================================================================

EARTH_RADIUS_METRES = 6371000

# =============================================================================
# MAP SETTINGS
# =============================================================================

DEFAULT_ZOOM = 15

ROUTE_COLOUR = "blue"

ROUTE_WEIGHT = 4

ROUTE_OPACITY = 0.80

START_MARKER_COLOUR = "green"

END_MARKER_COLOUR = "red"

# =============================================================================
# REPORT SETTINGS
# =============================================================================

REPORT_TITLE = "GPS Mission Analysis Report"

COMPANY_NAME = "GPS Route Processing System"

# =============================================================================
# PLOT SETTINGS
# =============================================================================

ELEVATION_FIGSIZE = (12, 5)

ELEVATION_DPI = 150

# =============================================================================
# APPLICATION SETTINGS
# =============================================================================

VERBOSE = True