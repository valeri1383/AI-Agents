import pandas as pd
import plotly.express as px
import datetime
from collections import defaultdict

class AppointmentVisualization:
    def __init__(self, appointment_system):
        self.appointment_system = appointment_system

    def create_appointment_charts(self):
        appointment_data = self.appointment_system.appointments
        df = pd.DataFrame(appointment_data)
        df['date'] = pd.to_datetime(df['date'])

        # Daily appointments
        daily_counts = df['date'].value_counts().reset_index()
        daily_counts.columns = ['Date', 'Count']
        fig = px.bar(daily_counts, x='Date', y='Count', title='Daily Appointments')
        fig.show()

    def generate_doctor_utilization_graphs(self):
        appointment_data = self.appointment_system.appointments
        df = pd.DataFrame(appointment_data)
        doctor_utilization = df['doctor_name'].value_counts().reset_index()
        doctor_utilization.columns = ['Doctor', 'Count']
        fig = px.pie(doctor_utilization, names='Doctor', values='Count', title='Doctor Utilization')
        fig.show()

    def plot_booking_patterns(self):
        appointment_data = self.appointment_system.appointments
        df = pd.DataFrame(appointment_data)
        df['time'] = pd.to_datetime(df['time'], format='%H:%M').dt.time
        time_counts = df['time'].value_counts().reset_index()
        time_counts.columns = ['Time', 'Count']
        fig = px.line(time_counts, x='Time', y='Count', title='Booking Patterns Over Time')
        fig.show()

    def create_patient_demographics(self):
        appointment_data = self.appointment_system.patients
        demographics = defaultdict(int)
        
        # Assuming we add some demographic data to appointments
        for patient in appointment_data.values():
            demographics[len(patient["appointments"])] += 1
        
        demographics_df = pd.DataFrame(list(demographics.items()), columns=['Appointment Frequency', 'Count'])
        fig = px.bar(demographics_df, x='Appointment Frequency', y='Count', title='Patient Demographics')
        fig.show()
    
    def generate_daily_reports(self):
        today = datetime.date.today()
        today_appointments = [appt for appt in self.appointment_system.appointments if appt['date'] == today.strftime("%Y-%m-%d")]
        report = {
            'total_appointments': len(today_appointments),
            'booked': sum(1 for appt in today_appointments if appt['status'] == 'booked'),
            'cancelled': sum(1 for appt in today_appointments if appt['status'] == 'cancelled'),
        }
        return report

    def create_interactive_dashboard(self):
        self.create_appointment_charts()
        self.generate_doctor_utilization_graphs()
        self.plot_booking_patterns()
        self.create_patient_demographics()
        report = self.generate_daily_reports()
        print("Daily Report:", report)

# Integrate with the existing AppointmentSystem
appointment_system = AppointmentSystem()
visualization = AppointmentVisualization(appointment_system)

# Example usage:
visualization.create_interactive_dashboard()