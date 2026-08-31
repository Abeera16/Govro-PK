"""
Scraping pipeline: fetches each configured government source with Playwright
(to handle JS-rendered pages), extracts clean textual content with BeautifulSoup,
and returns structured documents ready for chunking + embedding.
"""
import asyncio

from bs4 import BeautifulSoup
from playwright.async_api import async_playwright

from app.core.logging_config import logger
from app.scraper.sources import GOV_SOURCES
from app.utils.retry import with_retry

REQUEST_TIMEOUT_MS = 30000


@with_retry(max_attempts=3, min_wait=2, max_wait=10)
async def fetch_rendered_html(url: str) -> str:
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True, args=["--ignore-certificate-errors"])
        try:
            page = await browser.new_page(
                user_agent="GovroPK-Bot/1.0 (+https://govropk.pk)",
                ignore_https_errors=True,
            )
            await page.goto(url, timeout=REQUEST_TIMEOUT_MS, wait_until="networkidle")
            html = await page.content()
            return html
        finally:
            await browser.close()


def extract_clean_text(html: str) -> str:
    soup = BeautifulSoup(html, "html.parser")
    for tag in soup(["script", "style", "nav", "footer", "header", "noscript", "svg"]):
        tag.decompose()

    main = soup.find("main") or soup.find("article") or soup.body or soup
    text = main.get_text(separator=" ", strip=True)
    return text


async def scrape_source(source: dict) -> dict | None:
    url = source["url"]
    logger.info(f"Scraping: {url}")
    try:
        html = await fetch_rendered_html(url)
        text = extract_clean_text(html)
        if len(text) < 200:
            logger.warning(f"Very little content extracted from {url} ({len(text)} chars)")
        return {
            "url": url,
            "category": source["category"],
            "title": source["title"],
            "text": text,
        }
    except Exception as exc:  # noqa: BLE001
        logger.error(f"Failed to scrape {url}: {exc}")
        return None


async def scrape_all_sources(sources: list[dict] | None = None) -> list[dict]:
    sources = sources or GOV_SOURCES
    results = await asyncio.gather(*(scrape_source(s) for s in sources))
    return [r for r in results if r is not None]
