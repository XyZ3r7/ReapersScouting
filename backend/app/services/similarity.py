from __future__ import annotations

from rapidfuzz.fuzz import token_set_ratio
from sqlalchemy.orm import Session
from app.models.report import TeamReport
from app.core.config import settings


def _norm_text(s: str | None) -> str:
    return (s or "").strip()


def compute_similarity_0_100(db: Session, other_team: int) -> tuple[float, dict]:
    our_team = settings.OUR_TEAM_ID

    our = db.query(TeamReport).filter(TeamReport.team_number == our_team).one_or_none()
    oth = db.query(TeamReport).filter(TeamReport.team_number == other_team).one_or_none()

    if not our or not oth:
        return 0.0, {
            "reason": "missing_report",
            "our_report_exists": bool(our),
            "other_report_exists": bool(oth),
        }

    # A) 结构化字段：drivetrain/intake/cycle_speed
    struct_points = 0.0
    struct_total = 0.0
    breakdown = {}

    def eq_score(label: str, a: str | None, b: str | None, weight: float):
        nonlocal struct_points, struct_total
        struct_total += weight
        if (a or "").lower().strip() and (b or "").lower().strip() and (a or "").lower().strip() == (b or "").lower().strip():
            struct_points += weight
            breakdown[label] = {"weight": weight, "score": weight, "detail": "equal"}
        else:
            breakdown[label] = {"weight": weight, "score": 0.0, "detail": "different_or_missing"}

    def num_close(label: str, a: int | None, b: int | None, weight: float):
        nonlocal struct_points, struct_total
        struct_total += weight
        if a is None or b is None:
            breakdown[label] = {"weight": weight, "score": 0.0, "detail": "missing"}
            return
        # 差 0 -> 1.0, 差 9 -> 0.0（因为 1-10）
        dist = abs(int(a) - int(b))
        frac = max(0.0, 1.0 - dist / 9.0)
        sc = weight * frac
        struct_points += sc
        breakdown[label] = {"weight": weight, "score": sc, "detail": {"a": a, "b": b, "dist": dist}}

    eq_score("drivetrain", our.drivetrain, oth.drivetrain, weight=20.0)
    eq_score("intake_type", our.intake_type, oth.intake_type, weight=15.0)
    num_close("cycle_speed", our.cycle_speed, oth.cycle_speed, weight=15.0)

    struct_score = 0.0 if struct_total == 0 else (struct_points / struct_total) * 100.0

    # B) 文本字段：strengths/weaknesses/notes/auto_notes
    our_text = " ".join(
        [_norm_text(our.auto_notes), _norm_text(our.strengths), _norm_text(our.weaknesses), _norm_text(our.notes)]
    )
    oth_text = " ".join(
        [_norm_text(oth.auto_notes), _norm_text(oth.strengths), _norm_text(oth.weaknesses), _norm_text(oth.notes)]
    )
    text_score = float(token_set_ratio(our_text, oth_text))  # 0-100
    breakdown["text_similarity"] = {"weight": 50.0, "score": text_score, "detail": "token_set_ratio"}

    # 总分加权：结构化 50%，文本 50%
    final = 0.5 * struct_score + 0.5 * text_score
    breakdown["struct_score"] = {"score": struct_score, "detail": "normalized_struct_fields"}
    breakdown["final"] = {"score": final}

    return round(final, 2), breakdown
