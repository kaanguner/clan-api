from typing import List
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from sqlalchemy import func

from ..database import get_db
from ..models import Clan
from ..schemas import (
    ClanCreate,
    ClanResponse,
    ClanListResponse,
    MessageResponse
)

router = APIRouter(prefix="/clans", tags=["clans"])


@router.post(
    "",
    response_model=ClanResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new clan",
    description="Creates a new clan with the specified name and region. Returns the created clan with auto-generated UUID and timestamp."
)
def create_clan(clan_data: ClanCreate, db: Session = Depends(get_db)):
    """
    Create a new clan.
    
    - **name**: Clan name (required)
    - **region**: Region code like "TR", "US" (required)
    """
    new_clan = Clan(
        name=clan_data.name,
        region=clan_data.region
    )
    db.add(new_clan)
    db.commit()
    db.refresh(new_clan)
    return new_clan


@router.get(
    "",
    response_model=ClanListResponse,
    summary="List all clans",
    description="Returns a list of all clans with their details."
)
def list_clans(db: Session = Depends(get_db)):
    """Get all clans from the database."""
    clans = db.query(Clan).order_by(Clan.created_at.desc()).all()
    return ClanListResponse(clans=clans, count=len(clans))


@router.get(
    "/search",
    response_model=ClanListResponse,
    summary="Search clans by name",
    description="Search for clans whose name contains the search term. Minimum 3 characters required."
)
def search_clans(
    name: str = Query(
        ...,
        min_length=3,
        description="Search term (minimum 3 characters, case-insensitive)"
    ),
    db: Session = Depends(get_db)
):
    """
    Search for clans by name.
    
    - **name**: Search term (minimum 3 characters, uses ILIKE for case-insensitive contains search)
    """
    search_pattern = f"%{name}%"
    clans = db.query(Clan).filter(
        func.lower(Clan.name).like(func.lower(search_pattern))
    ).order_by(Clan.created_at.desc()).all()
    
    return ClanListResponse(clans=clans, count=len(clans))


@router.delete(
    "/{clan_id}",
    response_model=MessageResponse,
    summary="Delete a clan",
    description="Deletes a specific clan by its UUID."
)
def delete_clan(clan_id: UUID, db: Session = Depends(get_db)):
    """
    Delete a clan by UUID.
    
    - **clan_id**: UUID of the clan to delete
    """
    clan = db.query(Clan).filter(Clan.id == clan_id).first()
    
    if not clan:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Clan with id '{clan_id}' not found"
        )
    
    db.delete(clan)
    db.commit()
    
    return MessageResponse(
        message=f"Clan '{clan.name}' deleted successfully",
        id=clan_id
    )
