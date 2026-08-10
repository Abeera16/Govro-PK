from app.agents.llm_factory import get_chat_model
from app.agents.prompts import ROUTER_SYSTEM_PROMPT
from app.agents.state import AgentState
from app.core.logging_config import logger

VALID_CATEGORIES = {
    "passport", "nadra_cnic", "driving_license", "tax_filing",
    "scholarship", "utility_complaint", "legal_aid", "health", "general",
}


async def router_node(state: AgentState) -> dict:
    llm = get_chat_model(temperature=0.0)
    messages = [
        {"role": "system", "content": ROUTER_SYSTEM_PROMPT},
        {"role": "user", "content": state["user_query"]},
    ]
    try:
        response = await llm.ainvoke(messages)
        category = response.content.strip().lower()
        if category not in VALID_CATEGORIES:
            category = "general"
    except Exception as exc:  # noqa: BLE001
        logger.error(f"Router node failed, defaulting to 'general': {exc}")
        category = "general"

    trace = state.get("agent_trace", [])
    trace.append({"agent": "router", "action": "classify", "detail": f"category={category}"})
    return {"category": category, "agent_trace": trace}
