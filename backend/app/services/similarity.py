# from __future__ import annotations
# from sqlalchemy.orm import Session
# from app.models.report import TeamReport
# from app.core.config import settings
# from sentence_transformers import SentenceTransformer, util
# import re
#
# model = SentenceTransformer('all-MiniLM-L6-v2')
#
# def extract_number(value: str):
#     if not value:
#         return None
#     match = re.search(r"\d+", value)
#     return int(match.group()) if match else None
#
# def jaccard_similarity(a: str, b: str):
#     set_a = set(a.lower().split())
#     set_b = set(b.lower().split())
#     if not set_a or not set_b:
#         return 0.0
#     return len(set_a & set_b) / len(set_a | set_b)
#
# def compare_numeric_field(a: str, b: str, weight: float, scale: float = 50.0):
#     na = extract_number(a)
#     nb = extract_number(b)
#     if na is None or nb is None:
#         return 0.0
#     dist = abs(na - nb)
#     frac = max(0.0, 1.0 - dist / scale)
#     return weight * frac
#
# def compute_similarity(db: Session, other_team: int):
#     our_team = settings.OUR_TEAM_ID
#
#     our = db.query(TeamReport).filter(TeamReport.team_number == our_team).one_or_none()
#     oth = db.query(TeamReport).filter(TeamReport.team_number == other_team).one_or_none()
#
#     if not our or not oth:
#         return 0.0, {"reason": "missing_report"}
#
#     breakdown = {}
#     struct_points = 0.0
#     struct_total = 0.0
#
#     def add(label, score, weight, detail):
#         nonlocal struct_points, struct_total
#         struct_points += score
#         struct_total += weight
#         breakdown[label] = {"weight": weight, "score": round(score, 2), "detail": detail}
#
#     # shooting_range (Jaccard)
#     weight = 25
#     sim = jaccard_similarity(our.shooting_range or "", oth.shooting_range or "")
#     add("shooting_range", sim * weight, weight, {"similarity": sim})
#
#     # robots_scored (scale=10)
#     weight = 20
#     if our.robots_scored is not None and oth.robots_scored is not None:
#         dist = abs(our.robots_scored - oth.robots_scored)
#         frac = max(0.0, 1.0 - dist / 10.0)
#         add("robots_scored", frac * weight, weight, {"dist": dist})
#     else:
#         add("robots_scored", 0.0, weight, "missing")
#
#     # max_score_without_pattern
#     weight = 15
#     score = compare_numeric_field(our.max_score_without_pattern, oth.max_score_without_pattern, weight)
#     add("max_score_without_pattern", score, weight, {})
#
#     # max_score_with_pattern
#     weight = 10
#     score = compare_numeric_field(our.max_score_with_pattern, oth.max_score_with_pattern, weight)
#     add("max_score_with_pattern", score, weight, {})
#
#     # needs_human_player
#     weight = 15
#     add("needs_human_player",
#         weight if our.needs_human_player == oth.needs_human_player else 0.0,
#         weight,
#         "match" if our.needs_human_player == oth.needs_human_player else "different")
#
#     # has_lifting_for_parking
#     weight = 15
#     add("has_lifting_for_parking",
#         weight if our.has_lifting_for_parking == oth.has_lifting_for_parking else 0.0,
#         weight,
#         "match" if our.has_lifting_for_parking == oth.has_lifting_for_parking else "different")
#
#     # structured score normalized to 0–100
#     struct_score = (struct_points / struct_total) * 100 if struct_total else 0
#     breakdown["struct_score"] = {"score": round(struct_score, 2)}
#
#     # notes similarity (reduced weight)
#     emb_a = model.encode(our.notes or "", convert_to_tensor=True)
#     emb_b = model.encode(oth.notes or "", convert_to_tensor=True)
#     notes_score = util.cos_sim(emb_a, emb_b).item() * 100
#     breakdown["notes_similarity"] = {"score": round(notes_score, 2)}
#
#     # final score: 80% struct + 20% notes
#     final = 0.8 * struct_score + 0.2 * notes_score
#     breakdown["final"] = {"score": round(final, 2)}
#
#     return round(final, 2), breakdown
from sqlalchemy.orm import Session
from sentence_transformers import SentenceTransformer, util
import re
from app.models.report import TeamReport
from app.core.config import settings

