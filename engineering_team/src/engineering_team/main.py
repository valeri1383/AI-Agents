#!/usr/bin/env python
import sys
import warnings
import os
from datetime import datetime
from engineering_team.crew import EngineeringTeam

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

# Create output directory if it doesn't exist
os.makedirs('output', exist_ok=True)

# BALANCED requirements - similar structure to trading example but for healthcare
requirements = """
An advanced healthcare appointment management system for a medical clinic with data insights.

CORE FUNCTIONALITY:
- Patient registration with name, email, phone, and password
- Patient login with email/password authentication
- Book appointments from available time slots (9:00 AM, 11:00 AM, 2:00 PM, 4:00 PM, 6:00 PM)
- Support for 3 doctors with different specialties (Dr. Smith - General Practice, Dr. Johnson - Cardiology, Dr. Williams - Dermatology)
- View current and historical appointments with doctor information
- Cancel appointments with confirmation
- Prevent double-booking and past-date appointments
- Patient appointment history with visit notes

ENHANCED FEATURES:
- Appointment reminder system (email notifications)
- Basic patient medical notes and visit summaries
- Waiting list for fully booked slots
- Appointment statistics and visualizations
- Simple admin dashboard with charts and metrics
- Export appointment data to CSV format
- Email confirmations for bookings and cancellations

VISUALIZATION REQUIREMENTS:
- Daily/weekly/monthly appointment charts
- Doctor utilization graphs
- Patient booking patterns over time
- Appointment status distribution (booked, cancelled, completed)
- Peak booking hours visualization
- Patient demographics charts (age groups, appointment frequency)

TECHNICAL REQUIREMENTS:
- Clean Gradio interface with separate tabs for patients and admin
- Interactive charts using plotly or similar
- Automated email system for notifications
- Simple data export functionality
- Session management for user login states
"""

module_name = "healthcare_app.py"
class_name = "AppointmentSystem"

def run():
    """
    Run the healthcare appointment crew.
    """
    inputs = {
        'requirements': requirements,
        'module_name': module_name,
        'class_name': class_name,
        'project_type': 'Healthcare Appointment System'
    }

    # Create and run the crew
    result = EngineeringTeam().crew().kickoff(inputs=inputs)

if __name__ == "__main__":
    run()