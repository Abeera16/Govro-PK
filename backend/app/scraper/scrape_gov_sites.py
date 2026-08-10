"""CLI entrypoint invoked by scripts/run_scraper.py — see that file for usage."""
import asyncio
import json
from pathlib import Path

from app.core.logging_config import configure_logging, logger
from app.scraper.pipeline import scrape_all_sources

OUTPUT_PATH = Path(__file__).resolve().parent.parent.parent / "data" / "scraped_gov_docs.json"


async def main() -> None:
    configure_logging()
    logger.info("Starting government sites scrape...")
    docs = await scrape_all_sources()
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(json.dumps(docs, indent=2, ensure_ascii=False), encoding="utf-8")
    logger.info(f"Scraped {len(docs)} documents -> {OUTPUT_PATH}")


if __name__ == "__main__":
    asyncio.run(main())
