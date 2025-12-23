from pydantic import BaseModel


class EventSyncResult(BaseModel):
    event_code: str
    season: int
    teams_upserted: int
    matches_upserted: int
    participations_upserted: int
