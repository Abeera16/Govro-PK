from fastapi import APIRouter, Depends

from app.auth.jwt_handler import get_current_user
from app.mcp.tools.gov_api_tool import list_service_keys
from app.models.db_models import User

router = APIRouter(prefix="/agents", tags=["agents"])


@router.get("/graph-info")
async def graph_info(current_user: User = Depends(get_current_user)):
    return {
        "nodes": [
            {"name": "supervisor", "description": "Initializes and orchestrates the run"},
            {"name": "router", "description": "Classifies the query into a service category"},
            {"name": "clarification_agent", "description": "Human-in-the-loop clarification when ambiguous"},
            {"name": "retrieval_agent", "description": "RAG search over ChromaDB gov document index"},
            {"name": "fallback_agent", "description": "Tavily web search fallback for low-confidence retrieval"},
            {"name": "citation_agent", "description": "Synthesizes grounded answer with citations"},
        ],
        "edges": [
            ["supervisor", "router"],
            ["router", "clarification_agent"],
            ["clarification_agent", "retrieval_agent (or END if clarification needed)"],
            ["retrieval_agent", "citation_agent (or fallback_agent if low confidence)"],
            ["fallback_agent", "citation_agent"],
            ["citation_agent", "END"],
        ],
    }


@router.get("/services")
async def services(current_user: User = Depends(get_current_user)):
    return {"services": await list_service_keys()}