# -----------------------------
# Notes similarity (Hybrid)
# -----------------------------
model = SentenceTransformer('all-MiniLM-L6-v2')

def jaccard_similarity(a: str, b: str):
    set_a = set(re.findall(r"\w+", a.lower()))
    set_b = set(re.findall(r"\w+", b.lower()))
    if not set_a or not set_b:
        return 0.0
    return len(set_a & set_b) / len(set_a | set_b)

def compute_notes_similarity(text_a: str, text_b: str) -> float:
    a = text_a.strip()
    b = text_b.strip()

    # Exact match
    if a == b:
        return 100.0

    # Jaccard
    jac = jaccard_similarity(a, b) * 100

    # Embedding
    emb_a = model.encode(a, convert_to_tensor=True)
    emb_b = model.encode(b, convert_to_tensor=True)
    emb = util.cos_sim(emb_a, emb_b).item() * 100

    # Hybrid fusion
    final = 0.3 * jac + 0.3 * emb
    return round(final, 2)

# -----------------------------
# Main similarity function
# -----------------------------
def compute_similarity(db: Session, other_team: int):
    our_team = settings.OUR_TEAM_ID

    our = db.query(TeamReport).filter(TeamReport.team_number == our_team).one_or_none()
    oth = db.query(TeamReport).filter(TeamReport.team_number == other_team).one_or_none()

    if not our or not oth:
        return 0.0, {"reason": "missing_report"}

    breakdown = {}
    struct_points = 0.0
    struct_total = 0.0

    def add(label, score, weight, detail):
        nonlocal struct_points, struct_total
        struct_points += score
        struct_total += weight
        breakdown[label] = {"weight": weight, "score": round(score, 2), "detail": detail}

    # shooting_range
    weight = 25
    sim = jaccard_similarity(our.shooting_range or "", oth.shooting_range or "")
    add("shooting_range", sim * weight, weight, {"similarity": sim})

    # robots_scored
    weight = 20
    if our.robots_scored is not None and oth.robots_scored is not None:
        dist = abs(our.robots_scored - oth.robots_scored)
        frac = max(0.0, 1.0 - dist / 10.0)
        add("robots_scored", frac * weight, weight, {"dist": dist})
    else:
        add("robots_scored", 0.0, weight, "missing")

    # max_score_without_pattern
    weight = 15
    add("max_score_without_pattern", 15, weight, "placeholder")

    # max_score_with_pattern
    weight = 10
    add("max_score_with_pattern", 10, weight, "placeholder")

    # needs_human_player
    weight = 15
    add("needs_human_player",
        weight if our.needs_human_player == oth.needs_human_player else 0.0,
        weight,
        "match" if our.needs_human_player == oth.needs_human_player else "different")

    # has_lifting_for_parking
    weight = 15
    add("has_lifting_for_parking",
        weight if our.has_lifting_for_parking == oth.has_lifting_for_parking else 0.0,
        weight,
        "match" if our.has_lifting_for_parking == oth.has_lifting_for_parking else "different")

    # structured score
    struct_score = (struct_points / struct_total) * 100 if struct_total else 0
    breakdown["struct_score"] = {"score": round(struct_score, 2)}

    # notes similarity
    notes_score = compute_notes_similarity(our.notes or "", oth.notes or "")
    breakdown["notes_similarity"] = {"score": notes_score}

    # final score
    final = 0.8 * struct_score + 0.2 * notes_score
    breakdown["final"] = {"score": round(final, 2)}

    return round(final, 2), breakdown
