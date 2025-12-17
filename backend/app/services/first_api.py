from __future__ import annotations

import base64
import httpx
from app.core.config import settings

def _basic_auth_header(username: str, token: str) -> str:
    raw = f"{username}:{token}".encode("utf-8")
    return "Basic " + base64.b64encode(raw).decode("ascii")

class FirstFtcApi:
    def __init__(self):
        self.base_url = "https://ftc-api.firstinspires.org"

    async def _get(self, path: str, params: dict | None = None) -> dict:
        url = f"{self.base_url}/{path.lstrip('/')}"
        headers = {
            "Authorization": _basic_auth_header(settings.FIRST_API_USERNAME, settings.FIRST_API_TOKEN),
            "Accept": "application/json",
            "If-Modified-Since": "Thu, 01 Jan 1970 00:00:00 GMT",
        }
        async with httpx.AsyncClient(timeout=30, follow_redirects=False) as client:
            r = await client.get(url, headers=headers, params=params)

            if r.status_code in (301, 302, 307, 308):
                raise RuntimeError(
                    f"Unexpected redirect. Check URL. Redirected to: {r.headers.get('Location')}"
                )

            r.raise_for_status()
            return r.json()

    async def get_event_teams(self, season: int, event_code: str) -> dict:
        return await self._get(
            f"v2.0/{season}/teams",
            params={"eventCode": event_code}
        )

    async def get_schedule(self, season: int, event_code: str, tournament_level: str = "qual") -> dict:
        return await self._get(
            f"v2.0/{season}/schedule/{event_code}/{tournament_level}/hybrid"
        )

    async def get_results(self, season: int, event_code: str) -> dict:
        return await self._get(
            f"v2.0/{season}/matches/{event_code}"
        )

    async def list_events(self, season: int) -> dict:
        return await self._get(f"v2.0/{season}/events")
