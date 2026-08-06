from fastapi import FastAPI
from .routes import scholarships, students, recommendations
from .database import engine, Base
from . import models
from .routes import simulation
from .routes import search
from .routes import dashboard

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(
    scholarships.router,
    prefix="/scholarships",
    tags=["Scholarships"]
)

app.include_router(
    search.router
)

app.include_router(
    students.router,
    prefix="/students",
    tags=["Students"]
)

app.include_router(
    recommendations.router,
    prefix="/recommendations",
    tags=["Recommendations"]
)

@app.get("/")
def home():
    return {"message": "AI Scholarship Finder API is running!"}

app.include_router(
    simulation.router
)

app.include_router(
    dashboard.router,
    prefix="/dashboard",
    tags=["Dashboard"]
)