import sqlite3

def get_db():
    # Added timeout to avoid "database is locked"
    connection = sqlite3.connect("students.db", timeout=10)
    connection.row_factory = sqlite3.Row
    return connection

def create_tables():
    with get_db() as db:  # ensures auto commit + auto close
        db.execute("""
            CREATE TABLE IF NOT EXISTS students(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                roll_number TEXT UNIQUE NOT NULL
            )
        """)

        db.execute("""
            CREATE TABLE IF NOT EXISTS grades(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_id INTEGER,
                subject TEXT NOT NULL,
                marks INTEGER NOT NULL,
                FOREIGN KEY(student_id) REFERENCES students(id)
            )
        """)
