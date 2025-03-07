from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import subprocess
import os
import sqlite3
import sys
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
        subprocess.Popen(["python", "dev/face_recognition.py"], shell=True)
        return jsonify({"message": "🚀 Face Recognition Started!"})
    except Exception as e:
        return jsonify({"error": str(e)})

# -------------------- (4) Collect New Samples (Fixed) --------------------
@app.route("/collect_samples")
def collect_samples():
    if "username" not in session:
        return redirect(url_for("login"))

    try:
        script_path = os.path.join(os.getcwd(), "dev", "collect_samples.py")
        print(f"✅ Running script at: {script_path}")

        subprocess.run(["python", script_path], cwd=os.path.dirname(script_path))
        return jsonify({"message": "📸 Collecting New Samples!"})

    except Exception as e:
        return jsonify({"error": str(e)})

# -------------------- (5) Train Model --------------------
@app.route("/train_model")
def train_model():
    if "username" not in session or session["username"] != "admin":
        return jsonify({"error": "❌ Access Denied!"})

    try:
        subprocess.Popen(["python", "dev/train_model.py"], shell=True)
        return jsonify({"message": "🤖 Training Model Started!"})
    except Exception as e:
        return jsonify({"error": str(e)})

# -------------------- (6) View Attendance (Fixed) --------------------
@app.route("/view_attendance")
def view_attendance():
    if "username" not in session:
        return redirect(url_for("login"))

    try:
        conn = sqlite3.connect("database/attendance.db")  # Ensure the correct path
        cursor = conn.cursor()

        # Fetching attendance records
        cursor.execute("SELECT id, name, date, time FROM attendance ORDER BY date DESC, time DESC")
        attendance_records = cursor.fetchall()
        conn.close()

        return jsonify({"message": "📊 Viewing Attendance!", "data": attendance_records})

    except Exception as e:
        return jsonify({"error": str(e)})

# -------------------- (7) Logout --------------------
@app.route("/logout")
def logout():
    session.pop("username", None)
    return redirect(url_for("login"))

# -------------------- (8) Run Flask App --------------------
if __name__ == "__main__":
    app.run(debug=True)
