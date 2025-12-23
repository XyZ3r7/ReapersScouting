# from __future__ import annotations
#
# import re
# from typing import Dict, Any, Tuple
#
# from sqlalchemy.orm import Session
# from sentence_transformers import SentenceTransformer, util
#
# from app.core.config import settings
# from app.models.team import Team
# from app.models.match import MatchReport
#
# # Notes similarity model
# model = SentenceTransformer("all-MiniLM-L6-v2")
#
#
# def jaccard_similarity(a: str, b: str) -> float:
#     set_a = set(re.findall(r"\w+", a.lower()))
#     set_b = set(re.findall(r"\w+", b.lower()))
#     if not set_a or not set_b:
#         return 0.0
#     return len(set_a & set_b) / len(set_a | set_b)
#
#
# def compute_notes_similarity(text_a: str, text_b: str) -> float:
#     a = (text_a or "").strip()
#     b = (text_b or "").strip()
#
#     if not a and not b:
#         return 0.0
#
#     if a == b and a:
#         return 100.0
#
#     jac = jaccard_similarity(a, b) * 100.0
#
#     emb_a = model.encode(a, convert_to_tensor=True)
#     emb_b = model.encode(b, convert_to_tensor=True)
#     emb = util.cos_sim(emb_a, emb_b).item() * 100.0
#
#     final = 0.3 * jac + 0.3 * emb
#     return round(final, 2)
#
#
# def get_latest_report_for_team_number(db: Session, team_number: int) -> MatchReport | None:
#     team = db.query(Team).filter(Team.team_number == team_number).one_or_none()
#     if not team:
#         return None
#
#     # latest by date then match_number then id
#     report = (
#         db.query(MatchReport)
#         .filter(MatchReport.team_id == team.team_number)
#         .order_by(
#             MatchReport.match_date.desc().nullslast(),
#             MatchReport.match_number.desc().nullslast(),
#             MatchReport.id.desc(),
#         )
#         .first()
#     )
#     return report
#
#
# def compute_similarity(db: Session, other_team: int) -> Tuple[float, Dict[str, Any]]:
#     our_team_number = settings.OUR_TEAM_ID  # your config uses OUR_TEAM_ID
#
#     our = get_latest_report_for_team_number(db, our_team_number)
#     oth = get_latest_report_for_team_number(db, other_team)
#
#     if not our or not oth:
#         return 0.0, {"reason": "missing_report"}
#
#     breakdown: Dict[str, Any] = {}
#     struct_points = 0.0
#     struct_total = 0.0
#
#     def add(label: str, score: float, weight: float, detail: Any) -> None:
#         nonlocal struct_points, struct_total
#         struct_points += score
#         struct_total += weight
#         breakdown[label] = {
#             "weight": weight,
#             "score": round(score, 2),
#             "detail": detail,
#         }
#
#     # shooting_range
#     weight = 25.0
#     sim = jaccard_similarity(our.shooting_range or "", oth.shooting_range or "")
#     add("shooting_range", sim * weight / 100.0, weight, {"similarity": sim})
#
#     # robots_scored
#     weight = 20.0
#     if our.robots_scored is not None and oth.robots_scored is not None:
#         dist = abs(our.robots_scored - oth.robots_scored)
#         frac = max(0.0, 1.0 - dist / 10.0)
#         add("robots_scored", frac * weight, weight, {"dist": dist})
#     else:
#         add("robots_scored", 0.0, weight, "missing")
#
#     # max_score_without_pattern (placeholder: full weight if both non-empty and equal)
#     weight = 15.0
#     if our.max_score_without_pattern and oth.max_score_without_pattern:
#         score = weight if our.max_score_without_pattern == oth.max_score_without_pattern else weight * 0.5
#         detail = {
#             "our": our.max_score_without_pattern,
#             "other": oth.max_score_without_pattern,
#         }
#     else:
#         score = 0.0
#         detail = "missing"
#     add("max_score_without_pattern", score, weight, detail)
#
#     # max_score_with_pattern (similar placeholder logic)
#     weight = 10.0
#     if our.max_score_with_pattern and oth.max_score_with_pattern:
#         score = weight if our.max_score_with_pattern == oth.max_score_with_pattern else weight * 0.5
#         detail = {
#             "our": our.max_score_with_pattern,
#             "other": oth.max_score_with_pattern,
#         }
#     else:
#         score = 0.0
#         detail = "missing"
#     add("max_score_with_pattern", score, weight, detail)
#
#     # needs_human_player
#     weight = 15.0
#     needs_match = our.needs_human_player == oth.needs_human_player and our.needs_human_player is not None
#     add(
#         "needs_human_player",
#         weight if needs_match else 0.0,
#         weight,
#         "match" if needs_match else "different",
#     )
#
#     # has_lifting_for_parking
#     weight = 15.0
#     lift_match = our.has_lifting_for_parking == oth.has_lifting_for_parking and our.has_lifting_for_parking is not None
#     add(
#         "has_lifting_for_parking",
#         weight if lift_match else 0.0,
#         weight,
#         "match" if lift_match else "different",
#     )
#
#     struct_score = (struct_points / struct_total) * 100.0 if struct_total else 0.0
#     breakdown["struct_score"] = {"score": round(struct_score, 2)}
#
#     notes_score = compute_notes_similarity(our.notes or "", oth.notes or "")
#     breakdown["notes_similarity"] = {"score": notes_score}
#
#     final = 0.8 * struct_score + 0.2 * notes_score
#     breakdown["final"] = {"score": round(final, 2)}
#
#     breakdown["meta"] = {
#         "our_team": our_team_number,
#         "other_team": other_team,
#         "our_match_date": getattr(our, "match_date", None),
#         "other_match_date": getattr(oth, "match_date", None),
#     }
#
#     return round(final, 2), breakdown
