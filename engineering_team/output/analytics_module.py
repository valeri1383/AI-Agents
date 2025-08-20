import pandas as pd
import datetime
import plotly.express as px
import streamlit as st
import csv

class AppointmentAnalytics:
    def __init__(self, appointment_system):
        self.appointment_system = appointment_system

    def generate_appointment_reports(self):
        df = pd.DataFrame(self.appointment_system.appointments)
        report = df.groupby(['doctor_name', 'status']).size().reset_index(name='count')
        return report

    def create_patient_demographics(self):
        patients = self.appointment_system.patients
        age_groups = defaultdict(int)
        for patient in patients.values():
            # Example age categories
            age = 30  # Placeholder for real age calculation
            if age < 18:
                age_groups['Under 18'] += 1
            elif 18 <= age < 30:
                age_groups['18-29'] += 1
            elif 30 <= age < 50:
                age_groups['30-49'] += 1
            else:
                age_groups['50 and above'] += 1
        return age_groups

    def analyze_doctor_utilization(self):
        df = pd.DataFrame(self.appointment_system.appointments)
        utilization = df.groupby('doctor_name')['status'].value_counts().unstack(fill_value=0)
        return utilization

    def track_appointment_trends(self):
        df = pd.DataFrame(self.appointment_system.appointments)
        df['date'] = pd.to_datetime(df['date'])
        trend = df.groupby(df['date'].dt.to_period('M')).size()
        return trend

    def create_revenue_reports(self):
        # Placeholder for revenue calculation
        revenue = len(self.appointment_system.appointments) * 100  # Assuming $100 per appointment
        return f"Total Revenue: ${revenue}"

    def generate_operational_metrics(self):
        total_booked = len([appt for appt in self.appointment_system.appointments if appt['status'] == 'booked'])
        total_cancelled = len([appt for appt in self.appointment_system.appointments if appt['status'] == 'cancelled'])
        return {
            "Total Appointments": len(self.appointment_system.appointments),
            "Total Booked": total_booked,
            "Total Cancelled": total_cancelled,
        }

    def export_data_to_csv(self, filename):
        return self.appointment_system.export_appointments_to_csv(filename)

    def run_dashboard(self):
        st.title("Appointment Analytics Dashboard")
        
        st.subheader("Appointment Reports")
        appointment_reports = self.generate_appointment_reports()
        st.write(appointment_reports)

        st.subheader("Patient Demographics")
        demographics = self.create_patient_demographics()
        st.bar_chart(demographics)

        st.subheader("Doctor Utilization")
        utilization = self.analyze_doctor_utilization()
        st.line_chart(utilization)

        st.subheader("Appointment Trends")
        trends = self.track_appointment_trends()
        st.line_chart(trends)

        st.subheader("Revenue Reports")
        revenue = self.create_revenue_reports()
        st.write(revenue)

        st.subheader("Operational Metrics")
        metrics = self.generate_operational_metrics()
        st.write(metrics)

        if st.button('Export Appointments to CSV'):
            self.export_data_to_csv('appointments.csv')
            st.success("Data exported successfully.")

# Initialize system and analytics
appointment_system = AppointmentSystem()
analytics = AppointmentAnalytics(appointment_system)

# Run the dashboard
if __name__ == "__main__":
    analytics.run_dashboard()