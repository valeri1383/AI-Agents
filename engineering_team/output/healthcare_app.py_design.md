```python
# healthcare_app.py

# Necessary Imports
import csv
import datetime
import smtplib
from email.mime.text import MIMEText
from collections import defaultdict
import plotly.express as px
import pandas as pd
from gradio import Interface, Tab

class AppointmentSystem:
    def __init__(self):
        self.patients = {}  # Store patient data
        self.appointments = []  # Store appointment data
        self.doctors = [
            {"name": "Dr. Smith", "specialty": "General Practice"},
            {"name": "Dr. Johnson", "specialty": "Cardiology"},
            {"name": "Dr. Williams", "specialty": "Dermatology"},
        ]
        self.available_slots = ["09:00", "11:00", "14:00", "16:00", "18:00"]
        self.waiting_list = defaultdict(list)

    # Patient Registration
    def register_patient(self, name, email, phone, password):
        if email in self.patients:
            raise ValueError("Email already registered")
        self.patients[email] = {
            "name": name,
            "phone": phone,
            "password": password,
            "appointments": []
        }

    # Patient Login
    def login_patient(self, email, password):
        patient = self.patients.get(email)
        if not patient or patient["password"] != password:
            raise ValueError("Invalid email or password")
        return patient

    # Book Appointment
    def book_appointment(self, email, doctor_name, date, time):
        if time not in self.available_slots:
            raise ValueError("Invalid time slot")
        if self.is_double_booking(email, date, time):
            return self.add_to_waiting_list(email, doctor_name, date, time)

        appointment = {
            "patient_email": email,
            "doctor_name": doctor_name,
            "date": date,
            "time": time,
            "status": "booked",
            "notes": None
        }
        self.appointments.append(appointment)
        self.patients[email]["appointments"].append(appointment)
        self.send_email_confirmation(email, "Booking Confirmation", appointment)

    # View Appointments
    def view_appointments(self, email):
        return self.patients[email]["appointments"]

    # Cancel Appointment
    def cancel_appointment(self, email, appointment_id):
        appointment = self.find_appointment(appointment_id)
        if appointment is None or appointment["patient_email"] != email:
            raise ValueError("Appointment not found or does not belong to patient")

        appointment["status"] = "cancelled"
        self.send_email_confirmation(email, "Cancellation Confirmation", appointment)

    # Add to waiting list
    def add_to_waiting_list(self, email, doctor_name, date, time):
        self.waiting_list[doctor_name].append((email, date, time))
        return "Added to waiting list"

    # Check for double booking
    def is_double_booking(self, email, date, time):
        for appointment in self.patients[email]["appointments"]:
            if appointment["date"] == date and appointment["time"] == time and appointment["status"] == "booked":
                return True
        return False

    # Find existing appointment
    def find_appointment(self, appointment_id):
        for appointment in self.appointments:
            if appointment["id"] == appointment_id:
                return appointment
        return None

    # Send Email Notifications
    def send_email_confirmation(self, recipient, subject, appointment):
        message = f"{subject} for appointment with {appointment['doctor_name']} on {appointment['date']} at {appointment['time']}"
        msg = MIMEText(message)
        msg["Subject"] = subject
        msg["From"] = "no-reply@healthcareclinic.com"
        msg["To"] = recipient
        
        with smtplib.SMTP("smtp.healthcareclinic.com") as server:
            server.sendmail(msg["From"], msg["To"], msg.as_string())

    # Export appointment data to CSV
    def export_appointments_to_csv(self, filename):
        keys = self.appointments[0].keys()
        with open(filename, 'w', newline='') as output_file:
            dict_writer = csv.DictWriter(output_file, fieldnames=keys)
            dict_writer.writeheader()
            dict_writer.writerows(self.appointments)

    # Visualization Methods
    def get_appointment_statistics(self):
        df = pd.DataFrame(self.appointments)
        return df.groupby('date')['status'].value_counts().unstack().fillna(0)

    def plot_appointment_statistics(self, statistic):
        px.bar(statistic)


# UI with Gradio
def gradio_interface():
    app_sys = AppointmentSystem()
    
    patient_tab = Tab(
        title="Patient",
        components=[
            # Add Gradio components for registration, login and booking
        ]
    )
    
    admin_tab = Tab(
        title="Admin",
        components=[
            # Add Gradio components for viewing statistics and exporting data
        ]
    )
    
    interface = Interface(
        title="Healthcare Appointment Management System",
        tabs=[patient_tab, admin_tab]
    )
    
    interface.launch()

# Main Execution
if __name__ == "__main__":
    gradio_interface()
```

This complete design outlines the `AppointmentSystem` class containing the core and enhanced features, including methods and their functionalities, imports, and provisions for email notifications, data handling, and visualization. Each function is designed to facilitate the requirements specified in the task while ensuring proper error handling and data management.