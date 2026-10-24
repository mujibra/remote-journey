
import sqlite3
from contextlib import closing

DB_NAME = "job_tracker.db"

ALLOWED_STATUSES = {
    "Applied",
    "Interview",
    "Rejected",
    "Accepted"
}


def initialize_database():
    with closing(sqlite3.connect(DB_NAME)) as connection:
        connection.execute("""
            CREATE TABLE IF NOT EXISTS applications (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                company TEXT NOT NULL,
                position TEXT NOT NULL,
                status TEXT NOT NULL DEFAULT 'Applied'
            )
        """)
        connection.commit()


def add_application(company, position):
    if not isinstance(company, str) or not company.strip():
        raise ValueError("Company name is required")

    if not isinstance(position, str) or not position.strip():
        raise ValueError("Position is required")

    company = company.strip()
    position = position.strip()

    if is_duplicate(company, position):
        raise ValueError("This application already exists")

    with closing(sqlite3.connect(DB_NAME)) as connection:
        cursor = connection.execute(
            """
            INSERT INTO applications (company, position)
            VALUES (?, ?)
            """,
            (company, position)
        )
        connection.commit()
        return cursor.lastrowid


def get_applications():
    with closing(sqlite3.connect(DB_NAME)) as connection:
        connection.row_factory = sqlite3.Row

        rows = connection.execute("""
            SELECT id, company, position, status
            FROM applications
            ORDER BY id
        """).fetchall()

        return [dict(row) for row in rows]


def is_duplicate(company, position):
    with closing(sqlite3.connect(DB_NAME)) as connection:
        row = connection.execute(
            """
            SELECT 1
            FROM applications
            WHERE LOWER(TRIM(company)) = LOWER(TRIM(?))
              AND LOWER(TRIM(position)) = LOWER(TRIM(?))
            LIMIT 1
            """,
            (company, position)
        ).fetchone()

        return row is not None
    
def update_application_status(application_id, new_status):
    if new_status not in ALLOWED_STATUSES:
        raise ValueError("Invalid application status")

    with closing(sqlite3.connect(DB_NAME)) as connection:
        cursor = connection.execute(
            """
            UPDATE applications
            SET status = ?
            WHERE id = ?
            """,
            (new_status, application_id)
        )
        connection.commit()

        return cursor.rowcount > 0
    
def delete_application(application_id):
    with closing(sqlite3.connect(DB_NAME)) as connection:
        cursor = connection.execute(
            "DELETE FROM applications WHERE id = ?",
            (application_id,)
        )
        connection.commit()

        return cursor.rowcount > 0

if __name__ == "__main__":
    initialize_database()
    print("Database initialized.")
