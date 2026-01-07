# Changelog

All notable changes to this project will be documented in this file.

---

## [2.0.0] - 2026-01-07

### ⚠️ Breaking Changes
- **Merged repositories**: `clan-analytics-dbt` repository is now deprecated. All DBT code moved here.
- **Removed Part 3**: DWH Architecture proposal removed (not required in new case study)

### Added
- `dbt/` folder with complete DBT project
  - `daily_metrics.sql` - Main aggregation model
  - `sources.yml` - BigQuery source definitions
  - `schema.yml` - Data quality tests (4 tests)
- `api/` restructured folder
  - `config.py` - Settings management with pydantic
  - `database.py` - Cloud SQL connector support
  - `routes/clans.py` - Organized CRUD endpoints
  - `schemas.py` - Pydantic request/response models
- `scripts/create_bq_table.py` - BigQuery external table creator
- `api/docker-compose.yml` - Local development setup
- `api/scripts/deploy.sh` - Cloud Run deployment
- `IMPROVEMENTS.md` - Future optimization ideas

### Changed
- README updated with v2.0.0 info and deprecation notice
- API now uses SQLAlchemy ORM instead of raw psycopg2
- Data files moved to GCS (not in repo)

### Removed
- `dwh_architecture.txt`
- `orchestration_flow.txt`
- `incremental_loading_strategy.txt`
- `table_schemas.md`
- `performance_and_cost.txt`
- `improvements.txt`
- `data_analyst_case_revised_april/` (17 CSV.gz files, ~196MB)

---

## [1.0.0] - Initial Release

### Added
- Part 1: Clan API with FastAPI
- Part 2: DBT model (in separate repo `clan-analytics-dbt`)
- Part 3: DWH Architecture proposal documents
