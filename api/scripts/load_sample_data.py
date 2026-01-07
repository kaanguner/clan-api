"""
Sample Data Loader for Clans Table

This script loads the actual sample clan data from CSV into the database.
Run it after the database is initialized.

Usage:
    python -m scripts.load_sample_data
"""

import sys
import os
import csv
from datetime import datetime, timezone
from uuid import uuid4

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database import SessionLocal, init_db
from app.models import Clan


def parse_timestamp(timestamp_str: str) -> datetime:
    """Parse timestamp from CSV, handling various formats."""
    if not timestamp_str or not timestamp_str.strip():
        return datetime.now(timezone.utc)
    
    timestamp_str = timestamp_str.strip()
    
    # Try different formats
    formats = [
        "%Y-%m-%d %H:%M:%S",
        "%Y-%m-%d %H:%M:%S ",  # trailing space
        "%Y-%m-%d %-H:%M:%S",  # single digit hour
    ]
    
    for fmt in formats:
        try:
            dt = datetime.strptime(timestamp_str, fmt)
            return dt.replace(tzinfo=timezone.utc)
        except ValueError:
            continue
    
    # Manual parse for single-digit hours like "4:23:50"
    try:
        parts = timestamp_str.split(' ')
        if len(parts) == 2:
            date_part = parts[0]
            time_part = parts[1]
            year, month, day = map(int, date_part.split('-'))
            time_components = time_part.split(':')
            hour = int(time_components[0])
            minute = int(time_components[1])
            second = int(time_components[2]) if len(time_components) > 2 else 0
            return datetime(year, month, day, hour, minute, second, tzinfo=timezone.utc)
    except:
        pass
    
    # Fallback to current time
    print(f"Warning: Could not parse timestamp '{timestamp_str}', using current time")
    return datetime.now(timezone.utc)


def load_sample_data(csv_path: str = None):
    """Load sample clan data from CSV into the database."""
    print("Initializing database...")
    init_db()
    
    db = SessionLocal()
    
    # Default CSV path
    if csv_path is None:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.dirname(os.path.dirname(script_dir))
        csv_path = os.path.join(project_root, "clan_sample_data (1).csv")
    
    try:
        # Check if data already exists
        existing_count = db.query(Clan).count()
        if existing_count > 0:
            print(f"Database already has {existing_count} clans. Skipping sample data load.")
            return
        
        if not os.path.exists(csv_path):
            print(f"CSV file not found: {csv_path}")
            print("Please provide the path to clan_sample_data.csv")
            return
        
        clans_loaded = 0
        print(f"Loading clans from {csv_path}...")
        
        with open(csv_path, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            for row in reader:
                if len(row) >= 2:
                    name = row[0].strip()
                    region = row[1].strip().upper()
                    timestamp = parse_timestamp(row[2] if len(row) > 2 else "")
                    
                    if name:  # Skip empty rows
                        clan = Clan(
                            id=uuid4(),
                            name=name,
                            region=region,
                            created_at=timestamp
                        )
                        db.add(clan)
                        clans_loaded += 1
        
        db.commit()
        print(f"Successfully loaded {clans_loaded} clans!")
        
        # Verify and show sample
        clans = db.query(Clan).limit(10).all()
        print("\nSample of loaded clans:")
        for clan in clans:
            print(f"  - {clan.name} ({clan.region}) - {clan.created_at}")
            
    except Exception as e:
        print(f"Error loading sample data: {e}")
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    # Check for custom path argument
    csv_path = sys.argv[1] if len(sys.argv) > 1 else None
    load_sample_data(csv_path)
