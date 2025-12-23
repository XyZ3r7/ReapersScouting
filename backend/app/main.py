from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.db import Base, engine
from app.core.config import settings
from app.routers import health, sync, matches, reports

Base.metadata.create_all(bind=engine)

app = FastAPI(title="FTC Scouting Backend", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router)
app.include_router(sync.router)
app.include_router(matches.router)
app.include_router(reports.router)


@app.get("/")
def root():
    return {"message": "FTC Scouting Backend"}
