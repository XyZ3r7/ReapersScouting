from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import select

from . import models, schemas


# ===== Team =====

def get_team_by_number(db: Session, team_number: int) -> Optional[models.Team]:
    stmt = select(models.Team).where(models.Team.team_number == team_number)
    return db.execute(stmt).scalar_one_or_none()


def get_team(db: Session, team_id: int) -> Optional[models.Team]:
    stmt = select(models.Team).where(models.Team.id == team_id)
    return db.execute(stmt).scalar_one_or_none()


def get_teams(db: Session, skip: int = 0, limit: int = 100) -> List[models.Team]:
    stmt = select(models.Team).offset(skip).limit(limit)
    return list(db.execute(stmt).scalars().all())


def create_team(db: Session, team_in: schemas.TeamCreate) -> models.Team:
    db_team = models.Team(
        team_number=team_in.team_number,
        name=team_in.name,
        location=team_in.location,
        rookie_year=team_in.rookie_year,
    )
    db.add(db_team)
    db.commit()
    db.refresh(db_team)
    return db_team


def update_team(db: Session, db_team: models.Team, update_in: schemas.TeamUpdate) -> models.Team:
    if update_in.name is not None:
        db_team.name = update_in.name
    if update_in.location is not None:
        db_team.location = update_in.location
    if update_in.rookie_year is not None:
        db_team.rookie_year = update_in.rookie_year
    db.commit()
    db.refresh(db_team)
    return db_team


# ===== Review =====

def create_team_review(db: Session, review_in: schemas.TeamReviewCreate) -> models.TeamReview:
    db_review = models.TeamReview(
        team_id=review_in.team_id,
        reviewer=review_in.reviewer,
        auto_score=review_in.auto_score,
        teleop_score=review_in.teleop_score,
        endgame_score=review_in.endgame_score,
        defense_score=review_in.defense_score,
        reliability=review_in.reliability,
        comment=review_in.comment,
    )
    db.add(db_review)
    db.commit()
    db.refresh(db_review)
    return db_review


def get_reviews_for_team(db: Session, team_id: int) -> List[models.TeamReview]:
    stmt = select(models.TeamReview).where(models.TeamReview.team_id == team_id)
    return list(db.execute(stmt).scalars().all())


# ===== Event =====

def create_event(db: Session, event_in: schemas.EventCreate) -> models.Event:
    db_event = models.Event(
        code=event_in.code,
        name=event_in.name,
        location=event_in.location,
        start_date=event_in.start_date,
        end_date=event_in.end_date,
    )
    db.add(db_event)
    db.commit()
    db.refresh(db_event)
    return db_event


def get_events(db: Session, skip: int = 0, limit: int = 100) -> List[models.Event]:
    stmt = select(models.Event).offset(skip).limit(limit)
    return list(db.execute(stmt).scalars().all())
