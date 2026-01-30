"""API router for books endpoints."""
from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional

from ..database import get_db
from ..models import Book


router = APIRouter(
    prefix="/books",
    tags=["books"]
)


@router.get("/", response_model=List[Book])
def get_all_books(testament: Optional[str] = Query(None, description="Filter by testament: OT or NT")):
    """
    Get all books of the Bible.
    
    Args:
        testament: Optional filter for Old Testament (OT) or New Testament (NT).
        
    Returns:
        List[Book]: List of books.
    """
    with get_db() as conn:
        if testament:
            if testament.upper() not in ["OT", "NT"]:
                raise HTTPException(status_code=400, detail="Testament must be OT or NT")
            cursor = conn.execute(
                "SELECT id, name, testament FROM books WHERE testament = ? ORDER BY id",
                (testament.upper(),)
            )
        else:
            cursor = conn.execute("SELECT id, name, testament FROM books ORDER BY id")
        
        books = [Book(**dict(row)) for row in cursor.fetchall()]
    return books


@router.get("/{book_id}", response_model=Book)
def get_book_by_id(book_id: int):
    """
    Get a specific book by ID.
    
    Args:
        book_id: The ID of the book.
        
    Returns:
        Book: The book details.
        
    Raises:
        HTTPException: If book not found.
    """
    with get_db() as conn:
        cursor = conn.execute(
            "SELECT id, name, testament FROM books WHERE id = ?",
            (book_id,)
        )
        row = cursor.fetchone()
        
        if not row:
            raise HTTPException(status_code=404, detail="Book not found")
        
        return Book(**dict(row))


@router.get("/name/{book_name}", response_model=Book)
def get_book_by_name(book_name: str):
    """
    Get a specific book by name.
    
    Args:
        book_name: The name of the book.
        
    Returns:
        Book: The book details.
        
    Raises:
        HTTPException: If book not found.
    """
    with get_db() as conn:
        cursor = conn.execute(
            "SELECT id, name, testament FROM books WHERE name = ?",
            (book_name,)
        )
        row = cursor.fetchone()
        
        if not row:
            raise HTTPException(status_code=404, detail="Book not found")
        
        return Book(**dict(row))
