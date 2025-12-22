from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pathlib import Path

from app.core.db import Base, engine
from app.routers import health, sync, reports, compare

app = FastAPI(title="FTC Scouting Backend", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

frontend_path = Path(__file__).resolve().parent.parent / "frontend"
app.mount("/", StaticFiles(directory=str(frontend_path), html=True), name="frontend")

app.include_router(health.router)
app.include_router(sync.router)
app.include_router(reports.router)
app.include_router(compare.router)

@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)
