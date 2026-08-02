from fastapi import FastAPI
from .routes import scholarships
from .database import engine, Base
from . import models

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(
    scholarships.router,
    prefix="/scholarships",
    tags=["Scholarships"]
)


@app.get("/")
def home():
    return {"message": "AI Scholarship Finder API is running!"}