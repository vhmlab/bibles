"""Main FastAPI application for Bible translations API."""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routers import translations, books, verses


app = FastAPI(
    title="Bible Translations API",
    description="""
    A RESTful API for accessing Bible translations, books, and verses.
    
    ## Features
    
    * **Translations**: Get information about available Bible translations
    * **Books**: Browse books of the Bible (Old and New Testament)
    * **Verses**: Read and search Bible verses across different translations
    
    ## Usage
    
    All endpoints are read-only. The API provides access to:
    - Multiple Bible translations
    - All books organized by testament
    - Individual verses and verse ranges
    - Full-text search across verses
    
    ## Database Schema
    
    The API is backed by a SQLite database with three main tables:
    - `translations`: Bible translation information
    - `books`: Books of the Bible
    - `verses`: Individual verses with references to translations and books
    """,
    version="1.0.0",
    contact={
        "name": "Bible API Support",
        "email": "support@example.com"
    },
    license_info={
        "name": "MIT License"
    }
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust this in production
    allow_credentials=True,
    allow_methods=["GET"],  # Only GET methods since it's read-only
    allow_headers=["*"],
)

# Include routers
app.include_router(translations.router)
app.include_router(books.router)
app.include_router(verses.router)


@app.get("/", tags=["root"])
def read_root():
    """
    Root endpoint providing API information.
    
    Returns:
        dict: Welcome message and API information.
    """
    return {
        "message": "Welcome to the Bible Translations API",
        "version": "1.0.0",
        "documentation": "/docs",
        "endpoints": {
            "translations": "/translations",
            "books": "/books",
            "verses": "/verses"
        }
    }


@app.get("/health", tags=["health"])
def health_check():
    """
    Health check endpoint.
    
    Returns:
        dict: API health status.
    """
    return {"status": "healthy"}
