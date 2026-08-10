from app.agents.llm_factory import get_chat_model
from app.agents.prompts import FALLBACK_NOTICE, SYNTHESIS_SYSTEM_PROMPT
from app.agents.state import AgentState
from app.core.logging_config import logger
from app.models.schemas import Citation
from app.rag.retriever import docs_to_citations


def _format_context(rag_results: list[dict], web_results: list[dict]) -> str:
    parts = []
    for i, r in enumerate(rag_results, start=1):
        parts.append(f"[GOV-DOC {i}] ({r.get('title')}, {r.get('url')}):\n{r.get('text')}")
    for i, r in enumerate(web_results, start=1):
        parts.append(f"[WEB {i}] ({r.get('title')}, {r.get('url')}):\n{r.get('text')}")
    return "\n\n".join(parts) if parts else "No relevant context was retrieved."


async def citation_node(state: AgentState) -> dict:
    """Synthesizes the final answer grounded in retrieved context and attaches citations."""
    trace = state.get("agent_trace", [])
    rag_results = state.get("rag_results", []) or []
    web_results = state.get("web_results", []) or []
    gov_info = state.get("gov_lookup_result")

    context = _format_context(rag_results, web_results)
    gov_info_str = str(gov_info) if gov_info else "No structured record found."

    llm = get_chat_model(temperature=0.2)
    system_prompt = SYNTHESIS_SYSTEM_PROMPT.format(context=context, gov_info=gov_info_str)

    history = state.get("messages", [])[-6:]
    messages = [{"role": "system", "content": system_prompt}, *history,
                {"role": "user", "content": state["user_query"]}]

    try:
        response = await llm.ainvoke(messages)
        answer = response.content.strip()
    except Exception as exc:  # noqa: BLE001
        logger.error(f"Synthesis LLM call failed: {exc}")
        answer = (
            "I'm sorry, I ran into an error generating a response. Please try again shortly, "
            "or contact the relevant department directly."
        )

    if web_results and not rag_results:
        answer = f"{answer}\n\n_{FALLBACK_NOTICE}_"

    citations: list[Citation] = []
    if rag_results:
        citations += docs_to_citations(rag_results, source_type="gov_rag")
    if web_results:
        citations += docs_to_citations(web_results, source_type="web_search")

    trace.append(
        {"agent": "citation_agent", "action": "synthesize", "detail": f"citations={len(citations)}"}
    )

    return {
        "final_answer": answer,
        "citations": [c.model_dump() for c in citations],
        "agent_trace": trace,
    }
