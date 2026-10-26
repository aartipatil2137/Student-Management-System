
from flask import (
    Flask, render_template, request,
    redirect, url_for, flash
)
import mysql.connector
from mysql.connector import Error
from student import Student

app = Flask(__name__)
app.secret_key = "change-this-secret-key-before-deployment"

# Change the password to your MySQL password.
DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "YOUR_MYSQL_PASSWORD",
    "database": "student_management"
}

def get_connection():
    return mysql.connector.connect(**DB_CONFIG)

def get_students(search=""):
    connection = get_connection()
    try:
        cursor = connection.cursor(dictionary=True)
        term = f"%{search}%"

        cursor.execute("""
            SELECT id, name, email, phone, course, marks
            FROM students
            WHERE name LIKE %s
               OR course LIKE %s
               OR email LIKE %s
            ORDER BY id DESC
        """, (term, term, term))

        return cursor.fetchall()
    finally:
        connection.close()

@app.route("/")
def index():
    search = request.args.get("search", "").strip()

    try:
        students = get_students(search)
        return render_template(
            "index.html",
            students=students,
            search=search
        )
    except Error:
        app.logger.exception("Database connection failed")
        flash(
            "Database error. Check MySQL and DB_CONFIG.",
            "error"
        )
        return render_template(
            "index.html",
            students=[],
            search=search
        )

@app.route("/add", methods=["GET", "POST"])
def add_student():
    if request.method == "POST":
        student = Student(
            name=request.form.get("name", "").strip(),
            email=request.form.get("email", "").strip(),
            phone=request.form.get("phone", "").strip(),
            course=request.form.get("course", "").strip(),
            marks=request.form.get("marks", "").strip()
        )

        errors = student.validate()

        if errors:
            for error in errors:
                flash(error, "error")
            return render_template(
                "add_edit.html",
                student=student,
                mode="Add"
            )

        connection = None
        cursor = None

        try:
            connection = get_connection()
            cursor = connection.cursor()

            cursor.execute("""
                INSERT INTO students
                    (name, email, phone, course, marks)
                VALUES (%s, %s, %s, %s, %s)
            """, (
                student.name,
                student.email,
                student.phone,
                student.course,
                student.marks
            ))

            connection.commit()
            flash("Student added successfully.", "success")
            return redirect(url_for("index"))

        except Error:
            app.logger.exception("Could not add student")
            flash("Could not save student. Check database settings.", "error")

        finally:
            if cursor:
                cursor.close()
            if connection and connection.is_connected():
                connection.close()

    return render_template(
        "add_edit.html",
        student=None,
        mode="Add"
    )

@app.route("/edit/<int:student_id>", methods=["GET", "POST"])
def edit_student(student_id):
    connection = get_connection()

    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute(
            "SELECT * FROM students WHERE id = %s",
            (student_id,)
        )
        existing = cursor.fetchone()
    finally:
        cursor.close()
        connection.close()

    if existing is None:
        flash("Student not found.", "error")
        return redirect(url_for("index"))

    if request.method == "POST":
        student = Student(
            name=request.form.get("name", "").strip(),
            email=request.form.get("email", "").strip(),
            phone=request.form.get("phone", "").strip(),
            course=request.form.get("course", "").strip(),
            marks=request.form.get("marks", "").strip()
        )

        errors = student.validate()

        if errors:
            for error in errors:
                flash(error, "error")
            student.id = student_id
            return render_template(
                "add_edit.html",
                student=student,
                mode="Edit"
            )

        connection = get_connection()
        cursor = connection.cursor()

        try:
            cursor.execute("""
                UPDATE students
                SET name=%s, email=%s, phone=%s,
                    course=%s, marks=%s
                WHERE id=%s
            """, (
                student.name,
                student.email,
                student.phone,
                student.course,
                student.marks,
                student_id
            ))

            connection.commit()
            flash("Student updated successfully.", "success")
            return redirect(url_for("index"))

        except Error:
            app.logger.exception("Could not update student")
            flash("Could not update student.", "error")

        finally:
            cursor.close()
            connection.close()

    return render_template(
        "add_edit.html",
        student=existing,
        mode="Edit"
    )

@app.route("/delete/<int:student_id>", methods=["POST"])
def delete_student(student_id):
    connection = None
    cursor = None

    try:
        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute(
            "DELETE FROM students WHERE id = %s",
            (student_id,)
        )
        connection.commit()

        if cursor.rowcount:
            flash("Student deleted successfully.", "success")
        else:
            flash("Student not found.", "error")

    except Error:
        app.logger.exception("Could not delete student")
        flash("Could not delete student.", "error")

    finally:
        if cursor:
            cursor.close()
        if connection and connection.is_connected():
            connection.close()

    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)