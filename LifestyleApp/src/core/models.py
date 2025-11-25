from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import List

class MoodType(Enum):
    HAPPY = "happy"
    SAD = "sad"
    ANXIOUS = "anxious"
    NEUTRAL = "neutral"

@dataclass
class DailySymptomLog:
    date: datetime
    sleep_hours: float
    physical_comfort: int
    mental_fog: bool
    mood: MoodType
    overall_wellbeing: int
    activity_level: int
    medication_adherence: bool
    notes: str
    pain_symptoms: List[str] = field(default_factory=list)
    fatigue_symptoms: List[str] = field(default_factory=list)
    temperature_sensitivity: List[str] = field(default_factory=list)
    visual_symptoms: List[str] = field(default_factory=list)
    
    @property
    def sleep_color_code(self) -> str:
        if self.sleep_hours < 6:
            return "#ffcdd2"  # Light red
        elif self.sleep_hours < 7.5:
            return "#fff9c4"  # Light yellow
        return "#c8e6c9"  # Light green
    
    @property
    def physical_comfort_color(self) -> str:
        if self.physical_comfort <= 3:
            return "#ffcdd2"  # Light red
        elif self.physical_comfort <= 6:
            return "#fff9c4"  # Light yellow
        return "#c8e6c9"  # Light green
    
    @property
    def mood_color(self) -> str:
        colors = {
            MoodType.HAPPY: "#c8e6c9",    # Light green
            MoodType.SAD: "#ffcdd2",      # Light red
            MoodType.ANXIOUS: "#fff9c4",  # Light yellow
            MoodType.NEUTRAL: "#e0e0e0"   # Light gray
        }
        return colors[self.mood]
    
    @property
    def mental_fog_color(self) -> str:
        return "#ffcdd2" if self.mental_fog else "#c8e6c9"
    
    @property
    def average_pain_level(self) -> float:
        return len(self.pain_symptoms)
    
    @property
    def average_fatigue_level(self) -> float:
        return len(self.fatigue_symptoms)
    
    @property
    def total_symptoms_reported(self) -> int:
        return (len(self.pain_symptoms) +
                len(self.fatigue_symptoms) +
                len(self.temperature_sensitivity) +
                len(self.visual_symptoms))

@dataclass
class WeeklySummary:
    week_start_date: datetime
    week_end_date: datetime
    daily_summaries: List[DailySymptomLog]
    average_wellbeing: float
    symptom_trend: str
    most_common_symptoms: List[str]
    weekly_notes: str
    
    def calculate_trends(self) -> None:
        """Calculate trends based on daily summaries"""
        if len(self.daily_summaries) < 2:
            self.symptom_trend = "Insufficient data"
            return
        
        first_symptoms = self.daily_summaries[0].total_symptoms_reported
        last_symptoms = self.daily_summaries[-1].total_symptoms_reported
        
        if last_symptoms < first_symptoms:
            self.symptom_trend = "Improving"
        elif last_symptoms > first_symptoms:
            self.symptom_trend = "Worsening"
        else:
            self.symptom_trend = "Stable"
        
        # Calculate most common symptoms
        all_symptoms = []
        for log in self.daily_summaries:
            all_symptoms.extend(log.pain_symptoms)
            all_symptoms.extend(log.fatigue_symptoms)
            all_symptoms.extend(log.temperature_sensitivity)
            all_symptoms.extend(log.visual_symptoms)
            
        if all_symptoms:
            from collections import Counter
            symptom_counts = Counter(all_symptoms)
            self.most_common_symptoms = [symptom for symptom, _ in symptom_counts.most_common(5)]
    
    @property
    def average_sleep_hours(self) -> float:
        """Calculate average sleep hours from daily entries"""
        if not self.daily_summaries:
            return 0.0
        return sum(ds.sleep_hours for ds in self.daily_summaries) / len(self.daily_summaries)
    
    @property
    def average_physical_comfort(self) -> float:
        """Calculate average physical comfort from daily entries"""
        if not self.daily_summaries:
            return 0.0
        return sum(ds.physical_comfort for ds in self.daily_summaries) / len(self.daily_summaries)
    
    @property
    def average_activity_level(self) -> float:
        """Calculate average activity level from daily entries"""
        if not self.daily_summaries:
            return 0.0
        return sum(ds.activity_level for ds in self.daily_summaries) / len(self.daily_summaries)
    
    @property
    def average_pain_level(self) -> float:
        """Calculate average pain level from daily entries"""
        if not self.daily_summaries:
            return 0.0
        return sum(ds.average_pain_level for ds in self.daily_summaries) / len(self.daily_summaries)
    
    @property
    def average_fatigue_level(self) -> float:
        """Calculate average fatigue level from daily entries"""
        if not self.daily_summaries:
            return 0.0
        return sum(ds.average_fatigue_level for ds in self.daily_summaries) / len(self.daily_summaries)
    
    @property
    def medication_adherence_rate(self) -> float:
        """Calculate medication adherence rate from daily entries"""
        if not self.daily_summaries:
            return 0.0
        adherent_days = sum(1 for ds in self.daily_summaries if ds.medication_adherence)
        return (adherent_days / len(self.daily_summaries)) * 100
    
    @property
    def mental_fog_days(self) -> int:
        """Count days with mental fog from daily entries"""
        return sum(1 for ds in self.daily_summaries if ds.mental_fog)
    
    @property
    def mood_distribution(self) -> dict:
        """Calculate mood distribution from daily entries"""
        from collections import Counter
        mood_counts = Counter(ds.mood for ds in self.daily_summaries)
        return {mood.name: count for mood, count in mood_counts.items()}