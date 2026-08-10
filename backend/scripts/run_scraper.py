"""Run the full government-sites scraping pipeline.
   python scripts/run_scraper.py
"""
import asyncio
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

from app.scraper.scrape_gov_sites import main  # noqa: E402

if __name__ == "__main__":
    asyncio.run(main())
