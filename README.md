
# PharmEasy Regional Pulse

## Key Assumption

No external business cause is assumed from the order data alone. Any explanation for the observed regional sales movements must be independently verified before being treated as confirmed.


## Setup

Install the required Python packages:

`pip install pandas streamlit plotly`

## Project Overview

This project analyzes PharmEasy regional sales performance for April-June 2026. The workflow covers deterministic dataset generation, data cleaning and quality validation, SQLite analysis, significant regional movement detection, human-reviewed reporting, and a Streamlit dashboard.

## Pipeline

### Part 1 — Data Quality

1. Generate the deterministic source dataset:

```bash
python generate_dataset.py
