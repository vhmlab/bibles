"""API router for translations endpoints."""
from fastapi import APIRouter, HTTPException
from typing import List

from ..database import get_db
from ..models import Translation


router = APIRouter(
    prefix="/translations",
    tags=["translations"]
)


@router.get("/", response_model=List[Translation])
def get_all_translations():
    """
    Get all available Bible translations.
    
    Returns:
        List[Translation]: List of all translations in the database.
    """
    with get_db() as conn:
        cursor = conn.execute("SELECT id, name, abbreviation, language FROM translations ORDER BY name")
        translations = [Translation(**dict(row)) for row in cursor.fetchall()]
    return translations


@router.get("/{translation_id}", response_model=Translation)
def get_translation_by_id(translation_id: int):
    """
    Get a specific translation by ID.
    
    Args:
        translation_id: The ID of the translation.
        
    Returns:
        Translation: The translation details.
        
    Raises:
        HTTPException: If translation not found.
    """
    with get_db() as conn:
        cursor = conn.execute(
            "SELECT id, name, abbreviation, language FROM translations WHERE id = ?",
            (translation_id,)
        )
        row = cursor.fetchone()
        
        if not row:
            raise HTTPException(status_code=404, detail="Translation not found")
        
        return Translation(**dict(row))


@router.get("/abbreviation/{abbreviation}", response_model=Translation)
def get_translation_by_abbreviation(abbreviation: str):
    """
    Get a specific translation by abbreviation (e.g., KJV, NIV).
    
    Args:
        abbreviation: The abbreviation of the translation.
        
    Returns:
        Translation: The translation details.
        
    Raises:
        HTTPException: If translation not found.
    """
    with get_db() as conn:
        cursor = conn.execute(
            "SELECT id, name, abbreviation, language FROM translations WHERE abbreviation = ?",
            (abbreviation.upper(),)
        )
        row = cursor.fetchone()
        
        if not row:
            raise HTTPException(status_code=404, detail="Translation not found")
        
        return Translation(**dict(row))
