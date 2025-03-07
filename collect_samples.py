import cv2
import os
import subprocess
import sys

print("🔍 Checking camera access...")
cap = cv2.VideoCapture(0)  # Open the default camera

if not cap.isOpened():
    print("🚨 Error: Camera not detected!")
    exit()

print("✅ Camera detected! Starting sample collection...")
######
sys.stdout.reconfigure(encoding='utf-8')
venv_path = os.path.join(os.getcwd(), ".venv", "Scripts", "python.exe")  # Windows
if sys.executable != venv_path:
    print("⚡ Switching to Virtual Environment...")
    subprocess.call([venv_path] + sys.argv)
    sys.exit()

print(f"✅ Using Virtual Environment: {sys.executable}")


# Paths
DATASET_PATH = "dataset"

# Ensure dataset directory exists
os.makedirs(DATASET_PATH, exist_ok=True)

# Ask for the person's name (used for folder naming)
person_name = input("Enter person's name: ").strip()
person_path = os.path.join(DATASET_PATH, person_name)

# Create directory if new, else append to existing
os.makedirs(person_path, exist_ok=True)

# Load Face Detector
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

# Open Webcam
cap = cv2.VideoCapture(0)

print(f"📸 Collecting samples for {person_name}... Press 'q' to stop early.")
sample_count = 0
REQUIRED_SAMPLES = 500  # Number of images to collect

while True:
    ret, frame = cap.read()
    if not ret:
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(50, 50))

    for (x, y, w, h) in faces:
        face_roi = gray[y:y+h, x:x+w]
        face_roi = cv2.resize(face_roi, (100, 100))

        # Save face image
        file_path = os.path.join(person_path, f"{sample_count}.jpg")
        cv2.imwrite(file_path, face_roi)

        sample_count += 1
        print(f"✅ Captured sample {sample_count}/{REQUIRED_SAMPLES}")

        # Draw box
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

    cv2.imshow("Collecting Samples", frame)
    
    # Stop if 'q' is pressed or enough samples are collected
    if cv2.waitKey(1) & 0xFF == ord('q') or sample_count >= REQUIRED_SAMPLES:
        break

cap.release()
cv2.destroyAllWindows()

print(f"📁 {sample_count} samples saved in: {person_path}")

print("📢 Training model with new data...")
subprocess.run(["python", "train_model.py"])
print("✅ Training completed!")
