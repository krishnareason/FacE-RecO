import cv2
import time

# Load OpenCV's pre-trained face detection model
model_file = cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
face_cascade = cv2.CascadeClassifier(model_file)

# Open webcam
video_capture = cv2.VideoCapture(0)

while True:
    start_time = time.time()  # Start time for latency measurement

    ret, frame = video_capture.read()
    if not ret:
        print("Failed to capture frame")
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  # Convert to grayscale for faster detection

    # Detect faces
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

    end_time = time.time()  # End time after processing

    # Draw rectangles around detected faces
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

    # Calculate and print latency
    latency = end_time - start_time
    print(f"Latency per frame: {latency:.4f} seconds")

    cv2.imshow('Face Detection', frame)

    # Press 'q' to exit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

video_capture.release()
cv2.destroyAllWindows()
