# PharmEasy Regional Pulse

## Key Assumption

No external business cause is assumed from the order data alone. Any explanation for observed regional sales movements must be independently verified before being treated as confirmed.

## Setup

Install required packages:

`pip install pandas streamlit plotly`

## Project Overview

This project analyzes PharmEasy regional sales performance for April-June 2026. The workflow covers deterministic dataset generation, data cleaning and quality validation, SQLite analysis, significant regional movement detection, human-reviewed reporting, and a Streamlit dashboard.

## Complete Pipeline

1. `python generate_dataset.py`
2. `python clean_data.py`
3. `python build_db.py`
4. `python queries.py`
5. `python metrics_engine.py`
6. `python draft_report.py`
7. `python review_gate.py`
8. `streamlit run app.py`

Review `data_quality_report.md`, `memo.md`, `reliability_checklist.md`, and `presentation_storyline.md` during the workflow.

## Part 4 Artifact Cover Note

1. `app.py` — dashboard
2. `data_quality_report.md` — data quality
3. `memo.md` — decision memo
4. `presentation_storyline.md` — presentation framing and pushback

## Reviewer Consumption Order

1. `app.py`
2. `data_quality_report.md`
3. `memo.md`
4. `presentation_storyline.md`

## Key Finding

Guntur sales increased by 122.19% from ₹62,442.27 in April to ₹138,738.93 in May 2026. Guntur sales then decreased by 28.11% to ₹99,745.18 in June. The movement should be reviewed and validated against business context rather than treated as a confirmed sustained trend.

## Repository Files

- `generate_dataset.py`
- `clean_data.py`
- `data_quality_report.md`
- `build_db.py`
- `queries.py`
- `metrics_engine.py`
- `draft_report.py`
- `memo.md`
- `review_gate.py`
- `audit_log.jsonl`
- `reliability_checklist.md`
- `app.py`
- `presentation_storyline.md`
- `README.md`
