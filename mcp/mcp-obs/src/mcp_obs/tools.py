"""Tool schemas, handlers, and registry for the observability MCP server."""

from __future__ import annotations

from collections.abc import Awaitable, Callable
from dataclasses import dataclass

from mcp.types import Tool
from pydantic import BaseModel, Field

from mcp_obs.client import ObservabilityClient


ToolPayload = BaseModel | list[BaseModel]
ToolHandler = Callable[[ObservabilityClient, BaseModel], Awaitable[ToolPayload]]


@dataclass(frozen=True, slots=True)
class ToolSpec:
    name: str
    description: str
    model: type[BaseModel]
    handler: ToolHandler

    def as_tool(self) -> Tool:
        schema = self.model.model_json_schema()
        schema.pop("$defs", None)
        schema.pop("title", None)
        return Tool(name=self.name, description=self.description, inputSchema=schema)


class String(BaseModel):
    """A simple string input."""
    value: str = Field(default_factory(str)


class LogsSearchQuery(BaseModel):
    """Query for searching logs."""
    logs_query: str = Field(
        ..., 
        description="LogsQL query string (e.g., '_time:1h service.name:\"Learning Management Service\" severity:ERROR')"
    )
    limit: int = Field(
        default=100, 
        ge=1, 
        description="Maximum number of log entries to return (default 100)"
    )
    start: str | None = Field(
        default=None, 
        description="Start time filter (e.g., '1h', '2024-01-01T00:00:00Z')"
    )
    end: str | None = Field(
        default=None, 
        description="End time filter"
    )


class LogsErrorCountQuery(BaseModel):
    """Query for counting errors."""
    service: str | None = Field(
        default=None, 
        description="Service name to filter (e.g., 'Learning Management Service')"
    )
    time_window: str = Field(
        default="1h", 
        description="Time window (e.g., '1h', '10m', '24h')"
    )


class TracesListQuery(BaseModel):
    """Query for listing traces."""
    service: str | None = Field(
        default="Learning Management Service", 
        description="Service name to filter"
    )
    limit: int = Field(
        default=100, 
        ge=1, 
        description="Maximum number of traces to return (default 100)"
    )


class TracesGetQuery(BaseModel):
    """Query for getting a specific trace."""
    trace_id: str = Field(
        ..., 
        description="Trace ID to fetch"
    )


async def _logs_search(client: ObservabilityClient, args: LogsSearchQuery) -> ToolPayload:
    """Search logs using LogsQL."""
    response = await client.logs_search(
        query=args.logs_query,
        limit=args.limit,
        start=args.start,
        end=args.end,
    )
    response.raise_for_status()
    data = response.json()
    return data.get("data", [])


async def _logs_error_count(client: ObservabilityClient, args: LogsErrorCountQuery) -> ToolPayload:
    """Count errors per service over a time window."""
    response = await client.logs_error_count(
        service=args.service,
        time_window=args.time_window,
    )
    response.raise_for_status()
    data = response.json()
    
    # Process to get error counts per service
    errors_by_service = {}
    for entry in data.get("data", []):
        service_name = entry.get("service", {}).get("name", "unknown")
        if service_name in errors_by_service:
            errors_by_service[service_name] += 1
        else:
            errors_by_service[service_name] = 1
    
    # Return as a list of dicts for consistency
    result = [{"service": svc, "error_count": count} for svc, count in errors_by_service.items()]
    return result


async def _traces_list(client: ObservabilityClient, args: TracesListQuery) -> ToolPayload:
    """List recent traces for a service."""
    response = await client.traces_list(
        service=args.service,
        limit=args.limit,
    )
    response.raise_for_status()
    return response.json().get("data", [])


async def _traces_get(client: ObservabilityClient, args: TracesGetQuery) -> ToolPayload:
    """Get a specific trace by ID."""
    response = await client.traces_get(trace_id=args.trace_id)
    response.raise_for_status()
    return response.json().get("data", {})


TOOL_SPECS = (
    ToolSpec(
        "mcp_obs_logs_search",
        "Search logs using LogsQL queries.",
        LogsSearchQuery,
        _logs_search,
    ),
    ToolSpec(
        "mcp_obs_logs_error_count",
        "Count error-level logs per service over a time window.",
        LogsErrorCountQuery,
        _logs_error_count,
    ),
    ToolSpec(
        "mcp_obs_traces_list",
        "List recent traces for a service.",
        TracesListQuery,
        _traces_list,
    ),
    ToolSpec(
        "mcp_obs_traces_get",
        "Get a specific trace by ID.",
        TracesGetQuery,
        _traces_get,
    ),
)
TOOLS_BY_NAME = {spec.name: spec for spec in TOOL_SPECS}