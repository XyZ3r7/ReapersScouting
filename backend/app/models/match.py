from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship

from app.core.db import Base


class Match(Base):
    __tablename__ = "matches"

    id = Column(Integer, primary_key=True, index=True)
    season = Column(Integer, index=True, nullable=False)
    event_code = Column(String(32), index=True, nullable=False)

    match_key = Column(String(64), index=True, nullable=False)   # e.g. "Q1"
    match_number = Column(Integer, index=True, nullable=True)
    match_type = Column(String(32), nullable=True)               # qual, playoff, etc.
    start_time = Column(DateTime, nullable=True)

    red_score = Column(Integer, nullable=True)
    blue_score = Column(Integer, nullable=True)

    participations = relationship("MatchParticipation", back_populates="match", cascade="all, delete-orphan")
    reports = relationship("MatchReport", back_populates="match", cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return f"<Match {self.event_code} {self.match_key}>"
