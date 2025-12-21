
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.db import get_db
from app.core.config import settings
from app.schemas.compare import SimilarityResult
from app.services.similarity import compute_similarity

router = APIRouter(prefix="/compare", tags=["compare"])


@router.get("/{other_team}", response_model=SimilarityResult)
def compare(other_team: int, db: Session = Depends(get_db)):
    # Prevent comparing with self
    if other_team == settings.OUR_TEAM_ID:
        raise HTTPException(status_code=400, detail="cannot_compare_with_self")

    # Compute similarity score and breakdown
    score, breakdown = compute_similarity(db, other_team)

    # Return structured response
    return SimilarityResult(
        our_team=settings.OUR_TEAM_ID,
        other_team=other_team,
        similarity_0_100=score,
        breakdown=breakdown
    )
