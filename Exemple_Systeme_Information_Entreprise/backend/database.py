from pathlib import Path
import sqlite3

DB_PATH = Path(__file__).resolve().parent.parent / "employees.db"

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("""
        CREATE TABLE IF NOT EXISTS employees (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            full_name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            department TEXT NOT NULL,
            job_title TEXT NOT NULL
        )
    """)
    conn.commit()
    return conn
