# 🦴 Bone Fracture Classification Website

A deep learning–based web application that classifies bone fractures from uploaded X-ray images and generates a patient report. Built using Flask and a trained TensorFlow/Keras model.

---

## 📌 Project Overview

This project is a complete end-to-end machine learning web application that:

* Accepts X-ray image uploads
* Classifies whether a bone is fractured or normal
* Displays prediction results on a report page

Designed as project demonstrating model deployment with a Flask backend.

---

## 🧠 Model Details

* Model Type: Deep Learning (CNN)
* Framework: TensorFlow / Keras
* Input: X-ray image
* Output: Fracture / Normal classification
* Saved Model: `.tflite` format for faster inference

---

## 🏗️ Project Structure

```
Bone-Fracture-Classification-Website/
│
├── model/                # Trained model files
├── static/               # CSS, images, UI assets
├── templates/            # HTML pages
│   ├── home.html
│   └── result.html
│
├── app.py                # Main Flask backend
├── email_utils.py        # Email sending logic
├── requirements.txt      # Python dependencies
├── runtime.txt           # Python version for deployment
├── profile.txt           # Deployment config
└── README.md             # Project documentation
```

---

## ⚙️ Features

* Upload X-ray image
* Real-time fracture prediction
* Clean report generation page
* Lightweight `.tflite` model for faster performance
* Deployed on Railway

---

## 🚀 Installation & Run Locally

### 1️⃣ Clone Repository

```
git clone https://github.com/your-username/Bone-Fracture-Classification-Website.git
cd Bone-Fracture-Classification-Website
```

### 2️⃣ Create Virtual Environment

```
python -m venv venv
venv\Scripts\activate
```

### 3️⃣ Install Dependencies

```
pip install -r requirements.txt
```

### 4️⃣ Run Flask App

```
python app.py
```

Open in browser:

```
http://127.0.0.1:5000
```

---

## 🌐 Deployment

This project can be deployed on:

* PythonAnywhere
* Render
* Heroku (with minor config)
* AWS / GCP VM
* Railway

Make sure:

* `requirements.txt` is updated
* Model path is correct in `app.py`


