# -*- coding: utf-8 -*-
from datetime import datetime
from pathlib import Path
import sqlite3
import json

# Initialize database
db_path = Path.cwd() / "data" / "symptoms.db"
db_path.parent.mkdir(exist_ok=True)

# Create database and table
with sqlite3.connect(str(db_path)) as conn:
    conn.execute("""
        CREATE TABLE IF NOT EXISTS daily_logs (
            date TEXT PRIMARY KEY,
            sleep_hours REAL,
            physical_comfort INTEGER,
            mental_fog BOOLEAN,
            mood TEXT,
            overall_wellbeing INTEGER,
            activity_level INTEGER,
            medication_adherence BOOLEAN,
            notes TEXT,
            pain_symptoms TEXT,
            fatigue_symptoms TEXT,
            temperature_sensitivity TEXT,
            visual_symptoms TEXT
        )
    """)
    
    # Insert test data
    conn.execute("""
        INSERT OR REPLACE INTO daily_logs VALUES (
            ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?
        )
    """, (
        datetime.now().isoformat(),
        8.0,
        7,
        False,
        "HAPPY",
        8,
        3,
        True,
        "Test entry",
        json.dumps([]),
        json.dumps([]),
        json.dumps([]),
        json.dumps([])
    ))
    conn.commit()
    
    # Verify data
    print("\nAll logs in database:")
    cursor = conn.execute("SELECT * FROM daily_logs")
    for row in cursor:
        print(f"Date: {row[0]}, Sleep: {row[1]}, Mood: {row[4]}")
