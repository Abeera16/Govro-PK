"""Create all database tables. Run once (or on deploy) with:
   python scripts/init_db.py
"""
import asyncio
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

from app.core.database import init_models  # noqa: E402
from app.core.logging_config import configure_logging, logger  # noqa: E402


async def main() -> None:
    configure_logging()
    await init_models()
    logger.info("All tables created successfully.")


if __name__ == "__main__":
    asyncio.run(main())
