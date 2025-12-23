from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.db import get_db
from app.core.config import settings
from app.models.match import Match
from app.schemas.match import MatchOut

router = APIRouter(prefix="/matches", tags=["matches"])


@router.get("/event/{event_code}", response_model=list[MatchOut])
def list_matches_for_event(event_code: str, db: Session = Depends(get_db)):
    season = settings.FIRST_API_SEASON
    matches = (
        db.query(Match)
        .filter(Match.season == season, Match.event_code == event_code)
        .order_by(Match.match_number.asc().nullslast(), Match.id.asc())
        .all()
    )
    return matches


@router.get("/{match_id}", response_model=MatchOut)
def get_match(match_id: int, db: Session = Depends(get_db)):
    match = db.query(Match).filter(Match.id == match_id).one_or_none()
    if not match:
        raise HTTPException(status_code=404, detail="Match not found")
    return match
