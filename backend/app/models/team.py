from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.core.db import Base

class Team(Base):
    __tablename__ = "teams"

    id = Column(Integer, primary_key=True, index=True)
    team_number = Column(Integer, unique=True, index=True)

    reports = relationship("MatchReport", back_populates="team")
