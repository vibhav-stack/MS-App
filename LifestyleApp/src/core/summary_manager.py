from datetime import datetime, timedelta
from typing import List, Optional, Dict, Any
from .models import DailySummary, WeeklySummary, DailySymptomLog, MoodType

class SummaryManager:
    """Manager class for handling daily and weekly summaries"""
    
    @staticmethod
    def generate_daily_summary(symptom_log: DailySymptomLog) -> DailySummary:
        """Generate a daily summary from a symptom log"""
        total_pain = sum(s.severity for s in symptom_log.pain_symptoms)
        avg_pain = total_pain / len(symptom_log.pain_symptoms) if symptom_log.pain_symptoms else 0
        
        total_fatigue = sum(s.energy_level for s in symptom_log.fatigue_symptoms)
        avg_fatigue = total_fatigue / len(symptom_log.fatigue_symptoms) if symptom_log.fatigue_symptoms else 0
        
        return DailySummary(
            date=symptom_log.date,
            overall_wellbeing=symptom_log.overall_wellbeing,
            average_pain_level=round(avg_pain, 2),
            average_fatigue_level=round(avg_fatigue, 2),
            total_symptoms_reported=(
                len(symptom_log.pain_symptoms) +
                len(symptom_log.fatigue_symptoms) +
                len(symptom_log.temperature_sensitivity) +
                len(symptom_log.visual_symptoms)
            ),
            # These would typically come from user input in the UI
            mood_rating=3,  # Default value
            activity_level=3,  # Default value
            sleep_quality=3,  # Default value
            notes=symptom_log.notes
        )
    
    @staticmethod
    def get_display_data(summary: DailySummary) -> Dict[str, Any]:
        """
        Converts a DailySummary into a display-ready format with all necessary
        visual indicators and color codes
        """
        return {
            "date": summary.date.strftime("%Y-%m-%d"),
            
            "sleep": {
                "value": f"{summary.sleep_hours:.1f} hours",
                "color": summary.sleep_color_code,
                "status": "Low" if summary.sleep_hours < 6 else 
                         "Moderate" if summary.sleep_hours < 7.5 else "Good"
            },
            
            "physical_comfort": {
                "value": summary.physical_comfort,
                "color": summary.physical_comfort_color,
                "display": f"{summary.physical_comfort}/10"
            },
            
            "mental_fog": {
                "value": "Yes" if summary.mental_fog else "No",
                "color": summary.mental_fog_color,
                "icon": "🌫️" if summary.mental_fog else "☀️"
            },
            
            "mood": {
                "value": summary.mood.capitalize(),
                "color": summary.mood_color,
                "icon": "😊" if summary.mood == MoodType.HAPPY else
                       "😢" if summary.mood == MoodType.SAD else
                       "😰" if summary.mood == MoodType.ANXIOUS else "😐"
            },
            
            # Additional metrics for display
            "overall_stats": {
                "wellbeing": f"{summary.overall_wellbeing}/10",
                "pain_level": f"{summary.average_pain_level:.1f}/10",
                "fatigue_level": f"{summary.average_fatigue_level:.1f}/10",
                "symptoms": summary.total_symptoms_reported,
                "medication": "✓" if summary.medication_adherence else "✗"
            }
        }

    @staticmethod
    def get_sleep_recommendation(sleep_hours: float) -> str:
        """Provides sleep-related recommendations based on hours slept"""
        if sleep_hours < 6:
            return "Consider adjusting your schedule to get more rest. Aim for at least 7.5 hours."
        elif sleep_hours < 7.5:
            return "You're getting close to the recommended amount. Try to get an extra 30-60 minutes."
        return "Great job maintaining a healthy sleep schedule!"
        
    @staticmethod
    def analyze_symptom_patterns(daily_summaries: List[DailySummary]) -> dict:
        """Analyze patterns in symptoms over time"""
        patterns = {
            "sleep_pattern": [],
            "comfort_correlation": [],
            "mood_distribution": {},
            "common_combinations": []
        }
        
        # Analyze sleep patterns
        sleep_hours = [ds.sleep_hours for ds in daily_summaries]
        patterns["sleep_pattern"] = {
            "average": sum(sleep_hours) / len(sleep_hours),
            "variance": sum((x - patterns["sleep_pattern"]["average"])**2 for x in sleep_hours) / len(sleep_hours),
            "trend": "Improving" if sleep_hours[-1] > sleep_hours[0] else "Declining"
        }
        
        # Analyze comfort and mood correlations
        for summary in daily_summaries:
            # Track mood distribution
            patterns["mood_distribution"][summary.mood] = patterns["mood_distribution"].get(summary.mood, 0) + 1
            
            # Check for symptom combinations
            if summary.mental_fog and summary.physical_comfort < 5:
                patterns["common_combinations"].append("Mental fog with low physical comfort")
        
        return patterns

    @staticmethod
    def generate_weekly_summary(daily_summaries: List[DailySummary]) -> Optional[WeeklySummary]:
        """Generate a weekly summary from a list of daily summaries"""
        if not daily_summaries:
            return None
            
        # Sort summaries by date
        sorted_summaries = sorted(daily_summaries, key=lambda x: x.date)
        
        # Calculate weekly averages
        avg_wellbeing = sum(d.overall_wellbeing for d in daily_summaries) / len(daily_summaries)
        
        # Determine trend
        if len(daily_summaries) >= 2:
            start_avg = sum(d.overall_wellbeing for d in daily_summaries[:3]) / min(3, len(daily_summaries))
            end_avg = sum(d.overall_wellbeing for d in daily_summaries[-3:]) / min(3, len(daily_summaries))
            trend = "Improving" if end_avg > start_avg else "Worsening" if end_avg < start_avg else "Stable"
        else:
            trend = "Stable"
        
        return WeeklySummary(
            week_start_date=sorted_summaries[0].date,
            week_end_date=sorted_summaries[-1].date,
            daily_summaries=sorted_summaries,
            average_wellbeing=round(avg_wellbeing, 2),
            symptom_trend=trend,
            most_common_symptoms=[],  # TODO: Implement symptom frequency analysis
            weekly_notes="\n".join(filter(None, [d.notes for d in daily_summaries]))
        )