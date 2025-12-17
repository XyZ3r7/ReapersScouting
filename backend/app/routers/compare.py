from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.db import get_db
from app.core.config import settings
from app.schemas.compare import SimilarityResult
from app.services.similarity import compute_similarity_0_100

router = APIRouter(prefix="/compare", tags=["compare"])


@router.get("/{other_team}", response_model=SimilarityResult)
def compare(other_team: int, db: Session = Depends(get_db)):
    if other_team == settings.OUR_TEAM_ID:
        raise HTTPException(status_code=400, detail="cannot_compare_with_self")

    score, breakdown = compute_similarity_0_100(db, other_team)
    return SimilarityResult(
        our_team=settings.OUR_TEAM_ID,
        other_team=other_team,
        similarity_0_100=score,
        breakdown=breakdown,
    )
