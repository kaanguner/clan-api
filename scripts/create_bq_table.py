"""
Script to create BigQuery external table from GCS data.
"""
from google.cloud import bigquery
from google.api_core.exceptions import NotFound

# Project and dataset info
PROJECT_ID = "vertigo-games-case-2026"
DATASET_ID = "vertigo_raw"
TABLE_ID = "user_daily_metrics"
GCS_URI = "gs://vertigo-games-case-2026-data/user_metrics/*.csv.gz"

def main():
    # Initialize client
    client = bigquery.Client(project=PROJECT_ID)
    
    # First, create dataset if it doesn't exist
    dataset_ref = f"{PROJECT_ID}.{DATASET_ID}"
    try:
        client.get_dataset(dataset_ref)
        print(f"Dataset {dataset_ref} already exists")
    except NotFound:
        print(f"Creating dataset {dataset_ref} in location EU...")
        dataset = bigquery.Dataset(dataset_ref)
        dataset.location = "EU"
        dataset = client.create_dataset(dataset, timeout=30)
        print(f"Created dataset: {dataset.full_dataset_id}")
    
    # Also create vertigo_analytics dataset for DBT output
    analytics_dataset_ref = f"{PROJECT_ID}.vertigo_analytics"
    try:
        existing = client.get_dataset(analytics_dataset_ref)
        if existing.location != "EU":
            print(f"Dataset {analytics_dataset_ref} exists but in wrong location ({existing.location}). Deleting and recreating in EU...")
            client.delete_dataset(analytics_dataset_ref, delete_contents=True, not_found_ok=True)
            raise NotFound("Recreating")
        print(f"Dataset {analytics_dataset_ref} already exists in EU")
    except NotFound:
        print(f"Creating dataset {analytics_dataset_ref} in location EU...")
        analytics_dataset = bigquery.Dataset(analytics_dataset_ref)
        analytics_dataset.location = "EU"
        analytics_dataset = client.create_dataset(analytics_dataset, timeout=30)
        print(f"Created dataset: {analytics_dataset.full_dataset_id}")
    
    # Full table reference
    table_ref = f"{PROJECT_ID}.{DATASET_ID}.{TABLE_ID}"
    
    # Delete existing table if any
    try:
        client.delete_table(table_ref, not_found_ok=True)
        print(f"Deleted existing table (if any): {table_ref}")
    except Exception as e:
        print(f"Note: Could not delete table: {e}")
    
    # Define external table configuration
    external_config = bigquery.ExternalConfig("CSV")
    external_config.source_uris = [GCS_URI]
    external_config.autodetect = True
    external_config.options.skip_leading_rows = 1
    
    # Create table with external config
    table = bigquery.Table(table_ref)
    table.external_data_configuration = external_config
    
    # Create the table
    try:
        created_table = client.create_table(table)
        print(f"Created external table: {created_table.full_table_id}")
        print(f"Table location: {created_table.location}")
        
        # Verify by querying
        query = f"SELECT COUNT(*) as cnt FROM `{table_ref}` LIMIT 1"
        result = list(client.query(query).result())
        print(f"Row count query result: {result[0].cnt}")
        
    except Exception as e:
        print(f"Error creating table: {e}")
        raise

if __name__ == "__main__":
    main()
