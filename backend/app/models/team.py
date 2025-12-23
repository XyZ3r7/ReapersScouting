from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship

from app.core.db import Base


class Team(Base):
    __tablename__ = "teams"

    id = Column(Integer, primary_key=True, index=True)
    team_number = Column(Integer, unique=True, index=True, nullable=False)

    name = Column(String(256), nullable=True)
    city = Column(String(128), nullable=True)
    state_prov = Column(String(64), nullable=True)
    country = Column(String(64), nullable=True)

    from_event_sync = Column(Boolean, default=False)

    participations = relationship("MatchParticipation", back_populates="team", cascade="all, delete-orphan")
    reports = relationship("MatchReport", back_populates="team", cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return f"<Team #{self.team_number} {self.name or ''}>"
