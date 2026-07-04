"""
geojson_export.py
-----------------

Export GPS route to GeoJSON.
"""

from __future__ import annotations

import json
from pathlib import Path

import pandas as pd

from src.config import CSV_COLUMNS


def export_geojson(
    dataframe: pd.DataFrame,
    output_file: Path,
):
    """
    Export dataframe to GeoJSON.

    Parameters
    ----------
    dataframe : pandas.DataFrame

    output_file : pathlib.Path
    """

    if dataframe.empty:
        raise ValueError("Cannot export an empty dataframe.")

    lat = CSV_COLUMNS["latitude"]
    lon = CSV_COLUMNS["longitude"]
    alt = CSV_COLUMNS["altitude"]
    time = CSV_COLUMNS["timestamp"]

    speed_available = CSV_COLUMNS["speed"] in dataframe.columns
    heading_available = CSV_COLUMNS["heading"] in dataframe.columns

    # ------------------------------------------------------------------
    # LineString
    # ------------------------------------------------------------------

    line_coordinates = []

    for _, row in dataframe.iterrows():

        line_coordinates.append(
            [
                row[lon],
                row[lat],
            ]
        )

    features = []

    features.append(
        {
            "type": "Feature",
            "geometry": {
                "type": "LineString",
                "coordinates": line_coordinates,
            },
            "properties": {
                "name": "GPS Route"
            },
        }
    )

    # ------------------------------------------------------------------
    # Point Features
    # ------------------------------------------------------------------

    for index, row in dataframe.iterrows():

        properties = {
            "point": int(index + 1),
            "timestamp": str(row[time]),
            "altitude": float(row[alt]),
        }

        if speed_available:

            properties["speed"] = float(
                row[CSV_COLUMNS["speed"]]
            )

        if heading_available:

            properties["heading"] = float(
                row[CSV_COLUMNS["heading"]]
            )

        features.append(
            {
                "type": "Feature",
                "geometry": {
                    "type": "Point",
                    "coordinates": [
                        row[lon],
                        row[lat],
                    ],
                },
                "properties": properties,
            }
        )

    geojson = {
        "type": "FeatureCollection",
        "features": features,
    }

    output_file.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    with open(
        output_file,
        "w",
        encoding="utf-8",
    ) as file:

        json.dump(
            geojson,
            file,
            indent=4,
        )