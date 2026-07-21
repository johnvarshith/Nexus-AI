from pydantic import BaseModel, Field
from typing import Dict, Any

class FetchLogsInput(BaseModel):
    service: str = Field(description="Microservice name (e.g., checkout-service)")
    lines: int = Field(default=50, description="Number of log lines")

class QueryRunbookInput(BaseModel):
    keyword: str = Field(description="Error keyword to search in runbooks")

# Simulated handlers (import your actual logic here)
async def fetch_logs_tool(service: str, lines: int = 50) -> str:
    from backend.agents.researcher import mock_fetch_logs
    return mock_fetch_logs(service)

async def query_runbook_tool(keyword: str) -> str:
    from backend.agents.researcher import MOCK_RUNBOOKS
    for key, advice in MOCK_RUNBOOKS.items():
        if key in keyword.lower():
            return advice
    return "No runbook found."

# MCP Registry – this matches the MCP standard
TOOL_REGISTRY: Dict[str, Dict[str, Any]] = {
    "fetch_logs": {
        "name": "fetch_logs",
        "description": "Fetches recent error logs for a microservice.",
        "input_schema": FetchLogsInput.model_json_schema(),
        "handler": fetch_logs_tool
    },
    "query_runbook": {
        "name": "query_runbook",
        "description": "Searches historical runbooks for known fixes.",
        "input_schema": QueryRunbookInput.model_json_schema(),
        "handler": query_runbook_tool
    }
}

def list_tools() -> list:
    return [
        {"name": t["name"], "description": t["description"], "inputSchema": t["input_schema"]}
        for t in TOOL_REGISTRY.values()
    ]

async def call_tool(name: str, arguments: dict) -> str:
    if name not in TOOL_REGISTRY:
        return f"Tool '{name}' not found."
    handler = TOOL_REGISTRY[name]["handler"]
    return await handler(**arguments)