from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, Response
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware

import pandas as pd
import joblib


# =========================
# APP SETUP
# =========================

app = FastAPI()

app.add_middleware(
    SessionMiddleware,
    secret_key="student-performance-secret-key"
)

templates = Jinja2Templates(directory="templates")

app.mount(
    "/static",
    StaticFiles(directory="static"),
    name="static"
)


# =========================
# LOAD MODEL
# =========================

model = joblib.load("model/student_model.pkl")


# =========================
# HOME
# =========================

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):

    last_analysis = request.session.get("last_analysis")

    return templates.TemplateResponse(
        request=request,
        name="home.html",
        context={
            "last_analysis": last_analysis
        }
    )


# =========================
# PREDICTOR PAGE
# =========================

@app.get("/predict", response_class=HTMLResponse)
async def predictor(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="predict.html",
        context={}
    )


# =========================
# MAKE PREDICTION
# =========================

@app.post("/predict", response_class=HTMLResponse)
async def make_prediction(
    request: Request,

    # Academic routine
    hours_studied: float = Form(...),
    classes_per_week: int = Form(...),
    classes_attended: int = Form(...),
    previous_scores: float = Form(...),

    # Learning environment
    parental_involvement: str = Form(...),
    access_to_resources: str = Form(...),
    motivation_level: str = Form(...),
    internet_access: str = Form(...),
    tutoring_sessions: int = Form(...),
    teacher_quality: str = Form(...),
    peer_influence: str = Form(...),

    # Lifestyle
    sleep_hours: float = Form(...),
    physical_activity: int = Form(...),
    extracurricular_activities: str = Form(...),

    # Logistics
    distance_from_home: str = Form(...)
):

    # =========================
    # ATTENDANCE
    # =========================

    if classes_per_week <= 0:
        attendance = 0
    else:
        attendance = (classes_attended / classes_per_week) * 100

    attendance = round(min(attendance, 100), 1)


    # =========================
    # MODEL INPUT
    # =========================

    data = pd.DataFrame({
        "Hours_Studied": [hours_studied],
        "Attendance": [attendance],
        "Parental_Involvement": [parental_involvement],
        "Access_to_Resources": [access_to_resources],
        "Extracurricular_Activities": [extracurricular_activities],
        "Sleep_Hours": [sleep_hours],
        "Previous_Scores": [previous_scores],
        "Motivation_Level": [motivation_level],
        "Internet_Access": [internet_access],
        "Tutoring_Sessions": [tutoring_sessions],
        "Teacher_Quality": [teacher_quality],
        "Peer_Influence": [peer_influence],
        "Physical_Activity": [physical_activity],
        "Distance_from_Home": [distance_from_home]
    })


    # =========================
    # PREDICTION
    # =========================

    prediction = model.predict(data)[0]
    prediction = round(float(prediction), 1)


    # =========================
    # PERFORMANCE LEVEL
    # =========================

    if prediction >= 80:
        performance_level = "Excellent"

    elif prediction >= 70:
        performance_level = "Very Good"

    elif prediction >= 60:
        performance_level = "Developing"

    else:
        performance_level = "Needs Improvement"


    # =========================
    # INSIGHTS
    # =========================

    insights = []

    if attendance >= 90:
        insights.append(
            "Your attendance is very strong."
        )

    elif attendance < 75:
        insights.append(
            "Your attendance may be limiting your academic performance."
        )


    if hours_studied >= 20:
        insights.append(
            "You maintain a strong weekly study commitment."
        )

    elif hours_studied < 10:
        insights.append(
            "Your weekly independent study time is relatively low."
        )


    if sleep_hours >= 7:
        insights.append(
            "Your reported sleep duration supports a consistent academic routine."
        )

    elif sleep_hours < 6:
        insights.append(
            "Your reported sleep duration is relatively low."
        )


    if previous_scores >= 80:
        insights.append(
            "Your previous academic performance is strong."
        )


    if motivation_level == "High":
        insights.append(
            "You report a high level of academic motivation."
        )


    if access_to_resources == "Low":
        insights.append(
            "Limited access to learning resources may make studying more difficult."
        )


    if teacher_quality == "High":
        insights.append(
            "You report a strong teaching environment."
        )


    if peer_influence == "Positive":
        insights.append(
            "Your peer environment appears supportive of your studies."
        )


    # =========================
    # RECOMMENDATIONS
    # =========================

    recommendations = []

    if attendance < 90:
        recommendations.append(
            "Try to improve attendance and catch up quickly on missed classes."
        )

    if hours_studied < 20:
        recommendations.append(
            "Consider building a more consistent weekly independent study routine."
        )

    if sleep_hours < 7:
        recommendations.append(
            "Try to maintain a more consistent sleep schedule."
        )

    if tutoring_sessions == 0:
        recommendations.append(
            "Consider tutoring or academic support for difficult topics."
        )

    if physical_activity < 2:
        recommendations.append(
            "Consider adding regular physical activity to your weekly routine."
        )

    if motivation_level == "Low":
        recommendations.append(
            "Break larger academic goals into smaller weekly targets."
        )

    if access_to_resources == "Low":
        recommendations.append(
            "Look for additional learning resources through your school or online."
        )

    if internet_access == "No":
        recommendations.append(
            "Use offline study materials or school resources when internet access is limited."
        )

    if peer_influence == "Negative":
        recommendations.append(
            "Try to protect focused study time from negative peer pressure."
        )

    if not recommendations:
        recommendations.append(
            "Maintain your current routine and continue monitoring your progress."
        )


    # =========================
    # SAVE FOR HOME PAGE
    # =========================

    request.session["last_analysis"] = {
        "prediction": prediction,
        "performance_level": performance_level,
        "hours_studied": hours_studied,
        "attendance": attendance,
        "sleep_hours": sleep_hours,
        "motivation_level": motivation_level
    }


    # =========================
    # RESULT PAGE
    # =========================

    return templates.TemplateResponse(
        request=request,
        name="result.html",
        context={
            "prediction": prediction,
            "performance_level": performance_level,

            "hours_studied": hours_studied,
            "classes_per_week": classes_per_week,
            "classes_attended": classes_attended,
            "attendance": attendance,
            "previous_scores": previous_scores,

            "parental_involvement": parental_involvement,
            "access_to_resources": access_to_resources,
            "motivation_level": motivation_level,
            "internet_access": internet_access,
            "tutoring_sessions": tutoring_sessions,
            "teacher_quality": teacher_quality,
            "peer_influence": peer_influence,

            "sleep_hours": sleep_hours,
            "physical_activity": physical_activity,
            "extracurricular_activities": extracurricular_activities,
            "distance_from_home": distance_from_home,

            "insights": insights,
            "recommendations": recommendations
        }
    )


