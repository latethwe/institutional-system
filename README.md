# Institutional Environmental Monitoring System

FastAPI backend for institutional air-quality monitoring with RBAC, ABAC, audit logging, H3 spatial indexing, and event-driven analytics updates.

## Stack
- Python
- FastAPI
- SQLAlchemy
- SQLite
- h3-py

## Run
```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

## Group member roles
- Iliyas Malibekov: Architecture & Security
- Nursultan Zhanbulat: Data Modeling & H3 Integration
- Zhassulan Tursynbay: Backend APIs & Event-driven Component
- Nuriya Sultanseitova: QA, Demo Scenarios & Documentation

## Default users
- `admin` / `admin123` (Admin)
- `operator` / `operator123` (Operator)
- `analyst` / `analyst123` (Analyst, assigned demo H3 regions)

## Required endpoints
- `POST /login`
- `POST /measurements`
- `GET /measurements/by-h3/{h3_index}`
- `GET /analytics/region/{h3_index}`
- `GET /audit-logs`

## Security behavior
- RBAC enforced via dependency checks.
- ABAC rule: Analysts can access analytics only for their assigned H3 regions.

## Event-driven behavior
On each new measurement, an in-memory event (`measurement.created`) triggers aggregate recalculation for the corresponding H3 region.

## H3 usage in system
- `lat/lon` from each measurement is converted into H3 index (resolution 9).
- H3 index is stored in `measurements.h3_index`.
- Regional analytics are maintained in `air_quality_aggregates` keyed by `h3_index`.
- API supports H3 query/filter (`GET /measurements/by-h3/{h3_index}`) and aggregation (`GET /analytics/region/{h3_index}`).

## Submission-oriented docs
- Full report: `docs/project_report.md`
- Link to git: `https://github.com/latethwe/institutional-system`