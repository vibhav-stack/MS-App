import os
import sys
from pathlib import Path

# Add the project root to Python path
project_root = str(Path(__file__).resolve().parent)
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from src.core.database import SymptomDatabase

def main():
    # Delete existing database if it exists
    db_path = Path("data/symptoms.db")
    if db_path.exists():
        print(f"Deleting existing database at {db_path}")
        os.remove(db_path)
    
    # Initialize new database
    db = SymptomDatabase()
    print(f"New database initialized at: {db.db_path}")

if __name__ == "__main__":
    main()
