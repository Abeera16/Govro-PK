"""
Chunk and embed scraped government documents, then upsert them into Qdrant,
recording metadata in Postgres (GovDocument) for auditability.

Usage:
    python scripts/ingest_to_qdrant.py
"""
import asyncio
import json
import sys
import uuid
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

from sqlalchemy import select  # noqa: E402

from app.core.database import AsyncSessionLocal, init_models  # noqa: E402
from app.core.logging_config import configure_logging, logger  # noqa: E402
from app.models.db_models import GovDocument  # noqa: E402
from app.rag.chunking import chunk_text, document_checksum  # noqa: E402
from app.rag.vector_store import delete_by_source, upsert_chunks  # noqa: E402

DATA_PATH = Path(__file__).resolve().parent.parent / "data" / "scraped_gov_docs.json"


async def ingest_document(session, doc: dict) -> None:
    url, title, category, text = doc["url"], doc["title"], doc["category"], doc["text"]
    checksum = document_checksum(text)

    result = await session.execute(select(GovDocument).where(GovDocument.source_url == url))
    existing = result.scalar_one_or_none()

    if existing and existing.checksum == checksum:
        logger.info(f"Unchanged, skipping: {url}")
        return

    chunks = chunk_text(text)
    if not chunks:
        logger.warning(f"No chunks produced for {url}, skipping")
        return

    delete_by_source(url)

    texts = [c.text for c in chunks]
    metadatas = [
        {"source_url": url, "title": title, "category": category, "chunk_index": c.chunk_index}
        for c in chunks
    ]
    ids = [str(uuid.uuid5(uuid.NAMESPACE_URL, f"{url}::chunk::{c.chunk_index}")) for c in chunks]
    upsert_chunks(texts=texts, metadatas=metadatas, ids=ids)

    if existing:
        existing.checksum = checksum
        existing.chunk_count = len(chunks)
        existing.title = title
        existing.category = category
    else:
        session.add(
            GovDocument(
                source_url=url, title=title, category=category, checksum=checksum, chunk_count=len(chunks)
            )
        )

    logger.info(f"Ingested {len(chunks)} chunks for {url}")


async def main() -> None:
    configure_logging()
    await init_models()

    if not DATA_PATH.exists():
        logger.error(f"No scraped data found at {DATA_PATH}. Run scripts/run_scraper.py first.")
        return

    docs = json.loads(DATA_PATH.read_text(encoding="utf-8"))
    async with AsyncSessionLocal() as session:
        for doc in docs:
            await ingest_document(session, doc)
        await session.commit()

    logger.info(f"Ingestion complete: {len(docs)} source documents processed.")


if __name__ == "__main__":
    asyncio.run(main())
