"""API router for verses endpoints."""
from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional

from ..database import get_db
from ..models import Verse, VerseWithDetails


router = APIRouter(
    prefix="/verses",
    tags=["verses"]
)


@router.get("/", response_model=List[VerseWithDetails])
def get_verses(
    translation: str = Query(..., description="Translation abbreviation (e.g., KJV, NIV)"),
    book: str = Query(..., description="Book name (e.g., Genesis, John)"),
    chapter: int = Query(..., description="Chapter number"),
    verse_start: Optional[int] = Query(None, description="Starting verse number"),
    verse_end: Optional[int] = Query(None, description="Ending verse number (for range)"),
):
    """
    Get verses from a specific book, chapter, and optionally verse range.
    
    Args:
        translation: Translation abbreviation (e.g., KJV, NIV).
        book: Book name (e.g., Genesis, John).
        chapter: Chapter number.
        verse_start: Optional starting verse number.
        verse_end: Optional ending verse number for range queries.
        
    Returns:
        List[VerseWithDetails]: List of verses with full details.
        
    Raises:
        HTTPException: If translation or book not found.
    """
    with get_db() as conn:
        # Build query based on parameters
        query = """
            SELECT 
                v.id,
                t.name as translation_name,
                t.abbreviation as translation_abbreviation,
                b.name as book_name,
                b.testament,
                v.chapter,
                v.verse,
                v.text
            FROM verses v
            JOIN translations t ON v.translation_id = t.id
            JOIN books b ON v.book_id = b.id
            WHERE t.abbreviation = ? AND b.name = ? AND v.chapter = ?
        """
        params = [translation.upper(), book, chapter]
        
        if verse_start is not None:
            if verse_end is not None:
                query += " AND v.verse BETWEEN ? AND ?"
                params.extend([verse_start, verse_end])
            else:
                query += " AND v.verse = ?"
                params.append(verse_start)
        
        query += " ORDER BY v.verse"
        
        cursor = conn.execute(query, params)
        verses = [VerseWithDetails(**dict(row)) for row in cursor.fetchall()]
        
        if not verses:
            raise HTTPException(
                status_code=404,
                detail="No verses found for the specified criteria"
            )
        
        return verses


@router.get("/{verse_id}", response_model=Verse)
def get_verse_by_id(verse_id: int):
    """
    Get a specific verse by ID.
    
    Args:
        verse_id: The ID of the verse.
        
    Returns:
        Verse: The verse details.
        
    Raises:
        HTTPException: If verse not found.
    """
    with get_db() as conn:
        cursor = conn.execute(
            "SELECT id, translation_id, book_id, chapter, verse, text FROM verses WHERE id = ?",
            (verse_id,)
        )
        row = cursor.fetchone()
        
        if not row:
            raise HTTPException(status_code=404, detail="Verse not found")
        
        return Verse(**dict(row))


@router.get("/search/text", response_model=List[VerseWithDetails])
def search_verses(
    query: str = Query(..., min_length=3, description="Search query (minimum 3 characters)"),
    translation: Optional[str] = Query(None, description="Filter by translation abbreviation"),
    testament: Optional[str] = Query(None, description="Filter by testament: OT or NT"),
    limit: int = Query(100, le=1000, description="Maximum number of results (max 1000)")
):
    """
    Search for verses containing specific text.
    
    Args:
        query: Search query (minimum 3 characters).
        translation: Optional filter by translation abbreviation.
        testament: Optional filter by testament (OT or NT).
        limit: Maximum number of results (max 1000).
        
    Returns:
        List[VerseWithDetails]: List of matching verses with full details.
    """
    with get_db() as conn:
        sql_query = """
            SELECT 
                v.id,
                t.name as translation_name,
                t.abbreviation as translation_abbreviation,
                b.name as book_name,
                b.testament,
                v.chapter,
                v.verse,
                v.text
            FROM verses v
            JOIN translations t ON v.translation_id = t.id
            JOIN books b ON v.book_id = b.id
            WHERE v.text LIKE ?
        """
        params = [f"%{query}%"]
        
        if translation:
            sql_query += " AND t.abbreviation = ?"
            params.append(translation.upper())
        
        if testament:
            if testament.upper() not in ["OT", "NT"]:
                raise HTTPException(status_code=400, detail="Testament must be OT or NT")
            sql_query += " AND b.testament = ?"
            params.append(testament.upper())
        
        sql_query += " LIMIT ?"
        params.append(limit)
        
        cursor = conn.execute(sql_query, params)
        verses = [VerseWithDetails(**dict(row)) for row in cursor.fetchall()]
        
        return verses


@router.get("/chapter/all", response_model=List[VerseWithDetails])
def get_chapter(
    translation: str = Query(..., description="Translation abbreviation (e.g., KJV, NIV)"),
    book: str = Query(..., description="Book name (e.g., Genesis, John)"),
    chapter: int = Query(..., description="Chapter number")
):
    """
    Get all verses from a specific chapter.
    
    Args:
        translation: Translation abbreviation.
        book: Book name.
        chapter: Chapter number.
        
    Returns:
        List[VerseWithDetails]: All verses in the chapter.
        
    Raises:
        HTTPException: If no verses found.
    """
    return get_verses(translation=translation, book=book, chapter=chapter)
