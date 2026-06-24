# DIVVY RIDES DATA ENGINEERING PROJECT SERIES

## From Junior ETL Pipeline → Mid-Level Lakehouse → Senior Divvy Intelligence Platform.

---

# Divvy Rides Data Engineering Project Series

A comprehensive Data Engineering portfolio project series built around the complete lifecycle of bike-sharing trip data.

This repository demonstrates how a Data Engineer can progressively evolve a simple file ingestion exercise into increasingly sophisticated data platforms that mirror real-world industry systems.

The project is intentionally structured into three levels:

| Level   | Project                              | Target Role             |
| ------- | ------------------------------------ | ----------------------- |
| Level 1 | Divvy Rides ETL Pipeline             | Junior Data Engineer    |
| Level 2 | Divvy Rides Analytics Lakehouse      | Mid-Level Data Engineer |
| Level 3 | Divvy Intelligence Platform          | Senior Data Engineer    |

Using the same dataset, each level introduces new architectural patterns, tooling, scalability considerations, and business value.

---

# Repository Goals

This repository demonstrates the complete Data Engineering lifecycle:

```text
Data Generation
      ↓
Data Ingestion
      ↓
Data Storage
      ↓
Data Transformation
      ↓
Data Serving
```

while showcasing practical engineering skills used in production environments.

---

# Dataset Overview

## Source

Divvy Bike Share Trips

## Dataset Characteristics

| Attribute   | Value          |
| ----------- | -------------- |
| Records     | ~1,000,000     |
| Size        | ~400 MB        |
| Format      | CSV            |
| Compression | ZIP            |
| Frequency   | Monthly        |
| Domain      | Urban Mobility |

## Sample Fields

```csv
ride_id
rideable_type
started_at
ended_at
start_station_name
end_station_name
start_lat
start_lng
end_lat
end_lng
member_casual
```

---

# Why This Dataset?

Bike-sharing data contains many characteristics commonly encountered in industry:

* Large files
* Historical datasets
* Geographic information
* Customer segmentation
* Time-series data
* Operational metrics
* Location analytics

These characteristics make it an excellent dataset for demonstrating Data Engineering concepts.

---

# Business Context

Bike-share operators generate millions of ride events every month.

Without a centralized analytics pipeline, answering operational and strategic questions becomes difficult.

The goal of these projects is to transform raw ride data into actionable business insights.

---

# Business Questions Answered

## Customer Analytics

* How many rides occur per day?
* What percentage of rides come from members?
* What percentage come from casual riders?
* How does customer behavior differ?

---

## Operational Analytics

* Which stations are busiest?
* Which stations are underutilized?
* Which stations experience peak demand?

---

## Product Analytics

* Which bike types are most popular?
* What is the average trip duration?
* Which routes are most frequently used?

---

## Strategic Analytics

* Where should additional bikes be deployed?
* Which stations should be expanded?
* Which locations show growing demand?

---

# Project Evolution

---

# PROJECT 1: Divvy Rides ETL Pipeline

### Objective

Build a reliable ETL pipeline that:

* Downloads datasets
* Validates data
* Cleans records
* Generates analytics datasets
* Produces reporting outputs

---

## Architecture

```text
HTTP Sources
      │
      ▼
Downloader
      │
      ▼
Raw Storage
      │
      ▼
Validation
      │
      ▼
Transformation
      │
      ▼
Analytics Tables
      │
      ▼
Power BI
```

---

## Recommended Tools

### Why These Tools?

For:

```text
1 Million Rows
400 MB Dataset
```

Distributed computing is unnecessary.

The most efficient stack is:

### Ingestion

* Python
* Requests

### Processing

* Pandas

### Storage

* Parquet

### Analytics

* PostgreSQL

### Dashboard

* Power BI

### Containerization

* Docker

### Version Control

* Git

---

## Deliverables

### Data Ingestion Layer

Downloads datasets automatically.

### Data Quality Layer

Performs validation checks.

### Transformation Layer

Produces analytics-ready datasets.

### Reporting Layer

Creates aggregated business metrics.

### Dashboard Layer

Visualizes insights.

---

## Skills Demonstrated

* Python
* ETL
* SQL
* Docker
* Data Validation
* Data Modeling

---

# PROJECT 2: Divvy Rides Analytics Lakehouse

### Objective

Transform the ETL pipeline into a scalable modern data platform.

---

## Architecture

