from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
import uuid
from datetime import datetime
from app.database import get_db_connection

app = FastAPI(title="Clan Management API")

class ClanCreate(BaseModel):
    name: str
    region: Optional[str] = None

@app.post("/clans")
async def create_clan(clan: ClanCreate):
    conn = get_db_connection()
    cur = conn.cursor()
    clan_id = str(uuid.uuid4())
    
    try:
        cur.execute(
            "INSERT INTO clans (id, name, region) VALUES (%s, %s, %s)",
            (clan_id, clan.name, clan.region)
        )
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=f"Database error: {e}")
    finally:
        cur.close()
        conn.close()
    
    return {"id": clan_id, "message": "Clan created successfully."}

@app.get("/clans")
async def list_clans(region: Optional[str] = None, sort_by: str = "created_at"):
    conn = get_db_connection()
    cur = conn.cursor()
    
    query = "SELECT id, name, region, created_at FROM clans"
    params = []
    
    if region:
        query += " WHERE region = %s"
        params.append(region)
    
    allowed_sort_columns = ["created_at", "name", "region", "id"]
    if sort_by not in allowed_sort_columns:
        raise HTTPException(status_code=400, detail=f"Invalid sort_by parameter. Allowed: {', '.join(allowed_sort_columns)}")
    
    query += f" ORDER BY {sort_by}"
    
    try:
        cur.execute(query, params)
        clans_data = cur.fetchall()
        
        columns = [desc[0] for desc in cur.description]
        clans = [dict(zip(columns, row)) for row in clans_data]
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {e}")
    finally:
        cur.close()
        conn.close()
    
    return {"clans": clans}

@app.get("/clans/{clan_id}")
async def get_clan(clan_id: str):
    conn = get_db_connection()
    cur = conn.cursor()
    
    try:
        cur.execute("SELECT id, name, region, created_at FROM clans WHERE id = %s", (clan_id,))
        clan_data = cur.fetchone()
        
        if not clan_data:
            raise HTTPException(status_code=404, detail="Clan not found")
        
        columns = [desc[0] for desc in cur.description]
        clan = dict(zip(columns, clan_data))
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {e}")
    finally:
        cur.close()
        conn.close()
    
    return {"clan": clan}

@app.delete("/clans/{clan_id}")
async def delete_clan(clan_id: str):
    conn = get_db_connection()
    cur = conn.cursor()
    
    try:
        cur.execute("DELETE FROM clans WHERE id = %s", (clan_id,))
        conn.commit()
        
        if cur.rowcount == 0:
            raise HTTPException(status_code=404, detail="Clan not found")
        
    except HTTPException:
        raise
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=f"Database error: {e}")
    finally:
        cur.close()
        conn.close()
    
    return {"message": "Clan deleted successfully"}