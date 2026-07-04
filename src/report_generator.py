"""
report_generator.py
-------------------

Generate an HTML report using a Jinja2 template.
"""

from __future__ import annotations

from datetime import datetime
from src.config import PROJECT_VERSION
from pathlib import Path

from jinja2 import Environment
from jinja2 import FileSystemLoader


TEMPLATE_DIRECTORY = Path("templates")
TEMPLATE_NAME = "report_template.html"


def generate_report(
    dataset_name: str,
    validation_summary,
    route_statistics,
    output_file: Path,
):
    """
    Generate an HTML report.
    """

    environment = Environment(
        loader=FileSystemLoader(
            TEMPLATE_DIRECTORY
        )
    )

    template = environment.get_template(
        TEMPLATE_NAME
    )

    html = template.render(

        dataset=dataset_name,

        generated=datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        ),

        version=PROJECT_VERSION,

        validation=validation_summary,

        stats=route_statistics,

    )

    output_file.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    output_file.write_text(
        html,
        encoding="utf-8",
    )