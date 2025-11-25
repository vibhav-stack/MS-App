from typing import Dict, Any, List
from datetime import datetime

def validate_symptom_data(data: Dict[str, Any]) -> List[str]:
    """
    Validate symptom data input
    Returns a list of error messages (empty if validation passes)
    """
    errors = []

    # Validate overall wellbeing
    if 'overall_wellbeing' in data:
        wellbeing = data['overall_wellbeing']
        if not isinstance(wellbeing, int) or wellbeing < 0 or wellbeing > 10:
            errors.append('Overall wellbeing must be an integer between 0 and 10')

    # Validate pain symptoms
    if 'pain_symptoms' in data:
        if not isinstance(data['pain_symptoms'], list):
            errors.append('Pain symptoms must be a list')
        else:
            for i, pain in enumerate(data['pain_symptoms']):
                if not isinstance(pain, dict):
                    errors.append(f'Pain symptom {i} must be a dictionary')
                else:
                    if 'location' not in pain:
                        errors.append(f'Pain symptom {i} must include location')
                    if 'severity' in pain and (not isinstance(pain['severity'], int) or 
                                             pain['severity'] < 0 or pain['severity'] > 10):
                        errors.append(f'Pain symptom {i} severity must be between 0 and 10')

    # Validate fatigue symptoms
    if 'fatigue_symptoms' in data:
        if not isinstance(data['fatigue_symptoms'], list):
            errors.append('Fatigue symptoms must be a list')
        else:
            for i, fatigue in enumerate(data['fatigue_symptoms']):
                if not isinstance(fatigue, dict):
                    errors.append(f'Fatigue symptom {i} must be a dictionary')
                else:
                    if 'energy_level' in fatigue and (not isinstance(fatigue['energy_level'], int) or 
                                                    fatigue['energy_level'] < 0 or fatigue['energy_level'] > 10):
                        errors.append(f'Fatigue symptom {i} energy level must be between 0 and 10')

    # Validate temperature sensitivity
    if 'temperature_sensitivity' in data:
        if not isinstance(data['temperature_sensitivity'], list):
            errors.append('Temperature sensitivity must be a list')
        else:
            for i, temp in enumerate(data['temperature_sensitivity']):
                if not isinstance(temp, dict):
                    errors.append(f'Temperature sensitivity {i} must be a dictionary')
                else:
                    if 'temperature' not in temp:
                        errors.append(f'Temperature sensitivity {i} must include temperature value')
                    if 'environment' not in temp:
                        errors.append(f'Temperature sensitivity {i} must include environment')

    # Validate visual symptoms
    if 'visual_symptoms' in data:
        if not isinstance(data['visual_symptoms'], list):
            errors.append('Visual symptoms must be a list')
        else:
            for i, visual in enumerate(data['visual_symptoms']):
                if not isinstance(visual, dict):
                    errors.append(f'Visual symptom {i} must be a dictionary')
                else:
                    if 'affected_eye' not in visual:
                        errors.append(f'Visual symptom {i} must include affected eye')
                    if 'type' not in visual:
                        errors.append(f'Visual symptom {i} must include type')

    return errors

def validate_date_range(start_date: datetime, end_date: datetime) -> List[str]:
    """
    Validate a date range
    Returns a list of error messages (empty if validation passes)
    """
    errors = []
    
    if not isinstance(start_date, datetime):
        errors.append('Start date must be a datetime object')
    if not isinstance(end_date, datetime):
        errors.append('End date must be a datetime object')
    
    if start_date and end_date and start_date > end_date:
        errors.append('Start date must be before end date')
    
    if start_date and start_date > datetime.now():
        errors.append('Start date cannot be in the future')
    if end_date and end_date > datetime.now():
        errors.append('End date cannot be in the future')
    
    return errors