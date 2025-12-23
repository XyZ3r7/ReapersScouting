from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.db import get_db
from app.core.config import settings
from app.services.sync_service import SyncService
from app.schemas.sync import EventSyncResult
from app.models.match import Match
from app.models.match_participation import MatchParticipation
from app.models.team import Team

router = APIRouter(prefix="/sync", tags=["sync"])


@router.post("/event/{event_code}", response_model=EventSyncResult)
async def sync_event(event_code: str, db: Session = Depends(get_db)):
    service = SyncService()
    try:
        teams_upserted, matches_upserted, participations_upserted = await service.sync_event(db, event_code)
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

    return EventSyncResult(
        event_code=event_code,
        season=settings.FIRST_API_SEASON,
        teams_upserted=teams_upserted,
        matches_upserted=matches_upserted,
        participations_upserted=participations_upserted,
    )


@router.get("/event/{event_code}/summary")
def event_summary(event_code: str, db: Session = Depends(get_db)):
    season = settings.FIRST_API_SEASON
    matches = db.query(Match).filter(Match.season == season, Match.event_code == event_code).all()
    match_ids = [m.id for m in matches]
    team_ids = (
        db.query(MatchParticipation.team_id)
        .filter(MatchParticipation.match_id.in_(match_ids))
        .distinct()
        .all()
    )
    team_count = (
        db.query(Team)
        .filter(Team.id.in_([tid for (tid,) in team_ids]))
        .count()
    )
    return {
        "event_code": event_code,
        "season": season,
        "matches": len(matches),
        "teams": team_count,
    }
