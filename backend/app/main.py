from fastapi import FastAPI
from .routes import ai, ingestion, scholarships, students, recommendations
from .database import engine, Base, migrate_schema
from . import models
from .routes import simulation
from .routes import search
from .routes import dashboard

Base.metadata.create_all(bind=engine)
migrate_schema()

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

app.include_router(
    ingestion.router,
    prefix="/ingestion",
    tags=["Ingestion"],
)

app.include_router(
    ai.router,
    prefix="/ai",
    tags=["AI"],
)
