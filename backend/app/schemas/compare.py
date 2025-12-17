from pydantic import BaseModel


class SimilarityResult(BaseModel):
    our_team: int
    other_team: int
    similarity_0_100: float
    breakdown: dict
