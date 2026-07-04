"""
map_generator.py
----------------

Generate an interactive GPS route map using Folium.
"""

from pathlib import Path

import folium
import pandas as pd

from src.config import CSV_COLUMNS


def create_route_map(
    dataframe: pd.DataFrame,
    output_file: Path,
):
    """
    Create an interactive HTML map.
    """

    if dataframe.empty:
        raise ValueError("Cannot create map from an empty dataframe.")

    lat_col = CSV_COLUMNS["latitude"]
    lon_col = CSV_COLUMNS["longitude"]
    alt_col = CSV_COLUMNS["altitude"]
    time_col = CSV_COLUMNS["timestamp"]

    speed_available = CSV_COLUMNS["speed"] in dataframe.columns

    start = dataframe.iloc[0]

    route_map = folium.Map(
        location=[
            start[lat_col],
            start[lon_col],
        ],
        zoom_start=16,
        control_scale=True,
    )

    coordinates = list(
        zip(
            dataframe[lat_col],
            dataframe[lon_col],
        )
    )

    # ---------------------------------------------------------
    # Route Polyline
    # ---------------------------------------------------------

    folium.PolyLine(
        coordinates,
        color="blue",
        weight=4,
        opacity=0.8,
        tooltip="GPS Route",
    ).add_to(route_map)

    # ---------------------------------------------------------
    # Start Marker
    # ---------------------------------------------------------

    folium.Marker(
        coordinates[0],
        popup="Mission Start",
        tooltip="Start",
        icon=folium.Icon(
            color="green",
            icon="play",
        ),
    ).add_to(route_map)

    # ---------------------------------------------------------
    # End Marker
    # ---------------------------------------------------------

    folium.Marker(
        coordinates[-1],
        popup="Mission End",
        tooltip="End",
        icon=folium.Icon(
            color="red",
            icon="stop",
        ),
    ).add_to(route_map)

    # ---------------------------------------------------------
    # GPS Points
    # ---------------------------------------------------------

    for _, row in dataframe.iterrows():

        popup = (
            f"<b>Timestamp:</b> {row[time_col]}<br>"
            f"<b>Latitude:</b> {row[lat_col]:.6f}<br>"
            f"<b>Longitude:</b> {row[lon_col]:.6f}<br>"
            f"<b>Altitude:</b> {row[alt_col]:.2f} m"
        )

        if speed_available:

            popup += (
                f"<br><b>Speed:</b> "
                f"{row[CSV_COLUMNS['speed']]:.2f} km/h"
            )

        folium.CircleMarker(
            location=[
                row[lat_col],
                row[lon_col],
            ],
            radius=3,
            weight=1,
            fill=True,
            popup=popup,
        ).add_to(route_map)

    # ---------------------------------------------------------
    # Fit map
    # ---------------------------------------------------------

    route_map.fit_bounds(coordinates)

    output_file.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    route_map.save(output_file)