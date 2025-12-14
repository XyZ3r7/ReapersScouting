from sqlalchemy import Column, Integer, String, Float, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime

from .database import Base


class Team(Base):
    __tablename__ = "teams"

    id = Column(Integer, primary_key=True, index=True)
    team_number = Column(Integer, unique=True, index=True, nullable=False)
    name = Column(String(255), nullable=True)
    location = Column(String(255), nullable=True)
    rookie_year = Column(Integer, nullable=True)

    reviews = relationship("TeamReview", back_populates="team", cascade="all, delete-orphan")


class TeamReview(Base):
    __tablename__ = "team_reviews"

    id = Column(Integer, primary_key=True, index=True)
    team_id = Column(Integer, ForeignKey("teams.id", ondelete="CASCADE"), nullable=False)
    reviewer = Column(String(255), nullable=False)

    auto_score = Column(Integer, nullable=False)
    teleop_score = Column(Integer, nullable=False)
    endgame_score = Column(Integer, nullable=False)
    defense_score = Column(Integer, nullable=False)
    reliability = Column(Integer, nullable=False)

    comment = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    team = relationship("Team", back_populates="reviews")


class Event(Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True, index=True)
    code = Column(String(50), unique=True, index=True, nullable=False)
    name = Column(String(255), nullable=False)
    location = Column(String(255), nullable=True)
    start_date = Column(DateTime, nullable=True)
    end_date = Column(DateTime, nullable=True)
