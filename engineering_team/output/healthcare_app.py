import csv
import datetime
import smtplib
from email.mime.text import MIMEText
from collections import defaultdict

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
        if not name or not email or not phone or not password:
            raise ValueError("All fields are required")
        if email in self.patients:
            raise ValueError("Email already registered")
        self.patients[email] = {
            "name": name,
            "phone": phone,
            "password": password,
            "appointments": []
        }
        return "Registration successful"

    # Patient Login
    def login_patient(self, email, password):
        patient = self.patients.get(email)
        if not patient or patient["password"] != password:
            raise ValueError("Invalid email or password")
        return "Login successful"

    # Book Appointment
    def book_appointment(self, email, doctor_name, date, time):
        if time not in self.available_slots:
            raise ValueError("Invalid time slot")
        if self.is_double_booking(email, date, time):
            return self.add_to_waiting_list(email, doctor_name, date, time)

        appointment = {
            "patient_email": email,
            "doctor_name": doctor_name,
            "date": self.validate_date(date),
            "time": time,
            "status": "booked"
        }
        self.appointments.append(appointment)
        self.patients[email]["appointments"].append(appointment)
        self.send_email_confirmation(email, "Booking Confirmation", appointment)
        return "Appointment booked successfully"

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
        return "Appointment cancelled successfully"

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

    # Validate date
    def validate_date(self, date_str):
        try:
            date = datetime.datetime.strptime(date_str, "%Y-%m-%d")
            if date < datetime.datetime.now():
                raise ValueError("Cannot book appointment in the past")
            return date.strftime("%Y-%m-%d")
        except ValueError as e:
            raise ValueError("Invalid date format. Use YYYY-MM-DD.")

    # Find existing appointment
    def find_appointment(self, appointment_id):
        for appointment in self.appointments:
            if appointment.get("id") == appointment_id:
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
        if not self.appointments:
            raise ValueError("No appointments to export")
        keys = self.appointments[0].keys()
        with open(filename, 'w', newline='') as output_file:
            dict_writer = csv.DictWriter(output_file, fieldnames=keys)
            dict_writer.writeheader()
            dict_writer.writerows(self.appointments)
        return f"Data exported to {filename} successfully."