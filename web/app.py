from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import subprocess
import os
import sqlite3
import sys
import csv

sys.stdout.reconfigure(encoding='utf-8')

app = Flask(__name__)
app.secret_key = "your_secret_key_here"  # Change this to a secure key

# -------------------- (1) User Authentication --------------------
users = {
    "admin": "admin123",
    "user": "user123"
}

@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if username in users and users[username] == password:
            session["username"] = username
            return redirect(url_for("dashboard"))
        else:
            return render_template("index.html", error="Invalid credentials!")

    return render_template("index.html")

# -------------------- (2) Dashboard --------------------
@app.route("/dashboard")
def dashboard():
    if "username" not in session:
        return redirect(url_for("login"))

    user = session["username"]

    # Fetch Attendance Data from Database
    conn = sqlite3.connect("database/attendance.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, date, time FROM attendance ORDER BY date DESC, time DESC")
    attendance_records = cursor.fetchall()
    conn.close()

    return render_template("dashboard.html", user=user, attendance=attendance_records)

# -------------------- (3) Run Face Recognition (Fixed) --------------------
@app.route("/run_face_recognition")
def run_face_recognition():
    if "username" not in session:
        return redirect(url_for("login"))

    try:
        subprocess.Popen(["python", "face_recognition.py"], shell=True)
        return jsonify({"message": "🚀 Face Recognition Started!"})
    except Exception as e:
        return jsonify({"error": str(e)})

# -------------------- (4) Collect New Samples (Fixed) --------------------
@app.route("/collect_samples", methods=["POST"])
def collect_samples():
    if "username" not in session:
        return redirect(url_for("login"))

    person_name = request.form.get("name")  # Get name from form input

    if not person_name:
        return jsonify({"error": "❌ Name is required!"})

    try:
        script_path = os.path.join(os.getcwd(), "collect_samples.py")
        print(f"✅ Running script at: {script_path} for {person_name}")

        subprocess.Popen(["python", script_path, person_name], shell=True)
        return jsonify({"message": f"📸 Collecting New Samples for {person_name}!"})

    except Exception as e:
        return jsonify({"error": str(e)})


# -------------------- (5) Train Model --------------------
@app.route("/train_model")
def train_model():
    if "username" not in session or session["username"] != "admin":
        return jsonify({"error": "❌ Access Denied!"})

    try:
        subprocess.Popen(["python", "train_model.py"], shell=True)
        return jsonify({"message": "🤖 Training Model Started!"})
    except Exception as e:
        return jsonify({"error": str(e)})

# -------------------- (6) View Attendance (Fixed) --------------------
@app.route("/view_attendance")
def view_attendance():
    if "username" not in session:
        return redirect(url_for("login"))

    try:
        conn = sqlite3.connect("database/attendance.db")
        cursor = conn.cursor()
        cursor.execute("SELECT id, name, date, time FROM attendance ORDER BY date DESC, time DESC")
        attendance_records = cursor.fetchall()
        conn.close()

        return render_template("dashboard.html", user=session["username"], attendance=attendance_records)

    except Exception as e:
        return jsonify({"error": str(e)})


# -------------------- (Admin Adds Person) --------------------
@app.route("/add_person", methods=["POST"])
def add_person():
    if "username" not in session or session["username"] != "admin":
        return jsonify({"error": "❌ Access Denied!"})

    new_person = request.form.get("new_person")

    if not new_person:
        return jsonify({"error": "❌ Name is required!"})

    try:
        os.makedirs(os.path.join("dataset", new_person), exist_ok=True)
        return redirect(url_for("dashboard"))

    except Exception as e:
        return jsonify({"error": str(e)})


# -------------------- (Admin Removes Person) --------------------
@app.route("/remove_person", methods=["POST"])
def remove_person():
    if "username" not in session or session["username"] != "admin":
        return jsonify({"error": "❌ Access Denied!"})

    remove_person = request.form.get("remove_person")

    if not remove_person:
        return jsonify({"error": "❌ Name is required!"})

    try:
        person_path = os.path.join("dataset", remove_person)

        if os.path.exists(person_path):
            import shutil
            shutil.rmtree(person_path)
            return redirect(url_for("dashboard"))
        else:
            return jsonify({"error": "❌ Person not found!"})

    except Exception as e:
        return jsonify({"error": str(e)})

# -------------------- (Admin watches logs) -------------------- 
# Route to display logs
@app.route("/logs")
def show_logs():
    logs = []
    try:
        with open("logs.csv", "r") as file:
            reader = csv.reader(file)
            logs = list(reader)  # Convert CSV rows to list
    except FileNotFoundError:
        logs = [["No Logs Found"]]

    return render_template("logs.html", logs=logs)
  


# -------------------- (7) Logout --------------------
@app.route("/logout")
def logout():
    session.pop("username", None)
    return redirect(url_for("login"))

# -------------------- (8) Run Flask App --------------------
if __name__ == "__main__":
    app.run(debug=True)
