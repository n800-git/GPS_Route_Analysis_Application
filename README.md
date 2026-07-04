# GPS Route Analysis Application

## Overview

This project processes GPS datasets in CSV format and generates detailed route analysis, interactive maps, GeoJSON exports, and HTML reports.

The application is built using Python with a modular architecture, automated testing, and a virtual environment.

---

## Features

- GPS dataset validation
- Route distance calculation
- Mission duration calculation
- Altitude analysis
- Speed analysis (if available)
- Heading analysis (if available)
- Interactive Folium map generation
- GeoJSON export
- HTML report generation
- Logging
- Unit testing
- Integration testing

---

## Project Structure

```
GPS_Assignment/

data/
docs/
logs/
output/
src/
templates/

AI_USAGE.md
.gitignore
main.py
main_validation.py
pyproject.toml
requirements.txt
README.md
```

---

## Requirements

Python 3.13+

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## Running the Application

```bash
python main.py
```

---

## Running Unit Tests

Run all tests:

```bash
python -m unittest discover tests
```

---

## Output

For each dataset the application generates:

- Interactive HTML Map
- GeoJSON Route
- HTML Report

Outputs are stored in:

```
output/
```

---

## Technologies Used

- Python
- Pandas
- NumPy
- Folium
- Jinja2
- Geopy
- Matplotlib

---

## Assumptions

At least 2 data points in Dataset_A_Clean_GPS and Dataset_C_Advanced_GPS each presumably contain errors or incorrect data, evident from generated html map outputs.

## Author

Omkar Chunekar

---

## Version

1.0.0
