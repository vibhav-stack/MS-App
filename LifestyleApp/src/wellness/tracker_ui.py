import os
import sys
import logging
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

# Add the parent directory to Python path
parent_dir = str(Path(__file__).resolve().parent.parent)
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

import streamlit as st
import plotly.graph_objects as go
from datetime import datetime, timedelta
from core.database import SymptomDatabase
from core.models import WeeklySummary, MoodType, DailySymptomLog

class WellnessUI:
    def __init__(self):
        self.db = SymptomDatabase()
        # Initialize session state for storing weekly data
        if 'weekly_data' not in st.session_state:
            st.session_state.weekly_data = None
        if 'force_refresh' not in st.session_state:
            st.session_state.force_refresh = False
        
    def render_daily_summary(self, summary):
        """Render the daily summary tab"""
        if not summary:
            st.warning("No data available for this date")
            if st.button("Add Entry for Today"):
                self._show_add_entry_form()
            return
            
        # Create three columns for main metrics
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown(
                f"""
                <div style='padding: 20px; border-radius: 10px; background-color: {summary.sleep_color_code}'>
                    <h3>Sleep</h3>
                    <p>{summary.sleep_hours} hours</p>
                </div>
                """,
                unsafe_allow_html=True
            )
        
        with col2:
            st.markdown(
                f"""
                <div style='padding: 20px; border-radius: 10px; background-color: {summary.physical_comfort_color}'>
                    <h3>Physical Comfort</h3>
                    <p>{summary.physical_comfort}/10</p>
                </div>
                """,
                unsafe_allow_html=True
            )
            
        with col3:
            st.markdown(
                f"""
                <div style='padding: 20px; border-radius: 10px; background-color: {summary.mood_color}'>
                    <h3>Mood</h3>
                    <p>{summary.mood.capitalize()}</p>
                </div>
                """,
                unsafe_allow_html=True
            )
            
        # Mental fog indicator
        st.markdown(
            f"""
            <div style='padding: 20px; border-radius: 10px; background-color: {summary.mental_fog_color}'>
                <h3>Mental Fog</h3>
                <p>{"Present" if summary.mental_fog else "None"}</p>
            </div>
            """,
            unsafe_allow_html=True
        )
        
        # Additional metrics
        st.subheader("Daily Statistics")
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Overall Wellbeing", f"{summary.overall_wellbeing}/10")
        col2.metric("Pain Level", f"{summary.average_pain_level:.1f}/10")
        col3.metric("Fatigue", f"{summary.average_fatigue_level:.1f}/10")
        col4.metric("Total Symptoms", str(summary.total_symptoms_reported))
        
        # Activity and medication
        st.subheader("Lifestyle Factors")
        col1, col2 = st.columns(2)
        col1.metric("Activity Level", f"{summary.activity_level}/5")
        col2.metric("Medication", "✓" if summary.medication_adherence else "✗")
        
        if summary.notes:
            st.text_area("Notes", summary.notes, disabled=True)
            
        # Edit button
        if st.button("Edit Entry"):
            self._show_edit_form(summary)
            
    def render_weekly_summary(self, start_date):
        """Render the weekly summary tab"""
        # Always ensure we have fresh data for weekly summary
        if isinstance(start_date, datetime):
            start_date = start_date.replace(hour=0, minute=0, second=0, microsecond=0)
        end_date = (start_date + timedelta(days=6)).replace(hour=23, minute=59, second=59)
        
        # Always fetch fresh data for weekly view (no caching)
        daily_summaries = self.db.get_weekly_logs(start_date, end_date)
        
        if not daily_summaries:
            st.warning("No data available for this week")
            if st.button("Add Entry for This Week"):
                self._show_add_entry_form()
            return
        
        # Create weekly summary with calculated averages from daily entries
        weekly_summary = WeeklySummary(
            week_start_date=start_date,
            week_end_date=end_date,
            daily_summaries=daily_summaries,
            average_wellbeing=sum(ds.overall_wellbeing for ds in daily_summaries) / len(daily_summaries) if daily_summaries else 0.0,
            symptom_trend="",  # Will be calculated
            most_common_symptoms=[],
            weekly_notes="\n".join(filter(None, [ds.notes for ds in daily_summaries]))
        )
        weekly_summary.calculate_trends()
        
        # Display week header
        st.subheader(f"Week of {start_date.strftime('%B %d, %Y')} to {end_date.strftime('%B %d, %Y')}")
        st.write(f"**{len(daily_summaries)}** day(s) with entries")
        
        # Display weekly overview metrics - all calculated from daily entries
        st.subheader("Weekly Overview")
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Average Wellbeing", f"{weekly_summary.average_wellbeing:.1f}/10")
        with col2:
            st.metric("Average Sleep", f"{weekly_summary.average_sleep_hours:.1f} hrs")
        with col3:
            st.metric("Physical Comfort", f"{weekly_summary.average_physical_comfort:.1f}/10")
        with col4:
            st.metric("Trend", weekly_summary.symptom_trend)
        
        # Additional metrics row
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Average Pain", f"{weekly_summary.average_pain_level:.1f}/10")
        with col2:
            st.metric("Average Fatigue", f"{weekly_summary.average_fatigue_level:.1f}/10")
        with col3:
            st.metric("Activity Level", f"{weekly_summary.average_activity_level:.1f}/5")
        with col4:
            st.metric("Medication Adherence", f"{weekly_summary.medication_adherence_rate:.0f}%")
        
        # Mental fog and mood distribution
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Days with Mental Fog", f"{weekly_summary.mental_fog_days}/{len(daily_summaries)}")
        with col2:
            mood_dist = weekly_summary.mood_distribution
            if mood_dist:
                mood_display = ", ".join([f"{mood}: {count}" for mood, count in mood_dist.items()])
                st.write(f"**Mood Distribution:** {mood_display}")
            
        # Create trend visualizations
        st.subheader("Weekly Trends")
        self._plot_weekly_trends(daily_summaries)
        
        # Most common symptoms
        if weekly_summary.most_common_symptoms:
            st.subheader("Most Common Symptoms")
            for symptom in weekly_summary.most_common_symptoms:
                st.write(f"• {symptom}")
        else:
            st.info("No symptoms reported this week")
                
        # Weekly notes
        if weekly_summary.weekly_notes:
            st.subheader("Weekly Notes")
            st.text_area("", weekly_summary.weekly_notes, disabled=True, key="weekly_notes_display")
    
    def _show_add_entry_form(self):
        """Show form to add a new entry"""
        with st.form("new_entry"):
            st.subheader("Add New Entry")
            
            sleep_hours = st.slider("Sleep Hours", 0.0, 24.0, 8.0, 0.5)
            physical_comfort = st.slider("Physical Comfort", 1, 10, 5)
            mental_fog = st.checkbox("Mental Fog")
            mood = st.selectbox("Mood", ["HAPPY", "SAD", "ANXIOUS", "NEUTRAL"])
            overall_wellbeing = st.slider("Overall Wellbeing", 0, 10, 5)
            activity_level = st.slider("Activity Level", 1, 5, 3)
            medication_adherence = st.checkbox("Medication Taken", value=True)
            notes = st.text_area("Notes")
            
            if st.form_submit_button("Save Entry"):
                self._save_new_entry(
                    sleep_hours, physical_comfort, mental_fog, 
                    mood, overall_wellbeing, activity_level, 
                    medication_adherence, notes
                )
    
    def _show_edit_form(self, summary):
        """Show form to edit an existing entry"""
        with st.form("edit_entry"):
            st.subheader("Edit Entry")
            
            sleep_hours = st.slider("Sleep Hours", 0.0, 24.0, float(summary.sleep_hours), 0.5)
            physical_comfort = st.slider("Physical Comfort", 1, 10, summary.physical_comfort)
            mental_fog = st.checkbox("Mental Fog", summary.mental_fog)
            mood = st.selectbox("Mood", ["HAPPY", "SAD", "ANXIOUS", "NEUTRAL"], 
                              index=["HAPPY", "SAD", "ANXIOUS", "NEUTRAL"].index(summary.mood.upper()))
            overall_wellbeing = st.slider("Overall Wellbeing", 0, 10, summary.overall_wellbeing)
            activity_level = st.slider("Activity Level", 1, 5, summary.activity_level)
            medication_adherence = st.checkbox("Medication Taken", summary.medication_adherence)
            notes = st.text_area("Notes", summary.notes or "")
            
            if st.form_submit_button("Update Entry"):
                self._update_entry(
                    summary.date, sleep_hours, physical_comfort, mental_fog,
                    mood, overall_wellbeing, activity_level,
                    medication_adherence, notes
                )
            
    def _plot_weekly_trends(self, daily_summaries):
        """Create trend visualizations"""
        dates = [ds.date.strftime("%Y-%m-%d") for ds in daily_summaries]
        
        # Wellbeing trend
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=dates,
            y=[ds.overall_wellbeing for ds in daily_summaries],
            name="Overall Wellbeing",
            line=dict(color="#2E8B57", width=2)
        ))
        fig.update_layout(
            title="Weekly Wellbeing Trend",
            xaxis_title="Date",
            yaxis_title="Score",
            yaxis_range=[0, 10]
        )
        st.plotly_chart(fig)
        
        # Sleep hours
        fig_sleep = go.Figure()
        sleep_hours = [ds.sleep_hours for ds in daily_summaries]
        fig_sleep.add_trace(go.Bar(
            x=dates,
            y=sleep_hours,
            name="Sleep Hours",
            marker_color=[
                "red" if h < 6 else "yellow" if h < 7.5 else "green"
                for h in sleep_hours
            ]
        ))
        fig_sleep.update_layout(
            title="Sleep Pattern",
            xaxis_title="Date",
            yaxis_title="Hours",
            yaxis_range=[0, 12]
        )
        st.plotly_chart(fig_sleep)
        
        # Symptoms comparison
        fig_symptoms = go.Figure()
        fig_symptoms.add_trace(go.Scatter(
            x=dates,
            y=[ds.average_pain_level for ds in daily_summaries],
            name="Pain",
            line=dict(color="red", width=2)
        ))
        fig_symptoms.add_trace(go.Scatter(
            x=dates,
            y=[ds.average_fatigue_level for ds in daily_summaries],
            name="Fatigue",
            line=dict(color="orange", width=2)
        ))
        fig_symptoms.update_layout(
            title="Symptoms Trends",
            xaxis_title="Date",
            yaxis_title="Severity",
            yaxis_range=[0, 10]
        )
        st.plotly_chart(fig_symptoms)
    
    def _save_new_entry(self, sleep_hours, physical_comfort, mental_fog,
                       mood, overall_wellbeing, activity_level,
                       medication_adherence, notes):
        """Save a new entry to the database"""
        logger.info("========== Starting New Entry Submission ==========")
        
        st.markdown("---")
        st.subheader("🔄 Form Submission Debug Log")
        
        # Log session state details
        logger.info("Checking session state...")
        st.write("📋 Session State Information:")
        selected_date = st.session_state.get('selected_date', datetime.now().date())
        session_info = f"""
Current Date: {datetime.now().date()}
Selected Date: {selected_date}
Session State Keys: {list(st.session_state.keys())}
Force Refresh: {st.session_state.get('force_refresh', False)}
Weekly Data Cache: {'Present' if st.session_state.get('weekly_data') is not None else 'None'}
        """
        st.code(session_info)
        logger.info("Session State Info:\n%s", session_info)
        
        # Log datetime creation
        logger.info("Processing datetime...")
        entry_datetime = datetime.combine(selected_date, datetime.min.time())
        st.write("⏰ DateTime Processing:")
        datetime_info = f"""
Input Date: {selected_date}
Created DateTime: {entry_datetime.isoformat()}
Date Only: {entry_datetime.date()}
Time Component: {entry_datetime.time()}
        """
        st.code(datetime_info)
        logger.info("DateTime Processing:\n%s", datetime_info)
        
        # Create and log DailySymptomLog object
        logger.info("Creating DailySymptomLog object...")
        st.write("📝 Creating Log Object:")
        log = DailySymptomLog(
            date=entry_datetime,
            sleep_hours=sleep_hours,
            physical_comfort=physical_comfort,
            mental_fog=mental_fog,
            mood=getattr(MoodType, mood),
            overall_wellbeing=overall_wellbeing,
            activity_level=activity_level,
            medication_adherence=medication_adherence,
            notes=notes,
            pain_symptoms=[],
            fatigue_symptoms=[],
            temperature_sensitivity=[],
            visual_symptoms=[]
        )
        
        # Log detailed object state
        log_details = f"""
Log Object Details:
- Date: {log.date.isoformat()}
- Sleep Hours: {log.sleep_hours}
- Physical Comfort: {log.physical_comfort}
- Mental Fog: {log.mental_fog}
- Mood: {log.mood.name}
- Overall Wellbeing: {log.overall_wellbeing}
- Activity Level: {log.activity_level}
- Medication Adherence: {log.medication_adherence}
- Notes Length: {len(notes) if notes else 0} characters
        """
        st.code(log_details)
        logger.info("Created log object:\n%s", log_details)
        
        try:
            logger.info("Starting database operation...")
            st.write("💾 Database Operation:")
            st.info("Attempting to save to database...")
            self.db.add_daily_log(log)
            logger.info("Database save completed successfully")
            st.success("✅ Entry saved successfully!")
            
            # Verify save by trying to read it back
            logger.info("Verifying database save...")
            st.write("🔍 Verifying Save:")
            verification_log = self.db.get_daily_log(log.date)
            if verification_log:
                verify_msg = f"Entry verified in database for date: {verification_log.date.strftime('%Y-%m-%d')}"
                logger.info(verify_msg)
                st.success(f"✅ {verify_msg}")
                verify_details = f"""
Verified Data:
- Sleep Hours: {verification_log.sleep_hours}
- Mood: {verification_log.mood.name}
- Wellbeing: {verification_log.overall_wellbeing}
                """
                st.code(verify_details)
                logger.info("Verified data:\n%s", verify_details)
            else:
                logger.error("Failed to verify entry in database!")
                st.error("❌ Entry not found in verification check!")
            
            # Force immediate data refresh
            logger.info("Managing cache and state...")
            st.write("🔄 Cache Management:")
            st.session_state.weekly_data = None
            st.session_state.force_refresh = True
            
            # Update the selected date to ensure proper view refresh
            if 'selected_date' in st.session_state:
                logger.info("Updating weekly view...")
                week_start = st.session_state.selected_date - timedelta(days=st.session_state.selected_date.weekday())
                st.write("📅 View Refresh:")
                week_info = f"""
Week Start Date: {week_start}
Selected Date: {st.session_state.selected_date}
Days from Week Start: {st.session_state.selected_date.weekday()}
                """
                st.code(week_info)
                logger.info("Week calculation:\n%s", week_info)
                self.render_weekly_summary(datetime.combine(week_start, datetime.min.time()))
            
            st.write("🔄 Final Steps:")
            final_steps = """
1. Cache cleared
2. Force refresh enabled
3. Weekly view updated
4. Triggering app rerun...
            """
            st.code(final_steps)
            logger.info("Final steps:\n%s", final_steps)
            logger.info("Triggering streamlit rerun...")
            # Rerun the app to refresh the view
            st.rerun()
        except Exception as e:
            error_msg = f"Error occurred: {str(e)}"
            logger.error(error_msg)
            logger.error("Full traceback:", exc_info=True)
            st.error("❌ Error occurred!")
            st.error(f"Error details: {str(e)}")
            import traceback
            st.code(traceback.format_exc())
    
    def _update_entry(self, date, sleep_hours, physical_comfort, mental_fog,
                     mood, overall_wellbeing, activity_level,
                     medication_adherence, notes):
        """Update an existing entry in the database"""
        log = self.db.get_daily_log(date)
        if log:
            log.sleep_hours = sleep_hours
            log.physical_comfort = physical_comfort
            log.mental_fog = mental_fog
            log.mood = getattr(MoodType, mood)
            log.overall_wellbeing = overall_wellbeing
            log.activity_level = activity_level
            log.medication_adherence = medication_adherence
            log.notes = notes
            
            self.db.update_daily_log(date, log)
            st.success("Entry updated successfully!")
            # Force refresh of weekly data
            st.session_state.force_refresh = True
            # Clear weekly data cache
            st.session_state.weekly_data = None
            st.rerun()
        else:
            st.error("Failed to update entry")

