from flask import Flask, render_template, request, redirect, url_for, session, send_from_directory
import json
import os

app = Flask(__name__)
app.secret_key = "supersecretkey"

DB_FILE = "user_database.json"

# Base resources folder
BASE_RESOURCES = os.path.join(os.getcwd(), "resources")

# ----------------- User DB Functions -----------------

def load_users():
    if os.path.exists(DB_FILE):
        with open(DB_FILE, "r") as f:
            return json.load(f)
    return {}

def save_users(users):
    with open(DB_FILE, "w") as f:
        json.dump(users, f, indent=4)

# ----------------- Routes -----------------

@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        users = load_users()
        username = request.form["username"]
        password = request.form["password"]

        if username in users and users[username]["password"] == password:
            session["user"] = username
            session["grade"] = users[username]["grade"]
            return redirect(url_for("dashboard"))
        else:
            return render_template("login.html", error="Invalid username or password")

    return render_template("login.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        users = load_users()
        username = request.form["username"]
        password = request.form["password"]
        grade = request.form["grade"]

        if username in users:
            return render_template("register.html", error="Username already exists")

        users[username] = {"password": password, "grade": grade}
        save_users(users)
        return redirect(url_for("login"))

    return render_template("register.html")

@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        return redirect(url_for("login"))
    return render_template("dashboard.html", grade=session["grade"])

# ----------------- Subject Page (MATH ONLY FOR NOW) -----------------

@app.route("/math")
def subject_math():
    if "user" not in session:
        return redirect(url_for("login"))

    grade = session["grade"]  # "7", "8", or "9"

    exams_base = os.path.join("resources", "resorces-MathExams")
    notes_base = os.path.join("resources", "resorces-MathNotes")

    # making folder names based on grades
    exams_folder = f"math{grade}Exams"   # math7Exams, math8Exams, math9Exams
    notes_folder = f"mathG{grade}"        # mathNotes7,8 and 9

    exams_path = os.path.join(exams_base, exams_folder)
    notes_path = os.path.join(notes_base, notes_folder)

    exams = os.listdir(exams_path) if os.path.exists(exams_path) else []
    notes = os.listdir(notes_path) if os.path.exists(notes_path) else []

    return render_template(
        "subject.html",
        subject="Math",
        exams=exams,
        notes=notes,
        grade=grade
    )



# ----------------- Open File -----------------

@app.route("/open/math/<res_type>/<grade>/<filename>")
def open_file(res_type, grade, filename):

    if res_type == "exams":
        base = os.path.join(BASE_RESOURCES, "resorces-MathExams", f"math{grade}Exams")
    else:
        base = os.path.join(BASE_RESOURCES, "resorces-MathNotes", f"mathG{grade}")

    file_path = os.path.join(base, filename)

    if os.path.exists(file_path):
        return send_from_directory(base, filename)
    else:
        return "File not found", 404

# ----------------- Logout -----------------

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

# ----------------- Run -----------------

if __name__ == "__main__":
    app.run(debug=True)
