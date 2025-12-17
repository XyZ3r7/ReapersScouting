from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.db import get_db
from app.services.sync_service import SyncService

router = APIRouter(prefix="/sync", tags=["sync"])
svc = SyncService()


@router.post("/event/{event_code}")
async def sync_event(event_code: str, db: Session = Depends(get_db)):
    return await svc.sync_event(db, event_code)

@router.get("/event/{event_code}/summary")
def event_summary(event_code: str, db: Session = Depends(get_db)):
    from app.models.ftcevent import Team, Match

    team_count = db.query(Team).count()
    match_count = db.query(Match).filter(Match.event_code == event_code).count()

    next_match = (
        db.query(Match)
        .filter(Match.event_code == event_code, Match.start_time != None)
        .order_by(Match.start_time)
        .first()
    )

    return {
        "event_code": event_code,
        "teams": team_count,
        "matches": match_count,
        "next_match": {
            "match_key": next_match.match_key if next_match else None,
            "start_time": next_match.start_time if next_match else None,
            "red_score": next_match.red_score,
            "blue_score": next_match.blue_score,
        } if next_match else None
    }

