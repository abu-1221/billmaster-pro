"""
BillMaster Pro - Database Connection & Helpers
Provides SQLite connection management and initialization.
"""

import sqlite3
import os


class Database:
    """SQLite database manager."""

    def __init__(self, db_path, schema_path):
        self.db_path = db_path
        self.schema_path = schema_path
        self._ensure_directory()

    def _ensure_directory(self):
        """Ensure the database directory exists."""
        db_dir = os.path.dirname(self.db_path)
        if db_dir and not os.path.exists(db_dir):
            os.makedirs(db_dir, exist_ok=True)

    def get_connection(self):
        """Get a new database connection with row factory."""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA journal_mode=WAL")
        conn.execute("PRAGMA foreign_keys=ON")
        return conn

    def init_schema(self):
        """Initialize database tables from schema.sql."""
        conn = self.get_connection()
        with open(self.schema_path, 'r') as f:
            conn.executescript(f.read())
        conn.commit()
        conn.close()

    def is_seeded(self):
        """Check if database already has data."""
        conn = self.get_connection()
        try:
            count = conn.execute("SELECT COUNT(*) FROM users").fetchone()[0]
            conn.close()
            return count > 0
        except Exception:
            conn.close()
            return False


# Global instance (set during app creation)
db = None


def get_db():
    """Get a database connection."""
    return db.get_connection()


def init_db(app_config):
    """Initialize the database with the given config."""
    global db
    db = Database(app_config.DATABASE_PATH, app_config.SCHEMA_PATH)
    db.init_schema()
    return db
