from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
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
# LOAD ML MODEL
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

    hours_studied: float = Form(...),
    attendance: float = Form(...),
    sleep_hours: float = Form(...),
    previous_scores: float = Form(...),

    motivation_level: str = Form(...),

    tutoring_sessions: int = Form(...),
    physical_activity: int = Form(...),

    extracurricular_activities: str = Form(...)
):

    # Create dataframe in exactly the same
    # format used during model training

    data = pd.DataFrame({
        "Hours_Studied": [hours_studied],
        "Attendance": [attendance],
        "Sleep_Hours": [sleep_hours],
        "Previous_Scores": [previous_scores],
        "Motivation_Level": [motivation_level],
        "Tutoring_Sessions": [tutoring_sessions],
        "Physical_Activity": [physical_activity],
        "Extracurricular_Activities": [extracurricular_activities]
    })


    # =========================
    # PREDICTION
    # =========================

    prediction = model.predict(data)[0]

    prediction = round(float(prediction), 1)

    # Performance level
    if prediction >= 80:
        performance_level = "Excellent"
    elif prediction >= 70:
        performance_level = "Very Good"
    elif prediction >= 60:
        performance_level = "Developing"
    else:
        performance_level = "Needs Improvement"

    # Save latest analysis for Home page
    request.session["last_analysis"] = {
        "prediction": prediction,
        "performance_level": performance_level,
        "hours_studied": hours_studied,
        "attendance": attendance,
        "sleep_hours": sleep_hours,
        "motivation_level": motivation_level
    }


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
            "Your weekly study time is relatively low."
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


    # =========================
    # RECOMMENDATIONS
    # =========================

    recommendations = []

    if attendance < 90:
        recommendations.append(
            "Aim for more consistent school attendance."
        )

    if hours_studied < 20:
        recommendations.append(
            "Consider increasing focused weekly study time."
        )

    if sleep_hours < 7:
        recommendations.append(
            "Try to maintain a more consistent sleep schedule."
        )

    if tutoring_sessions == 0:
        recommendations.append(
            "Consider academic support or tutoring for difficult subjects."
        )

    if physical_activity < 2:
        recommendations.append(
            "Consider adding regular physical activity to your weekly routine."
        )

    if not recommendations:
        recommendations.append(
            "Maintain your current routine and continue monitoring your progress."
        )


    # =========================
    # RESULTS PAGE
    # =========================

    return templates.TemplateResponse(
        request=request,
        name="result.html",

        context={
            "prediction": prediction,
            "performance_level": performance_level,

            "hours_studied": hours_studied,
            "attendance": attendance,
            "sleep_hours": sleep_hours,
            "previous_scores": previous_scores,

            "motivation_level": motivation_level,
            "tutoring_sessions": tutoring_sessions,
            "physical_activity": physical_activity,
            "extracurricular_activities": extracurricular_activities,

            "insights": insights,
            "recommendations": recommendations
        }
    )



@app.get("/how-it-works", response_class=HTMLResponse)
async def how_it_works(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="how_it_works.html",
        context={}
    )

@app.get("/improve", response_class=HTMLResponse)
async def improve(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="improve.html",
        context={}
    )

@app.get("/about", response_class=HTMLResponse)
async def about(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="about.html",
        context={}
    )


from fastapi.responses import Response

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

    return Response(content=content, media_type="application/xml")

@app.get("/robots.txt")
async def robots():
    content = """User-agent: *
Allow: /

Sitemap: https://student-performance-predictor-bas2.onrender.com/sitemap.xml
"""
    return Response(content=content, media_type="text/plain")