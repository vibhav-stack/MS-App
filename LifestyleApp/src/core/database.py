import sqlite3
import json
import os
import logging
from datetime import datetime
from typing import Optional, List
from pathlib import Path
from .models import DailySymptomLog, MoodType

# Configure logging for database operations
logger = logging.getLogger(__name__)

class SymptomDatabase:
    def __init__(self):
        # Get absolute path to the database file
        db_path = Path(__file__).resolve().parent.parent.parent / "data" / "symptoms.db"
        logger.info("\n=== Database Initialization ===")
        logger.info(f"Database path: {db_path}")
        logger.info(f"Database parent directory: {db_path.parent}")
        
        # Create and check data directory
        try:
            db_path.parent.mkdir(parents=True, exist_ok=True)
            logger.info(f"Data directory exists: {db_path.parent.exists()}")
            logger.info(f"Data directory is writable: {os.access(db_path.parent, os.W_OK)}")
            if db_path.exists():
                logger.info(f"Database file size: {db_path.stat().st_size} bytes")
            else:
                logger.info("Database file does not exist yet - will be created")
        except Exception as e:
            logger.error(f"Error creating data directory: {e}", exc_info=True)
            raise
            
        self.db_path = str(db_path)
        logger.info(f"Final database path: {self.db_path}")
        self._init_db()

    def _init_db(self):
        """Initialize the database with required tables"""
        with sqlite3.connect(self.db_path) as conn:
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
            conn.commit()

    def _row_to_log(self, row) -> DailySymptomLog:
        """Convert a database row to a DailySymptomLog object"""
        try:
            # Parse date from YYYY-MM-DD format
            date_str = row[0]
            if 'T' not in date_str:  # If it's just a date without time
                date_str += 'T00:00:00'  # Add midnight time
            
            return DailySymptomLog(
                date=datetime.fromisoformat(date_str),
                sleep_hours=row[1],
                physical_comfort=row[2],
                mental_fog=bool(row[3]),
                mood=MoodType[row[4]],
                overall_wellbeing=row[5],
                activity_level=row[6],
                medication_adherence=bool(row[7]),
                notes=row[8],
                pain_symptoms=json.loads(row[9]),
                fatigue_symptoms=json.loads(row[10]),
                temperature_sensitivity=json.loads(row[11]),
                visual_symptoms=json.loads(row[12])
            )
        except Exception as e:
            print(f"Error converting row to log: {e}")
            print(f"Row data: {row}")
            raise

    def add_daily_log(self, log: DailySymptomLog) -> None:
        """Add a daily symptom log to the database"""
        # Ensure date is normalized to start of day
        normalized_date = log.date.replace(hour=0, minute=0, second=0, microsecond=0)
        date_str = normalized_date.strftime('%Y-%m-%d')
        print(f"\n=== Database Operation: Adding Daily Log ===")
        print(f"Input date: {log.date}")
        print(f"Normalized date: {date_str}")
        print(f"Database path: {self.db_path}")
        print(f"Log details:")
        print(f"  - Sleep hours: {log.sleep_hours}")
        print(f"  - Physical comfort: {log.physical_comfort}")
        print(f"  - Mood: {log.mood.name}")
        print(f"  - Overall wellbeing: {log.overall_wellbeing}")
        
        try:
            # Create data directory if it doesn't exist
            db_dir = Path(self.db_path).parent
            db_dir.mkdir(parents=True, exist_ok=True)
            print(f"Ensuring database directory exists: {db_dir}")
            
            with sqlite3.connect(self.db_path) as conn:
                # Enable foreign keys and write-ahead logging for better reliability
                conn.execute("PRAGMA foreign_keys = ON")
                conn.execute("PRAGMA journal_mode = WAL")
                
                # Insert with date string only (no time component)
                print("Executing INSERT OR REPLACE query...")
                conn.execute("""
                    INSERT OR REPLACE INTO daily_logs VALUES (
                        ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?
                    )
                """, (
                    date_str,  # Store date without time component
                    log.sleep_hours,
                    log.physical_comfort,
                    log.mental_fog,
                    log.mood.name,
                    log.overall_wellbeing,
                    log.activity_level,
                    log.medication_adherence,
                    log.notes,
                    json.dumps(log.pain_symptoms),
                    json.dumps(log.fatigue_symptoms),
                    json.dumps(log.temperature_sensitivity),
                    json.dumps(log.visual_symptoms)
                ))
                conn.commit()
                print("Transaction committed successfully")
                
                # Verify the save by reading it back
                cursor = conn.execute("SELECT * FROM daily_logs WHERE date = ?", (date_str,))
                row = cursor.fetchone()
                if row:
                    print(f"Verified: Found log in database for date {row[0]}")
                    print(f"Database entry details: Sleep={row[1]}, Mood={row[4]}, Wellbeing={row[5]}")
                else:
                    print("Warning: Log was not found in database after saving")
        except Exception as e:
            print(f"Error saving log: {str(e)}")
            raise

    def get_daily_log(self, date: datetime) -> Optional[DailySymptomLog]:
        """Get a daily symptom log by date"""
        # Normalize date to YYYY-MM-DD format
        date_str = date.strftime('%Y-%m-%d')
        print(f"Searching for log on date: {date_str}")
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute("SELECT * FROM daily_logs WHERE date = ?", (date_str,))
            row = cursor.fetchone()
            if row:
                print(f"Found log for date {row[0]}")
                return self._row_to_log(row)
            else:
                print(f"No log found for date {date_str}")
                return None
        return None

    def update_daily_log(self, date: datetime, log: DailySymptomLog) -> None:
        """Update an existing daily log"""
        self.add_daily_log(log)  # Using REPLACE INTO in add_daily_log handles updates

    def get_daily_summary(self, date: datetime) -> Optional[DailySymptomLog]:
        """Get the daily summary for a specific date"""
        return self.get_daily_log(date)

    def get_weekly_logs(self, start_date: datetime, end_date: datetime) -> List[DailySymptomLog]:
        """Get all logs between start_date and end_date (inclusive)
        
        This automatically pulls from all daily entries in the date range.
        No separate weekly entry is needed - weekly summaries are calculated from daily entries.
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                print("\n=== Weekly Logs Query ===")
                # Check if database file exists
                print(f"Database file exists: {Path(self.db_path).exists()}")
                print(f"Database file size: {Path(self.db_path).stat().st_size if Path(self.db_path).exists() else 0} bytes")
                
                # Print all tables
                print("\nDatabase tables:")
                cursor = conn.execute("SELECT name FROM sqlite_master WHERE type='table'")
                tables = cursor.fetchall()
                for table in tables:
                    print(f"- {table[0]}")
                
                # Print database contents for debugging
                print("\nDatabase contents:")
                cursor = conn.execute("SELECT * FROM daily_logs")
                all_entries = cursor.fetchall()
                print(f"Found {len(all_entries)} entries:")
                for entry in all_entries:
                    print(f"Entry: Date={entry[0]}, Sleep={entry[1]}, Mood={entry[4]}, Wellbeing={entry[5]}")
                
                # Normalize dates to start/end of day for comparison
                start_date_normalized = start_date.replace(hour=0, minute=0, second=0, microsecond=0)
                end_date_normalized = end_date.replace(hour=23, minute=59, second=59, microsecond=999999)
                
                # Use date-only strings for comparison to avoid time issues
                start_str = start_date_normalized.strftime('%Y-%m-%d')
                end_str = end_date_normalized.strftime('%Y-%m-%d')
                
                print(f"\nQuerying for entries between {start_str} and {end_str}")
                
                # Query using direct date comparison
                cursor = conn.execute(
                    """
                    SELECT * FROM daily_logs 
                    WHERE date >= ? AND date <= ?
                    ORDER BY date
                    """,
                    (start_str, end_str)
                )
                rows = cursor.fetchall()
                print(f"Found {len(rows)} entries in date range")
                for row in rows:
                    print(f"Matched entry: Date={row[0]}, Sleep={row[1]}, Mood={row[4]}, Wellbeing={row[5]}")
                
                return [self._row_to_log(row) for row in rows]
        except Exception as e:
            print(f"Database error in get_weekly_logs: {str(e)}")
            import traceback
            traceback.print_exc()
            return []

    def debug_print_all_logs(self):
        """Print all logs in the database for debugging"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute("SELECT * FROM daily_logs")
            rows = cursor.fetchall()
            print("\nAll logs in database:")
            for row in rows:
                print(f"Date: {row[0]}, Sleep: {row[1]}, Mood: {row[4]}")