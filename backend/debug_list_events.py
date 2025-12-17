import asyncio

from app.services.first_api import FirstFtcApi
from app.core.config import settings


async def main():
    api = FirstFtcApi()
    season = settings.FIRST_API_SEASON
    print("DEBUG season =", season)

    data = await api.list_events(season)
    events = data.get("events") or []
    print("Total events:", len(events))

    for e in events[:20]:  # 只看前 20 个，够用了
        print(e.get("code"), "-", e.get("name"))


if __name__ == "__main__":
    asyncio.run(main())
