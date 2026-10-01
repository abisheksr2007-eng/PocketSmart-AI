import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from .config import settings
from .database import create_tables
from .routes.api import router as api
from .routes.auth import router as auth
from .routes.pages import router as pages
from .routes.planners import router as planners


app = FastAPI(
    title=settings.app_name,
    description=(
        "AI-powered budget planning and recommendation assistant."
    ),
    version="1.0.0",
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


os.makedirs(settings.upload_dir, exist_ok=True)

app.mount(
    "/static",
    StaticFiles(directory="static"),
    name="static",
)


@app.on_event("startup")
def startup_event():
    create_tables()


app.include_router(pages,
)
app.include_router(
    auth,
    prefix="/api",
)

app.include_router(
    planners,
    prefix="/api",
)

app.include_router(
    api,
    prefix="/api",
)


@app.get("/health")
def health():
    return {
        "status": "ok",
        "application": settings.app_name,
    }


@app.get("/startup")
def startup_check():
    return {
        "status": "running",
        "message": "PocketSmart AI is running successfully.",
    }