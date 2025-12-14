import requests
from sqlalchemy.orm import Session
from .database import SessionLocal
from . import models
from .config import get_settings

settings = get_settings()

BASE_URL = "https://ftc-events.firstinspires.org/v2.0"


import base64
import requests
from .config import get_settings

settings = get_settings()

BASE_URL = "https://ftc-events.firstinspires.org/v2.0"

import base64
import requests
from .config import get_settings

settings = get_settings()

BASE_URL = "https://ftc-api.firstinspires.org/v2.0"

def fetch(endpoint: str):
    url = f"{BASE_URL}/{settings.first_api_season}/{endpoint}"
    print(f"[SYNC] Fetching: {url}")

    # Build Basic Auth token
    token_raw = f"{settings.first_api_username}:{settings.first_api_token}"
    token_b64 = base64.b64encode(token_raw.encode()).decode()

    headers = {
        "Authorization": f"Basic {token_b64}",
        "Accept": "application/json",
        "User-Agent": "ReapersScouting/1.0"
    }

    response = requests.get(url, headers=headers)

    print("Status:", response.status_code)
    if response.status_code != 200:
        print(response.text)
        return None

    return response.json()




def sync_teams(db: Session):
    print("=== Syncing Teams ===")

    data = fetch("teams")
    if not data or "teams" not in data:
        print("[ERROR] No team data")
        return

    for t in data["teams"]:
        team_number = t.get("teamNumber")
        name = t.get("nameShort")
        location = f"{t.get('city')}, {t.get('stateProv')}, {t.get('country')}"
        rookie_year = t.get("rookieYear")

        db_team = db.query(models.Team).filter(models.Team.team_number == team_number).first()

        if db_team:
            db_team.name = name
            db_team.location = location
            db_team.rookie_year = rookie_year
        else:
            db_team = models.Team(
                team_number=team_number,
                name=name,
                location=location,
                rookie_year=rookie_year,
            )
            db.add(db_team)

    db.commit()
    print("✅ Teams synced.")


def sync_events(db: Session):
    print("=== Syncing Events ===")

    data = fetch("events")
    if not data or "events" not in data:
        print("[ERROR] No event data")
        return

    for e in data["events"]:
        code = e.get("code")
        name = e.get("name")
        location = e.get("venue")
        start_date = e.get("dateStart")
        end_date = e.get("dateEnd")

        db_event = db.query(models.Event).filter(models.Event.code == code).first()

        if db_event:
            db_event.name = name
            db_event.location = location
            db_event.start_date = start_date
            db_event.end_date = end_date
        else:
            db_event = models.Event(
                code=code,
                name=name,
                location=location,
                start_date=start_date,
                end_date=end_date,
            )
            db.add(db_event)

    db.commit()
    print("✅ Events synced.")


def run_sync():
    db = SessionLocal()
    try:
        sync_teams(db)
        sync_events(db)
    finally:
        db.close()


if __name__ == "__main__":
    run_sync()
