import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
USER_DB = os.path.join(BASE_DIR, "../users.db")
PATIENT_DB = os.path.join(BASE_DIR, "../../data/patients_data.db")


def get_user_db():
    conn = sqlite3.connect(USER_DB)
    conn.row_factory = sqlite3.Row
    return conn


def get_patient_db():
    conn = sqlite3.connect(PATIENT_DB)
    conn.row_factory = sqlite3.Row
    return conn


def get_user_by_credentials(username, password, role):
    conn = get_user_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username=? AND password=? AND role=?", (username, password, role))
    result = cursor.fetchone()
    conn.close()
    return result


def fetch_patient_summary(limit=10):
    conn = get_patient_db()
    cursor = conn.cursor()
    cursor.execute("SELECT Age, Gender, District FROM patients LIMIT ?", (limit,))
    result = cursor.fetchall()
    conn.close()
    return result
