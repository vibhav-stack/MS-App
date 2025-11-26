import streamlit as st
import pandas as pd
import sqlite3
from collections import Counter
from datetime import date
import os

def categorize_ms_stage_by_age(age: int) -> tuple[str, str]:
    """
    Categorize MS stage and return (stage, characteristics) based on age.
    """
    # Updated clinical logic
    if 20 <= age <= 40:
        return (
            "Clinically Isolated Syndrome (CIS)",
            "Single episode, mild symptoms, MRI shows lesions."
        )
    elif 20 < age <= 45:
        return (
            "Relapsing-Remitting MS (RRMS)",
            "Episodes of relapse and remission, mostly good recovery."
        )
    elif 30 < age <= 60:
        return (
            "Secondary Progressive MS (SPMS)",
            "Gradual worsening, increasing disability, fewer remissions."
        )
    elif age > 40:
        return (
            "Primary Progressive MS (PPMS)",
            "Steady progression, mostly motor and gait dysfunction."
        )
    else:
        return ("Unclassified", "Age outside guideline range.")

def categorize_ms_stage_by_relapse_count(relapse_count: int) -> tuple[str, str]:
    """
    Categorize MS stage and return (stage, characteristics) based on relapse count.
    """
    # Updated clinical logic
    if relapse_count == 0:
        return (
            "Clinically Isolated Syndrome (CIS)",
            "No relapses, first episode."
        )
    elif 1 <= relapse_count <= 3:
        return (
            "Relapsing-Remitting MS (RRMS)",
            "1–3 relapses, mostly good recovery."
        )
    elif 4 <= relapse_count <= 10:
        return (
            "Secondary Progressive MS (SPMS)",
            "4–10 relapses, increasing disability."
        )
    elif relapse_count > 10:
        return (
            "Primary Progressive MS (PPMS)",
            ">10 relapses, progressive worsening."
        )
    else:
        return ("Unclassified", "Relapse count outside guideline range.")

# --- Database Helper ---
def get_db_path():
    db_folder = os.path.join(os.path.dirname(__file__), "database")
    if not os.path.exists(db_folder):
        os.makedirs(db_folder)
    return os.path.join(db_folder, "ms_patients.db")

def fetch_all_patients():
    db_path = get_db_path()
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute('SELECT * FROM ms_patients')
    rows = c.fetchall()
    columns = [desc[0] for desc in c.description]
    conn.close()
    return rows, columns

def categorize_ms_stage_by_duration(duration_ms: int) -> tuple[str, str]:
    if duration_ms == 0:
        return (
            "Primary Progressive MS (PPMS)",
            "Progressive from onset."
        )
    elif 0 < duration_ms <= 1:
        return (
            "Clinically Isolated Syndrome (CIS)",
            "0–1 year."
        )
    elif 1 < duration_ms <= 15:
        return (
            "Relapsing-Remitting MS (RRMS)",
            "0–15 years."
        )
    elif duration_ms > 15:
        return (
            "Secondary Progressive MS (SPMS)",
            "Usually >15 years."
        )
    else:
        return ("Unclassified", "Duration outside guideline range.")

def fetch_all_patients():
    db_path = get_db_path()
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute('SELECT * FROM ms_patients')
    rows = c.fetchall()
    columns = [desc[0] for desc in c.description]
    conn.close()
    return rows, columns

def fetch_patient_by_id(patient_id):
    db_path = get_db_path()
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute('SELECT * FROM ms_patients WHERE id=?', (patient_id,))
    row = c.fetchone()
    conn.close()
    return row

