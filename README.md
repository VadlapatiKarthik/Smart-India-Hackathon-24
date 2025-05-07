# SIH Health App

A web-based application for health data entry and dynamic monitoring, built for Smart India Hackathon 2024.

## 🔧 Features

- ✅ Role-based login: Government, Healthcare Worker, User
- ✅ Dashboard rendering with HTML templates
- ✅ Excel-based patient data converted to SQLite (`patients_data.db`)
- ✅ Secure session-based login with `users.db`

## 🗂 Folder Structure

SIH_Health_App/
├── client/ # Frontend HTML files
│ └── templates/ # Dashboards for each role
├── server/ # Flask backend and login logic
├── data/ # SQLite DB from Excel
├── README.md
├── requirements.txt
└── .gitignore

## ⚙️ Setup Instructions

### 1. Install Requirements

```bash
pip install -r requirements.txt

### 2. Run the Flask App

cd server
python app.py

### 3. Access in Browser

http://127.0.0.1:5000/
