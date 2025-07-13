from fastapi import APIRouter, Request
from fastapi.websockets import WebSocket
from fastapi.responses import StreamingResponse
from typing import Dict, AsyncGenerator
import mcp.types as types
from mcp.server.lowlevel import Server
from mcp.server.sse import SseServerTransport
from knowledge_base.core.entity.knowledge import KnowledgeSource
from knowledge_base.app.api.service.knowledge import add_knowledge, search_knowledge
import json
import asyncio
import uuid

router = APIRouter(
    prefix="/v1/mcp", responses={404: {"description": "Not found url"}}
)

# Create a server instance
server = Server("knowledge-base-mcp-server")

# Store active sessions
active_sessions: Dict[str, Dict] = {}

# tools
@server.list_tools()
async def handle_list_tools() -> list[types.Tool]:
    return [
        types.Tool(
            name="search_knowledge",
            description="Search the knowledge base",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "Search query"},
                    "system_id": {"type": "string", "description": "System ID"}
                },
                "required": ["query", "system_id"]
            }
        ),
        types.Tool(
            name="add_knowledge",
            description="Add knowledge to the knowledge base",
            inputSchema={
                "type": "object",
                "properties": {
                    "items": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "system_id": {"type": "string", "description": "System ID"},
                                "data": {"type": "string", "description": "Data to add"},
                                "metadata": {"type": "object", "description": "Metadata to add"}
                            },
                            "required": ["system_id", "data"]
                        }
                    }
                },
                "required": ["items"]
            }
        )
    ]

@server.call_tool()
async def handle_call_tool(
    name: str, 
    arguments: dict,
) -> list[types.TextContent]:
    if name == "search_knowledge":
        query = arguments.get("query", "")
        system_id = arguments.get("system_id", "")
        result = await search_knowledge(system_id=system_id, query=query)
        return [types.TextContent(type="text", text=str(result))]

    elif name == "add_knowledge":
        items = arguments.get("items", [])
        source_list = [
            KnowledgeSource(
                system_id=item["system_id"],
                data=item["data"],
                metadata=item.get("metadata", {}),
            )
            for item in items
        ]
        await add_knowledge(source_list)
        return [types.TextContent(type="text", text="Success")]

    else:
        raise ValueError(f"Unknown tool: {name}")


# Alternative: Single endpoint approach (newer MCP streamable HTTP)
@router.post("/")
async def handle_mcp_streamable(request: Request):
    """Handle MCP requests with optional streaming response"""
    try:
        body = await request.json()
        method = body.get("method")
        params = body.get("params", {})
        request_id = body.get("id")
        print(method, params, request_id)

        if method == "initialize":
            response = {
                "jsonrpc": "2.0",
                "result": {
                    "protocolVersion": "2024-11-05",
                    "capabilities": {
                        "tools": {"listChanged": True},
                        "resources": {"listChanged": True}
                    },
                    "serverInfo": {
                        "name": "knowledge-base-mcp-server",
                        "version": "0.1.0"
                    }
                },
                "id": request_id
            }
            
        elif method == "tools/list":
            tools = await handle_list_tools()
            response = {
                "jsonrpc": "2.0",
                "result": {
                    "tools": [tool.model_dump() for tool in tools]
                },
                "id": request_id
            }

        elif method == "tools/call":
            name = params.get("name")
            arguments = params.get("arguments", {})
            result = await handle_call_tool(name, arguments)
            response = {
                "jsonrpc": "2.0",
                "result": {
                    "content": [content.model_dump() for content in result]
                },
                "id": request_id
            }
        
        elif method == "notifications/initialized":
            response = {
                "jsonrpc": "2.0",
                "error": {"code": -32601, "message": "Server should not reply notifications"},
                "id": None
            }

        else:
            response = {
                "jsonrpc": "2.0",
                "error": {"code": -32601, "message": f"Method not found: {method}"},
                "id": request_id
            }
        
        return response
        
    except Exception as e:
        return {
            "jsonrpc": "2.0",
            "error": {"code": -32603, "message": f"Internal error: {str(e)}"},
            "id": request_id
        }