def save_patient_data(name, age, gender, symptoms, relapse_count, duration_ms):
    db_path = get_db_path()
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS ms_patients (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        age INTEGER,
        gender TEXT,
        symptoms TEXT,
        relapse_count INTEGER,
        duration_ms INTEGER,
        diagnosis_date TEXT,
        last_relapse_date TEXT
    )''')
    c.execute('''INSERT INTO ms_patients (name, age, gender, symptoms, relapse_count, duration_ms) VALUES (?, ?, ?, ?, ?, ?)''',
        (name, age, gender, symptoms, relapse_count, duration_ms))
    conn.commit()
    conn.close()

def update_patient_data(patient_id, age, gender, symptoms, relapse_count, duration_ms):
    db_path = get_db_path()
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute('''UPDATE ms_patients SET age=?, gender=?, symptoms=?, relapse_count=?, duration_ms=? WHERE id=?''',
        (age, gender, symptoms, relapse_count, duration_ms, patient_id))
    conn.commit()
    conn.close()

# --- Daily Log Save Helper ---
def save_daily_log(patient_name: str, stage: str, date_str: str, new_symptoms: str, fatigue_level: int, sleep_hours: int, medication_taken: str):
    db_path = get_db_path()
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    # Map stage to table name
    stage_table_map = {
        "Stage 1": "stage1_daily_logs",
        "Stage 2": "stage2_daily_logs",
        "Stage 3": "stage3_daily_logs",
        "Stage 4": "stage4_daily_logs"
    }
    table_name = stage_table_map.get(stage, "stage1_daily_logs")
    # Ensure all stage tables exist
    for tbl in ["stage1_daily_logs", "stage2_daily_logs", "stage3_daily_logs", "stage4_daily_logs"]:
        c.execute(f'''CREATE TABLE IF NOT EXISTS {tbl} (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            patient_name TEXT,
            date TEXT,
            new_symptoms TEXT,
            fatigue_level INTEGER,
            sleep_hours INTEGER,
            medication_taken TEXT
        )''')
    # Ensure all stage tables exist
    for tbl in ["stage1_daily_logs", "stage2_daily_logs", "stage3_daily_logs", "stage4_daily_logs"]:
        c.execute(f'''CREATE TABLE IF NOT EXISTS {tbl} (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            patient_name TEXT,
            date TEXT,
            new_symptoms TEXT,
            fatigue_level INTEGER,
            sleep_hours INTEGER,
            medication_taken TEXT
        )''')
    # Ensure all stage tables exist
    for tbl in ["stage1_daily_logs", "stage2_daily_logs", "stage3_daily_logs", "stage4_daily_logs"]:
        c.execute(f'''CREATE TABLE IF NOT EXISTS {tbl} (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            patient_name TEXT,
            date TEXT,
            new_symptoms TEXT,
            fatigue_level INTEGER,
            sleep_hours INTEGER,
            medication_taken TEXT
        )''')
    # Save to stage-specific table
    c.execute(f'''INSERT INTO {table_name} (patient_name, date, new_symptoms, fatigue_level, sleep_hours, medication_taken)
        VALUES (?, ?, ?, ?, ?, ?)''',
        (patient_name, date_str, new_symptoms, fatigue_level, sleep_hours, medication_taken))
    # Also save to central all-patient table
    c.execute('''CREATE TABLE IF NOT EXISTS all_patient_daily_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        patient_name TEXT,
        date TEXT,
        stage TEXT,
        new_symptoms TEXT,
        fatigue_level INTEGER,
        sleep_hours INTEGER,
        medication_taken TEXT
    )''')
    c.execute('''INSERT INTO all_patient_daily_logs (patient_name, date, stage, new_symptoms, fatigue_level, sleep_hours, medication_taken)
        VALUES (?, ?, ?, ?, ?, ?, ?)''',
        (patient_name, date_str, stage, new_symptoms, fatigue_level, sleep_hours, medication_taken))
    conn.commit()
    conn.close()

def update_patient_data(patient_id, age, gender, symptoms, relapse_count, duration_ms):
    db_path = get_db_path()
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute('''UPDATE ms_patients SET age=?, gender=?, symptoms=?, relapse_count=?, duration_ms=? WHERE id=?''',
        (age, gender, symptoms, relapse_count, duration_ms, patient_id))
    conn.commit()
    conn.close()

## Duplicate save_daily_log removed; robust table creation is handled in the earlier definition.

def update_patient_data(patient_id, age, gender, symptoms, relapse_count, duration_ms):
    db_path = get_db_path()
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute('''UPDATE ms_patients SET age=?, gender=?, symptoms=?, relapse_count=?, duration_ms=? WHERE id=?''',
        (age, gender, symptoms, relapse_count, duration_ms, patient_id))
    conn.commit()
    conn.close()

# --- Daily Log Save Helper ---
def save_daily_log(patient_name: str, stage: str, date_str: str, new_symptoms: str, fatigue_level: int, sleep_hours: int, medication_taken: str):
    db_path = get_db_path()
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    # Map stage to table name
    stage_table_map = {
        "Stage 1": "stage1_daily_logs",
        "Stage 2": "stage2_daily_logs",
        "Stage 3": "stage3_daily_logs",
        "Stage 4": "stage4_daily_logs"
    }
    table_name = stage_table_map.get(stage, "stage1_daily_logs")
    # Save to stage-specific table
    c.execute(f'''INSERT INTO {table_name} (patient_name, date, new_symptoms, fatigue_level, sleep_hours, medication_taken)
        VALUES (?, ?, ?, ?, ?, ?)''',
        (patient_name, date_str, new_symptoms, fatigue_level, sleep_hours, medication_taken))
    # Also save to central all-patient table
    c.execute('''CREATE TABLE IF NOT EXISTS all_patient_daily_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        patient_name TEXT,
        date TEXT,
        stage TEXT,
        new_symptoms TEXT,
        fatigue_level INTEGER,
        sleep_hours INTEGER,
        medication_taken TEXT
    )''')
    c.execute('''INSERT INTO all_patient_daily_logs (patient_name, date, stage, new_symptoms, fatigue_level, sleep_hours, medication_taken)
        VALUES (?, ?, ?, ?, ?, ?, ?)''',
        (patient_name, date_str, stage, new_symptoms, fatigue_level, sleep_hours, medication_taken))
    conn.commit()
    conn.close()

def update_patient_data(patient_id, age, gender, symptoms, relapse_count, duration_ms):
    db_path = get_db_path()
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute('''UPDATE ms_patients SET age=?, gender=?, symptoms=?, relapse_count=?, duration_ms=? WHERE id=?''',
        (age, gender, symptoms, relapse_count, duration_ms, patient_id))
    conn.commit()
    conn.close()

# --- Daily Log Save Helper ---
def save_daily_log(patient_name: str, stage: str, date_str: str, new_symptoms: str, fatigue_level: int, sleep_hours: int, medication_taken: str):
    db_path = get_db_path()
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    # Map stage to table name
    stage_table_map = {
        "Stage 1": "stage1_daily_logs",
        "Stage 2": "stage2_daily_logs",
        "Stage 3": "stage3_daily_logs",
        "Stage 4": "stage4_daily_logs"
    }
    table_name = stage_table_map.get(stage, "stage1_daily_logs")
    # Save to stage-specific table
    c.execute(f'''INSERT INTO {table_name} (patient_name, date, new_symptoms, fatigue_level, sleep_hours, medication_taken)
        VALUES (?, ?, ?, ?, ?, ?)''',
        (patient_name, date_str, new_symptoms, fatigue_level, sleep_hours, medication_taken))
    # Also save to central all-patient table
    c.execute('''CREATE TABLE IF NOT EXISTS all_patient_daily_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        patient_name TEXT,
        date TEXT,
        stage TEXT,
        new_symptoms TEXT,
        fatigue_level INTEGER,
        sleep_hours INTEGER,
        medication_taken TEXT
    )''')
    c.execute('''INSERT INTO all_patient_daily_logs (patient_name, date, stage, new_symptoms, fatigue_level, sleep_hours, medication_taken)
        VALUES (?, ?, ?, ?, ?, ?, ?)''',
        (patient_name, date_str, stage, new_symptoms, fatigue_level, sleep_hours, medication_taken))
    conn.commit()
    conn.close()

def update_patient_data(patient_id, age, gender, symptoms, relapse_count, duration_ms):
    db_path = get_db_path()
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute('''UPDATE ms_patients SET age=?, gender=?, symptoms=?, relapse_count=?, duration_ms=? WHERE id=?''',
        (age, gender, symptoms, relapse_count, duration_ms, patient_id))
    conn.commit()
    conn.close()

# --- Daily Log Save Helper ---
def save_daily_log(patient_name: str, stage: str, date_str: str, new_symptoms: str, fatigue_level: int, sleep_hours: int, medication_taken: str):
    db_path = get_db_path()
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    # Map stage to table name
    stage_table_map = {
        "Stage 1": "stage1_daily_logs",
        "Stage 2": "stage2_daily_logs",
        "Stage 3": "stage3_daily_logs",
        "Stage 4": "stage4_daily_logs"
    }
    table_name = stage_table_map.get(stage, "stage1_daily_logs")
    # Save to stage-specific table
    c.execute(f'''INSERT INTO {table_name} (patient_name, date, new_symptoms, fatigue_level, sleep_hours, medication_taken)
        VALUES (?, ?, ?, ?, ?, ?)''',
        (patient_name, date_str, new_symptoms, fatigue_level, sleep_hours, medication_taken))
    # Also save to central all-patient table
    c.execute('''CREATE TABLE IF NOT EXISTS all_patient_daily_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        patient_name TEXT,
        date TEXT,
        stage TEXT,
        new_symptoms TEXT,
        fatigue_level INTEGER,
        sleep_hours INTEGER,
        medication_taken TEXT
    )''')
    c.execute('''INSERT INTO all_patient_daily_logs (patient_name, date, stage, new_symptoms, fatigue_level, sleep_hours, medication_taken)
        VALUES (?, ?, ?, ?, ?, ?, ?)''',
        (patient_name, date_str, stage, new_symptoms, fatigue_level, sleep_hours, medication_taken))
    conn.commit()
    conn.close()

def update_patient_data(patient_id, age, gender, symptoms, relapse_count, duration_ms):
    db_path = get_db_path()
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute('''UPDATE ms_patients SET age=?, gender=?, symptoms=?, relapse_count=?, duration_ms=? WHERE id=?''',
        (age, gender, symptoms, relapse_count, duration_ms, patient_id))
    conn.commit()
    conn.close()

# --- Daily Log Save Helper ---
def save_daily_log(patient_name: str, stage: str, date_str: str, new_symptoms: str, fatigue_level: int, sleep_hours: int, medication_taken: str):
    db_path = get_db_path()
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    # Map stage to table name
    stage_table_map = {
        "Stage 1": "stage1_daily_logs",
        "Stage 2": "stage2_daily_logs",
        "Stage 3": "stage3_daily_logs",
        "Stage 4": "stage4_daily_logs"
    }
    table_name = stage_table_map.get(stage, "stage1_daily_logs")
    # Save to stage-specific table
    c.execute(f'''INSERT INTO {table_name} (patient_name, date, new_symptoms, fatigue_level, sleep_hours, medication_taken)
        VALUES (?, ?, ?, ?, ?, ?)''',
        (patient_name, date_str, new_symptoms, fatigue_level, sleep_hours, medication_taken))
    # Also save to central all-patient table
    c.execute('''CREATE TABLE IF NOT EXISTS all_patient_daily_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        patient_name TEXT,
        date TEXT,
        stage TEXT,
        new_symptoms TEXT,
        fatigue_level INTEGER,
        sleep_hours INTEGER,
        medication_taken TEXT
    )''')
    c.execute('''INSERT INTO all_patient_daily_logs (patient_name, date, stage, new_symptoms, fatigue_level, sleep_hours, medication_taken)
        VALUES (?, ?, ?, ?, ?, ?, ?)''',
        (patient_name, date_str, stage, new_symptoms, fatigue_level, sleep_hours, medication_taken))
    conn.commit()
    conn.close()

def update_patient_data(patient_id, age, gender, symptoms, relapse_count, duration_ms):
    db_path = get_db_path()
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute('''UPDATE ms_patients SET age=?, gender=?, symptoms=?, relapse_count=?, duration_ms=? WHERE id=?''',
        (age, gender, symptoms, relapse_count, duration_ms, patient_id))
    conn.commit()
    conn.close()

# --- Daily Log Save Helper ---
def save_daily_log(patient_name: str, stage: str, date_str: str, new_symptoms: str, fatigue_level: int, sleep_hours: int, medication_taken: str):
    db_path = get_db_path()
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    # Map stage to table name
    stage_table_map = {
        "Stage 1": "stage1_daily_logs",
        "Stage 2": "stage2_daily_logs",
        "Stage 3": "stage3_daily_logs",
        "Stage 4": "stage4_daily_logs"
    }
    table_name = stage_table_map.get(stage, "stage1_daily_logs")
    # Save to stage-specific table
    c.execute(f'''INSERT INTO {table_name} (patient_name, date, new_symptoms, fatigue_level, sleep_hours, medication_taken)
        VALUES (?, ?, ?, ?, ?, ?)''',
        (patient_name, date_str, new_symptoms, fatigue_level, sleep_hours, medication_taken))
    # Also save to central all-patient table
    c.execute('''CREATE TABLE IF NOT EXISTS all_patient_daily_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        patient_name TEXT,
        date TEXT,
        stage TEXT,
        new_symptoms TEXT,
        fatigue_level INTEGER,
        sleep_hours INTEGER,
        medication_taken TEXT
    )''')
    c.execute('''INSERT INTO all_patient_daily_logs (patient_name, date, stage, new_symptoms, fatigue_level, sleep_hours, medication_taken)
        VALUES (?, ?, ?, ?, ?, ?, ?)''',
        (patient_name, date_str, stage, new_symptoms, fatigue_level, sleep_hours, medication_taken))
    conn.commit()
    conn.close()

def update_patient_data(patient_id, age, gender, symptoms, relapse_count, duration_ms):
    db_path = get_db_path()
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute('''UPDATE ms_patients SET age=?, gender=?, symptoms=?, relapse_count=?, duration_ms=? WHERE id=?''',
        (age, gender, symptoms, relapse_count, duration_ms, patient_id))
    conn.commit()
    conn.close()

# --- Daily Log Save Helper ---
def save_daily_log(patient_name: str, stage: str, date_str: str, new_symptoms: str, fatigue_level: int, sleep_hours: int, medication_taken: str):
    db_path = get_db_path()
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    # Map stage to table name
    stage_table_map = {
        "Stage 1": "stage1_daily_logs",
        "Stage 2": "stage2_daily_logs",
        "Stage 3": "stage3_daily_logs",
        "Stage 4": "stage4_daily_logs"
    }
    table_name = stage_table_map.get(stage, "stage1_daily_logs")
    # Save to stage-specific table
    c.execute(f'''INSERT INTO {table_name} (patient_name, date, new_symptoms, fatigue_level, sleep_hours, medication_taken)
        VALUES (?, ?, ?, ?, ?, ?)''',
        (patient_name, date_str, new_symptoms, fatigue_level, sleep_hours, medication_taken))
    # Also save to central all-patient table
    c.execute('''CREATE TABLE IF NOT EXISTS all_patient_daily_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        patient_name TEXT,
        date TEXT,
        stage TEXT,
        new_symptoms TEXT,
        fatigue_level INTEGER,
        sleep_hours INTEGER,
        medication_taken TEXT
    )''')
    c.execute('''INSERT INTO all_patient_daily_logs (patient_name, date, stage, new_symptoms, fatigue_level, sleep_hours, medication_taken)
        VALUES (?, ?, ?, ?, ?, ?, ?)''',
        (patient_name, date_str, stage, new_symptoms, fatigue_level, sleep_hours, medication_taken))
    conn.commit()
    conn.close()

def update_patient_data(patient_id, age, gender, symptoms, relapse_count, duration_ms):
    db_path = get_db_path()
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute('''UPDATE ms_patients SET age=?, gender=?, symptoms=?, relapse_count=?, duration_ms=? WHERE id=?''',
        (age, gender, symptoms, relapse_count, duration_ms, patient_id))
    conn.commit()
    conn.close()

# --- Daily Log Save Helper ---
def save_daily_log(patient_name: str, stage: str, date_str: str, new_symptoms: str, fatigue_level: int, sleep_hours: int, medication_taken: str):
    db_path = get_db_path()
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    # Map stage to table name
    stage_table_map = {
        "Stage 1": "stage1_daily_logs",
        "Stage 2": "stage2_daily_logs",
        "Stage 3": "stage3_daily_logs",
        "Stage 4": "stage4_daily_logs"
    }
    table_name = stage_table_map.get(stage, "stage1_daily_logs")
    # Save to stage-specific table
    c.execute(f'''INSERT INTO {table_name} (patient_name, date, new_symptoms, fatigue_level, sleep_hours, medication_taken)
        VALUES (?, ?, ?, ?, ?, ?)''',
        (patient_name, date_str, new_symptoms, fatigue_level, sleep_hours, medication_taken))
    # Also save to central all-patient table
    c.execute('''CREATE TABLE IF NOT EXISTS all_patient_daily_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        patient_name TEXT,
        date TEXT,
        stage TEXT,
        new_symptoms TEXT,
        fatigue_level INTEGER,
        sleep_hours INTEGER,
        medication_taken TEXT
    )''')
    c.execute('''INSERT INTO all_patient_daily_logs (patient_name, date, stage, new_symptoms, fatigue_level, sleep_hours, medication_taken)
        VALUES (?, ?, ?, ?, ?, ?, ?)''',
        (patient_name, date_str, stage, new_symptoms, fatigue_level, sleep_hours, medication_taken))
    conn.commit()
    conn.close()

def update_patient_data(patient_id, age, gender, symptoms, relapse_count, duration_ms):
    db_path = get_db_path()
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute('''UPDATE ms_patients SET age=?, gender=?, symptoms=?, relapse_count=?, duration_ms=? WHERE id=?''',
        (age, gender, symptoms, relapse_count, duration_ms, patient_id))
    conn.commit()
    conn.close()

# --- Daily Log Save Helper ---
def save_daily_log(patient_name: str, stage: str, date_str: str, new_symptoms: str, fatigue_level: int, sleep_hours: int, medication_taken: str):
    db_path = get_db_path()
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    # Map stage to table name
    stage_table_map = {
        "Stage 1": "stage1_daily_logs",
        "Stage 2": "stage2_daily_logs",
        "Stage 3": "stage3_daily_logs",
        "Stage 4": "stage4_daily_logs"
    }
    table_name = stage_table_map.get(stage, "stage1_daily_logs")
    # Save to stage-specific table
    c.execute(f'''INSERT INTO {table_name} (patient_name, date, new_symptoms, fatigue_level, sleep_hours, medication_taken)
        VALUES (?, ?, ?, ?, ?, ?)''',
        (patient_name, date_str, new_symptoms, fatigue_level, sleep_hours, medication_taken))
    # Also save to central all-patient table
    c.execute('''CREATE TABLE IF NOT EXISTS all_patient_daily_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        patient_name TEXT,
        date TEXT,
        stage TEXT,
        new_symptoms TEXT,
        fatigue_level INTEGER,
        sleep_hours INTEGER,
        medication_taken TEXT
    )''')
    c.execute('''INSERT INTO all_patient_daily_logs (patient_name, date, stage, new_symptoms, fatigue_level, sleep_hours, medication_taken)
        VALUES (?, ?, ?, ?, ?, ?, ?)''',
        (patient_name, date_str, stage, new_symptoms, fatigue_level, sleep_hours, medication_taken))
    conn.commit()
    conn.close()

def update_patient_data(patient_id, age, gender, symptoms, relapse_count, duration_ms):
    db_path = get_db_path()
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute('''UPDATE ms_patients SET age=?, gender=?, symptoms=?, relapse_count=?, duration_ms=? WHERE id=?''',
        (age, gender, symptoms, relapse_count, duration_ms, patient_id))
    conn.commit()
    conn.close()

# --- Daily Log Save Helper ---
def save_daily_log(patient_name: str, stage: str, date_str: str, new_symptoms: str, fatigue_level: int, sleep_hours: int, medication_taken: str):
    db_path = get_db_path()
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    # Map stage to table name
    stage_table_map = {
        "Stage 1": "stage1_daily_logs",
        "Stage 2": "stage2_daily_logs",
        "Stage 3": "stage3_daily_logs",
        "Stage 4": "stage4_daily_logs"
    }
    table_name = stage_table_map.get(stage, "stage1_daily_logs")
    # Save to stage-specific table
    c.execute(f'''INSERT INTO {table_name} (patient_name, date, new_symptoms, fatigue_level, sleep_hours, medication_taken)
        VALUES (?, ?, ?, ?, ?, ?)''',
        (patient_name, date_str, new_symptoms, fatigue_level, sleep_hours, medication_taken))
    # Also save to central all-patient table
    c.execute('''CREATE TABLE IF NOT EXISTS all_patient_daily_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        patient_name TEXT,
        date TEXT,
        stage TEXT,
        new_symptoms TEXT,
        fatigue_level INTEGER,
        sleep_hours INTEGER,
        medication_taken TEXT
    )''')
    c.execute('''INSERT INTO all_patient_daily_logs (patient_name, date, stage, new_symptoms, fatigue_level, sleep_hours, medication_taken)
        VALUES (?, ?, ?, ?, ?, ?, ?)''',
        (patient_name, date_str, stage, new_symptoms, fatigue_level, sleep_hours, medication_taken))
    conn.commit()
    conn.close()

def update_patient_data(patient_id, age, gender, symptoms, relapse_count, duration_ms):
    db_path = get_db_path()
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute('''UPDATE ms_patients SET age=?, gender=?, symptoms=?, relapse_count=?, duration_ms=? WHERE id=?''',
        (age, gender, symptoms, relapse_count, duration_ms, patient_id))
    conn.commit()
    conn.close()

# --- Daily Log Save Helper ---
def save_daily_log(patient_name: str, stage: str, date_str: str, new_symptoms: str, fatigue_level: int, sleep_hours: int, medication_taken: str):
    db_path = get_db_path()
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    # Map stage to table name
    stage_table_map = {
        "Stage 1": "stage1_daily_logs",
        "Stage 2": "stage2_daily_logs",
        "Stage 3": "stage3_daily_logs",
        "Stage 4": "stage4_daily_logs"
    }
    table_name = stage_table_map.get(stage, "stage1_daily_logs")
    # Save to stage-specific table
    c.execute(f'''INSERT INTO {table_name} (patient_name, date, new_symptoms, fatigue_level, sleep_hours, medication_taken)
        VALUES (?, ?, ?, ?, ?, ?)''',
        (patient_name, date_str, new_symptoms, fatigue_level, sleep_hours, medication_taken))
    # Also save to central all-patient table
    c.execute('''CREATE TABLE IF NOT EXISTS all_patient_daily_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        patient_name TEXT,
        date TEXT,
        stage TEXT,
        new_symptoms TEXT,
        fatigue_level INTEGER,
        sleep_hours INTEGER,
        medication_taken TEXT
    )''')
    c.execute('''INSERT INTO all_patient_daily_logs (patient_name, date, stage, new_symptoms, fatigue_level, sleep_hours, medication_taken)
        VALUES (?, ?, ?, ?, ?, ?, ?)''',
        (patient_name, date_str, stage, new_symptoms, fatigue_level, sleep_hours, medication_taken))
    conn.commit()
    conn.close()

def update_patient_data(patient_id, age, gender, symptoms, relapse_count, duration_ms):
    db_path = get_db_path()
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute('''UPDATE ms_patients SET age=?, gender=?, symptoms=?, relapse_count=?, duration_ms=? WHERE id=?''',
        (age, gender, symptoms, relapse_count, duration_ms, patient_id))
    conn.commit()
    conn.close()

# --- Daily Log Save Helper ---
def save_daily_log(patient_name: str, stage: str, date_str: str, new_symptoms: str, fatigue_level: int, sleep_hours: int, medication_taken: str):
    db_path = get_db_path()
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    # Map stage to table name
    stage_table_map = {
        "Stage 1": "stage1_daily_logs",
        "Stage 2": "stage2_daily_logs",
        "Stage 3": "stage3_daily_logs",
        "Stage 4": "stage4_daily_logs"
    }
    table_name = stage_table_map.get(stage, "stage1_daily_logs")
    # Save to stage-specific table
    c.execute(f'''INSERT INTO {table_name} (patient_name, date, new_symptoms, fatigue_level, sleep_hours, medication_taken)
        VALUES (?, ?, ?, ?, ?, ?)''',
        (patient_name, date_str, new_symptoms, fatigue_level, sleep_hours, medication_taken))
    # Also save to central all-patient table
    c.execute('''CREATE TABLE IF NOT EXISTS all_patient_daily_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        patient_name TEXT,
        date TEXT,
        stage TEXT,
        new_symptoms TEXT,
        fatigue_level INTEGER,
        sleep_hours INTEGER,
        medication_taken TEXT
    )''')
    c.execute('''INSERT INTO all_patient_daily_logs (patient_name, date, stage, new_symptoms, fatigue_level, sleep_hours, medication_taken)
        VALUES (?, ?, ?, ?, ?, ?, ?)''',
        (patient_name, date_str, stage, new_symptoms, fatigue_level, sleep_hours, medication_taken))
    conn.commit()
    conn.close()

def update_patient_data(patient_id, age, gender, symptoms, relapse_count, duration_ms):
    db_path = get_db_path()
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute('''UPDATE ms_patients SET age=?, gender=?, symptoms=?, relapse_count=?, duration_ms=? WHERE id=?''',
        (age, gender, symptoms, relapse_count, duration_ms, patient_id))
    conn.commit()
    conn.close()

# --- Daily Log Save Helper ---
def save_daily_log(patient_name: str, stage: str, date_str: str, new_symptoms: str, fatigue_level: int, sleep_hours: int, medication_taken: str):
    db_path = get_db_path()
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    # Map stage to table name
    stage_table_map = {
        "Stage 1": "stage1_daily_logs",
        "Stage 2": "stage2_daily_logs",
        "Stage 3": "stage3_daily_logs",
        "Stage 4": "stage4_daily_logs"
    }
    table_name = stage_table_map.get(stage, "stage1_daily_logs")
    # Save to stage-specific table
    c.execute(f'''INSERT INTO {table_name} (patient_name, date, new_symptoms, fatigue_level, sleep_hours, medication_taken)
        VALUES (?, ?, ?, ?, ?, ?)''',
        (patient_name, date_str, new_symptoms, fatigue_level, sleep_hours, medication_taken))
    # Also save to central all-patient table
    c.execute('''CREATE TABLE IF NOT EXISTS all_patient_daily_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        patient_name TEXT,
        date TEXT,
        stage TEXT,
        new_symptoms TEXT,
        fatigue_level INTEGER,
        sleep_hours INTEGER,
        medication_taken TEXT
    )''')
    c.execute('''INSERT INTO all_patient_daily_logs (patient_name, date, stage, new_symptoms, fatigue_level, sleep_hours, medication_taken)
        VALUES (?, ?, ?, ?, ?, ?, ?)''',
        (patient_name, date_str, stage, new_symptoms, fatigue_level, sleep_hours, medication_taken))
    conn.commit()
    conn.close()

def update_patient_data(patient_id, age, gender, symptoms, relapse_count, duration_ms):
    db_path = get_db_path()
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute('''UPDATE ms_patients SET age=?, gender=?, symptoms=?, relapse_count=?, duration_ms=? WHERE id=?''',
        (age, gender, symptoms, relapse_count, duration_ms, patient_id))
    conn.commit()
    conn.close()

# --- Daily Log Save Helper ---
def save_daily_log(patient_name: str, stage: str, date_str: str, new_symptoms: str, fatigue_level: int, sleep_hours: int, medication_taken: str):
    db_path = get_db_path()
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    # Map stage to table name
    stage_table_map = {
        "Stage 1": "stage1_daily_logs",
        "Stage 2": "stage2_daily_logs",
        "Stage 3": "stage3_daily_logs",
        "Stage 4": "stage4_daily_logs"
    }
    table_name = stage_table_map.get(stage, "stage1_daily_logs")
    # Save to stage-specific table
    c.execute(f'''INSERT INTO {table_name} (patient_name, date, new_symptoms, fatigue_level, sleep_hours, medication_taken)
        VALUES (?, ?, ?, ?, ?, ?)''',
        (patient_name, date_str, new_symptoms, fatigue_level, sleep_hours, medication_taken))
    # Also save to central all-patient table
    c.execute('''CREATE TABLE IF NOT EXISTS all_patient_daily_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        patient_name TEXT,
        date TEXT,
        stage TEXT,
        new_symptoms TEXT,
        fatigue_level INTEGER,
        sleep_hours INTEGER,
        medication_taken TEXT
    )''')
    c.execute('''INSERT INTO all_patient_daily_logs (patient_name, date, stage, new_symptoms, fatigue_level, sleep_hours, medication_taken)
        VALUES (?, ?, ?, ?, ?, ?, ?)''',
        (patient_name, date_str, stage, new_symptoms, fatigue_level, sleep_hours, medication_taken))
    conn.commit()
    conn.close()

def update_patient_data(patient_id, age, gender, symptoms, relapse_count, duration_ms):
    db_path = get_db_path()
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute('''UPDATE ms_patients SET age=?, gender=?, symptoms=?, relapse_count=?, duration_ms=? WHERE id=?''',
        (age, gender, symptoms, relapse_count, duration_ms, patient_id))
    conn.commit()
    conn.close()

# --- Daily Log Save Helper ---
def save_daily_log(patient_name: str, stage: str, date_str: str, new_symptoms: str, fatigue_level: int, sleep_hours: int, medication_taken: str):
    db_path = get_db_path()
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    # Map stage to table name
    stage_table_map = {
        "Stage 1": "stage1_daily_logs",
        "Stage 2": "stage2_daily_logs",
        "Stage 3": "stage3_daily_logs",
        "Stage 4": "stage4_daily_logs"
    }
    table_name = stage_table_map.get(stage, "stage1_daily_logs")
    # Save to stage-specific table
    c.execute(f'''INSERT INTO {table_name} (patient_name, date, new_symptoms, fatigue_level, sleep_hours, medication_taken)
        VALUES (?, ?, ?, ?, ?, ?)''',
        (patient_name, date_str, new_symptoms, fatigue_level, sleep_hours, medication_taken))
    # Also save to central all-patient table
    c.execute('''CREATE TABLE IF NOT EXISTS all_patient_daily_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        patient_name TEXT,
        date TEXT,
        stage TEXT,
        new_symptoms TEXT,
        fatigue_level INTEGER,
        sleep_hours INTEGER,
        medication_taken TEXT
    )''')
    c.execute('''INSERT INTO all_patient_daily_logs (patient_name, date, stage, new_symptoms, fatigue_level, sleep_hours, medication_taken)
        VALUES (?, ?, ?, ?, ?, ?, ?)''',
        (patient_name, date_str, stage, new_symptoms, fatigue_level, sleep_hours, medication_taken))
    conn.commit()
    conn.close()

def update_patient_data(patient_id, age, gender, symptoms, relapse_count, duration_ms):
    db_path = get_db_path()
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute('''UPDATE ms_patients SET age=?, gender=?, symptoms=?, relapse_count=?, duration_ms=? WHERE id=?''',
        (age, gender, symptoms, relapse_count, duration_ms, patient_id))
    conn.commit()
    conn.close()

# --- Daily Log Save Helper ---
def save_daily_log(patient_name: str, stage: str, date_str: str, new_symptoms: str, fatigue_level: int, sleep_hours: int, medication_taken: str):
    db_path = get_db_path()
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    # Map stage to table name
    stage_table_map = {
        "Stage 1": "stage1_daily_logs",
        "Stage 2": "stage2_daily_logs",
        "Stage 3": "stage3_daily_logs",
        "Stage 4": "stage4_daily_logs"
    }
    table_name = stage_table_map.get(stage, "stage1_daily_logs")
    # Save to stage-specific table
    c.execute(f'''INSERT INTO {table_name} (patient_name, date, new_symptoms, fatigue_level, sleep_hours, medication_taken)
        VALUES (?, ?, ?, ?, ?, ?)''',
        (patient_name, date_str, new_symptoms, fatigue_level, sleep_hours, medication_taken))
    # Also save to central all-patient table
    c.execute('''CREATE TABLE IF NOT EXISTS all_patient_daily_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        patient_name TEXT,
        date TEXT,
        stage TEXT,
        new_symptoms TEXT,
        fatigue_level INTEGER,
        sleep_hours INTEGER,
        medication_taken TEXT
    )''')
    c.execute('''INSERT INTO all_patient_daily_logs (patient_name, date, stage, new_symptoms, fatigue_level, sleep_hours, medication_taken)
        VALUES (?, ?, ?, ?, ?, ?, ?)''',
        (patient_name, date_str, stage, new_symptoms, fatigue_level, sleep_hours, medication_taken))
    conn.commit()
    conn.close()

def update_patient_data(patient_id, age, gender, symptoms, relapse_count, duration_ms):
    db_path = get_db_path()
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute('''UPDATE ms_patients SET age=?, gender=?, symptoms=?, relapse_count=?, duration_ms=? WHERE id=?''',
        (age, gender, symptoms, relapse_count, duration_ms, patient_id))
    conn.commit()
    conn.close()

# --- Daily Log Save Helper ---
def save_daily_log(patient_name: str, stage: str, date_str: str, new_symptoms: str, fatigue_level: int, sleep_hours: int, medication_taken: str):
    db_path = get_db_path()
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    # Map stage to table name
    stage_table_map = {
        "Stage 1": "stage1_daily_logs",
        "Stage 2": "stage2_daily_logs",
        "Stage 3": "stage3_daily_logs",
        "Stage 4": "stage4_daily_logs"
    }
    table_name = stage_table_map.get(stage, "stage1_daily_logs")
    # Save to stage-specific table
    c.execute(f'''INSERT INTO {table_name} (patient_name, date, new_symptoms, fatigue_level, sleep_hours, medication_taken)
        VALUES (?, ?, ?, ?, ?, ?)''',
        (patient_name, date_str, new_symptoms, fatigue_level, sleep_hours, medication_taken))
    # Also save to central all-patient table
    c.execute('''CREATE TABLE IF NOT EXISTS all_patient_daily_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        patient_name TEXT,
        date TEXT,
        stage TEXT,
        new_symptoms TEXT,
        fatigue_level INTEGER,
        sleep_hours INTEGER,
        medication_taken TEXT
    )''')
    c.execute('''INSERT INTO all_patient_daily_logs (patient_name, date, stage, new_symptoms, fatigue_level, sleep_hours, medication_taken)
        VALUES (?, ?, ?, ?, ?, ?, ?)''',
        (patient_name, date_str, stage, new_symptoms, fatigue_level, sleep_hours, medication_taken))
    conn.commit()
    conn.close()

def update_patient_data(patient_id, age, gender, symptoms, relapse_count, duration_ms):
    db_path = get_db_path()
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute('''UPDATE ms_patients SET age=?, gender=?, symptoms=?, relapse_count=?, duration_ms=? WHERE id=?''',
        (age, gender, symptoms, relapse_count, duration_ms, patient_id))
    conn.commit()
    conn.close()

# --- Daily Log Save Helper ---
def save_daily_log(patient_name: str, stage: str, date_str: str, new_symptoms: str, fatigue_level: int, sleep_hours: int, medication_taken: str):
    db_path = get_db_path()
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    # Map stage to table name
    stage_table_map = {
        "Stage 1": "stage1_daily_logs",
        "Stage 2": "stage2_daily_logs",
        "Stage 3": "stage3_daily_logs",
        "Stage 4": "stage4_daily_logs"
    }
    table_name = stage_table_map.get(stage, "stage1_daily_logs")
    # Save to stage-specific table
    c.execute(f'''INSERT INTO {table_name} (patient_name, date, new_symptoms, fatigue_level, sleep_hours, medication_taken)
        VALUES (?, ?, ?, ?, ?, ?)''',
        (patient_name, date_str, new_symptoms, fatigue_level, sleep_hours, medication_taken))
    # Also save to central all-patient table
    c.execute('''CREATE TABLE IF NOT EXISTS all_patient_daily_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        patient_name TEXT,
        date TEXT,
        stage TEXT,
        new_symptoms TEXT,
        fatigue_level INTEGER,
        sleep_hours INTEGER,
        medication_taken TEXT
    )''')
    c.execute('''INSERT INTO all_patient_daily_logs (patient_name, date, stage, new_symptoms, fatigue_level, sleep_hours, medication_taken)
        VALUES (?, ?, ?, ?, ?, ?, ?)''',
        (patient_name, date_str, stage, new_symptoms, fatigue_level, sleep_hours, medication_taken))
    conn.commit()
    conn.close()

def update_patient_data(patient_id, age, gender, symptoms, relapse_count, duration_ms):
    db_path = get_db_path()
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute('''UPDATE ms_patients SET age=?, gender=?, symptoms=?, relapse_count=?, duration_ms=? WHERE id=?''',
        (age, gender, symptoms, relapse_count, duration_ms, patient_id))
    conn.commit()
    conn.close()

# --- Daily Log Save Helper ---
def save_daily_log(patient_name: str, stage: str, date_str: str, new_symptoms: str, fatigue_level: int, sleep_hours: int, medication_taken: str):
    db_path = get_db_path()
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    # Map stage to table name
    stage_table_map = {
        "Stage 1": "stage1_daily_logs",
        "Stage 2": "stage2_daily_logs",
        "Stage 3": "stage3_daily_logs",
        "Stage 4": "stage4_daily_logs"
    }
    table_name = stage_table_map.get(stage, "stage1_daily_logs")
    # Save to stage-specific table
    c.execute(f'''INSERT INTO {table_name} (patient_name, date, new_symptoms, fatigue_level, sleep_hours, medication_taken)
        VALUES (?, ?, ?, ?, ?, ?)''',
        (patient_name, date_str, new_symptoms, fatigue_level, sleep_hours, medication_taken))
    # Also save to central all-patient table
    c.execute('''CREATE TABLE IF NOT EXISTS all_patient_daily_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        patient_name TEXT,
        date TEXT,
        stage TEXT,
        new_symptoms TEXT,
        fatigue_level INTEGER,
        sleep_hours INTEGER,
        medication_taken TEXT
    )''')
    c.execute('''INSERT INTO all_patient_daily_logs (patient_name, date, stage, new_symptoms, fatigue_level, sleep_hours, medication_taken)
        VALUES (?, ?, ?, ?, ?, ?, ?)''',
        (patient_name, date_str, stage, new_symptoms, fatigue_level, sleep_hours, medication_taken))
    conn.commit()
    conn.close()

def update_patient_data(patient_id, age, gender, symptoms, relapse_count, duration_ms):
    db_path = get_db_path()
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute('''UPDATE ms_patients SET age=?, gender=?, symptoms=?, relapse_count=?, duration_ms=? WHERE id=?''',
        (age, gender, symptoms, relapse_count, duration_ms, patient_id))
    conn.commit()
    conn.close()

# --- Daily Log Save Helper ---
def save_daily_log(patient_name: str, stage: str, date_str: str, new_symptoms: str, fatigue_level: int, sleep_hours: int, medication_taken: str):
    db_path = get_db_path()
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    # Map stage to table name
    stage_table_map = {
        "Stage 1": "stage1_daily_logs",
        "Stage 2": "stage2_daily_logs",
        "Stage 3": "stage3_daily_logs",
        "Stage 4": "stage4_daily_logs"
    }
    table_name = stage_table_map.get(stage, "stage1_daily_logs")
    # Save to stage-specific table
    c.execute(f'''INSERT INTO {table_name} (patient_name, date, new_symptoms, fatigue_level, sleep_hours, medication_taken)
        VALUES (?, ?, ?, ?, ?, ?)''',
        (patient_name, date_str, new_symptoms, fatigue_level, sleep_hours, medication_taken))
    # Also save to central all-patient table
    c.execute('''CREATE TABLE IF NOT EXISTS all_patient_daily_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        patient_name TEXT,
        date TEXT,
        stage TEXT,
        new_symptoms TEXT,
        fatigue_level INTEGER,
        sleep_hours INTEGER,
        medication_taken TEXT
    )''')
    c.execute('''INSERT INTO all_patient_daily_logs (patient_name, date, stage, new_symptoms, fatigue_level, sleep_hours, medication_taken)
        VALUES (?, ?, ?, ?, ?, ?, ?)''',
        (patient_name, date_str, stage, new_symptoms, fatigue_level, sleep_hours, medication_taken))
    conn.commit()
    conn.close()

def update_patient_data(patient_id, age, gender, symptoms, relapse_count, duration_ms):
    db_path = get_db_path()
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute('''UPDATE ms_patients SET age=?, gender=?, symptoms=?, relapse_count=?, duration_ms=? WHERE id=?''',
        (age, gender, symptoms, relapse_count, duration_ms, patient_id))
    conn.commit()
    conn.close()

# --- Daily Log Save Helper ---
def save_daily_log(patient_name: str, stage: str, date_str: str, new_symptoms: str, fatigue_level: int, sleep_hours: int, medication_taken: str):
    db_path = get_db_path()
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    # Map stage to table name
    stage_table_map = {
        "Stage 1": "stage1_daily_logs",
        "Stage 2": "stage2_daily_logs",
        "Stage 3": "stage3_daily_logs",
        "Stage 4": "stage4_daily_logs"
    }
    table_name = stage_table_map.get(stage, "stage1_daily_logs")
    # Save to stage-specific table
    c.execute(f'''INSERT INTO {table_name} (patient_name, date, new_symptoms, fatigue_level, sleep_hours, medication_taken)
        VALUES (?, ?, ?, ?, ?, ?)''',
        (patient_name, date_str, new_symptoms, fatigue_level, sleep_hours, medication_taken))
    # Also save to central all-patient table
    c.execute('''CREATE TABLE IF NOT EXISTS all_patient_daily_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        patient_name TEXT,
        date TEXT,
        stage TEXT,
        new_symptoms TEXT,
        fatigue_level INTEGER,
        sleep_hours INTEGER,
        medication_taken TEXT
    )''')
    c.execute('''INSERT INTO all_patient_daily_logs (patient_name, date, stage, new_symptoms, fatigue_level, sleep_hours, medication_taken)
        VALUES (?, ?, ?, ?, ?, ?, ?)''',
        (patient_name, date_str, stage, new_symptoms, fatigue_level, sleep_hours, medication_taken))
    conn.commit()
    conn.close()

def update_patient_data(patient_id, age, gender, symptoms, relapse_count, duration_ms):
    db_path = get_db_path()
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute('''UPDATE ms_patients SET age=?, gender=?, symptoms=?, relapse_count=?, duration_ms=? WHERE id=?''',
        (age, gender, symptoms, relapse_count, duration_ms, patient_id))
    conn.commit()
    conn.close()

# --- Daily Log Save Helper ---
def save_daily_log(patient_name: str, stage: str, date_str: str, new_symptoms: str, fatigue_level: int, sleep_hours: int, medication_taken: str):
    db_path = get_db_path()
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    # Map stage to table name
    stage_table_map = {
        "Stage 1": "stage1_daily_logs",
        "Stage 2": "stage2_daily_logs",
        "Stage 3": "stage3_daily_logs",
        "Stage 4": "stage4_daily_logs"
    }
    table_name = stage_table_map.get(stage, "stage1_daily_logs")
    # Save to stage-specific table
    c.execute(f'''INSERT INTO {table_name} (patient_name, date, new_symptoms, fatigue_level, sleep_hours, medication_taken)
        VALUES (?, ?, ?, ?, ?, ?)''',
        (patient_name, date_str, new_symptoms, fatigue_level, sleep_hours, medication_taken))
    # Also save to central all-patient table
    c.execute('''CREATE TABLE IF NOT EXISTS all_patient_daily_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        patient_name TEXT,
        date TEXT,
        stage TEXT,
        new_symptoms TEXT,
        fatigue_level INTEGER,
        sleep_hours INTEGER,
        medication_taken TEXT
    )''')
    c.execute('''INSERT INTO all_patient_daily_logs (patient_name, date, stage, new_symptoms, fatigue_level, sleep_hours, medication_taken)
        VALUES (?, ?, ?, ?, ?, ?, ?)''',
        (patient_name, date_str, stage, new_symptoms, fatigue_level, sleep_hours, medication_taken))
    conn.commit()
    conn.close()

def update_patient_data(patient_id, age, gender, symptoms, relapse_count, duration_ms):
    db_path = get_db_path()
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute('''UPDATE ms_patients SET age=?, gender=?, symptoms=?, relapse_count=?, duration_ms=? WHERE id=?''',
        (age, gender, symptoms, relapse_count, duration_ms, patient_id))
    conn.commit()
    conn.close()

# --- Daily Log Save Helper ---
def save_daily_log(patient_name: str, stage: str, date_str: str, new_symptoms: str, fatigue_level: int, sleep_hours: int, medication_taken: str):
    db_path = get_db_path()
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    # Map stage to table name
    stage_table_map = {
        "Stage 1": "stage1_daily_logs",
        "Stage 2": "stage2_daily_logs",
        "Stage 3": "stage3_daily_logs",
        "Stage 4": "stage4_daily_logs"
    }
    table_name = stage_table_map.get(stage, "stage1_daily_logs")
    # Save to stage-specific table
    c.execute(f'''INSERT INTO {table_name} (patient_name, date, new_symptoms, fatigue_level, sleep_hours, medication_taken)
        VALUES (?, ?, ?, ?, ?, ?)''',
        (patient_name, date_str, new_symptoms, fatigue_level, sleep_hours, medication_taken))
    # Also save to central all-patient table
    c.execute('''CREATE TABLE IF NOT EXISTS all_patient_daily_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        patient_name TEXT,
        date TEXT,
        stage TEXT,
        new_symptoms TEXT,
        fatigue_level INTEGER,
        sleep_hours INTEGER,
        medication_taken TEXT
    )''')
    c.execute('''INSERT INTO all_patient_daily_logs (patient_name, date, stage, new_symptoms, fatigue_level, sleep_hours, medication_taken)
        VALUES (?, ?, ?, ?, ?, ?, ?)''',
        (patient_name, date_str, stage, new_symptoms, fatigue_level, sleep_hours, medication_taken))
    conn.commit()
    conn.close()

def update_patient_data(patient_id, age, gender, symptoms, relapse_count, duration_ms):
    db_path = get_db_path()
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute('''UPDATE ms_patients SET age=?, gender=?, symptoms=?, relapse_count=?, duration_ms=? WHERE id=?''',
        (age, gender, symptoms, relapse_count, duration_ms, patient_id))
    conn.commit()
    conn.close()

# --- Daily Log Save Helper ---
def save_daily_log(patient_name: str, stage: str, date_str: str, new_symptoms: str, fatigue_level: int, sleep_hours: int, medication_taken: str):
    db_path = get_db_path()
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    # Map stage to table name
    stage_table_map = {
        "Stage 1": "stage1_daily_logs",
        "Stage 2": "stage2_daily_logs",
        "Stage 3": "stage3_daily_logs",
        "Stage 4": "stage4_daily_logs"
    }
    table_name = stage_table_map.get(stage, "stage1_daily_logs")
    # Save to stage-specific table
    c.execute(f'''INSERT INTO {table_name} (patient_name, date, new_symptoms, fatigue_level, sleep_hours, medication_taken)
        VALUES (?, ?, ?, ?, ?, ?)''',
        (patient_name, date_str, new_symptoms, fatigue_level, sleep_hours, medication_taken))
    # Also save to central all-patient table
    c.execute('''CREATE TABLE IF NOT EXISTS all_patient_daily_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        patient_name TEXT,
        date TEXT,
        stage TEXT,
        new_symptoms TEXT,
        fatigue_level INTEGER,
        sleep_hours INTEGER,
        medication_taken TEXT
    )''')
    c.execute('''INSERT INTO all_patient_daily_logs (patient_name, date, stage, new_symptoms, fatigue_level, sleep_hours, medication_taken)
        VALUES (?, ?, ?, ?, ?, ?, ?)''',
        (patient_name, date_str, stage, new_symptoms, fatigue_level, sleep_hours, medication_taken))
    conn.commit()
    conn.close()

def update_patient_data(patient_id, age, gender, symptoms, relapse_count, duration_ms):
    db_path = get_db_path()
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute('''UPDATE ms_patients SET age=?, gender=?, symptoms=?, relapse_count=?, duration_ms=? WHERE id=?''',
        (age, gender, symptoms, relapse_count, duration_ms, patient_id))
    conn.commit()
    conn.close()

# --- Daily Log Save Helper ---
def save_daily_log(patient_name: str, stage: str, date_str: str, new_symptoms: str, fatigue_level: int, sleep_hours: int, medication_taken: str):
    db_path = get_db_path()
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    # Map stage to table name
    stage_table_map = {
        "Stage 1": "stage1_daily_logs",
        "Stage 2": "stage2_daily_logs",
        "Stage 3": "stage3_daily_logs",
        "Stage 4": "stage4_daily_logs"
    }
    table_name = stage_table_map.get(stage, "stage1_daily_logs")
    # Save to stage-specific table
    c.execute(f'''INSERT INTO {table_name} (patient_name, date, new_symptoms, fatigue_level, sleep_hours, medication_taken)
        VALUES (?, ?, ?, ?, ?, ?)''',
        (patient_name, date_str, new_symptoms, fatigue_level, sleep_hours, medication_taken))
    # Also save to central all-patient table
    c.execute('''CREATE TABLE IF NOT EXISTS all_patient_daily_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        patient_name TEXT,
        date TEXT,
        stage TEXT,
        new_symptoms TEXT,
        fatigue_level INTEGER,
        sleep_hours INTEGER,
        medication_taken TEXT
    )''')
    c.execute('''INSERT INTO all_patient_daily_logs (patient_name, date, stage, new_symptoms, fatigue_level, sleep_hours, medication_taken)
        VALUES (?, ?, ?, ?, ?, ?, ?)''',
        (patient_name, date_str, stage, new_symptoms, fatigue_level, sleep_hours, medication_taken))
    conn.commit()
    conn.close()

def update_patient_data(patient_id, age, gender, symptoms, relapse_count, duration_ms):
    db_path = get_db_path()
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute('''UPDATE ms_patients SET age=?, gender=?, symptoms=?, relapse_count=?, duration_ms=? WHERE id=?''',
        (age, gender, symptoms, relapse_count, duration_ms, patient_id))
    conn.commit()
    conn.close()

# --- Daily Log Save Helper ---
def save_daily_log(patient_name: str, stage: str, date_str: str, new_symptoms: str, fatigue_level: int, sleep_hours: int, medication_taken: str):
    db_path = get_db_path()
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    # Map stage to table name
    stage_table_map = {
        "Stage 1": "stage1_daily_logs",
        "Stage 2": "stage2_daily_logs",
        "Stage 3": "stage3_daily_logs",
        "Stage 4": "stage4_daily_logs"
    }
    table_name = stage_table_map.get(stage, "stage1_daily_logs")
    # Save to stage-specific table
    c.execute(f'''INSERT INTO {table_name} (patient_name, date, new_symptoms, fatigue_level, sleep_hours, medication_taken)
        VALUES (?, ?, ?, ?, ?, ?)''',
        (patient_name, date_str, new_symptoms, fatigue_level, sleep_hours, medication_taken))
    # Also save to central all-patient table
    c.execute('''CREATE TABLE IF NOT EXISTS all_patient_daily_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        patient_name TEXT,
        date TEXT,
        stage TEXT,
        new_symptoms TEXT,
        fatigue_level INTEGER,
        sleep_hours INTEGER,
        medication_taken TEXT
    )''')
    c.execute('''INSERT INTO all_patient_daily_logs (patient_name, date, stage, new_symptoms, fatigue_level, sleep_hours, medication_taken)
        VALUES (?, ?, ?, ?, ?, ?, ?)''',
        (patient_name, date_str, stage, new_symptoms, fatigue_level, sleep_hours, medication_taken))
    conn.commit()
    conn.close()

def update_patient_data(patient_id, age, gender, symptoms, relapse_count, duration_ms):
    db_path = get_db_path()
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute('''UPDATE ms_patients SET age=?, gender=?, symptoms=?, relapse_count=?, duration_ms=? WHERE id=?''',
        (age, gender, symptoms, relapse_count, duration_ms, patient_id))
    conn.commit()
    conn.close()

# --- Daily Log Save Helper ---
def save_daily_log(patient_name: str, stage: str, date_str: str, new_symptoms: str, fatigue_level: int, sleep_hours: int, medication_taken: str):
    db_path = get_db_path()
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    # Map stage to table name
    stage_table_map = {
        "Stage 1": "stage1_daily_logs",
        "Stage 2": "stage2_daily_logs",
        "Stage 3": "stage3_daily_logs",
        "Stage 4": "stage4_daily_logs"
    }
    table_name = stage_table_map.get(stage, "stage1_daily_logs")
    # Save to stage-specific table
    c.execute(f'''INSERT INTO {table_name} (patient_name, date, new_symptoms, fatigue_level, sleep_hours, medication_taken)
        VALUES (?, ?, ?, ?, ?, ?)''',
        (patient_name, date_str, new_symptoms, fatigue_level, sleep_hours, medication_taken))
    # Also save to central all-patient table
    c.execute('''CREATE TABLE IF NOT EXISTS all_patient_daily_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        patient_name TEXT,
        date TEXT,
        stage TEXT,
        new_symptoms TEXT,
        fatigue_level INTEGER,
        sleep_hours INTEGER,
        medication_taken TEXT
    )''')
    c.execute('''INSERT INTO all_patient_daily_logs (patient_name, date, stage, new_symptoms, fatigue_level, sleep_hours, medication_taken)
        VALUES (?, ?, ?, ?, ?, ?, ?)''',
        (patient_name, date_str, stage, new_symptoms, fatigue_level, sleep_hours, medication_taken))
    conn.commit()
    conn.close()

def update_patient_data(patient_id, age, gender, symptoms, relapse_count, duration_ms):
    db_path = get_db_path()
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute('''UPDATE ms_patients SET age=?, gender=?, symptoms=?, relapse_count=?, duration_ms=? WHERE id=?''',
        (age, gender, symptoms, relapse_count, duration_ms, patient_id))
    conn.commit()
    conn.close()

# --- Daily Log Save Helper ---
def save_daily_log(patient_name: str, stage: str, date_str: str, new_symptoms: str, fatigue_level: int, sleep_hours: int, medication_taken: str):
    db_path = get_db_path()
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    # Map stage to table name
    stage_table_map = {
        "Stage 1": "stage1_daily_logs",
        "Stage 2": "stage2_daily_logs",
        "Stage 3": "stage3_daily_logs",
        "Stage 4": "stage4_daily_logs"
    }
    table_name = stage_table_map.get(stage, "stage1_daily_logs")
    # Save to stage-specific table
    c.execute(f'''INSERT INTO {table_name} (patient_name, date, new_symptoms, fatigue_level, sleep_hours, medication_taken)
        VALUES (?, ?, ?, ?, ?, ?)''',
        (patient_name, date_str, new_symptoms, fatigue_level, sleep_hours, medication_taken))
    # Also save to central all-patient table
    c.execute('''CREATE TABLE IF NOT EXISTS all_patient_daily_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        patient_name TEXT,
        date TEXT,
        stage TEXT,
        new_symptoms TEXT,
        fatigue_level INTEGER,
        sleep_hours INTEGER,
        medication_taken TEXT
    )''')
    c.execute('''INSERT INTO all_patient_daily_logs (patient_name, date, stage, new_symptoms, fatigue_level, sleep_hours, medication_taken)
        VALUES (?, ?, ?, ?, ?, ?, ?)''',
        (patient_name, date_str, stage, new_symptoms, fatigue_level, sleep_hours, medication_taken))
    conn.commit()
    conn.close()

def update_patient_data(patient_id, age, gender, symptoms, relapse_count, duration_ms):
    db_path = get_db_path()
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute('''UPDATE ms_patients SET age=?, gender=?, symptoms=?, relapse_count=?, duration_ms=? WHERE id=?''',
        (age, gender, symptoms, relapse_count, duration_ms, patient_id))
    conn.commit()
    conn.close()

# --- Daily Log Save Helper ---
def save_daily_log(patient_name: str, stage: str, date_str: str, new_symptoms: str, fatigue_level: int, sleep_hours: int, medication_taken: str):
    db_path = get_db_path()
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    # Map stage to table name
    stage_table_map = {
        "Stage 1": "stage1_daily_logs",
        "Stage 2": "stage2_daily_logs",
        "Stage 3": "stage3_daily_logs",
        "Stage 4": "stage4_daily_logs"
    }
    table_name = stage_table_map.get(stage, "stage1_daily_logs")
    # Save to stage-specific table
    c.execute(f'''INSERT INTO {table_name} (patient_name, date, new_symptoms, fatigue_level, sleep_hours, medication_taken)
        VALUES (?, ?, ?, ?, ?, ?)''',
        (patient_name, date_str, new_symptoms, fatigue_level, sleep_hours, medication_taken))
    # Also save to central all-patient table
    c.execute('''CREATE TABLE IF NOT EXISTS all_patient_daily_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        patient_name TEXT,
        date TEXT,
        stage TEXT,
        new_symptoms TEXT,
        fatigue_level INTEGER,
        sleep_hours INTEGER,
        medication_taken TEXT
    )''')
    c.execute('''INSERT INTO all_patient_daily_logs (patient_name, date, stage, new_symptoms, fatigue_level, sleep_hours, medication_taken)
        VALUES (?, ?, ?, ?, ?, ?, ?)''',
        (patient_name, date_str, stage, new_symptoms, fatigue_level, sleep_hours, medication_taken))
    conn.commit()
    conn.close()

def update_patient_data(patient_id, age, gender, symptoms, relapse_count, duration_ms):
    db_path = get_db_path()
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute('''UPDATE ms_patients SET age=?, gender=?, symptoms=?, relapse_count=?, duration_ms=? WHERE id=?''',
        (age, gender, symptoms, relapse_count, duration_ms, patient_id))
    conn.commit()
    conn.close()

# --- Daily Log Save Helper ---
def save_daily_log(patient_name: str, stage: str, date_str: str, new_symptoms: str, fatigue_level: int, sleep_hours: int, medication_taken: str):
    db_path = get_db_path()
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    # Map stage to table name
    stage_table_map = {
        "Stage 1": "stage1_daily_logs",
        "Stage 2": "stage2_daily_logs",
        "Stage 3": "stage3_daily_logs",
        "Stage 4": "stage4_daily_logs"
    }
    table_name = stage_table_map.get(stage, "stage1_daily_logs")
    # Save to stage-specific table
    c.execute(f'''INSERT INTO {table_name} (patient_name, date, new_symptoms, fatigue_level, sleep_hours, medication_taken)
        VALUES (?, ?, ?, ?, ?, ?)''',
        (patient_name, date_str, new_symptoms, fatigue_level, sleep_hours, medication_taken))
    # Also save to central all-patient table
    c.execute('''CREATE TABLE IF NOT EXISTS all_patient_daily_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        patient_name TEXT,
        date TEXT,
        stage TEXT,
        new_symptoms TEXT,
        fatigue_level INTEGER,
        sleep_hours INTEGER,
        medication_taken TEXT
    )''')
    c.execute('''INSERT INTO all_patient_daily_logs (patient_name, date, stage, new_symptoms, fatigue_level, sleep_hours, medication_taken)
        VALUES (?, ?, ?, ?, ?, ?, ?)''',
        (patient_name, date_str, stage, new_symptoms, fatigue_level, sleep_hours, medication_taken))
    conn.commit()
    conn.close()

def update_patient_data(patient_id, age, gender, symptoms, relapse_count, duration_ms):
    db_path = get_db_path()
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute('''UPDATE ms_patients SET age=?, gender=?, symptoms=?, relapse_count=?, duration_ms=? WHERE id=?''',
        (age, gender, symptoms, relapse_count, duration_ms, patient_id))
    conn.commit()
    conn.close()

# --- Daily Log Save Helper ---
def save_daily_log(patient_name: str, stage: str, date_str: str, new_symptoms: str, fatigue_level: int, sleep_hours: int, medication_taken: str):
    db_path = get_db_path()
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    # Map stage to table name
    stage_table_map = {
        "Stage 1": "stage1_daily_logs",
        "Stage 2": "stage2_daily_logs",
        "Stage 3": "stage3_daily_logs",
        "Stage 4": "stage4_daily_logs"
    }
    table_name = stage_table_map.get(stage, "stage1_daily_logs")
    # Save to stage-specific table
    c.execute(f'''INSERT INTO {table_name} (patient_name, date, new_symptoms, fatigue_level, sleep_hours, medication_taken)
        VALUES (?, ?, ?, ?, ?, ?)''',
        (patient_name, date_str, new_symptoms, fatigue_level, sleep_hours, medication_taken))
    # Also save to central all-patient table
    c.execute('''CREATE TABLE IF NOT EXISTS all_patient_daily_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        patient_name TEXT,
        date TEXT,
        stage TEXT,
        new_symptoms TEXT,
        fatigue_level INTEGER,
        sleep_hours INTEGER,
        medication_taken TEXT
    )''')
    c.execute('''INSERT INTO all_patient_daily_logs (patient_name, date, stage, new_symptoms, fatigue_level, sleep_hours, medication_taken)
        VALUES (?, ?, ?, ?, ?, ?, ?)''',
        (patient_name, date_str, stage, new_symptoms, fatigue_level, sleep_hours, medication_taken))
    conn.commit()
    conn.close()

def update_patient_data(patient_id, age, gender, symptoms, relapse_count, duration_ms):
    db_path = get_db_path()
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute('''UPDATE ms_patients SET age=?, gender=?, symptoms=?, relapse_count=?, duration_ms=? WHERE id=?''',
        (age, gender, symptoms, relapse_count, duration_ms, patient_id))
    conn.commit()
    conn.close()

# --- Daily Log Save Helper ---
def save_daily_log(patient_name: str, stage: str, date_str: str, new_symptoms: str, fatigue_level: int, sleep_hours: int, medication_taken: str):
    db_path = get_db_path()
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    # Map stage to table name
    stage_table_map = {
        "Stage 1": "stage1_daily_logs",
        "Stage 2": "stage2_daily_logs",
        "Stage 3": "stage3_daily_logs",
        "Stage 4": "stage4_daily_logs"
    }
    table_name = stage_table_map.get(stage, "stage1_daily_logs")
    # Save to stage-specific table
    c.execute(f'''INSERT INTO {table_name} (patient_name, date, new_symptoms, fatigue_level, sleep_hours, medication_taken)
        VALUES (?, ?, ?, ?, ?, ?)''',
        (patient_name, date_str, new_symptoms, fatigue_level, sleep_hours, medication_taken))
    # Also save to central all-patient table
    c.execute('''CREATE TABLE IF NOT EXISTS all_patient_daily_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        patient_name TEXT,
        date TEXT,
        stage TEXT,
        new_symptoms TEXT,
        fatigue_level INTEGER,
        sleep_hours INTEGER,
        medication_taken TEXT
    )''')
    c.execute('''INSERT INTO all_patient_daily_logs (patient_name, date, stage, new_symptoms, fatigue_level, sleep_hours, medication_taken)
        VALUES (?, ?, ?, ?, ?, ?, ?)''',
        (patient_name, date_str, stage, new_symptoms, fatigue_level, sleep_hours, medication_taken))
    conn.commit()
    conn.close()

def update_patient_data(patient_id, age, gender, symptoms, relapse_count, duration_ms):
    db_path = get_db_path()
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute('''UPDATE ms_patients SET age=?, gender=?, symptoms=?, relapse_count=?, duration_ms=? WHERE id=?''',
        (age, gender, symptoms, relapse_count, duration_ms, patient_id))
    conn.commit()
    conn.close()

# --- Daily Log Save Helper ---
def save_daily_log(patient_name: str, stage: str, date_str: str, new_symptoms: str, fatigue_level: int, sleep_hours: int, medication_taken: str):
    db_path = get_db_path()
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    # Map stage to table name
    stage_table_map = {
        "Stage 1": "stage1_daily_logs",
        "Stage 2": "stage2_daily_logs",
        "Stage 3": "stage3_daily_logs",
        "Stage 4": "stage4_daily_logs"
    }
    table_name = stage_table_map.get(stage, "stage1_daily_logs")
    # Save to stage-specific table
    c.execute(f'''INSERT INTO {table_name} (patient_name, date, new_symptoms, fatigue_level, sleep_hours, medication_taken)
        VALUES (?, ?, ?, ?, ?, ?)''',
        (patient_name, date_str, new_symptoms, fatigue_level, sleep_hours, medication_taken))
    # Also save to central all-patient table
    c.execute('''CREATE TABLE IF NOT EXISTS all_patient_daily_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        patient_name TEXT,
        date TEXT,
        stage TEXT,
        new_symptoms TEXT,
        fatigue_level INTEGER,
        sleep_hours INTEGER,
        medication_taken TEXT
    )''')
    c.execute('''INSERT INTO all_patient_daily_logs (patient_name, date, stage, new_symptoms, fatigue_level, sleep_hours, medication_taken)
        VALUES (?, ?, ?, ?, ?, ?, ?)''',
        (patient_name, date_str, stage, new_symptoms, fatigue_level, sleep_hours, medication_taken))
    conn.commit()
    conn.close()

def update_patient_data(patient_id, age, gender, symptoms, relapse_count, duration_ms):
    db_path = get_db_path()
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute('''UPDATE ms_patients SET age=?, gender=?, symptoms=?, relapse_count=?, duration_ms=? WHERE id=?''',
        (age, gender, symptoms, relapse_count, duration_ms, patient_id))
    conn.commit()
    conn.close()

# --- Daily Log Save Helper ---
def save_daily_log(patient_name: str, stage: str, date_str: str, new_symptoms: str, fatigue_level: int, sleep_hours: int, medication_taken: str):
    db_path = get_db_path()
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    # Map stage to table name
    stage_table_map = {
        "Stage 1": "stage1_daily_logs",
        "Stage 2": "stage2_daily_logs",
        "Stage 3": "stage3_daily_logs",
        "Stage 4": "stage4_daily_logs"
    }
    table_name = stage_table_map.get(stage, "stage1_daily_logs")
    # Save to stage-specific table
    c.execute(f'''INSERT INTO {table_name} (patient_name, date, new_symptoms, fatigue_level, sleep_hours, medication_taken)
        VALUES (?, ?, ?, ?, ?, ?)''',
        (patient_name, date_str, new_symptoms, fatigue_level, sleep_hours, medication_taken))
    # Also save to central all-patient table
    c.execute('''CREATE TABLE IF NOT EXISTS all_patient_daily_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        patient_name TEXT,
        date TEXT,
        stage TEXT,
        new_symptoms TEXT,
        fatigue_level INTEGER,
        sleep_hours INTEGER,
        medication_taken TEXT
    )''')
    c.execute('''INSERT INTO all_patient_daily_logs (patient_name, date, stage, new_symptoms, fatigue_level, sleep_hours, medication_taken)
        VALUES (?, ?, ?, ?, ?, ?, ?)''',
        (patient_name, date_str, stage, new_symptoms, fatigue_level, sleep_hours, medication_taken))
    conn.commit()
    conn.close()

# --- Streamlit App ---
st.title("MS Patient Classification")
tab_daily_log, tab_admin, tab_insights = st.tabs([
    "Patient Daily Log", "Patients Admin", "Insights Admin"
])

with tab_daily_log:
    st.header("Patient Daily Log Entry")
    rows, columns = fetch_all_patients()
    if rows:
        name_index = columns.index('name') if 'name' in columns else 1
        patient_names = [row[name_index] for row in rows]
        selected_name = st.selectbox("Select Patient Name", patient_names, key="dailylog_patient_select")
        selected_row = next((row for row in rows if row[name_index] == selected_name), None)
        if selected_row:
            age = selected_row[2]
            relapse_count = selected_row[5]
            duration_ms = selected_row[6]
            # Determine MS stage
            stage_age, _ = categorize_ms_stage_by_age(age)
            stage_duration, _ = categorize_ms_stage_by_duration(duration_ms)
            stage_relapse, _ = categorize_ms_stage_by_relapse_count(relapse_count)
            stages = [stage_age, stage_duration, stage_relapse]
            stage_counts = Counter(stages)
            most_common_stage = max(stage_counts, key=stage_counts.get)
            stage_map = {
                "Clinically Isolated Syndrome (CIS)": 1,
                "Relapsing-Remitting MS (RRMS)": 2,
                "Secondary Progressive MS (SPMS)": 3,
                "Primary Progressive MS (PPMS)": 4
            }
            stage_number = stage_map.get(most_common_stage, 1)
            # Render form for each stage
            if stage_number == 1:
                with st.form("stage1_daily_form"):
                    st.subheader("Stage 1 Daily Form (CIS)")
                    new_symptoms = st.text_input("Any new symptoms today?", key="stage1_new_symptoms")
                    st.text_input("Any worsening of existing symptoms?", key="stage1_worsening_symptoms")
                    fatigue_level = st.slider("Fatigue level (0–10):", 0, 10, key="stage1_fatigue")
                    st.slider("Cognitive clarity (0–10):", 0, 10, key="stage1_cognitive")
                    st.text_input("Any numbness or tingling today?", key="stage1_numbness")
                    st.text_input("Any balance issues or near-falls?", key="stage1_balance")
                    st.radio("Estimated protein intake today (≥40g?):", ["Yes", "No"], key="stage1_protein")
                    st.radio("Fruit & vegetable servings today (5–9 cups?):", ["Yes", "No"], key="stage1_fruit_veg")
                    st.radio("Did you avoid high-sugar/processed foods?", ["Yes", "No"], key="stage1_avoid_sugar")
                    sleep_hours = st.number_input("Hours of sleep last night:", min_value=0, max_value=24, key="stage1_sleep_hours")
                    st.slider("Sleep quality (0–10):", 0, 10, key="stage1_sleep_quality")
                    st.radio("Exercise or walking today?", ["Yes", "No"], key="stage1_exercise")
                    st.slider("Stress level (0–10):", 0, 10, key="stage1_stress")
                    medication_taken = st.radio("Did you take your MS medication today?", ["Yes", "No"], key="stage1_medication")
                    st.radio("Any symptom lasting >24 hours?", ["Yes", "No"], key="stage1_symptom_24h")
                    submitted = st.form_submit_button("Save Entry")
                    if submitted:
                        save_daily_log(selected_name, "Stage 1", str(date.today()), new_symptoms, fatigue_level, sleep_hours, medication_taken)
                        st.success("Daily log entry saved!")
                        st.rerun()
            elif stage_number == 2:
                with st.form("stage2_daily_form"):
                    st.subheader("Stage 2 Daily Form (RRMS)")
                    new_symptoms = st.text_input("Any new symptoms today?", key="stage2_new_symptoms", placeholder="")
                    st.text_input("Any worsening symptoms?", key="stage2_worsening_symptoms", placeholder="")
                    fatigue_level = st.slider("Fatigue level (0–10):", 0, 10, key="stage2_fatigue")
                    st.slider("Pain level (0–10):", 0, 10, key="stage2_pain")
                    st.text_input("Any muscle stiffness or spasms?", key="stage2_stiffness", placeholder="")
                    st.text_input("Any visual changes today?", key="stage2_visual", placeholder="")
                    st.selectbox("Walking ability today:", ["normal", "slow", "difficult"], key="stage2_walking")
                    st.radio("Did symptoms interfere with daily tasks?", ["Yes", "No"], key="stage2_interfere_tasks")
                    st.radio("Protein intake estimate (met goal?):", ["Yes", "No"], key="stage2_protein")
                    st.text_input("Fruit & vegetable servings today:", key="stage2_fruit_veg", placeholder="")
                    sleep_hours = st.number_input("Hours of sleep:", min_value=0, max_value=24, key="stage2_sleep_hours")
                    st.slider("Sleep quality (0–10):", 0, 10, key="stage2_sleep_quality")
                    st.text_input("Exercise today? Duration/type:", key="stage2_exercise", placeholder="")
                    st.slider("Stress level (0–10):", 0, 10, key="stage2_stress")
                    medication_taken = st.radio("Did you take your medication?", ["Yes", "No"], key="stage2_medication")
                    st.radio("Any symptom lasting >24 hours?", ["Yes", "No"], key="stage2_symptom_24h")
                    submitted = st.form_submit_button("Save Entry")
                    if submitted:
                        save_daily_log(selected_name, "Stage 2", str(date.today()), new_symptoms, fatigue_level, sleep_hours, medication_taken)
                        st.success("Daily log entry saved!")
                        st.rerun()
            elif stage_number == 3:
                with st.form("stage3_daily_form"):
                    st.subheader("Stage 3 Daily Form (SPMS)")
                    new_symptoms = st.text_input("Any new neurological symptoms?", key="stage3_new_neuro_symptoms", placeholder="")
                    st.text_input("Any worsening symptoms today?", key="stage3_worsening_symptoms", placeholder="")
                    fatigue_level = st.slider("Fatigue (0–10):", 0, 10, key="stage3_fatigue")
                    st.slider("Muscle weakness (0–10):", 0, 10, key="stage3_weakness")
                    st.text_input("Balance issues, stumbles, or falls?", key="stage3_balance", placeholder="")
                    st.selectbox("Walking ability:", ["normal", "slow", "support needed"], key="stage3_walking")
                    st.text_input("Bladder or bowel changes today?", key="stage3_bladder_bowel", placeholder="")
                    st.slider("Cognitive clarity (0–10):", 0, 10, key="stage3_cognitive")
                    st.text_input("Memory or focus issues today?", key="stage3_memory_focus", placeholder="")
                    st.text_input("Fine motor difficulty (typing, buttons)?", key="stage3_fine_motor", placeholder="")
                    st.slider("Mood today (0–10):", 0, 10, key="stage3_mood")
                    sleep_hours = st.number_input("Sleep hours:", min_value=0, max_value=24, key="stage3_sleep_hours")
                    st.slider("Sleep quality (0–10):", 0, 10, key="stage3_sleep_quality")
                    medication_taken = st.radio("Did you take your medication?", ["Yes", "No"], key="stage3_medication")
                    st.slider("Stress level (0–10):", 0, 10, key="stage3_stress")
                    st.radio("Any symptom lasting >24 hours?", ["Yes", "No"], key="stage3_symptom_24h")
                    submitted = st.form_submit_button("Save Entry")
                    if submitted:
                        save_daily_log(selected_name, "Stage 3", str(date.today()), new_symptoms, fatigue_level, sleep_hours, medication_taken)
                        st.success("Daily log entry saved!")
                        st.rerun()
            elif stage_number == 4:
                with st.form("stage4_daily_form"):
                    st.subheader("Stage 4 Daily Form (PPMS)")
                    new_symptoms = st.text_input("Any new or worsening symptoms today?", key="stage4_new_worsening_symptoms", placeholder="")
                    fatigue_level = st.slider("Fatigue (0–10):", 0, 10, key="stage4_fatigue")
                    st.slider("Pain (0–10):", 0, 10, key="stage4_pain")
                    st.slider("Weakness (0–10):", 0, 10, key="stage4_weakness")
                    st.selectbox("Walking ability:", ["normal", "slow", "cane", "walker", "wheelchair", "unable"], key="stage4_walking")
                    st.text_input("Any falls or near-falls today?", key="stage4_falls", placeholder="")
                    st.text_input("Bladder or bowel issues today?", key="stage4_bladder_bowel", placeholder="")
                    st.text_input("Any trouble swallowing?", key="stage4_swallowing", placeholder="")
                    st.slider("Cognitive function (0–10):", 0, 10, key="stage4_cognitive")
                    st.text_input("Trouble speaking or finding words?", key="stage4_speaking", placeholder="")
                    st.text_input("Vision issues today?", key="stage4_vision", placeholder="")
                    sleep_hours = st.number_input("Sleep hours:", min_value=0, max_value=24, key="stage4_sleep_hours")
                    st.slider("Sleep quality (0–10):", 0, 10, key="stage4_sleep_quality")
                    medication_taken = st.radio("Did you take your medication?", ["Yes", "No"], key="stage4_medication")
                    st.radio("Did you need help with daily tasks today?", ["Yes", "No"], key="stage4_help_daily_tasks")
                    st.radio("Any symptom lasting >24 hours?", ["Yes", "No"], key="stage4_symptom_24h")
                    submitted = st.form_submit_button("Save Entry")
                    if submitted:
                        save_daily_log(selected_name, "Stage 4", str(date.today()), new_symptoms, fatigue_level, sleep_hours, medication_taken)
                        st.success("Daily log entry saved!")
                        st.rerun()
            else:
                st.info("Unable to determine MS stage for this patient. Please check their data.")

with tab_admin:
    st.header("Saved MS Patient Records")
    subtab_profile, subtab_records = st.tabs(["Profile Info", "Patient Records"])
    with subtab_profile:
        subtab_enter, subtab_update = st.tabs(["Enter Patient Information", "Update Patient Information"])
        with subtab_enter:
            st.subheader("Enter Patient Information")
            with st.form("enter_patient_form"):
                name = st.text_input("Patient Name", key="enter_name")
                age = st.number_input("Age", min_value=0, max_value=120, key="enter_age")
                gender = st.selectbox("Gender", ["Male", "Female", "Other"], key="enter_gender")
                symptoms = st.text_area("Symptoms", key="enter_symptoms")
                relapse_count = st.number_input("Relapse Count", min_value=0, max_value=100, key="enter_relapse_count")
                duration_ms = st.number_input("Duration of MS (years)", min_value=0, max_value=100, key="enter_duration_ms")
                submitted = st.form_submit_button("Save Patient")
                if submitted:
                    save_patient_data(name, age, gender, symptoms, relapse_count, duration_ms)
                    st.success("Patient information saved!")
                    st.rerun()
        with subtab_update:
            st.subheader("Update Patient Information")
            rows, columns = fetch_all_patients()
            if rows:
                patient_ids = [row[0] for row in rows]
                selected_id = st.selectbox("Select Patient ID to Update", patient_ids, key="update_patient_id")
                patient = fetch_patient_by_id(selected_id)
                if patient:
                    with st.form("update_patient_form"):
                        age = st.number_input("Age", min_value=0, max_value=120, value=patient[2], key="update_age")
                        gender = st.selectbox("Gender", ["Male", "Female", "Other"], index=["Male", "Female", "Other"].index(patient[3]), key="update_gender")
                        symptoms = st.text_area("Symptoms", value=patient[4], key="update_symptoms")
                        relapse_count = st.number_input("Relapse Count", min_value=0, max_value=100, value=patient[5], key="update_relapse_count")
                        duration_ms = st.number_input("Duration of MS (years)", min_value=0, max_value=100, value=patient[6], key="update_duration_ms")
                        submitted = st.form_submit_button("Update Patient")
                        delete_submitted = st.form_submit_button("Delete Patient Information")
                        if submitted:
                            update_patient_data(selected_id, age, gender, symptoms, relapse_count, duration_ms)
                            st.success("Patient information updated!")
                            st.rerun()
                        if delete_submitted:
                            db_path = get_db_path()
                            conn = sqlite3.connect(db_path)
                            c = conn.cursor()
                            c.execute('DELETE FROM ms_patients WHERE id=?', (selected_id,))
                            conn.commit()
                            conn.close()
                            st.success("Patient information deleted!")
                            st.rerun()
                else:
                    st.warning("Selected patient not found.")
            else:
                st.info("No patients found to update.")
    with subtab_records:
        rows, columns = fetch_all_patients()
        if rows:
            df = pd.DataFrame(rows, columns=columns)
            cols_to_remove = ['id', 'diagnosis_date', 'last_relapse_date']
            display_columns = [col for col in df.columns if col not in cols_to_remove]
            st.dataframe(df[display_columns])
        # --- Four Daily Log Records Tables by Stage ---
        st.markdown("---")
        st.markdown("<h3 style='color:#2c3e50;'>Daily Log Records by Stage</h3>", unsafe_allow_html=True)
        db_path = get_db_path()
        conn = sqlite3.connect(db_path)
        c = conn.cursor()
        stage_tables = [
            ("stage1_daily_logs", "Stage 1 Daily Logs"),
            ("stage2_daily_logs", "Stage 2 Daily Logs"),
            ("stage3_daily_logs", "Stage 3 Daily Logs"),
            ("stage4_daily_logs", "Stage 4 Daily Logs")
        ]
        # Ensure all stage tables exist before selecting
        for tbl in ["stage1_daily_logs", "stage2_daily_logs", "stage3_daily_logs", "stage4_daily_logs"]:
            c.execute(f'''CREATE TABLE IF NOT EXISTS {tbl} (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                patient_name TEXT,
                date TEXT,
                new_symptoms TEXT,
                fatigue_level INTEGER,
                sleep_hours INTEGER,
                medication_taken TEXT
            )''')
        for table_name, table_title in stage_tables:
            st.markdown(f"<h4 style='color:#2980b9;'>{table_title}</h4>", unsafe_allow_html=True)
            try:
                c.execute(f'SELECT * FROM {table_name}')
                stage_rows = c.fetchall()
                stage_columns = [desc[0] for desc in c.description]
                stage_df = pd.DataFrame(stage_rows, columns=stage_columns)
            except sqlite3.OperationalError:
                stage_df = pd.DataFrame([], columns=["Patient Name", "Date", "New Symptoms", "Fatigue Level", "Sleep Hours", "Medication Taken"])
            st.dataframe(stage_df, height=200)
        # --- Combined Daily Log Table ---
        st.markdown("---")
        st.markdown("<h3 style='color:#16a085;'>All Patient Daily Log Entries</h3>", unsafe_allow_html=True)
        combined_df = pd.DataFrame()
        for table_name, _ in stage_tables:
            try:
                c.execute(f'SELECT * FROM {table_name}')
                rows = c.fetchall()
                columns = [desc[0] for desc in c.description]
                temp_df = pd.DataFrame(rows, columns=columns)
                temp_df['source_table'] = table_name
                combined_df = pd.concat([combined_df, temp_df], ignore_index=True)
            except sqlite3.OperationalError:
                continue
        if not combined_df.empty:
            st.dataframe(combined_df, height=350)
        else:
            st.info("No daily log entries found.")
        conn.close()

with tab_insights:

    st.markdown("### Patient Insights")
    import openai_dailylog_module
    rows, columns = fetch_all_patients()
    if rows:
        df = pd.DataFrame(rows, columns=columns)
        patient_names = [f"{row['name']} (ID: {row['id']})" if 'name' in row and 'id' in row else f"{row[1]} (ID: {row[0]})" for _, row in df.iterrows()]
        selected_patient = st.selectbox("Select Patient", patient_names)
        # Find the selected patient row
        selected_row = None
        for _, row in df.iterrows():
            label = f"{row['name']} (ID: {row['id']})" if 'name' in row and 'id' in row else f"{row[1]} (ID: {row[0]})"
            if label == selected_patient:
                selected_row = row
                break
        if selected_row is not None:
            age = selected_row['age'] if 'age' in selected_row else selected_row[2]
            relapse_count = selected_row['relapse_count'] if 'relapse_count' in selected_row else selected_row[5]
            duration_ms = selected_row['duration_ms'] if 'duration_ms' in selected_row else selected_row[6]
            def classify_stage(age, relapse_count, duration_ms):
                if 20 <= age <= 40 and relapse_count <= 1 and duration_ms <= 1:
                    return 1, "Clinically Isolated Syndrome (CIS)"
                elif 20 < age <= 45 and 2 <= relapse_count <= 10 and 0 < duration_ms <= 15:
                    return 2, "Relapsing-Remitting MS (RRMS)"
                elif 30 < age <= 60 and relapse_count <= 10 and duration_ms > 10:
                    return 3, "Secondary Progressive MS (SPMS)"
                elif age > 40 and relapse_count <= 1 and duration_ms == 0:
                    return 4, "Primary Progressive MS (PPMS)"
                else:
                    return 0, "Unclassified"
            stage_num, stage_name = classify_stage(age, relapse_count, duration_ms)
            action_phrase = ""
            if stage_num == 1:
                action_phrase = "Maintain Healthy Diet"
            elif stage_num == 2:
                action_phrase = "Regular Physical Activity"
            elif stage_num == 3:
                action_phrase = "Stress Reduction Practices"
            elif stage_num == 4:
                action_phrase = "Mobility and Balance"
            what_to_do = ""
            if stage_num == 1:
                what_to_do = "Eat at least 40 grams of protein per day, plus 5–9 cups of fresh fruits and vegetables daily for anti-inflammatory nutrition.​"
            elif stage_num == 2:
                what_to_do = "Engage in moderate exercise (like brisk walking) for at least 150 minutes per week to maintain mobility and fitness.​"
            elif stage_num == 3:
                what_to_do = "Practice mindfulness meditation or stress reduction (such as yoga, breathing exercises, or guided relaxation) for at least 10–20 minutes daily.​"
            elif stage_num == 4:
                what_to_do = "Perform mobility and balance exercises (e.g., walking, stretching, gentle resistance training) for 15–30 minutes most days of the week to preserve physical function.​"
            st.write(f"**MS Stage:** {stage_name} (Stage {stage_num})")
            if action_phrase:
                st.write(f"**Action Phrase:** {action_phrase}")
            if what_to_do:
                st.write(f"**What to Do:** {what_to_do}")
            # Get all OpenAI summaries for this patient, passing stage info
            if st.button("Generate AI Insights for This Patient"):
                patient_name = selected_row['name'] if 'name' in selected_row else selected_row[1]
                results = openai_dailylog_module.process_daily_logs_with_openai(stage_name=stage_name)
                patient_results = [item for item in results if item['log'][0] == patient_name]
                if patient_results:
                    for item in patient_results:
                        st.markdown(f"**Date:** {item['log'][1]}")
                        st.markdown(f"**Daily Log:** {item['log']}")
                        st.markdown(f"**AI Summary:** {item['summary']}")
                        st.markdown("---")
                else:
                    st.info("No daily logs found for this patient.")
    else:
        st.info("No patient data found.")