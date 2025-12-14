from math import sqrt
from typing import List, Optional, Dict
from .models import Team


def compute_average_vector(team: Team) -> Optional[List[float]]:
    if not team.reviews:
        return None

    n = len(team.reviews)
    sums = [0.0] * 5

    for r in team.reviews:
        sums[0] += r.auto_score
        sums[1] += r.teleop_score
        sums[2] += r.endgame_score
        sums[3] += r.defense_score
        sums[4] += r.reliability

    return [s / n for s in sums]


def cosine_similarity(a: List[float], b: List[float]) -> float:
    dot = sum(x * y for x, y in zip(a, b))
    norm_a = sqrt(sum(x * x for x in a))
    norm_b = sqrt(sum(y * y for y in b))
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return dot / (norm_a * norm_b)


def compute_similarity_for_all(
    our_team_vector: List[float],
    teams: List[Team]
) -> Dict[int, float]:
    result: Dict[int, float] = {}
    for team in teams:
        v = compute_average_vector(team)
        if v is None:
            continue
        sim = cosine_similarity(our_team_vector, v)
        result[team.id] = sim
    return result
