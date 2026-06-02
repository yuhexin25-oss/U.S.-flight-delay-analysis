# U.S. Flight Delay Analysis

**FlightScope** is a portfolio-scale aviation analytics platform for studying delay patterns across the U.S. domestic air transportation network. It combines data engineering, GIS, network science, and statistical analysis in a structure designed to scale from a compact demonstration dataset to BTS monthly extracts for 2019-2025.

![Project status](https://img.shields.io/badge/status-foundation%20release-0d5d9f)
![Python](https://img.shields.io/badge/python-3.11%2B-102a43)
![DuckDB](https://img.shields.io/badge/database-DuckDB-f36f45)

## Overview

The primary deliverable is a complete interactive aviation analytics website.

> **Data disclaimer:** This project currently uses mock BTS-style demo data. It is designed as a visualization prototype. Real BTS, FAA, OpenFlights, and NOAA datasets will be integrated in the next phase. No real-time flight API is currently connected.

The repository also includes a repeatable ETL skeleton, analytical DuckDB schema, reusable airport and route analysis helpers, and a notebook starter for future historical-data research.

## Research Motivation

Delays are not isolated events. They reflect airport capacity, airline operations, route connectivity, regional weather, and how disruption propagates through a network. This project asks how those systems interact and why some airports are more operationally resilient than others.

## Research Questions

- Which airports and routes experience the highest arrival delays and cancellation rates?
- How do major hubs differ from regional airports across seasons?
- Which airports occupy the most central positions in the domestic route network?
- How do carrier, weather, NAS, security, and late-aircraft delays vary by airport and airline?
- Which weather conditions are most strongly associated with delay and cancellation risk?

## Data Sources

| Source | Purpose | Integration status |
| --- | --- | --- |
| [BTS Airline On-Time Performance](https://www.transtats.bts.gov/ontime/) | Flight-level operations and delay causes | Pipeline-shaped sample ready; monthly export ingestion next |
| [OpenFlights Airport Database](https://openflights.org/data.html) | Airport coordinates and metadata | Reference downloader ready |
| [FAA Airports](https://www.faa.gov/airports) | Infrastructure, runway, tower, and hub fields | Schema extension planned |
| [NOAA Climate Data Online](https://www.ncei.noaa.gov/cdo-web/) | Visibility, wind, precipitation, temperature, and storms | Weather join module planned |

The current dashboard data is a historical-style demonstration dataset for interface development. It is not a live stream and should not be interpreted as current operational flight status.

## Quick Start

Create an environment and install dependencies:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Run the offline demonstration pipeline and build DuckDB:

```bash
make database
python3 -m src.visualization.export_dashboard_data
```

Open the GitHub Pages compatible dashboard directly from the repository root:

```bash
open index.html
```

No build step is required. The visualization libraries load from CDNs, while realistic demonstration records are embedded locally in `app.js` for direct `file://` viewing. Matching processed JSON files under `data/processed/` document the future real-data contract. You can also serve the website at `http://localhost:8000` with `python3 -m http.server 8000`.

## Pipeline

```text
download_data.py -> clean_data.py -> merge_datasets.py -> build_database.py
      raw CSVs      validated CSVs    aggregates        DuckDB views
```

Use `python3 download_data.py --sample` for a small offline extract. Without `--sample`, the downloader retrieves the OpenFlights reference database and leaves clear locations for BTS, FAA, and NOAA source extracts.

## Project Structure

```text
data/                 raw and processed extracts
database/             DuckDB schema and generated database
notebooks/            exploratory analysis template
src/download/         source acquisition
src/cleaning/         validation, cleaning, and enrichment
src/analysis/         metrics and NetworkX route analysis
src/visualization/    dashboard export helpers
web/                  responsive static dashboard
figures/              generated maps and charts
```

## Methodology

### GIS Analysis

Airport coordinates support interactive mapping, geographic comparisons, and future hotspot clustering. FAA infrastructure attributes will allow comparisons between capacity proxies and operational outcomes.

### Network Analysis

Routes are modeled as directed edges and airports as nodes. The analysis helpers calculate route-level volume and delay intensity, plus degree and betweenness centrality with NetworkX.

### Statistical Analysis

The initial schema captures delay causes and airport performance metrics. Future work will add NOAA joins, correlation analysis, regression models, and prediction workflows.

## Current Findings

The bundled sample is intentionally small and exists to verify the platform, not to support research conclusions. Reproducible findings will be added after full BTS extracts are ingested and validated.

## Visualizations

The website includes:

- A responsive dark aviation command-center interface with sidebar navigation
- An interactive Leaflet airport map with bubble, heatmap, combined, and route-line layers
- Global year, season, airline, delay-threshold, metric, and airport-type filters
- Airport search, clickable rankings, detail metrics, and weather summaries
- A D3.js route-network explorer with hover tooltips and linked node selection
- Dedicated hub-versus-regional, airline, route-ranking, and seasonal sections
- Plotly monthly trends, delay causes, comparisons, rankings, and seasonal analysis

## Future Work

- Automate BTS monthly ZIP ingestion for 2019-2025
- Integrate FAA infrastructure metrics and NOAA station observations
- Add airport, airline, route, region, season, and year filters
- Export Plotly trend views and route overlays to the website
- Add spatial clustering and weather-delay regression models
- Extend the platform toward delay prediction and real-time tracking
