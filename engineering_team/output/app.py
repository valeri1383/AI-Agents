import gradio as gr
import plotly.express as px
import pandas as pd
from healthcare_app import AppointmentSystem

# Initialize backend system
appointment_system = AppointmentSystem()

# Wrapper functions to handle interactions with the backend
def register_patient(name, email, phone, password):
    try:
        result = appointment_system.register_patient(name, email, phone, password)
        return result
    except ValueError as e:
        return str(e)

def login_patient(email, password):
    try:
        result = appointment_system.login_patient(email, password)
        return result
    except ValueError as e:
        return str(e)

def book_appointment(email, doctor, date, time):
    try:
        result = appointment_system.book_appointment(email, doctor, date, time)
        return result
    except ValueError as e:
        return str(e)

def view_appointments(email):
    try:
        appointments = appointment_system.view_appointments(email)
        appointment_strings = [f"{app['date']} {app['time']} with {app['doctor_name']}: {app['status']}" for app in appointments]
        return "\n".join(appointment_strings)
    except ValueError as e:
        return str(e)

def cancel_appointment(email, appointment_id):
    try:
        result = appointment_system.cancel_appointment(email, appointment_id)
        return result
    except ValueError as e:
        return str(e)

def analytics_dashboard():
    try:
        appointments_df = pd.DataFrame(appointment_system.appointments)
        
        if appointments_df.empty:
            return "No appointment data available."

        total_patients = len(appointment_system.patients)
        total_appointments = len(appointment_system.appointments)
        
        # Create charts
        figs = []
        figs.append(px.histogram(appointments_df, x='date', title='Appointments Over Time'))
        figs.append(px.pie(appointments_df, names='doctor_name', title='Doctor Utilization'))
        
        agg_data = appointments_df['status'].value_counts().reset_index()
        figs.append(px.bar(agg_data, x='index', y='status', title='Appointment Status Distribution'))

        markdown_text = f"**Total Patients**: {total_patients}\n\n**Total Appointments**: {total_appointments}\n\n"
        return markdown_text, figs
    except Exception as e:
        return str(e), []

def export_data():
    try:
        filename = "appointments.csv"
        result = appointment_system.export_appointments_to_csv(filename)
        return result
    except ValueError as e:
        return str(e)

# Gradio interface
with gr.Blocks() as demo:
    with gr.Tab("Patient Registration"):
        name_input = gr.Textbox(label="Name")
        email_input = gr.Textbox(label="Email")
        phone_input = gr.Textbox(label="Phone")
        password_input = gr.Textbox(label="Password", type="password")
        register_button = gr.Button("Register")
        register_output = gr.Markdown()
        register_button.click(fn=register_patient, inputs=[name_input, email_input, phone_input, password_input], outputs=register_output)

    with gr.Tab("Patient Login"):
        login_email_input = gr.Textbox(label="Email")
        login_password_input = gr.Textbox(label="Password", type="password")
        login_button = gr.Button("Login")
        login_output = gr.Markdown()
        login_button.click(fn=login_patient, inputs=[login_email_input, login_password_input], outputs=login_output)

    with gr.Tab("Book Appointment"):
        email_for_booking = gr.Textbox(label="Email")
        doctor_dropdown = gr.Dropdown(["Dr. Smith", "Dr. Johnson", "Dr. Williams"], label="Doctor")
        date_input = gr.Textbox(label="Date", placeholder="YYYY-MM-DD")
        time_dropdown = gr.Dropdown(["09:00", "11:00", "14:00", "16:00", "18:00"], label="Time")
        book_button = gr.Button("Book Appointment")
        book_output = gr.Markdown()
        book_button.click(fn=book_appointment, inputs=[email_for_booking, doctor_dropdown, date_input, time_dropdown], outputs=book_output)

    with gr.Tab("View Appointments"):
        view_email_input = gr.Textbox(label="Email")
        view_button = gr.Button("View Appointments")
        view_output = gr.Markdown()
        view_button.click(fn=view_appointments, inputs=view_email_input, outputs=view_output)

    with gr.Tab("Cancel Appointment"):
        cancel_email_input = gr.Textbox(label="Email")
        appointment_id_input = gr.Number(label="Appointment ID")
        cancel_button = gr.Button("Cancel Appointment")
        cancel_output = gr.Markdown()
        cancel_button.click(fn=cancel_appointment, inputs=[cancel_email_input, appointment_id_input], outputs=cancel_output)

    with gr.Tab("Analytics Dashboard"):
        analytics_button = gr.Button("Show Dashboard")
        analytics_output = gr.Markdown()
        charts_output = gr.Plot()
        analytics_button.click(fn=analytics_dashboard, outputs=[analytics_output, charts_output])
        
        export_button = gr.Button("Export Appointment Data")
        export_output = gr.Markdown()
        export_button.click(fn=export_data, outputs=export_output)

demo.launch()