import asyncio
import json
from app.core.scraper import scrape_website

async def main():
    res = await scrape_website("https://dainwi.vercel.app")
    print(json.dumps(res, indent=2))

if __name__ == "__main__":
    asyncio.run(main())
