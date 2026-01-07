# Future Improvements & Optimization Ideas

This document outlines potential improvements for the Vertigo Games Data Engineer Case Study project.

---

## 🔄 DBT & Data Pipeline

### Implemented ✅
- **BigQuery Partitioning** - `daily_metrics` partitioned by `event_date`
- **BigQuery Clustering** - Clustered by `country`, `platform`
- **Pre-aggregated Marts** - `daily_metrics` ready for BI tools

### Future Improvements

| Improvement | Impact | Complexity |
|-------------|--------|------------|
| **Incremental Models** | Reduce BigQuery costs by only processing new data | Medium |
| **dbt Snapshots** | Track slowly changing dimensions (SCD Type 2) for user attributes | Medium |
| **Data Quality Tests** | Add `dbt_expectations` package for advanced data validation | Low |
| **CI/CD Pipeline** | GitHub Actions to run `dbt test` on PR, `dbt run` on merge | Medium |
| **Cloud Composer** | Automate daily dbt runs with Airflow DAGs | High |
| **Real-time Ingestion** | Pub/Sub + Dataflow for streaming events to Bronze layer | High |

---

## 🚀 API & Backend

### Implemented ✅
- **SQLAlchemy ORM** - Clean database abstraction
- **FastAPI Dependency Injection** - Efficient DB session management
- **Cloud Run + Cloud SQL** - Serverless, scalable deployment

### Future Improvements

| Improvement | Impact | Complexity |
|-------------|--------|------------|
| **Caching Layer** | Add Redis for frequently accessed clan data | Medium |
| **Rate Limiting** | Protect API from abuse with `slowapi` or API Gateway | Low |
| **Pagination** | Add cursor-based pagination for `GET /clans` | Low |
| **GET /clans/{id}** | Add endpoint to fetch single clan by UUID | Low |
| **Filter & Sort** | Add `?region=TR&sort=created_at` query params | Low |
| **API Versioning** | Prefix routes with `/v1/` for future compatibility | Low |
| **Health Checks** | Add `/ready` endpoint checking DB connectivity | Low |
| **OpenTelemetry** | Add distributed tracing for observability | Medium |

---

## 💰 Cost Optimization

| Strategy | Description | Savings |
|----------|-------------|---------|
| **Incremental dbt** | Only process new rows each run | 60-80% |
| **Partitioned Queries** | Always filter by `event_date` | 50-90% |
| **Clustered Tables** | Filter by `country`, `platform` | 20-40% |
| **Cloud Run Min Instances = 0** | Scale to zero when idle | Variable |
| **Cloud SQL db-f1-micro** | Smallest instance for dev/test | ~$10/mo |

---

## 🔒 Security

| Improvement | Description |
|-------------|-------------|
| **Secret Manager** | Store DB credentials in GCP Secret Manager |
| **IAM Authentication** | Use Cloud Run service accounts instead of passwords |
| **VPC Connector** | Private networking between Cloud Run and Cloud SQL |
| **Input Validation** | Already using Pydantic, but add more strict regex patterns |

---

## 📊 Observability

| Tool | Purpose |
|------|---------|
| **Cloud Logging** | Already integrated via Cloud Run |
| **Cloud Monitoring** | Add custom metrics for API latency, error rates |
| **dbt Artifacts** | Store `manifest.json` for lineage tracking |
| **Looker Studio** | Connect directly to `daily_metrics` for dashboards |

---

*Last updated: v2.0.0*
