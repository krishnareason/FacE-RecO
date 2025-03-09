# 🎯 Face Recognition Attendance System 🚀  

📌 **An AI-powered face recognition system using supervised learning for automated attendance tracking with an admin dashboard.**  

---

## 📸 Features  
✅ **Face Recognition Attendance** – Users can mark attendance using facial recognition.  
✅ **Supervised Machine Learning** – Trained on labeled face images using **Face Recognition library**.  
✅ **Admin Dashboard** – View logs, add/remove users, train model, collect samples.  
✅ **Live Attendance Logging** – Stores name, date, and time dynamically.  
✅ **Secure Access** – Different views for **admin** and **users**.  
✅ **JavaScript for UI Enhancements** – Uses **SweetAlert** popups and smooth interactions.  

---

## 🏗 Project Structure  

**📂 Face-Recognition-Attendance**  
**│── 📂 static**  
**│ │── 📂 images (For storing UI-related images)**  
**│── 📂 templates**  
**│ │── dashboard.html (Main dashboard UI)**  
**│── 📂 models**  
**│ │── face_data.pkl (Serialized trained model)**   
**│── app.py (Flask backend & ML logic)**  
**│── requirements.txt (Dependencies)**  
**│── README.md (This file)**  


## 🛠️ Tech Stack

🔹 **Backend** –  
<img src="https://upload.wikimedia.org/wikipedia/commons/3/3c/Flask_logo.svg" width="50" height="50"> Flask (Python)  
🔹 **Frontend** –  
&nbsp; &nbsp; <img src="https://upload.wikimedia.org/wikipedia/commons/6/61/HTML5_logo_and_wordmark.svg" width="40"> HTML
&nbsp; &nbsp; <img src="https://upload.wikimedia.org/wikipedia/commons/6/62/CSS3_logo.svg" width="40"> CSS
&nbsp; &nbsp; <img src="https://upload.wikimedia.org/wikipedia/commons/b/b2/Bootstrap_logo.svg" width="40"> Bootstrap
&nbsp; &nbsp; <img src="https://upload.wikimedia.org/wikipedia/commons/6/6a/JavaScript-logo.png" width="40"> JavaScript

🔹 **Database** –  
<img src="https://upload.wikimedia.org/wikipedia/commons/3/38/SQLite370.svg" width="50"> SQLite / CSV  
🔹 **Machine Learning** –  
<img src="https://upload.wikimedia.org/wikipedia/commons/3/32/OpenCV_Logo_with_text_svg_version.svg" width="50"> OpenCV & Face Recognition (Supervised Learning)  

## 🚀 Setup & Installation  

### 🔹 Step 1: Clone the Repository  
```bash
git clone https://github.com/your-username/face-recognition-attendance.git
cd face-recognition-attendance
```
### 🔹 Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```
### 🔹 Step 3: Run the Flask App
```bash
python app.py
```
## 📍 Visit: http://127.0.0.1:5000/


## 📸 Screenshots

### 🔹 Login Page
<img src="https://media-hosting.imagekit.io//54c49d6aa3c24da1/landing%20page.png?Expires=1836121010&Key-Pair-Id=K2ZIVPTIP2VGHC&Signature=KedackPukCPFexpsNsZZnItFDE4IganjT4XwmskonR2po9Dmalprm7LdGM9ZhNfwfDwVFk2gPM-7flV7283mZSn0LK8AH4kL9KUmCe-4LNIyqGQRj1QKOc02nKh9LAEsr0ks7nD~aIi7kBCtt4IfSgin31vTrJdWYoFzqTzNCxr-2s8-kxILP-3~7p~bz6ftWFljIau7MEW3y2ekglBihslZMZ3OUYzgdYexP2Xco9750uTX9Y5c6Cja6xOJKQlFEt~7EJllSjAPMPl6MH~2dD3mnPfldmGytSDP9mj2gYx8bPIKSPtQIMXT95OuQD4~r-N5wZttovxdyNl1YQaCpw__" width="600">

### 🔹 Face Recognition in Action (Dashboard)
<img src="https://media-hosting.imagekit.io//55acdd2e28ae4da0/admin.png?Expires=1836121138&Key-Pair-Id=K2ZIVPTIP2VGHC&Signature=gRtS7yxWlUbxU2fCpLHKMLC~sW6QIJLFMR2QqnyM6fYabJjBdhDaMiyIelvVpNGogi2GI3rGa46ervzTxe1KSNTnx0sR5Q7z70UAHZ1adkggOY-XZCnKh9CZNm3trP6cizhk66De215SWI6iXphmA4FXtK5MgbUQPZRBFVoGHqKoYpY8xwCQxXvbVVLNHetpBdQlCErdPb99BBoonK-CWOO1i53m~L9CYYlg442qMzIuNx4fjPl0tJrTZUBMmjZ3ZYn5a1nJoHbOGdMCTCsdtrxnjx54au2p8WBLjxK78xG8EoTBbdg9Afpi7XlyMiJaoAKqK8j2BBub2bs~7N89dQ__" width="600">  

---

## 🏗️ How It Works?

### 🔹 Supervised Learning Model
- The model is trained on labeled images of registered users.
- Uses the `face_recognition` library to extract **128-d feature vectors** from images.
- During recognition, it compares live images with stored embeddings to classify the user.

### 🔹 Admin Panel
- 📷 Collect samples for new users.
- 🧠 Train the model with new data.
- 📊 Manage attendance logs.

### 🔹 JavaScript Enhancements
- **SweetAlert popups** for smooth user experience.
- **Button clicks** trigger model training, face recognition, and attendance marking.  

## 🛡️ Security Features  
### 🔍 1. Liveness Detection (Prevention Against Spoofing)  
- Ensures real faces are detected, not just photos or videos.  
- Future improvement: Implement Depth Map Analysis or Blink Detection.  
### 🚪 2. Role-Based Access Control (RBAC)  
- Admin can manage users, train models, and view logs.  
- Regular users can only mark attendance.
### 📜 3. Logs & Monitoring  
- Every login & attendance activity is logged for security audits.
- Admins can monitor unauthorized access attempts.  
---

## 🛡️ Security & Future Improvements
✅ **Hashing & Encryption for Secure Data**  
✅ **Real-time Face Detection with Deep Learning**  
✅ **Cloud Deployment for Scalability**  

---

## 🤝 Contributing  
Pull requests are welcome! For major changes, please open an issue first.

---

## 📜 License  
This project is **open-source** under the **MIT License**.



