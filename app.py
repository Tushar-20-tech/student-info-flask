from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

# Initialize database
def init_db():
    conn = sqlite3.connect("database.db")
    cur = conn.cursor()
    cur.execute('''CREATE TABLE IF NOT EXISTS students
                   (id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT,
                    roll TEXT,
                    dept TEXT,
                    email TEXT)''')
    conn.commit()
    conn.close()

init_db()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/add_student", methods=["POST"])
def add_student():
    name = request.form["name"]
    roll = request.form["roll"]
    dept = request.form["dept"]
    email = request.form["email"]

    conn = sqlite3.connect("database.db")
    cur = conn.cursor()
    cur.execute("INSERT INTO students (name, roll, dept, email) VALUES (?, ?, ?, ?)",
                (name, roll, dept, email))
    conn.commit()
    conn.close()
    return redirect("/students")

@app.route("/students")
def students():
    conn = sqlite3.connect("database.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM students")
    data = cur.fetchall()
    conn.close()
    return render_template("students.html", students=data)

if __name__ == "__main__":
    app.run(debug=True)
