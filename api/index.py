from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import sqlite3
from typing import List, Optional

DATABASE = "students.db"

# Use a single shared connection for simplicity in this demo. In production use a proper DB.
_conn = None

def get_db():
    global _conn
    if _conn is None:
        _conn = sqlite3.connect(DATABASE, check_same_thread=False)
        _conn.row_factory = sqlite3.Row
    return _conn

def init_db():
    conn = get_db()
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE,
            grade TEXT
        )
        """
    )
    conn.commit()

class StudentIn(BaseModel):
    name: str
    email: Optional[str] = None
    grade: Optional[str] = None

class Student(StudentIn):
    id: int

app = FastAPI(title="Student Tracker API")
init_db()

@app.get("/students", response_model=List[Student])
def list_students():
    conn = get_db()
    cur = conn.execute("SELECT id, name, email, grade FROM students ORDER BY id")
    rows = cur.fetchall()
    return [Student(**dict(r)) for r in rows]

@app.get("/students/{student_id}", response_model=Student)
def get_student(student_id: int):
    conn = get_db()
    cur = conn.execute("SELECT id, name, email, grade FROM students WHERE id = ?", (student_id,))
    row = cur.fetchone()
    if not row:
        raise HTTPException(status_code=404, detail="Student not found")
    return Student(**dict(row))

@app.post("/students", response_model=Student, status_code=201)
def create_student(s: StudentIn):
    conn = get_db()
    try:
        cur = conn.execute(
            "INSERT INTO students (name, email, grade) VALUES (?, ?, ?)",
            (s.name, s.email, s.grade),
        )
        conn.commit()
        student_id = cur.lastrowid
    except sqlite3.IntegrityError as e:
        raise HTTPException(status_code=400, detail=str(e))
    cur = conn.execute("SELECT id, name, email, grade FROM students WHERE id = ?", (student_id,))
    row = cur.fetchone()
    return Student(**dict(row))

@app.put("/students/{student_id}", response_model=Student)
def update_student(student_id: int, s: StudentIn):
    conn = get_db()
    cur = conn.execute("SELECT id FROM students WHERE id = ?", (student_id,))
    if not cur.fetchone():
        raise HTTPException(status_code=404, detail="Student not found")
    try:
        conn.execute(
            "UPDATE students SET name = ?, email = ?, grade = ? WHERE id = ?",
            (s.name, s.email, s.grade, student_id),
        )
        conn.commit()
    except sqlite3.IntegrityError as e:
        raise HTTPException(status_code=400, detail=str(e))
    cur = conn.execute("SELECT id, name, email, grade FROM students WHERE id = ?", (student_id,))
    row = cur.fetchone()
    return Student(**dict(row))

@app.delete("/students/{student_id}", status_code=204)
def delete_student(student_id: int):
    conn = get_db()
    cur = conn.execute("SELECT id FROM students WHERE id = ?", (student_id,))
    if not cur.fetchone():
        raise HTTPException(status_code=404, detail="Student not found")
    conn.execute("DELETE FROM students WHERE id = ?", (student_id,))
    conn.commit()
    return None

@app.get("/")
def root():
    return {"message": "Student Tracker API — use /students endpoints"}