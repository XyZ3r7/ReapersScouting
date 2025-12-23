from pydantic import BaseModel


class TeamBase(BaseModel):
    team_number: int
    name: str | None = None
    city: str | None = None
    state_prov: str | None = None
    country: str | None = None


class TeamOut(TeamBase):
    id: int

    class Config:
        orm_mode = True
