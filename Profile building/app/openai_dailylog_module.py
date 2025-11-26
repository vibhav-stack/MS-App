import os
import sqlite3
import openai
from dotenv import load_dotenv

def get_db_path():
    return os.path.join(os.path.dirname(__file__), "database", "ms_patients.db")

def fetch_all_daily_logs():
    db_path = get_db_path()
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute('''SELECT patient_name, date, stage, new_symptoms, fatigue_level, sleep_hours, medication_taken FROM all_patient_daily_logs''')
    logs = c.fetchall()
    conn.close()
    return logs

def format_prompt(log, stage_name=None):
    patient_name, date, stage, new_symptoms, fatigue_level, sleep_hours, medication_taken = log
    prompt = (
        f"Patient Daily Log:\n"
        f"Name: {patient_name}\n"
        f"Date: {date}\n"
        f"Stage: {stage}\n"
        f"New Symptoms: {new_symptoms}\n"
        f"Fatigue Level: {fatigue_level}\n"
        f"Sleep Hours: {sleep_hours}\n"
        f"Medication Taken: {medication_taken}\n"
    )
    if stage_name:
        prompt += f"\nClinical Stage Classification: {stage_name}\n"
        prompt += f"\nPlease provide a summary and recommendations tailored to this MS stage and the above daily log."
    else:
        prompt += f"\nPlease provide a summary and any recommendations for this patient based on the above daily log."
    return prompt

def process_daily_logs_with_openai(stage_name=None):
    load_dotenv()
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise EnvironmentError("OPENAI_API_KEY environment variable not set.")
    openai.api_key = api_key
    logs = fetch_all_daily_logs()
    results = []
    for log in logs:
        prompt = format_prompt(log, stage_name=stage_name)
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}]
        )
        summary = response.choices[0].message["content"]
        results.append({"log": log, "summary": summary})
    return results

if __name__ == "__main__":
    results = process_daily_logs_with_openai()
    for item in results:
        print("--- Daily Log ---")
        print(item["log"])
        print("--- OpenAI Summary ---")
        print(item["summary"])
        print()
