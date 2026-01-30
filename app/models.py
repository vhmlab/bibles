"""Pydantic models for API request/response schemas."""
from pydantic import BaseModel, Field
from typing import Optional, Literal


class Translation(BaseModel):
    """Translation model."""
    id: int
    name: str
    abbreviation: str
    language: str

    class Config:
        from_attributes = True


class Book(BaseModel):
    """Book model."""
    id: int
    name: str
    testament: Literal["OT", "NT"] = Field(..., description="Old Testament (OT) or New Testament (NT)")

    class Config:
        from_attributes = True


class Verse(BaseModel):
    """Verse model."""
    id: int
    translation_id: int
    book_id: int
    chapter: int
    verse: int
    text: str

    class Config:
        from_attributes = True


class VerseWithDetails(BaseModel):
    """Verse model with additional details."""
    id: int
    translation_name: str
    translation_abbreviation: str
    book_name: str
    testament: str
    chapter: int
    verse: int
    text: str

    class Config:
        from_attributes = True


class VerseRange(BaseModel):
    """Model for verse range queries."""
    translation_abbreviation: str
    book_name: str
    chapter: int
    start_verse: int
    end_verse: int
    verses: list[Verse]

    class Config:
        from_attributes = True
