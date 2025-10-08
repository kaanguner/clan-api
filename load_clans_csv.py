import os
import csv
from datetime import datetime
import psycopg2
from app.config import DATABASE_URL

def load_clans_from_csv():
    csv_file_path = "clan_sample_data.csv"
    conn = None
    cursor = None

    try:
        conn = psycopg2.connect(DATABASE_URL)
        cursor = conn.cursor()

        with open(csv_file_path, mode='r', newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)

            insert_count = 0
            for row in reader:
                name = row.get('name')
                region = row.get('region')
                created_at = row.get('created_at')

                if not name or not region:
                    print(f"Skipping row due to missing name or region: {row}")
                    continue

                if created_at:
                    try:
                        int_ts = int(float(created_at))
                        created_at = datetime.fromtimestamp(int_ts).strftime('%Y-%m-%d %H:%M:%S')
                    except (ValueError, TypeError):
                        pass

                    cursor.execute(
                        "INSERT INTO clans (name, region, created_at) VALUES (%s, %s, %s)",
                        (name, region, created_at)
                    )
                else:
                    cursor.execute(
                        "INSERT INTO clans (name, region) VALUES (%s, %s)",
                        (name, region)
                    )
                insert_count += 1

            conn.commit()
            print(f"Successfully inserted {insert_count} clans from '{csv_file_path}' into the database.")

    except FileNotFoundError:
        print(f"Error: CSV file not found at {csv_file_path}")
    except psycopg2.Error as e:
        print(f"Database error: {e}")
        if conn:
            conn.rollback()
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
            print("Database connection closed.")

if __name__ == "__main__":
    load_clans_from_csv()