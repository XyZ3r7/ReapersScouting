import json
from sqlalchemy.orm import Session

from app.models.ftcevent import Team, Match, MatchParticipation, Event
from app.services.first_api import FirstFtcApi
from app.core.config import settings


def _safe_get(d: dict, *keys, default=None):
    cur = d
    for k in keys:
        if not isinstance(cur, dict) or k not in cur:
            return default
        cur = cur[k]
    return cur


class SyncService:
    def __init__(self):
        self.api = FirstFtcApi()

    async def sync_event(self, db: Session, event_code: str) -> dict:
        season = settings.FIRST_API_SEASON

        # 1) Teams
        teams_payload = await self.api.get_event_teams(season, event_code)
        teams = teams_payload.get("teams") or teams_payload.get("Teams") or []
        upsert_team_count = 0
        for t in teams:
            num = t.get("teamNumber") or t.get("team_number")
            if not num:
                continue
            row = db.get(Team, int(num))
            if not row:
                row = Team(team_number=int(num))
                db.add(row)
            row.name = t.get("name")
            row.city = t.get("city")
            row.state_prov = t.get("stateProv") or t.get("state_prov")
            row.country = t.get("country")
            upsert_team_count += 1

        # 2) Schedule (times)
        schedule_payload = await self.api.get_schedule(season, event_code)
        sched_matches = schedule_payload.get("schedule") or schedule_payload.get("Schedule") or []

        # key -> start_time
        start_time_by_key: dict[str, str] = {}
        for m in sched_matches:
            mk = (m.get("matchNumber") or m.get("match_number") or m.get("matchKey") or m.get("match_key"))
            if mk is None:
                continue
            start_time_by_key[str(mk)] = m.get("startTime") or m.get("start_time")

        # 3) Results (scores + participants + breakdown)
        results_payload = await self.api.get_results(season, event_code)
        res_matches = results_payload.get("matches") or results_payload.get("Matches") or []

        upsert_match_count = 0
        upsert_participation_count = 0

        for m in res_matches:
            match_key = str(m.get("matchNumber") or m.get("match_number") or m.get("matchKey") or m.get("match_key"))
            if not match_key:
                continue

            match_type = m.get("tournamentLevel") or m.get("matchType") or m.get("match_type")
            red_score = _safe_get(m, "scoreRedFinal", default=None) or m.get("redScore")
            blue_score = _safe_get(m, "scoreBlueFinal", default=None) or m.get("blueScore")

            db_match = (
                db.query(Match)
                .filter(Match.season == season, Match.event_code == event_code, Match.match_key == match_key)
                .one_or_none()
            )
            if not db_match:
                db_match = Match(season=season, event_code=event_code, match_key=match_key)
                db.add(db_match)

            db_match.match_type = str(match_type) if match_type is not None else None
            db_match.start_time = start_time_by_key.get(match_key) or m.get("startTime") or m.get("start_time")
            db_match.red_score = int(red_score) if red_score is not None else None
            db_match.blue_score = int(blue_score) if blue_score is not None else None
            db.flush()

            alliances = m.get("alliances") or {}
            for alliance_name in ["red", "blue"]:
                a = alliances.get(alliance_name) or {}
                teams_list = a.get("teams") or a.get("Teams") or []

                for idx, p in enumerate(teams_list, start=1):
                    team_num = p.get("teamNumber") or p.get("team_number") or p.get("team")
                    if not team_num:
                        continue

                    part = (
                        db.query(MatchParticipation)
                        .filter(MatchParticipation.match_id == db_match.id, MatchParticipation.team_number == int(team_num))
                        .one_or_none()
                    )
                    if not part:
                        part = MatchParticipation(match_id=db_match.id, team_number=int(team_num))
                        db.add(part)

                    part.alliance = alliance_name
                    part.station = idx
                    part.score_detail_json = json.dumps(p.get("scoreDetails") or p.get("score_detail") or p.get("scoreBreakdown") or {})
                    upsert_participation_count += 1

            upsert_match_count += 1

        db.commit()
        return {
            "event_code": event_code,
            "season": season,
            "teams_upserted": upsert_team_count,
            "matches_upserted": upsert_match_count,
            "participations_upserted": upsert_participation_count,
        }
