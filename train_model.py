import cv2
import numpy as np
import os
from sklearn.utils.class_weight import compute_class_weight
import sys
sys.stdout.reconfigure(encoding='utf-8')

# Paths
dataset_path = "dataset/"
model_path = "models/model.yml"
labels_path = "models/labels.npy"

# Load Face Detector
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

# Initialize LBPH Face Recognizer
face_recognizer = cv2.face.LBPHFaceRecognizer_create(radius=2, neighbors=8, grid_x=8, grid_y=8)

# Read dataset
faces_data = []
labels = []
label_map = {}  
current_id = 0  

for person_name in os.listdir(dataset_path):
    person_folder = os.path.join(dataset_path, person_name)

    if os.path.isdir(person_folder):  
        print(f"📂 Processing: {person_name}...")  
        label_map[current_id] = person_name  
        person_id = current_id  
        current_id += 1  

        for filename in os.listdir(person_folder):
            img_path = os.path.join(person_folder, filename)
            img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)  

            if img is None:
                print(f"❌ Cannot read: {img_path}")
                continue

            # Preprocess Image
            img = cv2.equalizeHist(img)  # Histogram Equalization for better contrast

            # Detect Face
            faces = face_cascade.detectMultiScale(img, scaleFactor=1.2, minNeighbors=7, minSize=(60, 60))

            for (x, y, w, h) in faces:
                face_roi = img[y:y+h, x:x+w]
                face_roi = cv2.resize(face_roi, (100, 100))  # Resize to fixed size
                faces_data.append(face_roi)
                labels.append(person_id)

# **Ensure dataset is balanced**
label_counts = {label: labels.count(label) for label in set(labels)}
min_count = min(label_counts.values())  

balanced_faces = []
balanced_labels = []

for label in label_counts:
    face_subset = [faces_data[i] for i in range(len(labels)) if labels[i] == label][:min_count]
    label_subset = [label] * min_count
    balanced_faces.extend(face_subset)
    balanced_labels.extend(label_subset)

faces_data = balanced_faces  
labels = balanced_labels  

# Train and Save Model
if len(faces_data) > 0:
    face_recognizer.train(faces_data, np.array(labels))
    face_recognizer.save(model_path)  
    np.save(labels_path, label_map)  
    print("✅ Model trained successfully!")
    print(f"🔹 Labels Mapping: {label_map}")
    print(f"📁 Model saved in: {model_path}")
else:
    print("❌ No faces found! Add more images first.")

