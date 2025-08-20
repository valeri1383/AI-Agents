
FROM python:3.9
WORKDIR /app
COPY . /app
RUN pip install Flask flask_sqlalchemy Flask-Mail pandas
CMD ["python", "-u", "healthcare_app.py"]
