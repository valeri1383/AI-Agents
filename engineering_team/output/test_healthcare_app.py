import unittest
from healthcare_app import AppointmentSystem
from unittest.mock import patch, MagicMock
import datetime

class TestAppointmentSystem(unittest.TestCase):
    def setUp(self):
        self.app_system = AppointmentSystem()

    def test_register_patient_success(self):
        result = self.app_system.register_patient("John Doe", "john@example.com", "1234567890", "password123")
        self.assertEqual(result, "Registration successful")
        self.assertIn("john@example.com", self.app_system.patients)

    def test_register_patient_missing_fields(self):
        with self.assertRaises(ValueError) as context:
            self.app_system.register_patient("", "john@example.com", "1234567890", "password123")
        self.assertEqual(str(context.exception), "All fields are required")

    def test_register_patient_email_already_registered(self):
        self.app_system.register_patient("John Doe", "john@example.com", "1234567890", "password123")
        with self.assertRaises(ValueError) as context:
            self.app_system.register_patient("Jane Doe", "john@example.com", "0987654321", "password456")
        self.assertEqual(str(context.exception), "Email already registered")

    def test_login_patient_success(self):
        self.app_system.register_patient("John Doe", "john@example.com", "1234567890", "password123")
        result = self.app_system.login_patient("john@example.com", "password123")
        self.assertEqual(result, "Login successful")

    def test_login_patient_invalid_email(self):
        with self.assertRaises(ValueError) as context:
            self.app_system.login_patient("nonexistent@example.com", "password123")
        self.assertEqual(str(context.exception), "Invalid email or password")

    def test_login_patient_invalid_password(self):
        self.app_system.register_patient("John Doe", "john@example.com", "1234567890", "password123")
        with self.assertRaises(ValueError) as context:
            self.app_system.login_patient("john@example.com", "wrongpassword")
        self.assertEqual(str(context.exception), "Invalid email or password")

    def test_book_appointment_success(self):
        self.app_system.register_patient("John Doe", "john@example.com", "1234567890", "password123")
        result = self.app_system.book_appointment("john@example.com", "Dr. Smith", "2023-12-01", "09:00")
        self.assertEqual(result, "Appointment booked successfully")
        self.assertEqual(len(self.app_system.appointments), 1)

    def test_book_appointment_time_slot_invalid(self):
        self.app_system.register_patient("John Doe", "john@example.com", "1234567890", "password123")
        with self.assertRaises(ValueError) as context:
            self.app_system.book_appointment("john@example.com", "Dr. Smith", "2023-12-01", "10:00")
        self.assertEqual(str(context.exception), "Invalid time slot")

    def test_book_appointment_double_booking(self):
        self.app_system.register_patient("John Doe", "john@example.com", "1234567890", "password123")
        self.app_system.book_appointment("john@example.com", "Dr. Smith", "2023-12-01", "09:00")
        result = self.app_system.book_appointment("john@example.com", "Dr. Smith", "2023-12-01", "09:00")
        self.assertEqual(result, "Added to waiting list")
        self.assertEqual(len(self.app_system.waiting_list["Dr. Smith"]), 1)

    def test_view_appointments(self):
        self.app_system.register_patient("John Doe", "john@example.com", "1234567890", "password123")
        self.app_system.book_appointment("john@example.com", "Dr. Smith", "2023-12-01", "09:00")
        appointments = self.app_system.view_appointments("john@example.com")
        self.assertEqual(len(appointments), 1)

    def test_cancel_appointment_success(self):
        self.app_system.register_patient("John Doe", "john@example.com", "1234567890", "password123")
        self.app_system.book_appointment("john@example.com", "Dr. Smith", "2023-12-01", "09:00")
        appointment_id = self.app_system.appointments[0].get("id", 0)  # Using a dummy ID for testing
        result = self.app_system.cancel_appointment("john@example.com", appointment_id)
        self.assertEqual(result, "Appointment cancelled successfully")

    def test_cancel_appointment_not_found(self):
        self.app_system.register_patient("John Doe", "john@example.com", "1234567890", "password123")
        with self.assertRaises(ValueError) as context:
            self.app_system.cancel_appointment("john@example.com", 999)  # Non-existing ID
        self.assertEqual(str(context.exception), "Appointment not found or does not belong to patient")

    def test_validate_date_success(self):
        result = self.app_system.validate_date("2023-12-01")
        self.assertEqual(result, "2023-12-01")

    def test_validate_date_invalid_format(self):
        with self.assertRaises(ValueError) as context:
            self.app_system.validate_date("01-12-2023")
        self.assertEqual(str(context.exception), "Invalid date format. Use YYYY-MM-DD.")

    def test_validate_date_past_date(self):
        past_date = (datetime.datetime.now() - datetime.timedelta(days=1)).strftime("%Y-%m-%d")
        with self.assertRaises(ValueError) as context:
            self.app_system.validate_date(past_date)
        self.assertEqual(str(context.exception), "Cannot book appointment in the past")

    def test_export_appointments_to_csv_no_appointments(self):
        with self.assertRaises(ValueError) as context:
            self.app_system.export_appointments_to_csv("appointments.csv")
        self.assertEqual(str(context.exception), "No appointments to export")

    @patch("healthcare_app.smtplib.SMTP")
    def test_send_email_confirmation(self, mock_smtp):
        appointment = {
            "doctor_name": "Dr. Smith",
            "date": "2023-12-01",
            "time": "09:00"
        }
        self.app_system.send_email_confirmation("john@example.com", "Booking Confirmation", appointment)
        mock_smtp.assert_called_once()

if __name__ == '__main__':
    unittest.main()