from tavily import TavilyClient

from app.core.config import settings
from app.core.logging_config import logger
from app.utils.retry import with_retry


@with_retry(max_attempts=3)
async def tavily_search(query: str, max_results: int = 5) -> list[dict]:
    """Search the live web via Tavily, scoped to Pakistani government domains where possible."""
    if not settings.tavily_api_key:
        logger.warning("TAVILY_API_KEY not set, skipping web search")
        return []

    client = TavilyClient(api_key=settings.tavily_api_key)
    response = client.search(
        query=f"{query} Pakistan government official",
        search_depth="advanced",
        max_results=max_results,
        include_domains=[
            "nadra.gov.pk",
            "dgip.gov.pk",
            "fbr.gov.pk",
            "hec.gov.pk",
            "pmo.gov.pk",
            "pakistan.gov.pk",
            "punjab.gov.pk",
        ],
    )
    results = []
    for item in response.get("results", []):
        results.append(
            {
                "title": item.get("title", ""),
                "url": item.get("url", ""),
                "text": item.get("content", ""),
                "score": item.get("score", 0.0),
            }
        )
    return results
