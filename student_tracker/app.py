from flask import Flask, render_template, request, redirect
from database import get_db, create_tables
from models import StudentTracker

app = Flask(__name__)
create_tables()

@app.route("/")
def index():
    db = get_db()
    tracker = StudentTracker(db)
    students = tracker.get_all_students()
    return render_template("index.html", students=students)

@app.route("/add-student", methods=["GET", "POST"])
def add_student():
    if request.method == "POST":
        name = request.form["name"]
        roll = request.form["roll"]

        db = get_db()
        tracker = StudentTracker(db)
        tracker.add_student(name, roll)
        return redirect("/")

    return render_template("add_student.html")

@app.route("/add-grades", methods=["GET", "POST"])
def add_grades():
    if request.method == "POST":
        roll = request.form["roll"]
        subject = request.form["subject"]
        marks = int(request.form["marks"])

        db = get_db()
        tracker = StudentTracker(db)
        tracker.add_grade(roll, subject, marks)
        return redirect("/")

    return render_template("add_grades.html")

@app.route("/view-student", methods=["POST"])
def view_student():
    roll = request.form["roll"]

    db = get_db()
    tracker = StudentTracker(db)
    details = tracker.get_student_details(roll)
    avg = tracker.calculate_average(roll)

    return render_template("view_student.html",
                           details=details,
                           avg=avg)
    
if __name__ == "__main__":
    app.run(debug=True)