# =========================
# HOW IT WORKS
# =========================

@app.get("/how-it-works", response_class=HTMLResponse)
async def how_it_works(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="how_it_works.html",
        context={}
    )


# =========================
# IMPROVE
# =========================

@app.get("/improve", response_class=HTMLResponse)
async def improve(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="improve.html",
        context={}
    )


# =========================
# ABOUT
# =========================

@app.get("/about", response_class=HTMLResponse)
async def about(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="about.html",
        context={}
    )


# =========================
# SITEMAP
# =========================

@app.get("/sitemap.xml")
async def sitemap():

    content = """<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">

    <url>
        <loc>https://student-performance-predictor-bas2.onrender.com/</loc>
    </url>

    <url>
        <loc>https://student-performance-predictor-bas2.onrender.com/predict</loc>
    </url>

    <url>
        <loc>https://student-performance-predictor-bas2.onrender.com/how-it-works</loc>
    </url>

    <url>
        <loc>https://student-performance-predictor-bas2.onrender.com/improve</loc>
    </url>

    <url>
        <loc>https://student-performance-predictor-bas2.onrender.com/about</loc>
    </url>

</urlset>"""

    return Response(
        content=content,
        media_type="application/xml"
    )


# =========================
# ROBOTS
# =========================

@app.get("/robots.txt")
async def robots():

    content = """User-agent: *
Allow: /

Sitemap: https://student-performance-predictor-bas2.onrender.com/sitemap.xml
"""

    return Response(
        content=content,
        media_type="text/plain"
    )

