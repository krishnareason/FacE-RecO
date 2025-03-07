Face Recognition Attendance System 📸✅
🚀 An AI-powered Face Recognition System for Attendance Tracking 🚀

This project is a fully functional Face Recognition Attendance System that detects faces, collects new samples, and marks attendance automatically using OpenCV and machine learning models. It is built with Flask (for the web interface) and SQLite (for database management), allowing easy access via a web browser.

📌 Features
🎥 Real-time Face Recognition: Detect and recognize faces using OpenCV.
📸 Collect New Face Samples: Store multiple images for improved recognition accuracy.
📂 SQLite Database Integration: Automatically updates attendance records.
🖥️ Web Interface (Flask): User-friendly dashboard for easy interaction.
📊 View Attendance Records: Retrieve and analyze attendance data.
🔄 Retrain Model: Improve accuracy by adding new samples.
🏆 Secure Login System: Protect access to attendance data.
🛠️ Tech Stack
Python 🐍
Flask 🌐 (Backend)
OpenCV 👀 (Face Detection & Recognition)
SQLite 🗄️ (Database)
HTML, CSS, JavaScript 🎨 (Frontend)
📂 Project Structure
php
Copy
Edit
final_submission/
│── app.py                   # Main Flask application
│── database.db               # SQLite database
│── requirements.txt          # Dependencies
│── static/                   # Static files (CSS, JS, images)
│── templates/                # HTML templates
│── dev/
│   │── face_recognition.py   # Face recognition script
│   │── collect_samples.py    # Collect new face samples
│   │── train_model.py        # Train face recognition model
│── README.md                 # Project documentation
🖥️ Installation & Setup
Follow these steps to set up the project on your local machine.

1️⃣ Clone the Repository
sh
Copy
Edit
git clone https://github.com/the-steelix-flame/FacE-RecO.git
cd FacE-RecO
2️⃣ Install Dependencies
sh
Copy
Edit
pip install -r requirements.txt
3️⃣ Run the Flask App
sh
Copy
Edit
python app.py
Now, open your browser and go to:

cpp
Copy
Edit
http://127.0.0.1:5000
🚀 How to Use
🔹 Collect New Face Samples
Click "Collect New Samples" in the web interface.
Enter the name of the person.
The camera will capture 500 face samples for training.
The images are stored and used for recognition.
🔹 Train the Model
After collecting samples, train the model:

sh
Copy
Edit
python dev/train_model.py
This step updates the recognition system.

🔹 Start Face Recognition
Click "Start Face Recognition" or run:

sh
Copy
Edit
python dev/face_recognition.py
It will detect and recognize faces in real-time.

🔹 View Attendance
Click "View Attendance" to see all marked entries.

📊 Database Structure
The SQLite Database (database.db) stores attendance details in a table called attendance:

ID	Name	Date	Time
1	Akash	2025-03-07	10:30
2	John	2025-03-07	10:35
🛠️ Troubleshooting
1️⃣ Camera Not Opening?
Ensure OpenCV is installed:
sh
Copy
Edit
pip install opencv-python
Restart your PC and try again.
2️⃣ Face Not Recognized?
Try collecting more samples and re-train the model:
sh
Copy
Edit
python dev/train_model.py
Ensure good lighting while capturing samples.
3️⃣ Database Not Updating?
Check if database.db exists.
Ensure Flask is connected to the database.
💡 Future Improvements
✅ Improve Recognition Accuracy
📡 Deploy on Cloud for Remote Access
📱 Add Mobile App Support
📊 Generate Attendance Reports
📝 License
This project is open-source under the MIT License.

🎯 Contributors
💻 Developed by @the-steelix-flame
⭐ Feel free to contribute, report issues, or suggest improvements!

📌 Final Notes
If you found this project useful, please consider starring ⭐ the repository! 🚀
