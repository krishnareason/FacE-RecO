import cv2
import os
import sys

sys.stdout.reconfigure(encoding="utf-8")

print("🔍 Checking camera access...")
cap = cv2.VideoCapture(0)  # Open the default camera

# Set high resolution (1080p)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)

if not cap.isOpened():
    print("🚨 Error: Camera not detected!")
    exit()

print("✅ Camera detected! Starting sample collection...")

# Ensure the script receives a name argument
if len(sys.argv) < 2:
    print("❌ Error: No name provided! Run the script with a name argument.")
    sys.exit(1)

person_name = sys.argv[1].strip()

# Paths
DATASET_PATH = "dataset"
person_path = os.path.join(DATASET_PATH, person_name)

# Ensure dataset directory exists (don't delete old data)
os.makedirs(person_path, exist_ok=True)

# Load Face Detector
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

# Count existing images (to continue numbering)
existing_files = [f for f in os.listdir(person_path) if f.endswith(".jpg")]
sample_count = len(existing_files)

print(f"📸 Collecting samples for {person_name}... Press 'q' to stop early.")
REQUIRED_SAMPLES = sample_count + 1000  # Collect additional 1000 images

while True:
    ret, frame = cap.read()
    if not ret:
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=6, minSize=(60, 60))

    for (x, y, w, h) in faces:
        face_roi = gray[y:y+h, x:x+w]
        face_roi = cv2.resize(face_roi, (100, 100))

        # Save normal face image
        file_path = os.path.join(person_path, f"{sample_count}.jpg")
        cv2.imwrite(file_path, face_roi)

        # Save flipped face image (mirrored)
        flipped_face = cv2.flip(face_roi, 1)
        flipped_file_path = os.path.join(person_path, f"{sample_count}_flipped.jpg")
        cv2.imwrite(flipped_file_path, flipped_face)

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
os.system("python train_model.py")
print("✅ Training completed!")
