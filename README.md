# Clan Management API

This project is a simple REST API for managing gaming clans, built with FastAPI and deployed on Google Cloud Run.

## Features

*   Create a new clan.
*   List all clans, with filtering by region and sorting.
*   Get the details of a specific clan.
*   Delete a clan.

## Tech Stack

*   **Backend:** Python 3.11, FastAPI
*   **Database:** PostgreSQL (designed for Cloud SQL)
*   **Deployment:** Docker, Google Cloud Run

## Local Development Setup

1.  **Prerequisites:**
    *   Python 3.11
    *   Docker
    *   A running PostgreSQL instance.

2.  **Clone the repository:**
    ```bash
    git clone <your-repo-url>
    cd clan-api
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Set up the database:**
    *   Create a PostgreSQL database.
    *   Run the `schema.sql` file to create the `clans` table.

5.  **Configure environment variables:**
    *   Create a `.env` file in the root of the project.
    *   Add the following variables to the `.env` file, replacing the values with your local database credentials:
        ```
        DB_USER=your_db_user
        DB_PASSWORD=your_db_password
        DB_HOST=localhost
        DB_PORT=5432
        DB_NAME=your_db_name
        ```

6.  **Run the application:**
    ```bash
    uvicorn app.main:app --reload
    ```
    The API will be available at `http://127.0.0.1:8000`.

## API Endpoints

### Create a Clan

*   **URL:** `/clans`
*   **Method:** `POST`
*   **Body:**
    ```json
    {
      "name": "Shadow Warriors",
      "region": "TR"
    }
    ```
*   **Response:**
    ```json
    {
      "id": "generated-uuid",
      "message": "Clan created successfully."
    }
    ```

### List Clans

*   **URL:** `/clans`
*   **Method:** `GET`
*   **Query Parameters:**
    *   `region` (optional): Filter by region (e.g., `?region=TR`).
    *   `sort_by` (optional): Sort by `created_at`, `name`, `region`, or `id` (e.g., `?sort_by=name`).
*   **Response:**
    ```json
    {
      "clans": [
        {
          "id": "uuid-1",
          "name": "Shadow Warriors",
          "region": "TR",
          "created_at": "2023-10-27T10:00:00Z"
        },
        ...
      ]
    }
    ```

### Get a Clan

*   **URL:** `/clans/{clan_id}`
*   **Method:** `GET`
*   **Response:**
    ```json
    {
      "clan": {
        "id": "uuid-1",
        "name": "Shadow Warriors",
        "region": "TR",
        "created_at": "2023-10-27T10:00:00Z"
      }
    }
    ```

### Delete a Clan

*   **URL:** `/clans/{clan_id}`
*   **Method:** `DELETE`
*   **Response:**
    ```json
    {
      "message": "Clan deleted successfully"
    }
    ```

## Deployment to Google Cloud Run

1.  **Prerequisites:**
    *   Google Cloud SDK (`gcloud`) installed and configured.
    *   A Google Cloud project with Cloud Build, Cloud Run, and Cloud SQL APIs enabled.
    *   A Cloud SQL for PostgreSQL instance created.
    *   The database password stored in Google Secret Manager.

2.  **Build the Docker image:**
    ```bash
    gcloud builds submit --tag gcr.io/[PROJECT_ID]/clan-api
    ```

3.  **Deploy to Cloud Run:**
    ```bash
    gcloud run deploy clan-api \
      --image gcr.io/[PROJECT_ID]/clan-api \
      --platform managed \
      --region us-central1 \
      --allow-unauthenticated \
      --add-cloudsql-instances [PROJECT_ID]:[REGION]:[INSTANCE_NAME]
    ```
    Replace `[PROJECT_ID]`, `[REGION]`, and `[INSTANCE_NAME]` with your Google Cloud project details.