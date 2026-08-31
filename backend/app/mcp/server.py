"""
GovroPK MCP Server.

Exposes government-service tools (web search, structured gov lookups, RAG search
over ChromaDB) over the Model Context Protocol so any MCP-compatible client
(including our own LangGraph agents) can call them uniformly.

Run with:  python -m app.mcp.server
"""
import asyncio

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import TextContent, Tool

from app.core.logging_config import configure_logging, logger
from app.mcp.tools.gov_api_tool import gov_lookup, list_service_keys
from app.mcp.tools.rag_tool import rag_search
from app.mcp.tools.tavily_tool import tavily_search

configure_logging()
server = Server("govropk-mcp-server")


@server.list_tools()
async def list_tools() -> list[Tool]:
    return [
        Tool(
            name="rag_search",
            description="Search official Pakistani government documents indexed in ChromaDB "
                        "(passport, NADRA, driving license, tax, scholarship, health, legal aid, "
                        "utility complaint info) for relevant, citable passages.",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {"type": "string"},
                    "k": {"type": "integer", "default": 5},
                    "category": {"type": "string", "description": "optional category filter"},
                },
                "required": ["query"],
            },
        ),
        Tool(
            name="web_search",
            description="Search the live web (Tavily) scoped to official Pakistani government "
                        "domains, for information not yet present in the RAG corpus.",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {"type": "string"},
                    "max_results": {"type": "integer", "default": 5},
                },
                "required": ["query"],
            },
        ),
        Tool(
            name="gov_lookup",
            description="Structured lookup of a known government service (fees, documents "
                        "required, processing time, department, portal URL). "
                        f"Valid service_key values include: passport, nadra_cnic, driving_license, "
                        f"tax_filing, scholarship, utility_complaint, legal_aid, health.",
            inputSchema={
                "type": "object",
                "properties": {"service_key": {"type": "string"}},
                "required": ["service_key"],
            },
        ),
        Tool(
            name="list_services",
            description="List all structured government service keys available via gov_lookup.",
            inputSchema={"type": "object", "properties": {}},
        ),
    ]


@server.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    logger.info(f"MCP tool call: {name} args={arguments}")
    try:
        if name == "rag_search":
            result = await rag_search(
                query=arguments["query"],
                k=arguments.get("k", 5),
                category=arguments.get("category"),
            )
        elif name == "web_search":
            result = await tavily_search(
                query=arguments["query"], max_results=arguments.get("max_results", 5)
            )
        elif name == "gov_lookup":
            result = await gov_lookup(arguments["service_key"])
        elif name == "list_services":
            result = await list_service_keys()
        else:
            return [TextContent(type="text", text=f"Unknown tool: {name}")]

        return [TextContent(type="text", text=str(result))]
    except Exception as exc:  # noqa: BLE001
        logger.exception(f"MCP tool '{name}' failed")
        return [TextContent(type="text", text=f"ERROR: {exc}")]


async def main() -> None:
    logger.info("Starting GovroPK MCP server (stdio transport)")
    async with stdio_server() as (read_stream, write_stream):
        await server.run(read_stream, write_stream, server.create_initialization_options())


if __name__ == "__main__":
    asyncio.run(main())
