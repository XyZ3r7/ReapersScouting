from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from . import models, schemas, crud, similarity
from .database import engine, Base, get_db
from .config import get_settings

settings = get_settings()

Base.metadata.create_all(bind=engine)

app = FastAPI(title="FTC Scouting Backend", version="0.1.0")


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.post("/teams/", response_model=schemas.Team)
def create_team(team_in: schemas.TeamCreate, db: Session = Depends(get_db)):
    db_team = crud.get_team_by_number(db, team_number=team_in.team_number)
    if db_team:
        raise HTTPException(status_code=400, detail="Team number already exists")
    return crud.create_team(db, team_in)


@app.get("/teams/", response_model=List[schemas.Team])
def list_teams(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_teams(db, skip=skip, limit=limit)


@app.get("/teams/{team_id}", response_model=schemas.TeamWithReviews)
def get_team(team_id: int, db: Session = Depends(get_db)):
    db_team = crud.get_team(db, team_id=team_id)
    if not db_team:
        raise HTTPException(status_code=404, detail="Team not found")
    # 通过 orm_mode 自动带上 reviews
    return db_team


@app.patch("/teams/{team_id}", response_model=schemas.Team)
def update_team(team_id: int, update_in: schemas.TeamUpdate, db: Session = Depends(get_db)):
    db_team = crud.get_team(db, team_id=team_id)
    if not db_team:
        raise HTTPException(status_code=404, detail="Team not found")
    return crud.update_team(db, db_team=db_team, update_in=update_in)


# ===== 队伍评价 API =====

@app.post("/reviews/", response_model=schemas.TeamReview)
def create_review(review_in: schemas.TeamReviewCreate, db: Session = Depends(get_db)):
    db_team = crud.get_team(db, team_id=review_in.team_id)
    if not db_team:
        raise HTTPException(status_code=404, detail="Team not found")
    return crud.create_team_review(db, review_in)


@app.get("/teams/{team_id}/reviews", response_model=List[schemas.TeamReview])
def get_team_reviews(team_id: int, db: Session = Depends(get_db)):
    db_team = crud.get_team(db, team_id=team_id)
    if not db_team:
        raise HTTPException(status_code=404, detail="Team not found")
    return crud.get_reviews_for_team(db, team_id=team_id)


@app.post("/events/", response_model=schemas.Event)
def create_event(event_in: schemas.EventCreate, db: Session = Depends(get_db)):
    return crud.create_event(db, event_in)


@app.get("/events/", response_model=List[schemas.Event])
def list_events(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_events(db, skip=skip, limit=limit)


@app.get("/similar-teams/", response_model=List[schemas.TeamSimilarity])
def get_similar_teams(limit: int = 50, db: Session = Depends(get_db)):
    our_team = crud.get_team_by_number(db, team_number=settings.our_team_id)
    if not our_team:
        raise HTTPException(status_code=404, detail="Our team not found in database")

    our_vec = similarity.compute_average_vector(our_team)
    if our_vec is None:
        raise HTTPException(status_code=400, detail="Our team has no reviews yet")

    all_teams = crud.get_teams(db, skip=0, limit=10000)
    sims = similarity.compute_similarity_for_all(our_team_vector=our_vec, teams=all_teams)


    team_map = {t.id: t for t in all_teams}
    result = []
    for tid, sim in sims.items():
        if tid == our_team.id:
            continue
        result.append(
            schemas.TeamSimilarity(
                team=team_map[tid],
                similarity=sim,
            )
        )


    result.sort(key=lambda x: x.similarity, reverse=True)

    return result[:limit]
