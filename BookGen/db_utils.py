import sqlite3
from datetime import datetime
import string, os
from typing import Optional, List, Dict

# =========================
# Database Initialization
# =========================
def get_db_connection(db_path: str = "bookgen.db") -> sqlite3.Connection:
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    init_db(conn)
    return conn

def init_db(conn: sqlite3.Connection):
    cursor = conn.cursor()
    # -----------------
    # Books Table
    # -----------------
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS books (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL UNIQUE,
        ref_table TEXT NOT NULL UNIQUE,
        before_notes TEXT NOT NULL,
        after_notes TEXT,
        created_at TEXT NOT NULL,
        updated_at TEXT NOT NULL
    )
    """)
    conn.commit()

def _create_headings_table(conn: sqlite3.Connection, table_name: str):
    cursor = conn.cursor()
    # -----------------
    # Headings Table
    # -----------------
    cursor.execute(f"""
    CREATE TABLE IF NOT EXISTS {table_name} (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        heading_number INTEGER NOT NULL,
        heading_title TEXT NOT NULL,
        sub_heading TEXT,
        description TEXT,
        summary TEXT,
        content TEXT,
        before_notes TEXT,
        after_notes TEXT,
        created_at TEXT NOT NULL,
        updated_at TEXT NOT NULL
    )
    """)
    conn.commit()

# =========================
# Books Table Handlers
# =========================

def add_book(conn: sqlite3.Connection, title: str, before_notes: str) -> int:
    cursor = conn.cursor()
    # craete a random ref table for this book's headings
    chars = string.ascii_letters + string.digits
    random_bytes = os.urandom(16)
    while True:
        table_name = ''.join(chars[b % len(chars)] for b in random_bytes)
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=?", (table_name,))
        if not cursor.fetchone():
            break   
    _create_headings_table(conn, table_name)
    now = datetime.utcnow().isoformat()
    cursor.execute("""
    INSERT INTO books (title, before_notes, created_at, updated_at, ref_table)
    VALUES (?, ?, ?, ?, ?)
    """, (title, before_notes, now, now, table_name))
    conn.commit()
    return cursor.lastrowid

def update_book(conn: sqlite3.Connection, title: str = None, before_notes: Optional[str] = None, after_notes: Optional[str] = None):
    cursor = conn.cursor()
    fields = []
    values = []
    if before_notes is not None:
        fields.append("before_notes = ?")
        values.append(before_notes)
    if after_notes is not None:
        fields.append("after_notes = ?")
        values.append(after_notes)
    fields.append("updated_at = ?")
    values.append(datetime.utcnow().isoformat())
    values.append(title)
    cursor.execute(f"""
    UPDATE books
    SET {', '.join(fields)}
    WHERE title = ?
    """, values)
    conn.commit()

def delete_book(conn: sqlite3.Connection, title: str):
    cursor = conn.cursor()
    cursor.execute("SELECT ref_table FROM books WHERE title = ?", (title,))
    row = cursor.fetchone()
    if row:
        ref_table = row['ref_table']
        cursor.execute(f"DROP TABLE IF EXISTS {ref_table}")
    cursor.execute("DELETE FROM books WHERE title = ?", (title,))
    conn.commit()

def get_book(conn: sqlite3.Connection, title: str) -> Dict:
    # get book by title
    cursor = conn.cursor()
    cursor.execute("SELECT id, title, before_notes, after_notes FROM books WHERE title = ?", (title,))
    row = cursor.fetchone()
    return dict(row) if row else None

# =========================
# Headings Table Handlers
# =========================
def add_heading(conn: sqlite3.Connection, book_id: int, heading_number: int, heading_title: str, sub_heading: Optional[str] = None, description: Optional[str] = None) -> int:
    cursor = conn.cursor()
    now = datetime.utcnow().isoformat()
    cursor.execute("SELECT ref_table FROM books WHERE id = ?", (book_id,))
    row = cursor.fetchone()
    if not row:
        raise ValueError(f"No book found with id {book_id}")
    table_name = row['ref_table']
    cursor.execute(f"""
    INSERT INTO {table_name} (
        heading_number, heading_title,
        sub_heading, description, created_at, updated_at
    )
    VALUES (?, ?, ?, ?, ?, ?)
    """, (
        heading_number,
        heading_title,
        sub_heading,
        description,
        now,
        now
    ))
    conn.commit()
    return cursor.lastrowid

def update_heading(conn: sqlite3.Connection, book_id: int, heading_title: str, summary: Optional[str] = None, content: Optional[str] = None, before_notes: Optional[str] = None, after_notes: Optional[str] = None):
    cursor = conn.cursor()
    fields = []
    values = []
    cursor.execute("SELECT ref_table FROM books WHERE id = ?", (book_id,))
    row = cursor.fetchone()
    if not row:
        raise ValueError(f"No book found with id {book_id}")
    table_name = row['ref_table']
    for field, value in {
        "summary": summary,
        "content": content,
        "before_notes": before_notes,
        "after_notes": after_notes
        }.items():
        if value is not None:
            fields.append(f"{field} = ?")
            values.append(value)
    fields.append("updated_at = ?")
    values.append(datetime.utcnow().isoformat())
    values.append(heading_title)
    cursor.execute(f"""
    UPDATE {table_name}
    SET {', '.join(fields)}
    WHERE heading_title = ?
    """, values)
    conn.commit()

def get_headings_by_book(conn: sqlite3.Connection, book_id: int) -> List[Dict]:
    cursor = conn.cursor()
    cursor.execute("SELECT ref_table FROM books WHERE id = ?", (book_id,))
    row = cursor.fetchone()
    if not row:
        raise ValueError(f"No book found with id {book_id}")
    table_name = row['ref_table']
    cursor.execute(f"""
    SELECT heading_number, heading_title, sub_heading, description, summary, content from {table_name}
    """)
    rows = cursor.fetchall()
    return [dict(r) for r in rows]