```text
Bike Data
      │
      ▼
Airflow
      │
      ▼
Bronze Layer
      │
      ▼
PySpark
      │
      ▼
Silver Layer
      │
      ▼
Gold Layer
      │
      ▼
PostgreSQL
      │
      ▼
Power BI
```

---

## Additional Data Sources

### Weather Data

Weather influences ridership.

Examples:

* Temperature
* Rainfall
* Wind Speed

---

### Holiday Data

Public holidays affect demand.

Examples:

* Federal Holidays
* Special Events

---

## Recommended Tools

### Orchestration

Apache Airflow

### Processing

PySpark

### Storage

Parquet

### Data Lake

MinIO

### Quality

Great Expectations

### Warehouse

PostgreSQL

### Dashboard

Power BI

---

## Deliverables

### Bronze Layer

Raw immutable data.

### Silver Layer

Cleaned datasets.

### Gold Layer

Business-ready datasets.

### Data Quality Framework

Automated validation.

### Automated Scheduling

Airflow DAGs.

---

## Skills Demonstrated

* Airflow
* PySpark
* Data Lakes
* Data Quality
* Data Warehousing

---

# PROJECT 3: Divvy Intelligence Platform

### Objective

Build an enterprise-grade platform capable of both batch and streaming analytics.

---

## Architecture

```text
Ride Events
Weather APIs
Traffic APIs
       │
       ▼
Kafka
       │
       ▼
Spark Streaming
       │
       ▼
Iceberg Lakehouse
       │
       ▼
Analytics Layer
       │
       ├── Dashboards
       ├── APIs
       ├── Forecasting
       └── ML Models
```

---

## Advanced Use Cases

### Demand Forecasting

Predict station demand.

### Route Optimization

Optimize bike allocation.

### Customer Segmentation

Identify rider behavior.

### Real-Time Monitoring

Track live ride events.

### Anomaly Detection

Detect unusual ride activity.

---

## Recommended Tools

### Streaming

Apache Kafka

### Processing

Spark Streaming

### Lakehouse

Apache Iceberg

### Catalog

Nessie

### Query Engine

Trino

### Monitoring

Grafana

### APIs

FastAPI

### Infrastructure

Terraform

---

## Deliverables

### Real-Time Pipelines

Streaming ingestion.

### Lakehouse Architecture

Iceberg implementation.

### Feature Store

ML-ready datasets.

### Analytics APIs

FastAPI endpoints.

### Executive Dashboards

Operational visibility.

---

## Skills Demonstrated

* Kafka
* Spark Streaming
* Iceberg
* Data Governance
* Data Observability
* Infrastructure as Code

---

# Repository Structure

For your current repository:

```text
Divvy_Rides_DE_Project/

│
├── Divvy_Rides_ETL_Pipeline/
│
├── data/
│   ├── raw/
│   ├── staging/
│   ├── processed/
│   └── analytics/
│
├── logs/
│
├── tests/
│
├── docs/
│
├── dashboards/
│
├── src/
│
│   ├── ingestion/
│   │   ├── downloader.py
│   │   └── extractor.py
│
│   ├── validation/
│   │   └── quality_checks.py
│
│   ├── transformation/
│   │   ├── clean.py
│   │   └── enrich.py
│
│   ├── analytics/
│   │   └── metrics.py
│
│   ├── config/
│   │   └── settings.py
│
│   └── utils/
│       └── logger.py
│
├── .github/
│   └── workflows/
│
├── main.py
├── requirements.txt
├── pyproject.toml
└── README.md
```
## Data Engineering LifeCycle

### Ingestion

Tasks

* Build downloader
* Extract ZIP files
* Configure logging
* Create raw storage

Deliverables

* Downloaded datasets
* Extracted CSV files
* Dockerized pipeline

---


### Transformation

Tasks

* Validation checks
* Data cleaning
* Derived columns
* Parquet generation

Deliverables

* Processed datasets
* Quality reports
* Analytics-ready tables

---

### Serving

Tasks

* Generate metrics
* Build dashboards
* Documentation
* GitHub publication

Deliverables

* Power BI dashboard
* Architecture diagrams
* Complete README
* Portfolio-ready repository

---

# Real-World Applicability

The architecture and skills demonstrated in this repository directly map to use cases found in:

* Ride Sharing Companies
* Logistics Platforms
* Delivery Services
* Insurance Analytics
* Banking Data Warehouses
* Telecommunications
* Healthcare Analytics
* Government Mobility Programs

The same engineering principles used here are applied when processing:

* Uber Trips
* Lyft Data
* Bolt Ride Events
* Public Transit Data
* Fleet Management Systems

---