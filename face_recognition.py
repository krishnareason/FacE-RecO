import os
import sys
import subprocess
import cv2
import numpy as np
import sqlite3
import time
from collections import deque
import sys
sys.stdout.reconfigure(encoding='utf-8')

# -------------------- (1) Auto Activate Virtual Environment --------------------
venv_path = os.path.join(os.getcwd(), ".venv", "Scripts", "python.exe")  # Windows
if not os.path.exists(venv_path):
    venv_path = os.path.join(os.getcwd(), ".venv", "bin", "python")  # Linux/Mac

if sys.executable != venv_path:
    print("⚡ Switching to Virtual Environment...")
    subprocess.call([venv_path] + sys.argv)
    sys.exit()

print(f"✅ Using Virtual Environment: {sys.executable}")

# -------------------- (2) Load Face Recognition Model --------------------
MODEL_PATH = "models/model.yml"
LABELS_PATH = "models/labels.npy"

recognizer = cv2.face.LBPHFaceRecognizer_create()   
recognizer.read(MODEL_PATH)
label_map = np.load(LABELS_PATH, allow_pickle=True).item()

# -------------------- (3) Load Face Detector --------------------
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

# -------------------- (4) Attendance Database Setup --------------------
DB_PATH = "database/attendance.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS attendance (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            date TEXT,
            time TEXT
        )
    """)
    conn.commit()
    conn.close()

def mark_attendance(name):
    """ Marks attendance only once per person per day """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    date_today = time.strftime("%Y-%m-%d")
    time_now = time.strftime("%H:%M:%S")

    # Check if already marked today
    cursor.execute("SELECT * FROM attendance WHERE name = ? AND date = ?", (name, date_today))
    if cursor.fetchone() is None:
        cursor.execute("INSERT INTO attendance (name, date, time) VALUES (?, ?, ?)", (name, date_today, time_now))
        conn.commit()
        print(f"🟢 Attendance marked for {name} at {time_now}")

    conn.close()

init_db()  # Initialize the database

# -------------------- (5) Face Recognition --------------------
cap = cv2.VideoCapture(0)
prev_predictions = deque(maxlen=5)  # Stores past confidence values
prev_names = deque(maxlen=5)  # Stores past names

print("🎥 Real-Time Face Recognition Started... Press 'q' to exit.")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.equalizeHist(gray)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=6, minSize=(50, 50))

    for (x, y, w, h) in faces:
        face_roi = gray[y:y+h, x:x+w]
        face_roi = cv2.resize(face_roi, (100, 100))

        # Recognize Face
        label_id, confidence = recognizer.predict(face_roi)

        # Store predictions in the queue
        prev_predictions.append(confidence)
        prev_names.append(label_map[label_id] if confidence <90 else "New Person")

        # Select the most frequently occurring name in the last few frames
        most_common_name = max(set(prev_names), key=prev_names.count)

        # Final decision
        name = most_common_name
        color = (0, 255, 0) if name != "New Person" else (0, 0, 255)

        # Mark attendance (only once per person per day)
        if name != "New Person":
            mark_attendance(name)

        # Draw Box & Label
        cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
        cv2.putText(frame, name, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 2)

    cv2.imshow("Face Recognition", frame)
    time.sleep(0.1)  # Reduce flickering

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
