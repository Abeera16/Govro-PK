from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.agents.graph import run_agent_graph
from app.auth.jwt_handler import get_current_user
from app.core.database import get_db
from app.core.logging_config import logger
from app.memory.conversation_memory import (
    get_or_create_conversation,
    load_history,
    maybe_set_title,
    save_message,
)
from app.models.db_models import User
from app.models.schemas import AgentStep, ChatRequest, ChatResponse, Citation

router = APIRouter(prefix="/chat", tags=["chat"])


@router.post("", response_model=ChatResponse)
async def chat(
    payload: ChatRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    conversation = await get_or_create_conversation(db, current_user.id, payload.conversation_id)
    await maybe_set_title(db, conversation, payload.message)

    history = await load_history(db, conversation.id)

    await save_message(db, conversation.id, "user", payload.message)

    try:
        result = await run_agent_graph(
            user_query=payload.message,
            history=history,
            conversation_id=conversation.id,
            clarification_answer=payload.clarification_answer,
        )
    except Exception as exc:  # noqa: BLE001
        logger.exception("Agent graph execution failed")
        await db.commit()
        raise HTTPException(status_code=500, detail="Agent workflow failed. Please try again.") from exc

    if result.get("needs_clarification") and not payload.clarification_answer:
        assistant_text = result.get("clarification_question", "Could you clarify your request?")
        msg = await save_message(
            db, conversation.id, "assistant", assistant_text, agent_trace=result.get("agent_trace", [])
        )
        await db.commit()
        return ChatResponse(
            conversation_id=conversation.id,
            message_id=msg.id,
            answer=assistant_text,
            requires_clarification=True,
            clarification_question=assistant_text,
            citations=[],
            agent_trace=[AgentStep(**t) for t in result.get("agent_trace", [])],
        )

    answer = result.get("final_answer", "I could not generate an answer.")
    citations = result.get("citations", [])

    msg = await save_message(
        db,
        conversation.id,
        "assistant",
        answer,
        citations=citations,
        agent_trace=result.get("agent_trace", []),
    )
    await db.commit()

    return ChatResponse(
        conversation_id=conversation.id,
        message_id=msg.id,
        answer=answer,
        requires_clarification=False,
        citations=[Citation(**c) for c in citations],
        agent_trace=[AgentStep(**t) for t in result.get("agent_trace", [])],
    )
