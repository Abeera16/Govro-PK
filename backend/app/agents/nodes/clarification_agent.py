import json

from app.agents.llm_factory import get_chat_model
from app.agents.prompts import CLARIFICATION_SYSTEM_PROMPT
from app.agents.state import AgentState
from app.core.logging_config import logger


async def clarification_node(state: AgentState) -> dict:
    trace = state.get("agent_trace", [])

    # If the user already answered a prior clarification question, skip re-asking.
    if state.get("clarification_answer"):
        trace.append({"agent": "clarification_agent", "action": "skip", "detail": "answer already provided"})
        return {"needs_clarification": False, "agent_trace": trace}

    llm = get_chat_model(temperature=0.0)
    messages = [
        {"role": "system", "content": CLARIFICATION_SYSTEM_PROMPT},
        {"role": "user", "content": f"Category: {state.get('category')}\nQuery: {state['user_query']}"},
    ]
    try:
        response = await llm.ainvoke(messages)
        parsed = json.loads(response.content.strip().strip("`").removeprefix("json"))
        needs = bool(parsed.get("needs_clarification", False))
        question = parsed.get("question", "")
    except Exception as exc:  # noqa: BLE001
        logger.warning(f"Clarification parse failed, assuming no clarification needed: {exc}")
        needs, question = False, ""

    trace.append(
        {"agent": "clarification_agent", "action": "evaluate", "detail": f"needs_clarification={needs}"}
    )
    return {"needs_clarification": needs, "clarification_question": question, "agent_trace": trace}
