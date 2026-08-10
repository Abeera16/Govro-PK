from functools import lru_cache

from langgraph.graph import END, StateGraph

from app.agents.nodes.citation_agent import citation_node
from app.agents.nodes.clarification_agent import clarification_node
from app.agents.nodes.fallback_agent import fallback_node
from app.agents.nodes.retrieval_agent import retrieval_node, should_fallback_to_web
from app.agents.nodes.router import router_node
from app.agents.nodes.supervisor import route_after_clarification, supervisor_node
from app.agents.state import AgentState


@lru_cache
def build_graph():
    graph = StateGraph(AgentState)

    graph.add_node("supervisor", supervisor_node)
    graph.add_node("router", router_node)
    graph.add_node("clarification_agent", clarification_node)
    graph.add_node("retrieval_agent", retrieval_node)
    graph.add_node("fallback_agent", fallback_node)
    graph.add_node("citation_agent", citation_node)

    graph.set_entry_point("supervisor")
    graph.add_edge("supervisor", "router")
    graph.add_edge("router", "clarification_agent")

    graph.add_conditional_edges(
        "clarification_agent",
        route_after_clarification,
        {
            "end_for_clarification": END,
            "retrieval_agent": "retrieval_agent",
        },
    )

    graph.add_conditional_edges(
        "retrieval_agent",
        should_fallback_to_web,
        {
            "citation_agent": "citation_agent",
            "fallback_agent": "fallback_agent",
        },
    )

    graph.add_edge("fallback_agent", "citation_agent")
    graph.add_edge("citation_agent", END)

    return graph.compile()


async def run_agent_graph(
    user_query: str,
    history: list[dict],
    conversation_id: str,
    clarification_answer: str | None = None,
) -> dict:
    app = build_graph()
    initial_state: AgentState = {
        "messages": history,
        "conversation_id": conversation_id,
        "user_query": user_query,
        "clarification_answer": clarification_answer,
        "agent_trace": [],
    }
    result = await app.ainvoke(initial_state)
    return result
