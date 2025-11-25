from datetime import datetime
import sys
from pathlib import Path
sys.path.append(str(Path.cwd()))
from src.core.database import SymptomDatabase
from src.core.models import DailySymptomLog, MoodType

# Initialize database
db = SymptomDatabase()

# Create test entry
log = DailySymptomLog(
    date=datetime.now(),
    sleep_hours=8.0,
    physical_comfort=7,
    mental_fog=False,
    mood=MoodType.HAPPY,
    overall_wellbeing=8,
    activity_level=3,
    medication_adherence=True,
    notes='Test entry',
    pain_symptoms=[],
    fatigue_symptoms=[],
    temperature_sensitivity=[],
    visual_symptoms=[]
)

# Save entry
db.add_daily_log(log)

# Verify save
db.debug_print_all_logs()