def main():
    st.set_page_config(
        page_title="MS Wellness Tracker",
        page_icon="🏥",
        layout="wide"
    )
    
    st.title("MS Wellness Tracker")
    
    # Initialize session state
    if 'weekly_data' not in st.session_state:
        st.session_state.weekly_data = None
    if 'force_refresh' not in st.session_state:
        st.session_state.force_refresh = False
    if 'selected_date' not in st.session_state:
        st.session_state.selected_date = datetime.now().date()
    if 'last_update' not in st.session_state:
        st.session_state.last_update = datetime.now()
    
    # Clear cache if date changes
    current_date = datetime.now().date()
    if current_date != getattr(st.session_state, 'current_date', None):
        st.session_state.current_date = current_date
        st.session_state.weekly_data = None
        st.session_state.force_refresh = True
        
    ui = WellnessUI()
    
    # Date selection
    selected_date = st.date_input(
        "Select Date",
        value=datetime.now().date(),
        key='selected_date'  # This will store the date in session state
    )
    
    # Create tabs
    daily_tab, weekly_tab = st.tabs(["Daily Summary", "Weekly Summary"])
    
    # Handle daily tab
    with daily_tab:
        daily_summary = ui.db.get_daily_summary(datetime.combine(selected_date, datetime.min.time()))
        ui.render_daily_summary(daily_summary)
    
    # Handle weekly tab
    with weekly_tab:
        # Calculate week start (Monday) and end (Sunday)
        week_start = selected_date - timedelta(days=selected_date.weekday())
        ui.render_weekly_summary(datetime.combine(week_start, datetime.min.time()))

if __name__ == "__main__":
    main()