import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routes import ai, feedback, ingestion, scholarships, students, recommendations
from .database import engine, Base, migrate_schema
from . import models
from .routes import simulation
from .routes import search
from .routes import dashboard
from .rate_limit import WriteRateLimitMiddleware

Base.metadata.create_all(bind=engine)
migrate_schema()

app = FastAPI()

allowed_origins = [
    origin.strip()
    for origin in os.getenv(
        "INTELLIBLE_ALLOWED_ORIGINS",
        "http://localhost:5500,http://127.0.0.1:5500,http://localhost:5173,http://127.0.0.1:5173",
    ).split(",")
    if origin.strip()
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(WriteRateLimitMiddleware)

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

app.include_router(feedback.router, prefix="/feedback", tags=["Feedback"])

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
