from app.agents.state import AgentState
from app.mcp.client import mcp_client
from app.core.logging_config import logger


async def fallback_node(state: AgentState) -> dict:
    """Fallback web-search agent, invoked when RAG confidence is too low."""
    trace = state.get("agent_trace", [])
    query = state["user_query"]

    try:
        web_results = await mcp_client.call("web_search", query=query, max_results=5)
    except Exception as exc:  # noqa: BLE001
        logger.error(f"Web search fallback failed: {exc}")
        web_results = []

    trace.append(
        {"agent": "fallback_agent", "action": "web_search", "detail": f"found {len(web_results)} results"}
    )
    return {"web_results": web_results, "agent_trace": trace}
