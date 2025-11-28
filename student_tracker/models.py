class Student:
    def __init__(self, name, roll_number):
        self.name = name
        self.roll_number = roll_number


class StudentTracker:
    def __init__(self, db):
        self.db = db

    def add_student(self, name, roll_number):
        self.db.execute(
            "INSERT INTO students(name, roll_number) VALUES(?, ?)",
            (name, roll_number)
        )
        self.db.commit()

    def add_grade(self, roll_number, subject, marks):
        student = self.db.execute(
            "SELECT id FROM students WHERE roll_number = ?",
            (roll_number,)
        ).fetchone()

        if not student:
            return False

        self.db.execute(
            "INSERT INTO grades(student_id, subject, marks) VALUES(?,?,?)",
            (student["id"], subject, marks)
        )
        self.db.commit()
        return True

    def get_student_details(self, roll_number):
        student = self.db.execute(
            "SELECT * FROM students WHERE roll_number = ?",
            (roll_number,)
        ).fetchone()

        if not student:
            return None

        grades = self.db.execute(
            "SELECT subject, marks FROM grades WHERE student_id = ?",
            (student["id"],)
        ).fetchall()

        return student, grades

    def calculate_average(self, roll_number):
        student = self.db.execute(
            "SELECT id FROM students WHERE roll_number = ?",
            (roll_number,)
        ).fetchone()

        if not student:
            return None

        grades = self.db.execute(
            "SELECT marks FROM grades WHERE student_id = ?",
            (student["id"],)
        ).fetchall()

        if not grades:
            return 0

        avg = sum(g["marks"] for g in grades) / len(grades)
        return round(avg, 2)

    def get_all_students(self):
        return self.db.execute("SELECT * FROM students").fetchall()
