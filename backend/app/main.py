from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

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

app.include_router(health.router)
app.include_router(sync.router)
app.include_router(reports.router)
app.include_router(compare.router)

@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)
