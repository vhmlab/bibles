"""Database connection and session management.

Database file path is configurable via the `BIBLES_DB_PATH` environment
variable to make the deployment container-friendly. If the environment
variable is not set, it falls back to `bibles.db` in the project root.
"""
import os
import sqlite3
from contextlib import contextmanager
from typing import Generator
from pathlib import Path
from fastapi import HTTPException


DEFAULT_DB = Path(__file__).parent.parent / "bibles.db"
DATABASE_PATH = Path(os.getenv("BIBLES_DB_PATH", str(DEFAULT_DB))).resolve()


@contextmanager
def get_db() -> Generator[sqlite3.Connection, None, None]:
    """
    Context manager for database connections.
    
    Yields:
        sqlite3.Connection: Database connection with row factory set to Row.
    """
    try:
        conn = sqlite3.connect(str(DATABASE_PATH))
        conn.row_factory = sqlite3.Row
    except sqlite3.OperationalError as e:
        # Raise an HTTP-friendly error so FastAPI can return JSON
        raise HTTPException(status_code=500, detail=f"Database error: {e}")

    try:
        yield conn
    finally:
        conn.close()


def get_db_connection() -> sqlite3.Connection:
    """
    Get a database connection.
    
    Returns:
        sqlite3.Connection: Database connection with row factory set to Row.
    """
    try:
        conn = sqlite3.connect(str(DATABASE_PATH))
        conn.row_factory = sqlite3.Row
        return conn
    except sqlite3.OperationalError as e:
        raise HTTPException(status_code=500, detail=f"Database error: {e}")
