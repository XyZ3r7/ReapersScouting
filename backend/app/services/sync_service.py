from __future__ import annotations

from datetime import datetime
from typing import Tuple

from sqlalchemy.orm import Session

from app.core.config import settings
from app.models.team import Team
from app.models.match import Match
from app.models.match_participation import MatchParticipation
from app.services.first_api import FirstFtcApi


class SyncService:
    def __init__(self) -> None:
        self.api = FirstFtcApi()

    async def sync_event(self, db: Session, event_code: str) -> Tuple[int, int, int]:
        season = settings.FIRST_API_SEASON

        schedule_payload = await self.api.get_schedule(season, event_code)
        sched_matches = schedule_payload.get("schedule") or []

        start_time_by_match_number: dict[int, datetime | None] = {}
        for m in sched_matches:
            match_number = m.get("matchNumber")
            if match_number is None:
                continue
            start_raw = m.get("startTime")
            if isinstance(start_raw, str):
                try:
                    start_time = datetime.fromisoformat(start_raw.replace("Z", "+00:00"))
                except Exception:
                    start_time = None
            else:
                start_time = None
            start_time_by_match_number[int(match_number)] = start_time

        # 2. 拉 match results（swagger: EventMatchResultsModel_Version2）
        results_payload = await self.api.get_results(season, event_code)
        res_matches = results_payload.get("matches") or []

        team_numbers: set[int] = set()
        for m in res_matches:
            teams_list = m.get("teams") or []
            for t in teams_list:
                num = t.get("teamNumber")
                if num is not None:
                    try:
                        team_numbers.add(int(num))
                    except Exception:
                        pass

        # 4. Upsert Team
        upsert_team_count = 0
        for num in sorted(team_numbers):
            row = db.query(Team).filter(Team.team_number == num).one_or_none()
            if not row:
                row = Team(team_number=num, from_event_sync=True)
                db.add(row)
                upsert_team_count += 1

        db.flush()

        # 5. Upsert Match + Participation
        upsert_match_count = 0
        upsert_participation_count = 0

        for m in res_matches:
            match_number = m.get("matchNumber")
            if match_number is None:
                continue
            match_number = int(match_number)

            match_type = m.get("tournamentLevel")
            match_key = str(match_number)

            score_red_final = m.get("scoreRedFinal")
            score_blue_final = m.get("scoreBlueFinal")

            db_match = (
                db.query(Match)
                .filter(
                    Match.season == season,
                    Match.event_code == event_code,
                    Match.match_number == match_number,
                )
                .one_or_none()
            )
            if not db_match:
                db_match = Match(
                    season=season,
                    event_code=event_code,
                    match_key=match_key,
                    match_number=match_number,
                )
                db.add(db_match)

            db_match.match_type = match_type
            db_match.start_time = start_time_by_match_number.get(match_number)
            db_match.red_score = int(score_red_final) if score_red_final is not None else None
            db_match.blue_score = int(score_blue_final) if score_blue_final is not None else None

            db.flush()

            teams_list = m.get("teams") or []
            for t in teams_list:
                num = t.get("teamNumber")
                station = (t.get("station") or "").strip()  # "Red1" / "Blue2"
                if num is None or not station:
                    continue

                try:
                    team_num = int(num)
                except Exception:
                    continue

                alliance = None
                pos = None
                s_upper = station.upper()
                if s_upper.startswith("RED"):
                    alliance = "red"
                    try:
                        pos = int(s_upper.replace("RED", ""))
                    except Exception:
                        pos = None
                elif s_upper.startswith("BLUE"):
                    alliance = "blue"
                    try:
                        pos = int(s_upper.replace("BLUE", ""))
                    except Exception:
                        pos = None

                team = db.query(Team).filter(Team.team_number == team_num).one_or_none()
                if not team:
                    team = Team(team_number=team_num, from_event_sync=True)
                    db.add(team)
                    db.flush()

                part = (
                    db.query(MatchParticipation)
                    .filter(
                        MatchParticipation.match_id == db_match.id,
                        MatchParticipation.team_id == team.id,
                    )
                    .one_or_none()
                )
                if not part:
                    part = MatchParticipation(match_id=db_match.id, team_id=team.id)
                    db.add(part)

                part.alliance = alliance
                part.station = pos

                upsert_participation_count += 1

            upsert_match_count += 1

        db.commit()

        return upsert_team_count, upsert_match_count, upsert_participation_count
