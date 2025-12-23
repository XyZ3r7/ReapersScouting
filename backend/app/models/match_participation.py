from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from app.core.db import Base


class MatchParticipation(Base):
    __tablename__ = "match_participations"

    id = Column(Integer, primary_key=True, index=True)

    match_id = Column(Integer, ForeignKey("matches.id"), nullable=False, index=True)
    team_id = Column(Integer, ForeignKey("teams.id"), nullable=False, index=True)

    alliance = Column(String(8), nullable=True)  # "red" or "blue"
    station = Column(Integer, nullable=True)     # 1,2,3...

    score_detail_json = Column(String, nullable=True)

    match = relationship("Match", back_populates="participations")
    team = relationship("Team", back_populates="participations")

    def __repr__(self) -> str:
        return f"<MP match={self.match_id} team={self.team_id} {self.alliance}{self.station}>"
