# User Guide

## Step 1

Copy GPS CSV files into

```
data/
```

---

## Step 2

Activate the virtual environment.

Windows

```
.venv\Scripts\activate
```

---

## Step 3

Run

```
python main.py
```

---

## Step 4

Wait for processing to finish.

---

## Step 5

Open

```
output/
```

Each dataset will have its own folder containing

- map.html
- report.html
- route.geojson

---

## Troubleshooting

No datasets found

→ Verify CSV files are inside the data folder.

ImportError

→ Activate the virtual environment.

ModuleNotFoundError

→ Install dependencies

```
pip install -r requirements.txt
```