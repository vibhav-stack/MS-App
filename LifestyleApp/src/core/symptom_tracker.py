from datetime import datetime, timedelta
from typing import List, Optional, Dict, Any
from .models import (
    DailySymptomLog, PainSymptom, FatigueSymptom,
    TemperatureSensitivity, VisualSymptom
)
from .database import SymptomDatabase

class SymptomTracker:
    def __init__(self, db_path: str = 'data/symptoms.db'):
        self.db = SymptomDatabase(db_path)

    def log_symptoms(self, symptoms_data: Dict[str, Any]) -> int:
        """
        Log symptoms for the current day
        Returns the ID of the created log
        """
        daily_log = DailySymptomLog(
            overall_wellbeing=symptoms_data.get('overall_wellbeing', 5),
            notes=symptoms_data.get('notes', '')
        )

        # Add pain symptoms
        for pain_data in symptoms_data.get('pain_symptoms', []):
            daily_log.pain_symptoms.append(PainSymptom(**pain_data))

        # Add fatigue symptoms
        for fatigue_data in symptoms_data.get('fatigue_symptoms', []):
            daily_log.fatigue_symptoms.append(FatigueSymptom(**fatigue_data))

        # Add temperature sensitivity
        for temp_data in symptoms_data.get('temperature_sensitivity', []):
            daily_log.temperature_sensitivity.append(TemperatureSensitivity(**temp_data))

        # Add visual symptoms
        for visual_data in symptoms_data.get('visual_symptoms', []):
            daily_log.visual_symptoms.append(VisualSymptom(**visual_data))

        return self.db.add_daily_log(daily_log)

    def get_todays_log(self) -> Optional[DailySymptomLog]:
        """Get today's symptom log"""
        return self.db.get_daily_log(datetime.now())

    def get_weekly_summary(self) -> Dict[str, Any]:
        """Get a summary of symptoms for the past week"""
        end_date = datetime.now()
        start_date = end_date - timedelta(days=7)
        
        summary = {
            'pain': self.db.get_symptom_statistics('pain', start_date, end_date),
            'fatigue': self.db.get_symptom_statistics('fatigue', start_date, end_date),
            'temperature': self.db.get_symptom_statistics('temperature_sensitivity', start_date, end_date),
            'visual': self.db.get_symptom_statistics('visual', start_date, end_date),
            'overall_wellbeing': {
                'average': 0,
                'trend': []
            }
        }

        logs = self.db.get_logs_range(start_date, end_date)
        if logs:
            wellbeing_scores = [log.overall_wellbeing for log in logs]
            summary['overall_wellbeing']['average'] = sum(wellbeing_scores) / len(wellbeing_scores)
            summary['overall_wellbeing']['trend'] = wellbeing_scores

        return summary

    def get_symptom_history(self, symptom_type: str, days: int = 30) -> List[Dict[str, Any]]:
        """Get historical data for a specific symptom type"""
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        logs = self.db.get_logs_range(start_date, end_date)
        
        history = []
        for log in logs:
            symptoms = getattr(log, f'{symptom_type}_symptoms', [])
            for symptom in symptoms:
                history.append({
                    'date': log.date,
                    'severity': symptom.severity,
                    **symptom.dict(exclude={'severity', 'timestamp'})
                })
        
        return history

    def update_todays_log(self, updated_data: Dict[str, Any]) -> bool:
        """Update today's symptom log with new data"""
        current_log = self.get_todays_log()
        if not current_log:
            self.log_symptoms(updated_data)
            return True

        # Update existing log
        if 'overall_wellbeing' in updated_data:
            current_log.overall_wellbeing = updated_data['overall_wellbeing']
        if 'notes' in updated_data:
            current_log.notes = updated_data['notes']

        # Update specific symptom types
        for symptom_type in ['pain_symptoms', 'fatigue_symptoms', 
                            'temperature_sensitivity', 'visual_symptoms']:
            if symptom_type in updated_data:
                current_symptoms = getattr(current_log, symptom_type)
                new_symptoms_data = updated_data[symptom_type]
                
                # Clear existing and add new
                current_symptoms.clear()
                for symptom_data in new_symptoms_data:
                    symptom_class = globals()[symptom_type[:-1].title().replace('_', '')]
                    current_symptoms.append(symptom_class(**symptom_data))

        return self.db.update_daily_log(datetime.now(), current_log)

    def get_trigger_analysis(self) -> Dict[str, List[Dict[str, Any]]]:
        """Analyze common symptom triggers"""
        end_date = datetime.now()
        start_date = end_date - timedelta(days=90)  # Analysis over 90 days
        
        trigger_analysis = {}
        for symptom_type in ['pain', 'fatigue', 'temperature_sensitivity', 'visual']:
            stats = self.db.get_symptom_statistics(symptom_type, start_date, end_date)
            triggers = stats['common_triggers']
            
            # Sort triggers by frequency
            sorted_triggers = [
                {'trigger': trigger, 'count': count}
                for trigger, count in sorted(
                    triggers.items(),
                    key=lambda x: x[1],
                    reverse=True
                )
            ]
            
            trigger_analysis[symptom_type] = sorted_triggers

        return trigger_analysis