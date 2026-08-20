# Student Performance Predictor

A machine-learning web application that analyzes academic habits and estimates a student's exam performance.

The project combines **Data Science and Education** to explore how factors such as study time, attendance, sleep, motivation, tutoring, physical activity, and extracurricular activities relate to academic performance.

## Features

- Predicts an estimated exam score from 0 to 100
- Analyzes student study habits and academic information
- Provides personalized academic insights
- Generates recommendations based on user inputs
- Displays the user's latest analysis on the home page
- Responsive web interface
- Machine-learning model trained on student performance data

## Machine Learning Model

The model uses several academic and lifestyle factors:

- Hours studied per week
- Attendance
- Sleep hours
- Previous academic score
- Motivation level
- Tutoring sessions
- Physical activity
- Extracurricular activities

**Target variable:** Exam Score

Current model evaluation:

- **MAE:** 1.38
- **R² Score:** 0.606
- **Dataset size:** 6,607 student records

## Dataset

The project uses the **Student Performance Factors** dataset.

The dataset contains information about academic habits, student characteristics, and exam performance.

## Technologies

- Python
- FastAPI
- scikit-learn
- pandas
- NumPy
- Jinja2
- HTML
- CSS
- Uvicorn

## Project Structure

student-performance-predictor/

- `main.py` — FastAPI application
- `train_model.py` — machine-learning training script
- `data/` — dataset
- `model/` — trained model
- `templates/` — HTML pages
- `static/` — CSS, images, and static assets
- `requirements.txt` — Python dependencies

## Running the Project Locally

Install the required dependencies:

```bash
pip install -r requirements.txt
