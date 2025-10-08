import os
from google.cloud import secretmanager

DB_USER = os.getenv("DB_USER", "clan-api-service-account@projectvertigo.iam.gserviceaccount.com")
DB_NAME = os.getenv("DB_NAME", "clans_db")

if os.getenv("K_SERVICE"):
    DB_HOST = "/cloudsql/projectvertigo:europe-west4:sqlinstance"
else:
    DB_HOST = "127.0.0.1"

if os.getenv("K_SERVICE"):
    client = secretmanager.SecretManagerServiceClient()
    name = "projects/projectvertigo/secrets/clan-db-password/versions/latest"
    response = client.access_secret_version(request={"name": name})
    DB_PASSWORD = response.payload.data.decode("UTF-8")
else:
    DB_PASSWORD = os.getenv("DB_PASSWORD", "YOUR_LOCAL_DB_PASSWORD")