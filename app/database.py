"""Database connection and session management."""
import sqlite3
from contextlib import contextmanager
from typing import Generator
from pathlib import Path


DATABASE_PATH = Path(__file__).parent.parent / "bibles.db"


@contextmanager
def get_db() -> Generator[sqlite3.Connection, None, None]:
    """
    Context manager for database connections.
    
    Yields:
        sqlite3.Connection: Database connection with row factory set to Row.
    """
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
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
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    return conn
