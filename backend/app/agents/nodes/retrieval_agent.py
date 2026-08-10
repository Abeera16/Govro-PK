from app.agents.state import AgentState
from app.mcp.client import mcp_client
from app.core.logging_config import logger

RAG_CONFIDENCE_THRESHOLD = 0.55


async def retrieval_node(state: AgentState) -> dict:
    trace = state.get("agent_trace", [])
    query = state["user_query"]
    category = state.get("category", "general")

    try:
        rag_results = await mcp_client.call(
            "rag_search", query=query, k=5, category=None if category == "general" else category
        )
    except Exception as exc:  # noqa: BLE001
        logger.error(f"RAG retrieval failed: {exc}")
        rag_results = []

    try:
        gov_info = await mcp_client.call("gov_lookup", service_key=category)
    except Exception as exc:  # noqa: BLE001
        logger.error(f"Gov lookup failed: {exc}")
        gov_info = None

    confidence = max((r.get("score", 0.0) for r in rag_results), default=0.0)

    trace.append(
        {
            "agent": "retrieval_agent",
            "action": "rag_search",
            "detail": f"found {len(rag_results)} chunks, confidence={confidence:.2f}",
        }
    )

    return {
        "rag_results": rag_results,
        "gov_lookup_result": gov_info,
        "retrieval_confidence": confidence,
        "agent_trace": trace,
    }


def should_fallback_to_web(state: AgentState) -> str:
    """Conditional edge: decide whether retrieval was strong enough or we need web fallback."""
    if state.get("retrieval_confidence", 0.0) >= RAG_CONFIDENCE_THRESHOLD and state.get("rag_results"):
        return "citation_agent"
    return "fallback_agent"
