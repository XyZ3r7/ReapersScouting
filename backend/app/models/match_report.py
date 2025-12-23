from datetime import datetime, date

from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Date
from sqlalchemy.orm import relationship

from app.core.db import Base


class MatchReport(Base):
    __tablename__ = "match_reports"

    id = Column(Integer, primary_key=True, index=True)

    match_id = Column(Integer, ForeignKey("matches.id"), nullable=False, index=True)
    team_id = Column(Integer, ForeignKey("teams.id"), nullable=False, index=True)

    match_date = Column(Date, nullable=True)
    match_number = Column(Integer, nullable=True)

    shooting_range = Column(String, nullable=True)
    robots_scored = Column(Integer, nullable=True)
    max_score_without_pattern = Column(String, nullable=True)
    max_score_with_pattern = Column(String, nullable=True)
    needs_human_player = Column(String, nullable=True)
    has_lifting_for_parking = Column(String, nullable=True)
    notes = Column(String, nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)

    match = relationship("Match", back_populates="reports")
    team = relationship("Team", back_populates="reports")

    def __repr__(self) -> str:
        return f"<Report match={self.match_id} team={self.team_id}>"
