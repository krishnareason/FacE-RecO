import os
import sys
import subprocess
import cv2
import numpy as np
import sqlite3
import time
import csv
from collections import deque

sys.stdout.reconfigure(encoding='utf-8')

# Logging Setup
LOG_FILE = "logs.csv"

def log_event(event_type, message):
    """ Logs events to a CSV file """
    with open(LOG_FILE, mode="a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([time.strftime("%Y-%m-%d"), time.strftime("%H:%M:%S"), event_type, message])

log_event("SYSTEM", "Face recognition started.")

# Increase OpenCV Window Size
cv2.namedWindow("Face Recognition", cv2.WINDOW_NORMAL)
cv2.resizeWindow("Face Recognition", 800, 600)

# Auto Activate Virtual Environment
venv_path = os.path.join(os.getcwd(), ".venv", "Scripts", "python.exe")  # Windows
if not os.path.exists(venv_path):
    venv_path = os.path.join(os.getcwd(), ".venv", "bin", "python")  # Linux/Mac

if sys.executable != venv_path:
    log_event("SYSTEM", "Switching to virtual environment.")
    subprocess.call([venv_path] + sys.argv)
    sys.exit()

# Load Face Recognition Model
MODEL_PATH = "models/model.yml"
LABELS_PATH = "models/labels.npy"

recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read(MODEL_PATH)
label_map = np.load(LABELS_PATH, allow_pickle=True).item()

# Load Face Detector
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_eye.xml")

# Attendance Database Setup
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

    cursor.execute("SELECT * FROM attendance WHERE name = ? AND date = ?", (name, date_today))
    if cursor.fetchone() is None:
        cursor.execute("INSERT INTO attendance (name, date, time) VALUES (?, ?, ?)", (name, date_today, time_now))
        conn.commit()
        log_event("ATTENDANCE", f"Attendance marked for {name} at {time_now}")
    
    conn.close()

init_db()

# Advanced Spoofing Protection
frame_count = 0
blink_counter = 0
prev_predictions = deque(maxlen=5)
prev_names = deque(maxlen=5)
no_movement_counter = 0
last_face_position = None

def is_live_face(frame, gray, x, y, w, h):
    """ 
    Advanced liveness detection: 
    ✅ Checks eye blinking  
    ✅ Detects head movement  
    ✅ Screen reflection detection  
    """
    global blink_counter, no_movement_counter, last_face_position

    roi_gray = gray[y:y+h, x:x+w]
    roi_color = frame[y:y+h, x:x+w]

    # Head movement check
    if last_face_position is not None:
        movement = abs(last_face_position[0] - x) + abs(last_face_position[1] - y)
        if movement < 5:
            no_movement_counter += 1
        else:
            no_movement_counter = 0
    last_face_position = (x, y)

    # Screen reflection detection
    avg_pixel_intensity = np.mean(roi_gray)
    if avg_pixel_intensity > 200:
        log_event("SPOOFING ALERT", "High reflection detected! Possible screen use.")
        cv2.putText(frame, "⚠️ Spoofing Alert!", (50, 50), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (0, 0, 255), 2)
        return False

    # Eye blinking detection
    eyes = eye_cascade.detectMultiScale(roi_gray, scaleFactor=1.1, minNeighbors=5, minSize=(15, 15))
    if len(eyes) >= 2:
        blink_counter += 1
        if blink_counter >= 2:
            blink_counter = 0
            return True

    # No movement = possible spoofing
    if no_movement_counter > 30:
        log_event("SPOOFING ALERT", "No movement detected! Possible static image.")
        return False

    return False

# Face Recognition Loop
cap = cv2.VideoCapture(0)

cap.set(3, 1280)  # Width
cap.set(4, 720)   # Height

print("🎥 Real-Time Face Recognition Started... Press 'q' to exit.")

cv2.namedWindow("Face Recognition", cv2.WINDOW_NORMAL)
cv2.resizeWindow("Face Recognition", 800, 600)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.equalizeHist(gray)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=4, minSize=(60, 60))

    for (x, y, w, h) in faces:
        if not is_live_face(frame, gray, x, y, w, h):
            print("❌ Fake Face Detected! Ignoring...")
            continue

        face_roi = gray[y:y+h, x:x+w]
        face_roi = cv2.resize(face_roi, (100, 100))

        label_id, confidence = recognizer.predict(face_roi)
        prev_predictions.append(confidence)
        prev_names.append(label_map[label_id] if confidence < 115 else "New Person")

        most_common_name = max(set(prev_names), key=prev_names.count)
        name = most_common_name
        color = (0, 255, 0) if name != "New Person" else (0, 0, 255)

        if name != "New Person":
            mark_attendance(name)

        cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
        cv2.putText(frame, name, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 2)

    cv2.imshow("Face Recognition", frame)
    time.sleep(0.1)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

log_event("SYSTEM", "Face recognition stopped.")
cap.release()
cv2.destroyAllWindows()
