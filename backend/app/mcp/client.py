"""
Lightweight in-process MCP client wrapper.

For this deployment the LangGraph agents run in the same Python process as the
FastAPI app, so rather than spawning a separate stdio/subprocess MCP client per
request, we call the underlying tool implementations directly through the same
interface names the MCP server exposes. This keeps a single source of truth for
tool schemas/behaviour (app/mcp/tools/*) while remaining swappable for a real
stdio/socket MCP client (see `app/mcp/server.py`) in a distributed deployment
(the `mcp-server` container is provided for that purpose).
"""
from app.core.logging_config import logger
from app.mcp.tools.gov_api_tool import gov_lookup, list_service_keys
from app.mcp.tools.rag_tool import rag_search
from app.mcp.tools.tavily_tool import tavily_search


class MCPToolClient:
    """Uniform async interface used by LangGraph agent nodes to call MCP tools."""

    async def call(self, tool_name: str, **kwargs) -> object:
        logger.info(f"MCP client -> tool={tool_name} kwargs={kwargs}")
        if tool_name == "rag_search":
            return await rag_search(**kwargs)
        if tool_name == "web_search":
            return await tavily_search(**kwargs)
        if tool_name == "gov_lookup":
            return await gov_lookup(**kwargs)
        if tool_name == "list_services":
            return await list_service_keys()
        raise ValueError(f"Unknown MCP tool: {tool_name}")


mcp_client = MCPToolClient()
